#!/usr/bin/env python3
"""F3 solver B (independent re-derivation of gold), written from the frozen G0 spec (F3.G0.v7, sections 1-3, 2.2,
T1-T44, solver B paragraph of section 3) and the spec 2.4 row format only. It never imports or reads the F3
generator (c_src/F3/gen/) or solver A.

Paradigm: parse the rendered row text (state / card / instructions / options) back into facts, then answer with a
lazy, memoized BACKWARD resolver over a pointer graph (void edges, per-value correction edges, rename closure, timed
merge edges, supersede edges, gap nodes): each query walks from the query point backwards in effect order to the last
valid writer, recursing for transfer checks / lock rule / merges. Open-world rows use the T2 knowability table
(exact setter after every missing entry) instead of replay.

Usage: python solver_b.py [--files a.jsonl,b.jsonl] [--out mismatch.json]
Output: mismatch.json with ids + gold + solver-B answer + spec item (never row text).
"""
from __future__ import annotations

import html as _html
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
STYLES = os.path.join(LEAN, "c_src", "formats", "formats-1", "data", "styles.jsonl")


class ParseError(Exception):
    pass


# ----------------------------------------------------------------------------------------------------------------
# 1. Tokens: IDs, hashes, dates, times
# ----------------------------------------------------------------------------------------------------------------
ID_PAT = r"[A-Z]{2,3}-(?=[A-Z]*[0-9])[A-Z0-9]{2,4}"
ID_RE = re.compile(r"(?<![A-Za-z0-9\-])" + ID_PAT + r"(?![A-Za-z0-9\-])")
HASH_RE = re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{12}(?![0-9a-zA-Z])")
ANYID = r"(?:" + ID_PAT + r"|[0-9a-f]{12})"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
     "december"])}
MON_ABBR = {k[:3]: v for k, v in MONTHS.items()}
MON_ABBR["sept"] = 9
MON_RX = r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?"
DATE_RX = (r"(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2} " + MON_RX + r" \d{4}|" + MON_RX + r" \d{1,2}, \d{4})")
DATE_RE = re.compile(r"(?<![\d/\-])" + DATE_RX + r"(?![\d/\-])", re.I)
TIME_RX = r"(?:[01]\d|2[0-3]):[0-5]\d"


def _mon(s):
    s = s.lower().rstrip(".")
    if s in MONTHS:
        return MONTHS[s]
    return MON_ABBR[s[:4] if s.startswith("sept") else s[:3]]


def _ord(y, m, d):
    import datetime
    return datetime.date(y, m, d).toordinal()


def parse_date(s: str, dmy: str | None):
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return _ord(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        a, b, y = int(m[1]), int(m[2]), int(m[3])
        if dmy == "dmy":
            return _ord(y, b, a)
        if dmy == "mdy":
            return _ord(y, a, b)
        raise ParseError("numeric date with unknown order")
    m = re.fullmatch(r"(\d{1,2}) (" + MON_RX + r") (\d{4})", s, re.I)
    if m:
        return _ord(int(m[3]), _mon(m[2]), int(m[1]))
    m = re.fullmatch(r"(" + MON_RX + r") (\d{1,2}), (\d{4})", s, re.I)
    if m:
        return _ord(int(m[3]), _mon(m[1]), int(m[2]))
    raise ParseError("bad date " + s)


def parse_time(s):
    if s is None:
        return None
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*", str(s))
    if not m:
        raise ParseError("bad time")
    return int(m[1]) * 60 + int(m[2])


# ----------------------------------------------------------------------------------------------------------------
# 2. Container decoding: state text -> units (dict records or text lines), each with a section label
# ----------------------------------------------------------------------------------------------------------------
_styles = None


def style_container(fs):
    global _styles
    if _styles is None:
        _styles = {}
        for ln in open(STYLES):
            s = json.loads(ln)
            _styles[s["id"]] = s
    s = _styles.get(fs)
    return (s or {}).get("container"), (s or {}).get("skin")


def norm_key(k: str) -> str:
    k = str(k)
    k = re.sub(r"([a-z])([A-Z])", r"\1 \2", k)  # camelCase
    k = k.replace("_", " ").replace("-", " ")
    k = re.sub(r"\s+", " ", k).strip().lower()
    return k


def _strip_fences(t: str) -> str:
    return "\n".join(ln for ln in t.split("\n") if not re.match(r"^\s*(```|~~~)", ln))


def _walk(obj, section, out):
    """Walk a parsed JSON / YAML document; dicts that carry IDs or an entry number become records."""
    if isinstance(obj, dict):
        flat = {}
        nested = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                nested.append((k, v))
            else:
                flat[k] = v
        if flat and not nested:
            out.append((section, {norm_key(k): ("" if v is None else str(v)) for k, v in flat.items()}))
            return
        for k, v in flat.items():
            sv = "" if v is None else str(v)
            out.append((norm_key(k), sv))
        for k, v in nested:
            _walk(v, norm_key(k), out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, section, out)
    else:
        out.append((section, "" if obj is None else str(obj)))


def _yaml_load(t):
    import yaml
    return yaml.load(t, Loader=yaml.BaseLoader)


def decode_structured(text: str):
    t = _strip_fences(text)
    # JSON first
    i = min([p for p in (t.find("{"), t.find("[")) if p >= 0], default=-1)
    if i >= 0:
        try:
            obj = json.loads(t[i:])
            out = []
            _walk(obj, "", out)
            return out
        except Exception:
            pass
        # JSON lines
        try:
            objs = [json.loads(ln) for ln in t.split("\n") if ln.strip().startswith("{")]
            if objs:
                out = []
                for o in objs:
                    _walk(o, "", out)
                return out
        except Exception:
            pass
    import textwrap
    t2 = textwrap.dedent(t)
    try:
        obj = _yaml_load(t2)
        if isinstance(obj, (dict, list)):
            out = []
            _walk(obj, "", out)
            return out
    except Exception:
        pass
    return None


def decode_html(text: str):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(_strip_fences(text), "html.parser")
    out = []
    section = ""
    body = soup
    for el in body.descendants:
        name = getattr(el, "name", None)
        if name in ("h1", "h2", "h3", "h4", "h5", "h6", "caption", "strong", "b", "summary", "legend"):
            if el.find_parent("table") is None or name == "caption":
                section = el.get_text(" ", strip=True)
                out.append((section, "§" + section))
        elif name == "table":
            rows = el.find_all("tr")
            if not rows:
                continue
            hdr = [c.get_text(" ", strip=True) for c in rows[0].find_all(["th", "td"])]
            for r in rows[1:]:
                cells = [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])]
                if len(cells) != len(hdr):
                    raise ParseError("html row width")
                out.append((section, {norm_key(h): v for h, v in zip(hdr, cells)}))
        elif name in ("li", "p", "pre", "dd", "td") and el.find_parent("table") is None:
            if el.find(["li", "p", "table"]) is not None:
                continue
            txt = el.get_text(" ", strip=False)
            for ln in txt.split("\n"):
                if ln.strip():
                    out.append((section, ln.strip()))
        elif name == "dl":
            dts = el.find_all("dt")
            dds = el.find_all("dd")
            if len(dts) == len(dds) and dts:
                out.append((section, {norm_key(a.get_text(" ", strip=True)): b.get_text(" ", strip=True)
                                      for a, b in zip(dts, dds)}))
    return out


KV_LINE = re.compile(r"^\s*(?P<k>[A-Za-z][A-Za-z0-9 _'()\-/]*?)\s*(?:=|::|:|\.{2,})\s*(?P<v>.*?)\s*$")


def _split_pipe(ln):
    s = ln.strip()
    if s.startswith("|"):
        s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
    return [c.strip() for c in s.split("|")]


def decode_lines(text: str, kv_mode: bool):
    """Line containers (prose, memo, sop, log, chat, email, kv, markdown tables, pipe tables in memos)."""
    lines = _strip_fences(text).split("\n")
    out = []
    section = ""
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        s = re.sub(r"^\s*(?:>\s?)+", "", ln).rstrip()  # quoted email lines
        st = s.strip()
        if not st:
            i += 1
            continue
        # pipe table block (>= 2 separators on header and every row)
        if st.count("|") >= 2 and not ID_RE.match(st) or (st.count("|") >= 3):
            hdr = _split_pipe(st)
            if any(norm_key(h) in ("entry", "holder", "subject", "action", "no", "entry no", "recorded", "date")
                   for h in hdr) or any(norm_key(h) == "current record" for h in hdr):
                j = i + 1
                rows = []
                while j < n:
                    s2 = re.sub(r"^\s*(?:>\s?)+", "", lines[j]).strip()
                    if not s2 or s2.count("|") < len(hdr) - 1:
                        break
                    if re.fullmatch(r"[|\-:+= ]+", s2):
                        j += 1
                        continue
                    cells = _split_pipe(s2)
                    if len(cells) != len(hdr):
                        raise ParseError("pipe row width")
                    rows.append({norm_key(h): c for h, c in zip(hdr, cells)})
                    j += 1
                for r in rows:
                    out.append((section, r))
                i = j
                continue
        # grid tables (+----+)
        if re.fullmatch(r"\+[-=+]+\+", st):
            i += 1
            continue
        if kv_mode:
            # block of key/value lines
            j = i
            block = []
            while j < n:
                s2 = re.sub(r"^\s*(?:>\s?)+", "", lines[j]).strip()
                if not s2:
                    break
                m = KV_LINE.match(s2)
                if not m or re.match(r"^\[.*\]$", s2) or s2.startswith("#"):
                    break
                block.append((m["k"], m["v"]))
                j += 1
            if block and (len(block) >= 2):
                out.append((section, {norm_key(k): v for k, v in block}))
                i = j
                continue
            # header line
            hdr = st.strip("[]#=*: ").strip()
            section = hdr
            out.append((section, "§" + hdr))
            i += 1
            continue
        out.append((section, st))
        i += 1
    return out


