"""v3_lead_score: the independent decide2 for F5 `gen3_lead_score` (yn2b SPEC 4.1, 8.1).

Written by builder D from the SPEC (sections 4, 5/F5, 8) and from the RENDERED rows only. It never imports or reads
`gen3_lead_score.py` (the generator and its `decide`) and never reads a row's gold, trace or shortcut fields.

What it does, per raw row (the `yn2b_raw` format):
  1. parse_state(state)        -> Doc: the rubric text, scoring date, lead record, web form, CRM record and the
                                   event stream (activity, messages, rep notes, notes), from any of the 14 surfaces
                                   (json, kv, markdown, prose, log x4, email, chat, table x4).
  2. parse_rubric(title, rules) -> Rubric: every numbered rule is matched by a strict pattern; an unknown sentence
                                   raises ParseError (nothing is silently skipped). Amendments in force on the
                                   scoring date are applied, and their "from" value is asserted.
  3. evaluate(doc, rubric)     -> Result: score (points / criteria / gates / weighted points), level, sales-ready.
  4. decide2_row(row)          -> the gold string: a level text (score rows), 'yes'/'no' (yes/no rows) or one of
                                   the two JB-letter option strings.

Only the rendered row is used: state, instructions, options. The yes/no card (meta.defs) is only checked by the
report (`card_report`) to confirm what yes means; decide2 itself never reads meta or gold.

Readings. Where the rubric text leaves room, decide2 uses DEFAULT_READINGS (chosen from the rubric text and the
card before any comparison with the gold). `sensitivity` re-runs every row under each alternative reading and
lists the rows whose answer depends on it: that is the ambiguity report.

CLI (from lean/):
  ../.venv/bin/python golden_src/gen3/v3_lead_score.py            agreement, structure, sensitivity, cards (prints)
  ../.venv/bin/python golden_src/gen3/v3_lead_score.py --quick    agreement only
  ../.venv/bin/python golden_src/gen3/v3_lead_score.py --write    also writes yn2b/v3_lead_score_agreement.json and
                                                                  appends its sha256 to MANIFEST_yn2b.jsonl
Tests: yn2b/tests/test_v3_lead_score_{scorer,parse,written}.py (+ v3f5_helpers.py).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
DEFS = LEAN / "data" / "v14_parts" / "yn2b_defs"
KEY = "gen3_lead_score"


class ParseError(Exception):
    """The rendered row could not be read unambiguously. decide2 never guesses."""


# ------------------------------------------------------------------------------------------------ small helpers
_TS = re.compile(r"^(\d{4}-\d\d-\d\d)T(\d\d):(\d\d):(\d\d)Z$")
_TS_EMAIL = re.compile(r"^(\d{4}-\d\d-\d\d) (\d\d):(\d\d) UTC$")
_DATE = re.compile(r"^\d{4}-\d\d-\d\d$")


def to_int(s: str) -> int:
    s = s.strip()
    if not re.fullmatch(r"\d{1,3}(,\d{3})*|\d+", s):
        raise ParseError(f"not an integer: {s!r}")
    return int(s.replace(",", ""))


def to_date(s: str) -> dt.date:
    s = s.strip()
    if not _DATE.match(s):
        raise ParseError(f"not a date: {s!r}")
    return dt.date.fromisoformat(s)


def to_ts(s: str) -> dt.datetime:
    s = s.strip()
    m = _TS.match(s)
    if m:
        return dt.datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:{m.group(3)}:{m.group(4)}")
    m = _TS_EMAIL.match(s)
    if m:
        return dt.datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:{m.group(3)}:00")
    raise ParseError(f"not a timestamp: {s!r}")


def split_list(s: str) -> list[str]:
    """'a, b and c' / 'a, b or c' / 'a' -> items."""
    s = s.strip()
    parts = re.split(r", | and | or ", s)
    return [p.strip() for p in parts if p.strip()]


# ------------------------------------------------------------------------------------------------ the parsed state
@dataclass
class Event:
    kind: str                 # activity | message | rep_note | note
    time: dt.datetime
    text: str                 # activity string, message text, note text
    who: str | None = None    # sender / rep (messages, rep notes)
    lead: str | None = None   # lead id (activity)


@dataclass
class Doc:
    title: str
    rules: list[str]
    scoring_date: dt.date
    lead: dict
    form: dict
    crm: dict
    events: list[Event]
    extra: dict = field(default_factory=dict)   # fields that carry no scoring meaning (e.g. an enrichment note)


LEAD_KEYS = {"Lead id", "Company", "Company domain", "Region", "Current customer", "Primary contact",
             "Primary contact title", "Primary contact email", "Other contact", "Other contact title",
             "Other contact email", "Enrichment lookup", "Lead created"}
FORM_KEYS = {"Submitted by", "Submitted at", "Company size range", "Budget status", "Budget amount", "Target date",
             "Main problem"}
CRM_KEYS = {"Owner", "Stage", "Recorded score", "Recorded level", "Score reason"}
NOTE_KEYS = {"Enrichment note"}   # an untrusted free-text field; never scored


def _put(d: dict, k: str, v: str, where: str):
    if k in d and d[k] != v:
        raise ParseError(f"duplicate field {k!r} in {where}")
    d[k] = v


def _field(doc_parts: dict, section: str, k: str, v: str):
    k = k.strip()
    v = v.strip()
    if k in NOTE_KEYS:
        doc_parts["extra"].setdefault(k, []).append(v)
        return
    table = {"lead": LEAD_KEYS, "form": FORM_KEYS, "crm": CRM_KEYS}[section]
    if k not in table:
        raise ParseError(f"unknown field {k!r} in section {section}")
    _put(doc_parts[section], k, v, section)


# ---- json ----
_JSON_SCHEMAS = {
    # top key -> role
    "date_scored": "date", "as_of": "date", "scoring_date": "date",
    "qualification_rubric": "rubric", "scoring_rubric": "rubric", "rubric": "rubric",
    "prospect": "lead", "lead_record": "lead", "lead": "lead",
    "inbound_form": "form", "form_submission": "form", "web_form": "form",
    "events": "activity", "activity_log": "activity", "activity": "activity",
    "prospect_messages": "messages", "correspondence": "messages", "messages": "messages",
    "rep_call_notes": "rep_notes", "sales_notes": "rep_notes", "rep_notes": "rep_notes",
    "crm_fields": "crm", "crm_record": "crm", "crm": "crm",
}


def _parse_json(state: str) -> dict:
    d = json.loads(state)
    parts = {"title": None, "rules": None, "date": None, "lead": {}, "form": {}, "crm": {}, "events": [],
             "extra": {}}
    for k, v in d.items():
        role = _JSON_SCHEMAS.get(k)
        if role is None:
            raise ParseError(f"unknown json key {k!r}")
        if role == "date":
            parts["date"] = v
        elif role == "rubric":
            if set(v) != {"title", "rules"}:
                raise ParseError(f"rubric keys {sorted(v)}")
            parts["title"], parts["rules"] = v["title"], list(v["rules"])
        elif role in ("lead", "form", "crm"):
            for kk, vv in v.items():
                _field(parts, role, kk, vv)
        elif role == "activity":
            for e in v:
                if set(e) != {"time", "lead", "activity"}:
                    raise ParseError(f"activity keys {sorted(e)}")
                parts["events"].append(Event("activity", to_ts(e["time"]), e["activity"], lead=e["lead"]))
        elif role == "messages":
            for e in v:
                if set(e) != {"time", "from", "text"}:
                    raise ParseError(f"message keys {sorted(e)}")
                parts["events"].append(Event("message", to_ts(e["time"]), e["text"], who=e["from"]))
        elif role == "rep_notes":
            for e in v:
                if set(e) != {"time", "rep", "note"}:
                    raise ParseError(f"rep note keys {sorted(e)}")
                parts["events"].append(Event("rep_note", to_ts(e["time"]), e["note"], who=e["rep"]))
    return parts


# ---- kv ----
_KV_ROLE = {"scoring_date": "date", "as_of": "date", "date_scored": "date"}


def _parse_kv(state: str) -> dict:
    parts = {"title": None, "rules": [], "date": None, "lead": {}, "form": {}, "crm": {}, "events": [],
             "extra": {}}
    rows: dict[tuple, dict] = {}
    order: list[tuple] = []
    for line in state.split("\n"):
        if not line.strip():
            continue
        if ": " not in line:
            raise ParseError(f"kv line without ': ' {line!r}")
        k, v = line.split(": ", 1)
        segs = k.split(".")
        role = _KV_ROLE.get(k) or _JSON_SCHEMAS.get(segs[0])
        if role is None:
            raise ParseError(f"unknown kv key {k!r}")
        if role == "date":
            parts["date"] = v
        elif role == "rubric":
            if segs[1:] == ["title"]:
                parts["title"] = v
            elif segs[1] == "rules" and len(segs) == 3:
                if not v.startswith(f"{segs[2]}. "):
                    raise ParseError(f"rule number mismatch {line!r}")
                parts["rules"].append(v)
            else:
                raise ParseError(f"rubric kv {k!r}")
        elif role in ("lead", "form", "crm"):
            _field(parts, role, ".".join(segs[1:]), v)
        else:
            if len(segs) != 3 or not segs[1].isdigit():
                raise ParseError(f"list kv {k!r}")
            key = (role, int(segs[1]))
            if key not in rows:
                rows[key] = {}
                order.append(key)
            rows[key][segs[2]] = v
    for key in order:
        role, e = key[0], rows[key]
        if role == "activity":
            parts["events"].append(Event("activity", to_ts(e["time"]), e["activity"], lead=e["lead"]))
        elif role == "messages":
            parts["events"].append(Event("message", to_ts(e["time"]), e["text"], who=e["from"]))
        elif role == "rep_notes":
            parts["events"].append(Event("rep_note", to_ts(e["time"]), e["note"], who=e["rep"]))
    return parts


# ---- the text surfaces ----
_HEADERS = {
    "Lead record": "lead", "Web form": "form", "CRM record": "crm", "Activity": "activity", "Messages": "messages",
    "Rep notes": "rep_notes", "Chat transcript": "chat", "Emails (oldest first)": "email",
    "Event log (oldest first)": "log", "Event log (newest first)": "log", "Event log (not in time order)": "log",
    "Event log (grouped by source, oldest first within each group)": "log_grouped", "Scoring date": "date",
}
_GROUP = {"== activity ==": "activity", "== message ==": "message", "== rep note ==": "rep_note"}
_NAME = r"[A-Z][a-z]+ [A-Z][a-z]+"


def _msg_line(s: str) -> tuple[str, str]:
    m = re.match(rf"^({_NAME}): (.*)$", s)
    if not m:
        raise ParseError(f"not 'Name: text': {s!r}")
    return m.group(1), m.group(2)


def _table_rows(lines: list[str]) -> list[list[str]] | None:
    """csv / md / pipe / records table -> list of cell lists (header first); None if these lines are no table."""
    if not lines:
        return None
    if lines[0] == "Table (first row is the header):":
        lines = lines[1:]
        out = []
        for ln in lines:
            if not (ln.startswith("| ") and ln.endswith(" |")):
                raise ParseError(f"pipe row {ln!r}")
            out.append([c.strip() for c in ln[2:-2].split(" | ")])
        return out
    if lines[0].startswith("| ") and len(lines) > 1 and re.fullmatch(r"\|(---\|)+", lines[1]):
        out = []
        for i, ln in enumerate(lines):
            if i == 1:
                continue
            if not (ln.startswith("| ") and ln.endswith(" |")):
                raise ParseError(f"md row {ln!r}")
            out.append([c.strip() for c in ln[2:-2].split(" | ")])
        return out
    if lines[0] in ("Field,Value", "Entry,Time,Lead id,Activity"):
        return [r for r in csv.reader(io.StringIO("\n".join(lines)))]
    if lines[0].startswith("- Field: ") or lines[0].startswith("- Entry: "):
        out = []
        hdr = None
        for ln in lines:
            if not ln.startswith("- "):
                raise ParseError(f"record row {ln!r}")
            cells = ln[2:].split("; ")
            kv = [c.split(": ", 1) for c in cells]
            if any(len(x) != 2 for x in kv):
                raise ParseError(f"record cells {ln!r}")
            h = [x[0] for x in kv]
            if hdr is None:
                hdr = h
                out.append(hdr)
            elif h != hdr:
                raise ParseError(f"record header drift {ln!r}")
            out.append([x[1] for x in kv])
        return out
    return None


def _fields_from_lines(parts: dict, section: str, lines: list[str]):
    tab = _table_rows(lines)
    if tab is not None:
        if tab[0] != ["Field", "Value"]:
            raise ParseError(f"field table header {tab[0]}")
        for r in tab[1:]:
            if len(r) != 2:
                raise ParseError(f"field row {r}")
            _field(parts, section, r[0], r[1])
        return
    for ln in lines:
        s = ln[2:] if ln.startswith("- ") else ln
        if ": " not in s:
            raise ParseError(f"field line {ln!r}")
        k, v = s.split(": ", 1)
        _field(parts, section, k, v)


def _activity_from_lines(parts: dict, lines: list[str]):
    tab = _table_rows(lines)
    if tab is not None:
        if tab[0] != ["Entry", "Time", "Lead id", "Activity"]:
            raise ParseError(f"activity table header {tab[0]}")
        for r in tab[1:]:
            if len(r) != 4:
                raise ParseError(f"activity row {r}")
            parts["events"].append(Event("activity", to_ts(r[1]), r[3], lead=r[2]))
        return
    for ln in lines:
        m = re.match(r"^- (\S+) \| (L\d+) \| (.*)$", ln)
        if m:
            parts["events"].append(Event("activity", to_ts(m.group(1)), m.group(3), lead=m.group(2)))
            continue
        m = re.match(r"^On (\S+), lead (L\d+): (.*)$", ln)
        if m:
            parts["events"].append(Event("activity", to_ts(m.group(1)), m.group(3), lead=m.group(2)))
            continue
        _loose_line(parts, ln, "activity")


def _loose_line(parts: dict, ln: str, where: str):
    """A line that is not a row of its section: only an untrusted enrichment note may appear this way."""
    s = ln[2:] if ln.startswith("- ") else ln
    if s.startswith("Enrichment note: "):
        parts["extra"].setdefault("Enrichment note", []).append(s[len("Enrichment note: "):])
        return
    raise ParseError(f"unreadable line in {where}: {ln!r}")


def _notes_from_lines(parts: dict, lines: list[str], kind: str):
    for ln in lines:
        m = re.match(r"^- (\S+) \| (.*)$", ln)
        if m and not re.match(r"^L\d+ \| ", m.group(2)):
            who, text = _msg_line(m.group(2))
            parts["events"].append(Event(kind, to_ts(m.group(1)), text, who=who))
            continue
        if m:   # '- T | Lnnn | note: ...' planted inside a notes/messages list: an activity-log entry
            m2 = re.match(r"^- (\S+) \| (L\d+) \| (.*)$", ln)
            parts["events"].append(Event("activity", to_ts(m2.group(1)), m2.group(3), lead=m2.group(2)))
            continue
        m = re.match(rf'^On (\S+), ({_NAME}) wrote: "(.*)"$', ln)
        if m and kind == "message":
            parts["events"].append(Event("message", to_ts(m.group(1)), m.group(3), who=m.group(2)))
            continue
        m = re.match(rf'^On (\S+), rep ({_NAME}) noted: "(.*)"$', ln)
        if m and kind == "rep_note":
            parts["events"].append(Event("rep_note", to_ts(m.group(1)), m.group(3), who=m.group(2)))
            continue
        m = re.match(r"^On (\S+), lead (L\d+): (.*)$", ln)
        if m:
            parts["events"].append(Event("activity", to_ts(m.group(1)), m.group(3), lead=m.group(2)))
            continue
        _loose_line(parts, ln, kind)


def _chat_from_lines(parts: dict, lines: list[str]):
    for ln in lines:
        m = re.match(r"^\[(\S+)\] (.*)$", ln)
        if m:
            who, text = _msg_line(m.group(2))
            parts["events"].append(Event("message", to_ts(m.group(1)), text, who=who))
            continue
        _loose_line(parts, ln, "chat")


def _email_from_block(parts: dict, block: list[str]):
    """Emails: blocks separated by a '----------' line: From/To/Date/Subject, a blank line, the body."""
    text = "\n".join(block).strip("\n")
    if not text:
        return
    for chunk in text.split("\n\n----------\n\n"):
        lines = chunk.split("\n")
        if len(lines) < 6 or not lines[0].startswith("From: ") or not lines[1].startswith("To: ") \
                or not lines[2].startswith("Date: ") or not lines[3].startswith("Subject: ") or lines[4] != "":
            raise ParseError(f"email block {chunk[:120]!r}")
        body = "\n".join(lines[5:])
        if "\n" in body:
            raise ParseError(f"multi-line email body {body!r}")
        parts["events"].append(Event("message", to_ts(lines[2][6:]), body, who=lines[0][6:]))


def _log_from_lines(parts: dict, lines: list[str]):
    for ln in lines:
        m = re.match(r"^(\S+) \[(activity|message|rep note)\] (.*)$", ln)
        if not m:
            _loose_line(parts, ln, "log")
            continue
        t, kind, rest = to_ts(m.group(1)), m.group(2), m.group(3)
        if kind == "activity":
            m2 = re.match(r"^#(L\d+) (.*)$", rest)
            if not m2:
                raise ParseError(f"log activity {ln!r}")
            parts["events"].append(Event("activity", t, m2.group(2), lead=m2.group(1)))
        else:
            who, text = _msg_line(rest)
            parts["events"].append(Event("message" if kind == "message" else "rep_note", t, text, who=who))


def _grouped_from_lines(parts: dict, lines: list[str]):
    cur = None
    for ln in lines:
        if ln in _GROUP:
            cur = _GROUP[ln]
            continue
        if not ln:
            continue
        m = re.match(r"^(\S+Z) (.*)$", ln)
        if not m or cur is None:
            _loose_line(parts, ln, "log_grouped")
            continue
        t, rest = to_ts(m.group(1)), m.group(2)
        if cur == "activity":
            m2 = re.match(r"^#(L\d+) (.*)$", rest)
            if not m2:
                raise ParseError(f"grouped activity {ln!r}")
            parts["events"].append(Event("activity", t, m2.group(2), lead=m2.group(1)))
        else:
            who, text = _msg_line(rest)
            parts["events"].append(Event(cur, t, text, who=who))


def _prose_lead(parts: dict, lines: list[str]):
    """Prose lead record: fixed sentence shapes."""
    for ln in lines:
        m = re.match(r"^Lead record: lead (L\d+) is (.+) \(company domain (\S+)\)\.$", ln)
        if m:
            _field(parts, "lead", "Lead id", m.group(1))
            _field(parts, "lead", "Company", m.group(2))
            _field(parts, "lead", "Company domain", m.group(3))
            continue
        m = re.match(r"^Region: (.+)\. Current customer: (yes|no)\.$", ln)
        if m:
            _field(parts, "lead", "Region", m.group(1))
            _field(parts, "lead", "Current customer", m.group(2))
            continue
        m = re.match(rf"^The primary contact is ({_NAME}), (.+), email (\S+?)\.$", ln)
        if m:
            _field(parts, "lead", "Primary contact", m.group(1))
            _field(parts, "lead", "Primary contact title", m.group(2))
            _field(parts, "lead", "Primary contact email", m.group(3))
            continue
        m = re.match(rf"^Another contact on the account is ({_NAME}), (.+), email (\S+?)\.$", ln)
        if m:
            _field(parts, "lead", "Other contact", m.group(1))
            _field(parts, "lead", "Other contact title", m.group(2))
            _field(parts, "lead", "Other contact email", m.group(3))
            continue
        m = re.match(r"^The enrichment lookup lists (.+)\.$", ln)
        if m:
            _field(parts, "lead", "Enrichment lookup", m.group(1))
            continue
        m = re.match(r"^The lead was created on (\S+)\.$", ln)
        if m:
            _field(parts, "lead", "Lead created", m.group(1))
            continue
        m = re.match(r"^Enrichment note: (.*)$", ln)
        if m:
            parts["extra"].setdefault("Enrichment note", []).append(m.group(1))
            continue
        raise ParseError(f"prose lead line {ln!r}")


def _prose_form(parts: dict, lines: list[str]):
    for ln in lines:
        m = re.match(rf"^Web form: ({_NAME}) submitted the web form at (\S+)\.$", ln)
        if m:
            _field(parts, "form", "Submitted by", m.group(1))
            _field(parts, "form", "Submitted at", m.group(2))
            continue
        m = re.match(r"^([A-Z][a-z]+(?: [a-z]+)*): (.*)\.$", ln)
        if m and m.group(1) in FORM_KEYS:
            _field(parts, "form", m.group(1), m.group(2))
            continue
        raise ParseError(f"prose form line {ln!r}")


def _prose_crm(parts: dict, lines: list[str]):
    for ln in lines:
        m = re.match(rf"^CRM record: the owner is ({_NAME}) and the stage is (\S+?)\.$", ln)
        if m:
            _field(parts, "crm", "Owner", m.group(1))
            _field(parts, "crm", "Stage", m.group(2))
            continue
        m = re.match(r"^(Recorded score|Recorded level|Score reason): (.*)$", ln)
        if m:
            v = m.group(2)
            if v.endswith("."):
                v = v[:-1]
            _field(parts, "crm", m.group(1), v)
            continue
        m = re.match(r"^Enrichment note: (.*)$", ln)
        if m:
            parts["extra"].setdefault("Enrichment note", []).append(m.group(1))
            continue
        raise ParseError(f"prose crm line {ln!r}")


def _parse_text(state: str) -> dict:
    parts = {"title": None, "rules": [], "date": None, "lead": {}, "form": {}, "crm": {}, "events": [],
             "extra": {}}
    lines = state.split("\n")
    first = lines[0]
    parts["title"] = first[3:] if first.startswith("## ") else first
    i = 1
    while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
        parts["rules"].append(lines[i])
        i += 1
    # sections
    sections: list[tuple[str, str, list[str]]] = []   # (role, header line, body lines)
    cur = None
    for ln in lines[i:]:
        hdr = None
        if ln.startswith("## "):
            hdr = ln[3:]
        elif ln.endswith(":") and ln[:-1] in _HEADERS:
            hdr = ln[:-1]
        if hdr is not None:
            if hdr not in _HEADERS:
                raise ParseError(f"unknown section {ln!r}")
            cur = [_HEADERS[hdr], ln, []]
            sections.append(cur)
            continue
        m = re.match(r"^Scoring date: (\S+?)\.?$", ln)
        if m:
            parts["date"] = m.group(1)
            cur = None
            continue
        if ln.startswith("Lead record: lead "):          # prose sections open with a sentence
            cur = ["prose_lead", ln, [ln]]
            sections.append(cur)
            continue
        if ln.startswith("Web form: ") and " submitted the web form at " in ln:
            cur = ["prose_form", ln, [ln]]
            sections.append(cur)
            continue
        if ln.startswith("CRM record: the owner is "):
            cur = ["prose_crm", ln, [ln]]
            sections.append(cur)
            continue
        if cur is None:
            if ln.strip():
                raise ParseError(f"text outside any section {ln!r}")
            continue
        cur[2].append(ln)
    for role, hdr, body in sections:
        if role == "email":
            _email_from_block(parts, body)
            continue
        if role == "log_grouped":
            _grouped_from_lines(parts, body)
            continue
        # drop the trailing blank lines that separate sections (blank lines inside a section are an error)
        while body and not body[-1].strip():
            body.pop()
        if any(not b.strip() for b in body):
            raise ParseError(f"blank line inside section {hdr!r}")
        if role == "date":
            if len(body) != 1:
                raise ParseError("scoring date section")
            parts["date"] = body[0]
        elif role in ("lead", "form", "crm"):
            _fields_from_lines(parts, role, body)
        elif role == "prose_lead":
            _prose_lead(parts, body)
        elif role == "prose_form":
            _prose_form(parts, body)
        elif role == "prose_crm":
            _prose_crm(parts, body)
        elif role == "activity":
            _activity_from_lines(parts, body)
        elif role == "messages":
            _notes_from_lines(parts, body, "message")
        elif role == "rep_notes":
            _notes_from_lines(parts, body, "rep_note")
        elif role == "chat":
            _chat_from_lines(parts, body)
        elif role == "log":
            _log_from_lines(parts, body)
        else:
            raise ParseError(f"role {role}")
    return parts


def parse_state(state: str) -> Doc:
    s = state.lstrip()
    if s.startswith("{"):
        parts = _parse_json(state)
    elif state.startswith("scoring_date: ") or state.startswith("as_of: ") or state.startswith("date_scored: "):
        parts = _parse_kv(state)
    else:
        parts = _parse_text(state)
    if not parts["title"] or not parts["rules"] or not parts["date"]:
        raise ParseError("missing rubric title, rules or scoring date")
    for i, r in enumerate(parts["rules"], 1):
        if not r.startswith(f"{i}. "):
            raise ParseError(f"rule {i} numbering: {r[:40]!r}")
    return Doc(parts["title"], parts["rules"], to_date(parts["date"]), parts["lead"], parts["form"], parts["crm"],
               parts["events"], parts["extra"])


# ------------------------------------------------------------------------------------------------ the rubric
STATUS_WORDS = {"approved budget": "approved", "requested a budget": "requested", "hope to get a budget": "hoped",
                "if we had a budget": "hypothetical"}
_STATUS_SENT = ("Status words: 'approved budget' means approved; 'requested a budget' means requested; "
                "'hope to get a budget' means hoped; 'if we had a budget' means hypothetical. "
                "A monthly amount equals 12 times that amount per year.")
_STATUS_SENT_W = ("Reading budget statements: 'approved budget' = approved; 'requested a budget' = requested; "
                  "'hope to get a budget' = hoped; 'if we had a budget' = hypothetical. "
                  "Monthly and yearly amounts convert at 12 months per year.")


@dataclass
class Window:
    days: int
    inclusive: bool           # True: 'at most N' (exactly N counts); False: 'less than N'

    def ok(self, age: int) -> bool:
        if age < 0:
            raise ParseError("event after the scoring date")
        return age <= self.days if self.inclusive else age < self.days


@dataclass
class Horizon:
    """'on or after the scoring date and at most / fewer than N days after it'."""
    days: int
    inclusive: bool

    def ok(self, diff: int) -> bool:
        return diff >= 0 and (diff <= self.days if self.inclusive else diff < self.days)


@dataclass
class BudgetTest:
    min_annual_x12: int       # the minimum as a yearly amount, in dollars x 12 (exact for monthly and yearly units)
    statuses: tuple           # counting statuses
    rule: int = 0

    def met(self, stmt) -> bool:
        if stmt is None:
            return False
        return stmt["status"] in self.statuses and stmt["annual_x12"] >= self.min_annual_x12


@dataclass
class Rubric:
    archetype: str = ""                       # points | bant | gated | weighted
    rule_kind: dict = field(default_factory=dict)       # rule number -> kind
    rep_target_ok: bool = False               # rep notes giving the target date are evidence
    stmt_window: Window | None = None
    size_source: str = ""                     # form | enrichment
    title_points: dict = field(default_factory=dict)
    size_bands: list = field(default_factory=list)      # (lo, hi|None, points)
    act_points: dict = field(default_factory=dict)
    act_type_max: int | None = None
    act_window: Window | None = None
    act_cap: int | None = None
    unsub_penalty: int | None = None
    budget: BudgetTest | None = None
    budget_points: int = 0
    timeline: Horizon | None = None
    timeline_points: int = 0
    timeline_rule: int = 0
    levels: list = field(default_factory=list)          # level names, ascending
    level_bands: list = field(default_factory=list)     # points / weighted: (lo, hi|None) per level
    count_levels: dict = field(default_factory=dict)    # bant: count -> level index
    gates: list = field(default_factory=list)           # (level index, kind, params)
    base_level: str = ""
    overrides: list = field(default_factory=list)       # ('ceiling'|'floor', level index)
    disq: list = field(default_factory=list)            # (kind, params)
    disq_level: str = ""
    ready_level: str = ""
    need_list: list = field(default_factory=list)
    auth_list: list = field(default_factory=list)
    bands: dict = field(default_factory=dict)           # seniority band letter -> titles
    # weighted
    fit_bands: list = field(default_factory=list)
    role_score: dict = field(default_factory=dict)
    eng_bands: list = field(default_factory=list)
    eng_rules: tuple = ()
    wbudget: dict = field(default_factory=dict)
    wtimeline: list = field(default_factory=list)       # (max days, score) ascending
    wtimeline_other: int = 0
    weights: dict = field(default_factory=dict)
    tiebreak_scores: tuple = ()
    effective: dt.date | None = None
    amendments: list = field(default_factory=list)      # (effective date, rule, change dict, text)


def _money_x12(amount: str, per: str) -> int:
    a = to_int(amount)
    if per == "year":
        return a * 12
    if per == "month":
        return a * 144
    raise ParseError(f"period {per!r}")


def _parse_bands(body: str, unit: str, value_suffix: str) -> list:
    """'fewer than 25 employees 0 points; 25 to 99 employees 4 points; 2,500 employees or more 23 points' ->
    [(lo, hi, value)] contiguous from 0. unit 'employees' / 'points'; value_suffix ' points' or ''."""
    out = []
    for item in body.split("; "):
        m = re.fullmatch(rf"fewer than ([\d,]+) {unit} (\d+){value_suffix}", item)
        if m:
            out.append((0, to_int(m.group(1)) - 1, int(m.group(2))))
            continue
        m = re.fullmatch(rf"([\d,]+) to ([\d,]+) {unit} (\d+){value_suffix}", item)
        if m:
            out.append((to_int(m.group(1)), to_int(m.group(2)), int(m.group(3))))
            continue
        m = re.fullmatch(rf"([\d,]+) {unit} or more (\d+){value_suffix}", item)
        if m:
            out.append((to_int(m.group(1)), None, int(m.group(2))))
            continue
        raise ParseError(f"band item {item!r}")
    _check_contiguous([(a, b) for a, b, _ in out])
    return out


def _check_contiguous(bands):
    if bands[0][0] != 0:
        raise ParseError(f"bands do not start at 0: {bands}")
    for (a, b), (c, d) in zip(bands, bands[1:]):
        if b is None or c != b + 1:
            raise ParseError(f"bands not contiguous: {bands}")
    if bands[-1][1] is not None:
        raise ParseError(f"last band is bounded: {bands}")


def _band_value(bands, x: int) -> int:
    for lo, hi, v in bands:
        if x >= lo and (hi is None or x <= hi):
            return v
    raise ParseError(f"value {x} outside the bands")


_RULE_RX: list = []   # filled below: (compiled regex, handler)


def _rule(pattern):
    def deco(fn):
        _RULE_RX.append((re.compile(pattern, re.S), fn))
        return fn
    return deco


EVIDENCE_A = ("only the primary contact's own words are evidence, meaning the web form they submitted and the "
              "emails or chat messages they wrote themselves. Rep notes, and anything the contact reports another "
              "person as saying, are not evidence{exc}. When several evidence statements of the same kind exist, "
              "only the most recent one is used.")
EVIDENCE_W = ("the primary contact's own statements, that is, the web form they filled in and the emails or chat "
              "messages they wrote. Notes written by reps, and anything the contact attributes to someone else, are "
              "not admissible{exc}. Where the contact said the same kind of thing more than once, use only the "
              "latest admissible statement.")


@_rule(r"^(\d+)\. Scope: score only the primary contact named in the lead record\. Other people at the company are "
       r"not scored, and activity logged under any other lead id does not count\.$")
def _r_scope(R, m, n):
    R.rule_kind[n] = "scope"


@_rule(r"^(\d+)\. Who is scored: only the primary contact shown in the lead record\. Colleagues at the same company "
       r"are not scored, and any activity filed under a different lead id is ignored\.$")
def _r_scope_w(R, m, n):
    R.rule_kind[n] = "scope"


@_rule(r"^(\d+)\. Evidence: (.*)$")
def _r_evidence(R, m, n):
    body = m.group(2)
    if body == EVIDENCE_A.format(exc=""):
        pass
    else:
        mm = re.fullmatch(re.escape(EVIDENCE_A.format(exc="@@")).replace("@@", r", except that a rep note giving the "
                          r"prospect's target date is evidence for rule (\d+)"), body)
        if not mm:
            raise ParseError(f"evidence rule {body!r}")
        R.rep_target_ok = True
        R.rule_kind.setdefault("_rep_target_rule", int(mm.group(1)))
    R.rule_kind[n] = "evidence"


@_rule(r"^(\d+)\. Admissible evidence: (.*)$")
def _r_evidence_w(R, m, n):
    body = m.group(2)
    if body == EVIDENCE_W.format(exc=""):
        pass
    else:
        mm = re.fullmatch(re.escape(EVIDENCE_W.format(exc="@@")).replace("@@", r", with one exception: a rep note "
                          r"recording the prospect's target date is admissible for rule (\d+)"), body)
        if not mm:
            raise ParseError(f"evidence rule {body!r}")
        R.rep_target_ok = True
        R.rule_kind.setdefault("_rep_target_rule", int(mm.group(1)))
    R.rule_kind[n] = "evidence"


@_rule(r"^(\d+)\. Statement window: only statements (at most|less than) (\d+) days old on the scoring date are "
       r"evidence; a statement exactly (\d+) days old (is|is not)\. Age is the scoring date minus the statement's "
       r"date\.$")
def _r_stmt_window(R, m, n):
    inc = m.group(2) == "at most"
    if m.group(3) != m.group(4) or (m.group(5) == "is") != inc:
        raise ParseError("statement window wording")
    R.stmt_window = Window(int(m.group(3)), inc)
    R.rule_kind[n] = "stmt_window"


@_rule(r"^(\d+)\. Company size: (.*)$")
def _r_size(R, m, n):
    b = m.group(2)
    if b == "use the employee count from the enrichment lookup; ignore the employee range picked on the web form.":
        R.size_source = "enrichment"
    elif b == "use the lower end of the employee range picked on the web form; ignore the enrichment lookup.":
        R.size_source = "form"
    else:
        raise ParseError(f"size rule {b!r}")
    R.rule_kind[n] = "size"


@_rule(r"^(\d+)\. Headcount: (.*)$")
def _r_size_w(R, m, n):
    b = m.group(2)
    if b == "take the enrichment lookup's employee figure; the web-form employee range is not used.":
        R.size_source = "enrichment"
    elif b == "take the bottom of the employee range chosen on the web form; the enrichment lookup is not used.":
        R.size_source = "form"
    else:
        raise ParseError(f"headcount rule {b!r}")
    R.rule_kind[n] = "size"


def _title_table(body: str, suffix: str) -> dict:
    out = {}
    for item in body.split("; "):
        mm = re.fullmatch(rf"(.+?) (\d+){suffix}", item)
        if not mm:
            raise ParseError(f"title item {item!r}")
        if mm.group(1) in out:
            raise ParseError(f"duplicate title {mm.group(1)!r}")
        out[mm.group(1)] = int(mm.group(2))
    return out


@_rule(r"^(\d+)\. Title points \(the primary contact's exact title\): (.*)\.$")
def _r_title(R, m, n):
    R.title_points = _title_table(m.group(2), " points")
    R.rule_kind[n] = "title"


@_rule(r"^(\d+)\. Size points \(company size as in rule (\d+)\): (.*)\.$")
def _r_size_pts(R, m, n):
    R.size_bands = _parse_bands(m.group(3), "employees", " points")
    R.rule_kind[n] = "size_points"


def _act_table(body: str, suffix: str) -> dict:
    out = {}
    for item in body.split("; "):
        mm = re.fullmatch(rf"([a-zA-Z ]+?) (\d+){suffix}", item)
        if not mm:
            raise ParseError(f"activity item {item!r}")
        if mm.group(1) in out:
            raise ParseError(f"duplicate activity {mm.group(1)!r}")
        out[mm.group(1)] = int(mm.group(2))
    return out


@_rule(r"^(\d+)\. Activity points: (.*?)\. Other activity types score 0 points\. A webinar or trade show meeting "
       r"scores only if attended; a registration alone scores 0 points\. The same activity type on the same day "
       r"counts once\.(?: Each activity type counts at most (\d+) times? in total\.)?$")
def _r_act(R, m, n):
    R.act_points = _act_table(m.group(2), " points")
    R.act_type_max = int(m.group(3)) if m.group(3) else None
    R.rule_kind[n] = "act_points"


@_rule(r"^(\d+)\. Engagement activities and their points: (.*?)\. Anything else earns nothing\. Webinars and trade "
       r"show meetings earn points only when attended; signing up alone earns nothing\. Repeats of one activity type "
       r"on one calendar day count a single time\.$")
def _r_act_w(R, m, n):
    R.act_points = _act_table(m.group(2), "")
    R.rule_kind[n] = "act_points"


@_rule(r"^(\d+)\. Activity window: only activity (at most|less than) (\d+) days old on the scoring date counts; "
       r"activity exactly (\d+) days old (counts|does not count)\. Age is the scoring date minus the activity's date "
       r"\(UTC\)\.$")
def _r_act_window(R, m, n):
    inc = m.group(2) == "at most"
    if m.group(3) != m.group(4) or (m.group(5) == "counts") != inc:
        raise ParseError("activity window wording")
    R.act_window = Window(int(m.group(3)), inc)
    R.rule_kind[n] = "act_window"


@_rule(r"^(\d+)\. Recency: an activity counts only if it happened (fewer than|at most) (\d+) days before the scoring "
       r"date \(exactly (\d+) days before (does not count|still counts)\)\. Age is the scoring date minus the "
       r"activity date, in UTC\.$")
def _r_act_window_w(R, m, n):
    inc = m.group(2) == "at most"
    if m.group(3) != m.group(4) or (m.group(5) == "still counts") != inc:
        raise ParseError("recency wording")
    R.act_window = Window(int(m.group(3)), inc)
    R.rule_kind[n] = "act_window"


@_rule(r"^(\d+)\. Activity cap: activity points count up to (\d+) points in total\.$")
def _r_cap(R, m, n):
    R.act_cap = int(m.group(2))
    R.rule_kind[n] = "act_cap"


@_rule(r"^(\d+)\. Engagement ceiling: at most (\d+) activity points are counted\.$")
def _r_cap_w(R, m, n):
    R.act_cap = int(m.group(2))
    R.rule_kind[n] = "act_cap"


@_rule(r"^(\d+)\. Unsubscribes: each unsubscribe from marketing email inside the activity window subtracts (\d+) "
       r"points \(the same day counts once\)\. The total never goes below 0\.$")
def _r_unsub(R, m, n):
    R.unsub_penalty = int(m.group(2))
    R.rule_kind[n] = "unsub"


def _statuses(s: str) -> tuple:
    items = split_list(s)
    for it in items:
        if it not in ("approved", "requested", "hoped", "hypothetical"):
            raise ParseError(f"status {it!r}")
    return tuple(items)


_BUDGET_TAIL = (r" has a counting status and an amount of at least \$([\d,]+) per (year|month)\. Counting statuses: "
                r"([a-z ,]+)\. " + re.escape(_STATUS_SENT) + "$")


@_rule(r"^(\d+)\. Budget: add (\d+) points when the most recent budget statement that is evidence under rule (\d+)"
       + _BUDGET_TAIL)
def _r_budget_pts(R, m, n):
    R.budget = BudgetTest(_money_x12(m.group(4), m.group(5)), _statuses(m.group(6)), n)
    R.budget_points = int(m.group(2))
    R.rule_kind[n] = "budget"


@_rule(r"^(\d+)\. Budget terms: a counting budget means that the most recent budget statement that is evidence under "
       r"rule (\d+)" + _BUDGET_TAIL)
def _r_budget_terms(R, m, n):
    R.budget = BudgetTest(_money_x12(m.group(3), m.group(4)), _statuses(m.group(5)), n)
    R.rule_kind[n] = "budget"


@_rule(r"^(\d+)\. Budget criterion: met when the most recent budget statement that is evidence under rules (\d+) and "
       r"(\d+)" + _BUDGET_TAIL)
def _r_budget_crit(R, m, n):
    R.budget = BudgetTest(_money_x12(m.group(4), m.group(5)), _statuses(m.group(6)), n)
    R.rule_kind[n] = "budget"


@_rule(r"^(\d+)\. Budget score \(the latest admissible budget statement, see rule (\d+)\): (\d+) if it is approved "
       r"with at least \$([\d,]+) per (year|month); (\d+) if it is requested with at least \$([\d,]+) per (year|month); "
       r"(\d+) if it is approved or requested with a smaller amount; (\d+) otherwise\. "
       + re.escape(_STATUS_SENT_W) + "$")
def _r_budget_w(R, m, n):
    a, b = _money_x12(m.group(4), m.group(5)), _money_x12(m.group(7), m.group(8))
    if a != b:
        raise ParseError("weighted budget minimums differ")
    R.wbudget = {"min": a, "approved": int(m.group(3)), "requested": int(m.group(6)), "small": int(m.group(9)),
                 "other": int(m.group(10))}
    R.budget = BudgetTest(a, ("approved", "requested"), n)
    R.rule_kind[n] = "budget"


_HORIZON = r"is on or after the scoring date and (at most|fewer than) (\d+) days after it"


@_rule(r"^(\d+)\. Timeline: add (\d+) points when the most recent target date that is evidence under rule (\d+) "
       + _HORIZON + r"\.$")
def _r_timeline_pts(R, m, n):
    R.timeline = Horizon(int(m.group(5)), m.group(4) == "at most")
    R.timeline_points = int(m.group(2))
    R.timeline_rule = n
    R.rule_kind[n] = "timeline"


@_rule(r"^(\d+)\. Timeline criterion: met when the most recent target date that is evidence under rules (\d+) and "
       r"(\d+) " + _HORIZON + r"\.$")
def _r_timeline_crit(R, m, n):
    R.timeline = Horizon(int(m.group(5)), m.group(4) == "at most")
    R.timeline_rule = n
    R.rule_kind[n] = "timeline"


@_rule(r"^(\d+)\. Timeline score \(the latest admissible target date, see rule (\d+)\): (\d+) if it is at most (\d+) "
       r"days after the scoring date; (\d+) if at most (\d+) days; (\d+) if at most (\d+) days; (\d+) if it is later, "
       r"before the scoring date, or missing\.$")
def _r_timeline_w(R, m, n):
    g = [int(x) for x in m.groups()[2:]]
    R.wtimeline = [(g[1], g[0]), (g[3], g[2]), (g[5], g[4])]
    R.wtimeline_other = g[6]
    if not (g[1] < g[3] < g[5]):
        raise ParseError("weighted timeline steps")
    R.timeline_rule = n
    R.rule_kind[n] = "timeline"


@_rule(r"^(\d+)\. Need criterion: met when the most recent main-problem statement that is evidence under rules (\d+) "
       r"and (\d+) names one of: (.*)\.$")
def _r_need(R, m, n):
    R.need_list = m.group(4).split("; ")
    R.rule_kind[n] = "need"


@_rule(r"^(\d+)\. Authority criterion: met when the primary contact's exact title is one of: (.*)\.$")
def _r_auth(R, m, n):
    R.auth_list = m.group(2).split("; ")
    R.rule_kind[n] = "authority"


@_rule(r"^(\d+)\. Seniority bands \(exact title\): (.*)\.$")
def _r_bands(R, m, n):
    for item in m.group(2).split("; "):
        mm = re.fullmatch(r"band ([A-Z]): (.*)", item)
        if not mm:
            raise ParseError(f"band item {item!r}")
        R.bands[mm.group(1)] = mm.group(2).split(", ")
    R.rule_kind[n] = "bands"


def _level_items(body: str, pat: str) -> list:
    out = []
    for item in body.split("; "):
        mm = re.fullmatch(pat, item)
        if not mm:
            raise ParseError(f"level item {item!r}")
        out.append(mm.groups())
    return out


@_rule(r"^(\d+)\. Levels by total points: (.*)\.$")
def _r_levels_pts(R, m, n):
    items = []
    for item in m.group(2).split("; "):
        mm = re.fullmatch(r"([\d,]+) to ([\d,]+) points is (.+)", item) or \
            re.fullmatch(r"([\d,]+) points or more is (.+)", item)
        if not mm:
            raise ParseError(f"level item {item!r}")
        if len(mm.groups()) == 3:
            items.append((to_int(mm.group(1)), to_int(mm.group(2)), mm.group(3)))
        else:
            items.append((to_int(mm.group(1)), None, mm.group(2)))
    _check_contiguous([(a, b) for a, b, _ in items])
    R.levels = [x[2] for x in items]
    R.level_bands = [(a, b) for a, b, _ in items]
    R.archetype = "points"
    R.rule_kind[n] = "levels"


@_rule(r"^(\d+)\. Levels by weighted total: (.*)\.$")
def _r_levels_w(R, m, n):
    items = []
    for item in m.group(2).split("; "):
        mm = re.fullmatch(r"(\d+) to (\d+) is (.+)", item) or re.fullmatch(r"(\d+) or more is (.+)", item)
        if not mm:
            raise ParseError(f"level item {item!r}")
        if len(mm.groups()) == 3:
            items.append((int(mm.group(1)), int(mm.group(2)), mm.group(3)))
        else:
            items.append((int(mm.group(1)), None, mm.group(2)))
    _check_contiguous([(a, b) for a, b, _ in items])
    R.levels = [x[2] for x in items]
    R.level_bands = [(a, b) for a, b, _ in items]
    R.archetype = "weighted"
    R.rule_kind[n] = "levels"


@_rule(r"^(\d+)\. Levels by the number of criteria met \(budget, authority, need, timeline\): (.*)\.$")
def _r_levels_bant(R, m, n):
    levels, cmap = [], {}
    for item in m.group(2).split("; "):
        mm = re.fullmatch(r"(\d) is (.+)", item) or re.fullmatch(r"(\d) (?:or|to) (\d) is (.+)", item)
        if not mm:
            raise ParseError(f"level item {item!r}")
        g = mm.groups()
        lo, hi, name = (int(g[0]), int(g[0]), g[1]) if len(g) == 2 else (int(g[0]), int(g[1]), g[2])
        if hi < lo:
            raise ParseError("bant range")
        # 'a or b' names two counts; 'a to b' a range; both are contiguous here
        if " or " in item and hi != lo + 1:
            raise ParseError(f"'or' with a gap: {item!r}")
        levels.append(name)
        for c in range(lo, hi + 1):
            if c in cmap:
                raise ParseError("bant count twice")
            cmap[c] = len(levels) - 1
    if sorted(cmap) != [0, 1, 2, 3, 4]:
        raise ParseError(f"bant counts {sorted(cmap)}")
    if [cmap[c] for c in range(5)] != sorted(cmap[c] for c in range(5)):
        raise ParseError("bant levels not ascending")
    R.levels = levels
    R.count_levels = cmap
    R.archetype = "bant"
    R.rule_kind[n] = "levels"


@_rule(r"^(\d+)\. Levels: gates are checked in order\. A lead's level is the highest level whose gate it passes "
       r"together with every earlier gate; a lead that fails gate 1 is (.+)\.$")
def _r_levels_gated(R, m, n):
    R.base_level = m.group(2)
    R.archetype = "gated"
    R.rule_kind[n] = "levels"


@_rule(r"^(\d+)\. Gate (\d+) \((.+)\): (.*)\.$")
def _r_gate(R, m, n):
    k, lvl, cond = int(m.group(2)), m.group(3), m.group(4)
    if k != len(R.gates) + 1:
        raise ParseError(f"gate order {k}")
    mm = re.fullmatch(r"company size \(rule (\d+)\) of at least ([\d,]+) employees", cond)
    if mm:
        g = ("size", {"min": to_int(mm.group(2))})
    else:
        mm = re.fullmatch(r"the primary contact is in seniority band (.+) \(rule (\d+)\)", cond)
        if mm:
            g = ("band", {"bands": split_list(mm.group(1))})
        else:
            mm = re.fullmatch(r"at least (\d+) activity points under rules (.+)", cond)
            if mm:
                g = ("activity", {"min": int(mm.group(1)), "rules": tuple(int(x) for x in split_list(mm.group(2)))})
            else:
                mm = re.fullmatch(r"a counting budget under rule (\d+)", cond)
                if mm:
                    g = ("budget", {"rule": int(mm.group(1))})
                else:
                    mm = re.fullmatch(r"the most recent target date that is evidence under rule (\d+) "
                                      + _HORIZON, cond)
                    if mm:
                        g = ("timeline", {"h": Horizon(int(mm.group(3)), mm.group(2) == "at most")})
                    else:
                        raise ParseError(f"gate condition {cond!r}")
    R.gates.append((lvl, g[0], g[1], n))
    R.rule_kind[n] = f"gate{k}"


@_rule(r"^(\d+)\. Override, applied after the level is set: (.*)\.$")
def _r_override(R, m, n):
    b = m.group(2)
    mm = re.fullmatch(r"a lead without a counting budget under rule (\d+) is at most (.+), so a higher level becomes "
                      r"(.+)", b)
    if mm:
        if mm.group(2) != mm.group(3):
            raise ParseError("override level mismatch")
        R.overrides.append(("ceiling_no_budget", mm.group(2), int(mm.group(1))))
    else:
        mm = re.fullmatch(r"a lead with a demo request that counts under rules (\d+) and (\d+) is at least (.+), so a "
                          r"lower level becomes (.+)", b)
        if not mm or mm.group(3) != mm.group(4):
            raise ParseError(f"override {b!r}")
        R.overrides.append(("floor_demo", mm.group(3), (int(mm.group(1)), int(mm.group(2)))))
    R.rule_kind[n] = "override"


def _disq_clause(R, cl: str):
    mm = re.fullmatch(r"the company (?:is on|appears on) the competitor list \((.+)\)", cl)
    if mm:
        return ("competitor", mm.group(1).split(", "))
    mm = re.fullmatch(r"the primary contact(?:'s email domain is a personal email domain| writes from a personal email "
                      r"domain) \((.+)\)", cl)
    if mm:
        return ("personal_domain", mm.group(1).split(", "))
    mm = re.fullmatch(r"the company's region is (?:not a served region|outside the served regions) \(served regions: "
                      r"(.+)\)", cl)
    if mm:
        return ("region", mm.group(1).split(", "))
    if cl in ("the company is a current customer", "the company already buys from us"):
        return ("customer", None)
    mm = re.fullmatch(r"the company has fewer than ([\d,]+) employees \(company size as in rule (\d+)\)", cl)
    if mm:
        return ("small", to_int(mm.group(1)))
    raise ParseError(f"disqualifier clause {cl!r}")


@_rule(r"^(\d+)\. Disqualifiers: (.*)\. A disqualified lead is (.+) whatever (?:its points and any override|its points"
       r"|criteria it meets|gates it passes)\.$")
def _r_disq(R, m, n):
    R.disq = [_disq_clause(R, c) for c in m.group(2).split("; ")]
    R.disq_level = m.group(3)
    R.rule_kind[n] = "disq"


@_rule(r"^(\d+)\. Automatic (.+) rating: (.*)\. Any one of these makes the lead (.+), whatever its weighted total\.$")
def _r_disq_w(R, m, n):
    if m.group(2) != m.group(4):
        raise ParseError("automatic rating level mismatch")
    R.disq = [_disq_clause(R, c) for c in m.group(3).split("; ")]
    R.disq_level = m.group(2)
    R.rule_kind[n] = "disq"


@_rule(r"^(\d+)\. Sales-ready: leads at (.+) or above are sales-ready and go to the sales team\.$")
def _r_ready(R, m, n):
    R.ready_level = m.group(2)
    R.rule_kind[n] = "ready"


@_rule(r"^(\d+)\. Handoff: a lead rated (.+) or higher counts as sales-ready and is passed to sales\.$")
def _r_ready_w(R, m, n):
    R.ready_level = m.group(2)
    R.rule_kind[n] = "ready"


@_rule(r"^(\d+)\. Fit score \(headcount as in rule (\d+)\): (.*)\.$")
def _r_fit(R, m, n):
    R.fit_bands = _parse_bands(m.group(3), "employees", "")
    R.rule_kind[n] = "fit"


@_rule(r"^(\d+)\. Role score \(the primary contact's exact title\): (.*)\.$")
def _r_role(R, m, n):
    R.role_score = _title_table(m.group(2), "")
    R.rule_kind[n] = "role"


@_rule(r"^(\d+)\. Engagement score \(activity points under rules (.+)\): (.*)\.$")
def _r_eng(R, m, n):
    R.eng_rules = tuple(int(x) for x in split_list(m.group(2)))
    R.eng_bands = _parse_bands(m.group(3), "points", "")
    R.rule_kind[n] = "engagement"


@_rule(r"^(\d+)\. Weighted total: (\d+) x fit \+ (\d+) x role \+ (\d+) x engagement \+ (\d+) x budget \+ (\d+) x "
       r"timeline\.$")
def _r_weights(R, m, n):
    R.weights = dict(zip(("fit", "role", "engagement", "budget", "timeline"), (int(x) for x in m.groups()[1:])))
    R.rule_kind[n] = "weights"


@_rule(r"^(\d+)\. Tie-break: when the weighted total equals the lowest total of a level exactly, the lead gets that "
       r"level only if its budget score is (\d+) or (\d+); otherwise it gets the level below\.$")
def _r_tiebreak(R, m, n):
    R.tiebreak_scores = (int(m.group(2)), int(m.group(3)))
    R.rule_kind[n] = "tiebreak"


@_rule(r"^(\d+)\. Amendment (\d+), effective (\d{4}-\d\d-\d\d), applies to leads scored on or after that date: in rule "
       r"(\d+),? (.*)\.$")
def _r_amend(R, m, n):
    R.amendments.append((to_date(m.group(3)), int(m.group(4)), m.group(5), m.group(0)))
    R.rule_kind[n] = "amendment"


def _apply_amendment(R: Rubric, rule: int, change: str):
    kind = R.rule_kind.get(rule, "")
    mm = re.fullmatch(r"the timeline limit changes from (\d+) to (\d+) days", change)
    if mm:
        a, b = int(mm.group(1)), int(mm.group(2))
        if kind == "timeline":
            h = R.timeline
        elif kind.startswith("gate") and R.gates[int(kind[4:]) - 1][1] == "timeline":
            h = R.gates[int(kind[4:]) - 1][2]["h"]
        else:
            raise ParseError(f"timeline amendment to rule {rule} ({kind})")
        if h.days != a:
            raise ParseError("amendment 'from' value")
        h.days = b
        return
    mm = re.fullmatch(r"the (activity|statement) window changes from (\d+) to (\d+) days", change)
    if mm:
        w = R.act_window if mm.group(1) == "activity" else R.stmt_window
        if kind != ("act_window" if mm.group(1) == "activity" else "stmt_window") or w.days != int(mm.group(2)):
            raise ParseError(f"window amendment {change!r}")
        w.days = int(mm.group(3))
        return
    mm = re.fullmatch(r"the budget minimum changes from \$([\d,]+) to \$([\d,]+) per (year|month)", change)
    if mm:
        if kind != "budget" or R.budget.min_annual_x12 != _money_x12(mm.group(1), mm.group(3)):
            raise ParseError(f"budget amendment {change!r}")
        R.budget.min_annual_x12 = _money_x12(mm.group(2), mm.group(3))
        return
    mm = re.fullmatch(r"the minimum for gate (\d+) changes from ([\d,]+) to ([\d,]+) (employees|activity points)",
                      change)
    if mm:
        k = int(mm.group(1))
        lvl, gk, gp, rn = R.gates[k - 1]
        if rn != rule or gk != {"employees": "size", "activity points": "activity"}[mm.group(4)] \
                or gp["min"] != to_int(mm.group(2)):
            raise ParseError(f"gate amendment {change!r}")
        gp["min"] = to_int(mm.group(3))
        return
    mm = re.fullmatch(r"the activity cap changes from (\d+) to (\d+) points", change)
    if mm:
        if kind != "act_cap" or R.act_cap != int(mm.group(1)):
            raise ParseError(f"cap amendment {change!r}")
        R.act_cap = int(mm.group(2))
        return
    mm = re.fullmatch(r"([a-zA-Z ]+) points change from (\d+) to (\d+)", change)
    if mm:
        t = mm.group(1)
        if kind != "act_points" or R.act_points.get(t) != int(mm.group(2)):
            raise ParseError(f"activity amendment {change!r}")
        R.act_points[t] = int(mm.group(3))
        return
    mm = re.fullmatch(r"the lowest total for (.+) changes from ([\d,]+) to ([\d,]+) points", change)
    if mm:
        if kind != "levels" or mm.group(1) not in R.levels:
            raise ParseError(f"level amendment {change!r}")
        i = R.levels.index(mm.group(1))
        a, b = to_int(mm.group(2)), to_int(mm.group(3))
        if i == 0 or R.level_bands[i][0] != a:
            raise ParseError(f"level amendment 'from' {change!r}")
        lo, hi = R.level_bands[i]
        plo, phi = R.level_bands[i - 1]
        if not (plo < b and (hi is None or b <= hi)):
            raise ParseError(f"level amendment leaves an empty band {change!r}")
        R.level_bands[i] = (b, hi)
        R.level_bands[i - 1] = (plo, b - 1)
        return
    raise ParseError(f"amendment change {change!r}")


def parse_rubric(title: str, rules: list[str], scoring_date: dt.date) -> Rubric:
    R = Rubric()
    mm = re.fullmatch(r"Lead scoring rubric LQ-\d+ \(version \d+\), effective (\d{4}-\d\d-\d\d)", title) or \
        re.fullmatch(r"Qualification scorecard LQ-\d+ \(revision \d+\), in force from (\d{4}-\d\d-\d\d)", title)
    if not mm:
        raise ParseError(f"rubric title {title!r}")
    R.effective = to_date(mm.group(1))
    if scoring_date < R.effective:
        raise ParseError("scoring date before the rubric's effective date")
    for i, text in enumerate(rules, 1):
        for rx, fn in _RULE_RX:
            m = rx.match(text)
            if m:
                if int(m.group(1)) != i:
                    raise ParseError("rule number")
                fn(R, m, i)
                break
        else:
            raise ParseError(f"unknown rule: {text!r}")
    # amendments in force on the scoring date, in their order
    for eff, rule, change, _ in R.amendments:
        if scoring_date >= eff:
            _apply_amendment(R, rule, change)
        else:   # still check the amendment names a real rule and value (parse it on a copy)
            import copy
            _apply_amendment(copy.deepcopy(R), rule, change)
    # structure checks
    if not R.archetype or not R.levels and R.archetype != "gated":
        raise ParseError("no level rule")
    if R.archetype == "gated":
        R.levels = [R.base_level] + [g[0] for g in R.gates]
    if len(set(R.levels)) != len(R.levels):
        raise ParseError("duplicate level names")
    for name in (R.disq_level, R.ready_level):
        if name and name not in R.levels:
            raise ParseError(f"level {name!r} not in the ladder")
    if R.disq and R.disq_level != R.levels[0]:
        raise ParseError("disqualified level is not the lowest")
    for _, name, _ in R.overrides:
        if name not in R.levels:
            raise ParseError(f"override level {name!r}")
    if not R.size_source:
        raise ParseError("no company size rule")
    return R


# ------------------------------------------------------------------------------------------------ statements
_BUDGET_MSG = [
    (re.compile(r"^We have an approved budget of \$([\d,]+) per (year|month) for this\.$"), "approved"),
    (re.compile(r"^We have requested a budget of \$([\d,]+) per (year|month) for this\.$"), "requested"),
    (re.compile(r"^We hope to get a budget of \$([\d,]+) per (year|month) for this\.$"), "hoped"),
    (re.compile(r"^If we had a budget of \$([\d,]+) per (year|month), we would buy this\.$"), "hypothetical"),
]
_TARGET_MSG = re.compile(r"^Our target date for going live is (\d{4}-\d\d-\d\d)\.$")
_PROBLEM_MSG = re.compile(r"^Our main problem is (.+)\.$")
# reported speech (never evidence): 'My <role> says ...' / 'My <role> wants this live by <date>.'
_REPORTED = re.compile(r"^My [A-Za-z ]+? (says|wants this live by) ")
_FILLER = {
    "Is there a reference customer we could talk to?", "Can the onboarding happen in two phases?",
    "Could you send over the security questionnaire?", "Thanks for the overview call earlier this week.",
    "Please resend the slides from the call.", "We are comparing a few options at the moment.",
    "Does the contract include a training session?", "Looping in a colleague from our IT team next week.",
}
_REP_TARGET = re.compile(r"^Call notes: the prospect's target date for going live is (\d{4}-\d\d-\d\d)\.$")


def classify_message(text: str):
    """-> ('budget', status, amount, per) | ('target', date) | ('problem', str) | ('reported', text) | ('other', text).
    'other' covers filler and untrusted notes (never evidence of any kind)."""
    for rx, status in _BUDGET_MSG:
        m = rx.match(text)
        if m:
            return ("budget", status, m.group(1), m.group(2))
    m = _TARGET_MSG.match(text)
    if m:
        return ("target", m.group(1))
    m = _PROBLEM_MSG.match(text)
    if m:
        return ("problem", m.group(1))
    if _REPORTED.match(text):
        return ("reported", text)
    return ("other", text)


FORM_STATUS = {"approved": "approved", "requested": "requested", "hoped": "hoped", "hypothetical": "hypothetical"}

# How decide2 reads the points where the rubric text leaves room. The defaults are the readings builder D chose from
# the rubric text (and the yes/no card) BEFORE comparing with any gold. The alternatives exist only for the
# ambiguity report (`sensitivity`): which rows would change answer under another defensible reading.
DEFAULT_READINGS = {
    "gate_score": "individual",        # 'N of M gates passed' counts every gate the lead passes | 'consecutive'
    "judge_reason": False,             # judge rows: yes iff recorded score and level match (the card) | also reason
    "unsub_before_cap": False,         # unsubscribe penalty comes off the total | off activity points before the cap
    "latest_counting_budget": False,   # the most recent budget statement decides | the most recent counting one
    "form_outside_window": False,      # the statement window applies to the web form too | the form is exempt
    "rep_target_no_window": False,     # the window applies to rep-note target dates too | they are exempt
    "type_max_before_dedupe": False,   # 'at most N times' counts after the same-day rule | before it
    "need_substring": False,           # 'names one of': the stated problem equals a listed need | contains one
    "disq_zero_score": False,          # a disqualified lead keeps its computed score | its score is 0
    # coverage probes (not defensible readings of the rubric: 'only the most recent one is used' is explicit).
    # They show whether the recency rule ever decides an item.
    "any_budget_counts": False,        # probe: any evidence budget statement that meets the test counts
    "any_target_counts": False,        # probe: any evidence target date inside the horizon counts
    "any_problem_counts": False,       # probe: any evidence main-problem statement naming a need counts
}


def _rd(readings):
    rd = dict(DEFAULT_READINGS)
    if readings:
        unknown = set(readings) - set(rd)
        if unknown:
            raise KeyError(f"unknown readings {sorted(unknown)}")
        rd.update(readings)
    return rd


def evidence(doc: Doc, R: Rubric, rd: dict | None = None) -> dict:
    """The most recent evidence statement of each kind (budget, target, problem), after the scope, evidence and
    statement-window rules. Returns {'budget': {...}|None, 'target': date|None, 'problem': str|None, 'notes': [...]}."""
    rd = _rd(rd)
    primary = doc.lead["Primary contact"]
    stmts = []   # (time, kind, value, source)

    def in_window(t: dt.datetime, src: str) -> bool:
        if R.stmt_window is None:
            return True
        if src == "form" and rd["form_outside_window"]:
            return True
        if src == "rep_note" and rd["rep_target_no_window"]:
            return True
        return R.stmt_window.ok((doc.scoring_date - t.date()).days)

    # web form: evidence only if the primary contact submitted it
    if doc.form:
        if doc.form.get("Submitted by") == primary:
            t = to_ts(doc.form["Submitted at"])
            if "Budget status" in doc.form or "Budget amount" in doc.form:
                st = doc.form.get("Budget status")
                am = doc.form.get("Budget amount")
                if st is None or am is None:
                    raise ParseError("half a budget on the form")
                mm = re.fullmatch(r"\$([\d,]+) per (year|month)", am)
                if not mm or st not in FORM_STATUS:
                    raise ParseError(f"form budget {st!r} {am!r}")
                stmts.append((t, "budget", {"status": FORM_STATUS[st], "annual_x12": _money_x12(mm.group(1),
                                                                                                mm.group(2))}, "form"))
            if "Target date" in doc.form:
                stmts.append((t, "target", to_date(doc.form["Target date"]), "form"))
            if "Main problem" in doc.form:
                stmts.append((t, "problem", doc.form["Main problem"], "form"))
    for e in doc.events:
        if e.kind == "message" and e.who == primary:
            c = classify_message(e.text)
            if c[0] == "budget":
                stmts.append((e.time, "budget", {"status": c[1], "annual_x12": _money_x12(c[2], c[3])}, "message"))
            elif c[0] == "target":
                stmts.append((e.time, "target", to_date(c[1]), "message"))
            elif c[0] == "problem":
                stmts.append((e.time, "problem", c[1], "message"))
        elif e.kind == "rep_note" and R.rep_target_ok:
            m = _REP_TARGET.match(e.text)
            if m:
                stmts.append((e.time, "target", to_date(m.group(1)), "rep_note"))
    if any(t.date() > doc.scoring_date for t, k, v, src in stmts):
        raise ParseError("statement dated after the scoring date")
    out = {"budget": None, "target": None, "problem": None}
    for kind in ("budget", "target", "problem"):
        cands = [(t, v) for t, k, v, src in stmts if k == kind and in_window(t, src)]
        if kind == "budget" and rd["latest_counting_budget"] and R.budget is not None:
            cands = [(t, v) for t, v in cands if v["status"] in R.budget.statuses]
        if cands:
            cands.sort(key=lambda x: x[0])
            if len(cands) > 1 and cands[-1][0] == cands[-2][0] and cands[-1][1] != cands[-2][1]:
                raise ParseError(f"two different {kind} statements at the same time")
            out[kind] = cands[-1][1]
        out["all_" + kind] = [v for _, v in sorted(cands, key=lambda x: x[0])]
    return out


# ------------------------------------------------------------------------------------------------ activity
_ACT = re.compile(r"^(?P<type>[A-Za-z ]+?)(?:: (?P<detail>.+)| '(?P<title>[^']+)': (?P<att>attended|registered, did "
                  r"not attend))?$")


def activity_type(text: str) -> tuple[str, bool]:
    """-> (activity type, attended_flag_ok). Registrations of webinars / trade show meetings are (type, False)."""
    m = _ACT.match(text)
    if not m:
        return (text, False)
    t = m.group("type")
    if m.group("att"):
        return (t, m.group("att") == "attended")
    return (t, True)


def activity_points(doc: Doc, R: Rubric, use_cap: bool = True, use_window: bool = True,
                    rd: dict | None = None) -> dict:
    """Activity points under the scope, activity points, window, per-type limit and cap rules."""
    rd = _rd(rd)
    lead_id = doc.lead["Lead id"]
    seen_day = set()
    per_type = {}
    raw = 0
    demo_counts = False
    unsub_days = set()
    for e in sorted((e for e in doc.events if e.kind == "activity"), key=lambda e: e.time):
        if e.lead != lead_id:
            continue
        age = (doc.scoring_date - e.time.date()).days
        if age < 0:
            raise ParseError("activity after the scoring date")
        in_win = R.act_window.ok(age) if (use_window and R.act_window) else True
        t, ok = activity_type(e.text)
        if t == "unsubscribe from marketing email" and e.text == t:
            if in_win:
                unsub_days.add(e.time.date())
            continue
        if not in_win or not ok:
            continue
        if t in ("webinar", "trade show meeting") and not re.search(r" '[^']+': attended$", e.text):
            raise ParseError(f"{t} without an attendance flag: {e.text!r}")
        if t not in R.act_points:
            continue
        if rd["type_max_before_dedupe"]:
            if R.act_type_max is not None and per_type.get(t, 0) >= R.act_type_max:
                continue
            per_type[t] = per_type.get(t, 0) + 1
        if (t, e.time.date()) in seen_day:
            continue
        seen_day.add((t, e.time.date()))
        if not rd["type_max_before_dedupe"]:
            if R.act_type_max is not None and per_type.get(t, 0) >= R.act_type_max:
                continue
            per_type[t] = per_type.get(t, 0) + 1
        raw += R.act_points[t]
        if t == "demo request":
            demo_counts = True
    capped = min(raw, R.act_cap) if (use_cap and R.act_cap is not None) else raw
    return {"raw": raw, "points": capped, "unsub_days": len(unsub_days), "demo": demo_counts}


def demo_counts(doc: Doc, R: Rubric) -> bool:
    """'a demo request that counts under rules <points> and <window>': a demo request under this lead id, inside
    the activity window."""
    lead_id = doc.lead["Lead id"]
    for e in doc.events:
        if e.kind != "activity" or e.lead != lead_id:
            continue
        t, ok = activity_type(e.text)
        if t == "demo request" and ok and R.act_window.ok((doc.scoring_date - e.time.date()).days):
            if "demo request" not in R.act_points:
                raise ParseError("demo request has no points but the override names it")
            return True
    return False


# ------------------------------------------------------------------------------------------------ evaluation
def company_size(doc: Doc, R: Rubric) -> int:
    if R.size_source == "enrichment":
        m = re.fullmatch(r"([\d,]+) employees?", doc.lead["Enrichment lookup"])
        if not m:
            raise ParseError(f"enrichment {doc.lead['Enrichment lookup']!r}")
        return to_int(m.group(1))
    rng = doc.form.get("Company size range")
    if rng is None:
        raise ParseError("no company size range on the form")
    m = re.fullmatch(r"([\d,]+) to ([\d,]+) employees", rng) or re.fullmatch(r"([\d,]+) or more employees", rng)
    if not m:
        raise ParseError(f"size range {rng!r}")
    return to_int(m.group(1))


def disqualified(doc: Doc, R: Rubric) -> list[str]:
    hits = []
    for kind, p in R.disq:
        if kind == "competitor" and doc.lead["Company"] in p:
            hits.append(kind)
        elif kind == "personal_domain":
            email = doc.lead["Primary contact email"]
            if "@" not in email:
                raise ParseError("email")
            if email.split("@", 1)[1] in p:
                hits.append(kind)
        elif kind == "region" and doc.lead["Region"] not in p:
            hits.append(kind)
        elif kind == "customer":
            cc = doc.lead["Current customer"]
            if cc not in ("yes", "no"):
                raise ParseError("current customer flag")
            if cc == "yes":
                hits.append(kind)
        elif kind == "small" and company_size(doc, R) < p:
            hits.append(kind)
    return hits


@dataclass
class Result:
    archetype: str
    score: int
    score_text: str
    level: str
    level_index: int
    ready: bool
    parts: dict
    disq: list


def _horizon_ok(h: Horizon, target, today) -> bool:
    return target is not None and h.ok((target - today).days)


def _budget_met(R: Rubric, ev: dict, rd: dict) -> bool:
    if rd["any_budget_counts"]:
        return any(R.budget.met(b) for b in ev["all_budget"])
    return R.budget.met(ev["budget"])


def _target_ok(h: Horizon, ev: dict, today, rd: dict) -> bool:
    if rd["any_target_counts"]:
        return any(_horizon_ok(h, t, today) for t in ev["all_target"])
    return _horizon_ok(h, ev["target"], today)


def _need_met(R: Rubric, ev: dict, rd: dict) -> bool:
    def names(p):
        return p in R.need_list if not rd["need_substring"] else any(x in p for x in R.need_list)
    if rd["any_problem_counts"]:
        return any(names(p) for p in ev["all_problem"])
    return ev["problem"] is not None and names(ev["problem"])


def evaluate(doc: Doc, R: Rubric, readings: dict | None = None) -> Result:
    rd = _rd(readings)
    ev = evidence(doc, R, rd)
    today = doc.scoring_date
    title = doc.lead["Primary contact title"]
    dq = disqualified(doc, R)
    parts = {}
    if R.archetype == "points":
        if title not in R.title_points:
            raise ParseError(f"title {title!r} not in the title table")
        size = company_size(doc, R)
        act = activity_points(doc, R, rd=rd)
        parts["size"] = _band_value(R.size_bands, size)
        parts["title"] = R.title_points[title]
        parts["activity"] = act["points"]
        if R.unsub_penalty is not None:
            parts["unsubscribes"] = -R.unsub_penalty * act["unsub_days"]
            if rd["unsub_before_cap"]:
                raw = max(0, act["raw"] + parts["unsubscribes"])
                parts["activity"] = min(raw, R.act_cap) if R.act_cap is not None else raw
                parts["unsubscribes"] = 0
        parts["budget"] = R.budget_points if (R.budget and _budget_met(R, ev, rd)) else 0
        parts["timeline"] = R.timeline_points if (R.timeline and _target_ok(R.timeline, ev, today, rd)) else 0
        total = sum(parts.values())
        if R.unsub_penalty is not None:
            total = max(0, total)
        elif total < 0:
            raise ParseError("negative total")
        li = next(i for i, (lo, hi) in enumerate(R.level_bands) if total >= lo and (hi is None or total <= hi))
        parts["_level_before_overrides"] = li
        for kind, name, ref in R.overrides:
            j = R.levels.index(name)
            if kind == "ceiling_no_budget":
                if not _budget_met(R, ev, rd) and li > j:
                    li = j
            elif kind == "floor_demo":
                if demo_counts(doc, R) and li < j:
                    li = j
        if len(R.overrides) > 1:
            raise ParseError("two overrides: order undefined")
        score, score_text = total, f"{total} points"
    elif R.archetype == "bant":
        crit = {
            "budget": _budget_met(R, ev, rd),
            "authority": title in R.auth_list,
            "need": _need_met(R, ev, rd),
            "timeline": _target_ok(R.timeline, ev, today, rd),
        }
        parts.update(crit)
        score = sum(crit.values())
        li = R.count_levels[score]
        score_text = f"{score} of 4 criteria met"
    elif R.archetype == "gated":
        passed = []
        for lvl, kind, p, rn in R.gates:
            if kind == "size":
                ok = company_size(doc, R) >= p["min"]
            elif kind == "band":
                band = [b for b, ts in R.bands.items() if title in ts]
                if len(band) != 1:
                    raise ParseError(f"title {title!r} in {len(band)} bands")
                ok = band[0] in p["bands"]
            elif kind == "activity":
                kinds = {R.rule_kind.get(x) for x in p["rules"]}
                if not kinds <= {"act_points", "act_window", "act_cap"} or "act_points" not in kinds:
                    raise ParseError(f"activity gate rules {p['rules']}")
                use_cap = "act_cap" in kinds
                if R.act_cap is not None and not use_cap:
                    raise ParseError("activity gate leaves out the cap rule")
                ok = activity_points(doc, R, use_cap=use_cap, use_window="act_window" in kinds,
                                     rd=rd)["points"] >= p["min"]
            elif kind == "budget":
                if R.rule_kind.get(p["rule"]) != "budget":
                    raise ParseError("budget gate rule ref")
                ok = _budget_met(R, ev, rd)
            elif kind == "timeline":
                ok = _target_ok(p["h"], ev, today, rd)
            else:
                raise ParseError(kind)
            passed.append(ok)
        parts["gates"] = passed
        k = 0
        while k < len(passed) and passed[k]:
            k += 1
        li = k
        score = sum(passed) if rd["gate_score"] == "individual" else k
        score_text = f"{score} of {len(passed)} gates passed"
    elif R.archetype == "weighted":
        size = company_size(doc, R)
        if title not in R.role_score:
            raise ParseError(f"title {title!r} not in the role table")
        kinds = {R.rule_kind.get(x) for x in R.eng_rules}
        if not kinds <= {"act_points", "act_window", "act_cap"}:
            raise ParseError("engagement rules")
        use_cap = "act_cap" in kinds
        if R.act_cap is not None and not use_cap:
            raise ParseError("engagement leaves out the ceiling rule")
        act = activity_points(doc, R, use_cap=use_cap, use_window="act_window" in kinds, rd=rd)
        b = ev["budget"]
        if b is None or b["status"] not in ("approved", "requested"):
            bscore = R.wbudget["other"]
        elif b["annual_x12"] >= R.wbudget["min"]:
            bscore = R.wbudget[b["status"]]
        else:
            bscore = R.wbudget["small"]
        tgt = ev["target"]
        tscore = R.wtimeline_other
        if tgt is not None and (tgt - today).days >= 0:
            for lim, sc in R.wtimeline:
                if (tgt - today).days <= lim:
                    tscore = sc
                    break
        parts = {"fit": _band_value(R.fit_bands, size), "role": R.role_score[title],
                 "engagement": _band_value(R.eng_bands, act["points"]), "budget": bscore, "timeline": tscore}
        total = sum(R.weights[k] * parts[k] for k in R.weights)
        li = next(i for i, (lo, hi) in enumerate(R.level_bands) if total >= lo and (hi is None or total <= hi))
        if R.tiebreak_scores and li > 0 and total == R.level_bands[li][0] and bscore not in R.tiebreak_scores:
            li -= 1
        score, score_text = total, f"{total} weighted points"
    else:
        raise ParseError(R.archetype)
    if dq:
        li = 0
        if rd["disq_zero_score"]:
            score = 0
            score_text = re.sub(r"^-?\d+", "0", score_text)
    level = R.levels[li]
    ready = li >= R.levels.index(R.ready_level)
    return Result(R.archetype, score, score_text, level, li, ready, parts, dq)


# ------------------------------------------------------------------------------------------------ questions
_READY_Q = [
    r"Is this lead sales-ready according to the rubric\?",
    r"Does this lead meet the rubric's bar for going to the sales team\?",
    r"Is the lead at the rubric's sales-ready level or higher\?",
    r"Under the rubric, is the lead ready for the sales team\?",
    r"Is the lead qualified for hand-off to sales under the rubric's levels\?",
    r"Applying the rubric as of the scoring date, is the lead ready for the sales team\?",
    r"Does the rubric put this lead at or above its sales-ready level\?",
    r"Under the scoring rubric, does this lead reach the sales-ready level\?",
    r"Does the scoring rubric make this lead sales-ready\?",
    r"According to the rubric, should this lead go to the sales team now\?",
    r"Is this lead sales-ready under the rubric\?",
]
_JUDGE_Q = [
    r"A score of (?P<s>.+?) \((?P<l>.+)\) was recorded for this lead, with the reason listed\. Is the recorded score "
    r"supported by the rubric\?",
    r"Is the recorded score of (?P<s>.+?) \((?P<l>.+)\) for this lead, with its stated reason, consistent with the "
    r"scoring rubric\?",
    r"The CRM record shows a recorded score of (?P<s>.+?) \((?P<l>.+)\) for this lead\. Does the rubric support that "
    r"recorded score\?",
    r"The recorded score is (?P<s>.+?) \((?P<l>.+)\), with the reason given\. Is that score consistent with the "
    r"rubric\?",
    r"Given the rubric, is the recorded score \((?P<s>.+?) \((?P<l>.+)\)\) consistent with the lead's record\?",
]
_SCORE_Q = [
    r"Apply the lead scoring rubric: which level should this lead be assigned\?",
    r"Under the scoring rubric in the record, which level does this lead get\?",
    r"What qualification level does the rubric give this lead\?",
    r"When the rubric is applied to this record, which level does the lead reach\?",
    r"Which rubric level fits this lead as of the scoring date\?",
    r"Using only the rubric's rules, what is this lead's qualification level\?",
    r"According to the scoring rubric, at what level does this lead sit\?",
]
# JB-letter option texts: (yes-description, no-description)
_JB_PAIRS = [
    ("Hand the lead to the sales team now.", "Keep the lead out of the sales queue for now."),
    ("The rubric puts the lead at or above its sales-ready level.", "The rubric puts the lead below its sales-ready "
                                                                   "level."),
    ("yes, this holds", "no, this does not hold"),
    ("The lead is sales-ready under the rubric.", "The lead is not sales-ready under the rubric."),
    ("The lead meets the rubric's sales-ready bar.", "The lead does not meet the rubric's sales-ready bar."),
    ("Sales-ready under the rubric", "Not sales-ready under the rubric"),
]
_NEG_CUES = re.compile(r"\b(not|below|out of)\b", re.I)


def classify_question(instr: str, options: list) -> tuple:
    """-> ('score',) | ('ready',) | ('judge', score_text, level) | ('jb', yes_option, no_option)."""
    for p in _JUDGE_Q:
        m = re.fullmatch(p, instr)
        if m:
            return ("judge", m.group("s"), m.group("l"))
    ready = any(re.fullmatch(p, instr) for p in _READY_Q)
    if ready and options == ["yes", "no"]:
        return ("ready",)
    if ready and len(options) == 2:
        for a, b in _JB_PAIRS:
            if set(options) == {a, b}:
                return ("jb", a, b)
        # an unknown pair: read the polarity from negation cues (exactly one option negative)
        neg = [bool(_NEG_CUES.search(o)) for o in options]
        if sum(neg) != 1:
            raise ParseError(f"JB options polarity {options}")
        return ("jb", options[neg.index(False)], options[neg.index(True)])
    if any(re.fullmatch(p, instr) for p in _SCORE_Q):
        return ("score",)
    raise ParseError(f"unknown question {instr!r}")


def card_meaning(defs_id: str | None) -> str | None:
    """The yes/no card is shown to the model; check that 'yes' is the positive reading of the question.
    Returns 'ready' / 'judge' (what yes asserts) or None when the row has no card."""
    if not defs_id:
        return None
    d = json.loads((DEFS / f"{KEY}__{defs_id}.json").read_text())
    y = d["yes"]
    if re.search(r"recorded", y) and not re.search(r"\b(other|different)\b", y):
        return "judge"
    if re.search(r"sales-ready", y) and not re.search(r"\bbelow\b", y):
        return "ready"
    raise ParseError(f"card yes {y!r}")


# ------------------------------------------------------------------------------------------------ decide2
def reason_matches(res: Result, reason: str | None) -> bool | None:
    """Does a CRM 'Score reason' state the same components decide2 computes? None when there is no reason."""
    if reason is None:
        return None
    if res.archetype in ("points", "weighted"):
        got = {k: int(x) for k, x in re.findall(r"([a-z]+) (-?\d+)", reason)}
        mine = {k: x for k, x in res.parts.items() if not k.startswith("_")}
        return got == mine
    if res.archetype == "bant":
        got = {k: x == "met" for k, x in re.findall(r"([a-z]+) (met|not met)", reason)}
        return got == {k: res.parts[k] for k in ("budget", "authority", "need", "timeline")}
    got = [x == "passed" for _, x in re.findall(r"gate (\d+) (passed|failed)", reason)]
    return got == res.parts["gates"]


def solve(row: dict, readings: dict | None = None) -> dict:
    """Everything decide2 derives for one raw row (for reports and tests). Uses state, instructions and options."""
    rd = _rd(readings)
    doc = parse_state(row["state"])
    R = parse_rubric(doc.title, doc.rules, doc.scoring_date)
    res = evaluate(doc, R, rd)
    q = classify_question(row["instructions"], list(row["options"]))
    out = {"q": q[0], "result": res, "rubric": R, "doc": doc}
    if q[0] == "score":
        if list(row["options"]) != R.levels:
            raise ParseError(f"score options {row['options']} != rubric levels {R.levels}")
        out["gold2"] = res.level
    elif q[0] == "ready":
        out["gold2"] = "yes" if res.ready else "no"
    elif q[0] == "jb":
        out["gold2"] = q[1] if res.ready else q[2]
    elif q[0] == "judge":
        rec_s, rec_l = q[1], q[2]
        crm_s, crm_l = doc.crm.get("Recorded score"), doc.crm.get("Recorded level")
        if (crm_s, crm_l) != (rec_s, rec_l):
            raise ParseError(f"question record {rec_s!r}/{rec_l!r} != CRM {crm_s!r}/{crm_l!r}")
        if rec_l not in R.levels:
            raise ParseError(f"recorded level {rec_l!r} is not a rubric level")
        out["recorded"] = (rec_s, rec_l)
        out["reason"] = doc.crm.get("Score reason")
        out["reason_ok"] = reason_matches(res, out["reason"])
        ok = rec_s == res.score_text and rec_l == res.level
        if rd["judge_reason"] and out["reason_ok"] is False:
            ok = False
        out["gold2"] = "yes" if ok else "no"
    return out


def decide2_row(row: dict, readings: dict | None = None) -> str:
    """SPEC 8.1 decide2 on the rendered row: a level text, 'yes'/'no', or a JB option string. Raises ParseError when
    the row cannot be read (never guesses); mv_core.verify_labels counts that as a failure."""
    return solve(row, readings)["gold2"]


def decide2_row_safe(row: dict, readings: dict | None = None):
    """decide2_row for mv_core.verify_labels: ParseError -> mv_core.UNDEFINED (a failure there)."""
    try:
        return decide2_row(row, readings)
    except ParseError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import mv_core
        return mv_core.UNDEFINED


# ------------------------------------------------------------------------------------------------ reports
def load_rows(split: str = "train") -> list[dict]:
    p = RAW / (f"{KEY}.jsonl" if split == "train" else f"dev/{KEY}.jsonl")
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def load_rels(split: str = "train") -> list[dict]:
    p = RAW / ("relations" if split == "train" else "dev/relations") / f"{KEY}.jsonl"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def _key(r: dict) -> str:
    m = r["meta"]
    return f"{m.get('dev_kind') or m['split']}/{m['qkind']}/{m['view']}"


def agreement(rows: list[dict], readings: dict | None = None) -> dict:
    """decide2 vs the program gold, per (part, qkind, view)."""
    from collections import Counter, defaultdict
    tab = defaultdict(Counter)
    dis = []
    answers = {}
    for r in rows:
        try:
            g2, err = decide2_row(r, readings), None
        except ParseError as e:
            g2, err = None, str(e)
        answers[r["rid"]] = g2
        ok = g2 == r["gold"]
        tab[_key(r)]["rows"] += 1
        tab[_key(r)]["agree"] += int(ok)
        if not ok:
            dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": g2, "error": err, "qkind": r["meta"]["qkind"],
                        "view": r["meta"]["view"], "fmt": r["meta"]["fmt"]})
    n = len(rows)
    agree = n - len(dis)
    return {"rows": n, "agree": agree, "rate": round(agree / max(1, n), 6),
            "table": {k: dict(v) for k, v in sorted(tab.items())}, "disagreements": dis, "answers": answers}


def structure_under_decide2(rows: list[dict], rels: list[dict], answers: dict) -> dict:
    """SPEC 8.3 under decide2 alone: contrast twins flip, equiv views keep, inv (attack) twins keep the answer.
    Also: format twins (equiv) must parse to the same facts (a parse-back parity check across surfaces)."""
    by = {r["rid"]: r for r in rows}
    out = {"contrast_pairs": 0, "contrast_not_flipped": [], "equiv": 0, "equiv_changed": [], "inv": 0,
           "inv_changed": [], "format_fact_mismatch": [], "unknown_rel": []}
    for r in rows:
        tw = r["meta"].get("twin_of")
        if r["meta"]["view"] == "contrast" and tw:
            out["contrast_pairs"] += 1
            if answers.get(r["rid"]) is None or answers.get(r["rid"]) == answers.get(tw):
                out["contrast_not_flipped"].append(r["rid"])
    for rel in rels:
        a, b, t = rel["a"], rel["b"], rel["type"]
        if t == "equiv":
            out["equiv"] += 1
            if answers.get(a) != answers.get(b) or answers.get(a) is None:
                out["equiv_changed"].append((a, b))
            if by[a]["meta"]["fmt"] != by[b]["meta"]["fmt"]:
                fa, fb = _facts(by[a]["state"]), _facts(by[b]["state"])
                if fa != fb:
                    out["format_fact_mismatch"].append((a, b, sorted(k for k in fa if fa[k] != fb.get(k))))
        elif t == "inv":
            out["inv"] += 1
            if answers.get(a) != answers.get(b) or answers.get(a) is None:
                out["inv_changed"].append((a, b))
        else:
            out["unknown_rel"].append(rel)
    out["ok"] = not (out["contrast_not_flipped"] or out["equiv_changed"] or out["inv_changed"]
                     or out["format_fact_mismatch"] or out["unknown_rel"])
    return out


def _facts(state: str) -> dict:
    """A surface-free view of a parsed state (for format-parity checks)."""
    d = parse_state(state)
    ev = sorted((e.kind, e.time.isoformat(), e.who or "", e.lead or "", e.text) for e in d.events)
    return {"title": d.title, "rules": tuple(d.rules), "date": d.scoring_date, "lead": d.lead, "form": d.form,
            "crm": d.crm, "events": tuple(ev), "extra": d.extra}


ALT_READINGS = {
    "gate_score=consecutive": {"gate_score": "consecutive"},
    "judge_reason=True": {"judge_reason": True},
    "unsub_before_cap=True": {"unsub_before_cap": True},
    "latest_counting_budget=True": {"latest_counting_budget": True},
    "form_outside_window=True": {"form_outside_window": True},
    "rep_target_no_window=True": {"rep_target_no_window": True},
    "type_max_before_dedupe=True": {"type_max_before_dedupe": True},
    "need_substring=True": {"need_substring": True},
    "disq_zero_score=True": {"disq_zero_score": True},
    "probe:any_budget_counts": {"any_budget_counts": True},
    "probe:any_target_counts": {"any_target_counts": True},
    "probe:any_problem_counts": {"any_problem_counts": True},
}


def sensitivity(rows: list[dict], base_answers: dict) -> dict:
    """For each alternative reading: the rows whose decide2 answer changes, and how many of those the program gold
    agrees with under the alternative (i.e. which reading the generator follows)."""
    out = {}
    for name, rd in ALT_READINGS.items():
        changed, gold_follows_alt = [], 0
        for r in rows:
            try:
                a = decide2_row(r, rd)
            except ParseError:
                a = None
            if a != base_answers.get(r["rid"]):
                changed.append(r["rid"])
                gold_follows_alt += int(a == r["gold"])
        out[name] = {"changed": len(changed), "gold_follows_alt": gold_follows_alt, "rids": changed}
    return out


def judge_reason_report(rows: list[dict]) -> dict:
    """Judge rows whose CRM 'Score reason' contradicts the rubric while score and level match (gold yes by the
    card): the question text says 'with the reason given', so these read two ways."""
    from collections import Counter
    c, rids = Counter(), []
    for r in rows:
        try:
            o = solve(r)
        except ParseError:
            continue
        if o["q"] != "judge":
            continue
        c[(o["result"].archetype, o["gold2"], bool(o["reason_ok"]))] += 1
        if o["gold2"] == "yes" and o["reason_ok"] is False:
            rids.append((r["rid"], r["meta"].get("card_style")))
    return {"by_archetype_gold_reasonok": {"/".join(map(str, k)): v for k, v in sorted(c.items())},
            "yes_with_wrong_reason": rids}


def card_report(rows: list[dict]) -> dict:
    """yes/no rows: the card printed with the row (meta.defs -> yn2b_defs) must say that 'yes' is the positive
    answer to the question decide2 read (ready -> sales-ready card; judge -> recorded-score card)."""
    bad, n, none = [], 0, 0
    for r in rows:
        if r["meta"]["qkind"] != "yn":
            continue
        q = classify_question(r["instructions"], list(r["options"]))[0]
        if r["meta"].get("card_style") == "none":
            none += 1
            continue
        n += 1
        if card_meaning(r["meta"].get("defs")) != q:
            bad.append(r["rid"])
    return {"yn_rows_with_card": n, "yn_rows_without_card": none, "card_question_mismatch": bad}


def full_report() -> dict:
    rep = {}
    for split in ("train", "dev"):
        rows, rels = load_rows(split), load_rels(split)
        ag = agreement(rows)
        rep[split] = {"agreement": {k: v for k, v in ag.items() if k != "answers"},
                      "structure": structure_under_decide2(rows, rels, ag["answers"]),
                      "sensitivity": sensitivity(rows, ag["answers"]),
                      "judge_reason": judge_reason_report(rows), "cards": card_report(rows)}
    return rep


DIAGNOSES = {
    "gate_score": {
        "class": "ambiguous_item (generator-side fix needed)",
        "why": "Judge row on a gated rubric. The rubric never defines the score 'N of M gates passed'. decide2 counts "
               "every gate the lead passes; the generator counts the gates passed in order up to the first failed "
               "gate (the level index). The CRM 'Score reason' on the same row lists a later gate as passed, so under "
               "the literal reading the recorded count contradicts the record itself. Fix: state the definition in "
               "the Levels rule (e.g. 'The score counts the gates passed in order, stopping at the first gate "
               "failed') or render the individual count; then regenerate. Not a decide2 parse error: the answer "
               "equals the gold under gate_score='consecutive'.",
    },
}


def diagnose(row: dict) -> dict:
    """For a disagreement: which named reading (if any) reproduces the gold."""
    hits = [name for name, rd in ALT_READINGS.items() if not name.startswith("probe:")
            and _safe(row, rd) == row["gold"]]
    if "gate_score=consecutive" in hits:
        # (disq_zero_score may also reproduce a disqualified lead's gold here, but the gold follows the default
        #  'a disqualified lead keeps its computed score' on every other judge row; see the sensitivity table)
        return {"reading": hits, **DIAGNOSES["gate_score"]}
    if hits:
        return {"reading": hits, "class": "ambiguous_item", "why": "the gold follows another reading of the rubric"}
    return {"reading": [], "class": "unexplained (trace by hand: generator bug or solver bug)", "why": ""}


def _safe(row, rd=None):
    try:
        return decide2_row(row, rd)
    except ParseError:
        return None


def _rel(p: Path) -> str:
    p = Path(p).resolve()
    return str(p.relative_to(LEAN)) if p.is_relative_to(LEAN) else str(p)


def write_agreement(out_path: Path | None = None, manifest: bool = True) -> dict:
    """Writes yn2b/v3_lead_score_agreement.json (the SPEC 8.1 record for F5) and appends its sha256 to
    golden_src/gen3/MANIFEST_yn2b.jsonl. Reads the raw rows only; writes nothing under data/."""
    import hashlib
    import sys
    out_path = Path(out_path or LEAN / "yn2b" / "v3_lead_score_agreement.json")
    rep = {"tool": "golden_src/gen3/v3_lead_score.py", "key": KEY, "author": "builder D (independent of decide)",
           "readings": DEFAULT_READINGS, "inputs": {}, "parts": {}}
    for split in ("train", "dev"):
        p = RAW / (f"{KEY}.jsonl" if split == "train" else f"dev/{KEY}.jsonl")
        rows, rels = load_rows(split), load_rels(split)
        rep["inputs"][split] = {"path": str(p.relative_to(LEAN)), "rows": len(rows),
                                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        ag = agreement(rows)
        by = {r["rid"]: r for r in rows}
        for d in ag["disagreements"]:
            d["diagnosis"] = diagnose(by[d["rid"]])
        se = sensitivity(rows, ag["answers"])
        rep["parts"][split] = {
            "rows": ag["rows"], "agree": ag["agree"], "disagree": ag["rows"] - ag["agree"], "rate": ag["rate"],
            "by_part_qkind_view": ag["table"], "disagreements": ag["disagreements"],
            "structure": {k: v for k, v in structure_under_decide2(rows, rels, ag["answers"]).items()},
            "sensitivity": {k: {"changed": v["changed"], "gold_follows_alt": v["gold_follows_alt"],
                                "rids": v["rids"]} for k, v in se.items()},
            "judge_reason": judge_reason_report(rows), "cards": card_report(rows)}
    text = json.dumps(rep, indent=1, ensure_ascii=False, default=str) + "\n"
    out_path.write_text(text)
    if manifest:
        sys.path.insert(0, str(LEAN / "yn2b"))
        import yn2b_common as yc
        yc.manifest_append({"tool": "golden_src/gen3/v3_lead_score.py", "key": KEY, "part": "decide2_agreement",
                            "path": _rel(out_path), "rows": sum(v["rows"] for v in
                                                                                  rep["parts"].values()),
                            "sha256": hashlib.sha256(text.encode()).hexdigest(), "inputs": rep["inputs"],
                            "agree": {k: [v["agree"], v["rows"]] for k, v in rep["parts"].items()}})
    return rep


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", help="write the full report here (scratch path; never under data/)")
    ap.add_argument("--quick", action="store_true", help="agreement only")
    ap.add_argument("--write", action="store_true",
                    help="write yn2b/v3_lead_score_agreement.json and append its sha256 to MANIFEST_yn2b.jsonl")
    a = ap.parse_args(argv)
    if a.write:
        rep = write_agreement()
        for k, v in rep["parts"].items():
            print(f"{k}: {v['agree']}/{v['rows']} agree; disagreements {[d['rid'] for d in v['disagreements']]}")
        return rep
    rep = {}
    for split in ("train", "dev"):
        rows = load_rows(split)
        ag = agreement(rows)
        rep[split] = {"agreement": {k: v for k, v in ag.items() if k != "answers"}}
        print(f"== {split}: {ag['agree']}/{ag['rows']} agree ({100 * ag['rate']:.2f}%)")
        for k, v in ag["table"].items():
            print(f"  {k:28s} {v.get('agree', 0):5d}/{v['rows']:5d}")
        for d in ag["disagreements"]:
            print("  DIS", d)
        if a.quick:
            continue
        rels = load_rels(split)
        st = structure_under_decide2(rows, rels, ag["answers"])
        rep[split]["structure"] = st
        print(f"  structure: contrast {st['contrast_pairs']} (not flipped {len(st['contrast_not_flipped'])}), "
              f"equiv {st['equiv']} (changed {len(st['equiv_changed'])}), inv {st['inv']} "
              f"(changed {len(st['inv_changed'])}), format fact mismatches {len(st['format_fact_mismatch'])}")
        se = sensitivity(rows, ag["answers"])
        rep[split]["sensitivity"] = se
        for name, v in se.items():
            print(f"  reading {name:32s} changes {v['changed']:4d} rows; gold follows it on {v['gold_follows_alt']}"
                  + (f"  {v['rids'][:8]}" if v["changed"] else ""))
        jr = judge_reason_report(rows)
        rep[split]["judge_reason"] = jr
        print(f"  judge rows, gold yes but the stated reason contradicts the rubric: {len(jr['yes_with_wrong_reason'])}"
              f" {jr['yes_with_wrong_reason']}")
        cr = card_report(rows)
        rep[split]["cards"] = cr
        print(f"  cards: {cr['yn_rows_with_card']} yes/no rows with a card, {cr['yn_rows_without_card']} without; "
              f"card/question mismatches {cr['card_question_mismatch']}")
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1, default=str))
    return rep


if __name__ == "__main__":
    main()
