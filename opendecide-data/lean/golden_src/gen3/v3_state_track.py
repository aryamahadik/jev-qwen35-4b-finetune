"""F3 `gen3_state_track` decide2: an independent solver (SPEC 8.1, builder B).

It re-derives the gold of every F3 row from the RENDERED row only: the state text (16 renderers), the question,
and the options. It never reads the generator's decision logic (gen3_state_track.py, gen3_state_track_sim.py) and
uses no latent field: `meta` is read only by the report code (to count rows by split, machine and question kind),
never by the solver.

How it works:
  1. `parse_state(text)` detects the renderer from the text itself and returns a `Doc`: title, context lines, the
     numbered rules (with dates), the starting time and entities, the events (time in UTC, id, source, text,
     listing position), the agent record (judge rows) and the notes. Notes are an untrusted channel: the solver
     never reads them for facts.
  2. `machine_of(doc)` names the state machine from the title/system line; `params(doc)` reads every parameter
     the machine needs (rosters, admins, lapse hours, business hours, slot values, tickets, ...) from the rule
     texts with this module's own regexes. A rule text that no regex reads raises `SolverError` (never guessed).
  3. `typed(machine, event)` maps each event line to one typed update with this module's own regexes (a line
     that no regex reads raises `SolverError`).
  4. `World.at(T)` replays the typed events in timestamp order up to T on this module's own simulator, applying
     the stated rules: guards (rejected requests change nothing), ids that take effect at most once, reverts,
     expiries, look-alike ids, partial tool batches, dialogue references.
  5. `decide2_row(raw_row)` parses the question (yes/no, judge, JB statement pair or fallback pair, choice,
     mirror with "None of these", score levels) and maps the simulated value to the row's answer.

Run on all rows:  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/v3_state_track.py [--write-report]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
KEY = "gen3_state_track"
TRAIN_PATH = LEAN / "data/v14_parts/yn2b_raw" / f"{KEY}.jsonl"
DEV_PATH = LEAN / "data/v14_parts/yn2b_raw/dev" / f"{KEY}.jsonl"
REPORT_PATH = LEAN / "yn2b" / "v3_state_track_agreement.json"
MANIFEST = HERE / "MANIFEST_yn2b.jsonl"

try:  # the shared UNDEFINED sentinel, so mv_core.verify_labels treats our "cannot decide" correctly
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import mv_core as _mv  # noqa: E402  (shared engine only: no F3 decision logic lives there)
    UNDEFINED = _mv.UNDEFINED
except Exception:  # pragma: no cover - standalone use
    _mv = None

    class _Undef:
        def __repr__(self) -> str:
            return "UNDEFINED"

    UNDEFINED = _Undef()


class SolverError(Exception):
    """The solver cannot read or decide the row (never guessed)."""


class Ambiguous(SolverError):
    """The rendered text allows two readings that give different answers."""


# ---------------------------------------------------------------------------------------------------------------
# 1. Times
# ---------------------------------------------------------------------------------------------------------------
TIME_RE = r"\d{4}-\d\d-\d\d(?:T\d\d:\d\d:\d\d(?:Z|[+-]\d\d:\d\d)| \d\d:\d\d UTC(?:[+-]\d\d:\d\d)?)"
_TIME_FULL = re.compile(TIME_RE + r"$")


def parse_time(s: str) -> datetime:
    """ISO (`...T09:05:00Z`, `...T09:05:00+01:00`) or space style (`... 09:05 UTC`, `... 09:05 UTC+01:00`) -> UTC."""
    s = s.strip()
    if not _TIME_FULL.match(s):
        raise SolverError(f"bad time {s!r}")
    if re.match(r"\d{4}-\d\d-\d\dT", s):
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    else:
        m = re.match(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d) UTC(?:([+-])(\d\d):(\d\d))?$", s)
        d = datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:00")
        off = timedelta(0)
        if m.group(3):
            off = timedelta(hours=int(m.group(4)), minutes=int(m.group(5)))
            if m.group(3) == "-":
                off = -off
        d = d.replace(tzinfo=timezone(off))
    return d.astimezone(timezone.utc)


# ---------------------------------------------------------------------------------------------------------------
# 2. The rendered state -> Doc
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Event:
    t: datetime
    eid: str
    by: str
    text: str
    pos: int


@dataclass
class Doc:
    fmt: str
    title: str
    context: dict[str, str]
    rules: list[tuple[int, str, str]]
    start: datetime
    entities: list[tuple[str, dict[str, str]]]
    events: list[Event]
    record: tuple[datetime, list[str]] | None
    notes: list[str]


RULE_RE = re.compile(r"^R(\d+)\.? \(in force from (\d{4}-\d\d-\d\d)\) (.*)$")
# field names a starting-state entry can carry (prose needs them; other renderers only use them for checks)
KNOWN_FIELDS = ["status", "customer", "owner", "opened", "kind", "grants", "members", "item", "on hand", "holds",
                "quarantine", "confirmed booking", "hold", "holder", "posted balance", "pending",
                "quantity in cart", "folder", "production", "rollout", "kill switch", "bucket",
                "version 1 content", "lock"]


def _rule(line: str) -> tuple[int, str, str]:
    m = RULE_RE.match(line.strip())
    if not m:
        raise SolverError(f"bad rule line {line[:60]!r}")
    return int(m.group(1)), m.group(2), m.group(3)


def _entity_eq(line: str) -> tuple[str, dict[str, str]]:
    """`- ID: k = v, k = v` (values may hold ', ' as in member lists; keys are lowercase words)."""
    body = line[2:] if line.startswith("- ") else line
    ident, rest = body.split(": ", 1)
    parts = re.split(r", (?=[a-z][a-z0-9 ]* = )", rest)
    f = {}
    for p in parts:
        if " = " not in p:
            raise SolverError(f"bad entity field {p!r}")
        k, v = p.split(" = ", 1)
        f[k] = v
    return ident, f


def _entity_prose(chunk: str, extra_keys: list[str]) -> tuple[str, dict[str, str]]:
    """`ID (k v, k v)`: the keys are the known field names (longest first)."""
    m = re.match(r"^(.+?) \((.*)\)$", chunk)
    if not m:
        raise SolverError(f"bad prose entity {chunk!r}")
    ident, body = m.group(1), m.group(2)
    keys = sorted(set(KNOWN_FIELDS + extra_keys), key=len, reverse=True)
    kre = "|".join(re.escape(k) for k in keys)
    pieces = re.split(rf", (?=(?:{kre}) )", body)
    f = {}
    for p in pieces:
        km = re.match(rf"^({kre}) (.*)$", p)
        if not km:
            raise SolverError(f"bad prose field {p!r}")
        f[km.group(1)] = km.group(2)
    return ident, f


LOG_LINE = re.compile(rf"^(?P<time>{TIME_RE}) \[(?P<by>[^\]]+)\] #(?P<id>[EMC]\d+) (?P<text>.*)$")
GROUP_LINE = re.compile(rf"^(?P<time>{TIME_RE}) #(?P<id>[EMC]\d+) (?P<text>.*)$")
CHAT_LINE = re.compile(rf"^\[(?P<time>{TIME_RE})\] (?P<by>.+?) \((?P<id>[EMC]\d+)\): (?P<text>.*)$")
PROSE_EV = re.compile(rf"At (?P<time>{TIME_RE}), (?P<by>[^,]+?) logged (?P<id>[EMC]\d+): ")


def _record_head(line: str) -> datetime:
    m = re.search(r"\(written at (.+?)\)", line)
    if not m:
        raise SolverError(f"bad record head {line!r}")
    return parse_time(m.group(1))


def _bullets(lines: list[str]) -> list[str]:
    return [ln[2:] for ln in lines if ln.startswith("- ")]


def parse_state(text: str, slot_keys: list[str] | None = None) -> Doc:
    """Detect the renderer from the text and parse it. `slot_keys` adds dialogue slot names for prose entities."""
    extra = slot_keys or []
    if text.startswith("{"):
        return _parse_json(text)
    if text.startswith("title: "):
        return _parse_kv(text)
    if text.startswith("# "):
        return _parse_md(text)
    return _parse_plain(text, extra)


def _parse_json(text: str) -> Doc:
    d = json.loads(text)
    if set(d) != {"title", "context", "rules", "starting_state", "events", "agent_record", "notes"}:
        raise SolverError(f"json keys {sorted(d)}")
    ents = []
    for e in d["starting_state"]["entries"]:
        e = dict(e)
        ents.append((e.pop("id"), {k: str(v) for k, v in e.items()}))
    evs = [Event(parse_time(e["time"]), e["id"], e["by"], e["event"], i) for i, e in enumerate(d["events"])]
    rec = None
    if d["agent_record"] is not None:
        rec = (parse_time(d["agent_record"]["written_at"]), list(d["agent_record"]["entries"]))
    return Doc("json", d["title"], dict(d["context"]), [_rule(r) for r in d["rules"]],
               parse_time(d["starting_state"]["as_of"]), ents, evs, rec, list(d["notes"]))


def _parse_kv(text: str) -> Doc:
    kv: list[tuple[str, str]] = []
    for ln in text.split("\n"):
        if ": " not in ln:
            raise SolverError(f"bad kv line {ln!r}")
        k, v = ln.split(": ", 1)
        kv.append((k, v))
    title, ctx, rules, notes = "", {}, [], []
    start = None
    ents: dict[int, tuple[str, dict[str, str]]] = {}
    evs: dict[int, dict[str, str]] = {}
    rec_t, rec_e = None, {}
    for k, v in kv:
        if k == "title":
            title = v
        elif k.startswith("context."):
            ctx[k[len("context."):]] = v
        elif k.startswith("rules."):
            rules.append(_rule(v))
        elif k == "starting_state.as_of":
            start = parse_time(v)
        elif k.startswith("starting_state.entries."):
            _, _, n, fld = k.split(".", 3)
            ident, f = ents.setdefault(int(n), ("", {}))
            if fld == "id":
                ents[int(n)] = (v, f)
            else:
                f[fld] = v
        elif k.startswith("events."):
            _, n, fld = k.split(".", 2)
            evs.setdefault(int(n), {})[fld] = v
        elif k == "agent_record":
            if v != "none":
                raise SolverError("kv agent_record")
        elif k == "agent_record.written_at":
            rec_t = parse_time(v)
        elif k.startswith("agent_record.entries."):
            rec_e[int(k.rsplit(".", 1)[1])] = v
        elif k.startswith("notes."):
            notes.append(v)
        else:
            raise SolverError(f"kv key {k!r}")
    events = [Event(parse_time(e["time"]), e["id"], e["by"], e["event"], i)
              for i, (_, e) in enumerate(sorted(evs.items()))]
    rec = (rec_t, [rec_e[i] for i in sorted(rec_e)]) if rec_t else None
    return Doc("kv", title, ctx, rules, start, [ents[i] for i in sorted(ents)], events, rec, notes)


def _parse_md(text: str) -> Doc:
    lines = text.split("\n")
    title = lines[0][2:]
    sec: dict[str, list[str]] = defaultdict(list)
    heads: dict[str, str] = {}
    cur = None
    for ln in lines[1:]:
        if ln.startswith("## "):
            cur = ln[3:]
            heads[cur.split(" (")[0].split(" at ")[0]] = cur
            continue
        if ln.strip():
            sec[cur].append(ln)
    ctx = dict(b.split(": ", 1) for b in _bullets(sec["Context"]))
    rules = [_rule(ln) for ln in sec["Rules"]]
    sh = heads["Starting state"]
    start = parse_time(sh[len("Starting state at "):])
    ents = [_entity_eq("- " + b) for b in _bullets(sec[sh])]
    evs = []
    for i, b in enumerate(_bullets(sec["Events"])):
        t, eid, by, txt = b.split(" | ", 3)
        evs.append(Event(parse_time(t), eid, by, txt, i))
    rec = None
    if "Agent record" in heads:
        h = heads["Agent record"]
        rec = (_record_head(h), _bullets(sec[h]))
    return Doc("markdown", title, ctx, rules, start, ents, evs, rec, _bullets(sec["Notes"]))


def _parse_plain(text: str, extra: list[str]) -> Doc:
    lines = text.split("\n")
    title = lines[0]
    i = 1
    ctx_lines = []
    while i < len(lines) and lines[i]:
        ctx_lines.append(lines[i])
        i += 1
    prose = "\nWhat happened:\n" in text
    ctx: dict[str, str] = {}
    if prose:
        if len(ctx_lines) != 1 or not ctx_lines[0].endswith("."):
            raise SolverError("prose context")
        for p in ctx_lines[0][:-1].split("; "):
            k, v = p.split(": ", 1)
            ctx[k] = v
    else:
        for c in ctx_lines:
            k, v = c.split(": ", 1)
            ctx[k] = v
    body = lines[i:]
    # blocks separated by headings
    rules, ents, evs, rec, notes = [], [], [], None, []
    start = None
    fmt = "?"
    j = 0

    def block(j0: int) -> tuple[list[str], int]:
        out = []
        j1 = j0
        while j1 < len(body) and not _is_head(body[j1]):
            out.append(body[j1])
            j1 += 1
        return out, j1

    while j < len(body):
        ln = body[j]
        if not ln:
            j += 1
            continue
        if ln == "Rules:":
            b, j = block(j + 1)
            rules = [_rule(x) for x in b if x]
        elif ln.startswith("Starting state at "):
            start = parse_time(ln[len("Starting state at "):-1])
            b, j = block(j + 1)
            ents = [_entity_eq(x) for x in b if x]
        elif ln.startswith("At ") and " the starting state was: " in ln:
            m = re.match(rf"^At ({TIME_RE}) the starting state was: (.*)\.$", ln)
            if not m:
                raise SolverError("prose start")
            start = parse_time(m.group(1))
            # dialogue slot names are field names too; they are listed in the rules printed above
            keys = list(extra)
            for _, _, rt in rules:
                sm = re.match(r"Slots and their allowed values: (.+)\.$", rt)
                if sm:
                    keys += [x.split(": ", 1)[0] for x in sm.group(1).split("; ")]
            ents = [_entity_prose(c, keys) for c in re.split(r"(?<=\)); ", m.group(2))]
            j += 1
        elif ln in ("Event log:", "Message thread:", "Transcript:", "Event table:", "What happened:"):
            b, j = block(j + 1)
            fmt, evs = _plain_events(ln, [x for x in b])
        elif ln.startswith("Agent record (written at "):
            t = _record_head(ln)
            b, j = block(j + 1)
            rec = (t, _bullets([x for x in b if x]))
        elif ln == "Notes:":
            b, j = block(j + 1)
            notes = _bullets([x for x in b if x])
        else:
            raise SolverError(f"unexpected line {ln[:60]!r}")
    if start is None:
        raise SolverError("no starting state")
    return Doc(fmt, title, ctx, rules, start, ents, evs, rec, notes)


def _is_head(ln: str) -> bool:
    return (ln in ("Rules:", "Event log:", "Message thread:", "Transcript:", "Event table:", "What happened:",
                   "Notes:") or ln.startswith("Starting state at ") or ln.startswith("Agent record (written at ")
            or (ln.startswith("At ") and " the starting state was: " in ln))


def _plain_events(head: str, b: list[str]) -> tuple[str, list[Event]]:
    evs: list[Event] = []
    if head == "Event log:":
        grouped = any(x.startswith("== ") for x in b)
        by = None
        for x in b:
            if not x:
                continue
            if grouped:
                if x.startswith("== ") and x.endswith(" =="):
                    by = x[3:-3]
                    continue
                m = GROUP_LINE.match(x)
                if not m or by is None:
                    raise SolverError(f"bad grouped line {x!r}")
                evs.append(Event(parse_time(m["time"]), m["id"], by, m["text"], len(evs)))
            else:
                m = LOG_LINE.match(x)
                if not m:
                    raise SolverError(f"bad log line {x!r}")
                evs.append(Event(parse_time(m["time"]), m["id"], m["by"], m["text"], len(evs)))
        return ("log:grouped" if grouped else "log"), evs
    if head == "Transcript:":
        for x in b:
            if not x:
                continue
            m = CHAT_LINE.match(x)
            if not m:
                raise SolverError(f"bad chat line {x!r}")
            evs.append(Event(parse_time(m["time"]), m["id"], m["by"], m["text"], len(evs)))
        return "chat", evs
    if head == "Message thread:":
        blocks, cur = [], []
        for x in b:
            if x == "-" * 10:
                blocks.append(cur)
                cur = []
            else:
                cur.append(x)
        blocks.append(cur)
        for bl in blocks:
            bl = [x for x in bl if x]
            if len(bl) != 4 or not bl[0].startswith("From: ") or not bl[1].startswith("Date: ") \
                    or not bl[2].startswith("Subject: event "):
                raise SolverError(f"bad email block {bl!r}")
            evs.append(Event(parse_time(bl[1][6:]), bl[2][len("Subject: event "):], bl[0][6:], bl[3], len(evs)))
        return "email", evs
    if head == "Event table:":
        rows = [x for x in b if x]
        if rows and rows[0] == "time,id,by,event":
            for rec in csv.reader(io.StringIO("\n".join(rows[1:]))):
                if len(rec) != 4:
                    raise SolverError(f"bad csv {rec!r}")
                evs.append(Event(parse_time(rec[0]), rec[1], rec[2], rec[3], len(evs)))
            return "table:csv", evs
        if rows and rows[0] == "| time | id | by | event |":
            for x in rows[2:]:
                if not (x.startswith("| ") and x.endswith(" |")):
                    raise SolverError(f"bad md row {x!r}")
                t, eid, by, txt = x[2:-2].split(" | ", 3)
                evs.append(Event(parse_time(t), eid, by, txt, len(evs)))
            return "table:md", evs
        for x in rows:
            m = re.match(rf"^- time: ({TIME_RE}); id: ([EMC]\d+); by: (.+?); event: (.*)$", x)
            if not m:
                raise SolverError(f"bad record row {x!r}")
            evs.append(Event(parse_time(m.group(1)), m.group(2), m.group(3), m.group(4), len(evs)))
        return "table:records", evs
    if head == "What happened:":
        txt = " ".join(x for x in b if x)
        ms = list(PROSE_EV.finditer(txt))
        if not ms or ms[0].start() != 0:
            raise SolverError("bad prose events")
        for k, m in enumerate(ms):
            end = ms[k + 1].start() if k + 1 < len(ms) else len(txt)
            body = txt[m.end():end].rstrip(" ")
            if not body.endswith((".", "?", "!")):
                raise SolverError(f"prose sentence without end {body!r}")
            evs.append(Event(parse_time(m["time"]), m["id"], m["by"], body, len(evs)))
        return "prose", evs
    raise SolverError(head)


# ---------------------------------------------------------------------------------------------------------------
# 3. Machine and rule parameters
# ---------------------------------------------------------------------------------------------------------------
TITLES = {"order event log": "orders", "ticket event log": "tickets", "resource event log": "access",
          "SKU event log": "inventory", "slot event log": "bookings", "account event log": "ledger",
          "booking event log": "dialogue", "item event log": "agent", "flag event log": "flags",
          "document event log": "docs"}


def machine_of(doc: Doc) -> str:
    suf = doc.title.split(" - ", 1)[1] if " - " in doc.title else ""
    if suf not in TITLES:
        raise SolverError(f"unknown title {doc.title!r}")
    return TITLES[suf]


def _names(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def rules_text(doc: Doc) -> list[str]:
    return [t for _, _, t in doc.rules]


def _find(doc: Doc, pat: str, flags=0) -> re.Match | None:
    for t in rules_text(doc):
        m = re.search(pat, t, flags)
        if m:
            return m
    return None


def _need(doc: Doc, pat: str) -> re.Match:
    m = _find(doc, pat)
    if not m:
        raise SolverError(f"rule not found: {pat}")
    return m


def params(doc: Doc, mach: str) -> dict[str, Any]:
    p: dict[str, Any] = {}
    txt = " ".join(rules_text(doc))
    if mach == "tickets":
        p["roster"] = _names(_need(doc, r"only to a person on the support roster: (.+)\.$").group(1))
        m = _need(doc, r"Resolution is due (\d+) business hours after the ticket was opened\. Business hours are "
                       r"(\d\d):(\d\d) to (\d\d):(\d\d) local time in (\S+), Monday to Friday, except these "
                       r"holidays: (.+)\.$")
        p["due_hours"] = int(m.group(1))
        p["open"] = (int(m.group(2)), int(m.group(3)))
        p["close"] = (int(m.group(4)), int(m.group(5)))
        p["tz"] = ZoneInfo(m.group(6))
        hol = m.group(7)
        p["holidays"] = set() if hol == "none listed" else {date.fromisoformat(x) for x in re.findall(
            r"\d{4}-\d\d-\d\d", hol)}
        if hol != "none listed" and not p["holidays"]:
            raise SolverError("holidays")
        m = _need(doc, r"Escalation level at a stated time: level 0 if the ticket is not overdue; otherwise measure "
                       r"the business time from the due time to its first resolution \(or to the stated time, if it "
                       r"was not resolved by then\): under (\d+) business hours is level 1, (\d+) to under (\d+) is "
                       r"level 2, (\d+) to under (\d+) is level 3, and (\d+) or more is level 4\.")
        a, b1, b2, c1, c2, d1 = (int(m.group(k)) for k in range(1, 7))
        if not (a == b1 and b2 == c1 and c2 == d1):
            raise SolverError("escalation thresholds")
        p["esc"] = (a, b2, c2)
    elif mach == "access":
        p["admins"] = _names(_need(doc, r"Only these admins may change access: (.+?)\. A change logged by anyone "
                                        r"else is rejected").group(1))
        p["tracked"] = _names(doc.context["people tracked"])
    elif mach == "inventory":
        _need(doc, r"it stops counting at its start time plus those minutes \(it no longer counts at exactly that "
                   r"time\), or when it is released")
        _need(doc, r"a clear returns quarantined units \(only up to the number in quarantine\)")
    elif mach == "bookings":
        p["default_minutes"] = int(_need(doc, r"for the stated minutes \(default (\d+)\)").group(1))
    elif mach == "ledger":
        p["lapse_hours"] = int(_need(doc, r"it lapses (\d+) hours after it was made \(it no longer counts at "
                                          r"exactly that time\)").group(1))
        p["currency"] = _need(doc, r"^Amounts are in ([A-Z]{3})\.").group(1)
    elif mach == "dialogue":
        m = _need(doc, r"^Slots and their allowed values: (.+)\.$")
        slots: dict[str, list[str]] = {}
        for part in m.group(1).split("; "):
            k, v = part.split(": ", 1)
            slots[k] = _names(v)
        p["slots"] = slots
        p["booking"] = _need(doc, r"requests about booking (\S+) change its slots").group(1)
    elif mach == "agent":
        p["kind"] = "cart" if "shopping cart" in doc.context.get("system", "") else (
            "files" if "file store" in doc.context.get("system", "") else None)
        if p["kind"] is None:
            raise SolverError("agent kind")
    elif mach == "flags":
        p["tickets"] = set(re.findall(r"CHG-\d+", _need(doc, r"take effect only with an approved change ticket: "
                                                                r"(.+?)\. Anything else").group(1)))
    elif mach == "docs":
        p["lock_minutes"] = int(_need(doc, r"A lock gives one person sole editing for (\d+) minutes from the lock "
                                           r"time").group(1))
        p["approvers"] = _names(_need(doc, r"Only these approvers can approve a version: (.+?)\. An approval by "
                                           r"anyone else").group(1))
    # rules every machine states (checked, so a renderer change cannot slip past)
    if mach in ("orders", "tickets", "access", "inventory", "bookings", "ledger", "flags", "docs"):
        if not re.search(r"(Events take effect in timestamp order|Changes apply in the order of their timestamps)",
                         txt):
            raise SolverError("time order rule")
    p["_text"] = txt
    return p


# ---------------------------------------------------------------------------------------------------------------
# 4. Event lines -> typed updates
# ---------------------------------------------------------------------------------------------------------------
P = r"(?P<p>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+)"  # a person name
AMT = r"(?P<amt>-?[\d,]+\.\d\d) (?P<cur>[A-Z]{3})"
U = r"(?P<n>\d+) units?"


def _m(pats: list[tuple[str, str]], text: str) -> tuple[str, dict[str, str]] | None:
    for kind, pat in pats:
        m = re.match(pat + r"\.?$", text)
        if m:
            return kind, {k: v for k, v in m.groupdict().items() if v is not None}
    return None


REVERT_PATS = [
    ("revert", r"revert event=(?P<ref>E\d+)"),
    ("revert", r"Operator reverted event (?P<ref>E\d+)"),
    ("revert", r"Undo of event (?P<ref>E\d+) requested"),
    ("revert", r"Front desk reverted event (?P<ref>E\d+)"),
    ("revert", r"Reversal of event (?P<ref>E\d+) posted"),
]

TYPED: dict[str, list[tuple[str, str]]] = {
    "orders": [
        ("pay", r"pay order=(?P<id>\S+?)"), ("pay", r"Payment captured for order (?P<id>\S+?)"),
        ("pay", r"Order (?P<id>\S+): the card payment went through"),
        ("pack", r"pack order=(?P<id>\S+?)"), ("pack", r"Warehouse finished packing order (?P<id>\S+?)"),
        ("pack", r"Order (?P<id>\S+) is boxed and labelled"),
        ("ship", r"ship order=(?P<id>\S+?)"), ("ship", r"Carrier collected order (?P<id>\S+?)"),
        ("ship", r"Order (?P<id>\S+) was handed to the courier"),
        ("deliver", r"deliver order=(?P<id>\S+?)"), ("deliver", r"Courier reports order (?P<id>\S+) delivered"),
        ("deliver", r"Order (?P<id>\S+) reached the customer"),
        ("cancel", r"cancel order=(?P<id>\S+?)"), ("cancel", r"Cancellation requested for order (?P<id>\S+?)"),
        ("cancel", r"Customer asked to cancel order (?P<id>\S+?)"),
        ("return", r"return order=(?P<id>\S+?)"), ("return", r"Order (?P<id>\S+) came back as a return"),
        ("return", r"Returned parcel for order (?P<id>\S+) checked in"),
    ] + REVERT_PATS,
    "tickets": [
        ("assign", r"assign ticket=(?P<id>\S+) owner=" + P), ("assign", r"Ticket (?P<id>\S+) assigned to " + P),
        ("assign", P + r" now owns ticket (?P<id>\S+?)"),
        ("start", r"start ticket=(?P<id>\S+?)"), ("start", r"Work started on ticket (?P<id>\S+?)"),
        ("start", r"Ticket (?P<id>\S+) picked up by its owner"),
        ("wait", r"wait ticket=(?P<id>\S+?)"), ("wait", r"Ticket (?P<id>\S+) is waiting on the customer"),
        ("wait", r"Asked the customer for details on ticket (?P<id>\S+?)"),
        ("resume", r"resume ticket=(?P<id>\S+?)"), ("resume", r"Customer answered on ticket (?P<id>\S+?)"),
        ("resume", r"New customer message on ticket (?P<id>\S+?)"),
        ("resolve", r"resolve ticket=(?P<id>\S+?)"), ("resolve", r"Ticket (?P<id>\S+) marked resolved"),
        ("resolve", r"Fix confirmed for ticket (?P<id>\S+?)"),
        ("reopen", r"reopen ticket=(?P<id>\S+?)"), ("reopen", r"Ticket (?P<id>\S+) reopened"),
        ("reopen", r"Customer reopened ticket (?P<id>\S+?)"),
        ("close", r"close ticket=(?P<id>\S+?)"), ("close", r"Ticket (?P<id>\S+) closed after review"),
        ("close", r"Review done, ticket (?P<id>\S+) closed"),
    ] + REVERT_PATS,
    "bookings": [
        ("hold", r"hold slot=(?P<id>\S+) user=" + P + r"(?: minutes=(?P<min>\d+))?"),
        ("hold", P + r" put a (?P<min>\d+)-minute hold on (?P<id>\S+?)"),
        ("hold", P + r" put a hold on (?P<id>\S+?)"),
        ("hold", r"Hold on (?P<id>\S+) for " + P + r", valid (?P<min>\d+) minutes"),
        ("hold", r"Hold on (?P<id>\S+) for " + P),
        ("confirm", r"confirm slot=(?P<id>\S+) user=" + P), ("confirm", P + r" confirmed the booking of (?P<id>\S+?)"),
        ("confirm", r"Booking of (?P<id>\S+) confirmed by " + P),
        ("cancel", r"cancel slot=(?P<id>\S+) user=" + P), ("cancel", P + r" cancelled the booking of (?P<id>\S+?)"),
        ("cancel", r"Booking of (?P<id>\S+) cancelled by " + P),
        ("release", r"release slot=(?P<id>\S+) user=" + P), ("release", P + r" released the hold on (?P<id>\S+?)"),
        ("release", P + r" let the hold on (?P<id>\S+) go"),
    ] + REVERT_PATS,
    "inventory": [
        ("receive", r"receive sku=(?P<id>\S+) qty=(?P<n>\d+)"), ("receive", r"Received " + U + r" of (?P<id>\S+) at the dock"),
        ("receive", r"Inbound pallet: " + U + r" of (?P<id>\S+) put away"),
        ("ship", r"ship sku=(?P<id>\S+) qty=(?P<n>\d+)"), ("ship", r"Picked and shipped " + U + r" of (?P<id>\S+?)"),
        ("ship", U + r" of (?P<id>\S+) left on an outbound order"),
        ("hold", r"hold sku=(?P<id>\S+) qty=(?P<n>\d+) minutes=(?P<min>\d+)"),
        ("hold", r"Reserved " + U + r" of (?P<id>\S+) for (?P<min>\d+) minutes"),
        ("hold", r"Hold placed: " + U + r" of (?P<id>\S+), valid (?P<min>\d+) minutes"),
        ("release", r"release hold=(?P<ref>E\d+)"), ("release", r"Hold (?P<ref>E\d+) released"),
        ("release", r"Customer dropped the reservation made in event (?P<ref>E\d+)"),
        ("quarantine", r"quarantine sku=(?P<id>\S+) qty=(?P<n>\d+)"),
        ("quarantine", U + r" of (?P<id>\S+) moved to quarantine"),
        ("quarantine", r"Quality flagged " + U + r" of (?P<id>\S+) for quarantine"),
        ("clear", r"clear_quarantine sku=(?P<id>\S+) qty=(?P<n>\d+)"),
        ("clear", r"(?P<n>\d+) quarantined units? of (?P<id>\S+) cleared for sale"),
        ("clear", r"Quality released " + U + r" of (?P<id>\S+) from quarantine"),
        ("count", r"count sku=(?P<id>\S+) on_hand=(?P<n>\d+)"),
        ("count", r"Cycle count: (?P<id>\S+) has " + U + r" on hand"),
        ("count", r"Shelf count for (?P<id>\S+) came to " + U),
    ] + REVERT_PATS,
    "ledger": [
        ("deposit", r"deposit account=(?P<id>\S+) amount=" + AMT), ("deposit", AMT + r" credited to account (?P<id>\S+?)"),
        ("deposit", r"Incoming payment of " + AMT + r" to (?P<id>\S+) settled"),
        ("fee", r"fee account=(?P<id>\S+) amount=" + AMT), ("fee", r"Monthly fee of " + AMT + r" charged to (?P<id>\S+?)"),
        ("fee", r"Service charge of " + AMT + r" booked on (?P<id>\S+?)"),
        ("transfer", r"transfer_out account=(?P<id>\S+) amount=" + AMT),
        ("transfer", r"Transfer of " + AMT + r" sent from (?P<id>\S+?)"),
        ("transfer", r"(?P<id>\S+) paid out " + AMT + r" by transfer"),
        ("auth", r"authorise account=(?P<id>\S+) amount=" + AMT), ("auth", r"Card authorisation of " + AMT + r" on (?P<id>\S+?)"),
        ("auth", r"Merchant hold of " + AMT + r" placed on account (?P<id>\S+?)"),
        ("post", r"post auth=(?P<ref>E\d+)"), ("post", r"Authorisation (?P<ref>E\d+) posted"),
        ("post", r"Merchant settled the hold from event (?P<ref>E\d+)"),
        ("revert", r"reverse event=(?P<ref>E\d+)"), ("revert", r"Reversal of event (?P<ref>E\d+) booked"),
        ("revert", r"Event (?P<ref>E\d+) reversed by the bank"),
    ],
    "access": [
        ("grant", r"grant role=(?P<role>viewer|editor|owner) to=(?P<to>.+?) resource=(?P<id>\S+?)(?: hours=(?P<h>\d+))?"),
        ("grant", r"(?P<to>.+?) was granted (?P<role>viewer|editor|owner) access to (?P<id>\S+?)(?: for (?P<h>\d+) hours?)?"),
        ("grant", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) gave (?P<to>.+?) the (?P<role>viewer|editor|owner) role on "
                  r"(?P<id>\S+?)(?: for (?P<h>\d+) hours?)?"),
        ("revoke", r"revoke grant=(?P<ref>E\d+)"),
        ("revoke", r"(?P<actor>.+?) revoked the grant made in event (?P<ref>E\d+)"),
        ("revoke", r"Grant (?P<ref>E\d+) withdrawn by (?P<actor>.+?)"),
        ("deny", r"deny user=" + P + r" resource=(?P<id>\S+?)"),
        ("deny", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) blocked " + P + r" from (?P<id>\S+?)"),
        ("deny", r"Deny rule added: " + P + r" on (?P<id>\S+?)"),
        ("lift", r"lift_deny user=" + P + r" resource=(?P<id>\S+?)"),
        ("lift", r"Deny rule for " + P + r" on (?P<id>\S+) removed"),
        ("lift", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) lifted the block on " + P + r" for (?P<id>\S+?)"),
        ("add", r"add_member user=" + P + r" group=(?P<g>\S+?)"),
        ("add", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) added " + P + r" to group (?P<g>\S+?)"),
        ("add", P + r" joined group (?P<g>\S+?)"),
        ("remove", r"remove_member user=" + P + r" group=(?P<g>\S+?)"),
        ("remove", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) removed " + P + r" from group (?P<g>\S+?)"),
        ("remove", P + r" left group (?P<g>\S+?)"),
        ("rename", r"rename_group from=(?P<g>\S+) to=(?P<g2>\S+?)"),
        ("rename", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) renamed group (?P<g>\S+) to (?P<g2>\S+?)"),
        ("rename", r"Group (?P<g>\S+) is now called (?P<g2>\S+?)"),
    ],
    "flags": [
        ("enable", r"enable flag=(?P<id>\S+) env=(?P<env>production|staging) change=(?P<chg>CHG-\d+|no change ticket)"),
        ("enable", r"(?P<actor>.+?) switched (?P<id>\S+) on in (?P<env>production|staging) \((?P<chg>[^)]+)\)"),
        ("enable", r"(?P<id>\S+) enabled for (?P<env>production|staging) under (?P<chg>CHG-\d+|no change ticket) by (?P<actor>.+?)"),
        ("disable", r"disable flag=(?P<id>\S+) env=(?P<env>production|staging) change=(?P<chg>CHG-\d+|no change ticket)"),
        ("disable", r"(?P<actor>.+?) switched (?P<id>\S+) off in (?P<env>production|staging) \((?P<chg>[^)]+)\)"),
        ("disable", r"(?P<id>\S+) disabled for (?P<env>production|staging) under (?P<chg>CHG-\d+|no change ticket) by (?P<actor>.+?)"),
        ("rollout", r"set_rollout flag=(?P<id>\S+) env=(?P<env>production|staging) percent=(?P<pct>\d+) "
                    r"change=(?P<chg>CHG-\d+|no change ticket)"),
        ("rollout", r"(?P<actor>.+?) set the (?P<env>production|staging) rollout of (?P<id>\S+) to (?P<pct>\d+)% "
                    r"\((?P<chg>[^)]+)\)"),
        ("rollout", r"Rollout of (?P<id>\S+) in (?P<env>production|staging) is now (?P<pct>\d+)% per (?P<chg>CHG-\d+|no change ticket)"),
        ("kill", r"kill flag=(?P<id>\S+?)"), ("kill", r"(?P<actor>.+?) hit the kill switch on (?P<id>\S+?)"),
        ("kill", r"Emergency stop engaged for (?P<id>\S+) by (?P<actor>.+?)"),
        ("unkill", r"unkill flag=(?P<id>\S+) change=(?P<chg>CHG-\d+|no change ticket)"),
        ("unkill", r"(?P<actor>.+?) cleared the kill switch on (?P<id>\S+) \((?P<chg>[^)]+)\)"),
        ("unkill", r"Emergency stop on (?P<id>\S+) lifted under (?P<chg>CHG-\d+|no change ticket) by (?P<actor>.+?)"),
        ("override", r"override flag=(?P<id>\S+) user=" + P + r" value=(?P<val>on|off) hours=(?P<h>\d+)"),
        ("override", r"(?P<actor>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+) forced (?P<id>\S+) (?P<val>on|off) for " + P
         + r" for (?P<h>\d+) hours?"),
        ("override", r"Temporary override: (?P<id>\S+) (?P<val>on|off) for " + P + r", (?P<h>\d+) hours?"),
        ("revert", r"revert event=(?P<ref>E\d+)"), ("revert", r"(?P<actor>\S+) reverted event (?P<ref>E\d+)"),
        ("revert", r"Undo of event (?P<ref>E\d+) requested by (?P<actor>\S+?)"),
    ],
    "docs": [
        ("save", r'save doc=(?P<id>\S+) content="(?P<c>[^"]+)"'),
        ("save", r'(?P<actor>.+?) saved a new version of (?P<id>\S+): "(?P<c>[^"]+)"'),
        ("save", r'New version of (?P<id>\S+) uploaded by (?P<actor>.+?) \("(?P<c>[^"]+)"\)'),
        ("restore", r"restore doc=(?P<id>\S+) version=(?P<k>\d+)"),
        ("restore", r"(?P<actor>.+?) restored version (?P<k>\d+) of (?P<id>\S+) as a new version"),
        ("restore", r"(?P<id>\S+): version (?P<k>\d+) brought back by (?P<actor>.+?)"),
        ("lock", r"lock doc=(?P<id>\S+?)"), ("lock", r"(?P<actor>.+?) locked (?P<id>\S+) for editing"),
        ("lock", r"(?P<id>\S+) checked out by (?P<actor>.+?)"),
        ("unlock", r"unlock doc=(?P<id>\S+?)"), ("unlock", r"(?P<actor>.+?) unlocked (?P<id>\S+?)"),
        ("unlock", r"(?P<id>\S+) checked back in by (?P<actor>.+?)"),
        ("approve", r"approve doc=(?P<id>\S+) version=(?P<k>\d+)"),
        ("approve", r"(?P<actor>.+?) approved version (?P<k>\d+) of (?P<id>\S+?)"),
        ("approve", r"Version (?P<k>\d+) of (?P<id>\S+) signed off by (?P<actor>.+?)"),
    ],
}


def typed(mach: str, ev: Event, prm: dict[str, Any]) -> tuple[str, dict[str, str]]:
    if mach == "agent":
        return _typed_agent(ev.text, prm)
    if mach == "dialogue":
        return _typed_dialogue(ev, prm)
    r = _m(TYPED[mach], ev.text)
    if r is None:
        raise SolverError(f"{mach}: unread event line {ev.text!r}")
    kind, g = r
    # the actor named inside a language line must be the logging source (else two readings)
    if "actor" in g and g["actor"] != ev.by:
        raise Ambiguous(f"{mach}: actor {g['actor']!r} in text differs from source {ev.by!r}")
    return kind, g


def _typed_agent(text: str, prm: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    m = re.match(r"^(?P<tool>(?:cart|files)\.\w+)\((?P<args>.*)\) -> (?P<res>ok|error: [^.]*|partial: .*?)\.?$", text)
    if not m:
        raise SolverError(f"agent: unread call {text!r}")
    tool, args, res = m["tool"], m["args"], m["res"]
    ns, op = tool.split(".")
    if ns != prm["kind"]:
        raise SolverError(f"agent: {ns} tool in a {prm['kind']} log")
    parts: list[tuple[str, str, str | None]] = []  # (op, item, arg)
    if op == "undo":
        a = re.fullmatch(r"call=(C\d+)", args)
        if not a:
            raise SolverError(f"agent undo {args!r}")
        parts = [("undo", a.group(1), None)]
    elif op in ("add", "remove", "set_quantity"):
        a = re.fullmatch(r"sku=(\S+), qty=(\d+)", args)
        if not a:
            raise SolverError(f"agent args {args!r}")
        parts = [({"add": "add", "remove": "remove", "set_quantity": "set"}[op], a.group(1), a.group(2))]
    elif op == "move":
        a = re.fullmatch(r"path=(\S+), folder=(\w+)", args)
        if not a:
            raise SolverError(f"agent args {args!r}")
        parts = [("move", a.group(1), a.group(2))]
    elif op in ("delete", "restore"):
        a = re.fullmatch(r"path=(\S+)", args)
        if not a:
            raise SolverError(f"agent args {args!r}")
        parts = [(op, a.group(1), None)]
    elif op in ("add_many", "remove_many", "set_many", "update_many", "move_many", "delete_many", "restore_many"):
        for item in args.split(", "):
            if ns == "cart":
                a = (re.fullmatch(r"(add|remove) (\S+) x(\d+)", item) or re.fullmatch(r"(set) (\S+) to (\d+)", item))
                if a:
                    parts.append((a.group(1), a.group(2), a.group(3)))
                    continue
                a = re.fullmatch(r"(\S+) x(\d+)", item)
                if a and op in ("add_many", "remove_many"):
                    parts.append((op[:-5], a.group(1), a.group(2)))
                    continue
                a = re.fullmatch(r"(\S+) to (\d+)", item)
                if a and op == "set_many":
                    parts.append(("set", a.group(1), a.group(2)))
                    continue
            else:
                a = re.fullmatch(r"move (\S+) to (\w+)", item) or re.fullmatch(r"(\S+) to (\w+)", item)
                if a and (op in ("move_many", "update_many")):
                    parts.append(("move", a.group(1), a.group(2)))
                    continue
                a = re.fullmatch(r"(delete|restore) (\S+)", item)
                if a and op == "update_many":
                    parts.append((a.group(1), a.group(2), None))
                    continue
                a = re.fullmatch(r"(\S+\.\w+)", item)
                if a and op in ("delete_many", "restore_many"):
                    parts.append((op[:-5], a.group(1), None))
                    continue
            raise SolverError(f"agent batch item {item!r}")
    else:
        raise SolverError(f"agent tool {tool!r}")
    if res == "ok":
        ok = [True] * len(parts)
    elif res.startswith("error"):
        ok = [False] * len(parts)
    else:
        st = res[len("partial: "):].split(", ")
        if len(st) != len(parts):
            raise SolverError(f"agent partial count {text!r}")
        ok = []
        for (o, item, _), s in zip(parts, st):
            sm = re.fullmatch(r"(\S+) (ok|failed)", s)
            if not sm or sm.group(1) != item:
                raise SolverError(f"agent partial item {s!r} vs {item!r}")
            ok.append(sm.group(2) == "ok")
    return "call", {"parts": parts, "ok": ok, "op": op}


def _typed_dialogue(ev: Event, prm: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    slots = prm["slots"]
    sre = "|".join(re.escape(s) for s in sorted(slots, key=len, reverse=True))
    vre = "|".join(re.escape(v) for v in sorted({v for vs in slots.values() for v in vs}, key=len, reverse=True))
    t = ev.text
    pats = [
        ("set", rf"Please set the (?P<s>{sre}) to (?P<v>{vre})\."),
        ("set", rf"I'd like the (?P<s>{sre}) to be (?P<v>{vre}), please\."),
        ("set", rf"Can you make the (?P<s>{sre}) (?P<v>{vre})\?"),
        ("set", rf"On booking (?P<ref>\S+) I want the (?P<s>{sre}) changed to (?P<v>{vre})\."),
        ("set_other", rf"For my other booking (?P<ref>\S+), please set the (?P<s>{sre}) to (?P<v>{vre})\."),
        ("not", rf"Not the (?P<v>{vre}), please\."),
        ("not", rf"Anything but (?P<v>{vre}) for the (?P<s>{sre})\."),
        ("same", rf"Let's go back to the (?P<s>{sre}) we had before\."),
        ("same", rf"Actually, keep the (?P<s>{sre}) the same as before\."),
        ("other_person", rf"(?P<who>[A-Z][a-z]+) says the (?P<s>{sre}) should be (?P<v>{vre})\."),
        ("other_person", rf"My colleague (?P<who>[A-Z][a-z]+) would prefer (?P<v>{vre}) for the (?P<s>{sre})\."),
        ("proposal", rf"Shall I switch the (?P<s>{sre}) to (?P<v>{vre})\?"),
        ("proposal", rf"Would you like the (?P<s>{sre}) to be (?P<v>{vre})\?"),
        ("confirm", rf"Confirmed: the (?P<s>{sre}) is (?P<v>{vre})\."),
        ("confirm", rf"Done - the (?P<s>{sre}) is now (?P<v>{vre})\."),
    ]
    for kind, pat in pats:
        m = re.fullmatch(pat, t)
        if m:
            g = m.groupdict()
            if kind == "not" and g.get("s") is None:
                owners = [s for s, vs in slots.items() if g["v"] in vs]
                if len(owners) != 1:
                    raise Ambiguous(f"dialogue: value {g['v']!r} in {len(owners)} slots")
                g["s"] = owners[0]
            if g.get("v") is not None and g["v"] not in slots[g["s"]]:
                g["bad_value"] = "1"
            return kind, {k: v for k, v in g.items() if v is not None}
    raise SolverError(f"dialogue: unread message {t!r}")


# ---------------------------------------------------------------------------------------------------------------
# 5. Simulators (one per machine). `World(doc).at(T)` returns a machine state object with observables.
#
# READINGS: the places where the rendered rule text can be read two ways. The first value is this solver's reading
# (argued in the report); the report re-runs every row under the other reading and lists the rows whose answer
# changes, so a template fix can remove the ambiguity.
#   clear_over_quarantine: "a clear returns quarantined units (only up to the number in quarantine)" with a clear of
#       more units than are in quarantine -> "reject" (R6: a request that breaks a rule is rejected) | "clamp".
#   restore_not_in_trash: "files.restore moves it from trash to inbox" on a file that is not in trash, result ok ->
#       "noop" (nothing in trash to move) | "inbox".
#   other_booking_self: "For my other booking <ref>, ..." whose ref is this booking -> "apply" (the rules decide by
#       the reference characters) | "ignore".
#   assistant_request: a request sentence ("Please set ...") logged by the Assistant -> "ignore" (only the customer's
#       own requests change slots) | "apply".
#   customer_proposal: a proposal sentence ("Shall I switch ...?", "Would you like ...?") logged by the Customer ->
#       "ignore" (a question, not a request) | "apply".
#   rehold_same_person: a hold on a slot by the person whose own hold there is still active -> "renew" (a new hold
#       with its own minutes; allowed, since only another person's active hold blocks it) | "keep" (changes nothing).
#   revert_of_resolve: a revert of the resolve that set the first resolution time -> "restore" (the first resolution
#       time is a value that event changed) | "keep".
#   same_as_before_excluded: 'same as before' whose most recent confirmed value was since excluded by 'not X' ->
#       "set" (the rule says it sets the slot to that value) | "reject" (a request for a value that is not allowed).
#   override_overlap: two overrides of one flag for one person -> "latest_in_force" (each lasts its own hours; of those
#       in force at the stated time the most recent decides) | "replace" (a new override ends the earlier one).
READINGS: dict[str, str] = {"clear_over_quarantine": "reject", "restore_not_in_trash": "noop",
                            "other_booking_self": "apply", "assistant_request": "ignore",
                            "customer_proposal": "ignore", "rehold_same_person": "renew",
                            "revert_of_resolve": "restore", "same_as_before_excluded": "set",
                            "override_overlap": "latest_in_force"}
ALT_READINGS: dict[str, str] = {"clear_over_quarantine": "clamp", "restore_not_in_trash": "inbox",
                                "other_booking_self": "ignore", "assistant_request": "apply",
                                "customer_proposal": "apply", "rehold_same_person": "keep",
                                "revert_of_resolve": "keep", "same_as_before_excluded": "reject",
                                "override_overlap": "replace"}
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Flags:
    """Things the replay met that a reader could take two ways; decide2 reports them next to disagreements."""
    notes: set[str] = field(default_factory=set)


def _money(s: str) -> Decimal:
    return Decimal(s.replace(",", ""))


def _units(n: int) -> str:
    return f"{n} unit" if n == 1 else f"{n} units"


class World:
    def __init__(self, doc: Doc, mach: str | None = None):
        self.doc = doc
        self.mach = mach or machine_of(doc)
        self.prm = params(doc, self.mach)
        self.flags = Flags()
        ts = [e.t for e in doc.events]
        if len(set(ts)) != len(ts):
            raise Ambiguous("two events share a timestamp: the time order is not recoverable")
        self.events = sorted(doc.events, key=lambda e: e.t)
        self.typed = [(e, typed(self.mach, e, self.prm)) for e in self.events]
        for e in self.events:
            if e.t < doc.start:
                raise Ambiguous(f"event {e.eid} before the starting time")
        # every rule must be in force from the starting time on
        for n, d, _ in doc.rules:
            if date.fromisoformat(d) > doc.start.date():
                raise Ambiguous(f"R{n} comes into force after the log starts")
        self.end = parse_time(doc.context["log exported at"].rstrip("."))
        if any(e.t > self.end for e in self.events):
            self.flags.notes.add("event_after_export")

    def at(self, T: datetime):
        sim = SIMS[self.mach](self)
        for e, (kind, g) in self.typed:
            if e.t > T:
                break
            sim.step(e, kind, g)
        sim.T = T
        return sim


class _Base:
    """Shared replay rules: ids take effect at most once; the step handler returns True when the request took
    effect (not rejected, entity exists)."""

    def __init__(self, w: World):
        self.w = w
        self.prm = w.prm
        self.done: set[str] = set()          # ids that took effect
        self.T: datetime | None = None

    def step(self, e: Event, kind: str, g: dict[str, Any]) -> None:
        if e.eid in self.done:
            return  # redelivery / retry of an id that already took effect
        if self.apply(e, kind, g):
            self.done.add(e.eid)

    def apply(self, e: Event, kind: str, g: dict[str, Any]) -> bool:  # pragma: no cover - abstract
        raise NotImplementedError


class _Restore(_Base):
    """Machines whose revert rule restores 'every value it changed' to its value just before that event.
    Values live in self.v[(entity, field)]; each effective event records the old values it overwrote."""

    def __init__(self, w: World):
        super().__init__(w)
        self.v: dict[tuple[str, str], Any] = {}
        self.changed: dict[str, dict[tuple[str, str], Any]] = {}
        self.reverted: set[str] = set()

    def setv(self, eid: str, key: tuple[str, str], val: Any) -> None:
        ch = self.changed.setdefault(eid, {})
        if key not in ch:
            ch[key] = self.v.get(key)
        self.v[key] = val

    def revert(self, e: Event, ref: str) -> bool:
        if ref not in self.done or ref in self.reverted:
            return False
        if self.w.typed_kind(ref) == "revert":
            self.w.flags.notes.add("revert_of_revert")
        for key, old in self.changed.get(ref, {}).items():
            self.setv(e.eid, key, old)
        self.reverted.add(ref)
        return True


def _typed_kind(self: World, eid: str) -> str | None:
    for e, (k, _) in self.typed:
        if e.eid == eid:
            return k
    return None


World.typed_kind = _typed_kind  # type: ignore[attr-defined]


# ---- orders ------------------------------------------------------------------------------------------------------
ORDER_STEPS = {"pay": ({"created"}, "paid"), "pack": ({"paid"}, "packed"), "ship": ({"packed"}, "shipped"),
               "deliver": ({"shipped"}, "delivered"), "cancel": ({"created", "paid", "packed"}, "cancelled"),
               "return": ({"delivered"}, "returned")}


class OrdersSim(_Restore):
    def __init__(self, w: World):
        super().__init__(w)
        _check_rule(w, "Order statuses change only by these steps: pay (created to paid), pack (paid to packed), ship "
                       "(packed to shipped), deliver (shipped to delivered), cancel (created, paid or packed to "
                       "cancelled), return (delivered to returned).")
        self.ids = [i for i, _ in w.doc.entities]
        for i, f in w.doc.entities:
            self.v[(i, "status")] = f["status"]

    def apply(self, e, kind, g):
        if kind == "revert":
            return self.revert(e, g["ref"])
        oid = g["id"]
        if oid not in self.ids:
            return False
        frm, to = ORDER_STEPS[kind]
        if self.v[(oid, "status")] not in frm:
            return False
        self.setv(e.eid, (oid, "status"), to)
        return True

    def status(self, oid: str) -> str:
        if oid not in self.ids:
            raise SolverError(f"unknown order {oid}")
        return self.v[(oid, "status")]


# ---- tickets -----------------------------------------------------------------------------------------------------
TICKET_STEPS = {"start": ({"assigned"}, "in_progress"), "wait": ({"in_progress"}, "waiting"),
                "resume": ({"waiting"}, "in_progress"), "resolve": ({"in_progress", "waiting"}, "resolved"),
                "reopen": ({"resolved"}, "in_progress"), "close": ({"resolved"}, "closed")}


class TicketsSim(_Restore):
    def __init__(self, w: World):
        super().__init__(w)
        _check_rule(w, "Ticket statuses: new, assigned, in_progress, waiting, resolved, closed. Steps: start (assigned "
                       "to in_progress), wait (in_progress to waiting), resume (waiting to in_progress, when the "
                       "customer answers), resolve (in_progress or waiting to resolved), reopen (resolved to "
                       "in_progress), close (resolved to closed).")
        _check_rule(w, "An assignment sets the owner and moves a new ticket to assigned. It is allowed only while the "
                       "ticket is new, assigned, in_progress or waiting, and only to a person on the support roster: ",
                    prefix=True)
        self.ids = [i for i, _ in w.doc.entities]
        self.opened: dict[str, datetime] = {}
        for i, f in w.doc.entities:
            self.v[(i, "status")] = f["status"]
            self.v[(i, "owner")] = None if f["owner"] == "nobody" else f["owner"]
            self.v[(i, "first_resolved")] = None
            if "opened" in f:
                self.opened[i] = parse_time(f["opened"])

    def apply(self, e, kind, g):
        if kind == "revert":
            ref = g["ref"]
            keep_fr = None
            if ref in self.done and ref not in self.reverted and self.w.typed_kind(ref) == "resolve":
                self.w.flags.notes.add("revert_of_resolve")
                if READINGS["revert_of_resolve"] == "keep":
                    keep_fr = {k: self.v[k] for k in self.changed.get(ref, {}) if k[1] == "first_resolved"}
            ok = self.revert(e, ref)
            for k, val in (keep_fr or {}).items():
                self.v[k] = val
            return ok
        tid = g["id"]
        if tid not in self.ids:
            return False
        st = self.v[(tid, "status")]
        if kind == "assign":
            if st not in ("new", "assigned", "in_progress", "waiting") or g["p"] not in self.prm["roster"]:
                return False
            self.setv(e.eid, (tid, "owner"), g["p"])
            if st == "new":
                self.setv(e.eid, (tid, "status"), "assigned")
            return True
        frm, to = TICKET_STEPS[kind]
        if st not in frm:
            return False
        self.setv(e.eid, (tid, "status"), to)
        if kind == "resolve" and self.v[(tid, "first_resolved")] is None:
            self.setv(e.eid, (tid, "first_resolved"), e.t)
        return True

    def owner(self, tid: str) -> str:
        if tid not in self.ids:
            raise SolverError(f"unknown ticket {tid}")
        return self.v[(tid, "owner")] or "nobody"

    def status(self, tid: str) -> str:
        return self.v[(tid, "status")]

    # SLA ------------------------------------------------------------------------------------------------------
    def _windows(self, a: datetime, b: datetime):
        """Business intervals (UTC) overlapping [a, b]."""
        tz = self.prm["tz"]
        d = a.astimezone(tz).date() - timedelta(days=1)
        last = b.astimezone(tz).date() + timedelta(days=1)
        while d <= last:
            if d.weekday() < 5 and d not in self.prm["holidays"]:
                o = datetime(d.year, d.month, d.day, *self.prm["open"], tzinfo=tz).astimezone(timezone.utc)
                c = datetime(d.year, d.month, d.day, *self.prm["close"], tzinfo=tz).astimezone(timezone.utc)
                yield o, c
            d += timedelta(days=1)

    def due(self, tid: str) -> datetime:
        if tid not in self.opened:
            raise SolverError(f"ticket {tid} has no opened time")
        need = timedelta(hours=self.prm["due_hours"])
        t0 = self.opened[tid]
        horizon = t0 + timedelta(days=60)
        for o, c in self._windows(t0, horizon):
            s = max(o, t0)
            if s >= c:
                continue
            if c - s >= need:
                return s + need
            need -= c - s
        raise SolverError("due time beyond horizon")

    def business(self, a: datetime, b: datetime) -> timedelta:
        tot = timedelta(0)
        if b <= a:
            return tot
        for o, c in self._windows(a, b):
            s, t = max(o, a), min(c, b)
            if t > s:
                tot += t - s
        return tot

    def overdue(self, tid: str) -> bool:
        due = self.due(tid)
        fr = self.v[(tid, "first_resolved")]
        return self.T > due and not (fr is not None and fr <= due)

    def escalation(self, tid: str) -> int:
        if not self.overdue(tid):
            return 0
        due = self.due(tid)
        fr = self.v[(tid, "first_resolved")]
        end = fr if fr is not None else self.T
        h = self.business(due, end)
        a, b, c = self.prm["esc"]
        if h < timedelta(hours=a):
            return 1
        if h < timedelta(hours=b):
            return 2
        if h < timedelta(hours=c):
            return 3
        return 4


# ---- bookings ----------------------------------------------------------------------------------------------------
class BookingsSim(_Restore):
    def __init__(self, w: World):
        super().__init__(w)
        for pat in ["A hold is allowed only if the slot has no confirmed booking and no active hold by another person.",
                    "A confirmation is allowed only for the person whose hold on that slot is active at that moment; "
                    "it turns the hold into that person's confirmed booking.",
                    "A cancellation is allowed only for the person who holds the confirmed booking; it frees the slot. "
                    "A release is allowed only for the person whose hold is active; it ends the hold.",
                    "A slot is free for a new hold when it has no confirmed booking and no active hold."]:
            _check_rule(w, pat)
        self.ids = [i for i, _ in w.doc.entities]
        for i, f in w.doc.entities:
            if f["hold"] != "none":
                raise SolverError("starting hold")
            self.v[(i, "conf")] = None if f["confirmed booking"] == "none" else f["confirmed booking"]
            self.v[(i, "hold")] = None

    def _active(self, sid: str, t: datetime):
        h = self.v[(sid, "hold")]
        if h is None:
            return None
        who, end = h
        return who if t < end else None

    def apply(self, e, kind, g):
        if kind == "revert":
            return self.revert(e, g["ref"])
        sid = g["id"]
        if sid not in self.ids:
            return False
        p = g["p"]
        conf = self.v[(sid, "conf")]
        act = self._active(sid, e.t)
        if kind == "hold":
            if conf is not None or (act is not None and act != p):
                return False
            mins = int(g.get("min", self.prm["default_minutes"]))
            if act == p:
                self.w.flags.notes.add("rehold_same_person")
                if READINGS["rehold_same_person"] == "keep":
                    return False
            self.setv(e.eid, (sid, "hold"), (p, e.t + timedelta(minutes=mins)))
            return True
        if kind == "confirm":
            if act != p:
                return False
            self.setv(e.eid, (sid, "conf"), p)
            self.setv(e.eid, (sid, "hold"), None)
            return True
        if kind == "cancel":
            if conf != p:
                return False
            self.setv(e.eid, (sid, "conf"), None)
            return True
        if kind == "release":
            if act != p:
                return False
            self.setv(e.eid, (sid, "hold"), None)
            return True
        raise SolverError(kind)

    def confirmed(self, sid: str) -> str:
        if sid not in self.ids:
            raise SolverError(f"unknown slot {sid}")
        return self.v[(sid, "conf")] or "nobody"

    def free(self, sid: str) -> bool:
        if sid not in self.ids:
            raise SolverError(f"unknown slot {sid}")
        return self.v[(sid, "conf")] is None and self._active(sid, self.T) is None


# ---- inventory ---------------------------------------------------------------------------------------------------
class InventorySim(_Base):

    def __init__(self, w: World):
        super().__init__(w)
        self.ids = [i for i, _ in w.doc.entities]
        self.on: dict[str, int] = {}
        self.q: dict[str, int] = {}
        self.holds: dict[str, dict[str, Any]] = {}  # hold event id -> {sku, n, end, active}
        self.log: dict[str, tuple[str, dict[str, Any]]] = {}
        self.reverted: set[str] = set()
        for i, f in w.doc.entities:
            if f["holds"] != "none":
                raise SolverError("starting holds")
            self.on[i] = int(f["on hand"])
            self.q[i] = int(f["quarantine"])

    def avail(self, sku: str, t: datetime) -> int:
        held = sum(h["n"] for h in self.holds.values() if h["sku"] == sku and h["active"] and t < h["end"])
        return max(0, self.on[sku] - held - self.q[sku])

    def apply(self, e, kind, g):
        t = e.t
        if kind == "revert":
            ref = g["ref"]
            if ref not in self.done or ref in self.reverted:
                return False
            k0, rec = self.log[ref]
            if k0 == "receive":
                self.on[rec["sku"]] = max(0, self.on[rec["sku"]] - rec["n"])
            elif k0 == "ship":
                self.on[rec["sku"]] += rec["n"]
            elif k0 == "hold":
                self.holds[ref]["active"] = False
            elif k0 == "release":
                self.holds[rec["hold"]]["active"] = True
            elif k0 == "quarantine":
                self.q[rec["sku"]] = max(0, self.q[rec["sku"]] - rec["n"])
            elif k0 == "clear":
                self.q[rec["sku"]] += rec["n"]
            elif k0 == "count":
                self.on[rec["sku"]] = rec["before"]
            else:
                self.w.flags.notes.add("revert_of_" + k0)
                raise Ambiguous(f"inventory revert of a {k0}")
            self.reverted.add(ref)
            self.log[e.eid] = ("revert", {"ref": ref})
            return True
        if kind == "release":
            ref = g["ref"]
            h = self.holds.get(ref)
            if h is None or not h["active"] or t >= h["end"]:
                return False
            h["active"] = False
            self.log[e.eid] = ("release", {"hold": ref})
            return True
        sku = g["id"]
        if sku not in self.ids:
            return False
        n = int(g["n"])
        if kind == "receive":
            self.on[sku] += n
            self.log[e.eid] = ("receive", {"sku": sku, "n": n})
            return True
        if kind == "ship":
            if n > self.avail(sku, t):
                return False
            self.on[sku] -= n
            self.log[e.eid] = ("ship", {"sku": sku, "n": n})
            return True
        if kind == "hold":
            if n > self.avail(sku, t):
                return False
            self.holds[e.eid] = {"sku": sku, "n": n, "end": t + timedelta(minutes=int(g["min"])), "active": True}
            self.log[e.eid] = ("hold", {"sku": sku, "n": n})
            return True
        if kind == "quarantine":
            if n > self.avail(sku, t):
                return False
            self.q[sku] += n
            self.log[e.eid] = ("quarantine", {"sku": sku, "n": n})
            return True
        if kind == "clear":
            if n > self.q[sku]:
                self.w.flags.notes.add("clear_more_than_quarantine")
                if READINGS["clear_over_quarantine"] == "reject":
                    return False
            k = min(n, self.q[sku])
            self.q[sku] -= k
            self.log[e.eid] = ("clear", {"sku": sku, "n": k})
            return True
        if kind == "count":
            before = self.on[sku]
            self.on[sku] = n
            self.log[e.eid] = ("count", {"sku": sku, "before": before})
            return True
        raise SolverError(kind)

    def available(self, sku: str) -> int:
        if sku not in self.ids:
            raise SolverError(f"unknown sku {sku}")
        return self.avail(sku, self.T)


# ---- ledger ------------------------------------------------------------------------------------------------------
class LedgerSim(_Base):
    def __init__(self, w: World):
        super().__init__(w)
        for pat in ["A post names the event id of an authorisation that is still pending and not lapsed: its amount "
                    "leaves the posted balance and it stops being pending. Any other post changes nothing.",
                    "A transfer out is allowed only if its amount is at most the available balance at that moment. "
                    "Deposits and fees are always applied."]:
            _check_rule(w, pat)
        self.ids = [i for i, _ in w.doc.entities]
        self.posted: dict[str, Decimal] = {}
        self.auths: dict[str, dict[str, Any]] = {}
        self.log: dict[str, tuple[str, dict[str, Any]]] = {}
        self.reverted: set[str] = set()
        self.cur = self.prm["currency"]
        for i, f in w.doc.entities:
            if f["pending"] != "none":
                raise SolverError("starting pending")
            amt, cur = f["posted balance"].rsplit(" ", 1)
            if cur != self.cur:
                raise SolverError("currency")
            self.posted[i] = _money(amt)

    def pending(self, acc: str, t: datetime) -> Decimal:
        return sum((a["amt"] for a in self.auths.values() if a["acc"] == acc and a["pending"] and t < a["lapse"]),
                   Decimal(0))

    def avail(self, acc: str, t: datetime) -> Decimal:
        return self.posted[acc] - self.pending(acc, t)

    def apply(self, e, kind, g):
        t = e.t
        if kind == "revert":
            ref = g["ref"]
            if ref not in self.done or ref in self.reverted:
                return False
            k0, rec = self.log[ref]
            if k0 == "deposit":
                self.posted[rec["acc"]] -= rec["amt"]
            elif k0 in ("fee", "transfer"):
                self.posted[rec["acc"]] += rec["amt"]
            elif k0 == "auth":
                a = self.auths[ref]
                if not a["pending"]:
                    self.w.flags.notes.add("reverse_auth_not_pending")
                a["pending"] = False
            elif k0 == "post":
                a = self.auths[rec["auth"]]
                self.posted[a["acc"]] += a["amt"]
                a["pending"] = True
            else:
                raise Ambiguous(f"ledger reversal of a {k0}")
            self.reverted.add(ref)
            self.log[e.eid] = ("revert", {"ref": ref})
            return True
        if kind == "post":
            a = self.auths.get(g["ref"])
            if a is None or not a["pending"] or t >= a["lapse"]:
                return False
            self.posted[a["acc"]] -= a["amt"]
            a["pending"] = False
            self.log[e.eid] = ("post", {"auth": g["ref"]})
            return True
        acc = g["id"]
        if acc not in self.ids:
            return False
        if g["cur"] != self.cur:
            raise SolverError("event currency")
        amt = _money(g["amt"])
        if kind == "deposit":
            self.posted[acc] += amt
        elif kind == "fee":
            self.posted[acc] -= amt
        elif kind == "transfer":
            if amt > self.avail(acc, t):
                return False
            self.posted[acc] -= amt
        elif kind == "auth":
            if amt > self.avail(acc, t):
                return False
            self.auths[e.eid] = {"acc": acc, "amt": amt, "pending": True,
                                 "lapse": t + timedelta(hours=self.prm["lapse_hours"])}
        else:
            raise SolverError(kind)
        self.log[e.eid] = (kind, {"acc": acc, "amt": amt})
        return True

    def posted_of(self, acc: str) -> Decimal:
        if acc not in self.ids:
            raise SolverError(f"unknown account {acc}")
        return self.posted[acc]

    def available(self, acc: str) -> Decimal:
        if acc not in self.ids:
            raise SolverError(f"unknown account {acc}")
        return self.avail(acc, self.T)


# ---- access ------------------------------------------------------------------------------------------------------
ROLE_RANK = {"viewer": 1, "editor": 2, "owner": 3}


class AccessSim(_Base):
    def __init__(self, w: World):
        super().__init__(w)
        for pat in ["Roles on a resource rank viewer < editor < owner. A person's access is the highest role among the "
                    "grants in force for them, given to them directly or to a group they belong to at the stated time.",
                    "A grant with a number of hours stops counting at its start time plus those hours (it no longer "
                    "counts at exactly that time). A grant without hours lasts until it is revoked.",
                    "A revoke names the event id of an earlier grant; that grant stops counting. A revoke of a grant "
                    "that never took effect, or is already revoked, changes nothing.",
                    "A deny rule blocks the person from the resource whatever grants they hold, until the deny rule "
                    "is lifted.",
                    "Renaming a group keeps its members and grants. After a rename, only the new name refers to the "
                    "group; a line using the old name changes nothing.",
                    "Viewing needs viewer or higher; editing needs editor or higher."]:
            _check_rule(w, pat)
        self.res: set[str] = set()
        self.gname: dict[str, int] = {}     # current group name -> group key
        self.members: dict[int, set[str]] = {}
        for i, f in w.doc.entities:
            if "kind" in f:
                if f["grants"] != "none":
                    raise SolverError("starting grants")
                self.res.add(i)
            elif "members" in f:
                k = len(self.members)
                self.gname[i] = k
                self.members[k] = set() if f["members"] == "none" else set(_names(f["members"]))
            else:
                raise SolverError(f"access entity {i}")
        self.grants: dict[str, dict[str, Any]] = {}
        self.deny: set[tuple[str, str]] = set()

    def _target(self, to: str):
        if re.fullmatch(r"[a-z][a-z0-9-]*", to):
            if to not in self.gname:
                return None
            return ("g", self.gname[to])
        return ("p", to)

    def apply(self, e, kind, g):
        if e.by not in self.prm["admins"]:
            return False
        t = e.t
        if kind == "grant":
            if g["id"] not in self.res:
                return False
            tg = self._target(g["to"])
            if tg is None:
                return False
            end = t + timedelta(hours=int(g["h"])) if "h" in g else None
            self.grants[e.eid] = {"res": g["id"], "to": tg, "role": g["role"], "end": end, "live": True}
            return True
        if kind == "revoke":
            gr = self.grants.get(g["ref"])
            if gr is None or not gr["live"]:
                return False
            gr["live"] = False
            return True
        if kind in ("deny", "lift"):
            if g["id"] not in self.res:
                return False
            key = (g["p"], g["id"])
            if kind == "deny":
                self.deny.add(key)
            else:
                if key not in self.deny:
                    return False
                self.deny.discard(key)
            return True
        if kind in ("add", "remove"):
            if g["g"] not in self.gname:
                return False
            ms = self.members[self.gname[g["g"]]]
            if kind == "add":
                ms.add(g["p"])
            else:
                if g["p"] not in ms:
                    return False
                ms.discard(g["p"])
            return True
        if kind == "rename":
            if g["g"] not in self.gname or g["g2"] in self.gname:
                return False
            self.gname[g["g2"]] = self.gname.pop(g["g"])
            return True
        raise SolverError(kind)

    def level(self, p: str, rid: str) -> str:
        if rid not in self.res:
            raise SolverError(f"unknown resource {rid}")
        if (p, rid) in self.deny:
            return "blocked by a deny"
        best = 0
        for gr in self.grants.values():
            if gr["res"] != rid or not gr["live"]:
                continue
            if gr["end"] is not None and self.T >= gr["end"]:
                continue
            kind, who = gr["to"]
            if (kind == "p" and who == p) or (kind == "g" and p in self.members[who]):
                best = max(best, ROLE_RANK[gr["role"]])
        return {0: "no access", 1: "viewer", 2: "editor", 3: "owner"}[best]

    def can(self, p: str, rid: str, need: str) -> bool:
        lv = self.level(p, rid)
        return lv in ROLE_RANK and ROLE_RANK[lv] >= ROLE_RANK[need]


# ---- dialogue ----------------------------------------------------------------------------------------------------
class DialogueSim(_Base):
    def __init__(self, w: World):
        super().__init__(w)
        for pat in ["Only the customer's own requests about booking ",
                    "A confirmation by the assistant counts only when it repeats the slot's current value; it makes "
                    "that value the slot's most recent confirmed value. Any other confirmation changes nothing.",
                    "'Same as before' (or 'go back to what we had before') sets the slot to its most recent confirmed "
                    "value.",
                    "'Not X' (or 'anything but X') removes X from the slot's allowed values. If X was the current "
                    "value, or the slot had no value, the slot then takes the only remaining allowed value when "
                    "exactly one remains; otherwise it has no value. A request for a value that is not allowed "
                    "changes nothing.",
                    "The starting state lists the confirmed values from before this chat; they count as confirmed."]:
            _check_rule(w, pat, prefix=pat.endswith(" "))
        self.bk = self.prm["booking"]
        ents = dict(w.doc.entities)
        if list(ents) != [self.bk]:
            raise SolverError("dialogue entities")
        self.val: dict[str, str | None] = {s: ents[self.bk].get(s) for s in self.prm["slots"]}
        if any(v is None for v in self.val.values()):
            raise SolverError("dialogue start values")
        self.conf = dict(self.val)
        self.allowed = {s: list(vs) for s, vs in self.prm["slots"].items()}

    def apply(self, e, kind, g):
        if kind == "proposal" and e.by == "Customer":
            self.w.flags.notes.add("customer_proposal_wording")
            if READINGS["customer_proposal"] == "apply":
                kind = "set"
        if kind in ("other_person", "proposal"):
            return False
        if kind in ("set", "not", "same", "set_other") and e.by != "Customer":
            self.w.flags.notes.add("assistant_request_wording")
            if READINGS["assistant_request"] == "ignore":
                return False
        if kind == "confirm" and e.by != "Assistant":
            self.w.flags.notes.add("customer_confirm_wording")
        if kind == "set_other":
            if g["ref"] != self.bk:
                return False
            # 'my other booking <ref>' whose ref is THIS booking: the rules decide by the reference characters
            self.w.flags.notes.add("other_booking_names_this_booking")
            if READINGS["other_booking_self"] == "ignore":
                return False
            kind = "set"
        if kind == "confirm":
            if e.by != "Assistant":
                return False
            s = g["s"]
            if self.val[s] != g["v"]:
                return False
            self.conf[s] = g["v"]
            return True
        s = g["s"]
        if kind == "set":
            if g.get("ref") is not None and g["ref"] != self.bk:
                return False
            if g["v"] not in self.allowed[s]:
                return False
            self.val[s] = g["v"]
            return True
        if kind == "not":
            x = g["v"]
            if x in self.allowed[s]:
                self.allowed[s].remove(x)
            if self.val[s] == x or self.val[s] is None:
                self.val[s] = self.allowed[s][0] if len(self.allowed[s]) == 1 else None
            return True
        if kind == "same":
            c = self.conf[s]
            if c is not None and c not in self.allowed[s]:
                self.w.flags.notes.add("same_as_before_excluded_value")
                if READINGS["same_as_before_excluded"] == "reject":
                    return False
            self.val[s] = c
            return True
        raise SolverError(kind)

    def value(self, slot: str) -> str:
        v = self.val[slot]
        if v is None:
            raise Ambiguous(f"slot {slot} has no value")
        return v


# ---- agent -------------------------------------------------------------------------------------------------------
class AgentSim(_Base):
    def __init__(self, w: World):
        super().__init__(w)
        _check_rule(w, "Each line is one tool call by the assistant, with the tool's result after the arrow. Only the "
                       "parts the result reports as ok change anything: 'ok' means every part succeeded, 'error' means "
                       "none did, and 'partial' lists each part as ok or failed.")
        _check_rule(w, "A line that repeats a call id is a retry. A call id takes effect at most once: a retry of a "
                       "call that already took effect changes nothing.")
        self.kind = self.prm["kind"]
        self.qty: dict[str, int] = {}
        self.folder: dict[str, str] = {}
        for i, f in w.doc.entities:
            if self.kind == "cart":
                self.qty[i] = int(f["quantity in cart"])
            else:
                self.folder[i] = f["folder"]
        self.undo_log: dict[str, list[tuple]] = {}
        self.undone: set[str] = set()

    def apply(self, e, kind, g):
        took = False
        log: list[tuple] = []
        for (op, item, arg), ok in zip(g["parts"], g["ok"]):
            if not ok:
                continue
            if op == "undo":
                ref = item
                if ref not in self.done or ref in self.undone:
                    continue
                if not self.undo_log.get(ref):
                    self.w.flags.notes.add("undo_of_undo_or_empty")
                for rec in reversed(self.undo_log.get(ref, [])):
                    self._undo(rec)
                self.undone.add(ref)
                took = True
                continue
            if self.kind == "cart":
                if item not in self.qty:
                    continue
                n = int(arg)
                before = self.qty[item]
                if op == "add":
                    self.qty[item] = before + n
                    log.append(("add", item, n))
                elif op == "remove":
                    k = min(n, before)
                    self.qty[item] = before - k
                    log.append(("remove", item, k))
                elif op == "set":
                    self.qty[item] = n
                    log.append(("set", item, before))
                else:
                    raise SolverError(op)
            else:
                if item not in self.folder:
                    continue
                before = self.folder[item]
                if op == "move":
                    self.folder[item] = arg
                elif op == "delete":
                    self.folder[item] = "trash"
                elif op == "restore":
                    if before != "trash":
                        self.w.flags.notes.add("restore_not_in_trash")
                        if READINGS["restore_not_in_trash"] == "noop":
                            continue  # nothing in trash to move: the ok part changes nothing (and is not undoable)
                    self.folder[item] = "inbox"
                else:
                    raise SolverError(op)
                log.append(("file", item, before))
            took = True
        if took:
            self.undo_log[e.eid] = log
        return took

    def _undo(self, rec: tuple) -> None:
        op, item, x = rec
        if op == "add":
            self.qty[item] = max(0, self.qty[item] - x)
        elif op == "remove":
            self.qty[item] += x
        elif op == "set":
            self.qty[item] = x
        elif op == "file":
            self.folder[item] = x

    def quantity(self, sku: str) -> int:
        if sku not in self.qty:
            raise SolverError(f"unknown sku {sku}")
        return self.qty[sku]

    def folder_of(self, f: str) -> str:
        if f not in self.folder:
            raise SolverError(f"unknown file {f}")
        return self.folder[f]


# ---- flags (held out) ----------------------------------------------------------------------------------------------
class FlagsSim(_Restore):
    def __init__(self, w: World):
        super().__init__(w)
        _check_rule(w, "A flag is on for a person in production when no kill switch is engaged and either an override "
                       "for that person is in force (then the override decides) or the flag is enabled in production "
                       "and the person's bucket number is below the production rollout percentage.")
        _check_rule(w, "Anyone on call may engage a kill switch without a ticket. An override lasts the stated hours "
                       "from its time (it no longer counts at exactly the end time).")
        self.flags_ids: list[str] = []
        self.bucket: dict[str, int] = {}
        for i, f in w.doc.entities:
            if "bucket" in f:
                self.bucket[i] = int(f["bucket"])
            else:
                self.flags_ids.append(i)
                self.v[(i, "prod")] = {"enabled": True, "disabled": False}[f["production"]]
                self.v[(i, "roll")] = int(f["rollout"].rstrip("%"))
                self.v[(i, "kill")] = {"on": True, "off": False}[f["kill switch"]]

    def apply(self, e, kind, g):
        if kind == "revert":
            return self.revert(e, g["ref"])
        fid = g["id"]
        if fid not in self.flags_ids:
            return False
        if kind == "kill":
            self.setv(e.eid, (fid, "kill"), True)
            return True
        if kind == "override":
            key = (fid, "ovr:" + g["p"])
            prev = self.v.get(key) or ()
            if any(e.t < end for _, _, end in prev):
                self.w.flags.notes.add("override_over_override")
            self.setv(e.eid, key, prev + ((g["val"] == "on", e.t, e.t + timedelta(hours=int(g["h"]))),))
            return True
        if g.get("env") == "staging":
            return True  # staging changes never affect production (not a production request)
        if g["chg"] not in self.prm["tickets"]:
            return False
        if kind == "enable":
            self.setv(e.eid, (fid, "prod"), True)
        elif kind == "disable":
            self.setv(e.eid, (fid, "prod"), False)
        elif kind == "rollout":
            self.setv(e.eid, (fid, "roll"), int(g["pct"]))
        elif kind == "unkill":
            self.setv(e.eid, (fid, "kill"), False)
        else:
            raise SolverError(kind)
        return True

    def rollout(self, fid: str) -> int:
        if fid not in self.flags_ids:
            raise SolverError(f"unknown flag {fid}")
        return self.v[(fid, "roll")]

    def on_for(self, fid: str, p: str) -> bool:
        if fid not in self.flags_ids or p not in self.bucket:
            raise SolverError("flag/person")
        if self.v[(fid, "kill")]:
            return False
        ovs = self.v.get((fid, "ovr:" + p)) or ()
        if READINGS["override_overlap"] == "replace":
            ovs = ovs[-1:]
        live = [o for o in ovs if o[1] <= self.T < o[2]]
        if live:
            return max(live, key=lambda o: o[1])[0]
        return self.v[(fid, "prod")] and self.bucket[p] < self.v[(fid, "roll")]


# ---- docs (held out) -----------------------------------------------------------------------------------------------
class DocsSim(_Base):
    def __init__(self, w: World):
        super().__init__(w)
        _check_rule(w, "Each save or restore adds one new version at the end; the current version is the last one. A "
                       "restore of version k adds a new version with the content of version k. Version 1 is the "
                       "starting content.")
        self.vers: dict[str, list[str]] = {}
        self.lock: dict[str, tuple[str, datetime] | None] = {}
        self.appr: dict[str, set[int]] = {}
        for i, f in w.doc.entities:
            if f["lock"] != "none":
                raise SolverError("starting lock")
            self.vers[i] = [f["version 1 content"]]
            self.lock[i] = None
            self.appr[i] = set()

    def _holder(self, d: str, t: datetime) -> str | None:
        lk = self.lock[d]
        if lk is None or t >= lk[1]:
            return None
        return lk[0]

    def apply(self, e, kind, g):
        d = g["id"]
        if d not in self.vers:
            return False
        who, t = e.by, e.t
        hold = self._holder(d, t)
        if kind in ("save", "restore"):
            if hold is not None and hold != who:
                return False
            if kind == "save":
                self.vers[d].append(g["c"])
            else:
                k = int(g["k"])
                if not 1 <= k <= len(self.vers[d]):
                    self.w.flags.notes.add("restore_missing_version")
                    return False
                self.vers[d].append(self.vers[d][k - 1])
            return True
        if kind == "lock":
            if hold is not None:
                return False
            self.lock[d] = (who, t + timedelta(minutes=self.prm["lock_minutes"]))
            return True
        if kind == "unlock":
            if hold != who:
                return False
            self.lock[d] = None
            return True
        if kind == "approve":
            k = int(g["k"])
            if who not in self.prm["approvers"] or not 1 <= k <= len(self.vers[d]):
                return False
            self.appr[d].add(k)
            return True
        raise SolverError(kind)

    def content(self, d: str) -> str:
        return self.vers[d][-1]

    def n_versions(self, d: str) -> int:
        return len(self.vers[d])

    def approved(self, d: str) -> bool:
        return len(self.vers[d]) in self.appr[d]


def _check_rule(w: World, text: str, prefix: bool = False) -> None:
    """The simulator's semantics were written from these rule texts; refuse a row whose text differs."""
    for t in rules_text(w.doc):
        if (t.startswith(text) if prefix else t == text):
            return
    raise SolverError(f"{w.mach}: expected rule not found: {text[:70]!r}")


