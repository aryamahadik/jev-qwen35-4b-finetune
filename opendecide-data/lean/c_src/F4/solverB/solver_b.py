#!/usr/bin/env python3
"""F4 independent solver B (written from G0_SPEC F4-G0-v7 sections 1, 2, 3, 4, 7, 9 and the row format only).

Paradigm: table-driven re-parse of the rendered row text into facts / rules / flags, then
  * OW (and short cards, labelled under OW): model enumeration (backtracking over the free
    atoms of the claim's clause-connected component; finite-domain region variables for
    missing values); FOLLOWS iff c true in all models, RULED_OUT iff false in all, else OPEN.
  * CW: Clark completion of the acyclic ground program, evaluated top-down (each atom is
    true iff it is a stated fact or one of its ground bodies holds; NAF for negative
    conditions and exceptions); negative-head rules and negative facts are constraints.
Values: integers scaled by 10^k (own comparator); dates: own parser -> day ordinals.
Never imports or reads generator (solver A) code or the sidecar.  Output JSON: agreement per file,
mismatches (id, file, gold, solver_b answer, form, world, spec item; no row text), parse notes, and
label-tag notes (rows whose meta L tag differs from solver B label of the asked claim).  Usage:
  solver_b.py OUT_JSON file1.jsonl [file2.jsonl ...]
"""
import sys, re, json, itertools, datetime, html.parser, csv, io, collections

ID_RE = r'[A-Z]{2}[-/][A-Z0-9]{5}'
ID_FULL = re.compile(r'^' + ID_RE + r'$')
ID_FIND = re.compile(r'(?<![A-Za-z0-9])' + ID_RE + r'(?![A-Za-z0-9])')
MONTHS = {m: i + 1 for i, m in enumerate(
    ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
     'september', 'october', 'november', 'december'])}
MON_RE = '(?:' + '|'.join(m.capitalize() for m in MONTHS) + ')'
DATE_RE = (r'(?:\d{4}-\d{2}-\d{2}|\d{1,2} ' + MON_RE + r' \d{4}|' + MON_RE + r' \d{1,2}, \d{4})')
NUM_RE = r'-?\d[\d,]*(?:\.\d+)?'


class ParseError(Exception):
    pass


ABLATE = set()   # diagnostic sensitivity runs only (--ablate); empty for the real check


# ---------------------------------------------------------------- values
def parse_date(s):
    s = s.strip()
    m = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r'(\d{1,2}) ([A-Za-z]+) (\d{4})', s)
        if m:
            d, mo, y = int(m.group(1)), MONTHS.get(m.group(2).lower()), int(m.group(3))
        else:
            m = re.fullmatch(r'([A-Za-z]+) (\d{1,2}), (\d{4})', s)
            if not m:
                return None
            mo, d, y = MONTHS.get(m.group(1).lower()), int(m.group(2)), int(m.group(3))
    if not mo:
        return None
    # own day-ordinal computation (proleptic Gregorian)
    return datetime.date(y, mo, d).toordinal()


def parse_num(s):
    """Return (scaled_int, scale) for a decimal string, or None."""
    s = s.strip().replace(',', '')
    m = re.fullmatch(r'(-?)(\d+)(?:\.(\d+))?', s)
    if not m:
        return None
    frac = m.group(3) or ''
    v = int(m.group(2) + frac) * (-1 if m.group(1) else 1)
    return (v, len(frac))


def num_cmp_pair(a, b):
    """Bring two (int, scale) numbers to one scale; return ints."""
    (va, sa), (vb, sb) = a, b
    k = max(sa, sb)
    return va * 10 ** (k - sa), vb * 10 ** (k - sb)


def parse_value(s):
    """A cell/fact value: ('date', ordinal) | ('num', (int, scale)) | None.  Strips units."""
    s = s.strip().strip('"').strip()
    if re.fullmatch(DATE_RE, s):
        return ('date', parse_date(s))
    m = re.fullmatch(r'(' + NUM_RE + r')\s*(?:%|[A-Za-z][A-Za-z \-]*)?', s)
    if m:
        n = parse_num(m.group(1))
        if n is not None:
            return ('num', n)
    return None


def norm_q(s):
    return re.sub(r'\s+', ' ', s.replace('_', ' ')).strip().lower()


def norm_src(s):
    s = s.strip().strip('*').strip().lower()
    s = re.sub(r'^the ', '', s)
    return re.sub(r'\s+', ' ', s)


