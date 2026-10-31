"""Read a rendered `state` back into (label, value) pairs and tables, per container, from the skin data of the
formats-1 pool (data/skins.jsonl, styles.jsonl, containers.jsonl, fences.jsonl, registers.jsonl). Written from the
skin specification (params), never from the renderer code (3.3).

Output: Doc(pairs=[(key, value_text)], tables=[(columns, rows)], lines_used=set(line numbers), unparsed=[lines]).
Keys are normalised by norm_key (lower-case words; snake, camel and as-given keys compare equal).
"""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from html.parser import HTMLParser

import yaml

from .common import FMT1, read_jsonl


@lru_cache(maxsize=None)
def _idx(name, key="id"):
    return {o[key]: o for o in read_jsonl(FMT1 / "data" / name)}


def style(sid):
    return _idx("styles.jsonl")[sid]


def skin(kid):
    return _idx("skins.jsonl")[kid]


def fence(fid):
    return _idx("fences.jsonl")[fid]


@lru_cache(maxsize=None)
def register(name):
    for o in read_jsonl(FMT1 / "data" / "registers.jsonl"):
        if o["name"] == name or o["id"] == name:
            return o
    raise KeyError(name)


def norm_key(s: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(s))
    return " ".join(w.lower() for w in re.findall(r"[A-Za-z0-9]+", s))


@dataclass
class Doc:
    pairs: list = field(default_factory=list)
    tables: list = field(default_factory=list)
    texts: list = field(default_factory=list)      # free text items (paragraphs, list items)
    title: str | None = None

    def get(self, label):
        k = norm_key(label)
        hits = [v for kk, v in self.pairs if norm_key(kk) == k]
        if len(hits) > 1 and len(set(hits)) > 1:
            raise ParseError(f"two values for {label!r}")
        return hits[0] if hits else None

    def keys(self):
        return [norm_key(k) for k, _ in self.pairs]


class ParseError(ValueError):
    pass


# ----------------------------------------------------------------------------------------------------------------- fences

def unfence(text, st):
    """Strip the style's fence (and the title line a fence puts above a fenced body). Returns (title, body)."""
    f = fence(st["fence"])
    title = None
    body = text
    if f["name"] == "none":
        return None, body
    if f["name"] == "indent4":
        lines = body.split("\n")
        idx = next((i for i, ln in enumerate(lines) if ln.startswith("    ")), None)
        if idx is not None and idx >= 2 and lines[idx - 1] == "":
            title = "\n".join(lines[:idx - 1])
            lines = lines[idx:]
        body = "\n".join(ln[4:] if ln.startswith("    ") else ln for ln in lines)
        return title, body
    op = f["open"].split("{lang}")[0]
    lines = body.split("\n")
    idx = next((i for i, ln in enumerate(lines) if ln.startswith(op)), None)
    if idx is None:
        raise ParseError("fence not found")
    if idx >= 2:
        title = "\n".join(lines[:idx - 1])
    close = f["close"]
    end = max(i for i, ln in enumerate(lines) if ln == close)
    return title, "\n".join(lines[idx + 1:end])


# ----------------------------------------------------------------------------------------------------------------- structured

def _walk_obj(o, doc: Doc, key=None):
    if isinstance(o, dict):
        if all(not isinstance(v, (dict, list)) for v in o.values()) and key is not None and key.startswith("__row"):
            return
        for k, v in o.items():
            if isinstance(v, dict):
                _walk_obj(v, doc, k)
            elif isinstance(v, list):
                if v and all(isinstance(x, dict) for x in v):
                    cols = []
                    for x in v:
                        for c in x:
                            if c not in cols:
                                cols.append(c)
                    doc.tables.append((cols, [[("" if x.get(c) is None else _sv(x.get(c))) for c in cols] for x in v],
                                       k))
                else:
                    doc.texts.extend(_sv(x) for x in v)
            else:
                doc.pairs.append((k, _sv(v)))
    elif isinstance(o, list):
        if o and all(isinstance(x, dict) for x in o):
            cols = []
            for x in o:
                for c in x:
                    if c not in cols:
                        cols.append(c)
            doc.tables.append((cols, [[_sv(x.get(c)) for c in cols] for x in o], None))


def _sv(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, float):
        return repr(v)
    return str(v)


def parse_json(body, sk):
    p = sk["params"]
    doc = Doc()
    if p["layout"] == "lines":
        rows = [json.loads(ln) for ln in body.split("\n") if ln.strip()]
        _walk_obj(rows, doc)
        return doc
    _walk_obj(json.loads(body), doc)
    return doc


def parse_yaml(body, sk):
    doc = Doc()
    lines = body.split("\n")
    if lines and lines[0].startswith("# "):
        doc.title = lines[0][2:]
        body = "\n".join(lines[1:])
    _walk_obj(yaml.safe_load(body), doc)
    return doc