SIMS = {"orders": OrdersSim, "tickets": TicketsSim, "bookings": BookingsSim, "inventory": InventorySim,
        "ledger": LedgerSim, "access": AccessSim, "dialogue": DialogueSim, "agent": AgentSim, "flags": FlagsSim,
        "docs": DocsSim}


# ---------------------------------------------------------------------------------------------------------------
# 6. Questions and statements -> propositions / observables
# ---------------------------------------------------------------------------------------------------------------
WHEN = r"(?P<w>the end of the (?:log|chat|session)|\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)"
NM = r"(?P<p>[A-Z][\w'-]*(?: [A-Z][\w'-]*)+)"

# yes/no questions: (regex, observable kind, negate)
YN_Q: list[tuple[str, str, bool]] = [
    # orders
    (rf"Can order (?P<id>\S+) still be cancelled at {WHEN}\?", "o_cancel", False),
    (rf"Under the rules, would a cancellation request for order (?P<id>\S+) be allowed at {WHEN}\?", "o_cancel", False),
    (rf"Would a cancellation request for order (?P<id>\S+) be rejected at {WHEN}\?", "o_cancel", True),
    (rf"Under the numbered rules, is the status of order (?P<id>\S+) (?P<v>\w+) at {WHEN}\?", "o_status", False),
    (rf"Is order (?P<id>\S+) in any status other than (?P<v>\w+) at {WHEN}\?", "o_status", True),
    (rf"Is order (?P<id>\S+) in status (?P<v>\w+) at {WHEN}\?", "o_status", False),
    # tickets
    (rf"Under the numbered rules, does ticket (?P<id>\S+) belong to {NM} at {WHEN}\?", "t_owner", False),
    (rf"Is ticket (?P<id>\S+) owned by someone other than {NM} at {WHEN}, or by nobody\?", "t_owner", True),
    (rf"Is {NM} the owner of ticket (?P<id>\S+) at {WHEN}\?", "t_owner", False),
    (rf"Had ticket (?P<id>\S+) missed its resolution due time at {WHEN}\?", "t_overdue", False),
    (rf"Is ticket (?P<id>\S+) overdue at {WHEN} under the SLA rules\?", "t_overdue", False),
    (rf"Is ticket (?P<id>\S+) still within its SLA at {WHEN}, with no missed due time\?", "t_overdue", True),
    # access
    (rf"Under the numbered rules, does {NM} have at least viewer access to (?P<id>\S+) at {WHEN}\?", "a_view", False),
    (rf"Under the numbered rules, is {NM} allowed to edit (?P<id>\S+) at {WHEN}\?", "a_edit", False),
    (rf"Can {NM} open (?P<id>\S+) for viewing at {WHEN}\?", "a_view", False),
    (rf"Can {NM} edit (?P<id>\S+) at {WHEN}\?", "a_edit", False),
    (rf"Is {NM} shut out of viewing (?P<id>\S+) at {WHEN}\?", "a_view", True),
    (rf"Is {NM} unable to edit (?P<id>\S+) at {WHEN}\?", "a_edit", True),
    # inventory
    (rf"Are at least (?P<n>\d+) units? of (?P<id>\S+) available at {WHEN}\?", "i_atleast", False),
    (rf"Under the numbered rules, does (?P<id>\S+) have (?P<n>\d+) or more units available at {WHEN}\?", "i_atleast",
     False),
    (rf"Are fewer than (?P<n>\d+) units? of (?P<id>\S+) available at {WHEN}\?", "i_atleast", True),
    # bookings
    (rf"Under the numbered rules, could anyone place a new hold on (?P<id>\S+) at {WHEN}\?", "b_free", False),
    (rf"Is (?P<id>\S+) free for a new hold at {WHEN}\?", "b_free", False),
    (rf"Is (?P<id>\S+) taken at {WHEN}, by a confirmed booking or an active hold\?", "b_free", True),
    (rf"Under the numbered rules, is (?P<id>\S+) booked and confirmed for {NM} at {WHEN}\?", "b_conf", False),
    (rf"Does {NM} hold the confirmed booking of (?P<id>\S+) at {WHEN}\?", "b_conf", False),
    (rf"Is (?P<id>\S+) without a confirmed booking for {NM} at {WHEN}\?", "b_conf", True),
    # ledger
    (rf"Is the available balance of account (?P<id>\S+) at least {AMT} at {WHEN}\?", "l_atleast", False),
    (rf"Under the numbered rules, does account (?P<id>\S+) have {AMT} or more available at {WHEN}\?", "l_atleast",
     False),
    (rf"Is the available balance of account (?P<id>\S+) below {AMT} at {WHEN}\?", "l_atleast", True),
    # dialogue
    (rf"Under the numbered rules, does booking (?P<id>\S+) have (?P<v>.+?) as its (?P<s>[a-z ]+?) at {WHEN}\?",
     "d_slot", False),
    (rf"Is the (?P<s>[a-z ]+?) of booking (?P<id>\S+) something other than (?P<v>.+?) at {WHEN}\?", "d_slot", True),
    (rf"Is the (?P<s>[a-z ]+?) of booking (?P<id>\S+) (?P<v>.+?) at {WHEN}\?", "d_slot", False),
    # agent
    (rf"Under the numbered rules, is the quantity of (?P<id>\S+) in the cart (?P<n>\d+) or more at {WHEN}\?",
     "g_atleast", False),
    (rf"Does the cart hold at least (?P<n>\d+) of (?P<id>\S+) at {WHEN}\?", "g_atleast", False),
    (rf"Does the cart hold fewer than (?P<n>\d+) of (?P<id>\S+) at {WHEN}\?", "g_atleast", True),
    (rf"Is (?P<id>\S+) somewhere other than the (?P<v>\w+) folder at {WHEN}\?", "g_folder", True),
    (rf"Is (?P<id>\S+) in the (?P<v>\w+) folder at {WHEN}\?", "g_folder", False),
    (rf"Under the numbered rules, does the (?P<v>\w+) folder hold (?P<id>\S+) at {WHEN}\?", "g_folder", False),
    # flags
    (rf"Is (?P<id>FF-\d+) on for {NM} in production at {WHEN}\?", "f_on", False),
    (rf"Under the numbered rules, does {NM} get (?P<id>FF-\d+) in production at {WHEN}\?", "f_on", False),
    (rf"Is (?P<id>FF-\d+) off for {NM} in production at {WHEN}\?", "f_on", True),
    # docs
    (rf"Under the numbered rules, has the current version of (?P<id>\S+) been approved at {WHEN}\?", "k_appr", False),
    (rf"Is the current version of (?P<id>\S+) approved at {WHEN}\?", "k_appr", False),
    (rf"Is the current version of (?P<id>\S+) still unapproved at {WHEN}\?", "k_appr", True),
    (rf'Under the numbered rules, does the current version of (?P<id>\S+) hold the "(?P<v>[^"]+)" content at {WHEN}\?',
     "k_content", False),
    (rf'Does the current version of (?P<id>\S+) hold anything other than the "(?P<v>[^"]+)" content at {WHEN}\?',
     "k_content", True),
    (rf'Is the current version of (?P<id>\S+) the "(?P<v>[^"]+)" content at {WHEN}\?', "k_content", False),
]