def decode_state(state: str, container: str):
    if container in ("json", "yaml"):
        r = decode_structured(state)
        if r is not None:
            return r
    if container == "html_snippet" or re.search(r"<(table|p|ul|ol|div|h\d|dl|article|section)\b", state):
        return decode_html(state)
    return decode_lines(state, kv_mode=(container == "key_value"))


# ----------------------------------------------------------------------------------------------------------------
# 3. Card / rule text -> stated toggles (statement registry, read by meaning, never by template id)
# ----------------------------------------------------------------------------------------------------------------
@dataclass
class Rules:
    world: str = "closed"          # closed | open
    gap: str | None = None         # explicit | skipped | leading
    marker: str | None = None
    n0: int | None = None
    nei: str | None = None
    none: str | None = None
    default_status: str | None = None
    default_qty: int | None = None
    rename: str | None = None      # alias | retire
    check: bool = False            # T18 / T40 sender check
    lock: str | None = None        # T19 / T40 locked status
    dmy: str | None = None         # dmy | mdy
    effective: bool = False        # T6
    notices: bool = False          # T41
    gitlike: bool = False          # T43
    status_field: str | None = None
    vocab: list = field(default_factory=list)
    stated: bool = False           # any rule stated at all


def parse_rules(text: str) -> Rules:
    R = Rules()
    t = re.sub(r"\s+", " ", text)
    if re.search(r"log is complete|Nothing is missing from this log", t):
        R.world = "closed"
        R.stated = True
    if re.search(r"Some (?:entries|notices|lines) are missing|This extract starts at|marks one or more missing|"
                 r"skipped (?:entry|reference) number is one missing", t):
        R.world = "open"
        R.stated = True
    m = re.search(r"This extract starts at (?:entry|notice|reference|line) (\d+)", t)
    if m:
        R.gap, R.n0 = "leading", int(m[1])
    elif re.search(r"skipped (?:entry|reference|sequence) number is one missing", t):
        R.gap = "skipped"
    else:
        m = re.search(r"Each '([^']+)' marks one or more missing", t)
        if m:
            R.gap, R.marker = "explicit", m[1]
    m = re.search(r"'([^']+)' is right exactly when the log, read with these rules, allows more than one answer", t)
    if m:
        R.nei = m[1]
    else:
        m = re.search(r"if the answer depends on a missing (?:entry|notice), choose '([^']+)'", t)
        if m:
            R.nei = m[1]
    m = re.search(r"'([^']+)' is right exactly when no listed", t)
    if m:
        R.none = m[1]
    m = re.search(r"any (.+?) it leaves blank starts as '([^']+)'", t)
    if m:
        R.default_status = m[2]
    m = re.search(r"and any .+? it leaves blank starts as (\d+)", t)
    if m:
        R.default_qty = int(m[1])
    if re.search(r"After a rename only the new ID is valid", t):
        R.rename = "retire"
    elif re.search(r"After a rename the old and new IDs name the same", t):
        R.rename = "alias"
    m = re.search(r"A transfer takes effect if and only if, at that moment, the named sender holds the .+? and its "
                  r"(.+?) is not '([^']+)'", t)
    if m:
        R.check, R.lock = True, m[2]
    else:
        if re.search(r"A transfer takes effect if and only if the named sender holds", t):
            R.check = True
        m = re.search(r"A transfer takes effect unless the .+? is '([^']+)' at that moment", t)
        if m:
            R.lock = m[1]
    m = re.search(r"Dates are written (day/month/year|month/day/year)", t)
    if m:
        R.dmy = "dmy" if m[1].startswith("day") else "mdy"
    if re.search(r"take effect on their effective date", t):
        R.effective = True
    if re.search(r"Each notice has a reference number", t):
        R.notices = True
    if re.search(r"Each line has a date and a sequence number", t):
        R.gitlike = True
    m = re.search(r"The (.+?) takes only these values: (.*?)(?:\.(?:\s|$)|$)", t)
    if m:
        R.status_field = norm_key(m[1])
        R.vocab = re.findall(r"'([^']*)'", m[2])
    return R


# ----------------------------------------------------------------------------------------------------------------
# 4. Facts: register + entries
# ----------------------------------------------------------------------------------------------------------------
@dataclass
class Entry:
    kind: str
    n: int
    k: int = 0
    date: int | None = None
    time: int | None = None
    eff: int | None = None
    hash: str | None = None
    item: str | None = None
    holder: str | None = None
    status: str | None = None
    qty: int | None = None
    fld: str | None = None
    delta: int | None = None
    sender: str | None = None
    receiver: str | None = None
    target: object = None
    slot: str | None = None
    value: object = None
    old: str | None = None
    new: str | None = None
    doc: str | None = None
    rec: str | None = None

    @property
    def ref(self):
        return (self.n, self.k)


@dataclass
class Facts:
    reg_items: dict = field(default_factory=dict)   # item -> {holder,status,qty}
    reg_docs: dict = field(default_factory=dict)    # doc -> record
    has_register: bool = False
    entries: list = field(default_factory=list)
    s6_d0: int | None = None


Q_RE = re.compile(r"'([^']*)'")


def _ids(s):
    return ID_RE.findall(s)


def _ints_outside_quotes(s):
    s2 = Q_RE.sub(" ", s)
    s2 = ID_RE.sub(" ", s2)
    s2 = HASH_RE.sub(" ", s2)
    return [int(x) for x in re.findall(r"(?<![\w.])[+-]?\d+(?![\w.])", s2)]


NOTE_RE = re.compile(r"\s*\((?:note|Note|NOTE)\s*:[^()]*\)")