def _fields_or_table(cols, rows, sk, doc):
    voc = sk.get("vocab") or {}
    if [norm_key(c) for c in cols] == [norm_key(voc.get("field", "field")), norm_key(voc.get("value", "value"))]:
        for r in rows:
            doc.pairs.append((r[0], r[1]))
    else:
        doc.tables.append((cols, rows, None))


def parse_csv(body, sk, title):
    p = sk["params"]
    parts = body.split("\n\n", 1)
    if title is None and len(parts) == 2 and "\n" not in parts[0] and (p["fixed"] or p["delim"] not in parts[0]):
        title, body = parts[0], parts[1]
    doc = Doc(title=title)
    if p["fixed"]:
        lines = [ln for ln in body.split("\n") if ln.strip()]
        head = re.split(r" {2,}", lines[0].strip())
        rows = []
        # columns by the header's start offsets
        starts = [m.start() for m in re.finditer(r"(?:(?<= {2})|^)\S", lines[0])]
        for ln in lines[1:]:
            cells = []
            for i, s in enumerate(starts):
                e = starts[i + 1] if i + 1 < len(starts) else None
                cells.append((ln[s:e] if e else ln[s:]).strip())
            rows.append(cells)
        _fields_or_table(head, rows, sk, doc)
        return doc
    r = list(csv.reader(io.StringIO(body), delimiter=p["delim"]))
    _fields_or_table(r[0], r[1:], sk, doc)
    return doc