# statements (JB options and the fallback question's proposition)
STMT: list[tuple[str, str, bool]] = [
    (rf"Order (?P<id>\S+) can still be cancelled at {WHEN}\.", "o_cancel", False),
    (rf"Order (?P<id>\S+) can no longer be cancelled at {WHEN}\.", "o_cancel", True),
    (rf"Order (?P<id>\S+) is not in status (?P<v>\w+) at {WHEN}\.", "o_status", True),
    (rf"Order (?P<id>\S+) is in status (?P<v>\w+) at {WHEN}\.", "o_status", False),
    (rf"{NM} does not own ticket (?P<id>\S+) at {WHEN}\.", "t_owner", True),
    (rf"{NM} owns ticket (?P<id>\S+) at {WHEN}\.", "t_owner", False),
    (rf"Ticket (?P<id>\S+) is not overdue at {WHEN}\.", "t_overdue", True),
    (rf"Ticket (?P<id>\S+) is overdue at {WHEN}\.", "t_overdue", False),
    (rf"{NM} cannot edit (?P<id>\S+) at {WHEN}\.", "a_edit", True),
    (rf"{NM} can edit (?P<id>\S+) at {WHEN}\.", "a_edit", False),
    (rf"{NM} cannot view (?P<id>\S+) at {WHEN}\.", "a_view", True),
    (rf"{NM} can view (?P<id>\S+) at {WHEN}\.", "a_view", False),
    (rf"At least (?P<n>\d+) units? of (?P<id>\S+) (?:are|is) available at {WHEN}\.", "i_atleast", False),
    (rf"Fewer than (?P<n>\d+) units? of (?P<id>\S+) (?:are|is) available at {WHEN}\.", "i_atleast", True),
    (rf"(?P<id>\S+) is not free for a new hold at {WHEN}\.", "b_free", True),
    (rf"(?P<id>\S+) is free for a new hold at {WHEN}\.", "b_free", False),
    (rf"{NM} does not hold the confirmed booking of (?P<id>\S+) at {WHEN}\.", "b_conf", True),
    (rf"{NM} holds the confirmed booking of (?P<id>\S+) at {WHEN}\.", "b_conf", False),
    (rf"Account (?P<id>\S+) has at least {AMT} available at {WHEN}\.", "l_atleast", False),
    (rf"Account (?P<id>\S+) has less than {AMT} available at {WHEN}\.", "l_atleast", True),
    (rf"The (?P<s>[a-z ]+?) of booking (?P<id>\S+) is not (?P<v>.+?) at {WHEN}\.", "d_slot", True),
    (rf"The (?P<s>[a-z ]+?) of booking (?P<id>\S+) is (?P<v>.+?) at {WHEN}\.", "d_slot", False),
    (rf"The cart holds at least (?P<n>\d+) of (?P<id>\S+) at {WHEN}\.", "g_atleast", False),
    (rf"The cart holds fewer than (?P<n>\d+) of (?P<id>\S+) at {WHEN}\.", "g_atleast", True),
    (rf"(?P<id>\S+) is not in the (?P<v>\w+) folder at {WHEN}\.", "g_folder", True),
    (rf"(?P<id>\S+) is in the (?P<v>\w+) folder at {WHEN}\.", "g_folder", False),
    (rf"(?P<id>FF-\d+) is on for {NM} in production at {WHEN}\.", "f_on", False),
    (rf"(?P<id>FF-\d+) is off for {NM} in production at {WHEN}\.", "f_on", True),
    (rf"The current version of (?P<id>\S+) is not approved at {WHEN}\.", "k_appr", True),
    (rf"The current version of (?P<id>\S+) is approved at {WHEN}\.", "k_appr", False),
    (rf'The current version of (?P<id>\S+) is not the "(?P<v>[^"]+)" content at {WHEN}\.', "k_content", True),
    (rf'The current version of (?P<id>\S+) is the "(?P<v>[^"]+)" content at {WHEN}\.', "k_content", False),
]

