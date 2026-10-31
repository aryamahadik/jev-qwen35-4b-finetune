"""Parser front end: turn a rendered `state` (any fmt1 container) into ordered text lines and tables.

Written from the container formats as they appear on the page (JSON / YAML objects, HTML, markdown, aligned or pipe
tables, prose), never from the renderer's code. Lines keep the exact strings; tables keep header + cell rows.
"""
from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser

import yaml

FENCE = re.compile(r"^\s*(```|~~~)")


def _dedent(text: str) -> str:
    lines = text.split("\n")
    ind = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    m = min(ind) if ind else 0
    return "\n".join(l[m:] for l in lines)


def strip_fence(text: str) -> str:
    out = [l for l in text.split("\n") if not FENCE.match(l)]
    return _dedent("\n".join(out)).strip("\n")


def _walk(o, lines, tables):
    if isinstance(o, dict):
        for k, v in o.items():
            lines.append(str(k))
            _walk(v, lines, tables)
    elif isinstance(o, list):
        if o and all(isinstance(x, dict) for x in o):
            cols = list(o[0].keys())
            if all(list(x.keys()) == cols for x in o):
                tables.append({"columns": [str(c) for c in cols], "rows": [[str(x[c]) for c in cols] for x in o]})
                for x in o:
                    lines.append(" | ".join(str(x[c]) for c in cols))
                return
        if o and all(isinstance(x, list) for x in o):
            tables.append({"columns": [str(c) for c in o[0]], "rows": [[str(c) for c in r] for r in o[1:]]})
        for x in o:
            _walk(x, lines, tables)
    elif o is None:
        lines.append("null")
    elif isinstance(o, bool):
        lines.append("true" if o else "false")
    else:
        lines.append(str(o))


class _H(HTMLParser):
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section", "ul", "ol", "table", "tr", "dt", "dd",
             "dl", "br", "article", "header", "footer", "blockquote", "pre", "caption", "thead", "tbody"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.cur = []
        self.tables = []
        self.tab = None
        self.row = None
        self.cell = None

    def flush(self):
        t = "".join(self.cur).strip()
        if t:
            self.lines.append(" ".join(t.split()))
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.flush()
            self.tab = {"columns": None, "rows": []}
        elif tag == "tr" and self.tab is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        if tag in self.BLOCK:
            self.flush()

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.row is not None and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.tab is not None and self.row is not None:
            if self.tab["columns"] is None:
                self.tab["columns"] = self.row
            else:
                self.tab["rows"].append(self.row)
            self.lines.append(" | ".join(self.row))
            self.row = None
            self.cur = []
        elif tag == "table" and self.tab is not None:
            if self.tab["columns"]:
                self.tables.append(self.tab)
            self.tab = None
        if tag in self.BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
        if self.row is None:
            self.cur.append(data)


def _md_tables(lines):
    tables = []
    i = 0
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith("|") and l.endswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(("|", "+")):
                block.append(lines[i].strip())
                i += 1
            rows = []
            for b in block:
                if b.startswith("+") or re.fullmatch(r"\|[\s\-:=|+]+\|", b):
                    continue
                rows.append([c.strip() for c in b.strip("|").split("|")])
            if rows:
                tables.append({"columns": rows[0], "rows": rows[1:]})
            continue
        i += 1
    return tables


def _aligned_tables(lines):
    """Aligned text tables: a header line followed by a rule line of '=' / '-' runs separated by spaces."""
    tables = []
    for i in range(1, len(lines)):
        rule = lines[i]
        if re.fullmatch(r"\s*[=\-]{2,}(\s+[=\-]{2,})+\s*", rule):
            spans = [(m.start(), m.end()) for m in re.finditer(r"[=\-]+", rule)]
            head = lines[i - 1]

            def cut(s):
                out = []
                for j, (a, b) in enumerate(spans):
                    end = spans[j + 1][0] if j + 1 < len(spans) else len(s) + 1
                    out.append(s[a:end].strip())
                return out
            rows = []
            k = i + 1
            while k < len(lines) and lines[k].strip():
                rows.append(cut(lines[k]))
                k += 1
            tables.append({"columns": cut(head), "rows": rows})
    return tables


def _pipe_text_tables(lines):
    """'a | b | c' lines (memo pipe tables) with no leading bar."""
    tables = []
    i = 0
    while i < len(lines):
        if " | " in lines[i] and not lines[i].strip().startswith("|"):
            block = []
            while i < len(lines) and " | " in lines[i] and not lines[i].strip().startswith("|"):
                block.append([c.strip() for c in lines[i].split(" | ")])
                i += 1
            if len(block) >= 2 and len({len(r) for r in block}) == 1:
                tables.append({"columns": block[0], "rows": block[1:]})
            continue
        i += 1
    return tables


def decode(state: str):
    """(kind, lines, tables). kind: json | yaml | html | text."""
    body = strip_fence(state)
    s = body.strip()
    if s.startswith("{") or s.startswith("["):
        try:
            o = json.loads(s)
            lines, tables = [], []
            _walk(o, lines, tables)
            return "json", lines, tables
        except json.JSONDecodeError:
            pass
    if re.search(r"<(section|ul|p|table|div|h[1-6]|dl|article|ol)\b", s):
        h = _H()
        h.feed(s)
        h.flush()
        return "html", h.lines, h.tables
    try:
        o = yaml.safe_load(s)
        if isinstance(o, dict) and len(o) >= 2 and any(isinstance(v, (list, dict)) for v in o.values()):
            lines, tables = [], []
            _walk(o, lines, tables)
            return "yaml", lines, tables
    except yaml.YAMLError:
        pass
    raw = state.split("\n")
    lines = [l.rstrip() for l in raw]
    tables = _md_tables(lines) + _aligned_tables(lines) + _pipe_text_tables(lines)
    return "text", lines, tables


def norm(s: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    return " ".join(re.findall(r"[a-z0-9]+", s.lower()))
