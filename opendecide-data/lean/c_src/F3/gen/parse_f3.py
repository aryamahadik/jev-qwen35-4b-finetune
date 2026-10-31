"""parse_f3: the G3 round-trip parser (G0 spec section 3, G3 checks 1-8).

Written from the spec and the two registries (registry.py: statement ids, surface grammar, record columns, stems)
plus the formats-1 style DATA (styles.jsonl / skins.jsonl, read as JSON). It never imports the renderer, the samplers,
textforms or fmt1's renderer code (an import lint in the G3 report checks this). Container readers: markdown tables,
HTML, JSON, YAML, key-value records, pipe tables, log lines, notices (email / chat / memo / prose), git-like lines,
and prose / memo / bullet text by sentence-level grammar match. A null, '~', empty string, empty 'key:' value or XF06
unknown marker in an F3 row is a parse failure (rule 20, R3-06).
"""
from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser

import yaml

import canon
import registry as R
import solver_a as SA
import solver_b as SB
from f3common import C_SRC, DATE_PATTERNS, FMT1_DIR, parse_date

import sys  # noqa: E402
sys.path.insert(0, str(C_SRC / "common"))
import negcount  # noqa: E402

# ------------------------------------------------------------------------------------------------ style data

_STYLES = {}
_SKINS = {}
for _l in open(FMT1_DIR / "data" / "styles.jsonl", encoding="utf-8"):
    if _l.strip():
        _o = json.loads(_l)
        _STYLES[_o["id"]] = _o
for _l in open(FMT1_DIR / "data" / "skins.jsonl", encoding="utf-8"):
    if _l.strip():
        _o = json.loads(_l)
        _SKINS[_o["id"]] = _o

ID = r"[A-Z]{2,4}-[0-9A-Z]{2,5}"
DOC = r"[A-Z]{2,3}-\d{2,3}"
ANYDATE = "(?:" + "|".join(DATE_PATTERNS[k] for k in ("iso", "mon_dmy", "mon_mdy", "num_dmy")) + ")"
TIME = r"\d{2}:\d{2}"
WORDS = r"[A-Za-z][A-Za-z' -]*?"


class ParseError(ValueError):
    pass


def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------------------------------------ template -> regex

def tregex(tmpl, slots, *, anchor=False):
    """Compile a registry template: literal text escaped (spaces -> \\s+), slots from `slots` (name -> regex);
    a slot used twice becomes a back-reference."""
    out, seen, pos = [], set(), 0
    for m in re.finditer(r"\{(\w+)\}", tmpl):
        lit = tmpl[pos:m.start()]
        out.append(re.escape(lit).replace(r"\ ", r"\s+"))
        name = m.group(1)
        if name in seen:
            out.append(f"(?P={name})")
        else:
            seen.add(name)
            out.append(f"(?P<{name}>{slots.get(name, '.+?')})")
        pos = m.end()
    out.append(re.escape(tmpl[pos:]).replace(r"\ ", r"\s+"))
    body = "".join(out)
    return re.compile(("^" + body + "$") if anchor else body)


# statement slots
T_SLOTS = {"item": WORDS, "items": WORDS, "holder": WORDS, "holders": WORDS, "field": WORDS, "qty": WORDS,
           "unit": WORDS, "kind": WORDS, "default": "[^']+", "S": "[^']+", "NEI": "[^']+", "None": "[^']+",
           "gap": "[^']+", "N0": r"\d+", "D0": ANYDATE, "Dlast": ANYDATE, "key": "subject|entry number|no particular key",
           "order": "date and time|date|effective-date", "dateorder": "day/month/year|month/day/year",
           "listing": "newest first|oldest first", "values": r"'[^']+'(?:, '[^']+')*",
           "qtyclause": r"(?:, and a blank [A-Za-z][A-Za-z' -]*? in a creation starts as 0)?",
           "code": "[^']+", "word": "[^']+", "meaning": r"[^.\n]+?"}
T_RE = {tid: [tregex(v, T_SLOTS) for v in vs] for tid, vs in R.T.items()}


def find_statements(text):
    """{T id: slot dict} for every registered statement found in the (normalised) card text; masked / swapped
    definitions as lists."""
    t = _norm(text)
    found = {}
    for tid, regs in T_RE.items():
        for rg in regs:
            if tid in ("T36m", "T36s"):
                ms = [m.groupdict() for m in rg.finditer(t)]
                if ms:
                    found.setdefault(tid, []).extend(ms)
                continue
            m = rg.search(t)
            if m:
                found[tid] = m.groupdict()
                break
    return found


# ------------------------------------------------------------------------------------------------ dates

def detect_date_format(dates, dateorder=None):
    for k in ("iso", "mon_dmy", "mon_mdy"):
        if dates and all(re.fullmatch(DATE_PATTERNS[k], d) for d in dates):
            return k
    if dates and all(re.fullmatch(DATE_PATTERNS["num_dmy"], d) for d in dates):
        if dateorder == "day/month/year":
            return "num_dmy"
        if dateorder == "month/day/year":
            return "num_mdy"
        raise ParseError("numeric dates without a stated date order")
    raise ParseError("unrecognised date format")


DT_RE = re.compile(f"(?P<date>{ANYDATE})(?: (?P<time>{TIME}))?")


# ------------------------------------------------------------------------------------------------ entry grammar

E_SLOTS = {"item": ID, "holder": ID, "sender": ID, "receiver": ID, "old": ID, "new": ID, "rec": ID, "doc": DOC,
           "s": "[^']+", "q": r"\d+", "a": r"\d+", "t": r"\d+(?:\.\d+)?", "kind": WORDS, "hnoun": WORDS,
           "field": WORDS, "qty": WORDS, "unit": WORDS, "doctype": WORDS, "m": r"\d+", "mk": r"\d+",
           "receiver2": ID}
BODY_RE = [(key, tregex(t, E_SLOTS, anchor=True)) for key, ts in R.BODY.items() for t in ts]
BODY4_RE = [(key, tregex(t, E_SLOTS, anchor=True)) for key, ts in R.BODY4.items() for t in ts]
GIT_SLOTS = dict(E_SLOTS, th="[0-9a-f]{12}", qtail=r"(?: [A-Za-z][A-Za-z' -]*? \d+)?")
GIT_RE = [(key, tregex(t, GIT_SLOTS, anchor=True)) for key, t in R.GIT.items()]
REG_RE = [tregex(t, E_SLOTS, anchor=True) for t in R.REGISTER_ITEM] + \
         [tregex(t, E_SLOTS, anchor=True) for t in R.REGISTER_ITEM_NQ]