JUDGE_Q = [r"Is the agent's recorded state consistent with the log under the numbered rules\?",
           r"Is every value in the agent record supported by the log and the numbered rules\?",
           r"Does every entry of the agent record match what the log gives under the numbered rules\?"]
FALLBACK_Q = [r"Under the numbered rules, does this statement hold\? (?P<s>.+)",
              r"Given the log and the numbered rules, is this statement true\? (?P<s>.+)"]
JB_Q = [r"Based on the log and the numbered rules, which statement holds\?",
        r"Which statement follows from the log under the numbered rules\?",
        r"Given the numbered rules, which of these two statements is true of the log\?"]
FALLBACK_PAIR = ["yes, this holds", "no, this does not hold"]

# value questions (choice / score): (regex, observable)
VAL_Q: list[tuple[str, str]] = [
    (rf"What status does order (?P<id>\S+) have at {WHEN}, under the numbered rules\?", "o_status"),
    (rf"Under the order rules, which status is order (?P<id>\S+) in at {WHEN}\?", "o_status"),
    (rf"Under the rules, how many listed orders have status shipped or delivered at {WHEN}\?", "o_count"),
    (rf"How many of the listed orders are shipped or delivered at {WHEN}\?", "o_count"),
    (rf"Who owns ticket (?P<id>\S+) at {WHEN}, under the numbered rules\?", "t_owner"),
    (rf"Under the support rules, which person is the owner of ticket (?P<id>\S+) at {WHEN}\?", "t_owner"),
    (rf"Under the SLA rules, which escalation level applies to ticket (?P<id>\S+) at {WHEN}\?", "t_level"),
    (rf"What escalation level does ticket (?P<id>\S+) have at {WHEN}\?", "t_level"),
    (rf"Under the access rules, which access level applies to {NM} on (?P<id>\S+) at {WHEN}\?", "a_level"),
    (rf"What access does {NM} have to (?P<id>\S+) at {WHEN}, under the numbered rules\?", "a_level"),
    (rf"How many of the tracked people can edit (?P<id>\S+) at {WHEN}\?", "a_count"),
    (rf"Under the access rules, how many tracked people hold editing access to (?P<id>\S+) at {WHEN}\?", "a_count"),
    (rf"Under the stock rules, what is the available quantity of (?P<id>\S+) at {WHEN}\?", "i_units"),
    (rf"How many units of (?P<id>SKU-\d+) are available at {WHEN}, under the numbered rules\?", "i_units"),
    (rf"Which band does the available quantity of (?P<id>\S+) fall in at {WHEN}\?", "i_units"),
    (rf"Under the stock rules, in which availability band is (?P<id>\S+) at {WHEN}\?", "i_units"),
    (rf"Under the booking rules, whose confirmed booking is (?P<id>\S+) at {WHEN}\?", "b_conf"),
    (rf"Who holds the confirmed booking of (?P<id>\S+) at {WHEN}, under the numbered rules\?", "b_conf"),
    (rf"Under the booking rules, how many listed slots are booked and confirmed at {WHEN}\?", "b_count"),
    (rf"How many of the listed slots have a confirmed booking at {WHEN}\?", "b_count"),
    (rf"What is the posted balance of account (?P<id>\S+) at {WHEN}, under the numbered rules\?", "l_posted"),
    (rf"Under the ledger rules, which posted balance does account (?P<id>\S+) show at {WHEN}\?", "l_posted"),
    (rf"Which band does the available balance of account (?P<id>\S+) fall in at {WHEN}\?", "l_avail"),
    (rf"Under the ledger rules, in which band is the available balance of (?P<id>\S+) at {WHEN}\?", "l_avail"),
    (rf"What is the (?P<s>[a-z ]+?) of booking (?P<id>\S+) at {WHEN}, under the numbered rules\?", "d_slot"),
    (rf"Under the chat rules, which (?P<s>[a-z ]+?) does booking (?P<id>\S+) have at {WHEN}\?", "d_slot"),
    (rf"How many units of (?P<id>\S+) are in the cart at {WHEN}, under the numbered rules\?", "g_qty"),
    (rf"Under the tool-log rules, what quantity of (?P<id>\S+) is in the cart at {WHEN}\?", "g_qty"),
    (rf"Which folder is (?P<id>\S+) in at {WHEN}, under the numbered rules\?", "g_folder"),
    (rf"Under the tool-log rules, which folder holds (?P<id>\S+) at {WHEN}\?", "g_folder"),
    (rf"Under the tool-log rules, how many listed items have a quantity of (?P<n>\d+) or more in the cart at {WHEN}\?",
     "g_count"),
    (rf"How many of the listed items are in the cart \(quantity (?P<n>\d+) or more\) at {WHEN}\?", "g_count"),
    (rf"How many of the listed files are in the (?P<v>\w+) folder at {WHEN}\?", "g_fcount"),
    (rf"Under the tool-log rules, how many listed files sit in the (?P<v>\w+) folder at {WHEN}\?", "g_fcount"),
    (rf"What is the production rollout percentage of (?P<id>\S+) at {WHEN}, under the numbered rules\?", "f_roll"),
    (rf"Under the flag rules, which production rollout does (?P<id>\S+) have at {WHEN}\?", "f_roll"),
    (rf"Under the flag rules, in which rollout band is (?P<id>\S+) for production at {WHEN}\?", "f_roll"),
    (rf"Which band is the production rollout of (?P<id>\S+) in at {WHEN}\?", "f_roll"),
    (rf"Which content is the current version of (?P<id>\S+) at {WHEN}, under the numbered rules\?", "k_content"),
    (rf"Under the document rules, what does the current version of (?P<id>\S+) hold at {WHEN}\?", "k_content"),
    (rf"Under the document rules, how many versions of (?P<id>\S+) exist at {WHEN}\?", "k_count"),
    (rf"How many versions does (?P<id>\S+) have at {WHEN}\?", "k_count"),
]