# ---------------------------------------------------------------- containers
class _HTML2Lines(html.parser.HTMLParser):
    BLOCK = {'p', 'div', 'section', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br',
             'table', 'thead', 'tbody', 'article', 'header', 'footer', 'blockquote', 'pre', 'dl', 'dt', 'dd'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.cur, self.row, self.cell = [], [], None, None

    def _flush(self):
        t = ''.join(self.cur).strip()
        if t:
            self.out.append(t)
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self._flush(); self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []
        elif tag in self.BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.row is not None and self.cell is not None:
            self.row.append(''.join(self.cell).strip()); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.out.append('| ' + ' | '.join(self.row) + ' |'); self.row = None
        elif tag in self.BLOCK:
            self._flush()

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
        else:
            self.cur.append(data)


def html_to_text(s):
    p = _HTML2Lines()
    p.feed(s)
    p.close()
    p._flush()
    return '\n'.join(p.out)


def _json_walk(v, lines, tables, key=None):
    if isinstance(v, dict):
        idk = next((k for k in v if k.lower() == 'id' and isinstance(v[k], str) and ID_FULL.match(v[k].strip())), None)
        if idk is not None:
            hdr, row = [], []
            for k, x in v.items():
                hdr.append('ID' if k == idk else k)
                row.append(_json_cell(x))
            tables.append({'headers': hdr, 'rows': [row], 'src': 'json'})
            return
        for k, x in v.items():
            _json_walk(x, lines, tables, k)
    elif isinstance(v, list):
        for x in v:
            _json_walk(x, lines, tables, key)
    elif isinstance(v, str):
        for ln in v.split('\n'):
            lines.append(ln)


def _json_cell(x):
    if x is True:
        return 'Yes'
    if x is False:
        return 'No'
    if x is None:
        return 'not recorded'
    if isinstance(x, list):
        return ', '.join(str(i) for i in x)
    if isinstance(x, (int, float)):
        return str(x)
    return str(x)


def try_json(s):
    t = s.strip()
    t = re.sub(r'^```[A-Za-z]*\s*\n', '', t)
    t = re.sub(r'\n\s*```\s*$', '', t).strip()
    if not t or t[0] not in '{[':
        return None
    try:
        return json.loads(t)
    except Exception:
        return None


def _split_md_row(line):
    t = line.strip()
    if t.startswith('|'):
        t = t[1:]
    if t.endswith('|'):
        t = t[:-1]
    return [c.strip() for c in t.split('|')]


def _is_sep_row(cells):
    return all(re.fullmatch(r':?[-=]{2,}:?', c) or c == '' for c in cells) and any(c for c in cells)


YAML_ENTRY = re.compile(r'^(\s*)(-\s+)?(id|ID|Id)\s*:\s*"?(' + ID_RE + r')"?\s*$')
YAML_KV = re.compile(r'^(\s*)([A-Za-z_][\w \-/]*?)\s*:\s*(.*?)\s*$')


def _flow_map(body):
    parts = re.split(r',\s*(?=["\']?[A-Za-z_][\w \-/]*["\']?\s*:\s)', body)
    d = []
    for p in parts:
        m = re.match(r'^\s*["\']?([^:"\']+?)["\']?\s*:\s*(.*?)\s*$', p)
        if not m:
            return None
        d.append((m.group(1).strip(), m.group(2).strip().strip('"\'')))
    return d


def _yaml_cell(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        v = v[1:-1]
    lv = v.lower()
    if lv == 'true':
        return 'Yes'
    if lv == 'false':
        return 'No'
    if lv in ('null', '~'):
        return 'not recorded'
    if v.startswith('[') and v.endswith(']'):
        return ', '.join(x.strip().strip('"\'') for x in v[1:-1].split(','))
    return v


def extract(text):
    """Return (lines, tables) for a record or card text."""
    lines, tables = [], []
    js = try_json(text)
    if js is not None:
        _json_walk(js, lines, tables)
        return lines, tables
    if re.search(r'<(div|p|table|ul|ol|li|section|h\d|tr|br)\b', text):
        text = html_to_text(text)
    raw = text.split('\n')
    i, n = 0, len(raw)
    while i < n:
        ln = raw[i]
        s = ln.strip()
        if s.startswith('```') or re.fullmatch(r'\+[-=+:]+\+', s) or s == '':
            i += 1; continue
        # markdown / grid / html tables
        if (s.startswith('|') and s.endswith('|') and s.count('|') >= 3) or re.match(r'^(ID|id)\s*\|', s):
            block = []
            while i < n:
                t = raw[i].strip()
                if (t.startswith('|') and t.endswith('|')) or (t.count('|') >= 1 and (
                        re.match(r'^"?' + ID_RE + r'"?\s*\|', t) or re.fullmatch(r'[-:| ]+', t) or re.match(r'^(ID|id)\s*\|', t))):
                    block.append(_split_md_row(t))
                elif re.fullmatch(r'\+[-=+:]+\+', t):
                    pass
                else:
                    break
                i += 1
            block = [b for b in block if not _is_sep_row(b)]
            if block:
                tables.append({'headers': block[0], 'rows': block[1:], 'src': 'md'})
            continue
        # CSV
        mcsv = re.match(r'^"?(ID|id)"?\s*([,;])', s)
        if mcsv:
            dl = mcsv.group(2)
            hdr = next(csv.reader([s], delimiter=dl))
            rows = []
            i += 1
            while i < n and re.match(r'^\s*"?' + ID_RE + r'"?\s*' + dl, raw[i]):
                rows.append(next(csv.reader([raw[i].strip()], delimiter=dl)))
                i += 1
            tables.append({'headers': [h.strip() for h in hdr], 'rows': [[c.strip() for c in r] for r in rows], 'src': 'csv'})
            continue
        # TSV
        if re.match(r'^\s*(ID|id)\t', ln):
            hdr = [h.strip() for h in ln.strip().split('\t')]
            rows = []
            i += 1
            while i < n and re.match(r'^\s*' + ID_RE + r'\t', raw[i]):
                rows.append([c.strip() for c in raw[i].strip('\n').lstrip(' ').split('\t')])
                i += 1
            tables.append({'headers': hdr, 'rows': rows, 'src': 'tsv'})
            continue
        # fixed-width
        if re.match(r'^\s*(ID|id)(\s{2,}|\t)\S', ln):
            starts = [m.start() for m in re.finditer(r'\S+(?: \S+)*', ln.replace('\t', '    '))]
            hdrline = ln.replace('\t', '    ')
            hdr = [hdrline[a:b].strip() for a, b in zip(starts, starts[1:] + [None])]
            rows = []
            i += 1
            while i < n and (re.match(r'^\s*' + ID_RE + r'\b', raw[i]) or re.fullmatch(r'\s*[=\-+]{3,}[=\-+ ]*', raw[i])):
                if not re.match(r'^\s*' + ID_RE + r'\b', raw[i]):
                    i += 1; continue
                r = raw[i].replace('\t', '    ')
                rows.append([r[a:b].strip() if a < len(r) else '' for a, b in zip(starts, starts[1:] + [None])])
                i += 1
            tables.append({'headers': hdr, 'rows': rows, 'src': 'fixed'})
            continue
        # YAML flow mapping entry
        m = re.match(r'^\s*(?:-\s+)?\{(.*)\}\s*,?\s*$', s)
        if m and re.search(r'\b(id|ID)\s*:\s*["\']?' + ID_RE, m.group(1)):
            d = _flow_map(m.group(1))
            if d:
                tables.append({'headers': ['ID' if k.lower() == 'id' else k for k, _ in d],
                               'rows': [[_yaml_cell(v) for _, v in d]], 'src': 'yamlflow'})
                i += 1; continue
        # YAML block entry
        m = YAML_ENTRY.match(ln)
        if m:
            ind = len(m.group(1)) + (len(m.group(2)) if m.group(2) else 0)
            hdr, row = ['ID'], [m.group(4)]
            i += 1
            while i < n:
                t = raw[i]
                if t.strip() == '':
                    i += 1; continue
                mm = YAML_KV.match(t)
                if not mm or len(mm.group(1)) != ind or t.strip().startswith('-'):
                    break
                hdr.append(mm.group(2)); row.append(_yaml_cell(mm.group(3)))
                i += 1
            tables.append({'headers': hdr, 'rows': [row], 'src': 'yaml'})
            continue
        lines.append(ln)
        i += 1
    return lines, tables


# ---------------------------------------------------------------- sentence grammar
P = r'[a-z][a-z\-]*'
UNIT = r'(?:\s*%|\s+[A-Za-z][A-Za-z\-]*(?: [A-Za-z][A-Za-z\-]*)*)?'


def clean_line(ln):
    s = ln.strip()
    for _ in range(4):
        s2 = re.sub(r'^(?:[-*•+·>◦▪‣–—]+|\d+[.)]|\(\d+\)|[a-z][.)](?=\s)|#+|Step \d+:)\s*', '', s)
        if s2 == s:
            break
        s = s2
    s = s.replace('**', '').replace('__', '')
    s = s.strip().rstrip(',').strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"' and s.count('"') == 2:
        s = s[1:-1].strip()
    return s


def split_sents(s):
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', s)
    return [p.strip() for p in parts if p.strip()]


def strip_period(s):
    s = s.strip()
    while s and s[-1] in '.;':
        s = s[:-1].rstrip()
    return s


def parse_cmp(s):
    """Written comparison/range/window -> ('rng', lo, hi) | (op, v); v = ('date', ord) | ('num', (int, k))."""
    s = s.strip()
    D = '(' + DATE_RE + ')'
    for pat, op in ((r'(?:between|from) ' + D + r' (?:and|to) ' + D, 'rng'),
                    (r'(?:on or before|by|no later than) ' + D, '<='),
                    (r'(?:on or after|no earlier than) ' + D, '>='),
                    (r'(?:before|prior to) ' + D, '<'),
                    (r'(?:after|later than) ' + D, '>')):
        m = re.fullmatch(pat, s)
        if m:
            if op == 'rng':
                return ('rng', ('date', parse_date(m.group(1))), ('date', parse_date(m.group(2))))
            return (op, ('date', parse_date(m.group(1))))
    N = '(' + NUM_RE + ')' + UNIT
    for pat, op in ((r'(?:between|from) ' + N + r' (?:and|to) ' + N, 'rng'),
                    (r'(?:at least|no fewer than|no less than) ' + N, '>='),
                    (N + r' or more', '>='),
                    (r'(?:more than|over|above|exceeds) ' + N, '>'),
                    (r'(?:at most|no more than|up to) ' + N, '<='),
                    (N + r' or (?:fewer|less)', '<='),
                    (r'(?:fewer than|less than|under|below) ' + N, '<')):
        m = re.fullmatch(pat, s)
        if m:
            if op == 'rng':
                return ('rng', ('num', parse_num(m.group(1))), ('num', parse_num(m.group(2))))
            return (op, ('num', parse_num(m.group(1))))
    return None


def parse_condition(c, subj_word='is'):
    """One condition of a rule body (subject implicit).  Returns a cond tuple or None.
    ('lit', pred, pol) | ('cmp', quantity, cmpspec)"""
    c = c.strip().rstrip(',').strip()
    m = re.fullmatch(r'(?:it )?is not (' + P + ')', c)
    if m:
        return ('lit', m.group(1), False)
    m = re.fullmatch(r'(?:it )?is (' + P + ')', c)
    if m:
        return ('lit', m.group(1), True)
    m = re.fullmatch(r'(?:it )?has (' + P + ') standing', c)
    if m:
        return ('lit', m.group(1), True)
    m = re.fullmatch(r'(?:it )?lacks the (' + P + ') designation', c)
    if m:
        return ('lit', m.group(1), False)
    m = re.fullmatch(r'(?:it )?fails to qualify as (' + P + ')', c)
    if m:
        return ('lit', m.group(1), False)
    m = re.fullmatch(r'(?:whose|its) (.+)', c)
    if m:
        rest = m.group(1)
        for mm in re.finditer(r' (is|exceeds) ', rest):
            q = rest[:mm.start()]
            tail = rest[mm.end():] if mm.group(1) == 'is' else 'exceeds ' + rest[mm.end():]
            cs = parse_cmp(tail)
            if cs is not None:
                return ('cmp', norm_q(q), cs)
    return None


COND_START = r'(?:is |whose |has |lacks |fails |its |it )'


def _disj(x):
    x = x.strip()
    if re.fullmatch(P, x):
        return ('lit', x, True)
    return parse_condition(x)


def parse_body(b):
    """Rule body (after 'that').  Returns (kind, conds, link) or None."""
    b = b.strip().rstrip(',').strip()
    m = re.fullmatch(r'is either (.+?) or (.+?),? but not both', b)
    if m:
        d1, d2 = _disj(m.group(1)), _disj(m.group(2))
        return ('xor', [d1, d2], None) if d1 and d2 else None
    m = re.fullmatch(r'is either (.+?) or (.+?) \(or both\)', b)
    if m:
        d1, d2 = _disj(m.group(1)), _disj(m.group(2))
        return ('or', [d1, d2], None) if d1 and d2 else None
    m = re.fullmatch(r'(?!is |whose |has |lacks |fails |its )(.+?) (?:a|an) (.+?) that (.+)', b)
    if m:
        cond = parse_condition(m.group(3))
        if cond and cond[0] == 'lit':
            return ('link', [cond], (m.group(1).strip(), m.group(2).strip()))
    ors = re.split(r'(?<!\bon) or (?!more\b|fewer\b|less\b|both\b)', b)
    ands = re.split(r' and (?=' + COND_START + ')', b)
    if len(ors) > 1 and len(ands) > 1:
        return None  # and/or mixed: rejected by the grammar
    if len(ors) == 2:
        d1 = parse_condition(ors[0])
        d2 = _disj(ors[1]) if not re.match(COND_START, ors[1]) else parse_condition(ors[1])
        return ('or', [d1, d2], None) if d1 and d2 else None
    conds = [parse_condition(a) for a in ands]
    if all(conds):
        return ('univ', conds, None)
    return None


def parse_rule_sentence(s):
    s = strip_period(s)
    exc = None
    m = re.fullmatch(r'(.*?),? (?:unless it is|except one that is) (' + P + ')', s)
    if m:
        s, exc = m.group(1), m.group(2)
    m = re.fullmatch(r'An? (.+?) is (' + P + r') only if it is (not )?(' + P + ')', s)
    if m:
        return {'kind': 'onlyif', 'type': m.group(1), 'conds': [('lit', m.group(2), True)],
                'head': (m.group(4), not m.group(3)), 'exc': exc}
    m = re.fullmatch(r'(Every|Each|All|Any|No) (.+?) that (.+),? is (not )?(' + P + ')', s)
    if m:
        q, T, body, neg, H = m.groups()
        pb = parse_body(body)
        if pb is None:
            return None
        kind, conds, link = pb
        pol = not neg
        if q == 'No':
            if neg:
                return None
            pol = False
        r = {'kind': kind, 'type': T, 'conds': conds, 'head': (H, pol), 'exc': exc}
        if link:
            r['link'] = link
        return r
    return None


LEADIN_ALL = re.compile(r'This provision covers every (.+?) that meets all of the following conditions:?')
LEADIN_K = re.compile(r'An? (.+?) is (not )?(' + P + r') if at least (\w+) of the following hold:?')
CLOSE_SUCH = re.compile(r'Every such (.+?) is (not )?(' + P + r')(?:,? (?:unless it is|except one that is) (' + P + '))?')
WORDNUM = {'one': 1, 'two': 2, 'three': 3, 'four': 4}


def parse_conjunct(e, c):
    c = c.strip()
    m = re.fullmatch(r'is an? (.+)', c)
    if m:
        return [('type', e, m.group(1).strip())]
    cond = parse_condition(c)
    if cond and cond[0] == 'lit':
        return [('lit', e, cond[1], cond[2])]
    m = re.fullmatch(r'has an? (.+?) of (.+)', c)
    if m:
        v = parse_value(m.group(2))
        if v is not None:
            return [('val', e, norm_q(m.group(1)), v)]
    m = re.fullmatch(r'(?!is |has an? )([a-z][a-z \-]*?) (' + ID_RE + r'(?:(?:,| and|, and) ' + ID_RE + r')*)', c)
    if m:
        return [('link', m.group(1).strip(), e, t) for t in ID_FIND.findall(m.group(2))]
    return None


TYPE_HINT = set()


def parse_fact(s):
    """Unattributed or attributed fact sentence -> list of atoms, or None."""
    s = strip_period(s)
    m = re.fullmatch(r'(' + ID_RE + r') (.+)', s)
    if not m:
        return None
    e, rest = m.group(1), m.group(2)
    parts = rest.split(' and ')
    out, buf = [], None
    for p in parts:
        cand = p if buf is None else buf + ' and ' + p
        r = parse_conjunct(e, cand)
        if r is None:
            buf = cand
        else:
            out.extend(r); buf = None
    if buf is not None:
        return None
    return out


V2_LABEL = re.compile(r'^[A-Z][A-Za-z ]{0,30}:\s*whether\b')
HEDGE = re.compile(r'^(Most|Many|Some|Not every|Usually|Often|In many|In most)\b|\b(usually|often)\b')
EHEDGE = re.compile(r'^' + ID_RE + r' (?:may well be|may be|might be) ' + P + r'$')
CLOS_PROSE = re.compile(r'[Tt]he record names every (.+?) that is (' + P + ')')
CLOS_COL = re.compile(r'[Tt]he (.+?) column is complete: a blank (.+?) cell means No')
ATTR_REP = re.compile(r'(.+?) reported that (.+)')
ATTR_Q = re.compile(r'([^:"]+?):\s*"(.+)"\.?')
ATTR_C = re.compile(r'([^:"]+?):\s*(.+)')


class Rec:
    def __init__(self):
        self.stmts = []        # (source|None, [atoms], origin)
        self.rules = []
        self.clos_prose = []   # (type, pred)
        self.clos_col = []     # pred
        self.tables = []
        self.unparsed = []
        self.notes = collections.Counter()


def _finish_pending(rec, pend, card_mode):
    if pend is None:
        return
    if pend['mode'] == 'k':
        items = pend['items']
        if items and all(items):
            rec.rules.append({'kind': 'kofn', 'type': pend['type'], 'conds': items, 'k': pend['k'],
                              'head': pend['head'], 'exc': None})
        else:
            rec.notes['bad_kofn'] += 1
    else:
        rec.notes['open_leadin'] += 1


def parse_text(text, rec, card_mode=False):
    lines, tables = extract(text)
    if not card_mode:
        rec.tables.extend(tables)
    pend = None
    for raw in lines:
        s = clean_line(raw)
        if not s:
            continue
        sp = strip_period(s)
        # bulleted rules
        if pend is not None:
            cond = parse_condition(sp) if re.match(r'(it|its) ', sp) else None
            if cond is not None:
                pend['items'].append(cond); continue
            m = CLOSE_SUCH.fullmatch(sp)
            if m and pend['mode'] == 'all':
                if pend['items'] and all(pend['items']):
                    rec.rules.append({'kind': 'univ', 'type': m.group(1), 'conds': pend['items'],
                                      'head': (m.group(3), not m.group(2)), 'exc': m.group(4)})
                else:
                    rec.notes['bad_bullets'] += 1
                pend = None; continue
            if pend['mode'] == 'k':
                _finish_pending(rec, pend, card_mode); pend = None
            else:
                rec.notes['leadin_interrupted'] += 1
        m = LEADIN_ALL.fullmatch(sp)
        if m:
            pend = {'mode': 'all', 'type': m.group(1), 'items': []}; continue
        m = LEADIN_K.fullmatch(sp)
        if m:
            k = m.group(4)
            k = int(k) if k.isdigit() else WORDNUM.get(k.lower())
            pend = {'mode': 'k', 'type': m.group(1), 'items': [], 'k': k, 'head': (m.group(3), not m.group(2))}
            continue
        if card_mode:
            for sent in split_sents(s):
                r = parse_rule_sentence(sent)
                if r:
                    r['card'] = True
                    rec.rules.append(r)
            continue
        m = CLOS_PROSE.fullmatch(sp)
        if m:
            rec.clos_prose.append((m.group(1), m.group(2))); continue
        m = CLOS_COL.fullmatch(sp)
        if m:
            rec.clos_col.append(norm_q(m.group(1))); continue
        if V2_LABEL.match(s):
            rec.notes['v2'] += 1; continue
        done = False
        for rx in (ATTR_REP, ATTR_Q, ATTR_C):
            m = rx.fullmatch(s)
            if m and not ID_FIND.search(m.group(1)):
                atoms = parse_fact(m.group(2))
                if atoms is not None and len(split_sents(m.group(2))) == 1:
                    rec.stmts.append((m.group(1).strip(), atoms, 'attr')); done = True
                    break
        if done:
            continue
        for sent in split_sents(s):
            r = parse_rule_sentence(sent)
            if r:
                rec.rules.append(r); continue
            atoms = parse_fact(sent)
            if atoms is not None:
                rec.stmts.append((None, atoms, 'prose')); continue
            sp2 = strip_period(sent)
            if HEDGE.search(sp2) or EHEDGE.fullmatch(sp2):
                rec.notes['hedge'] += 1; continue
            rec.unparsed.append(sent)
    if pend is not None:
        _finish_pending(rec, pend, card_mode)
    return rec


def tables_to_stmts(rec):
    for tbl in rec.tables:
        hdr = [h.strip() for h in tbl['headers']]
        low = [h.lower() for h in hdr]
        if 'id' not in low:
            rec.notes['table_no_id'] += 1
            continue
        ii = low.index('id')
        ti = low.index('type') if 'type' in low else None
        for row in tbl['rows']:
            row = list(row) + [''] * (len(hdr) - len(row))
            e = row[ii].strip().strip('"')
            if not ID_FULL.match(e):
                rec.notes['table_bad_id'] += 1
                continue
            atoms = []
            if ti is not None and row[ti].strip():
                atoms.append(('type', e, row[ti].strip()))
            for j, h in enumerate(hdr):
                if j in (ii, ti):
                    continue
                v = row[j].strip()
                hq = norm_q(h)
                if v == '':
                    atoms.append(('blank', e, hq))
                elif v.lower() == 'yes':
                    atoms.append(('lit', e, hq, True))
                elif v.lower() == 'no':
                    atoms.append(('lit', e, hq, False))
                elif v.lower() == 'not recorded':
                    atoms.append(('unk', e, hq))
                elif ID_FIND.search(v) and re.fullmatch(r'(?:' + ID_RE + r')(?:\s*(?:,|;|and)\s*' + ID_RE + r')*', v):
                    for t in ID_FIND.findall(v):
                        atoms.append(('link', hq, e, t))
                else:
                    pv = parse_value(v)
                    if pv is not None:
                        atoms.append(('val', e, hq, pv))
                    else:
                        rec.notes['cell_unparsed'] += 1
                        rec.unparsed.append('CELL[' + hq + ']')
            rec.stmts.append((None, atoms, 'table'))


def card_flags(ctext):
    f = {'world': None, 'unless': None, 'trust': None, 'trusted': set(), 'err': []}
    w = []
    if re.search(r'The record may be incomplete\.', ctext):
        w.append('ow')
    if re.search(r'Treat the record as complete\.', ctext):
        w.append('cw')
    if re.search(r"'Follows from', 'establishes' and 'shows' mean", ctext):
        w.append('short')
    if len(w) != 1:
        f['err'].append('world:' + ','.join(w))
    f['world'] = w[0] if w else None
    if 'If the record does not settle whether an exception holds' in ctext:
        f['unless'] = 'strict'
    if 'Exceptions are listed in full' in ctext:
        f['unless'] = 'listc' if f['unless'] is None else 'both'
    m = re.search(r'only those from (.+?) count as facts', ctext)
    if m:
        f['trust'] = 'list'
        lst = m.group(1)
        f['trusted_raw'] = norm_src(lst)
        f['trusted'] = set(norm_src(x) for x in re.split(r',\s*(?:or\s+|and\s+)?|\s+or\s+|\s+and\s+', lst) if x.strip())
    if 'Treat every statement in the record, with or without a source, as a fact' in ctext:
        f['trust'] = 'all' if f['trust'] is None else 'both'
    return f


def is_trusted(src, flags):
    if src is None:
        return True
    if flags['trust'] in (None, 'all'):
        return True
    n = norm_src(src)
    if n in flags['trusted']:
        return True
    raw = flags.get('trusted_raw', '')
    return bool(re.search(r'(^|, |,| or | and )' + re.escape(n) + r'($|,| or | and )', raw))


# ---------------------------------------------------------------- world
class World:
    """Ground facts after trust filtering."""

    def __init__(self, rec, flags):
        self.notes = rec.notes
        self.etype = {}
        self.facts = {}       # (pred, e) -> bool
        self.vals = {}        # (e, q) -> value
        self.unk = set()      # (e, q) marked unknown
        self.links = set()    # (phrase, e1, e2)
        self.blank = set()    # (e, pred)
        self.attr_seen = False
        for src, atoms, origin in rec.stmts:
            if src is not None:
                self.attr_seen = True
            trusted = is_trusted(src, flags)
            for a in atoms:
                if a[0] == 'type':
                    if a[1] in self.etype and self.etype[a[1]] != a[2]:
                        self.notes['type_conflict'] += 1
                    self.etype[a[1]] = a[2]
                    continue
                if not trusted:
                    continue
                if a[0] == 'lit':
                    k = (a[2], a[1])
                    if k in self.facts and self.facts[k] != a[3]:
                        self.notes['fact_conflict'] += 1
                    self.facts[k] = a[3]
                elif a[0] == 'val':
                    self.vals[(a[1], a[2])] = a[3]
                elif a[0] == 'unk':
                    self.unk.add((a[1], a[2]))
                elif a[0] == 'link':
                    if a[2] == a[3]:
                        self.notes['self_link'] += 1
                    self.links.add((norm_q(a[1]), a[2], a[3]))
                elif a[0] == 'blank':
                    self.blank.add((a[1], a[2]))
        self.rules = rec.rules
        self.flags = flags
        # closures
        self.closed = set()   # (pred, e) closed false
        for T, C in rec.clos_prose:
            for e, t in self.etype.items():
                if t == T and (C, e) not in self.facts:
                    self.closed.add((C, e))
        for C in rec.clos_col:
            types = set()
            for tbl in rec.tables:
                if C in [norm_q(h) for h in tbl['headers']]:
                    low = [h.strip().lower() for h in tbl['headers']]
                    if 'id' in low:
                        for row in tbl['rows']:
                            e = row[low.index('id')].strip().strip('"')
                            if e in self.etype:
                                types.add(self.etype[e])
            for e, t in self.etype.items():
                if t in types and (C, e) not in self.facts:
                    self.closed.add((C, e))
        for (e, C) in self.blank:
            if (C, e) not in self.closed:
                self.notes['blank_not_closed'] += 1
        if flags['world'] in ('ow', 'short') and flags['unless'] == 'listc':
            excs = set(r['exc'] for r in self.rules if r.get('exc'))
            for C in excs:
                for e in self.etype:
                    if (C, e) not in self.facts:
                        self.closed.add((C, e))

    def ents(self, T):
        return [e for e, t in self.etype.items() if t == T]

    def value(self, e, q):
        return self.vals.get((e, q))


def cmp_holds(v, spec):
    """Evaluate a written condition on a given value."""
    def c(a, b):
        if a[0] != b[0]:
            raise ParseError('value kind mismatch')
        if a[0] == 'date':
            return (a[1] > b[1]) - (a[1] < b[1])
        x, y = num_cmp_pair(a[1], b[1])
        return (x > y) - (x < y)
    op = spec[0]
    if op == 'rng':
        return c(v, spec[1]) >= 0 and c(v, spec[2]) <= 0
    r = c(v, spec[1])
    return {'>=': r >= 0, '>': r > 0, '<=': r <= 0, '<': r < 0}[op]


# ---------------------------------------------------------------- OW: ground clauses + enumeration
def _pts_regions(points, kind):
    """Regions for a missing value: list of representative predicates (lo, hi, eq) as tuples."""
    pts = sorted(set(points))
    regs = []
    prev = None
    for p in pts:
        regs.append(('open', prev, p))
        regs.append(('eq', p, p))
        prev = p
    regs.append(('open', prev, None))
    if kind == 'date':
        regs = [r for r in regs if not (r[0] == 'open' and r[1] is not None and r[2] is not None and r[2] - r[1] <= 1)]
    return regs


def _region_holds(reg, spec, kind, scale):
    """Does written condition spec hold everywhere on region reg?  Values are (int at common scale)."""
    def sv(x):
        return x[1] if kind == 'date' else x[1][0] * 10 ** (scale - x[1][1])
    op = spec[0]
    if reg[0] == 'eq':
        v = reg[1]
        if op == 'rng':
            return sv(spec[1]) <= v <= sv(spec[2])
        t = sv(spec[1])
        return {'>=': v >= t, '>': v > t, '<=': v <= t, '<': v < t}[op]
    lo, hi = reg[1], reg[2]
    # strictly inside (lo, hi): every written condition is constant on the open region
    if op == 'rng':
        a, b = sv(spec[1]), sv(spec[2])
        return lo is not None and hi is not None and lo >= a and hi <= b
    t = sv(spec[1])
    if op in ('>', '>='):
        return lo is not None and lo >= t
    return hi is not None and hi <= t


class OWTheory:
    def __init__(self, w, drop_card_rules=False):
        self.w = w
        self.fixed = {}
        for (p, e), v in w.facts.items():
            self.fixed[('P', p, e)] = v
        for (p, e) in w.closed:
            k = ('P', p, e)
            if k in self.fixed and self.fixed[k] is not False:
                w.notes['closure_vs_fact'] += 1
            self.fixed.setdefault(k, False)
        self.domains = {}
        self.regions = {}
        self._prep_regions()
        self.clauses = []
        for r in w.rules:
            self._ground(r)

    def _cmp_targets(self):
        for r in self.w.rules:
            if r['kind'] == 'link':
                continue
            for cond in r['conds']:
                if cond[0] == 'cmp':
                    for x in self.w.ents(r['type']):
                        yield x, cond

    def _prep_regions(self):
        pts = collections.defaultdict(list)
        kinds = {}
        for x, (_, q, spec) in self._cmp_targets():
            if self.w.value(x, q) is not None:
                continue
            ends = [spec[1], spec[2]] if spec[0] == 'rng' else [spec[1]]
            for v in ends:
                pts[(x, q)].append(v)
                kinds.setdefault((x, q), set()).add(v[0])
        for key, vs in pts.items():
            ks = kinds[key]
            if len(ks) != 1:
                raise ParseError('mixed value kinds')
            kind = ks.pop()
            scale = 0 if kind == 'date' else max(v[1][1] for v in vs)
            ivs = [v[1] if kind == 'date' else v[1][0] * 10 ** (scale - v[1][1]) for v in vs]
            regs = _pts_regions(ivs, kind)
            self.regions[key] = (kind, scale, regs)
            self.domains[('Q',) + key] = list(range(len(regs)))

    def cond_lit(self, cond, x):
        if cond[0] == 'lit':
            return (('P', cond[1], x), frozenset([cond[2]]))
        _, q, spec = cond
        v = self.w.value(x, q)
        if v is not None:
            return cmp_holds(v, spec)
        kind, scale, regs = self.regions[(x, q)]
        if kind == 'date' and spec[1][0] != 'date' or kind == 'num' and spec[1][0] != 'num':
            raise ParseError('cmp kind')
        return (('Q', x, q), frozenset(i for i, rg in enumerate(regs) if _region_holds(rg, spec, kind, scale)))

    def dom(self, var):
        return self.domains.get(var, [False, True])

    def neg(self, lit):
        if lit is True or lit is False:
            return not lit
        var, al = lit
        return (var, frozenset(v for v in self.dom(var) if v not in al))

    def add(self, items):
        cl = []
        for it in items:
            if it is True:
                return
            if it is False:
                continue
            cl.append(it)
        self.clauses.append(cl)

    def _ground(self, r):
        H, pol = r['head']
        kind = r['kind']
        if kind == 'link':
            phrase, T2 = r['link']
            phrase = norm_q(phrase)
            for (ph, x, y) in self.w.links:
                if ph == phrase and self.w.etype.get(x) == r['type'] and self.w.etype.get(y) == T2:
                    self.add([self.neg(self.cond_lit(r['conds'][0], y)), (('P', H, x), frozenset([pol]))])
            return
        for x in self.w.ents(r['type']):
            head = (('P', H, x), frozenset([pol]))
            lits = [self.cond_lit(c, x) for c in r['conds']]
            exc = [(('P', r['exc'], x), frozenset([True]))] if r.get('exc') else []
            if kind in ('univ', 'onlyif'):
                self.add([self.neg(l) for l in lits] + exc + [head])
            elif kind == 'kofn':
                for sub in itertools.combinations(lits, r['k']):
                    self.add([self.neg(l) for l in sub] + [head])
            elif kind == 'or':
                for l in lits:
                    self.add([self.neg(l), head])
            elif kind == 'xor':
                a, b = lits
                self.add([self.neg(a), b, head])
                self.add([a, self.neg(b), head])

    # ---- simplification by unit facts, components, enumeration
    def simplify(self):
        out = []
        for cl in self.clauses:
            new, sat = [], False
            for var, al in cl:
                if var in self.fixed:
                    if self.fixed[var] in al:
                        sat = True
                        break
                    continue
                new.append((var, al))
            if sat:
                continue
            out.append(new)
        self.sclauses = out
        par = {}

        def find(a):
            while par.setdefault(a, a) != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for cl in out:
            vs = [v for v, _ in cl]
            for v in vs:
                find(v)
            for v in vs[1:]:
                ra, rb = find(vs[0]), find(v)
                if ra != rb:
                    par[ra] = rb
        self.find = find
        self.comp = collections.defaultdict(list)
        for i, cl in enumerate(out):
            if cl:
                self.comp[find(cl[0][0])].append(i)
            else:
                self.comp[('EMPTY', i)].append(i)

    def sat(self, clause_ids, force=None, limit=2000000):
        """Backtracking model search over the vars of the given clauses; force = (var, value)."""
        cls = [self.sclauses[i] for i in clause_ids]
        if any(len(c) == 0 for c in cls):
            return False
        cnt = collections.Counter(v for c in cls for v, _ in c)
        order = [v for v, _ in cnt.most_common()]
        if force is not None and force[0] in cnt:
            order.remove(force[0]); order.insert(0, force[0])
        pos = {v: i for i, v in enumerate(order)}
        bucket = collections.defaultdict(list)
        for c in cls:
            bucket[max(pos[v] for v, _ in c)].append(c)
        asg = {}
        nodes = [0]

        def rec(i):
            if i == len(order):
                return True
            v = order[i]
            dom = [force[1]] if (force is not None and v == force[0]) else self.dom(v)
            for val in dom:
                nodes[0] += 1
                if nodes[0] > limit:
                    raise ParseError('search budget')
                asg[v] = val
                if all(any(asg[x] in al for x, al in c) for c in bucket[i]):
                    if rec(i + 1):
                        return True
            del asg[v]
            return False
        return rec(0)

    def consistent(self):
        for k, ids in self.comp.items():
            if not self.sat(ids):
                return False
        return True

    def label(self, pred, e, pol):
        var = ('P', pred, e)
        if var in self.fixed:
            can_t = self.fixed[var] == pol
            can_f = not can_t
        else:
            ids = self.comp.get(self.find(var), [])
            can_t = self.sat(ids, (var, pol)) if ids else True
            can_f = self.sat(ids, (var, not pol)) if ids else True
        if can_t and not can_f:
            return 'F'
        if can_f and not can_t:
            return 'R'
        if can_t and can_f:
            return 'O'
        return 'X'


# ---------------------------------------------------------------- CW: Clark completion, top-down
class CWProgram:
    def __init__(self, w):
        self.w = w
        self.memo = {}
        self.stack = set()
        self.by_head = collections.defaultdict(list)
        for r in w.rules:
            if r['head'][1]:
                self.by_head[r['head'][0]].append(r)

    def cond(self, c, x):
        if c[0] == 'lit':
            return self.val(c[1], x) == c[2]
        v = self.w.value(x, c[1])
        if v is None:
            self.w.notes['cw_missing_value'] += 1
            return False
        return cmp_holds(v, c[2])

    def body_holds(self, r, x):
        if r.get('exc') and self.val(r['exc'], x):
            return False
        kind = r['kind']
        if kind == 'univ':
            return all(self.cond(c, x) for c in r['conds'])
        if kind == 'kofn':
            return sum(1 for c in r['conds'] if self.cond(c, x)) >= r['k']
        if kind == 'or':
            return any(self.cond(c, x) for c in r['conds'])
        if kind == 'xor':
            return sum(1 for c in r['conds'] if self.cond(c, x)) == 1
        if kind == 'onlyif':
            self.w.notes['cw_onlyif'] += 1
            return all(self.cond(c, x) for c in r['conds'])
        if kind == 'link':
            phrase, T2 = r['link']
            phrase = norm_q(phrase)
            return any(self.cond(r['conds'][0], y) for (ph, a, y) in self.w.links
                       if ph == phrase and a == x and self.w.etype.get(y) == T2)
        raise ParseError('kind ' + kind)

    def val(self, p, x):
        k = (p, x)
        if k in self.memo:
            return self.memo[k]
        if k in self.stack:
            raise ParseError('cycle')
        self.stack.add(k)
        res = self.w.facts.get(k) is True
        if not res:
            for r in self.by_head.get(p, []):
                if self.w.etype.get(x) == r['type'] and self.body_holds(r, x):
                    res = True
                    break
        self.stack.discard(k)
        self.memo[k] = res
        return res

    def check_constraints(self):
        bad = 0
        for (p, x), v in self.w.facts.items():
            if v is False and self.val(p, x):
                bad += 1
        for r in self.w.rules:
            if not r['head'][1]:
                for x in self.w.ents(r['type']):
                    if self.body_holds(r, x) and self.val(r['head'][0], x):
                        bad += 1
        return bad

    def label(self, pred, e, pol):
        return 'F' if self.val(pred, e) == pol else 'R'


# ---------------------------------------------------------------- question + gold
CLAIM = r'(' + ID_RE + r') is (not )?(' + P + r')'
YN_PATS = [
    ('YN-T', re.compile(r'"' + CLAIM + r'"')),
    ('YN-dn', re.compile(r'not the case that (?:the record|it) does not (?:establish|show) that ' + CLAIM + r'\b')),
    ('YN-nF', re.compile(r'does not (?:establish|show) that ' + CLAIM + r'\b')),
    ('YN-nR', re.compile(r'does not rule out that ' + CLAIM + r'\b')),
    ('YN-F', re.compile(r'(?:establish|establishes|show|shows) that ' + CLAIM + r'\b')),
    ('YN-R', re.compile(r'(?:rule|rules) out that ' + CLAIM + r'\b')),
    ('YN-O', re.compile(r'(?:leave|leaves) open whether ' + CLAIM + r'\b')),
]


def yn_answer(form, lab):
    return {'YN-F': lab == 'F', 'YN-dn': lab == 'F', 'YN-T': lab == 'F', 'YN-R': lab == 'R',
            'YN-O': lab == 'O', 'YN-nF': lab != 'F', 'YN-nR': lab != 'R'}[form]


def outcome_of(t):
    t = t.strip().lower()
    if 'cannot be determined' in t or 'open' in t:
        return 'O'
    if 'rule' in t and 'out' in t or t == 'false':
        return 'R'
    if 'establish' in t or 'shows' in t or 'follows' in t or t == 'true':
        return 'F'
    return None


def parse_question(row):
    q = row['instructions'] or ''
    if row['qtype'] == 'noul':
        for form, rx in YN_PATS:
            ms = list(rx.finditer(q))
            if ms:
                m = ms[-1]
                return {'form': form, 'claims': [(m.group(1), m.group(3), not m.group(2))]}
        raise ParseError('yn frame')
    opts = row['options'] or []
    if opts and all(ID_FULL.match(o.strip()) for o in opts):
        ms = list(re.finditer(r'(?:establish|establishes|show|shows) that (?:it|one of these [^?.]+?) is (' + P + r')\b', q))
        if not ms:
            raise ParseError('entity frame')
        H = ms[-1].group(1)
        return {'form': 'CH-entity', 'claims': [(o.strip(), H, True) for o in opts], 'opts': opts}
    cl = [re.fullmatch(CLAIM, strip_period(o)) for o in opts]
    if any(cl) and all(c or o.strip().lower().startswith('none of these') for c, o in zip(cl, opts)):
        claims = [(c.group(1), c.group(3), not c.group(2)) if c else None for c in cl]
        return {'form': 'CH-claim', 'claims': claims, 'opts': opts}
    ms = list(re.finditer(r'the claim that ' + CLAIM + r'\b', q))
    if not ms:
        raise ParseError('ch frame')
    m = ms[-1]
    defs = {}
    for ln in (row['card'] or '').split('\n'):
        mm = re.match(r'^\s*-\s+(.+?):\s+(.+?)\s*$', ln)
        if mm:
            defs[mm.group(1).strip()] = mm.group(2)
    omap = {}
    for o in opts:
        oc = outcome_of(defs[o]) if o in defs else outcome_of(o)
        omap[o] = oc
    form = 'CH-3' if len(opts) == 3 else 'CH-2'
    return {'form': form, 'claims': [(m.group(1), m.group(3), not m.group(2))], 'opts': opts, 'omap': omap}


def solve_row(row):
    """Return dict: answer (B), form, world, labels, notes."""
    ctext = (row['card'] or '') if row['qtype'] == 'noul' else (row['instructions'] or '') + '\n' + (row['card'] or '')
    flags = card_flags(ctext)
    if flags['err']:
        raise ParseError(';'.join(flags['err']))
    rec = Rec()
    parse_text(row['state'] or '', rec)
    tables_to_stmts(rec)
    parse_text(ctext, rec, card_mode=True)
    if 'norules' in ABLATE:
        rec.rules = []
    if 'nocardrules' in ABLATE:
        rec.rules = [r for r in rec.rules if not r.get('card')]
    if 'noexc' in ABLATE:
        for r in rec.rules:
            r['exc'] = None
    if 'noclosure' in ABLATE:
        rec.clos_prose, rec.clos_col = [], []
    if 'alltrust' in ABLATE:
        flags['trust'] = 'all'
    if 'listc' in ABLATE and flags['unless'] == 'strict':
        flags['unless'] = 'listc'
    w = World(rec, flags)
    qs = parse_question(row)
    world = 'cw' if flags['world'] == 'cw' else 'ow'
    if 'flipworld' in ABLATE:
        world = 'ow' if world == 'cw' else 'cw'
    if world == 'ow':
        th = OWTheory(w)
        th.simplify()
        if not th.consistent():
            rec.notes['inconsistent'] += 1
        labf = th.label
    else:
        prog = CWProgram(w)
        bad = prog.check_constraints()
        if bad:
            rec.notes['cw_constraint_violation'] += bad
        labf = prog.label
    labels = []
    for c in qs['claims']:
        if c is None:
            labels.append(None)
            continue
        e, H, pol = c
        if e not in w.etype:
            rec.notes['claim_entity_untyped'] += 1
        labels.append(labf(H, e, pol))
    form = qs['form']
    ans = None
    if form.startswith('YN'):
        ans = 1 if yn_answer(form, labels[0]) else 0
    elif form in ('CH-3', 'CH-2'):
        hit = [o for o in qs['opts'] if qs['omap'].get(o) == labels[0]]
        ans = hit[0] if len(hit) == 1 else ('<no option for %s>' % labels[0] if not hit else '<several>')
    else:
        hit = [o for o, l in zip(qs['opts'], labels) if l == 'F']
        if not hit and form == 'CH-claim':
            hit = [o for o in qs['opts'] if o.strip().lower().startswith('none of these')]
        ans = hit[0] if len(hit) == 1 else ('<none qualifies>' if not hit else '<several:%d>' % len(hit))
    preds = set()
    for r in w.rules:
        preds.add(r['head'][0])
        for c in r['conds']:
            if c[0] == 'lit':
                preds.add(c[1])
        if r.get('exc'):
            preds.add(r['exc'])
    sus = [u for u in rec.unparsed if any(re.search(r'\b' + re.escape(p) + r'\b', u) for p in preds)]
    return {'answer': ans, 'form': form, 'world': flags['world'], 'unless': flags['unless'],
            'labels': labels, 'notes': dict(rec.notes), 'n_unparsed': len(rec.unparsed),
            'suspect_unparsed': len(sus), 'n_rules': len(w.rules), 'n_card_rules': sum(1 for r in w.rules if r.get('card')),
            'attr': w.attr_seen, 'trust': flags['trust'], '_sus': sus[:3], '_unp': rec.unparsed[:5], '_unp_all': rec.unparsed}


def spec_item(form, world):
    base = {'YN-F': 's1 YN-F (Q-A/Q-B; yes iff FOLLOWS)', 'YN-R': 's1 YN-R (yes iff RULED_OUT)',
            'YN-O': 's1 YN-O (yes iff OPEN)', 'YN-T': 's1 YN-T (yes iff TRUE)',
            'YN-nF': 's1 YN-nF (yes iff not FOLLOWS)', 'YN-nR': 's1 YN-nR (yes iff not RULED_OUT)',
            'YN-dn': 's1 YN-dn (as YN-F)', 'CH-3': 's1 CH-3 (label option)', 'CH-2': 's1 CH-2 (label option)',
            'CH-claim': 's1/2.4#4 CH-claim (single FOLLOWS/TRUE claim or None)',
            'CH-entity': 's1/2.4#4 CH-entity (single entity with FOLLOWS/TRUE)'}.get(form, form)
    sem = {'ow': 's3 OW model enumeration (clause 3)', 'short': 's7.4 short card, OW label (clause 3s)',
           'cw': 's3 CW Clark completion / least model (clauses 2, 3c, 5c)'}.get(world, str(world))
    return base + '; ' + sem


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--debug', default=None)
    ap.add_argument('--ids', default=None)
    ap.add_argument('--ablate', default='')
    a = ap.parse_args(argv)
    ABLATE.update(x for x in a.ablate.split(',') if x)
    want = set(a.ids.split(',')) if a.ids else None
    mism, summary, tagnotes = [], {}, []
    dbg = open(a.debug, 'w') if a.debug else None
    agg = collections.Counter()
    for fn in a.files:
        n = agree = 0
        short = fn.rsplit('/', 1)[-1]
        with open(fn) as fh:
            for line in fh:
                row = json.loads(line)
                if want and row['id'] not in want:
                    continue
                n += 1
                if a.limit and n > a.limit:
                    break
                gold = row['gold']
                try:
                    res = solve_row(row)
                    b = res['answer']
                except Exception as ex:  # parse or solver failure
                    res = {'answer': None, 'form': None, 'world': None, 'error': type(ex).__name__ + ': ' + str(ex)[:120]}
                    b = None
                ok = (b == gold) if res.get('error') is None else False
                if ok:
                    agree += 1
                else:
                    mism.append({'id': row['id'], 'file': short, 'gold': gold, 'solver_b': b,
                                 'kind': 'error' if res.get('error') else 'answer',
                                 'error': res.get('error'), 'form': res.get('form'), 'world': res.get('world'),
                                 'labels_b': res.get('labels'),
                                 'meta_label': next((e for e in row['meta']['edge'] if e.startswith('L:')), None),
                                 'sampler': row['meta']['sampler'],
                                 'spec_item': spec_item(res.get('form'), res.get('world')) if res.get('form') else 's4 round-trip parse (G3)'})
                ml = next((e for e in row['meta']['edge'] if e.startswith('L:')), None)
                bl = None
                labs, frm, opts = res.get('labels') or [], res.get('form') or '', row['options'] or []
                if labs and (frm.startswith('YN') or frm in ('CH-3', 'CH-2')):
                    bl = labs[0]
                elif labs and frm in ('CH-entity', 'CH-claim') and gold in opts and not str(gold).lower().startswith('none of these'):
                    bl = labs[opts.index(gold)]
                if bl is not None and ml is not None and {'L:F': 'F', 'L:R': 'R', 'L:O': 'O', 'L:T': 'F', 'L:Fa': 'R'}.get(ml) != bl:
                    tagnotes.append({'id': row['id'], 'file': short, 'form': frm, 'meta_label': ml, 'solver_b_label_of_asked_claim': bl,
                                     'twin_kind': row['meta'].get('twin_kind'), 'twin_of': row['meta'].get('twin_of'),
                                     'gold_agrees': ok, 'spec_item': 's1 "the row\'s claim c" (yes/no: the asked claim) / s10 edge L tag'})
                for k, v in (res.get('notes') or {}).items():
                    agg[k] += v
                if res.get('suspect_unparsed'):
                    agg['rows_with_suspect_unparsed'] += 1
                if dbg:
                    d = {k: v for k, v in res.items()}
                    d.update({'id': row['id'], 'gold': gold, 'ok': ok})
                    dbg.write(json.dumps(d, default=str) + '\n')
        summary[short] = {'rows': n if not a.limit else min(n, a.limit), 'agree': agree}
    tot = sum(s['rows'] for s in summary.values())
    ag = sum(s['agree'] for s in summary.values())
    out = {'solver': 'F4 solver B (model enumeration / Clark completion on re-parsed text)',
           'spec_id': 'F4-G0-v7', 'rows_checked': tot, 'agree': ag,
           'agree_pct': round(100.0 * ag / tot, 3) if tot else 0.0, 'per_file': summary,
           'parse_notes': dict(agg), 'n_mismatches': len(mism), 'mismatches': mism,
           'label_tag_notes_count': len(tagnotes),
           'label_tag_notes_by_twin_kind': dict(collections.Counter(str(t['twin_kind']) for t in tagnotes)),
           'label_tag_notes': tagnotes}
    with open(a.out, 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: out[k] for k in ('rows_checked', 'agree', 'agree_pct', 'per_file', 'n_mismatches')}))
    print(json.dumps(dict(agg)))


if __name__ == '__main__':
    main(sys.argv[1:])