def parse_body(body: str, e: Entry, rules: Rules):
    """One entry body (sentence form) -> fills Entry (kind + slots)."""
    b = NOTE_RE.sub("", body).strip()
    if rules.marker:
        b = b.replace(rules.marker, " ").strip()
    b = re.sub(r"(?:[.;]\s*)?\bP\.S\.\s*$", "", b).strip()
    b = re.sub(r"[.;]\s*$", "", b).strip()
    masked = Q_RE.sub("'Q'", b)
    quoted = Q_RE.findall(b)
    ids = _ids(b)
    if re.search(r"\b(?:is void|void entry)\b", masked) or re.match(r"revert\b", masked):
        m = re.search(r"entry (\d+)", masked)
        if m:
            e.kind, e.target = "VOID", (int(m[1]), 0)
            return
        m = HASH_RE.search(b)
        if m and masked.startswith("revert"):
            e.kind, e.target = "VOID", m[0]
            return
        raise ParseError("void target")
    m = re.search(r"notice (\d+) is withdrawn in full|withdraw notice (\d+)", masked)
    if m:
        e.kind, e.target = "WITHDRAW", int(m[1] or m[2])
        return
    m = (re.match(r"correction to entry (\d+):\s*(.*)$", b) or re.match(r"entry (\d+) corrected:\s*(.*)$", b))
    m2 = re.match(r"amend (\d+)\.(\d+):\s*(.*)$", b)
    m3 = re.match(r"fixup ([0-9a-f]{12}):\s*(.*)$", b)
    if m or m2 or m3:
        e.kind = "CORR"
        if m:
            e.target, rest = (int(m[1]), 0), m[2]
        elif m2:
            e.target, rest = (int(m2[1]), int(m2[2])), m2[3]
        else:
            e.target, rest = m3[1], m3[2]
        rq = Q_RE.findall(rest)
        rid = _ids(rest)
        rints = _ints_outside_quotes(rest)
        starting = bool(re.search(r"\bstart(?:ing)?\b", Q_RE.sub("", rest)))
        if rid and re.search(r"receiver", rest):
            e.slot, e.value = "receiver", rid[-1]
        elif rq:
            e.slot, e.value = ("start_status" if starting else "status"), rq[-1]
        elif rints:
            if re.search(r"\b(increase|decrease)\b", rest):
                e.slot = "size"
            else:
                e.slot = "start_qty" if starting else "qty"
            e.value = abs(rints[-1])
        else:
            raise ParseError("correction value")
        return
    m = re.match(r"record (" + ID_PAT + r") supersedes record (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.new, e.old = "SUPERSEDE", m[1], m[2]
        return
    m = re.match(r"record (" + ID_PAT + r") superseded by new record (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.old, e.new = "SUPERSEDE", m[1], m[2]
        return
    m = re.match(r"replace (" + ID_PAT + r") with (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.old, e.new = "SUPERSEDE", m[1], m[2]
        return
    m = re.match(r"record (" + ID_PAT + r") opened for .*?(" + ID_PAT + r")$", b)
    if m:
        e.kind, e.rec, e.doc = "CREATE_DOC", m[1], m[2]
        return
    m = re.match(r".*?(" + ID_PAT + r") started with record (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.doc, e.rec = "CREATE_DOC", m[1], m[2]
        return
    m = re.match(r"init (" + ID_PAT + r") for (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.rec, e.doc = "CREATE_DOC", m[1], m[2]
        return
    m = re.match(r"(?:.*?\s)?(" + ID_PAT + r") is renumbered as (?:.*?\s)?(" + ID_PAT + r")$", b) or \
        re.match(r"move (" + ID_PAT + r") -> (" + ID_PAT + r")$", b) or \
        re.match(r"(?:.*?\s)?(" + ID_PAT + r") (?:is )?renamed (?:to |as )?(?:.*?\s)?(" + ID_PAT + r")$", b)
    if m:
        e.kind, e.old, e.new = "RENAME", m[1], m[2]
        return
    m = re.match(r"(?:.*?\s)?(" + ID_PAT + r") (?:is )?merged into (?:.*?\s)?(" + ID_PAT + r")$", b) or \
        re.match(r"merge (" + ID_PAT + r") into (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.old, e.new = "MERGE", m[1], m[2]
        return
    if re.search(r"\bcreated for\b|\bregistered to\b", masked) or re.match(r"add " + ID_PAT + r" to ", b):
        if len(ids) < 2:
            raise ParseError("create ids")
        e.kind, e.item, e.holder = "CREATE", ids[0], ids[1]
        tail = b[b.index(ids[1]) + len(ids[1]):]
        tq = Q_RE.findall(tail)
        ti = _ints_outside_quotes(tail)
        e.status = tq[0] if tq else None
        e.qty = ti[0] if ti else None
        if len(tq) > 1 or len(ti) > 1:
            raise ParseError("create fields")
        return
    m = re.match(r"(" + ID_PAT + r") transferred from (" + ID_PAT + r") to (" + ID_PAT + r")$", b) or \
        re.match(r"hand (" + ID_PAT + r") from (" + ID_PAT + r") to (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.item, e.sender, e.receiver = "TRANSFER", m[1], m[2], m[3]
        return
    m = re.match(r"(" + ID_PAT + r") passed (" + ID_PAT + r") to (" + ID_PAT + r")$", b)
    if m:
        e.kind, e.sender, e.item, e.receiver = "TRANSFER", m[1], m[2], m[3]
        return
    m = re.match(r".+? of (" + ID_PAT + r") (increased|decreased) by (\d+)\b", b) or \
        re.match(r"(" + ID_PAT + r"): .+? (up|down) by (\d+)\b", b)
    if m:
        e.kind, e.item, e.fld = "ADJUST", m[1], "qty"
        e.delta = int(m[3]) * (1 if m[2] in ("increased", "up") else -1)
        return
    m = re.match(r"bump (" + ID_PAT + r") .+? ([+-]\d+)$", b)
    if m:
        e.kind, e.item, e.fld, e.delta = "ADJUST", m[1], "qty", int(m[2])
        return
    m = re.match(r".+? of (" + ID_PAT + r") set to (.+)$", b) or re.match(r"(" + ID_PAT + r"): .+? changed to (.+)$", b) \
        or re.match(r"set (" + ID_PAT + r") .+? ('[^']*'|\d+)$", b)
    if m:
        e.kind, e.item = "SET", m[1]
        v = m[2].strip()
        q = Q_RE.findall(v)
        if q:
            e.fld, e.value = "status", q[0]
        else:
            mi = re.match(r"(\d+)\b", v)
            if not mi:
                raise ParseError("set value")
            e.fld, e.value = "qty", int(mi[1])
        return
    raise ParseError("unknown body")


STD_KEYS = {"entry", "no", "entry no", "seq", "date", "time", "recorded", "effective", "subject", "action", "from",
            "to", "refers to", "note", "notes", "comment"}


def _int_lead(v):
    m = re.match(r"\s*([+-]?\d+)\b", str(v))
    return int(m[1]) if m else None


def _date_of(v, rules):
    v = str(v).strip()
    if not v:
        return None
    m = DATE_RE.search(v)
    if not m:
        raise ParseError("no date in " + v[:20])
    return parse_date(m[0], rules.dmy)


def record_to_facts(rec: dict, rules: Rules, facts: Facts):
    if "action" not in rec:
        if "current record" in rec:
            doc = [v for k, v in rec.items() if k != "current record" and ID_RE.fullmatch(str(v).strip())]
            if len(doc) != 1:
                raise ParseError("doc register")
            facts.reg_docs[doc[0].strip()] = rec["current record"].strip()
            facts.has_register = True
            return
        if "holder" in rec:
            item = [v for k, v in rec.items() if k != "holder" and ID_RE.fullmatch(str(v).strip())]
            if len(item) != 1:
                raise ParseError("register item")
            d = {"holder": rec["holder"].strip(), "status": None, "qty": None}
            for k, v in rec.items():
                if k == "holder" or str(v).strip() == item[0] or k in STD_KEYS:
                    continue
                v = str(v).strip()
                if v == "":
                    raise ParseError("blank in register")
                if k == rules.status_field or _int_lead(v) is None:
                    d["status"] = v
                else:
                    d["qty"] = _int_lead(v)
            facts.reg_items[item[0].strip()] = d
            facts.has_register = True
            return
        if rec.get("entry") or rec.get("no"):
            raise ParseError("entry record without action")
        return  # metadata record (title etc.)
    num = rec.get("entry") or rec.get("no") or rec.get("entry no") or rec.get("seq")
    n = _int_lead(num)
    if n is None:
        raise ParseError("entry number")
    e = Entry(kind="?", n=n)
    if "recorded" in rec or "effective" in rec:
        e.date = _date_of(rec.get("recorded", ""), rules)
        e.eff = _date_of(rec.get("effective", ""), rules)
    else:
        e.date = _date_of(rec.get("date", ""), rules)
    if rec.get("time", "").strip():
        e.time = parse_time(rec["time"])
    act = norm_key(rec["action"])
    subj = rec.get("subject", "").strip() or None
    frm = rec.get("from", "").strip() or None
    to = rec.get("to", "").strip() or None
    ref = rec.get("refers to", "").strip()
    vals = {k: str(v).strip() for k, v in rec.items() if k not in STD_KEYS and str(v).strip() != ""}

    def split_vals():
        st, qt = None, None
        for k, v in vals.items():
            if k == rules.status_field or _int_lead(v) is None:
                if st is not None:
                    raise ParseError("two status values")
                st = v
            else:
                if qt is not None:
                    raise ParseError("two qty values")
                qt = _int_lead(v)
        return st, qt

    if act == "create":
        e.kind, e.item, e.holder = "CREATE", subj, to
        e.status, e.qty = split_vals()
    elif act == "set":
        st, qt = split_vals()
        e.kind, e.item = "SET", subj
        if (st is None) == (qt is None):
            raise ParseError("set value")
        e.fld, e.value = ("status", st) if st is not None else ("qty", qt)
    elif act in ("increase", "decrease"):
        st, qt = split_vals()
        if qt is None:
            raise ParseError("adjust amount")
        e.kind, e.item, e.fld, e.delta = "ADJUST", subj, "qty", abs(qt) * (1 if act == "increase" else -1)
    elif act == "transfer":
        e.kind, e.item, e.sender, e.receiver = "TRANSFER", subj, frm, to
    elif act == "void":
        e.kind, e.target = "VOID", (_int_lead(ref), 0)
    elif act == "correct":
        e.kind, e.target = "CORR", (_int_lead(ref), 0)
        st, qt = split_vals()
        if to:
            e.slot, e.value = "receiver", to
        elif st is not None:
            e.slot, e.value = "status", st
        elif qt is not None:
            e.slot, e.value = "qty", abs(qt)
        else:
            raise ParseError("correct value")
    elif act == "rename":
        e.kind, e.old, e.new = "RENAME", subj, to
    elif act == "merge":
        e.kind, e.old, e.new = "MERGE", subj, to
    elif act == "supersede":
        e.kind, e.old, e.new = "SUPERSEDE", subj, to
    elif act in ("open record", "open"):
        e.kind, e.rec, e.doc = "CREATE_DOC", subj, to
    else:
        raise ParseError("unknown action " + act)
    facts.entries.append(e)


H_ENTRY = re.compile(
    r"(?:\bNo\.\s?(?P<n1>\d+),\s(?:recorded (?P<r1>" + DATE_RX + r")(?:, effective (?P<f1>" + DATE_RX + r"))?|(?P<d1>"
    + DATE_RX + r")(?: (?P<t1>" + TIME_RX + r"))?):\s"
    r"|\bEntry (?P<n2>\d+) \((?:recorded (?P<r2>" + DATE_RX + r")(?:, effective (?P<f2>" + DATE_RX + r"))?|(?P<d2>"
    + DATE_RX + r")(?: (?P<t2>" + TIME_RX + r"))?)\):\s"
    r"|(?P<d3>" + DATE_RX + r")(?: (?P<t3>" + TIME_RX + r"))? entry (?P<n3>\d+):\s)", re.I)
H_NOTICE = re.compile(r"\b(?:Notice|Reference) (?P<n>\d+)(?:, dated (?P<d>" + DATE_RX + r")|, (?P<d2>" + DATE_RX
                      + r"))\.", re.I)
H_CHANGE = re.compile(r"(?<![\w.,/:\-])(?P<n>\d+)\.(?P<k>\d+)\s(?=\S)")
H_GIT = re.compile(r"(?P<h>[0-9a-f]{12})\s+(?:(?P<d>" + DATE_RX + r")(?: (?P<t>" + TIME_RX + r"))? )?seq (?P<n>\d+):\s")

REG_HELD = re.compile(r"(" + ID_PAT + r"): held by (" + ID_PAT + r")((?:[^.']|'[^']*')*)")
REG_WITH = re.compile(r"(" + ID_PAT + r") with (" + ID_PAT + r");((?:[^.']|'[^']*')*)")
REG_DOC = re.compile(r"(" + ID_PAT + r")(?::| has) current record (" + ID_PAT + r")")


def _reg_fields(rest):
    q = Q_RE.findall(rest)
    ints = _ints_outside_quotes(rest)
    if len(q) > 1 or len(ints) > 1:
        raise ParseError("register fields")
    return (q[0] if q else None), (ints[0] if ints else None)


def scan_register_text(s: str, facts: Facts):
    found = False
    for m in REG_HELD.finditer(s):
        st, qt = _reg_fields(m[3])
        facts.reg_items[m[1]] = {"holder": m[2], "status": st, "qty": qt}
        found = True
    for m in REG_WITH.finditer(s):
        st, qt = _reg_fields(m[3])
        facts.reg_items[m[1]] = {"holder": m[2], "status": st, "qty": qt}
        found = True
    for m in REG_DOC.finditer(s):
        facts.reg_docs[m[1]] = m[2]
        found = True
    if found:
        facts.has_register = True
    return found


def _body_spans(line, matches):
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(line)
        out.append((m, line[m.end():end].strip()))
    return out


def text_to_facts(s: str, rules: Rules, facts: Facts, state: dict):
    if s.startswith("§"):
        return
    hg = list(H_GIT.finditer(s))
    if hg:
        pre = s[:hg[0].start()]
        dline = DATE_RE.search(pre)
        tline = re.search(TIME_RX, pre)
        for m, body in _body_spans(s, hg):
            e = Entry(kind="?", n=int(m["n"]), hash=m["h"])
            if m["d"]:
                e.date = parse_date(m["d"], rules.dmy)
                e.time = parse_time(m["t"]) if m["t"] else None
            elif dline:
                e.date = parse_date(dline[0], rules.dmy)
                e.time = parse_time(tline[0]) if tline else None
            body = re.sub(r'"\s*$', "", body)
            parse_body(body, e, rules)
            facts.entries.append(e)
        return
    hn = list(H_NOTICE.finditer(s))
    hc = list(H_CHANGE.finditer(s))
    if hn or (hc and state.get("notice")):
        evs = sorted(hn + hc, key=lambda m: m.start())
        pre = s[:evs[0].start()]
        scan_register_text(pre, facts)
        for i, m in enumerate(evs):
            end = evs[i + 1].start() if i + 1 < len(evs) else len(s)
            if m.re is H_NOTICE:
                state["notice"] = (int(m["n"]), parse_date(m["d"] or m["d2"], rules.dmy))
                continue
            if not state.get("notice"):
                raise ParseError("change outside notice")
            nn, nd = state["notice"]
            if int(m["n"]) != nn:
                raise ParseError("change number vs notice")
            e = Entry(kind="?", n=nn, k=int(m["k"]), date=nd)
            parse_body(s[m.end():end].strip(), e, rules)
            if e.kind == "CORR" and isinstance(e.target, tuple) and e.target[1] == 0:
                raise ParseError("S4 correction target")
            facts.entries.append(e)
        return
    he = list(H_ENTRY.finditer(s))
    if he:
        pre = s[:he[0].start()]
        scan_register_text(pre, facts)
        for m, body in _body_spans(s, he):
            n = int(m["n1"] or m["n2"] or m["n3"])
            e = Entry(kind="?", n=n)
            rd = m["r1"] or m["r2"]
            if rd:
                e.date = parse_date(rd, rules.dmy)
                fd = m["f1"] or m["f2"]
                e.eff = parse_date(fd, rules.dmy) if fd else None
            else:
                e.date = parse_date(m["d1"] or m["d2"] or m["d3"], rules.dmy)
                t = m["t1"] or m["t2"] or m["t3"]
                e.time = parse_time(t) if t else None
            body = re.sub(r'"\s*,?\s*$', "", body)
            parse_body(body, e, rules)
            facts.entries.append(e)
        return
    m = re.search(r"Opening snapshot \(end of (" + DATE_RX + r")\)", s, re.I)
    if m:
        facts.s6_d0 = parse_date(m[1], rules.dmy)
        facts.has_register = True
    scan_register_text(s, facts)


def guess_dmy(texts):
    a = b = False
    for t in texts:
        for m in re.finditer(r"(?<![\d/])(\d{1,2})/(\d{1,2})/(\d{4})(?![\d/])", t):
            if int(m[1]) > 12:
                a = True
            if int(m[2]) > 12:
                b = True
    if a and not b:
        return "dmy"
    if b and not a:
        return "mdy"
    return None


def build_facts(state: str, container: str, rules: Rules) -> Facts:
    facts = Facts()
    units = decode_state(state, container)
    st = {}
    for sec, u in units:
        if isinstance(u, dict):
            if any(isinstance(v, str) and H_ENTRY.search(v + " ") for v in u.values()) and "action" not in u:
                for v in u.values():
                    text_to_facts(str(v), rules, facts, st)
                continue
            record_to_facts(u, rules, facts)
        else:
            if "snapshot" in sec.lower() and DATE_RE.search(sec) and facts.s6_d0 is None:
                m = re.search(r"end of (" + DATE_RX + r")", sec, re.I)
                if m:
                    facts.s6_d0 = parse_date(m[1], rules.dmy)
            text_to_facts(u, rules, facts, st)
    return facts


def finish_facts(facts: Facts, rules: Rules, sampler: str):
    """Resolve S5 hash targets, expand S4 withdrawals, fix correction slots by target type, check numbering."""
    E = facts.entries
    byhash = {e.hash: e for e in E if e.hash}
    for e in E:
        if isinstance(e.target, str):
            t = byhash.get(e.target)
            if t is None:
                raise ParseError("hash target missing")
            e.target = t.ref
    out = []
    for e in E:
        if e.kind == "WITHDRAW":
            tgt = [x for x in E if x.n == e.target and x.kind != "WITHDRAW"]
            if not tgt:
                raise ParseError("withdrawn notice not shown")
            out.append(Entry(kind="VOID", n=e.n, k=e.k, date=e.date, target=[x.ref for x in tgt]))
        else:
            out.append(e)
    E = out
    refs = {}
    for e in E:
        if e.ref in refs:
            raise ParseError("duplicate entry ref")
        refs[e.ref] = e
    for e in E:
        if e.kind in ("VOID", "CORR"):
            tl = e.target if isinstance(e.target, list) else [e.target]
            for t in tl:
                if t not in refs:
                    raise ParseError("target not shown")
            if e.kind == "CORR":
                t = refs[e.target]
                if t.kind == "TRANSFER":
                    if e.slot != "receiver":
                        raise ParseError("corr slot transfer")
                elif t.kind == "SET":
                    if (t.fld == "status") != (e.slot in ("status", "start_status")) or e.slot == "receiver":
                        raise ParseError("corr slot set")
                    e.slot = "value"
                elif t.kind == "ADJUST":
                    if e.slot not in ("qty", "size", "start_qty"):
                        raise ParseError("corr slot adjust")
                    e.slot = "size"
                elif t.kind == "CREATE":
                    if e.slot in ("status", "start_status"):
                        e.slot = "start_status"
                    elif e.slot in ("qty", "start_qty"):
                        e.slot = "start_qty"
                    else:
                        raise ParseError("corr slot create")
                else:
                    raise ParseError("corr target kind " + t.kind)
    facts.entries = E
    # numbering
    if sampler == "S4" or any(e.k for e in E):
        nums = sorted({e.n for e in E})
        for nn in nums:
            ks = sorted(e.k for e in E if e.n == nn)
            if ks != list(range(1, len(ks) + 1)):
                raise ParseError("change numbering")
    else:
        nums = sorted(e.n for e in E)
    if not nums:
        raise ParseError("no entries")
    start = rules.n0 if rules.gap == "leading" else 1
    if nums[0] < start:
        raise ParseError("entry before start")
    missing = sorted(set(range(start, nums[-1] + 1)) - set(nums))
    if rules.world == "closed" and (missing or nums[0] != 1):
        raise ParseError("closed card has missing numbers")
    if rules.gap == "leading" and (missing or nums[0] != rules.n0):
        raise ParseError("leading extract inner gap")
    facts.missing = missing
    return facts


# ----------------------------------------------------------------------------------------------------------------
# 5. Question -> query
# ----------------------------------------------------------------------------------------------------------------
PT_RX = (r"(?P<pt> at the end of (?P<de>" + DATE_RX + r")| at the start of (?P<ds>" + DATE_RX + r")| on (?P<do>"
         + DATE_RX + r")| as of (?P<da>" + DATE_RX + r")| at any time between (?P<r1>" + DATE_RX + r") and (?P<r2>"
         + DATE_RX + r")| at the end| now| currently)?")
CMP_RX = r"(?P<cmp>no fewer than|no more than|at least|at most|more than|fewer than) (?P<N>\d+)"
KW = r"(?:[a-z][a-z\-']*(?: [a-z][a-z\-']*)* )?"   # optional kind words before an ID


def _point(m, rules):
    if m["de"]:
        return ("on", parse_date(m["de"], rules.dmy))
    if m["ds"]:
        return ("start", parse_date(m["ds"], rules.dmy))
    if m["do"]:
        return ("on", parse_date(m["do"], rules.dmy))
    if m["da"]:
        return ("on", parse_date(m["da"], rules.dmy))
    if m["r1"]:
        return ("range", parse_date(m["r1"], rules.dmy), parse_date(m["r2"], rules.dmy))
    return ("end",)


def parse_decl(s: str, rules: Rules):
    s = s.strip()
    m = re.fullmatch(r"it is not the case that (.+)", s)
    if m:
        return ("NOT", parse_decl(m[1], rules))
    # holding
    m = re.fullmatch(KW + r"(?P<x>" + ANYID + r") (?P<v>holds|held|does not hold|did not hold|still holds|no longer holds)"
                     r" " + KW + r"(?P<y>" + ANYID + r")" + PT_RX, s)
    if m:
        pt = _point(m, rules)
        v = m["v"]
        if v == "still holds":
            if m["pt"]:
                raise ParseError("still with point")
            return ("HOLD", m["x"], m["y"], ("end",), "still")
        if v == "no longer holds":
            if m["pt"]:
                raise ParseError("no longer with point")
            return ("NOLONGER", m["x"], m["y"])
        if pt[0] == "range":
            raise ParseError("holding range")
        c = ("HOLD", m["x"], m["y"], pt, "")
        return ("NOT", c) if "not" in v else c
    # count (Q6)
    m = re.fullmatch(KW + r"(?P<x>" + ANYID + r") (?P<v>holds|held) " + CMP_RX + r" [a-z][a-z \-']*?" + PT_RX, s)
    if m:
        return ("COUNT", m["x"], m["cmp"], int(m["N"]), _point(m, rules))
    # status / quantity of an item
    m = re.fullmatch(r"the (?P<f>.+?) of " + KW + r"(?P<y>" + ANYID + r") (?P<v>is not|was not|is|was) (?P<val>.+?)"
                     + PT_RX, s)
    if m and (m["val"].startswith("'") or re.match(CMP_RX, m["val"])):
        pt = _point(m, rules)
        neg = m["v"].endswith("not")
        val = m["val"]
        mc = re.fullmatch(CMP_RX + r"(?: [^']+)?", val)
        if mc:
            c = ("QTY", m["y"], mc["cmp"], int(mc["N"]), pt)
        else:
            vs = re.fullmatch(r"'([^']*)'(?: or '([^']*)')?", val)
            if not vs:
                raise ParseError("status value")
            c = ("STATUS", m["y"], [x for x in (vs[1], vs[2]) if x is not None], pt)
        return ("NOT", c) if neg else c
    # current record (Q3)
    m = re.fullmatch(r"(?P<r>" + ANYID + r") (?P<v>is|is not) the current record of " + KW + r"(?:the )?" + KW
                     + r"(?P<d>" + ANYID + r")(?: at the end| now| currently)?", s)
    if m:
        c = ("CURRENT", m["r"], m["d"])
        return ("NOT", c) if m["v"] == "is not" else c
    m = re.fullmatch(KW + r"(?P<d>" + ANYID + r") lacks (?P<r>" + ANYID + r") as its current record(?: at the end| now| "
                     r"currently)?", s)
    if m:
        return ("NOT", ("CURRENT", m["r"], m["d"]))
    # transfer took effect (Q8)
    m = re.fullmatch(r"the transfer in (?:entry (?P<n>\d+)|change (?P<a>\d+)\.(?P<b>\d+)) (?P<v>took effect|did not take "
                     r"effect|failed to take effect)", s)
    if m:
        ref = (int(m["n"]), 0) if m["n"] else (int(m["a"]), int(m["b"]))
        c = ("TOOK", ref)
        return c if m["v"] == "took effect" else ("NOT", c)
    raise ParseError("declarative")


def parse_question(q: str, rules: Rules):
    q = re.sub(r"\s+", " ", q.strip()).rstrip("?").strip()
    m = re.fullmatch(r"Is it true that (.+)", q)
    if m:
        return "yn", parse_decl(m[1], rules)
    m = re.fullmatch(r"Is it false that (.+)", q)
    if m:
        return "yn", ("NOT", parse_decl(m[1], rules))
    # interrogatives -> declaratives
    conv = [
        (r"Does (.+?) still hold (.+)", lambda m: f"{m[1]} still holds {m[2]}"),
        (r"Does (.+?) hold (.+)", lambda m: f"{m[1]} holds {m[2]}"),
        (r"Did (.+?) hold (.+)", lambda m: f"{m[1]} held {m[2]}"),
        (r"Is the (.+?) of (.+)", lambda m: f"the {m[1]} of {m[2]}"),
        (r"Was the (.+?) of (.+)", lambda m: f"the {m[1]} of {m[2]}"),
        (r"Did the transfer in (.+?) fail to take effect", lambda m: f"the transfer in {m[1]} failed to take effect"),
        (r"Did the transfer in (.+?) take effect", lambda m: f"the transfer in {m[1]} took effect"),
        (r"Does (.+?) lack (.+)", lambda m: f"{m[1]} lacks {m[2]}"),
        (r"Is (" + ANYID + r") the current record of (.+)", lambda m: f"{m[1]} is the current record of {m[2]}"),
    ]
    # choice forms first
    m = re.fullmatch(r"What (?:is|was) the (?P<f>.+?) of " + KW + r"(?P<y>" + ANYID + r")" + PT_RX, q)
    if m:
        return "choice", ("STATUS?", m["y"], _point(m, rules))
    m = re.fullmatch(r"(?:Who |Which " + KW + r")holds " + KW + r"(?P<y>" + ANYID + r")" + PT_RX, q)
    if m:
        return "choice", ("HOLDER?", m["y"], _point(m, rules))
    m = re.fullmatch(r"Which of these .+? does " + KW + r"(?P<x>" + ANYID + r") hold" + PT_RX, q)
    if m:
        return "choice", ("HELD?", m["x"], _point(m, rules))
    m = re.fullmatch(r"Which record of " + KW + r"(?:the )?" + KW + r"(?P<d>" + ANYID + r") is current(?: at the end| now|"
                     r" currently)?", q)
    if m:
        return "choice", ("CURRENT?", m["d"])
    for rx, f in conv:
        m = re.fullmatch(rx, q)
        if m:
            d = f(m)
            if rx.startswith("Is the") or rx.startswith("Was the"):
                # "Is the F of Y 'S' PT" -> "the F of Y is 'S' PT"
                mm = re.fullmatch(r"the (.+?) of (" + KW + ANYID + r") (.+)", d)
                if not mm:
                    raise ParseError("status question")
                d = f"the {mm[1]} of {mm[2]} {'is' if rx.startswith('Is') else 'was'} {mm[3]}"
            return "yn", parse_decl(d, rules)
    raise ParseError("question form")


def find_question(instr: str, state: str):
    cands = []
    t = instr
    for m in re.finditer(r"\?", t):
        j = m.start()
        starts = [0]
        for sep in ("\n", ". ", ": ", ") ", "? "):
            p = t.rfind(sep, 0, j)
            if p >= 0:
                starts.append(p + len(sep))
        seg = t[max(starts):j + 1].strip()
        seg = re.sub(r"^(?:[-*•+·>]\s*)+", "", seg)
        ids = ID_RE.findall(seg) + HASH_RE.findall(seg)
        if not ids and not re.search(r"entry \d+|change \d+\.\d+", seg):
            continue
        if all(x in state for x in ids):
            cands.append(seg)
    # S4 change refs contain '.', re-join "change 2.1 take effect?"
    if not cands:
        for m in re.finditer(r"Did the transfer in change \d+\.\d+ (?:take|fail to take) effect\?", t):
            cands.append(m[0])
        for m in re.finditer(r"Is it (?:true|false) that[^?\n]*?change \d+\.\d+[^?\n]*\?", t):
            cands.append(m[0])
    if not cands:
        raise ParseError("no question")
    return cands[-1]


# ----------------------------------------------------------------------------------------------------------------
# 6. Solver B: backward version-graph resolver
# ----------------------------------------------------------------------------------------------------------------
NOTEXIST = "<notexist>"
UNKNOWN = "<unknown>"


class Anomaly(Exception):
    pass


class Resolver:
    def __init__(self, facts: Facts, rules: Rules, sampler: str):
        self.F, self.R, self.sampler = facts, rules, sampler
        self.notes = []
        E = facts.entries
        self.byref = {e.ref: e for e in E}
        # void edges (VOIDs are never voided: rule 3)
        self.voided = set()
        for e in E:
            if e.kind == "VOID":
                tl = e.target if isinstance(e.target, list) else [e.target]
                for t in tl:
                    tk = self.byref[t].kind
                    if tk in ("VOID", "CREATE", "CREATE_DOC", "RENAME", "MERGE"):
                        raise Anomaly("void of non-voidable " + tk)
                    self.voided.add(t)
        # correction edges, one per corrected value: highest-numbered non-voided correction counts (T11, R3-01)
        best = {}
        for e in E:
            if e.kind == "CORR" and e.ref not in self.voided and e.target not in self.voided:
                key = (e.target, e.slot)
                if key not in best or e.ref > best[key].ref:
                    best[key] = e
        # effective (corrected) writers
        L = []
        for e in E:
            if e.kind in ("VOID", "CORR") or e.ref in self.voided:
                continue
            c = Entry(**{k: getattr(e, k) for k in e.__dataclass_fields__})
            for (t, slot), ce in best.items():
                if t != e.ref:
                    continue
                if slot == "receiver":
                    c.receiver = ce.value
                elif slot == "value":
                    c.value = ce.value
                elif slot == "size":
                    c.delta = abs(ce.value) * (1 if e.delta > 0 else -1)
                    if ce.value < 1:
                        raise Anomaly("adjust size < 1")
                elif slot == "start_status":
                    c.status = ce.value
                elif slot == "start_qty":
                    c.qty = ce.value
            L.append(c)
        self.L = sorted(L, key=self.okey)
        self.pos = {e.ref: i for i, e in enumerate(self.L)}
        # rename closure (whole log; renames are never voided or corrected)
        self.parent = {}
        renames = [e for e in self.L if e.kind == "RENAME"]
        for e in renames:
            self._union(e.old, e.new)
        self.renamed_from = {e.old: self.pos[e.ref] for e in renames}   # old ID -> position of its rename
        self.renamed_to = {e.old: e.new for e in renames}
        # merges (timed)
        self.absorbed = {}
        for e in self.L:
            if e.kind == "MERGE":
                a = self.ent(e.old)
                if a in self.absorbed:
                    raise Anomaly("double merge")
                self.absorbed[a] = self.pos[e.ref]
        # register keyed by entity
        self.reg = {}
        for i, d in facts.reg_items.items():
            self.reg[self.ent(i)] = d
        self.memo_h, self.memo_s, self.memo_q, self.memo_t = {}, {}, {}, {}
        self.open = rules.world == "open"
        if self.open:
            if renames or self.absorbed or rules.check or rules.lock:
                raise Anomaly("open card with rename/merge/check/lock")
        self.check_numbering()

    # effect-order key (section 3 step 3)
    def okey(self, e):
        if self.sampler == "S5" or e.hash:
            return (e.n, 0, 0)
        if e.k or self.sampler == "S4":
            return (e.date, e.n, e.k)
        if e.eff is not None or self.R.effective:
            if e.eff is None:
                raise Anomaly("S6 writer without effective date")
            return (e.eff, e.n, 0)
        return (e.date, -1 if e.time is None else e.time, e.n)

    def check_numbering(self):
        E = [e for e in self.F.entries]
        if self.sampler in ("S1", "S2", "S3", "S5"):
            srt = sorted(E, key=lambda e: e.n)
            for a, b in zip(srt, srt[1:]):
                ka = (a.date, -1 if a.time is None else a.time)
                kb = (b.date, -1 if b.time is None else b.time)
                if kb < ka:
                    self.notes.append("rule1: entry numbers do not follow date/time")
                    break
        if self.sampler == "S6":
            srt = sorted(E, key=lambda e: e.n)
            for a, b in zip(srt, srt[1:]):
                if b.date < a.date:
                    self.notes.append("rule1: S6 numbers do not follow recorded date")
                    break
        for e in E:
            if e.kind in ("VOID", "CORR"):
                tl = e.target if isinstance(e.target, list) else [e.target]
                if any(t >= e.ref for t in tl):
                    self.notes.append("rule1: void/correction not after target")

    # entities
    def _find(self, x):
        p = self.parent.setdefault(x, x)
        if p != x:
            r = self._find(p)
            self.parent[x] = r
            return r
        return x

    def _union(self, a, b):
        ra, rb = self._find(a), self._find(b)
        if ra != rb:
            self.parent[ra] = rb

    def ent(self, x):
        return self._find(x)

    def latest(self, x):
        cur = x
        seen = set()
        while cur in self.renamed_to and cur not in seen:
            seen.add(cur)
            cur = self.renamed_to[cur]
        return cur

    # validity of an (already corrected) entry at its own point (T14 retire, T15 absorbed; rule 10)
    def named(self, e):
        if e.kind == "CREATE":
            return [e.item, e.holder]
        if e.kind in ("SET", "ADJUST"):
            return [e.item]
        if e.kind == "TRANSFER":
            return [e.item, e.sender, e.receiver]
        if e.kind in ("RENAME", "MERGE"):
            return [e.old, e.new]
        return []

    def valid(self, j):
        e = self.L[j]
        for x in self.named(e):
            if x is None:
                continue
            if self.R.rename == "retire" and x in self.renamed_from and j > self.renamed_from[x]:
                return False
            a = self.absorbed.get(self.ent(x))
            if a is not None and j > a:
                return False
        return True

    def is_item_entry(self, e, it):
        return e.item is not None and self.ent(e.item) == it

    # holder(item, t-): state after L[0..i-1]
    def holder(self, it, i):
        key = (it, i)
        if key in self.memo_h:
            return self.memo_h[key]
        res = None
        for j in range(i - 1, -1, -1):
            e = self.L[j]
            if e.kind == "CREATE" and self.is_item_entry(e, it):
                if not self.valid(j):
                    raise Anomaly("create names retired/absorbed id")
                res = self.ent(e.holder)
                break
            if e.kind == "TRANSFER" and self.is_item_entry(e, it):
                if self.takes_effect(j):
                    res = self.ent(e.receiver)
                    break
                continue
            if e.kind == "MERGE" and self.valid(j):
                if self.holder(it, j) == self.ent(e.old):
                    res = self.ent(e.new)
                    break
        if res is None:
            d = self.reg.get(it)
            res = self.ent(d["holder"]) if d else NOTEXIST
        self.memo_h[key] = res
        return res

    def status(self, it, i):
        key = (it, i)
        if key in self.memo_s:
            return self.memo_s[key]
        res = None
        for j in range(i - 1, -1, -1):
            e = self.L[j]
            if e.kind == "SET" and e.fld == "status" and self.is_item_entry(e, it) and self.valid(j):
                res = e.value
                break
            if e.kind == "CREATE" and self.is_item_entry(e, it):
                res = e.status if e.status is not None else self.R.default_status
                if res is None:
                    raise Anomaly("blank creation status with no stated default")
                break
        if res is None:
            d = self.reg.get(it)
            res = d["status"] if d else NOTEXIST
            if d and res is None:
                raise Anomaly("register item without status")
        self.memo_s[key] = res
        return res

    def qty(self, it, i):
        key = (it, i)
        if key in self.memo_q:
            return self.memo_q[key]
        delta = 0
        res = None
        for j in range(i - 1, -1, -1):
            e = self.L[j]
            if not self.is_item_entry(e, it):
                continue
            if e.kind == "ADJUST" and self.valid(j):
                delta += e.delta
            elif e.kind == "SET" and e.fld == "qty" and self.valid(j):
                res = e.value + delta
                break
            elif e.kind == "CREATE":
                base = e.qty if e.qty is not None else self.R.default_qty
                if base is None:
                    raise Anomaly("blank creation quantity with no stated default")
                res = base + delta
                break
        if res is None:
            d = self.reg.get(it)
            if not d:
                res = NOTEXIST
            elif d["qty"] is None:
                raise Anomaly("no quantity field")
            else:
                res = d["qty"] + delta
        if res is not NOTEXIST and res < 0:
            self.notes.append("rule7: quantity below 0")
        self.memo_q[key] = res
        return res

    def takes_effect(self, j):
        if j in self.memo_t:
            return self.memo_t[j]
        e = self.L[j]
        ok = self.valid(j)
        it = self.ent(e.item)
        if ok and self.R.check:
            ok = self.holder(it, j) == self.ent(e.sender)
        if ok and self.R.lock is not None:
            ok = self.status(it, j) != self.R.lock
        if ok and not self.R.check and self.holder(it, j) != self.ent(e.sender):
            self.notes.append("rule6: sender is not the holder just before a transfer (check off)")
        if ok and self.ent(e.sender) == self.ent(e.receiver):
            self.notes.append("rule6: sender equals receiver")
        self.memo_t[j] = ok
        return ok

    # points
    def dkey(self, e):
        if e.eff is not None or self.R.effective:
            return e.eff
        return e.date

    def at(self, pt):
        if pt[0] == "end":
            return len(self.L)
        D = pt[1]
        if pt[0] == "on":
            return sum(1 for e in self.L if self.dkey(e) <= D)
        if pt[0] == "start":
            return sum(1 for e in self.L if self.dkey(e) < D)
        raise Anomaly("bad point")

    def range_points(self, d1, d2):
        pts = [sum(1 for e in self.L if self.dkey(e) < d1)]
        for j, e in enumerate(self.L):
            if d1 <= self.dkey(e) <= d2:
                pts.append(j + 1)
        return pts

    # open world (T2): exact setter after every missing entry
    def after_gaps(self, e):
        if self.R.gap == "leading":
            return True
        miss = self.F.missing
        if not miss:
            return True
        return e.n > max(miss)

    def open_value(self, it, what):
        last = None
        for j in range(len(self.L) - 1, -1, -1):
            e = self.L[j]
            if not self.is_item_entry(e, it):
                continue
            if what == "holder" and e.kind in ("CREATE", "TRANSFER"):
                last = j
                break
            if what == "status" and (e.kind == "CREATE" or (e.kind == "SET" and e.fld == "status")):
                last = j
                break
            if what == "qty" and (e.kind == "CREATE" or (e.kind == "SET" and e.fld == "qty")):
                last = j
                break
        if last is None or not self.after_gaps(self.L[last]):
            return UNKNOWN
        e = self.L[last]
        if what == "holder":
            return self.ent(e.holder if e.kind == "CREATE" else e.receiver)
        if what == "status":
            v = e.status if e.kind == "CREATE" else e.value
            if v is None:
                v = self.R.default_status
            if v is None:
                raise Anomaly("blank status no default")
            return v
        base = (e.qty if e.qty is not None else self.R.default_qty) if e.kind == "CREATE" else e.value
        if base is None:
            raise Anomaly("blank qty no default")
        for e2 in self.L[last + 1:]:
            if e2.kind == "ADJUST" and self.is_item_entry(e2, it):
                base += e2.delta
        return base

    def held_some_point(self, x, it):
        if self.open:
            d = self.reg.get(it)
            if d and self.F.has_register and self.R.gap != "leading" and self.ent(d["holder"]) == x:
                return True
            for e in self.L:
                if not self.is_item_entry(e, it) or not self.after_gaps(e):
                    continue
                if e.kind == "CREATE" and self.ent(e.holder) == x:
                    return True
                if e.kind == "TRANSFER" and (self.ent(e.receiver) == x or self.ent(e.sender) == x):
                    return True
            return False
        return any(self.holder(it, i) == x for i in range(0, len(self.L) + 1))

    def guard_end_of_dates(self, x, it):
        """T31 guard: X held Y in the opening state or at the end of some date."""
        if self.open:
            return self.held_some_point(x, it)
        if self.holder(it, 0) == x:
            return True
        dates = sorted({self.dkey(e) for e in self.L})
        return any(self.holder(it, self.at(("on", d))) == x for d in dates)

    # value getters used by claims
    def get(self, what, it, i):
        if self.open:
            if i != len(self.L):
                raise Anomaly("open card asks a non-end point")
            return self.open_value(it, what)
        if what == "holder":
            return self.holder(it, i)
        if what == "status":
            return self.status(it, i)
        return self.qty(it, i)

    def items(self):
        s = set(self.ent(i) for i in self.F.reg_items)
        s |= {self.ent(e.item) for e in self.L if e.kind == "CREATE"}
        return s

    def current_record(self, doc):
        root = self.F.reg_docs.get(doc)
        for e in self.L:
            if e.kind == "CREATE_DOC" and e.doc == doc:
                if root is not None:
                    raise Anomaly("document created twice")
                root = e.rec
        if root is None:
            raise Anomaly("document has no root")
        nxt = {}
        for e in self.L:
            if e.kind == "SUPERSEDE":
                if e.old in nxt:
                    raise Anomaly("supersede fork")
                nxt[e.old] = e.new
        cur, seen = root, {root}
        while cur in nxt:
            cur = nxt[cur]
            if cur in seen:
                raise Anomaly("supersede cycle")
            seen.add(cur)
        # rule 8 check: each supersede names the current record at its moment
        cur2 = {}
        for d, r in self.F.reg_docs.items():
            cur2[d] = r
        rec_doc = {r: d for d, r in self.F.reg_docs.items()}
        for e in self.L:
            if e.kind == "CREATE_DOC":
                cur2[e.doc] = e.rec
                rec_doc[e.rec] = e.doc
            elif e.kind == "SUPERSEDE":
                d = rec_doc.get(e.old)
                if d is None or cur2.get(d) != e.old:
                    self.notes.append("rule8: supersede of a record that is not current")
                else:
                    cur2[d] = e.new
                    rec_doc[e.new] = d
        return cur


CMP = {"at least": lambda a, n: a >= n, "no fewer than": lambda a, n: a >= n, "at most": lambda a, n: a <= n,
       "no more than": lambda a, n: a <= n, "more than": lambda a, n: a > n, "fewer than": lambda a, n: a < n}


def eval_claim(c, W: Resolver):
    k = c[0]
    if k == "NOT":
        return not eval_claim(c[1], W)
    if k == "HOLD":
        _, x, y, pt, flag = c
        it, xe = W.ent(y), W.ent(x)
        if pt[0] == "range":
            raise Anomaly("holding range")
        h = W.get("holder", it, W.at(pt))
        if h is UNKNOWN:
            raise Anomaly("yes/no answer UNKNOWN (open world)")
        if h is NOTEXIST:
            raise Anomaly("query item does not exist at query point")
        if flag == "still" and not W.guard_end_of_dates(xe, it):
            W.notes.append("T31 guard fails on a 'still' row")
        return h == xe
    if k == "NOLONGER":
        _, x, y = c
        it, xe = W.ent(y), W.ent(x)
        h = W.get("holder", it, len(W.L))
        if h is UNKNOWN:
            raise Anomaly("yes/no answer UNKNOWN (open world)")
        if not W.guard_end_of_dates(xe, it):
            W.notes.append("T31 guard fails on a 'no longer' row")
        return W.held_some_point(xe, it) and h != xe
    if k in ("STATUS", "QTY"):
        it = W.ent(c[1])
        pt = c[-1]

        def one(i):
            if k == "STATUS":
                v = W.get("status", it, i)
                if v in (UNKNOWN, NOTEXIST):
                    raise Anomaly("status " + v)
                return v in c[2]
            v = W.get("qty", it, i)
            if v in (UNKNOWN, NOTEXIST):
                raise Anomaly("qty " + str(v))
            return CMP[c[2]](v, c[3])
        if pt[0] == "range":
            return any(one(i) for i in W.range_points(pt[1], pt[2]))
        return one(W.at(pt))
    if k == "COUNT":
        _, x, cmp, n, pt = c
        xe = W.ent(x)
        i = W.at(pt)
        cnt = sum(1 for it in W.items() if W.get("holder", it, i) == xe)
        return CMP[cmp](cnt, n)
    if k == "CURRENT":
        return W.current_record(c[2]) == c[1]
    if k == "TOOK":
        ref = c[1]
        e = W.byref.get(ref)
        if e is None or e.kind != "TRANSFER":
            raise Anomaly("Q8 entry is not a transfer")
        if ref in W.voided:
            return False
        return W.takes_effect(W.pos[ref])
    raise Anomaly("claim kind " + k)


def answer_choice(q, W: Resolver, options, rules: Rules):
    k = q[0]
    if k == "STATUS?":
        it = W.ent(q[1])
        v = W.get("status", it, W.at(q[2]))
        if v is UNKNOWN:
            return rules.nei if rules.nei else UNKNOWN
        if v is NOTEXIST:
            raise Anomaly("status of non-existing item")
        return v
    if k == "HOLDER?":
        it = W.ent(q[1])
        h = W.get("holder", it, W.at(q[2]))
        if h is UNKNOWN:
            return rules.nei if rules.nei else UNKNOWN
        if h is NOTEXIST:
            raise Anomaly("holder of non-existing item")
        # options name each entity by its latest ID
        cands = [o for o in options if ID_RE.fullmatch(o) or HASH_RE.fullmatch(o)]
        hit = [o for o in cands if W.ent(o) == h]
        if len(hit) == 1:
            return hit[0]
        return W.latest(h)
    if k == "HELD?":
        xe = W.ent(q[1])
        i = W.at(q[2])
        listed = [o for o in options if ID_RE.fullmatch(o) or HASH_RE.fullmatch(o)]
        held = [o for o in listed if W.get("holder", W.ent(o), i) == xe]
        if len(held) > 1:
            raise Anomaly("Q7 rule 11: more than one listed item held")
        if held:
            return held[0]
        return rules.none if rules.none else "<none>"
    if k == "CURRENT?":
        return W.current_record(q[1])
    raise Anomaly("choice kind")


# ----------------------------------------------------------------------------------------------------------------
# 7. Row driver
# ----------------------------------------------------------------------------------------------------------------
def spec_items(row, rules: Rules, facts, query, form):
    """Spec items a row's label depends on (for the mismatch report; ids only, never text)."""
    items = []
    if query is not None:
        q = query
        flat = json.dumps(q)
        if form == "choice":
            items.append({"STATUS?": "Q1/Q2 status choice", "HOLDER?": "Q5", "HELD?": "Q7 (rule 11, T34)",
                          "CURRENT?": "Q3 (T13, T37)"}.get(q[0], q[0]))
        else:
            for tag, name in (("TOOK", "Q8 (T38)"), ("CURRENT", "Q3 (T13)"), ("COUNT", "Q6 (T39, T22)"),
                              ("NOLONGER", "Q4 no longer (T31)"), ("HOLD", "Q4 (T17)"), ("QTY", "Q1/Q2 threshold (T22)"),
                              ("STATUS", "Q1/Q2 status")):
                if '"' + tag + '"' in flat:
                    items.append(name)
                    break
            if '"NOT"' in flat:
                items.append("T44 negated stem (2.2)")
        if '"range"' in flat:
            items.append("T25")
        elif '"on"' in flat or '"start"' in flat:
            items.append("T24")
    if rules.world == "open":
        items.append("T2/T3 open world (" + str(rules.gap) + ")")
    if facts is not None:
        kinds = {e.kind for e in facts.entries}
        for kname, t in (("VOID", "T10"), ("CORR", "T11/T12"), ("RENAME", "T14 " + str(rules.rename)),
                         ("MERGE", "T15"), ("SUPERSEDE", "T13")):
            if kname in kinds:
                items.append(t)
    if rules.check and rules.lock:
        items.append("T40")
    elif rules.check:
        items.append("T18")
    elif rules.lock:
        items.append("T19")
    if rules.effective:
        items.append("T6/T7 effective dates")
    if row["meta"]["sampler"] == "S4":
        items.append("T41 notices")
    if row["meta"]["sampler"] == "S5":
        items.append("T43 git-like log")
    if not rules.stated:
        items.append("2.1 short/no card")
    return items


def solve_row(row):
    meta = row["meta"]
    sampler = meta["sampler"]
    container, _ = style_container(meta["format_style"])
    card = row.get("card") or ""
    instr = row.get("instructions") or ""
    rules = parse_rules(card + "\n" + instr)
    if rules.dmy is None:
        rules.dmy = guess_dmy([row["state"]])
    facts = build_facts(row["state"], container, rules)
    finish_facts(facts, rules, sampler)
    qtext = find_question(instr, row["state"])
    form, query = parse_question(qtext, rules)
    want = "yn" if row["qtype"] == "noul" else "choice"
    if form != want:
        raise ParseError("question form does not match qtype")
    W = Resolver(facts, rules, sampler)
    if rules.gap == "explicit":
        runs = sum(1 for i, x in enumerate(facts.missing) if i == 0 or facts.missing[i - 1] != x - 1)
        if row["state"].count(rules.marker) != runs:
            W.notes.append("T3: explicit gap markers do not match skipped numbers")
    if form == "yn":
        ans = 1 if eval_claim(query, W) else 0
    else:
        ans = answer_choice(query, W, row["options"], rules)
        if ans not in row["options"]:
            W.notes.append("solver-B answer not among options")
    return ans, rules, facts, query, form, W.notes


def _sha(path):
    import hashlib
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def sensitivity(rows):
    """Ablations: each deliberately wrong reading must move some labels, or agreement would be vacuous."""
    global parse_rules, eval_claim
    out = {}
    base_init, base_okey, base_after = Resolver.__init__, Resolver.okey, Resolver.after_gaps
    base_rules, base_claim = parse_rules, eval_claim

    def drop(kind):
        def init(self, facts, rules, sampler):
            facts.entries = [e for e in facts.entries if e.kind != kind]
            base_init(self, facts, rules, sampler)
        return init

    def rules_patch(fn):
        def pr(t):
            r = base_rules(t)
            fn(r)
            return r
        return pr

    def no_check(r):
        r.check, r.lock = False, None

    def swap_mode(r):
        if r.rename:
            r.rename = {"alias": "retire", "retire": "alias"}[r.rename]

    def rec_okey(self, e):
        return (e.date, e.n, 0) if e.eff is not None else base_okey(self, e)

    def no_not(c, W):
        return base_claim(c[1], W) if c[0] == "NOT" else base_claim(c, W)

    abl = [("ignore voids (T10)", lambda: setattr(Resolver, "__init__", drop("VOID"))),
           ("ignore corrections (T11)", lambda: setattr(Resolver, "__init__", drop("CORR"))),
           ("ignore transfer check / lock (T18/T19/T40)", lambda: globals().__setitem__("parse_rules", rules_patch(no_check))),
           ("swap rename mode (T14)", lambda: globals().__setitem__("parse_rules", rules_patch(swap_mode))),
           ("recorded-date order on S6 (T6)", lambda: setattr(Resolver, "okey", rec_okey)),
           ("ignore missing entries (T2)", lambda: setattr(Resolver, "after_gaps", lambda self, e: True)),
           ("ignore negation (T44)", lambda: globals().__setitem__("eval_claim", no_not))]
    for name, patch in abl:
        patch()
        moved = err = 0
        for row in rows:
            try:
                a = solve_row(row)[0]
            except Exception:
                err += 1
                continue
            moved += a != row["gold"]
        Resolver.__init__, Resolver.okey, Resolver.after_gaps = base_init, base_okey, base_after
        globals()["parse_rules"], globals()["eval_claim"] = base_rules, base_claim
        out[name] = {"labels_moved": moved, "unsolvable": err}
    return out


def run(files, out_path, log=None, with_sensitivity=False):
    spec = os.path.join(LEAN, "c_src", "F3", "G0_SPEC.md")
    frozen = json.load(open(os.path.join(LEAN, "c_src", "F3", "G0_FROZEN.json")))
    res = {"family": "F3", "spec_id": "F3.G0.v7", "g0_spec_sha256": _sha(spec),
           "g0_spec_sha256_matches_frozen": _sha(spec) == frozen.get("sha256"),
           "solver": "c_src/F3/solverB/solver_b.py", "solver_sha256": _sha(os.path.abspath(__file__)),
           "paradigm": "parse rendered row -> facts; lazy memoized backward version-graph resolver (void / "
                       "per-value correction / rename-closure / timed-merge / supersede edges, gap nodes); open "
                       "world by the T2 knowability table",
           "independence": "written from G0_SPEC.md (F3.G0.v7), spec 2.4 row format and the formats-1 style pool only; "
                           "never reads c_src/F3/gen/ or solver A; no sidecar field is used",
           "gold_convention": "noul: 1 = Yes, 0 = No (fmt1 loader_check); choice: exact option text",
           "files": {}, "mismatches": [], "parse_failures": [], "anomalies": [], "anomaly_counts": {}}
    allrows = []
    for fp in files:
        n = agree = mism = pfail = 0
        for ln in open(fp):
            row = json.loads(ln)
            allrows.append(row)
            n += 1
            rules = facts = query = form = None
            try:
                ans, rules, facts, query, form, notes = solve_row(row)
            except (ParseError, Anomaly, KeyError, ValueError, IndexError, TypeError, RecursionError) as ex:
                pfail += 1
                try:
                    rules = parse_rules((row.get("card") or "") + "\n" + (row.get("instructions") or ""))
                except Exception:
                    rules = Rules()
                res["parse_failures"].append({"id": row["id"], "file": os.path.basename(fp),
                                              "sampler": row["meta"]["sampler"], "kind": type(ex).__name__,
                                              "reason": str(ex)[:80], "gold": row["gold"],
                                              "spec_item": spec_items(row, rules, None, None, None)})
                continue
            if notes:
                res["anomalies"].append({"id": row["id"], "file": os.path.basename(fp),
                                         "sampler": row["meta"]["sampler"], "notes": sorted(set(notes))})
                for x in set(notes):
                    res["anomaly_counts"][x] = res["anomaly_counts"].get(x, 0) + 1
            if ans == row["gold"]:
                agree += 1
            else:
                mism += 1
                res["mismatches"].append({"id": row["id"], "file": os.path.basename(fp),
                                          "sampler": row["meta"]["sampler"], "qtype": row["qtype"],
                                          "gold": row["gold"], "solver_b": ans,
                                          "spec_item": spec_items(row, rules, facts, query, form)})
        res["files"][os.path.basename(fp)] = {"rows": n, "agree": agree, "mismatch": mism, "parse_fail": pfail}
        if log:
            log(f"{os.path.basename(fp)} rows={n} agree={agree} mismatch={mism} parse_fail={pfail}")
    tot = sum(v["rows"] for v in res["files"].values())
    ag = sum(v["agree"] for v in res["files"].values())
    res["total"] = {"rows": tot, "agree": ag, "agree_pct": round(100.0 * ag / tot, 3) if tot else 0.0,
                    "mismatch": len(res["mismatches"]), "parse_fail": len(res["parse_failures"]),
                    "rows_with_anomaly": len(res["anomalies"])}
    if with_sensitivity:
        res["sensitivity"] = sensitivity(allrows)
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    import argparse
    import time
    ap = argparse.ArgumentParser()
    out_dir = os.path.join(LEAN, "c_src", "F3", "out")
    ap.add_argument("--files", default=",".join(os.path.join(out_dir, f) for f in
                                                ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl")))
    ap.add_argument("--out", default=os.path.join(HERE, "mismatch.json"))
    ap.add_argument("--sensitivity", action="store_true")
    ap.add_argument("--progress", default=os.path.join(LEAN, "c_build", "progress_phase2.log"))
    a = ap.parse_args()
    sys.setrecursionlimit(20000)

    def log(msg):
        print(msg, flush=True)
        if a.progress:
            with open(a.progress, "a") as f:
                f.write("[F3] " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " solverB " + msg + "\n")
    r = run(a.files.split(","), a.out, log=log, with_sensitivity=a.sensitivity)
    log("total " + json.dumps(r["total"]) + (" sensitivity=" + json.dumps(
        {k: v["labels_moved"] for k, v in r.get("sensitivity", {}).items()}) if a.sensitivity else ""))