MACHINE_OF_OBS = {"o": "orders", "t": "tickets", "a": "access", "i": "inventory", "b": "bookings", "l": "ledger",
                  "d": "dialogue", "g": "agent", "f": "flags", "k": "docs"}


def _match(pats, text):
    for pat, *rest in pats:
        m = re.fullmatch(pat, text)
        if m:
            return m, rest
    return None, None


class Solver:
    """One row: parse once, simulate on demand (cached per time)."""

    def __init__(self, row: dict[str, Any]):
        self.row = row
        pre = parse_state(row["state"])
        mach = machine_of(pre)
        slot_keys: list[str] = []
        if mach == "dialogue" and pre.fmt == "prose":
            # prose entities need the slot names (read from the rules)
            slot_keys = list(params(pre, mach)["slots"])
            pre = parse_state(row["state"], slot_keys)
        self.doc = pre
        self.mach = mach
        self.world = World(self.doc, mach)
        self._cache: dict[datetime, Any] = {}

    def when(self, w: str) -> datetime:
        if w.startswith("the end of the"):
            want = {"orders": "log", "tickets": "log", "access": "log", "inventory": "log", "bookings": "log",
                    "ledger": "log", "flags": "log", "docs": "log", "dialogue": "chat", "agent": "session"}[self.mach]
            if not w.endswith(want):
                raise SolverError(f"'{w}' in a {self.mach} row")
            return self.world.end
        return parse_time(w)

    def sim(self, T: datetime):
        if T not in self._cache:
            self._cache[T] = self.world.at(T)
        return self._cache[T]

    # propositions ------------------------------------------------------------------------------------------------
    def prop(self, obs: str, g: dict[str, str]) -> bool:
        if MACHINE_OF_OBS[obs[0]] != self.mach:
            raise SolverError(f"{obs} question in a {self.mach} row")
        s = self.sim(self.when(g["w"]))
        if obs == "o_cancel":
            return s.status(g["id"]) in ("created", "paid", "packed")
        if obs == "o_status":
            return s.status(g["id"]) == g["v"]
        if obs == "t_owner":
            return s.owner(g["id"]) == g["p"]
        if obs == "t_overdue":
            return s.overdue(g["id"])
        if obs == "a_view":
            return s.can(g["p"], g["id"], "viewer")
        if obs == "a_edit":
            return s.can(g["p"], g["id"], "editor")
        if obs == "i_atleast":
            return s.available(g["id"]) >= int(g["n"])
        if obs == "b_free":
            return s.free(g["id"])
        if obs == "b_conf":
            return s.confirmed(g["id"]) == g["p"]
        if obs == "l_atleast":
            if g["cur"] != s.cur:
                raise SolverError("currency")
            return s.available(g["id"]) >= _money(g["amt"])
        if obs == "d_slot":
            if g["id"] != s.bk:
                raise SolverError("booking id")
            if g["s"] not in s.val:
                raise SolverError(f"slot {g['s']}")
            return s.value(g["s"]) == g["v"]
        if obs == "g_atleast":
            return s.quantity(g["id"]) >= int(g["n"])
        if obs == "g_folder":
            return s.folder_of(g["id"]) == g["v"]
        if obs == "f_on":
            return s.on_for(g["id"], g["p"])
        if obs == "k_appr":
            return s.approved(g["id"])
        if obs == "k_content":
            return s.content(g["id"]) == g["v"]
        raise SolverError(obs)

    def statement(self, text: str) -> bool:
        m, rest = _match(STMT, text)
        if not m:
            raise SolverError(f"unread statement {text!r}")
        obs, neg = rest
        return self.prop(obs, m.groupdict()) != neg

    # values ------------------------------------------------------------------------------------------------------
    def value(self, obs: str, g: dict[str, str]) -> Any:
        if MACHINE_OF_OBS[obs[0]] != self.mach:
            raise SolverError(f"{obs} question in a {self.mach} row")
        s = self.sim(self.when(g["w"]))
        if obs == "o_status":
            return s.status(g["id"])
        if obs == "o_count":
            return sum(s.status(i) in ("shipped", "delivered") for i in s.ids)
        if obs == "t_owner":
            return s.owner(g["id"])
        if obs == "t_level":
            return s.escalation(g["id"])
        if obs == "a_level":
            return s.level(g["p"], g["id"])
        if obs == "a_count":
            return sum(s.can(p, g["id"], "editor") for p in s.prm["tracked"])
        if obs == "i_units":
            return s.available(g["id"])
        if obs == "b_conf":
            return s.confirmed(g["id"])
        if obs == "b_count":
            return sum(s.v[(i, "conf")] is not None for i in s.ids)
        if obs == "l_posted":
            return s.posted_of(g["id"])
        if obs == "l_avail":
            return s.available(g["id"])
        if obs == "d_slot":
            if g["id"] != s.bk:
                raise SolverError("booking id")
            return s.value(g["s"])
        if obs == "g_qty":
            return s.quantity(g["id"])
        if obs == "g_folder":
            return s.folder_of(g["id"])
        if obs == "g_count":
            return sum(q >= int(g["n"]) for q in s.qty.values())
        if obs == "g_fcount":
            return sum(f == g["v"] for f in s.folder.values())
        if obs == "f_roll":
            return s.rollout(g["id"])
        if obs == "k_content":
            return s.content(g["id"])
        if obs == "k_count":
            return s.n_versions(g["id"])
        raise SolverError(obs)

    # agent record (judge rows) -----------------------------------------------------------------------------------
    def record_ok(self) -> bool:
        if self.doc.record is None:
            raise SolverError("judge question without an agent record")
        t, entries = self.doc.record
        s = self.sim(t)
        ok = True
        for ent in entries:
            ok &= self._entry(s, ent)
        return ok

    def _entry(self, s, ent: str) -> bool:
        m = self.mach
        pats = {
            "orders": [(r"order (?P<id>\S+) status: (?P<v>\w+)", lambda g: s.status(g["id"]) == g["v"])],
            "tickets": [(r"ticket (?P<id>\S+) owner: (?P<v>.+)", lambda g: s.owner(g["id"]) == g["v"]),
                        (r"ticket (?P<id>\S+) status: (?P<v>\w+)", lambda g: s.status(g["id"]) == g["v"]),
                        (r"ticket (?P<id>\S+) overdue: (?P<v>yes|no)",
                         lambda g: s.overdue(g["id"]) == (g["v"] == "yes")),
                        (r"ticket (?P<id>\S+) escalation level: level (?P<v>\d) - .+",
                         lambda g: s.escalation(g["id"]) == int(g["v"]))],
            "access": [(rf"{NM} access on (?P<id>\S+): (?P<v>.+)", lambda g: s.level(g["p"], g["id"]) == g["v"])],
            "inventory": [(r"(?P<id>\S+) available units: (?P<v>\d+) units?",
                           lambda g: s.available(g["id"]) == int(g["v"]))],
            "bookings": [(r"(?P<id>\S+) confirmed booking: (?P<v>.+)", lambda g: s.confirmed(g["id"]) == g["v"]),
                         (r"(?P<id>\S+) free: (?P<v>yes|no)", lambda g: s.free(g["id"]) == (g["v"] == "yes"))],
            "ledger": [(rf"(?P<id>\S+) posted balance: {AMT}",
                        lambda g: s.posted_of(g["id"]) == _money(g["amt"]) and g["cur"] == s.cur),
                       (rf"(?P<id>\S+) available balance: {AMT}",
                        lambda g: s.available(g["id"]) == _money(g["amt"]) and g["cur"] == s.cur)],
            "dialogue": [(r"booking (?P<id>\S+) (?P<s>[a-z ]+?): (?P<v>.+)",
                          lambda g: g["id"] == s.bk and s.value(g["s"]) == g["v"])],
            "agent": [(r"(?P<id>\S+) quantity in cart: (?P<v>\d+) units?", lambda g: s.quantity(g["id"]) == int(g["v"])),
                      (r"(?P<id>\S+) folder: (?P<v>\w+)", lambda g: s.folder_of(g["id"]) == g["v"])],
            "flags": [(rf"(?P<id>\S+) for {NM}: (?P<v>on|off)", lambda g: s.on_for(g["id"], g["p"]) == (g["v"] == "on")),
                      (r"(?P<id>\S+) production rollout: (?P<v>\d+)%", lambda g: s.rollout(g["id"]) == int(g["v"]))],
            "docs": [(r"(?P<id>\S+) current content: (?P<v>.+)", lambda g: s.content(g["id"]) == g["v"]),
                     (r"(?P<id>\S+) current version approved: (?P<v>yes|no)",
                      lambda g: s.approved(g["id"]) == (g["v"] == "yes")),
                     (r"(?P<id>\S+) number of versions: (?P<v>\d+)", lambda g: s.n_versions(g["id"]) == int(g["v"]))],
        }[m]
        for pat, fn in pats:
            mm = re.fullmatch(pat, ent)
            if mm:
                return fn(mm.groupdict())
        raise SolverError(f"unread record entry {ent!r}")

    # options -----------------------------------------------------------------------------------------------------
    def pick(self, obs: str, val: Any, options: list[str], g: dict[str, str]) -> str:
        hits = [o for o in options if o != "None of these" and self._opt_is(obs, val, o, g)]
        if len(hits) > 1:
            raise Ambiguous(f"{len(hits)} options fit value {val!r}")
        if hits:
            return hits[0]
        if "None of these" in options:
            return "None of these"
        raise SolverError(f"no option fits value {val!r}: {options}")

    def _opt_is(self, obs: str, val: Any, o: str, g: dict[str, str]) -> bool:
        if obs in ("o_status", "t_owner", "a_level", "b_conf", "d_slot", "g_folder", "k_content"):
            return o == val
        if obs in ("o_count", "a_count", "b_count", "g_count", "g_fcount"):
            m = re.fullmatch(r"(?:(\d+)|none) of the (\d+) (?:listed|tracked) \w+", o)
            if not m:
                raise SolverError(f"count option {o!r}")
            return val == (int(m.group(1)) if m.group(1) else 0)
        if obs == "t_level":
            m = re.fullmatch(r"level (\d) - .+", o)
            if not m:
                raise SolverError(f"level option {o!r}")
            return int(m.group(1)) == val
        if obs in ("i_units", "g_qty"):
            m = (re.fullmatch(r"(\d+) units?", o) or re.fullmatch(r"(\d+) to (\d+) units", o)
                 or re.fullmatch(r"(\d+) units or more", o))
            if not m:
                raise SolverError(f"units option {o!r}")
            if o.endswith("or more"):
                return val >= int(m.group(1))
            if " to " in o:
                return int(m.group(1)) <= val <= int(m.group(2))
            return val == int(m.group(1)) and o == _units(val)
        if obs == "l_posted":
            m = re.fullmatch(AMT, o)
            if not m:
                raise SolverError(f"money option {o!r}")
            return _money(m["amt"]) == val and m["cur"] == self.sim(self.when(g["w"])).cur
        if obs == "l_avail":
            cur = self.sim(self.when(g["w"])).cur
            m = re.fullmatch(r"below ([\d,]+\.\d\d) ([A-Z]{3})", o)
            if m:
                return m.group(2) == cur and val < _money(m.group(1))
            m = re.fullmatch(r"([\d,]+\.\d\d) to ([\d,]+\.\d\d) ([A-Z]{3})", o)
            if m:
                return m.group(3) == cur and _money(m.group(1)) <= val <= _money(m.group(2))
            m = re.fullmatch(r"([\d,]+\.\d\d) or more ([A-Z]{3})", o)
            if m:
                return m.group(2) == cur and val >= _money(m.group(1))
            raise SolverError(f"band option {o!r}")
        if obs == "f_roll":
            m = re.fullmatch(r"(\d+)%", o)
            if m:
                return val == int(m.group(1))
            m = re.fullmatch(r"(\d+)% to (\d+)%", o)
            if m:
                return int(m.group(1)) <= val <= int(m.group(2))
            raise SolverError(f"rollout option {o!r}")
        if obs == "k_count":
            m = re.fullmatch(r"(\d+) versions?", o)
            if m:
                return val == int(m.group(1))
            m = re.fullmatch(r"(\d+) or more versions", o)
            if m:
                return val >= int(m.group(1))
            raise SolverError(f"versions option {o!r}")
        raise SolverError(obs)

    # the row -----------------------------------------------------------------------------------------------------
    def answer(self) -> str:
        q, opts = self.row["instructions"], self.row["options"]
        if opts == ["yes", "no"]:
            for pat in JUDGE_Q:
                if re.fullmatch(pat, q):
                    return "yes" if self.record_ok() else "no"
            m, rest = _match(YN_Q, q)
            if not m:
                raise SolverError(f"unread yes/no question {q!r}")
            obs, neg = rest
            return "yes" if self.prop(obs, m.groupdict()) != neg else "no"
        if opts == FALLBACK_PAIR:
            for pat in FALLBACK_Q:
                m = re.fullmatch(pat, q)
                if m:
                    return opts[0] if self.statement(m.group("s")) else opts[1]
            raise SolverError(f"fallback pair with question {q!r}")
        if any(re.fullmatch(p, q) for p in JB_Q):
            if len(opts) != 2:
                raise SolverError("JB row needs two statements")
            v = [self.statement(o) for o in opts]
            if v[0] == v[1]:
                raise Ambiguous(f"both JB statements are {v[0]}")
            return opts[0] if v[0] else opts[1]
        m, rest = _match(VAL_Q, q)
        if not m:
            raise SolverError(f"unread question {q!r}")
        obs = rest[0]
        g = m.groupdict()
        return self.pick(obs, self.value(obs, g), opts, g)