REGDOC_RE = [tregex(t, E_SLOTS, anchor=True) for t in R.REGISTER_DOC]
HEAD_RE = [re.compile(r"Entry (?P<n>\d+) \((?P<dt>" + ANYDATE + f"(?: {TIME})?)\\): "),
           re.compile(r"No\. (?P<n>\d+), (?P<dt>" + ANYDATE + f"(?: {TIME})?): ")]
HEAD6_RE = [re.compile(r"Entry (?P<n>\d+) \(recorded (?P<rd>" + ANYDATE + r")(?:, effective (?P<ed>" + ANYDATE
                       + r"))?\): "),
            re.compile(r"No\. (?P<n>\d+), recorded (?P<rd>" + ANYDATE + r")(?:, effective (?P<ed>" + ANYDATE
                       + r"))?: ")]
LOGHEAD_RE = re.compile(r"(?<!to )entry (?P<n>\d+): ")
NOTE_RE = re.compile(r" \(note: (?P<text>[^()]*)\)\.$")


def parse_body(body, *, s4=False):
    """One entry body sentence -> (type key, slots). Notes are stripped first (T33)."""
    note = None
    m = NOTE_RE.search(body)
    if m:
        note = m.group("text")
        body = body[:m.start()] + "."
    for key, rg in (BODY4_RE if s4 else []) + BODY_RE:
        mm = rg.match(body)
        if mm:
            return key, mm.groupdict(), note
    raise ParseError("entry body matches no registered phrasing")


def body_to_entry(key, g, n, date, time, *, ref=None, k=None, s4_targets=None):
    """Registry body key + slots -> structure entry (targets are entry numbers; S4: resolved later)."""
    e = {"n": n, "date": date, "time": time}
    if ref is not None:
        e["ref"], e["k"] = ref, k
    if key.startswith("CREATE"):
        e.update(t="CREATE", item=g["item"], holder=g["holder"], status=g.get("s"),
                 qty=int(g["q"]) if g.get("q") is not None else None)
    elif key == "SET_status":
        e.update(t="SET", item=g["item"], field="status", value=g["s"])
    elif key == "SET_qty":
        e.update(t="SET", item=g["item"], field="qty", value=int(g["q"]))
    elif key in ("ADJUST_up", "ADJUST_down"):
        e.update(t="ADJUST", item=g["item"], sign=1 if key.endswith("up") else -1, amount=int(g["a"]))
    elif key == "TRANSFER":
        e.update(t="TRANSFER", item=g["item"], sender=g["sender"], receiver=g["receiver"])
    elif key == "VOID":
        e.update(t="VOID", target=int(g["t"]))
    elif key.startswith("CORR_") or key.startswith("AMEND_"):
        kind = key.split("_", 1)[1]
        slot = {"value_s": "value", "value_q": "value", "amount_up": "amount", "amount_down": "amount",
                "receiver": "receiver", "status": "status", "qty": "qty"}[kind]
        val = g.get("s") if kind in ("value_s", "status") else (g.get("receiver") if kind == "receiver" else
                                                                int(g.get("q") or g.get("a")))
        if key.startswith("AMEND_"):
            e.update(t="CORR", target=("ref", int(g["m"]), int(g["mk"])), slot=slot, value=val)
        else:
            tg = g["t"]
            e.update(t="CORR", target=int(tg) if "." not in tg else ("ref",) + tuple(int(x) for x in tg.split(".")),
                     slot=slot, value=val)
        e["_dir"] = "up" if kind == "amount_up" else ("down" if kind == "amount_down" else None)
    elif key == "SUPERSEDE":
        e.update(t="SUPERSEDE", old=g["old"], new=g["new"])
    elif key == "OPEN":
        e.update(t="OPEN", record=g["rec"], doc=g["doc"], _doctype=g.get("doctype"))
    elif key in ("RENAME_item", "RENAME_holder"):
        e.update(t="RENAME", kind=None, old=g["old"], new=g["new"])
    elif key == "MERGE":
        e.update(t="MERGE", absorbed=g["old"], survivor=g["new"])
    elif key == "WITHDRAW":
        e.update(t="WITHDRAW", target_ref=int(g["m"]))
    else:
        raise ParseError(f"unknown body key {key}")
    return e


# ------------------------------------------------------------------------------------------------ container readers

class _HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines, self.tables = [], []
        self._cell, self._row, self._tab, self._buf, self._caption = None, None, None, [], None
        self._in = []

    def handle_starttag(self, tag, attrs):
        self._in.append(tag)
        if tag == "table":
            self._tab = {"caption": self._caption, "rows": []}
            self._caption = None
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = []
        elif tag in ("li", "p", "h1", "h2", "h3", "h4", "dt", "dd", "caption"):
            self._buf = []

    def handle_endtag(self, tag):
        if self._in:
            self._in.pop()
        if tag in ("td", "th") and self._cell is not None:
            self._row.append(("".join(self._cell)).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self._tab["rows"].append(self._row)
            self._row = None
        elif tag == "table" and self._tab is not None:
            self.tables.append(self._tab)
            self._tab = None
        elif tag in ("li", "p", "dt", "dd"):
            self.lines.append(("".join(self._buf)).strip())
        elif tag in ("h1", "h2", "h3", "h4", "caption"):
            self._caption = ("".join(self._buf)).strip()
            self.lines.append(self._caption)

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)
        else:
            self._buf.append(data)


