"""Solver B (F13) container flattener.

Written from the F13 G0 spec (sections 2.1, 7) and the observed row format only; shares no code with the
generator. Turns any rendered document container (markdown, plain text, bold headings, HTML, JSON, YAML,
fenced or not) into an ordered list of sections. Each section: heading text, ordered elements:
  ('L', text)                         an item line (bullet, list item, JSON/YAML string)
  ('K', key, value)                   a key/value line (record field, mark line without a period)
  ('T', caption, header, rows)        a table (header: list of column names; rows: list of lists)
  ('C', caption)                      a caption line (record or table caption) with no table after it
"""
import json
import re
import textwrap
from html.parser import HTMLParser

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

CAPTION_RE = re.compile(r"^(?:Part \d+ of table \S+.*|Table \S+.*|.*\brecord [A-Z0-9][A-Z0-9-]*\d[A-Z0-9-]*.*|.*\brecord [A-Z0-9]+-[A-Z0-9]+)$")
BULLET_RE = re.compile(r"^\s*(?:[-*•▪–+]|\d+[.)]|[a-z][.)])\s+(.*)$")


class Section:
    __slots__ = ("heading", "els", "idx", "unit", "status", "meeting", "period")

    def __init__(self, heading, idx):
        self.heading = heading
        self.els = []
        self.idx = idx

    def lines(self):
        return [e[1] for e in self.els if e[0] == 'L']

    def __repr__(self):
        return "Section(%r, %d els)" % (self.heading, len(self.els))