def decide2_row(row: dict[str, Any]) -> Any:
    """The independent gold for one raw F3 row, or UNDEFINED when the row cannot be decided."""
    try:
        return Solver(row).answer()
    except SolverError:
        return UNDEFINED


def explain_row(row: dict[str, Any]) -> dict[str, Any]:
    """decide2 plus the reason when it fails and the replay notes (for the report)."""
    try:
        s = Solver(row)
        a = s.answer()
        return {"answer": a, "notes": sorted(s.world.flags.notes)}
    except Ambiguous as e:
        return {"answer": UNDEFINED, "error": f"ambiguous: {e}"}
    except SolverError as e:
        return {"answer": UNDEFINED, "error": str(e)}


# ---------------------------------------------------------------------------------------------------------------
# 7. Report
# ---------------------------------------------------------------------------------------------------------------
# Every mismatch of the 30 Sep build, traced by hand (see the final report); keyed by rid.
DIAGNOSIS: dict[str, dict[str, str]] = {}
_ASSIST = ("generator bug: the contrast twin rewrote an Assistant proposal ('Shall I switch the {s} to {v}?') into "
           "the request sentence 'Please set the {s} to {v}.' but kept the speaker 'Assistant'. The rules say only "
           "the customer's own requests change slots, so the line changes nothing and the twin does not flip; the "
           "program gold applies it.")