def _walk_strings(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            _walk_strings(v, out)
    elif isinstance(o, list):
        for v in o:
            _walk_strings(v, out)


def _walk_records(o, out):
    if isinstance(o, dict):
        if all(not isinstance(v, (dict, list)) for v in o.values()) and len(o) >= 2:
            out.append(o)
            return
        for v in o.values():
            _walk_records(v, out)
    elif isinstance(o, list):
        for v in o:
            _walk_records(v, out)


def unfence(state, style):
    """Strip the style's fence (data: fences.jsonl names) and any title line printed above a fenced block."""
    f = style.get("fence", "FN-none")
    if f in ("FN-bt", "FN-btlang"):
        ls = state.split("\n")
        i = next(k for k, ln in enumerate(ls) if ln.startswith("```"))
        j = max(k for k, ln in enumerate(ls) if ln.strip() == "```")
        return "\n".join(ls[i + 1:j])
    if f == "FN-ind4":
        ls = state.split("\n")
        body = [ln[4:] for ln in ls if ln.startswith("    ")]
        start = next((k for k, ln in enumerate(ls) if ln.startswith("    ")), 0)
        return "\n".join(ln[4:] if ln.startswith("    ") else ln for ln in ls[start:])
    return state


def read_container(state, style):
    """(text lines, record dicts) from the state text, by the style's container and skin (data only)."""
    state = unfence(state, style)
    cont = style["container"]
    skin = _SKINS[style["skin"]]
    p = skin.get("params", {})
    lines, recs = [], []
    if re.search(r"(?<![A-Za-z])(null|None|n/a|N/A|TBD)(?![A-Za-z])", state) and cont in ("json", "yaml"):
        if re.search(r":\s*(null|~)\s*(,|\n|}|$)", state):
            raise ParseError("null value in an F3 row (rule 20)")
    if cont == "json":
        body = state
        if p.get("layout") == "lines":
            objs = [json.loads(l) for l in body.splitlines() if l.strip()]
        else:
            objs = [json.loads(body)]
        for o in objs:
            _check_typed(o)
            _walk_records(o, recs)
            strs = []
            _walk_strings(o, strs)
            lines += strs
        return lines, recs
    if cont == "yaml":
        o = yaml.safe_load(state)
        _check_typed(o)
        _walk_records(o, recs)
        strs = []
        _walk_strings(o, strs)
        return strs, recs
    if cont == "html_snippet":
        hp = _HTML()
        hp.feed(state)
        for tb in hp.tables:
            rows = tb["rows"]
            if not rows:
                continue
            head = rows[0]
            for r in rows[1:]:
                recs.append({h: html.unescape(c) for h, c in zip(head, r) if c != ""})
        return [html.unescape(x) for x in hp.lines if x], recs
    if cont == "markdown_table" or (cont == "memo" and p.get("table") == "pipe"):
        cur = None
        for ln in state.split("\n"):
            s = ln.strip()
            if cont == "markdown_table" and s.startswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
                    continue
                if cur is None:
                    cur = cells
                else:
                    recs.append({h: c for h, c in zip(cur, cells) if c != ""})
                continue
            if cont == "memo" and " | " in ln and not s.startswith(("MEMO", "Quick", "Internal")):
                cells = [c.strip() for c in ln.split("|")]
                if cur is None or len(cells) != len(cur):
                    cur = cells
                else:
                    recs.append({h: c for h, c in zip(cur, cells) if c != ""})
                continue
            cur = None
            if s:
                lines.append(s)
        return lines, recs
    if cont == "key_value":
        sep = {"{key}: {value}": ": ", "{key} = {value}": " = ", "{key}={value}": "=", "{key} :: {value}": " :: ",
               "{key} {dots} {value}": None, "{key}:{pad} {value}": None}[p["line"]]
        for block in re.split(r"\n\s*\n", state):
            d = {}
            for ln in block.split("\n"):
                s = ln.rstrip()
                if not s:
                    continue
                if p["line"] == "{key} {dots} {value}":
                    m = re.match(r"^(\S+(?: \S+)*?) \.{3,} (.*)$", s)
                elif p["line"] == "{key}:{pad} {value}":
                    m = re.match(r"^([^:]+):\s+(.*)$", s)
                else:
                    if sep not in s:
                        lines.append(s)
                        continue
                    k, v = s.split(sep, 1)
                    m = None
                    if v == "" or v.strip() == "":
                        raise ParseError("empty 'key:' value (rule 20)")
                    d[k.strip()] = v
                    continue
                if not m:
                    lines.append(s)
                    continue
                if m.group(2).strip() == "":
                    raise ParseError("empty 'key:' value (rule 20)")
                d[m.group(1).strip()] = m.group(2)
            if len(d) >= 2:
                recs.append(d)
        return lines, recs
    # text containers: prose, memo, bullet_sop, email_thread, chat_log, log_lines
    out = []
    for ln in state.split("\n"):
        s = ln.strip()
        s = re.sub(r"^(?:>\s?)+", "", s)
        if cont == "log_lines" and p.get("parts") == ["logfmt"]:
            m = re.search(r'msg=("(?:[^"\\]|\\.)*"|\S+)$', s)
            ts = re.match(r"time=(.*?) (?:level=|actor=|msg=)", s)
            if m:
                msg = json.loads(m.group(1)) if m.group(1).startswith('"') else m.group(1)
                s = (ts.group(1) if ts else "") + " " + msg
        if s:
            out.append(s)
    return out, recs


def _check_typed(o):
    if o is None:
        raise ParseError("null value in an F3 row (rule 20)")
    if isinstance(o, dict):
        for v in o.values():
            _check_typed(v)
    elif isinstance(o, list):
        for v in o:
            _check_typed(v)
    elif isinstance(o, str) and (o.strip() == "" or o.strip().lower() in ("unknown", "not recorded", "~")):
        raise ParseError("empty or unknown-marker value (rule 20)")
    elif isinstance(o, bool):
        raise ParseError("boolean value in an F3 row (rule 20)")


# ------------------------------------------------------------------------------------------------ state parsing

def _key(k):
    return re.sub(r"[^a-z0-9]", "", str(k).lower())


FIXED = {_key(v): k for k, v in R.COL.items()}


def parse_state(state, style, stm, card_text_dateorder=None):
    """-> dict with register items / docs, entries (structure schema), gaps info, sampler kind, d0, notes count."""
    lines, recs = read_container(state, style)
    joined = "\n".join(lines)
    out = {"items": [], "docs": [], "entries": [], "markers": [], "sampler": None, "d0": None, "dates": [],
           "notes": 0, "notices": {}}
    gap = (stm.get("T3x") or stm.get("T3x4") or {}).get("gap")
    # S6 opening snapshot date
    if stm.get("T6"):
        out["d0_raw"] = stm["T6"]["D0"]
    else:
        m = re.search(r"Opening snapshot \(end of (" + ANYDATE + r")\)", joined, re.I)
        if m:
            out["d0_raw"] = m.group(1)
    # register lines (sentences)
    for ln in _sentences(lines):
        for rg in REG_RE:
            mm = rg.match(ln)
            if mm:
                g = mm.groupdict()
                out["items"].append([g["item"], g["holder"], g["s"], int(g["q"]) if g.get("q") else None])
                break
        for rg in REGDOC_RE:
            mm = rg.match(ln)
            if mm:
                out["docs"].append([mm.group("doc"), mm.group("rec")])
                out.setdefault("doctype", {})[mm.group("doc")] = mm.group("doctype")
    # git lines (S5)
    if re.search(r"\b[0-9a-f]{12}\b", joined) and " seq " in joined:
        _parse_git(lines, out)
        return out
    # notices (S4)
    if re.search(r"(?:Notice \d+, dated |Reference \d+, )", joined):
        _parse_notices(joined, out, gap)
        return out
    if recs and any(_key(k) == "action" for r in recs for k in r):
        _parse_records(recs, out)
    else:
        _parse_sentences(lines, out, gap)
    return out


def _sentences(lines):
    """Split text lines into register-line / entry candidates (prose inline mode joins sentences)."""
    out = []
    for ln in lines:
        ln = re.sub(r"^(?:[-*•+·]|\d+[.)]|Step \d+:|\(\d+\)|\[[^\]]*\])\s+", "", ln.strip())
        out.append(ln)
        # inline prose: several register sentences on one line
        parts = re.split(r"(?<=\.) (?=\S)", ln)
        if len(parts) > 1:
            out += parts
    return out


def _parse_sentences(lines, out, gap):
    text = "\n".join(lines)
    if gap:
        for m in re.finditer(re.escape(gap), text):
            out["markers"].append(m.start())
    heads = []
    for rg in HEAD6_RE + HEAD_RE:
        for m in rg.finditer(text):
            heads.append((m.start(), m.end(), m))
    log_heads = []
    if not heads:
        for m in LOGHEAD_RE.finditer(text):
            log_heads.append((m.start(), m.end(), m))
    hs = sorted(heads or log_heads, key=lambda x: x[0])
    seen = set()
    for i, (a, b, m) in enumerate(hs):
        if a in seen:
            continue
        seen.add(a)
        end = hs[i + 1][0] if i + 1 < len(hs) else len(text)
        seg = text[b:end]
        cut = len(seg)
        for mk in out["markers"]:
            if b <= mk < end:
                cut = min(cut, mk - b)
        seg = seg[:cut]
        seg = seg.split("\n")[0].strip() if "\n" in seg else seg.strip()
        gd = m.groupdict()
        n = int(gd["n"])
        if "rd" in gd and gd.get("rd"):
            date, time, eff = gd["rd"], None, gd.get("ed")
            out["sampler"] = "S6"
        elif "dt" in gd:
            dm = DT_RE.fullmatch(gd["dt"])
            date, time, eff = dm.group("date"), dm.group("time"), None
        else:
            line_start = text.rfind("\n", 0, a) + 1
            dm = DT_RE.search(text[line_start:a])
            if not dm:
                raise ParseError("log line without a date")
            date, time, eff = dm.group("date"), dm.group("time"), None
        key, g, note = parse_body(seg)
        if note:
            out["notes"] += 1
        e = body_to_entry(key, g, n, date, time)
        if eff:
            e["eff"] = eff
        e["_pos"] = a
        out["entries"].append(e)
    # explicit gap markers: after the entry that precedes each marker
    out["marker_after"] = []
    for mk in out["markers"]:
        prev = [e for e in out["entries"] if e["_pos"] < mk]
        if prev:
            out["marker_after"].append(max(prev, key=lambda e: e["_pos"])["n"])


def _parse_records(recs, out):
    for r in recs:
        kk = {_key(k): v for k, v in r.items()}
        if "action" in kk:
            continue
        if "holder" in kk and len(kk) >= 3:
            ks = list(r.keys())
            vals = list(r.values())
            item = vals[0]
            holder = kk["holder"]
            rest = [(k, v) for k, v in r.items() if _key(k) not in (_key(ks[0]), "holder")]
            status, qty = None, None
            for k, v in rest:
                if isinstance(v, int) or re.fullmatch(r"\d+", str(v)):
                    qty = int(v)
                else:
                    status = str(v)
            out["items"].append([str(item), str(holder), status, qty])
        elif "document" in kk:
            out["docs"].append([str(kk["document"]), str(kk.get("currentrecord"))])
            out.setdefault("doctype", {})[str(kk["document"])] = None
    rows = [r for r in recs if any(_key(k) == "action" for k in r)]
    # identify the status and quantity columns: the two non-fixed columns (quantity = all integers)
    other = {}
    for r in rows:
        for k, v in r.items():
            if _key(k) not in FIXED:
                other.setdefault(k, []).append(v)
    qcol = [k for k, vs in other.items() if all(isinstance(v, int) or re.fullmatch(r"\d+", str(v)) for v in vs)]
    scol = [k for k in other if k not in qcol]
    if len(qcol) > 1 or len(scol) > 1:
        # a status column whose few values happen to look numeric cannot occur (statuses carry no digits)
        raise ParseError("cannot identify status / quantity columns")
    for r in rows:
        kk = {FIXED.get(_key(k), k): v for k, v in r.items()}
        act = str(kk["action"])
        n = int(kk["entry"])
        if "recorded" in kk:
            date, time, eff = str(kk["recorded"]), None, (str(kk["effective"]) if "effective" in kk else None)
            out["sampler"] = "S6"
        else:
            date, time, eff = str(kk["date"]), (str(kk["time"]) if "time" in kk else None), None
        st = kk.get(scol[0]) if scol else None
        q = kk.get(qcol[0]) if qcol else None
        q = int(q) if q is not None else None
        subj, frm, to, ref = kk.get("subject"), kk.get("from"), kk.get("to"), kk.get("refers")
        if kk.get("note"):
            out["notes"] += 1
        e = {"n": n, "date": date, "time": time}
        if eff:
            e["eff"] = eff
        A_ = R.ACTIONS
        if act == A_["CREATE"]:
            e.update(t="CREATE", item=subj, holder=to, status=st, qty=q)
        elif act == A_["SET"]:
            if st is not None:
                e.update(t="SET", item=subj, field="status", value=st)
            else:
                e.update(t="SET", item=subj, field="qty", value=q)
        elif act in (A_["ADJUST_up"], A_["ADJUST_down"]):
            e.update(t="ADJUST", item=subj, sign=1 if act == A_["ADJUST_up"] else -1, amount=q)
        elif act == A_["TRANSFER"]:
            e.update(t="TRANSFER", item=subj, sender=frm, receiver=to)
        elif act == A_["VOID"]:
            e.update(t="VOID", target=int(ref))
        elif act in (A_["CORR"], A_["CORR_up"], A_["CORR_down"]):
            if act != A_["CORR"]:
                e.update(t="CORR", target=int(ref), slot="amount", value=q,
                         _dir="up" if act == A_["CORR_up"] else "down")
            elif to is not None:
                e.update(t="CORR", target=int(ref), slot="receiver", value=to)
            elif st is not None:
                e.update(t="CORR", target=int(ref), slot="_status", value=st)
            else:
                e.update(t="CORR", target=int(ref), slot="_qty", value=q)
        elif act == A_["SUPERSEDE"]:
            e.update(t="SUPERSEDE", old=subj, new=to)
        elif act == A_["OPEN"]:
            e.update(t="OPEN", record=subj, doc=to)
        elif act == A_["RENAME"]:
            e.update(t="RENAME", kind=None, old=subj, new=to)
        elif act == A_["MERGE"]:
            e.update(t="MERGE", absorbed=subj, survivor=to)
        else:
            raise ParseError("unknown action word")
        out["entries"].append(e)
    out["entries"].sort(key=lambda e: e["n"])
    out["marker_after"] = []


NOTICE_HEAD_RE = re.compile(r"(?:Notice (?P<r1>\d+), dated (?P<d1>" + ANYDATE + r")\.|Reference (?P<r2>\d+), (?P<d2>"
                            + ANYDATE + r")\.)")
CHANGE_RE = re.compile(r"(?<![\d/:])(?P<ref>\d+)\.(?P<k>\d+) (?=\S)")


def _parse_notices(text, out, gap):
    out["sampler"] = "S4"
    heads = list(NOTICE_HEAD_RE.finditer(text))
    n = 0
    for i, h in enumerate(heads):
        ref = int(h.group("r1") or h.group("r2"))
        date = h.group("d1") or h.group("d2")
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        seg = text[h.end():end]
        seg = re.split(r"\bP\.S\. \(note: ", seg)[0]
        if "P.S." in text[h.end():end]:
            out["notes"] += 1
        chs = [m for m in CHANGE_RE.finditer(seg) if int(m.group("ref")) == ref]
        out["notices"][ref] = date
        for j, m in enumerate(chs):
            b = m.end()
            e_ = chs[j + 1].start() if j + 1 < len(chs) else len(seg)
            body = seg[b:e_].strip()
            body = body.split("\n")[0].strip()
            if gap and gap in body:
                body = body.split(gap)[0].strip()
            key, g, note = parse_body(body, s4=True)
            n += 1
            e = body_to_entry(key, g, n, date, None, ref=ref, k=int(m.group("k")))
            out["entries"].append(e)
    out["marker_after"] = []
    if gap:
        for m in re.finditer(re.escape(gap), text):
            prev = [h for h in heads if h.start() < m.start()]
            if prev:
                out["marker_after"].append(int(prev[-1].group("r1") or prev[-1].group("r2")))


GIT_HEAD_RE = re.compile(r"(?P<h>[0-9a-f]{12})(?: (?P<dt>" + ANYDATE + f"(?: {TIME})?))? seq (?P<n>\\d+): ")


def _parse_git(lines, out):
    out["sampler"] = "S5"
    hashes = {}
    text = "\n".join(lines)
    heads = list(GIT_HEAD_RE.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end].split("\n")[0].strip()
        dt = m.group("dt")
        if dt is None:
            ls = text.rfind("\n", 0, m.start()) + 1
            dm = DT_RE.search(text[ls:m.start()])
            if not dm:
                raise ParseError("git line without a date")
            dt = dm.group(0)
        dm = DT_RE.fullmatch(dt)
        n = int(m.group("n"))
        hashes[m.group("h")] = n
        for key, rg in GIT_RE:
            mm = rg.match(body)
            if mm:
                g = mm.groupdict()
                e = {"n": n, "date": dm.group("date"), "time": dm.group("time")}
                if key == "CREATE":
                    q = re.search(r"(\d+)$", g.get("qtail") or "")
                    e.update(t="CREATE", item=g["item"], holder=g["holder"], status=g["s"],
                             qty=int(q.group(1)) if q else None)
                elif key == "SET_status":
                    e.update(t="SET", item=g["item"], field="status", value=g["s"])
                elif key == "SET_qty":
                    e.update(t="SET", item=g["item"], field="qty", value=int(g["q"]))
                elif key.startswith("ADJUST"):
                    e.update(t="ADJUST", item=g["item"], sign=1 if key.endswith("up") else -1, amount=int(g["a"]))
                elif key == "TRANSFER":
                    e.update(t="TRANSFER", item=g["item"], sender=g["sender"], receiver=g["receiver"])
                elif key == "VOID":
                    e.update(t="VOID", target=("hash", g["th"]))
                elif key.startswith("CORR"):
                    slot = {"CORR_value_s": "value", "CORR_value_q": "value", "CORR_amount": "amount",
                            "CORR_receiver": "receiver", "CORR_status": "status", "CORR_qty": "qty"}[key]
                    val = g.get("s") if key in ("CORR_value_s", "CORR_status") else (
                        g.get("receiver") if key == "CORR_receiver" else int(g.get("q") or g.get("a")))
                    e.update(t="CORR", target=("hash", g["th"]), slot=slot, value=val)
                elif key == "SUPERSEDE":
                    e.update(t="SUPERSEDE", old=g["old"], new=g["new"])
                elif key == "OPEN":
                    e.update(t="OPEN", record=g["rec"], doc=g["doc"])
                elif key == "RENAME":
                    e.update(t="RENAME", kind=None, old=g["old"], new=g["new"])
                elif key == "MERGE":
                    e.update(t="MERGE", absorbed=g["old"], survivor=g["new"])
                out["entries"].append(e)
                break
        else:
            raise ParseError("git line matches no registered phrasing")
    for e in out["entries"]:
        if isinstance(e.get("target"), tuple) and e["target"][0] == "hash":
            if e["target"][1] not in hashes:
                raise ParseError("revert / fixup names an unknown line hash")
            e["target"] = hashes[e["target"][1]]
    out["entries"].sort(key=lambda e: e["n"])
    out["marker_after"] = []


# ------------------------------------------------------------------------------------------------ question stems

KINDW = r"(?:(?!that |case |not )[A-Za-z][A-Za-z'-]* ){0,4}"
Q_SLOTS = {"field": WORDS, "qty": WORDS, "unit": WORDS, "items": WORDS, "hnoun": WORDS, "doctype": WORDS,
           "Y": f"{KINDW}{ID}", "X": f"{KINDW}{ID}", "S": "[^']+",
           "CMP": "at least|at most|more than|fewer than|no fewer than|no more than", "N": r"\d+",
           "END": "at the end|now|currently", "DP": "on|as of|at the end of|at the start of", "D": ANYDATE,
           "D1": ANYDATE, "D2": ANYDATE, "R": ID, "DOC": DOC, "ENT": r"entry \d+|change \d+\.\d+"}


def _stem_patterns():
    pats = []
    for key, st in R.STEM.items():
        for nm in ("QA", "N3"):
            if nm in st:
                pats.append((key, nm, None, tregex(st[nm], Q_SLOTS, anchor=True)))
        for i, t in enumerate(st.get("QC", [])):
            pats.append((key, "QC", i, tregex(t, Q_SLOTS, anchor=True)))
        for cn in ("C", "Cn", "C2", "C3"):
            if cn in st:
                for fr in ("A", "N1", "N2", "N4", "N5", "D"):
                    tmpl = R.FRAME[fr]
                    inner = {"A": "C", "N1": "Cn", "N2": "C2", "N4": "C", "N5": "C", "D": "Cx"}[fr]
                    if fr == "D" and cn not in ("Cn", "C2", "C3"):
                        continue
                    if fr != "D" and inner != cn:
                        continue
                    full = tmpl.replace("{" + inner + "}", st[cn])
                    pats.append((key, fr, cn, tregex(full, Q_SLOTS, anchor=True)))
    return pats


_FRAME_ORDER = {"D": 0, "N4": 1, "N5": 2, "N2": 3, "N3": 4, "N1": 5, "A": 6, "QA": 7, "QC": 8}
STEM_PATS = sorted(_stem_patterns(), key=lambda p: _FRAME_ORDER[p[1]])
_ID_ONLY = re.compile(ID + "$")


def _strip_kind(v):
    if v is None:
        return None
    m = re.search("(" + ID + ")$", v)
    return m.group(1) if m else v


def parse_question(instr):
    """The last sentence of the instructions that matches a registered stem -> (stem text, parsed dict)."""
    cands = re.findall(r"[^\n?]*\?", instr)
    for raw in reversed(cands):
        s = raw.strip()
        s = re.sub(r"^(?:Question:|Q:|The question to answer:)\s*", "", s)
        # the question may follow the wording in the same paragraph (IP2): try every sentence start
        starts = [0] + [m.end() for m in re.finditer(r"[.!:;] ", s)]
        for st in starts:
            frag = s[st:].strip()
            for key, nm, cn, rg in STEM_PATS:
                m = rg.match(frag)
                if m:
                    return frag, {"key": key, "form": nm, "claim": cn, "slots": m.groupdict()}
    raise ParseError("no registered question stem in the instructions")


# ------------------------------------------------------------------------------------------------ row parsing

def card_texts(row):
    """The card text the parser reads (section 1 layout): the card field on yes/no rows; option-definition lines
    plus the instructions on choice rows."""
    if row["qtype"] == "noul":
        return row.get("card") or "", {}
    defs = {}
    for ln in (row.get("card") or "").split("\n"):
        if ln.startswith("- ") and ": " in ln:
            k, v = ln[2:].split(": ", 1)
            defs[k] = v
    return row.get("instructions") or "", defs


def parse_row(row):
    style = _STYLES[row["meta"]["format_style"]]
    ctext, defs = card_texts(row)
    stm = find_statements(ctext)
    stem, qp = parse_question(row["instructions"])
    st = parse_state(row["state"], style, stm)
    S, Q, tg, info = assemble(row, st, stm, defs, qp)
    return {"S": S, "Q": Q, "toggles": tg, "stem": stem, "statements": stm, "defs": defs, "info": info,
            "state": st, "card_text": ctext}


def assemble(row, st, stm, defs, qp):
    # dates
    dateorder = (stm.get("T26") or {}).get("dateorder")
    raw_dates = [e["date"] for e in st["entries"]] + [e["eff"] for e in st["entries"] if e.get("eff")]
    sl = qp["slots"]
    raw_dates += [sl[k] for k in ("D", "D1", "D2") if sl.get(k)]
    if st.get("d0_raw"):
        raw_dates.append(st["d0_raw"])
    fmt = detect_date_format(raw_dates, dateorder)
    conv = lambda d: parse_date(d, fmt) if d else d  # noqa: E731
    sampler = st["sampler"] or "S1"
    ents = []
    for e in st["entries"]:
        e = dict(e)
        e.pop("_pos", None)
        e["date"] = conv(e["date"])
        if e.get("eff"):
            e["eff"] = conv(e["eff"])
        ents.append(e)
    # S4: change numbering -> internal n in (ref, k) order; amend targets by (ref, k)
    if sampler == "S4":
        ents.sort(key=lambda e: (e["ref"], e["k"]))
        for i, e in enumerate(ents, start=1):
            e["n"] = i
        byrk = {(e["ref"], e["k"]): e["n"] for e in ents}
        for e in ents:
            if e["t"] == "CORR" and isinstance(e["target"], tuple):
                e["target"] = byrk[(e["target"][1], e["target"][2])]
    by_n = {e["n"]: e for e in ents}
    items = {it[0] for it in st["items"]} | {e["item"] for e in ents if e.get("item")}
    for e in ents:
        if e["t"] == "RENAME":
            e["kind"] = "item" if (e["old"] in items or e["new"] in items) else "holder"
            if e["kind"] == "item":
                items.add(e["new"])
        if e["t"] == "CORR":
            tgt = by_n.get(e["target"])
            if tgt is None:
                raise ParseError("a correction names an entry that is not shown")
            if e["slot"] in ("_status", "_qty"):
                e["slot"] = ("status" if e["slot"] == "_status" else "qty") if tgt["t"] == "CREATE" else "value"
            elif e["slot"] in ("value", "status", "qty", "amount"):
                # phrasing overlaps ('the <field> should read', 'starting <field>', 'increase of'): the target's
                # entry type decides the slot (A11: one correctable value per slot)
                if tgt["t"] == "CREATE":
                    e["slot"] = "status" if isinstance(e["value"], str) else "qty"
                elif tgt["t"] == "ADJUST":
                    e["slot"] = "amount"
                else:
                    e["slot"] = "value"
            if e.get("_dir") and tgt["t"] == "ADJUST" and (e["_dir"] == "up") != (tgt["sign"] > 0):
                raise ParseError("a correction restates the wrong direction")
            e.pop("_dir", None)
        if e["t"] == "OPEN":
            e.pop("_doctype", None)
    # world, gaps, toggles
    world = "open" if ({"T2", "T2c"} & set(stm)) else "closed"
    gs = None
    for t, v in (("T3x", "explicit"), ("T3x4", "explicit"), ("T3s", "skipped"), ("T3s4", "skipped"),
                 ("T3l", "leading"), ("T3l4", "leading")):
        if t in stm:
            gs = v
    S = {"sampler": sampler, "world": world, "gap_style": gs, "n0": None,
         "toggles": {"rename_mode": "alias" if "T14a" in stm else ("retire" if "T14r" in stm else None),
                     "check": "T18" in stm or "T40" in stm, "lock": "T19" in stm or "T40" in stm,
                     "lock_status": (stm.get("T19") or stm.get("T40") or {}).get("S"),
                     "timed": any(e.get("time") for e in ents)},
         "has_qty": any(it[3] is not None for it in st["items"]) or any(
             e["t"] in ("ADJUST",) or (e["t"] == "SET" and e["field"] == "qty") or e.get("qty") is not None
             for e in ents) or "T28" in stm,
         "statuses": re.findall(r"'([^']+)'", (stm.get("T36") or {}).get("values", "")),
         "default_status": (stm.get("T9c") or stm.get("T9cq") or stm.get("T42") or stm.get("T42k") or {}).get(
             "default"),
         "register": {"items": [list(x) for x in st["items"]], "docs": [list(x) for x in st["docs"]]},
         "entries": ents, "gaps": [], "d0": conv(st.get("d0_raw")) if st.get("d0_raw") else None}
    if world == "open":
        if sampler == "S4":
            refs = sorted({e["ref"] for e in ents})
            if gs == "leading":
                S["n0"] = refs[0]
            else:
                miss = [r for r in range(refs[0], refs[-1] + 1) if r not in refs]
                S["gap_refs"] = miss
                S["gaps"] = sorted({max(e["n"] for e in ents if e["ref"] < r) for r in miss})
        else:
            ns = [e["n"] for e in ents]
            if gs == "leading":
                S["n0"] = ns[0]
                if str(ns[0]) != (stm.get("T3l") or {}).get("N0"):
                    raise ParseError("leading extract start differs from the card's N0")
            else:
                S["gaps"] = sorted({ns[i] for i in range(len(ns) - 1) if ns[i + 1] > ns[i] + 1})
                if gs == "explicit" and sorted(set(st.get("marker_after", []))) != S["gaps"]:
                    raise ParseError("explicit gap markers do not sit at the skipped numbers")
    # query
    Q = build_query(qp, S, row, stm, conv, by_n)
    vocab = "masked" if ("T36m" in stm or (defs and any(re.search(r"\d", k) for k in defs))) else (
        "swapped" if ("T36s" in stm or defs) else "plain")
    stated = sorted(set(stm) | ({"T36m"} if vocab == "masked" else set()) | ({"T36s"} if vocab == "swapped" else set()))
    slots = {"S": S["toggles"]["lock_status"], "key": (stm.get("T42") or stm.get("T42k") or {}).get("key"),
             "listing": (stm.get("T43") or {}).get("listing")}
    tg = canon.toggles_from(stated, slots, date_fmt=fmt, timed=S["toggles"]["timed"], vocab=vocab)
    return S, Q, tg, {"date_fmt": fmt, "vocab": vocab}


def build_query(qp, S, row, stm, conv, by_n):
    key, form, cn, sl = qp["key"], qp["form"], qp["claim"], qp["slots"]
    kind, ptk = key
    Q = {"form": "choice" if form == "QC" else "yn"}
    if form != "QC":
        if form in ("QA", "A"):
            Q["neg"] = "A"
        elif form == "N3":
            Q["neg"] = "N3"
        elif form == "D":
            Q["neg"] = "D"
            Q["dbase"] = {"Cn": "N1", "C2": "N2", "C3": "N3"}[cn]
        else:
            Q["neg"] = form
    if sl.get("Y"):
        Q["item"] = _strip_kind(sl["Y"])
    if sl.get("X"):
        Q["holder"] = _strip_kind(sl["X"])
    if kind in ("status", "qty", "holder") and ptk in ("end", "still"):
        Q["point"] = {"kind": "end"}
    elif ptk == "date":
        Q["point"] = {"kind": sl.get("DP") or "on", "date": conv(sl["D"])}
    elif ptk == "range":
        Q["point"] = {"kind": "range", "d1": conv(sl["D1"]), "d2": conv(sl["D2"])}
    if kind == "status":
        Q.update(qt="Q1" if ptk == "end" else "Q2", kind="status")
        if Q["form"] == "yn":
            Q["value"] = sl["S"]
    elif kind == "qty":
        Q.update(qt="Q1" if ptk == "end" else "Q2", kind="qty", cmp=sl["CMP"], n=int(sl["N"]))
    elif kind == "record":
        Q.update(qt="Q3", kind="record", doc=sl["DOC"])
        if Q["form"] == "yn":
            Q["record"] = sl["R"]
    elif kind == "holder":
        if Q["form"] == "choice":
            Q.update(qt="Q5", kind="holder")
        else:
            Q.update(qt="Q4", kind="holder")
            if ptk == "still":
                if form in ("QA", "A", "N5"):
                    Q["still"] = True
                Q["point"] = {"kind": "end"}
    elif kind == "count":
        Q.update(qt="Q6", kind="count", cmp=sl["CMP"], n=int(sl["N"]))
    elif kind == "inverse":
        none = (stm.get("T34o") or {}).get("None")
        if not none:
            raise ParseError("a Q7 row whose card states no None option")
        Q.update(qt="Q7", kind="inverse", none_option=none,
                 candidates=[o for o in row["options"] if o != none])
    elif kind == "transfer":
        Q.update(qt="Q8", kind="transfer")
        ent = sl["ENT"]
        if ent.startswith("change"):
            r, k = ent.split()[1].split(".")
            hit = [e["n"] for e in S["entries"] if e.get("ref") == int(r) and e.get("k") == int(k)]
            if not hit:
                raise ParseError("Q8 names a change that is not shown")
            Q["entry"] = hit[0]
        else:
            Q["entry"] = int(ent.split()[1])
    return Q


# ------------------------------------------------------------------------------------------------ G3 checks

_NEG_EXPECT = {"A": (0, 0), "N1": (1, 1), "N2": (1, 1), "N3": (0, 1), "N4": (1, 1), "N5": (0, 1)}


def check_row(row, card, expect):
    """G3 checks 1-8 on one rendered row against the generator's record. {"ok", "why"}."""
    try:
        P = parse_row(row)
    except (ParseError, json.JSONDecodeError, yaml.YAMLError, KeyError, ValueError, IndexError) as ex:
        return {"ok": False, "why": "parse:" + str(ex)[:80]}
    S, Q = P["S"], P["Q"]
    ex_S, ex_Q = expect["S"], expect["Q"]
    # check 1: structure hash
    h = canon.structure_hash(S, P["toggles"], Q)
    if h != expect["hash"]:
        why = _hash_diff(S, P["toggles"], Q, ex_S, expect["toggles"], ex_Q)
        return {"ok": False, "why": "hash:" + why}
    # check 2: solver B on the parse gives the row's label
    try:
        lb, info = SB.solve(S, Q)
    except AssertionError as ex:
        return {"ok": False, "why": "solverB_assert"}
    gold = row["gold"]
    if S["world"] == "open" and lb == SB.UNKNOWN:
        lb = (P["statements"].get("T34n") or {}).get("NEI")
    elif row["qtype"] == "choice" and Q["qt"] == "Q5":
        lb = SA.latest_id(S, None, lb)
    if lb != gold:
        return {"ok": False, "why": "solverB_on_parse"}
    # check 3: every ID in the log, query and options exists in the structure
    ids = _struct_ids(S)
    for k in ("item", "holder", "record"):
        if Q.get(k) and Q[k] not in ids:
            return {"ok": False, "why": "id_not_in_structure"}
    if row["qtype"] == "choice":
        none = (P["statements"].get("T34o") or {}).get("None")
        nei = (P["statements"].get("T34n") or {}).get("NEI")
        for o in row["options"]:
            if re.fullmatch(ID, o) and o not in ids:
                return {"ok": False, "why": "option_id_not_in_structure"}
    # check 4: toggles
    if P["toggles"] != expect["toggles"]:
        return {"ok": False, "why": "toggles"}
    # check 5: negation count and stem form
    nc = negcount.count(P["stem"])
    if (nc.k_syn, nc.k_all) != expect["neg"]:
        return {"ok": False, "why": "negcount"}
    if Q["form"] == "yn" and Q.get("neg", "A") != "A" and "T44" not in P["statements"]:
        return {"ok": False, "why": "negated_row_without_T44"}
    for w in ("answer", "answers", "answered", "option", "options", "choice", "choices", "correct", "correctly",
              "incorrect", "incorrectly"):
        if Q["form"] == "yn" and re.search(r"\b" + w + r"\b", P["stem"], re.I):
            return {"ok": False, "why": "banned_word_in_stem"}
    # check 6: option set
    if row["qtype"] == "choice" and sorted(row["options"]) != sorted(expect["options"]):
        return {"ok": False, "why": "options"}
    # check 7: illustrations and worked examples
    bad = check_blocks(P, row)
    if bad:
        return {"ok": False, "why": "block:" + bad}
    return {"ok": True, "why": "ok", "hash": h}


def _struct_ids(S):
    ids = set()
    for it in S["register"]["items"]:
        ids.add(it[0]); ids.add(it[1])
    for d, r in S["register"].get("docs", []):
        ids.add(r)
    for e in S["entries"]:
        for k in ("item", "holder", "sender", "receiver", "old", "new", "absorbed", "survivor", "record"):
            if isinstance(e.get(k), str):
                ids.add(e[k])
        if e["t"] == "CORR" and e["slot"] == "receiver":
            ids.add(e["value"])
    return ids


def _hash_diff(S, tg, Q, eS, etg, eQ):
    a = canon.canonical(S, tg, Q)
    b = canon.canonical(eS, etg, eQ)
    for part in ("toggles", "query"):
        if a[part] != b[part]:
            ks = [k for k in set(a[part]) | set(b[part]) if a[part].get(k) != b[part].get(k)]
            return part + ":" + ",".join(sorted(ks))[:40]
    fa, fb = a["facts"], b["facts"]
    ks = [k for k in fa if fa.get(k) != fb.get(k)]
    if "entries" in ks and len(fa["entries"]) == len(fb["entries"]):
        for x, y in zip(fa["entries"], fb["entries"]):
            if x != y:
                d = [k for k in set(x) | set(y) if x.get(k) != y.get(k)]
                return "entry:" + x["t"] + ":" + ",".join(sorted(d))
    return "facts:" + ",".join(ks)


ILLUS_RE = re.compile(r"(?:Illustration|For instance): (?P<log>.+?) (?:Result|So): (?P<claim>[^\n]+?)\.(?=\s|$)")
FEW_Q_RE = re.compile(r"Question: (?P<q>[^\n?]+\?)")
ANS_RE = re.compile(r"(?:Answer|A|Output|Outcome|Answer key|Its answer):\s*(?P<a>Yes|No)\b")


def _mini_parse(text, toggles):
    ents = []
    heads = list(LOGHEAD_RE.finditer(text))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[h.end():end].strip()
        key, g, note = parse_body(body)
        n = int(h.group("n"))
        ents.append(body_to_entry(key, g, n, "2030-01-%02d" % (n + 1), None))
    docs = [[m.group("doc"), m.group("rec")] for rg in REGDOC_RE for m in [rg.search(text)] if m] \
        if False else []
    m = re.search(r"document (" + DOC + r"): current record (" + ID + r")\.", text)
    if m:
        docs = [[m.group(1), m.group(2)]]
    items = {e["item"] for e in ents if e.get("item")}
    for e in ents:
        if e["t"] == "RENAME":
            e["kind"] = "item" if e["old"] in items else "holder"
    S = {"sampler": "S1", "world": "closed", "gap_style": None, "n0": None, "toggles": toggles, "has_qty": False,
         "statuses": [], "default_status": None, "register": {"items": [], "docs": docs}, "entries": ents,
         "gaps": []}
    return S


FEW_RE = re.compile(r"(?P<log>entry 1: [^\n]+?)\nQuestion: (?P<q>[^\n?]+\?)\n(?:Answer|A|Output|Outcome|Answer key|"
                    r"Its answer): (?P<a>Yes|No)\b")


def check_blocks(P, row):
    raw = P["card_text"] if row["qtype"] == "noul" else row["instructions"]
    raw = "\n".join(re.sub(r"^(?:>\s?|\s+)+", "", ln) for ln in raw.split("\n"))
    text = _norm(raw)
    tg = P["S"]["toggles"]
    mtg = {"rename_mode": tg["rename_mode"], "check": tg["check"], "lock": tg["lock"],
           "lock_status": tg["lock_status"], "timed": False}
    row_ids = _struct_ids(P["S"])
    for m in ILLUS_RE.finditer(text):
        try:
            S = _mini_parse(m.group("log"), mtg)
            _, qp = _claim_query(m.group("claim"))
            Q = build_query(qp, S, {"options": []}, P["statements"], lambda d: d, {})
        except (ParseError, KeyError) as ex:
            return "illustration_parse"
        if SA.answer(S, Q) not in (1,):
            return "illustration_outcome"
        if _struct_ids(S) & row_ids:
            return "illustration_ids_in_row"
    for m in FEW_RE.finditer(raw):
        try:
            S = _mini_parse(m.group("log"), mtg)
            _, qp = parse_question(m.group("q"))
            Q = build_query(qp, S, {"options": []}, P["statements"], lambda d: d, {})
        except (ParseError, KeyError):
            return "fewshot_parse"
        if SA.answer(S, Q) != (1 if m.group("a") == "Yes" else 0):
            return "fewshot_outcome"
        if _struct_ids(S) & row_ids:
            return "fewshot_ids_in_row"
    return None


def _claim_query(claim):
    for key, nm, cn, rg in STEM_PATS:
        if nm in ("A",) and cn == "C":
            pass
    pats = []
    for key, st in R.STEM.items():
        for cn in ("C", "Cn"):
            if cn in st:
                pats.append((key, cn, tregex(st[cn], Q_SLOTS, anchor=True)))
    for key, cn, rg in pats:
        m = rg.match(claim)
        if m:
            return claim, {"key": key, "form": "A" if cn == "C" else "N1", "claim": cn, "slots": m.groupdict()}
    raise ParseError("illustration result is no registered claim")