class _HP(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.cur, self.cell, self.dts, self.in_cell, self.texts = [], None, [], [], None, []
        self.pairs = []
        self.tables = []
        self.tab = None
        self.dl_key = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tab = []
        elif tag == "tr":
            self.cur = []
        elif tag in ("td", "th", "dt", "dd", "p", "li", "h1", "h2", "h3", "h4", "caption"):
            self.in_cell = tag
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cur is not None:
            self.cur.append(("".join(self.cell), tag))
            self.in_cell = None
        elif tag == "tr" and self.tab is not None:
            self.tab.append(self.cur)
            self.cur = None
        elif tag == "table":
            self.tables.append(self.tab)
            self.tab = None
        elif tag == "dt":
            self.dl_key = "".join(self.cell)
            self.in_cell = None
        elif tag == "dd":
            self.pairs.append((self.dl_key, "".join(self.cell)))
            self.in_cell = None
        elif tag in ("p", "li", "h1", "h2", "h3", "h4", "caption"):
            self.texts.append("".join(self.cell))
            self.in_cell = None

    def handle_data(self, data):
        if self.in_cell:
            self.cell.append(data)


def parse_html(body, sk):
    hp = _HP()
    hp.feed(body)
    doc = Doc()
    doc.pairs.extend(hp.pairs)
    voc = sk.get("vocab") or {}
    for tab in hp.tables:
        if not tab:
            continue
        if tab and all(len(r) == 2 and r[0][1] == "th" and r[1][1] == "td" for r in tab):
            for r in tab:
                doc.pairs.append((r[0][0], r[1][0]))
            continue
        head = [c for c, t in tab[0]]
        rows = [[c for c, t in r] for r in tab[1:]]
        _fields_or_table(head, rows, sk, doc)
    doc.texts.extend(hp.texts)
    return doc


# ----------------------------------------------------------------------------------------------------------------- text

_MD_ROW = re.compile(r"^\|(.*)\|$")


def _text_tables(lines):
    """Find md / pipe / aligned / grid tables in plain-text lines. Returns (tables, used line numbers)."""
    tabs, used = [], set()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if _MD_ROW.match(ln.strip()) and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in _MD_ROW.match(ln.strip()).group(1).split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and _MD_ROW.match(lines[j].strip()):
                rows.append([c.strip() for c in _MD_ROW.match(lines[j].strip()).group(1).split("|")])
                j += 1
            tabs.append((head, rows, None))
            used.update(range(i, j))
            i = j
            continue
        if ln.startswith("+") and set(ln) <= set("+-") and i + 2 < len(lines):
            j = i
            block = []
            while j < len(lines) and (lines[j].startswith("+") or lines[j].startswith("|")):
                block.append(lines[j])
                j += 1
            data = [b for b in block if b.startswith("|")]
            if data:
                head = [c.strip() for c in data[0].strip("|").split("|")]
                rows = [[c.strip() for c in d.strip("|").split("|")] for d in data[1:]]
                tabs.append((head, rows, None))
                used.update(range(i, j))
                i = j
                continue
        if i + 1 < len(lines) and lines[i + 1].strip() and set(lines[i + 1].replace(" ", "")) == {"="} \
                and "  " in lines[i + 1]:
            rule = lines[i + 1]
            starts = [m.start() for m in re.finditer(r"=+", rule)]
            def cut(s):
                out = []
                for k, st in enumerate(starts):
                    e = starts[k + 1] if k + 1 < len(starts) else None
                    out.append((s[st:e] if e else s[st:]).strip())
                return out
            head = cut(ln)
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip():
                rows.append(cut(lines[j]))
                j += 1
            tabs.append((head, rows, None))
            used.update(range(i, j))
            i = j
            continue
        if " | " in ln and i + 1 < len(lines) and " | " in lines[i + 1] and ln.count("|") == lines[i + 1].count("|"):
            j = i
            block = []
            while j < len(lines) and " | " in lines[j] and lines[j].count("|") == ln.count("|"):
                block.append(lines[j])
                j += 1
            if len(block) >= 2:
                head = [c.strip() for c in block[0].split(" | ")]
                rows = [[c.strip() for c in b.split(" | ")] for b in block[1:]]
                tabs.append((head, rows, None))
                used.update(range(i, j))
                i = j
                continue
        i += 1
    return tabs, used


def _kv_line(ln, fmts):
    for rx in fmts:
        m = rx.match(ln)
        if m:
            return m.group("k").strip(), m.group("v").strip()
    return None


def _fmt_rx(fmt):
    """A regex from a skin's line or field format ({key}/{label}/{LABEL}/{key_l}, {value}, {dots}, {pad})."""
    out = []
    for p in re.split(r"(\{[A-Za-z_]+\})", fmt):
        if p in ("{key}", "{label}", "{LABEL}", "{key_l}"):
            out.append(r"(?P<k>.+?)")
        elif p == "{value}":
            out.append(r"(?P<v>.*\S)")
        elif p == "{dots}":
            out.append(r"\.{3,}")
        elif p == "{pad}":
            out.append(r" *")
        elif p == "{n}":
            out.append(r"\d+")
        else:
            out.append(re.escape(p))
    return re.compile("^" + "".join(out) + "$")


GENERIC_KV = [_fmt_rx("- {key}: {value}"), _fmt_rx("* {key}: {value}"), _fmt_rx("• {key}: {value}"),
              _fmt_rx("+ {key}: {value}"), _fmt_rx("{key}: {value}")]


def parse_text(body, st, sk, title):
    cont = st["container"]
    p = sk["params"]
    lines = body.split("\n")
    doc = Doc(title=title)
    tabs, used = _text_tables(lines)
    for cols, rows, cap in tabs:
        _fields_or_table(cols, rows, sk, doc)
    fmts = []
    if cont == "prose":
        ff = p["field_fmt"]
        fmts.append(_fmt_rx(ff.rstrip(".")))
        fmts.append(_fmt_rx(ff))
    elif cont == "key_value":
        fmts.append(_fmt_rx(p["line"]))
    elif cont == "memo":
        fmts.append(_fmt_rx(p["header_fmt"]))
        fmts.append(_fmt_rx(p["bullet"] + "{key}: {value}"))
    elif cont == "bullet_sop":
        fmts.append(_fmt_rx(p["bullet"] + "{key}: {value}"))
        fmts.append(_fmt_rx("  " + p["bullet"] + "{key}: {value}"))
    fmts += GENERIC_KV
    for i, ln in enumerate(lines):
        if i in used or not ln.strip():
            continue
        if cont == "prose" and p.get("list_mode") == "inline":
            parts = re.split(r"(?<=\.) (?=\S)", ln)
        else:
            parts = [ln]
        for part in parts:
            s = part.strip()
            if cont == "prose" and p.get("list_mode") == "numbered_paras":
                s = re.sub(r"^\d+\. ", "", s)
            kv = None
            for rx in fmts:
                m = rx.match(s)
                if m:
                    k, v = m.group("k").strip(), m.group("v").strip()
                    if cont == "prose" and v.endswith("."):
                        v = v[:-1]
                    kv = (k, v)
                    break
            if kv:
                doc.pairs.append(kv)
            else:
                doc.texts.append(s)
    return doc


def parse_state(state: str, sid: str) -> Doc:
    st = style(sid)
    sk = skin(st["skin"])
    cont = st["container"]
    title, body = unfence(state, st)
    if cont == "json":
        doc = parse_json(body, sk)
    elif cont == "yaml":
        doc = parse_yaml(body, sk)
    elif cont == "csv":
        doc = parse_csv(body, sk, title)
    elif cont == "html_snippet":
        doc = parse_html(body, sk)
    elif cont in ("prose", "memo", "bullet_sop", "key_value", "markdown_table", "email_thread", "form"):
        doc = parse_text(body, st, sk, title)
    else:
        raise ParseError(f"container {cont} is not an F2 container")
    return doc