for _rid, _s, _v in [("f3-tr-004911-1", "menu", "tasting menu"), ("f3-tr-008864-1", "time", "18:30"),
                     ("f3-tr-009213-1", "time", "18:30")]:
    DIAGNOSIS[_rid] = {"kind": "generator_bug", "why": _ASSIST.format(s=_s, v=_v)}
for _rid in ("f3-tr-009128-0", "f3-tr-009128-1", "f3-tr-009128-2"):
    DIAGNOSIS[_rid] = {
        "kind": "generator_bug",
        "why": "revert E2295 names E7565, an assignment made while TCK-394415 was already 'assigned' (it changed "
               "only the owner). The rule restores only 'every value it changed', so the owner goes back to Kisia "
               "Zinholm and the status stays 'closed'; the later assignment E5398 is then rejected (closed ticket). "
               "The program gold (owner Basetta Desley) is reproduced exactly when the revert also resets the "
               "status to 'assigned', i.e. the generator treats the unchanged status as changed by the assignment. "
               "That variant changes no other ticket row."}
DIAGNOSIS["f3-tr-007254-0"] = {
    "kind": "ambiguous",
    "why": "files.restore(path=notes-2285.pdf) -> ok at 12:53 while the file is in archive, not trash. The rule "
           "says 'files.restore moves it from trash to inbox'; with nothing in trash the call can be read as a no-op "
           "(this solver) or as 'move to inbox' (the program gold; the row's contrast twin relies on it). Fix: never "
           "emit an ok restore of a file that is not in trash, or word the rule 'files.restore moves the file to "
           "inbox'."}