def _unq(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        inner = s[1:-1]
        if s[0] == '"':
            try:
                return json.loads(s)
            except Exception:
                return inner.replace('\\"', '"')
        return inner.replace("''", "'")
    return s


def strip_fence(text):
    t = text.strip('\n')
    lines = t.split('\n')
    if lines and lines[0].strip().startswith('```'):
        lines = lines[1:]
        while lines and not lines[-1].strip():
            lines.pop()
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
    return '\n'.join(lines)


# ---------------------------------------------------------------- structured (JSON / YAML)
def _is_caption_key(k):
    if CAPTION_RE.match(k.strip()):
        return True
    n = re.sub(r"[^a-z0-9]+", " ", k.lower()).strip()
    return bool(re.search(r"\brecord [a-z0-9]+ [a-z0-9]+$", n) or re.match(r"^(part \d+ of )?table [a-z0-9]+( continued)?$", n))


def _walk_value(sec, key, val, out, heading_level):
    """Add the content of `val` (under key `key`) to section `sec`."""
    if isinstance(val, str) or isinstance(val, (int, float)) or val is None:
        sec.els.append(('K', key, '' if val is None else str(val)))
        return
    if isinstance(val, list):
        if val and all(isinstance(x, dict) for x in val):
            header = []
            for x in val:
                for k in x:
                    if k not in header:
                        header.append(k)
            rows = [[('' if x.get(h) is None else str(x.get(h))) for h in header] for x in val]
            sec.els.append(('T', key, header, rows))
            return
        for x in val:
            if isinstance(x, (str, int, float)):
                sec.els.append(('L', str(x)))
            elif isinstance(x, dict):
                # a list item that is a mapping: treat each pair as k/v, or nested
                for k2, v2 in x.items():
                    if isinstance(v2, (str, int, float)) or v2 is None:
                        sec.els.append(('K', str(k2), '' if v2 is None else str(v2)))
                    else:
                        _walk_value(sec, str(k2), v2, out, heading_level + 1)
            elif isinstance(x, list):
                _walk_value(sec, key, x, out, heading_level + 1)
        return
    if isinstance(val, dict):
        # a record (caption key, flat dict of scalars) or nested content
        if key is not None and all(isinstance(v, (str, int, float)) or v is None for v in val.values()) and \
                _is_caption_key(key):
            sec.els.append(('T', key, ['Field', 'Value'],
                            [[str(k), '' if v is None else str(v)] for k, v in val.items()]))
            return
        for k2, v2 in val.items():
            k2s = str(k2)
            if isinstance(v2, list) and v2 and all(isinstance(x, dict) for x in v2):
                _walk_value(sec, k2s, v2, out, heading_level + 1)
            elif isinstance(v2, list):
                if k2s.lower() in ('points', 'items', 'lines', 'notes', 'entries', 'content', 'body', 'text',
                                    'bullets', 'facts', 'list'):
                    _walk_value(sec, k2s, v2, out, heading_level + 1)
                elif _is_caption_key(k2s):
                    sec.els.append(('C', k2s))
                    _walk_value(sec, k2s, v2, out, heading_level + 1)
                else:
                    _walk_value(sec, k2s, v2, out, heading_level + 1)
            elif isinstance(v2, dict):
                if _is_caption_key(k2s) and all(isinstance(v, (str, int, float)) or v is None for v in v2.values()):
                    sec.els.append(('T', k2s, ['Field', 'Value'],
                                    [[str(k), '' if v is None else str(v)] for k, v in v2.items()]))
                else:
                    _walk_value(sec, k2s, v2, out, heading_level + 1)
            else:
                if k2s.lower() in ('heading', 'title', 'name', 'section', 'id') and sec.heading is None:
                    sec.heading = str(v2)
                else:
                    sec.els.append(('K', k2s, '' if v2 is None else str(v2)))


def flatten_struct(obj):
    secs = []
    if isinstance(obj, dict) and len(obj) == 1 and isinstance(next(iter(obj.values())), (dict, list)) and \
            not isinstance(next(iter(obj.values())), str):
        k0 = next(iter(obj))
        if str(k0).lower() in ('document', 'doc', 'report', 'manual', 'file', 'root'):
            obj = obj[k0]
    if isinstance(obj, dict):
        items = list(obj.items())
    elif isinstance(obj, list):
        items = [(None, x) for x in obj]
    else:
        return secs
    for k, v in items:
        if k is not None and str(k).lower() in ('name', 'title', 'document', 'heading') and isinstance(v, str):
            continue
        if k is not None and str(k).lower() == 'sections' and isinstance(v, list):
            for x in v:
                sec = Section(None, len(secs))
                secs.append(sec)
                if isinstance(x, dict):
                    _walk_value(sec, None, x, secs, 1)
                else:
                    _walk_value(sec, None, x, secs, 1)
            continue
        sec = Section(None if k is None else str(k), len(secs))
        secs.append(sec)
        _walk_value(sec, None if k is None else str(k), v, secs, 1)
    return secs


# ---------------------------------------------------------------- HTML
class _HP(HTMLParser):
    BLOCK = {'li', 'p', 'pre', 'caption', 'figcaption', 'blockquote'}
    HEAD = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.toks = []      # ('H', text) ('L', text) ('T', rows[list of (cells, is_th list)]) ('S',) section start
        self.buf = None
        self.mode = None
        self.table = None
        self.row = None
        self.cell = None
        self.cell_th = False
        self.depth_sec = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('section', 'article'):
            self._flush()
            self.toks.append(('S',))
        elif tag in self.HEAD:
            self._flush()
            self.buf = []
            self.mode = 'H'
        elif tag == 'table':
            self._flush()
            self.table = []
        elif tag == 'tr' and self.table is not None:
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []
            self.cell_th = (tag == 'th')
        elif tag in ('dt', 'dd') and self.table is None:
            self._flush()
            self.buf = []
            self.mode = tag.upper()
        elif tag in self.BLOCK and self.table is None:
            self._flush()
            self.buf = []
            self.mode = 'L'
        elif tag == 'br' and self.buf is not None:
            self.buf.append('\n')

    def handle_endtag(self, tag):
        if tag in self.HEAD and self.mode == 'H':
            self._flush()
        elif tag in ('td', 'th') and self.cell is not None:
            self.row.append((''.join(self.cell).strip(), self.cell_th))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == 'table' and self.table is not None:
            self.toks.append(('T', self.table))
            self.table = None
        elif tag in self.BLOCK and self.mode == 'L':
            self._flush()
        elif tag in ('dt', 'dd') and self.mode == tag.upper():
            self._flush()

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
        elif self.buf is not None:
            self.buf.append(data)
        elif data.strip() and self.table is None:
            # bare text: treat as a line
            self.toks.append(('L', data.strip()))

    def _flush(self):
        if self.buf is not None:
            t = re.sub(r'\s+', ' ', ''.join(self.buf)).strip()
            if t:
                if self.mode == 'DT':
                    self.toks.append(('DT', t))
                elif self.mode == 'DD':
                    if self.toks and self.toks[-1][0] == 'DT':
                        k = self.toks.pop()[1]
                        self.toks.append(('K', k, t))
                    else:
                        self.toks.append(('L', t))
                else:
                    self.toks.append((self.mode, t))
        self.buf = None
        self.mode = None


def flatten_html(text):
    p = _HP()
    p.feed(text)
    p.close()
    p._flush()
    toks = p.toks
    has_sec = any(t[0] == 'S' for t in toks)
    secs = []
    cur = None
    first_h_done = False
    i = 0
    pending_caption = None
    while i < len(toks):
        t = toks[i]
        if t[0] == 'S':
            cur = Section(None, len(secs))
            secs.append(cur)
            i += 1
            continue
        if t[0] == 'H':
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            is_cap = CAPTION_RE.match(t[1]) is not None or (nxt is not None and nxt[0] == 'T')
            if cur is not None and (is_cap or (has_sec and cur.heading is not None and nxt is not None and nxt[0] == 'T')):
                if nxt is not None and nxt[0] == 'T':
                    pending_caption = t[1]
                else:
                    cur.els.append(('C', t[1]))
                i += 1
                continue
            if has_sec:
                if cur is None:
                    # document title before the first section
                    i += 1
                    continue
                if cur.heading is None:
                    cur.heading = t[1]
                else:
                    cur.els.append(('C', t[1]))
            else:
                if not first_h_done and not secs:
                    first_h_done = True
                    # title: skip
                    i += 1
                    continue
                cur = Section(t[1], len(secs))
                secs.append(cur)
            i += 1
            continue
        if cur is None:
            cur = Section(None, len(secs))
            secs.append(cur)
        if t[0] == 'L':
            _add_line(cur, t[1])
        elif t[0] == 'K':
            cur.els.append(('K', t[1], t[2]))
        elif t[0] == 'DT':
            cur.els.append(('L', t[1]))
        elif t[0] == 'T':
            rows = t[1]
            cap = pending_caption
            pending_caption = None
            _add_html_table(cur, cap, rows)
        i += 1
    return [s for s in secs if s.els or s.heading]


def _add_html_table(sec, cap, rows):
    if not rows:
        return
    # vertical record table: every row is [th, td]
    if all(len(r) == 2 and r[0][1] and not r[1][1] for r in rows):
        sec.els.append(('T', cap, ['Field', 'Value'], [[r[0][0], r[1][0]] for r in rows]))
        return
    header = None
    body = rows
    if rows and all(c[1] for c in rows[0]):
        header = [c[0] for c in rows[0]]
        body = rows[1:]
    elif rows:
        header = [c[0] for c in rows[0]]
        body = rows[1:]
    sec.els.append(('T', cap, header, [[c[0] for c in r] for r in body]))


def _add_line(sec, t):
    sec.els.append(('L', t))


# ---------------------------------------------------------------- line-based text
KV_RE = re.compile(r"^([^:|]{1,80}?):\s+(.*\S)\s*$")


def _split_fixed(line, cuts):
    cells = []
    for j, c in enumerate(cuts):
        e = cuts[j + 1] if j + 1 < len(cuts) else None
        cells.append(line[c:e].strip() if e is not None else line[c:].strip())
    return cells


def _fixed_cuts(header):
    # column starts: position 0 and every position after a run of >= 2 spaces
    cuts = [0]
    for m in re.finditer(r" {2,}(?=\S)", header):
        cuts.append(m.end())
    return cuts


def _heading_text(t):
    t = t.strip()
    t = re.sub(r"^#+\s*", "", t)
    t = re.sub(r"\s*#+$", "", t)
    if t.startswith('**') and t.endswith('**') and len(t) > 4:
        t = t[2:-2]
    m = re.match(r"^=+\s*(.*?)\s*=+$", t)
    if m:
        t = m.group(1)
    m = re.match(r"^\[(.*)\]$", t)
    if m:
        t = m.group(1)
    m = re.match(r"^\d+\.\s+(.*)$", t)
    if m:
        t = m.group(1)
    if t.endswith(':'):
        t = t[:-1]
    return t.strip()


def flatten_lines(text):
    lines = text.split('\n')
    n = len(lines)
    secs = []
    cur = None
    title_seen = False
    i = 0
    in_record = False

    def new_sec(h):
        nonlocal cur
        cur = Section(h, len(secs))
        secs.append(cur)

    ind = []
    for x in lines:
        mm = BULLET_RE.match(x)
        if mm and x.strip():
            ind.append((len(x) - len(x.lstrip()), x.strip().endswith('.')))
    nested_top = None
    if ind:
        levels = sorted(set(a for a, _ in ind))
        if len(levels) >= 2:
            top = levels[0]
            tops = [b for a, b in ind if a == top]
            if tops and sum(tops) <= 0.1 * len(tops):
                nested_top = top
    while i < n:
        raw = lines[i]
        t = raw.strip()
        if not t:
            in_record = False
            i += 1
            continue
        if re.match(r"^[=\-~_*]{3,}$", t):
            i += 1
            continue
        # pipe table (grid borders '+---+' allowed)
        if (t.startswith('|') and t.endswith('|')) or (re.match(r"^\+[-=+]+\+$", t) and i + 1 < n and
                                                        lines[i + 1].strip().startswith('|')):
            block = []
            while i < n and (lines[i].strip().startswith('|') or re.match(r"^\+[-=+]+\+$", lines[i].strip())):
                if lines[i].strip().startswith('|'):
                    block.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in b.strip('|').split('|')] for b in block]
            rows = [r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r if c)]
            cap = None
            if cur is not None and cur.els and cur.els[-1][0] == 'C':
                cap = cur.els.pop()[1]
            if cur is None:
                new_sec(None)
            if rows:
                cur.els.append(('T', cap, rows[0], rows[1:]))
            in_record = False
            continue
        m = BULLET_RE.match(raw)
        if m and nested_top is not None and (len(raw) - len(raw.lstrip())) == nested_top and \
                not m.group(1).strip().endswith('.'):
            new_sec(_heading_text(m.group(1)))
            in_record = False
            i += 1
            continue
        is_numbered_heading = False
        if m and re.match(r"^\s*\d+[.)]\s", raw):
            body = m.group(1).strip()
            # numbered heading: no final period, not a k/v line, followed by a bullet/blank/caption
            if not body.endswith('.') and not KV_RE.match(body) and not body.startswith('"'):
                is_numbered_heading = True
        if m and not is_numbered_heading:
            body = _unq(m.group(1))
            if cur is None:
                new_sec(None)
            km = KV_RE.match(body)
            if km and not body.endswith('.') and '|' not in body:
                cur.els.append(('K', km.group(1).strip(), _unq(km.group(2))))
            else:
                # a bulleted caption ("- Event alcohol permit file" style) is a heading-like caption
                if CAPTION_RE.match(body) and not body.endswith('.'):
                    cur.els.append(('C', body))
                    in_record = True
                elif not body.endswith('.') and not km and raw[:1] in '-*' and i + 1 < n and \
                        re.match(r"^\s{2,}\S", lines[i + 1]) and not BULLET_RE.match(lines[i + 1].strip() and lines[i + 1] or 'x'):
                    new_sec(_heading_text(body))
                else:
                    cur.els.append(('L', body))
            i += 1
            continue
        # quoted line (YAML-ish leftovers)
        if t.startswith('"') and t.endswith('"'):
            if cur is None:
                new_sec(None)
            cur.els.append(('L', _unq(t)))
            i += 1
            continue
        # bare pipe table ("a | b | c" lines, no outer pipes)
        if t.count(' | ') >= 1 and i + 1 < n and lines[i + 1].strip().count('|') == t.count('|'):
            npipe = t.count('|')
            block = []
            while i < n and lines[i].strip() and lines[i].strip().count('|') == npipe:
                block.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in b.split('|')] for b in block]
            rows = [r for r in rows if not all(re.match(r"^:?[-=]{2,}:?$", c) for c in r if c)]
            cap = None
            if cur is not None and cur.els and cur.els[-1][0] == 'C':
                cap = cur.els.pop()[1]
            if cur is None:
                new_sec(None)
            if rows:
                cur.els.append(('T', cap, rows[0], rows[1:]))
            in_record = False
            continue
        # fixed-width table: this line and next line both have >= 2 runs of 2+ spaces
        if re.search(r"\S {2,}\S", t) and i + 1 < n and re.search(r"\S {2,}\S", lines[i + 1].strip()):
            header_line = raw.rstrip()
            cuts = _fixed_cuts(header_line)
            header = _split_fixed(header_line, cuts)
            rows = []
            i += 1
            while i < n and lines[i].strip() and not re.match(r"^[=\-]{3,}$", lines[i].strip()):
                if re.match(r"^[-\s]+$", lines[i]):
                    i += 1
                    continue
                rr = _split_fixed(lines[i].rstrip(), cuts)
                if not all(re.match(r"^[-=+]*$", c) for c in rr):
                    rows.append(rr)
                i += 1
            cap = None
            if cur is not None and cur.els and cur.els[-1][0] == 'C':
                cap = cur.els.pop()[1]
            if cur is None:
                new_sec(None)
            cur.els.append(('T', cap, header, rows))
            in_record = False
            continue
        km = KV_RE.match(t)
        if in_record and km:
            cur.els.append(('K', km.group(1).strip(), _unq(km.group(2))))
            i += 1
            continue
        hb = _heading_text(t)
        if CAPTION_RE.match(hb) and cur is not None:
            cur.els.append(('C', hb))
            in_record = True
            i += 1
            continue
        if km and not t.endswith(':') and cur is not None and cur.els and not t.startswith('#') and \
                not re.match(r"^(Chapter|Annex|Part|Section|Appendix)\b", t) and \
                (cur.els[-1][0] in ('K',) ):
            cur.els.append(('K', km.group(1).strip(), _unq(km.group(2))))
            i += 1
            continue
        # heading
        if not title_seen and not secs:
            title_seen = True
            # the first non-empty line(s) before any section is the document title / memo header
            if i + 1 < n and lines[i + 1].strip() and not BULLET_RE.match(lines[i + 1]) and \
                    not re.match(r"^[=\-]{3,}$", lines[i + 1].strip()):
                # two-line memo header ("Quick memo" + title): skip both
                i += 2
                continue
            i += 1
            continue
        new_sec(hb)
        in_record = False
        i += 1
    return secs


def looks_yaml(t):
    lines = [x for x in t.split('\n') if x.strip()]
    if not lines:
        return False
    top = [x for x in lines if not x.startswith(' ') and not x.startswith('-')]
    if not top:
        return False
    k = sum(1 for x in top if re.match(r"^[^\s#][^:]*:(\s|$)", x) or x.startswith('#'))
    return k == len(top) and any(re.match(r"^\s+- ", x) or re.match(r"^- ", x) for x in lines)


def flatten(text):
    t = textwrap.dedent(strip_fence(text))
    s = t.lstrip()
    if s.startswith('{') or s.startswith('['):
        try:
            return flatten_struct(json.loads(s))
        except Exception:
            if yaml is not None:
                try:
                    return flatten_struct(yaml.safe_load(s))
                except Exception:
                    pass
    if s.startswith('<'):
        return flatten_html(s)
    if yaml is not None and looks_yaml(t):
        try:
            obj = yaml.safe_load(t)
            if isinstance(obj, (dict, list)):
                return flatten_struct(obj)
        except Exception:
            pass
    return flatten_lines(t)