for _rid in ("f3-dh-000146-0", "f3-dh-000146-1", "f3-dh-000286-0"):
    DIAGNOSIS[_rid] = {
        "kind": "generator_bug",
        "why": "two overrides of one flag for one person: a newer, shorter override ends before the stated time "
               "while an older, longer one ('lasts the stated hours from its time') is still in force. The program "
               "gold lets the newer override cancel the older one; no rule says so. Fix the rule text ('a new "
               "override for the same person replaces any earlier one') or the generator."}


def _tz_info() -> dict[str, str]:
    """The SLA clock needs the tz database; record which one this run used (zoneinfo, system or tzdata)."""
    for root in ("/usr/share/zoneinfo", "/var/db/timezone/zoneinfo"):
        vp = Path(root) / "+VERSION"
        if vp.exists():
            return {"source": f"system:{root}", "version": vp.read_text().strip()}
    try:  # pragma: no cover
        import tzdata  # type: ignore
        return {"source": "tzdata", "version": getattr(tzdata, "IANA_VERSION", "?")}
    except Exception:  # pragma: no cover
        return {"source": "unknown", "version": "?"}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _qclass(r: dict[str, Any]) -> str:
    m = r["meta"]
    if m.get("judge"):
        return "judge"
    return {"yn": "yes/no", "choice": "choice", "score": "score", "jb": "jb"}.get(m.get("qkind"), str(m.get("qkind")))


def run(paths: dict[str, Path]) -> dict[str, Any]:
    rep: dict[str, Any] = {"tool": "golden_src/gen3/v3_state_track.py", "key": KEY, "inputs": {}, "parts": {}}
    for part, p in paths.items():
        rows = [json.loads(line) for line in p.open()]
        rep["inputs"][part] = {"path": str(p.relative_to(LEAN)), "sha256": _sha(p), "rows": len(rows)}
        agg: dict[str, Any] = {"rows": len(rows), "agree": 0, "disagree": 0, "undefined": 0}
        by: dict[str, Counter] = defaultdict(Counter)
        dis: list[dict[str, Any]] = []
        notes = Counter()
        for r in rows:
            ex = explain_row(r)
            a = ex["answer"]
            keyq = f"{r['meta'].get('pack')}/{_qclass(r)}"
            by[keyq]["rows"] += 1
            for n in ex.get("notes", []):
                notes[n] += 1
            if a is UNDEFINED:
                agg["undefined"] += 1
                by[keyq]["undefined"] += 1
                dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": None, "error": ex.get("error"),
                            "fmt": r["meta"].get("fmt"), "q": r["instructions"]})
            elif a == r["gold"]:
                agg["agree"] += 1
                by[keyq]["agree"] += 1
            else:
                agg["disagree"] += 1
                by[keyq]["disagree"] += 1
                dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": a, "notes": ex.get("notes"),
                            "fmt": r["meta"].get("fmt"), "q": r["instructions"]})
        agg["rate"] = round(agg["agree"] / max(1, agg["rows"]), 6)
        agg["by_machine_question"] = {k: dict(v) for k, v in sorted(by.items())}
        agg["replay_notes"] = dict(notes)
        agg["mismatches"] = dis
        rep["parts"][part] = agg
    return rep


def readings_sensitivity(paths: dict[str, Path]) -> dict[str, Any]:
    """For every READINGS switch: the rows whose decide2 answer changes under the other reading (with the program
    gold), i.e. the rows where the rendered text alone does not settle the label."""
    rows = [(part, json.loads(line)) for part, p in paths.items() for line in p.open()]
    base = {r["rid"]: explain_row(r)["answer"] for _, r in rows}
    out: dict[str, Any] = {}
    saved = dict(READINGS)
    try:
        for k in saved:
            READINGS.clear()
            READINGS.update(saved)
            READINGS[k] = ALT_READINGS[k]
            ch = []
            for part, r in rows:
                a = explain_row(r)["answer"]
                if a != base[r["rid"]]:
                    ch.append({"rid": r["rid"], "part": part, "gold": r["gold"],
                               "primary": None if base[r["rid"]] is UNDEFINED else base[r["rid"]],
                               "alt": None if a is UNDEFINED else a})
            out[k] = {"primary": saved[k], "alt": ALT_READINGS[k], "rows_changed": len(ch),
                      "gold_follows": ("primary" if all(c["gold"] == c["primary"] for c in ch) else
                                       "alt" if all(c["gold"] == c["alt"] for c in ch) else "mixed") if ch else None,
                      "rows": ch}
    finally:
        READINGS.clear()
        READINGS.update(saved)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-report", action="store_true")
    ap.add_argument("--train", default=str(TRAIN_PATH))
    ap.add_argument("--dev", default=str(DEV_PATH))
    a = ap.parse_args()
    paths = {"train": Path(a.train), "dev": Path(a.dev)}
    rep = run(paths)
    rep["readings"] = readings_sensitivity(paths)
    rep["diagnosis"] = DIAGNOSIS
    rep["solver_sha256"] = _sha(Path(__file__))
    rep["tz"] = _tz_info()
    for part, v in rep["parts"].items():
        print(part, {k: v[k] for k in ("rows", "agree", "disagree", "undefined", "rate")})
        for d in v["mismatches"][:40]:
            print("  ", d)
    for k, v in rep["readings"].items():
        print("reading", k, v["primary"], "vs", v["alt"], "rows changed:", v["rows_changed"], "gold follows:",
              v["gold_follows"])
    if a.write_report:
        REPORT_PATH.write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str) + "\n")
        rec = {"written": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "tool": "golden_src/gen3/v3_state_track.py", "key": KEY, "part": "decide2_agreement",
               "path": str(REPORT_PATH.relative_to(LEAN)), "rows": sum(v["rows"] for v in rep["parts"].values()),
               "sha256": _sha(REPORT_PATH), "inputs": rep["inputs"], "solver_sha256": rep["solver_sha256"],
               "tz": rep["tz"], "readings": READINGS,
               "agreement": {p: {k: v[k] for k in ("rows", "agree", "disagree", "undefined", "rate")}
                             for p, v in rep["parts"].items()}}
        with MANIFEST.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("wrote", REPORT_PATH)


if __name__ == "__main__":
    main()
