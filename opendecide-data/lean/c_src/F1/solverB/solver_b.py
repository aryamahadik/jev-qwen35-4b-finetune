#!/usr/bin/env python3
"""F1 solver B (independent solver for G2, round 1).

Written only from c_src/F1/G0_SPEC.md (v7, frozen) sections 1, 2, 4, 6 and the row format; never from solver A's
code (c_src/F1/gen/ is not read). Paradigm: the rendered row is parsed back into fact tables (fields, rules, notices,
policy, case); gold is re-derived declaratively: every rule's status (in force / met / switched off / applies) is a
set computed as a fixpoint over the exception graph, the open world is an explicit completion table over critical
points, and the depth A test enumerates all notice subsets. z3 is not installed in the project venv, so the
SMT encoding named in the spec is replaced by this exhaustive table/fixpoint encoding (same decision procedure).
Output: per-row answer + depth; the runner compares with the row's stored gold / meta.depth.
"""
import json, re, sys, csv, io, itertools, textwrap
from decimal import Decimal
from datetime import date, timedelta
from html.parser import HTMLParser

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


class ParseError(Exception):
    pass


# ----------------------------------------------------------------------------------------------------------------
# 1. Container normalisation: any format style -> list of units ('line', text) | ('kv', key, value) |
#    ('sec', title) | ('table', [[(header, cell), ...], ...])
# ----------------------------------------------------------------------------------------------------------------
GENERIC_KEYS = {'title', 'name', 'notes', 'summary', 'text', 'body', 'header', 'heading', 'note', 'intro',
                'content', 'description', 'line', 'value', 'subject', 'greeting', 'closing', 'sign off', 'signoff',
                'p', 'paragraph', 'statement', 'item', 'entry', 'from', 'to', 'cc'}


def fmt_scalar(v):
    if v is True:
        return 'yes'
    if v is False:
        return 'no'
    if v is None:
        return ''
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, float):
        s = repr(v)
        return s
    return str(v)


def decamel(k):
    """camelCase / PascalCase record keys (held-out styles) -> lower-case words."""
    if ' ' not in k and '_' not in k and re.search(r'[a-z0-9][A-Z]', k):
        return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', k).lower()
    return k


def _walk(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            kk = decamel(str(k)).replace('_', ' ').strip()
            if isinstance(v, (dict, list)):
                out.append(('sec', kk))
                _walk(v, out)
            else:
                vs = fmt_scalar(v)
                if kk.lower() in GENERIC_KEYS:
                    out.append(('line', vs))
                else:
                    out.append(('kv', kk, vs))
    elif isinstance(o, list):
        flat = o and all(isinstance(x, dict) for x in o) and all(
            not any(isinstance(v, (dict, list)) for v in x.values()) for x in o)
        if flat and any(any(str(k).lower() in ('outcome', 'result') for k in x) for x in o):
            out.append(('table', [[(str(k).replace('_', ' '), fmt_scalar(v)) for k, v in x.items()] for x in o]))
        else:
            for x in o:
                if isinstance(x, dict):
                    out.append(('sec', ''))
                    _walk(x, out)
                elif isinstance(x, list):
                    _walk(x, out)
                else:
                    out.append(('line', fmt_scalar(x)))
    else:
        out.append(('line', fmt_scalar(o)))


BLOCK_TAGS = {'p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'section', 'article', 'header', 'footer',
              'ul', 'ol', 'table', 'thead', 'tbody', 'pre', 'blockquote', 'dt', 'dd', 'dl', 'main', 'aside', 'hr',
              'caption', 'figure', 'nav', 'details', 'summary'}


class _H(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.table = None
        self.row = None
        self.cell = None

    def flush(self):
        t = ''.join(self.buf).strip()
        self.buf = []
        if t:
            for ln in t.split('\n'):
                if ln.strip():
                    self.out.append(('line', ln.strip()))

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.flush()
            self.table = []
        elif tag == 'tr' and self.table is not None:
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []
        elif tag in BLOCK_TAGS and self.cell is None:
            self.flush()

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == 'table' and self.table is not None:
            self.out.append(('rawtable', self.table))
            self.table = None
        elif tag == 'dt' and self.cell is None:
            self.dt_key = ' '.join(''.join(self.buf).split())
            self.buf = []
        elif tag == 'dd' and self.cell is None and getattr(self, 'dt_key', None):
            self.out.append(('kv', self.dt_key, ' '.join(''.join(self.buf).split())))
            self.buf = []
            self.dt_key = None
        elif tag in BLOCK_TAGS and self.cell is None:
            self.flush()

    def handle_data(self, d):
        if self.cell is not None:
            self.cell.append(d)
        else:
            self.buf.append(d)


def rawtable_to_units(rows):
    """rows: list of cell lists, first = header. Decision tables (an outcome column) stay tables; 2-column
    record tables become kv units."""
    rows = [r for r in rows if r and not all(re.fullmatch(r':?-{2,}:?|=+', c.strip()) for c in r if c.strip())]
    if not rows:
        return []
    hdr = [h.strip() for h in rows[0]]
    if any(h.lower() in ('outcome', 'result') for h in hdr):
        return [('table', [list(zip(hdr, [c.strip() for c in r])) for r in rows[1:]])]
    out = []
    if len(hdr) == 2:
        if hdr[0].lower() not in ('field', 'fact', 'item', 'key', 'detail', 'attribute', 'name', 'property'):
            out.append(('kv', hdr[0], hdr[1]))
        for r in rows[1:]:
            if len(r) >= 2:
                out.append(('kv', r[0].strip(), r[1].strip()))
        return out
    for r in rows:
        out.append(('line', ' | '.join(r)))
    return out


BULLET = re.compile(r'^\s*(?:[-*•+>]|\d{1,3}[.)]|\(\d{1,3}\)|[a-z][.)])\s+')
HDR_DECOR = re.compile(r'^\s*(?:#{1,6}\s*|={2,}\s*|-{3,}\s*$|\*{3,}\s*$)')


def clean_line(ln):
    s = ln.strip()
    s = HDR_DECOR.sub('', s)
    s = re.sub(r'\s*={2,}\s*$', '', s)
    s = BULLET.sub('', s)
    s = s.replace('**', '').replace('__', '')
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in '"\'' and s.count(s[0]) == 2:
        s = s[1:-1]
    if s.startswith('[') and s.endswith(']') and ':' in s and s.count('[') == 1:
        s = s[1:-1]
    if s.startswith('`') and s.endswith('`'):
        s = s.strip('`')
    return s.strip()


def _text_units(s):
    lines = s.split('\n')
    out = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        st = ln.strip()
        # pipe tables (markdown or bare "a | b | c")
        if st.count('|') >= 2 or (st.startswith('|') and st.count('|') >= 1 and len(st) > 2):
            j = i
            grp = []
            while j < n and (lines[j].strip().count('|') >= 2 or (lines[j].strip().startswith('|') and len(lines[j].strip()) > 2)):
                cells = [c.strip() for c in lines[j].strip().strip('|').split('|')]
                grp.append(cells)
                j += 1
            out.extend(rawtable_to_units(grp))
            i = j
            continue
        # fixed-width / csv decision tables: a block that holds an 'Otherwise' row
        if re.match(r'^\s*(Row|Otherwise|Line|Entry)\b', st) or re.search(r'\S {2,}\S', st) and re.search(r'(?i)\boutcome\b', st):
            j = i
            grp = []
            while j < n and lines[j].strip() and (re.search(r'\S {2,}\S', lines[j]) or ',' in lines[j]) and not re.match(r'^\s*[-=]{3,}\s*$', lines[j]):
                grp.append(lines[j])
                j += 1
            if any(re.match(r'^\s*Otherwise\b', g.strip()) for g in grp) and len(grp) >= 2:
                if all(re.search(r'\S {2,}\S', g) for g in grp):
                    rows = [re.split(r'\s{2,}', g.strip()) for g in grp]
                else:
                    rows = list(csv.reader(io.StringIO('\n'.join(g.strip() for g in grp))))
                out.extend(rawtable_to_units(rows))
                i = j
                continue
        c = clean_line(ln)
        if c and not re.fullmatch(r'[-=*_#`~\s]+', c):
            out.append(('line', c))
        i += 1
    return out


def _post(units):
    """turn rawtable units into table/kv units and clean line units."""
    out = []
    for u in units:
        if u[0] == 'rawtable':
            out.extend(rawtable_to_units(u[1]))
        elif u[0] == 'line':
            for part in u[1].split('\n'):
                c = clean_line(part)
                if c and not re.fullmatch(r'[-=*_#`~\s]+', c):
                    out.append(('line', c))
        else:
            out.append(u)
    return out


def normalize(state):
    s = '\n'.join(l for l in state.split('\n') if not re.match(r'^\s*```', l))
    s = textwrap.dedent(s).strip('\n')
    st = s.strip()
    if st[:1] in '{[':
        try:
            o = json.loads(st)
            out = []
            _walk(o, out)
            return _post(out), 'json'
        except Exception:
            pass
    if re.search(r'<(p|div|h\d|section|article|table|ul|li|header)\b[^>]*>', st):
        h = _H()
        h.feed(st)
        h.flush()
        return _post(h.out), 'html'
    if yaml is not None and re.match(r'^(#[^\n]*\n)?\s*[\w ]+:', st) and re.search(r'\n\s*-\s', st):
        try:
            o = yaml.safe_load(st)
            if isinstance(o, dict) and len(o) >= 2:
                out = []
                _walk(o, out)
                m = re.match(r'^#\s*(.+)', st)
                if m:
                    out.insert(0, ('line', m.group(1).strip()))
                return _post(out), 'yaml'
        except Exception:
            pass
    return _text_units(s), 'text'


# ----------------------------------------------------------------------------------------------------------------
# 2. Sentences, dates, numbers
# ----------------------------------------------------------------------------------------------------------------
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9\'"(\[])')


def split_sentences(t):
    t = t.replace('e.g.', 'e\x01g\x01').replace('i.e.', 'i\x01e\x01')
    parts = []
    depth = 0
    cur = ''
    # do not split inside brackets
    i = 0
    for piece in re.split(r'(\s+)', t):
        cur += piece
        depth += piece.count('[') + piece.count('(') - piece.count(']') - piece.count(')')
        if piece.isspace() is False and depth <= 0 and re.search(r'[.!?]$', piece):
            parts.append(cur)
            cur = ''
    if cur.strip():
        parts.append(cur)
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(p.replace('e\x01g\x01', 'e.g.').replace('i\x01e\x01', 'i.e.'))
    # re-merge pieces that start lowercase (not a sentence start) or that are decimal tails
    merged = []
    for p in out:
        if merged and (not re.match(r'[A-Z0-9\'"(\[]', p)) and not re.match(r'^[a-z][^:.]{0,80}: \S', p):
            merged[-1] = merged[-1] + ' ' + p
        else:
            merged.append(p)
    return merged


MONTHS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                                           'september', 'october', 'november', 'december'])}
DATE_RE = r'(?:\d{4}-\d{2}-\d{2}|\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})'


def parse_date(s):
    s = s.strip().strip('.').strip()
    m = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r'(\d{1,2}) ([A-Za-z]+) (\d{4})', s)
    if m and m.group(2).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
    m = re.fullmatch(r'([A-Za-z]+) (\d{1,2}), (\d{4})', s)
    if m and m.group(1).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    raise ParseError('bad date %r' % s[:40])


NUM_RE = r'-?\d[\d,]*(?:\.\d+)?'


def parse_num(s):
    return Decimal(s.replace(',', ''))


# ----------------------------------------------------------------------------------------------------------------
# 3. Fields block
# ----------------------------------------------------------------------------------------------------------------
def nkey(s):
    return ' '.join(s.replace('_', ' ').lower().split()).strip(' .:')


class Field:
    def __init__(self, name, typ, unit=None, step=None, lo=None, hi=None, values=None):
        self.name, self.typ, self.unit, self.step, self.lo, self.hi = name, typ, unit, step, lo, hi
        self.values = values
        self.key = nkey(name)

    def __repr__(self):
        return 'Field(%s,%s,%s,%s,%s,%s,%s)' % (self.key, self.typ, self.unit, self.step, self.lo, self.hi, self.values)


def split_values(inner):
    return [v.strip() for v in inner.split(',') if v.strip()]


def parse_field_def(name, d):
    d = d.strip().rstrip('.').strip()
    if d == 'a yes/no fact':
        return Field(name, 'bool')
    if d == 'a date':
        return Field(name, 'date')
    m = re.fullmatch(r'a date from (.+) to (.+)', d)
    if m:
        return Field(name, 'date', step=1, lo=parse_date(m.group(1)), hi=parse_date(m.group(2)))
    m = re.fullmatch(r'one of [\[(](.*)[\])]', d)
    if m:
        return Field(name, 'cat', values=split_values(m.group(1)))
    m = re.fullmatch(r'an amount in (.+?), to the cent, from (%s) ?(.*?) to (%s) ?(.*)' % (NUM_RE, NUM_RE), d)
    if m:
        return Field(name, 'num', unit=m.group(1), step=Decimal('0.01'), lo=parse_num(m.group(2)), hi=parse_num(m.group(4)))
    m = re.fullmatch(r'a whole number of (.+?), from (%s) ?(.*?) to (%s) ?(.*)' % (NUM_RE, NUM_RE), d)
    if m:
        return Field(name, 'num', unit=m.group(1), step=Decimal(1), lo=parse_num(m.group(2)), hi=parse_num(m.group(4)))
    m = re.fullmatch(r'a number of (.+?) in multiples of (%s), from (%s) ?(.*?) to (%s) ?(.*)' % (NUM_RE, NUM_RE, NUM_RE), d)
    if m:
        return Field(name, 'num', unit=m.group(1), step=parse_num(m.group(2)), lo=parse_num(m.group(3)), hi=parse_num(m.group(5)))
    return None


FIELD_LINE = re.compile(r'^([A-Za-z][^:]{0,90}?): ((?:a yes/no fact|a date|one of [\[(]|an amount in |a whole number of |a number of ).*)$')


# ----------------------------------------------------------------------------------------------------------------
# 4. Literals.  ('n', key, lo, hi) inclusive range on the step grid (None = open end); ('d', key, lo, hi) dates;
#    ('c', key, 'in'|'out', frozenset(values)); ('b', key, True|False)
# ----------------------------------------------------------------------------------------------------------------
CMP_NUM = [('greater than or equal to', 'ge'), ('less than or equal to', 'le'), ('no less than', 'ge'),
           ('not less than', 'ge'), ('no fewer than', 'ge'), ('no more than', 'le'), ('not more than', 'le'),
           ('a minimum of', 'ge'), ('a maximum of', 'le'), ('at least', 'ge'), ('at most', 'le'),
           ('more than', 'gt'), ('greater than', 'gt'), ('higher than', 'gt'), ('over', 'gt'), ('above', 'gt'),
           ('in excess of', 'gt'), ('less than', 'lt'), ('fewer than', 'lt'), ('lower than', 'lt'),
           ('under', 'lt'), ('below', 'lt'), ('up to', 'le'), ('within', 'le')]
CMP_DATE = [('on or before', 'le'), ('no later than', 'le'), ('on or after', 'ge'), ('no earlier than', 'ge'),
            ('not later than', 'le'), ('not earlier than', 'ge'), ('before', 'lt'), ('after', 'gt'),
            ('earlier than', 'lt'), ('later than', 'gt')]
NEG_CUE = re.compile(r"\b(no|not|n't|never|lacks?|lacking|without|failed|fails|fail|declined|declines|declining|"
                     r"absent|none|nobody|refused|missing|did not|does not|has not|have not|was not|were not|is not)\b|n't\b", re.I)


def strip_unit(v, unit):
    v = v.strip().rstrip('.').strip()
    m = re.match(r'^(%s)\s*(.*)$' % NUM_RE, v)
    if not m:
        raise ParseError('no number in %r' % v[:30])
    rem = m.group(2).strip()
    if rem and unit is not None and rem != unit and rem.lower() != unit.lower():
        raise ParseError('unit mismatch %r vs %r' % (rem[:30], unit))
    return parse_num(m.group(1))


def canon_range(op, val, step):
    if op == 'ge':
        return (val, None)
    if op == 'gt':
        return (val + step, None)
    if op == 'le':
        return (None, val)
    if op == 'lt':
        return (None, val - step)
    raise ParseError(op)


def parse_value_cmp(rest, f):
    """rest = text after '<field> is ' (or an S3 cell).  Returns a literal or None."""
    rest = rest.strip().rstrip('.').strip()
    if f.typ == 'num':
        m = re.fullmatch(r'between (%s)\s*.*? and (%s)\s*.*' % (NUM_RE, NUM_RE), rest)
        if m:
            return ('n', f.key, parse_num(m.group(1)), parse_num(m.group(2)))
        for w, op in CMP_NUM:
            if rest.startswith(w + ' '):
                v = strip_unit(rest[len(w) + 1:], f.unit)
                lo, hi = canon_range(op, v, f.step)
                return ('n', f.key, lo, hi)
        m = re.fullmatch(r'(%s)\s*.*? or (more|less|fewer|above|below|over|under)' % NUM_RE, rest)
        if m:
            v = parse_num(m.group(1))
            return ('n', f.key, v, None) if m.group(2) in ('more', 'above', 'over') else ('n', f.key, None, v)
        return None
    if f.typ == 'date':
        m = re.fullmatch(r'(?:from|between) (%s) (?:to|and) (%s)' % (DATE_RE, DATE_RE), rest)
        if m:
            return ('d', f.key, parse_date(m.group(1)), parse_date(m.group(2)))
        for w, op in CMP_DATE:
            if rest.startswith(w + ' '):
                d = parse_date(rest[len(w) + 1:])
                lo, hi = canon_range(op, d, timedelta(days=1))
                return ('d', f.key, lo, hi)
        return None
    if f.typ == 'cat':
        m = re.fullmatch(r'(not )?one of [\[(](.*)[\])]', rest)
        if m:
            low = {x.lower(): x for x in f.values}
            vals = [low.get(v.lower(), v) for v in split_values(m.group(2))]
            if not all(v in f.values for v in vals):
                raise ParseError('cat value not in domain')
            return ('c', f.key, 'out' if m.group(1) else 'in', frozenset(vals))
        m = re.fullmatch(r'(not )?(.+)', rest)
        low = {x.lower(): x for x in f.values}
        if m and m.group(2).lower() in low:
            return ('c', f.key, 'out' if m.group(1) else 'in', frozenset([low[m.group(2).lower()]]))
        return None
    return None


STOP = set('the a an of to in on for is was were be been being has have had its it this that with by at from and or '
           'as are there their his her our your any case file s'.split())
NEGW = {'no', 'not', 'never', 'lacks', 'lack', 'lacking', 'without', 'failed', 'fails', 'fail', 'declined', 'declines',
        'declining', 'absent', 'none', 'refused', 'did', 'does', 'do', 'n', 't', 'missing'}


SUFFIXES = ('ations', 'ation', 'ments', 'ment', 'ness', 'ings', 'ing', 'edly', 'ures', 'ure', 'ally', 'ers', 'ies',
            'ied', 'ed', 'es', 'er', 'ly', 's', 'e', 'y')


def stem1(t):
    for suf in SUFFIXES:
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            return t[:-len(suf)]
    return t


def stems(s):
    toks = re.findall(r"[a-z0-9]+", s.lower())
    return {stem1(t)[:4] for t in toks if t not in STOP and t not in NEGW and len(t) > 1}


class Ctx:
    """parsing context: fields of the row."""

    def __init__(self, fields, pack_id=None):
        self.fields = fields
        self.by_key = {f.key: f for f in fields}
        self.bools = [f for f in fields if f.typ == 'bool']
        self.bstems = {f.key: stems(f.name) for f in self.bools}
        voc = pack_vocab(pack_id) if pack_id else {}
        self.variants = {}
        for f in self.bools:
            vs = [stems(f.name)]
            for a in voc.get(f.key, []):
                st = stems(re.sub(r'\{[A-Za-z_]+\}', ' ', a))
                if st:
                    vs.append(st)
            self.variants[f.key] = vs
            self.bstems[f.key] = set().union(*vs)

    def match_bool(self, phrase, ents=(), min_score=0.3):
        ps = stems(phrase)
        allst = set().union(*self.bstems.values()) if self.bstems else set()
        for e in ents:
            if e:
                ps -= (stems(e) - allst)
        best, bscore, second = None, 0.0, 0.0
        for f in self.bools:
            sc = -1.0
            for fs in self.variants[f.key]:
                if not fs:
                    continue
                ov = len(ps & fs)
                sc = max(sc, ov / len(fs) + 0.01 * ov - 0.001 * len(ps - fs))
            if sc > bscore:
                best, second, bscore = f, bscore, sc
            elif sc > second:
                second = sc
        if best is None or bscore < min_score or abs(bscore - second) < 1e-9:
            return None
        # r1.1 fix: a cue word that is part of the field's own name ('pull test fail') is not a negation of the
        # phrase; count cues in the phrase beyond those in the field name (parity = negated)
        n_phrase = len(NEG_CUE.findall(phrase))
        n_name = len(NEG_CUE.findall(best.name)) if NEG_CUE.search(best.name or '') else 0
        neg = (n_phrase - n_name) % 2 == 1 if n_name else n_phrase > 0
        return ('b', best.key, not neg)

    def field_prefix(self, s):
        """split '<field> is <rest>' for non-bool fields; returns (field, rest) or None."""
        low = s.lower()
        if low.startswith('the '):
            cands = [low, low[4:]]
        else:
            cands = [low]
        for c in cands:
            off = len(low) - len(c)
            for f in sorted(self.fields, key=lambda f: -len(f.key)):
                if f.typ == 'bool':
                    continue
                if c.startswith(f.key + ' is ') or c.startswith(f.key + ' was '):
                    k = len(f.key) + (4 if c[len(f.key):].startswith(' is ') else 5)
                    return f, s[off + k:]
        return None

    def parse_literal(self, s, ents=()):
        s = s.strip().rstrip('.').strip()
        fp = self.field_prefix(s)
        if fp:
            lit = parse_value_cmp(fp[1], fp[0])
            if lit is not None:
                return lit
            raise ParseError('literal value: %r' % s[:80])
        b = self.match_bool(s, ents)
        if b is None:
            raise ParseError('literal: %r' % s[:80])
        return b


# ----------------------------------------------------------------------------------------------------------------
# 5. Conditions: items ('lit', L) ('or', fs) ('xor', fs) ('all', fs) ('any', fs) ('kofn', k, fs) ('not', L)
# ----------------------------------------------------------------------------------------------------------------
def split_top(s, sep):
    out, depth, cur, i = [], 0, '', 0
    while i < len(s):
        ch = s[i]
        if ch in '[(':
            depth += 1
        elif ch in '])':
            depth -= 1
        if depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur = ''
            i += len(sep)
            continue
        cur += ch
        i += 1
    out.append(cur)
    return out


LIST_RE = re.compile(r'^(any|all|at least (\d+)) of the following (?:hold|holds|apply|are met|is met)?:?\s*[\[(](.*)[\])]$', re.S)


def parse_item(p, ctx, ents):
    p = p.strip()
    m = LIST_RE.match(p)
    if m:
        mem = [x for x in split_top(m.group(3), ';') if x.strip()]
        lits = frozenset(ctx.parse_literal(x, ents) for x in mem)
        if m.group(1) == 'any':
            return ('any', lits)
        if m.group(1) == 'all':
            return ('all', lits)
        return ('kofn', int(m.group(2)), lits)
    ors = split_top(p, ' or ')
    if len(ors) >= 2:
        try:
            return ('or', frozenset(ctx.parse_literal(x, ents) for x in ors))
        except ParseError:
            pass
    return ('lit', ctx.parse_literal(p, ents))


def parse_condition(text, ctx, ents=()):
    text = text.strip()
    m = re.fullmatch(r'(.+?),? or both', text)
    if m:
        return [('or', frozenset(ctx.parse_literal(x, ents) for x in split_top(m.group(1), ' or ')))]
    m = re.fullmatch(r'either (.+?) or (.+?),? but not both', text)
    if m:
        return [('xor', frozenset([ctx.parse_literal(m.group(1), ents), ctx.parse_literal(m.group(2), ents)]))]
    pieces = split_top(text, ' and ')

    def rec(i):
        if i == len(pieces):
            return []
        err = None
        for j in range(i + 1, len(pieces) + 1):
            try:
                it = parse_item(' and '.join(pieces[i:j]), ctx, ents)
            except ParseError as e:
                err = e
                continue
            try:
                return [it] + rec(j)
            except ParseError as e:
                err = e
        raise err or ParseError('cond')
    items = rec(0)
    return items


# ----------------------------------------------------------------------------------------------------------------
# 6. Rules and notices
# ----------------------------------------------------------------------------------------------------------------
class Rule:
    def __init__(self, rid, kind, items, outcome=None, target=None, tier=None, date_=None, last=None):
        self.id, self.kind, self.items, self.outcome, self.target = rid, kind, items, outcome, target
        self.tier, self.date, self.last = tier, date_, last
        self.rank = None

    def copy(self):
        r = Rule(self.id, self.kind, list(self.items), self.outcome, self.target, self.tier, self.date, self.last)
        r.rank = self.rank
        return r

    def __repr__(self):
        return 'Rule(%s,%s,t=%s,o=%s,tier=%s,d=%s,last=%s,items=%s)' % (self.id, self.kind, self.target, self.outcome,
                                                                        self.tier, self.date, self.last, self.items)


class Notice:
    def __init__(self, num, typ, target, rule, eff, iss, body, pos=None):
        self.num, self.typ, self.target, self.rule, self.eff, self.iss, self.body = num, typ, target, rule, eff, iss, body
        self.pos = pos

    def __repr__(self):
        return 'Notice(%s,%s,t=%s,eff=%s,iss=%s,pos=%s,rule=%s)' % (self.num, self.typ, self.target, self.eff, self.iss,
                                                                   self.pos, self.rule)


RULE_HEAD = re.compile(r'^(?P<lab>[A-Z][A-Za-z]*(?: [a-z]+)?) (?P<id>\d+)(?: \((?P<par>[^()]*(?:\([^()]*\)[^()]*)*)\))?: (?P<body>.+)$')
LAST_RE = re.compile(r'^(?:This|That|The) [a-z]+(?: \d+)? (?:is|stays|remains) in force (?:only )?for cases whose (.+?) is on or before (%s)\.?$' % DATE_RE)
LAST_IN = re.compile(r'in force for cases whose (.+?) is on or before (%s)' % DATE_RE)


def parse_paren(par, rule_kw):
    out = {'target': None, 'tier': None, 'date': None, 'last': None}
    if not par:
        return out
    for p in [x.strip() for x in par.split(';')]:
        m = re.fullmatch(r'exception to (?:[A-Za-z]+ )?(\d+)', p, re.I)
        if m:
            out['target'] = int(m.group(1))
            continue
        m = re.fullmatch(r'in force from (%s)' % DATE_RE, p)
        if m:
            out['date'] = parse_date(m.group(1))
            continue
        m = LAST_IN.search(p)
        if m:
            out['last'] = parse_date(m.group(2))
            continue
        m = re.fullmatch(r'(.+?) tier', p)
        if m:
            out['tier'] = m.group(1).strip().lower()
            continue
        raise ParseError('paren part %r' % p[:40])
    return out


def parse_rule_body(rid, par, body, ctx, ents, gov=None):
    pp = parse_paren(par, None)
    body = body.strip()
    last = pp['last']
    # trailing last-applicable sentence inside the same body
    m = re.search(r'\.\s+(?:This|That|The) [a-z]+(?: \d+)? (?:is|stays|remains) in force (?:only )?for cases whose (.+?) is on or before (%s)\.?$' % DATE_RE, body)
    if m:
        last = parse_date(m.group(2))
        body = body[:m.start()]
    body = body.rstrip('.').strip()
    unl = None
    m = re.fullmatch(r'The outcome is (.+?) only if (.+)', body)
    if m:
        return Rule(rid, 'onlyif', parse_condition(m.group(2), ctx, ents), m.group(1).strip(), None, pp['tier'], pp['date'], last)
    m = re.fullmatch(r'If (.+?), (?:[A-Za-z]+ )?(\d+) (?:is switched off|does not apply)(?: and the outcome is (.+?))?(?:, unless (.+))?', body)
    if m:
        items = parse_condition(m.group(1), ctx, ents)
        if m.group(4):
            items.append(('not', ctx.parse_literal(m.group(4), ents)))
        tgt = int(m.group(2))
        kind = 'oexc' if m.group(3) else 'pexc'
        return Rule(rid, kind, items, m.group(3).strip() if m.group(3) else None, tgt, pp['tier'], pp['date'], last)
    m = re.fullmatch(r'(?:[A-Za-z]+ )?(\d+) does not apply if (.+)', body)
    if m:
        return Rule(rid, 'pexc', parse_condition(m.group(2), ctx, ents), None, int(m.group(1)), pp['tier'], pp['date'], last)
    m = re.fullmatch(r'If (.+?), the outcome is (.+?)(?:, unless (.+))?', body)
    if m:
        items = parse_condition(m.group(1), ctx, ents)
        if m.group(3):
            items.append(('not', ctx.parse_literal(m.group(3), ents)))
        return Rule(rid, 'gen', items, m.group(2).strip(), pp['target'], pp['tier'], pp['date'], last)
    raise ParseError('rule body: %r' % body[:90])


NOTICE_HEAD = re.compile(r'^(?P<lab>[A-Z][A-Za-z]*(?: [a-z]+)?) (?P<n>\d+) from (?P<body>.+?) \((?P<dates>[^()]*)\): (?P<rest>.+)$')
REF_RE = re.compile(r'^(?:The )?(?P<what>[A-Za-z][A-Za-z \-]*?) reference(?: is|:)\s*(?P<ref>.+?)\.?$')


def parse_notice_dates(d):
    iss = eff = None
    for p in d.split(';'):
        p = p.strip()
        m = re.fullmatch(r'issued (?:on )?(%s)' % DATE_RE, p)
        if m:
            iss = parse_date(m.group(1))
            continue
        m = re.fullmatch(r'(?:effective|takes effect|in force from)(?: on)? (%s)' % DATE_RE, p)
        if m:
            eff = parse_date(m.group(1))
            continue
        raise ParseError('notice dates %r' % p[:40])
    if eff is None:
        raise ParseError('notice without effective date')
    return iss, eff


def unit_texts(units):
    """flatten to a list of (kind, payload, section) where kind in s (sentence) / kv / table."""
    out = []
    sec = ''
    for u in units:
        if u[0] == 'sec':
            sec = u[1]
            out.append(('sec', u[1], sec))
        elif u[0] == 'table':
            out.append(('table', u[1], sec))
        elif u[0] == 'kv':
            k, v = u[1], u[2]
            if re.fullmatch(r'[a-z]', k.strip()) or k.strip().isdigit():
                for s in split_sentences(v):
                    out.append(('s', s, sec))
            else:
                out.append(('kv', (k, v), sec))
        else:
            t = u[1]
            for s in split_sentences(t):
                out.append(('s', s, sec))
    return out


def kv_as_sentence(k, v):
    return '%s: %s' % (k[:1].upper() + k[1:], v)


HDR_ISSUED = re.compile(r'^Issued by (.+?)\.$')
HDR_BASE = re.compile(r'^Base policy effective (%s)\.?$' % DATE_RE)
HDR_SCOPE = re.compile(r"^This policy covers cases whose (.+?) is (.+?); a case's governing date is its (.+?)\.$")


class Case:
    def __init__(self, ref):
        self.ref = ref
        self.vals = {}
        self.neg_seen = set()
        self.notrec = set()
        self.junk = []


JUNK_RE = re.compile(r"(?i)\b(ignore|disregard|pick|choose|select|override|treat this|answer|instruction|system message|"
                     r"note to the reader|correct answer|option listed|first option|second option|last option|"
                     r"skip the rules|without reading)\b")


def parse_fact(t, ctx, case, ents):
    """t: one case sentence or 'key: value'. Returns True if it set a fact."""
    t = t.strip()
    m = re.match(r'^([^:]{1,90}): (.+)$', t)
    if m and nkey(m.group(1)) in ctx.by_key:
        f = ctx.by_key[nkey(m.group(1))]
        return set_val(case, f, m.group(2), ctx)
    if m:
        alt = {re.sub(r'[-/]', ' ', k): f for k, f in ctx.by_key.items()}
        k2 = ' '.join(re.sub(r'[-/]', ' ', nkey(m.group(1))).split())
        if k2 in alt:
            return set_val(case, alt[k2], m.group(2), ctx)
    m = re.match(r'^(?:The |the )?(.+?) (?:is|was|are|were) (.+?)\.?$', t)
    if m:
        fp = ctx.field_prefix(t.rstrip('.'))
        if fp:
            return set_val(case, fp[0], fp[1], ctx)
    if re.search(r'not recorded', t, re.I):
        for f in ctx.fields:
            if f.key in t.lower():
                case.notrec.add(f.key)
                return True
    if t.endswith(',') or JUNK_RE.search(t):
        case.junk.append(t)
        return False
    b = ctx.match_bool(t, ents, min_score=0.6)
    if b is not None and len(stems(t) & ctx.bstems[b[1]]) >= 1:
        k = b[1]
        if k in case.vals and case.vals[k] != b[2]:
            raise ParseError('bool fact twice with different values: %s' % k)
        case.vals[k] = b[2]
        return True
    case.junk.append(t)
    return False


def set_val(case, f, v, ctx):
    v = v.strip().rstrip('.').strip().strip('"').strip()
    if re.fullmatch(r"(?i)not recorded|\(?not recorded\)?|\[not recorded\]", v):
        case.notrec.add(f.key)
        return True
    if f.typ == 'bool':
        lv = v.lower()
        if lv in ('yes', 'true', 'y'):
            case.vals[f.key] = True
        elif lv in ('no', 'false', 'n'):
            case.vals[f.key] = False
        else:
            raise ParseError('bool value %r' % v[:20])
    elif f.typ == 'num':
        case.vals[f.key] = strip_unit(v, f.unit)
    elif f.typ == 'date':
        case.vals[f.key] = parse_date(v)
    elif f.typ == 'cat':
        if v not in f.values:
            low = {x.lower(): x for x in f.values}
            if v.lower() in low:
                v = low[v.lower()]
            else:
                raise ParseError('cat value %r' % v[:30])
        case.vals[f.key] = v
    return True


def compile_table(rows, ctx):
    rules, default = [], None
    for r in rows:
        if not r:
            continue
        label = r[0][1].strip()
        outc = [c for h, c in r if nkey(h) in ('outcome', 'result')]
        if len(outc) != 1:
            raise ParseError('table row without outcome')
        outc = outc[0].strip()
        if label.lower().startswith('otherwise'):
            default = outc
            continue
        m = re.search(r'(\d+)', label)
        if not m:
            raise ParseError('table row label %r' % label[:20])
        items, tier, d = [], None, None
        for h, c in r[1:]:
            hk, c = nkey(h), c.strip()
            if hk in ('outcome', 'result'):
                continue
            if (hk == 'tier' or hk.endswith(' tier')) and hk not in ctx.by_key:
                tier = re.sub(r'\s*tier$', '', c.lower()).strip()
                continue
            if ('in force from' in hk or hk in ('date', 'in force', 'effective', 'from', 'took effect')) and hk not in ctx.by_key:
                d = parse_date(c)
                continue
            if c.lower() in ('any', '-', '', 'any tier', 'n/a'):
                continue
            f = ctx.by_key.get(hk)
            if f is None:
                raise ParseError('table header %r' % hk[:40])
            if f.typ == 'bool':
                if c.lower() not in ('yes', 'no', 'true', 'false'):
                    raise ParseError('bool cell %r' % c[:20])
                items.append(('lit', ('b', f.key, c.lower() in ('yes', 'true'))))
            else:
                lit = parse_value_cmp(re.sub(r'^is ', '', c), f)
                if lit is None:
                    raise ParseError('cell %r' % c[:40])
                items.append(('lit', lit))
        rules.append(Rule(int(m.group(1)), 'gen', items, outc, None, tier, d))
    return rules, default


class Parsed:
    pass


def parse_state(state, pack_id=None):
    units, mode = normalize(state)
    its = unit_texts(units)
    return parse_its(its, mode, pack_id)


def parse_its(its, mode, pack_id=None):
    P = Parsed()
    P.mode = mode
    fields, seen = [], set()
    P.body = P.B = P.gov = P.scope = P.entity = None
    for kind, p, sec in its:
        t = p if kind == 's' else (kv_as_sentence(*p) if kind == 'kv' else None)
        if t is None:
            continue
        m = FIELD_LINE.match(t)
        if m:
            f = parse_field_def(m.group(1), m.group(2))
            if f is not None and f.key not in seen:
                seen.add(f.key)
                fields.append(f)
            continue
        m = HDR_ISSUED.match(t)
        if m and P.body is None:
            P.body = m.group(1).strip()
        m = HDR_BASE.match(t)
        if m and P.B is None:
            P.B = parse_date(m.group(1))
        m = HDR_SCOPE.match(t)
        if m and P.gov is None:
            P.scope = (m.group(1), m.group(2))
            P.gov = nkey(m.group(3))
        m = re.match(r'^(?:[^:]+): (.+?) (?:policy|flowchart)$', t)
        if m and P.entity is None:
            P.entity = m.group(1).strip().lower()
    if P.body is None or P.B is None or P.gov is None:
        raise ParseError('header incomplete')
    P.fields = fields
    ctx = Ctx(fields, pack_id)
    P.ctx = ctx
    if P.gov not in ctx.by_key:
        raise ParseError('governing field not in Fields block')
    walk_state(P, its, ctx)
    return P


def walk_state(P, its, ctx):
    P.rules, P.notices, P.cases, P.tables, P.inert, P.other = {}, [], [], [], [], []
    pending = None
    last_rule = None
    cur = None
    in_case = False
    ents = [e for e in [P.entity] if e]
    for kind, p, sec in its:
        if kind == 'sec':
            continue
        if kind == 'table':
            P.tables.append(p)
            in_case = False
            continue
        t = p if kind == 's' else kv_as_sentence(*p)
        if FIELD_LINE.match(t) or HDR_ISSUED.match(t) or HDR_BASE.match(t) or HDR_SCOPE.match(t):
            in_case = False
            continue
        m = re.match(r'^(?:Draft|Proposed)[a-z ]* from (.+?) \((.*?)\): (.+)$', t)
        if m:
            in_case = False
            rest = m.group(3)
            mm = re.search(r'(\d+) is replaced by the following text|A new [a-z]+ (\d+) is added', rest)
            d = Notice(None, 'draft', int(mm.group(1) or mm.group(2)) if mm else None, None, None, None, m.group(1))
            P.inert.append(d)
            pending = d if mm else None
            continue
        m = NOTICE_HEAD.match(t)
        if m:
            in_case = False
            iss, eff = parse_notice_dates(m.group('dates'))
            body = m.group('body').strip()
            rest = m.group('rest').strip()
            inert = body != P.body
            mm = re.fullmatch(r'(?:[A-Za-z]+ )?(\d+) is repealed\.?', rest)
            if mm:
                n = Notice(int(m.group('n')), 'repeal', int(mm.group(1)), None, eff, iss, body)
                pending = None
            else:
                mm = re.fullmatch(r'(?:[A-Za-z]+ )?(\d+) is replaced by the following text\.?', rest)
                mi = re.fullmatch(r'A new [a-z]+ (\d+) is added(?: (at the top|at the bottom|directly below (?:[A-Za-z]+ )?(\d+)))?\.?', rest)
                if mm:
                    n = Notice(int(m.group('n')), 'replace', int(mm.group(1)), None, eff, iss, body)
                elif mi:
                    pos = None
                    if mi.group(2):
                        pos = 'top' if 'top' in mi.group(2) else ('bottom' if 'bottom' in mi.group(2) else ('after', int(mi.group(3))))
                    n = Notice(int(m.group('n')), 'insert', int(mi.group(1)), None, eff, iss, body, pos)
                else:
                    raise ParseError('notice rest %r' % rest[:60])
                pending = n
            (P.inert if inert else P.notices).append(n)
            continue
        m = RULE_HEAD.match(t)
        if m and re.match(r'(If |The outcome is |Either |(?:[A-Z][a-z]+ )?\d+ does not apply if )', m.group('body')) and not re.match(
                r"If (all rules|no rule|rules with|the tie rule|an 'only if'|any of these fields|the missing)", m.group('body')):
            in_case = False
            rid = int(m.group('id'))
            r = parse_rule_body(rid, m.group('par'), m.group('body'), ctx, ents)
            if pending is not None:
                if pending.target != rid:
                    raise ParseError('notice text id mismatch')
                pending.rule = r
                pending = None
            else:
                if rid in P.rules:
                    raise ParseError('duplicate rule id %d' % rid)
                P.rules[rid] = r
            last_rule = r
            continue
        m = LAST_RE.match(t)
        if m and last_rule is not None:
            last_rule.last = parse_date(m.group(2))
            continue
        m = REF_RE.match(t)
        if m and not re.search(r'\d+ (?:is|was) ', t):
            cur = Case(m.group('ref').strip())
            P.cases.append(cur)
            in_case = True
            if m.group('what').lower() not in ('case',):
                ents.append(m.group('what').lower())
            continue
        if in_case:
            parse_fact(t, ctx, cur, ents + [cur.ref])
            continue
        P.other.append(t)


# ----------------------------------------------------------------------------------------------------------------
# 7. Pack vocabulary (spec 4: the parser may use the pack's declared vocabulary).  Schema-agnostic: every dict in the
#    pack whose name/label/term/key equals a field name contributes its alias / phrase / statement strings.
# ----------------------------------------------------------------------------------------------------------------
PACK_FILES = ['packs-1/packs.jsonl', 'packs-2/packs.jsonl', 'packs-3/packs-3.jsonl', 'packs-4/packs.jsonl']
PACK_ROOT = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/packs/'
_PACKS = None
_PACK_IDX = {}
ALIAS_KEYS = {'aliases', 'alias', 'synonyms', 'phrases', 'pos_statement', 'neg_statement', 'statements', 'positive',
              'negative', 'true_phrase', 'false_phrase', 'phrasings', 'true', 'false', 'pos', 'neg', 'surface',
              'surfaces', 'renderings', 'yes', 'no', 'statement', 'phrase', 'lexicon', 'true_text', 'false_text',
              'positive_phrase', 'negative_phrase', 'yes_phrase', 'no_phrase', 'variants', 'term'}
NAME_KEYS = ('name', 'label', 'term', 'key', 'field', 'attribute')


def _strings(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, list):
        for x in o:
            _strings(x, out)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ALIAS_KEYS:
                _strings(v, out)


def _index_pack(o, idx):
    if isinstance(o, dict):
        for nk in NAME_KEYS:
            v = o.get(nk)
            if isinstance(v, str):
                key = nkey(v)
                lst = idx.setdefault(key, [])
                _strings({k: vv for k, vv in o.items() if k in ALIAS_KEYS}, lst)
        for v in o.values():
            _index_pack(v, idx)
    elif isinstance(o, list):
        for x in o:
            _index_pack(x, idx)


def pack_vocab(pack_id):
    global _PACKS
    if _PACKS is None:
        _PACKS = {}
        for f in PACK_FILES:
            try:
                for line in open(PACK_ROOT + f):
                    o = json.loads(line)
                    _PACKS[o.get('id')] = o
            except FileNotFoundError:
                pass
    if pack_id not in _PACK_IDX:
        idx = {}
        if pack_id in _PACKS:
            _index_pack(_PACKS[pack_id], idx)
        _PACK_IDX[pack_id] = idx
    return _PACK_IDX[pack_id]


# ----------------------------------------------------------------------------------------------------------------
# 8. Policy statements (card field on Q3, instructions + Interpretation section on choice rows, document on short rows)
# ----------------------------------------------------------------------------------------------------------------
def classify_prec(t):
    tl = t.lower()
    if 'first row' in tl or 'from the top' in tl or 'top to bottom' in tl:
        return 'ORDER'
    if 'specific' in tl or "all of the other rule's conditions" in tl:
        return 'SPEC'
    if 'latest' in tl or 'took effect later' in tl:
        return 'LATER'
    if 'override' in tl or 'tier' in tl:
        return 'PRIORITY'
    return None


def policy_sentences(texts):
    out = []
    for t in texts:
        if not t:
            continue
        for line in t.split('\n'):
            line = clean_line(line)
            for s in split_sentences(line):
                if re.search(r'(?i)for example|hypothetical', s):
                    continue
                out.append(s)
    return out


def parse_policy(sents):
    pol = {'world': 'closed', 'prim': None, 'sec': None, 'tie': None, 'strict': None, 'default': None,
           'fallback': None, 'M': None, 'mfields': None, 'tiers': None, 'cbd': None, 'none': None, 'codes': {},
           'escalate': None, 'gov_stmt': None}
    for i, s in enumerate(sents):
        sl = s.lower()
        if 'may be incomplete' in sl or 'unknown, not false' in sl:
            pol['world'] = 'open'
        m = re.search(r"marked 'not recorded'.*?the outcome is (.+?), whatever the other rules say: (.+?)\.?$", s)
        if m:
            pol['M'] = m.group(1).strip()
            pol['mfields'] = [nkey(x) for x in re.split(r',\s*(?:and\s+)?|\s+and\s+', m.group(2)) if x.strip()]
        m = re.search(r'If no rule that gives an outcome applies, the outcome is (.+?)\.?$', s)
        if m and pol['default'] is None:
            pol['default'] = m.group(1).strip()
        m = re.search(r'If no rule that gives an outcome applies, the basis is (.+?)\.?$', s)
        if m:
            pol['codes']['D'] = m.group(1).strip()
        m = re.search(r'If the tie rule decides, the basis is (.+?)(?:,|\.?$)', s)
        if m:
            pol['codes']['T'] = m.group(1).strip()
        m = re.search(r"'[Oo]nly if' rule .*?the basis is (.+?)(?:,|\.?$)", s)
        if m:
            pol['codes']['F'] = m.group(1).strip()
        m = re.search(r'missing-field rule decides, the basis is (.+?)(?:,|\.?$)', s)
        if m:
            pol['codes']['M'] = m.group(1).strip()
        m = re.search(r'the outcome is (.+?) instead', s)
        if m:
            pol['fallback'] = m.group(1).strip()
        m = re.search(r'When rules that apply give different outcomes, (.+)$', s)
        if m:
            c = classify_prec(m.group(1))
            if pol['prim'] is None:
                pol['prim'] = c
            if c == 'PRIORITY':
                pol['tiers'] = parse_tiers(m.group(1))
        if pol['prim'] is None and re.search(r'(?i)first row whose conditions are met|checked from the top|from top to bottom', s):
            pol['prim'] = 'ORDER'
        m = re.search(r'still left after (.+?), (.+)$', s)
        if m:
            rest = m.group(2)
            mm = re.match(r'the outcome is (.+?)\.?$', rest)
            if mm:
                pol['tie'] = 'esc'
                pol['escalate'] = mm.group(1).strip()
            elif 'strictest' in rest:
                pol['tie'] = 'strict'
                mm = re.search(r'From strictest to least strict: (.+?)\.?$', rest)
                if not mm and i + 1 < len(sents):
                    mm = re.search(r'From strictest to least strict: (.+?)\.?$', sents[i + 1])
                if mm:
                    pol['strict'] = [x.strip() for x in mm.group(1).split(', ')]
            else:
                pol['sec'] = classify_prec(rest)
                pol['_tb_prim'] = classify_prec(m.group(1))
                if pol['sec'] == 'PRIORITY' and parse_tiers(rest):
                    pol['tiers'] = parse_tiers(rest)
        m = re.search(r"'(.+?)' (?:is the answer only if|means the file does not settle)", s)
        if m:
            pol['cbd'] = m.group(1)
        m = re.search(r"it differs from '(.+?)', which rules can give", s)
        if m:
            pol['escalate'] = m.group(1)
        m = re.search(r"If no listed case gets .*?, (?:the answer is|choose) '(.+?)'\.?$", s)
        if m:
            pol['none'] = m.group(1)
    if pol.get('_tb_prim'):
        pol['prim'] = pol['_tb_prim']
    return pol


def parse_tiers(t):
    m = re.search(r'(.+?) rules override (.+)$', t)
    if not m:
        return None
    first = re.sub(r'^.*?,\s*', '', m.group(1)).strip()
    tiers = [first] + re.findall(r'(?:override|then) (.+?) rules', m.group(0))[0:]
    tiers = [re.sub(r'\s*tier$', '', x.strip().lower()) for x in tiers]
    seen = []
    for x in tiers:
        if x not in seen:
            seen.append(x)
    return seen


# ----------------------------------------------------------------------------------------------------------------
# 9. Declarative evaluation
# ----------------------------------------------------------------------------------------------------------------
def lit_true(L, env):
    k = L[1]
    if k not in env:
        raise ParseError('no value for field %r' % k)
    v = env[k]
    if v is None:
        raise ParseError('field %r has no value' % k)
    if L[0] == 'b':
        return v is L[2]
    if L[0] in ('n', 'd'):
        lo, hi = L[2], L[3]
        return (lo is None or v >= lo) and (hi is None or v <= hi)
    if L[0] == 'c':
        return (v in L[3]) if L[2] == 'in' else (v not in L[3])
    raise ParseError('lit kind')


def item_true(it, env):
    k = it[0]
    if k == 'lit':
        return lit_true(it[1], env)
    if k == 'not':
        return not lit_true(it[1], env)
    if k in ('or', 'any'):
        return any(lit_true(x, env) for x in it[1])
    if k == 'all':
        return all(lit_true(x, env) for x in it[1])
    if k == 'xor':
        return sum(1 for x in it[1] if lit_true(x, env)) == 1
    if k == 'kofn':
        return sum(1 for x in it[2] if lit_true(x, env)) >= it[1]
    raise ParseError('item kind')


def rule_items_closure(rules, rid, seen=None):
    """SPEC items of a rule: own items plus its target's, recursively (A05)."""
    seen = seen or set()
    if rid in seen:
        raise ParseError('exception cycle')
    seen.add(rid)
    r = rules[rid]
    s = set(r.items)
    if r.kind in ('pexc', 'oexc') and r.target in rules:
        s |= rule_items_closure(rules, r.target, seen)
    return frozenset(s)


def in_force(P, g, removed=frozenset()):
    """gold step 2 on the parsed structure. Returns (rules dict id->Rule, order list for ORDER)."""
    rules = {}
    for rid, r in P.rules.items():
        rr = r.copy()
        if rr.date is None:
            rr.date = P.B
        rules[rid] = rr
    order = list(P.base_order)
    ops = [n for n in P.notices if n.num not in removed and n.eff <= g]
    ops.sort(key=lambda n: (n.eff, n.num))
    for n in ops:
        if n.typ == 'repeal':
            rules.pop(n.target, None)
            if n.target in order:
                order.remove(n.target)
        elif n.typ == 'replace':
            old = rules.get(n.target)
            new = n.rule.copy()
            if old is not None:
                new.kind = old.kind if not (old.kind in ('pexc', 'oexc') and new.kind in ('pexc', 'oexc')) else new.kind
                new.target = old.target
            new.date = n.eff
            rules[n.target] = new
            if n.target not in order:
                order.append(n.target)
        elif n.typ == 'insert':
            new = n.rule.copy()
            new.date = n.eff
            rules[n.target] = new
            if n.pos is None or n.pos == 'bottom':
                order.append(n.target)
            elif n.pos == 'top':
                order.insert(0, n.target)
            else:
                k = n.pos[1]
                if k in order:
                    order.insert(order.index(k) + 1, n.target)
                else:
                    order.append(n.target)
    for rid in list(rules):
        if rules[rid].last is not None and rules[rid].last < g:
            del rules[rid]
    changed = True
    while changed:
        changed = False
        for rid in list(rules):
            r = rules[rid]
            if r.kind in ('pexc', 'oexc') and r.target not in rules:
                del rules[rid]
                changed = True
    order = [x for x in order if x in rules]
    for i, rid in enumerate(order):
        rules[rid].rank = i
    return rules


def beats(pol, rules, r, s, closure):
    if pol == 'SPEC':
        return closure[r.id] > closure[s.id]
    if pol == 'LATER':
        return r.date > s.date
    if pol == 'PRIORITY':
        T = closure['__tiers__']
        if r.tier not in T or s.tier not in T:
            raise ParseError('tier missing')
        return T.index(r.tier) < T.index(s.tier)
    if pol == 'ORDER':
        return r.rank < s.rank
    raise ParseError('policy %r' % pol)


def decide(P, env, g, removed=frozenset(), notrec=False):
    """closed case -> dict(outcome, source, win, cands, X, P, O)."""
    pol = P.pol
    if notrec:
        return {'outcome': pol['M'], 'source': 'M', 'win': None, 'X': 0, 'P': 0, 'O': 0, 'cands': []}
    rules = in_force(P, g, removed)
    fires = {}

    def fire(rid):
        if rid in fires:
            return fires[rid]
        r = rules[rid]
        if r.kind == 'onlyif':
            fires[rid] = False
            return False
        ok = all(item_true(it, env) for it in r.items)
        if r.kind in ('pexc', 'oexc'):
            ok = ok and fire(r.target)
        fires[rid] = ok
        return ok
    eff = {}
    targeted = {}
    for rid, r in rules.items():
        if r.kind in ('pexc', 'oexc'):
            targeted.setdefault(r.target, []).append(rid)

    def effective(rid):
        if rid not in eff:
            eff[rid] = fire(rid) and not any(effective(e) for e in targeted.get(rid, []))
        return eff[rid]

    def level(rid):
        r = rules[rid]
        return 1 + level(r.target) if r.kind in ('pexc', 'oexc') else 0
    Xd = max([level(rid) for rid, r in rules.items() if r.kind in ('pexc', 'oexc') and fire(rid)] or [0])
    cands = [r for rid, r in rules.items() if r.kind in ('gen', 'oexc') and fire(rid)
             and not any(effective(e) for e in targeted.get(rid, []))]
    outs = {r.outcome for r in cands}
    Pd = 1 if len(outs) >= 2 else 0
    win = None
    if not cands:
        o, src = pol['default'], 'D'
    elif len(outs) == 1:
        o, src = cands[0].outcome, 'R'
    else:
        closure = {rid: rule_items_closure(rules, rid) for rid in rules} if 'SPEC' in (pol['prim'], pol['sec']) else {}
        closure['__tiers__'] = pol['tiers'] or []
        W = [r for r in cands if not any(beats(pol['prim'], rules, s, r, closure) and s.outcome != r.outcome for s in cands)]
        if len({r.outcome for r in W}) == 1:
            o, src = W[0].outcome, 'R'
        else:
            if pol['sec']:
                W = [r for r in W if not any(beats(pol['sec'], rules, s, r, closure) and s.outcome != r.outcome for s in W)]
            if len({r.outcome for r in W}) == 1:
                o, src = W[0].outcome, 'R'
            elif pol['tie'] == 'esc':
                o, src = pol['escalate'], 'T'
            elif pol['tie'] == 'strict':
                rem = {r.outcome for r in W}
                order = pol['strict']
                if not order or any(x not in order for x in rem):
                    raise ParseError('strictness order incomplete')
                o, src = min(rem, key=order.index), 'T'
            else:
                raise ParseError('no tie rule')
    if src == 'R':
        holders = [r for r in cands if r.outcome == o]
        if len(holders) == 1:
            src, win = 'ONE', holders[0].id
        else:
            src = 'MANY'
    Od = 0
    oi = [r for r in rules.values() if r.kind == 'onlyif' and r.outcome == o]
    if oi and not all(all(item_true(it, env) for it in r.items) for r in oi):
        if pol['fallback'] is None:
            raise ParseError('fallback unknown')
        o, src, win, Od = pol['fallback'], 'F', None, 1
    return {'outcome': o, 'source': src, 'win': win, 'X': Xd, 'P': Pd, 'O': Od, 'cands': cands}


def removal_closure(P, T):
    rem = set(T)
    changed = True
    while changed:
        changed = False
        ins = {n.target for n in P.notices if n.num in rem and n.typ == 'insert'}
        for n in P.notices:
            if n.num in rem:
                continue
            dep = False
            if n.typ in ('replace', 'repeal') and n.target in ins:
                dep = True
            if n.typ == 'insert' and isinstance(n.pos, tuple) and n.pos[1] in ins:
                dep = True
            if n.typ == 'insert' and n.rule is not None and n.rule.kind in ('pexc', 'oexc') and n.rule.target in ins:
                dep = True
            if dep:
                rem.add(n.num)
                changed = True
    return frozenset(rem)


def closed_eval(P, env, g, notrec):
    """returns (decision, depth) for one closed case (section 1 depth algorithm)."""
    d = decide(P, env, g, frozenset(), notrec)
    if d['source'] == 'M':
        return d, 1
    nums = [n.num for n in P.notices]
    changing = []
    for k in range(1, len(nums) + 1):
        for T in itertools.combinations(nums, k):
            T = frozenset(T)
            if any(c < T for c in changing):
                continue
            o2 = decide(P, env, g, removal_closure(P, T), notrec)['outcome']
            if o2 != d['outcome']:
                changing.append(T)
    minimal = [T for T in changing if not any(c < T for c in changing)]
    members = set().union(*minimal) if minimal else set()
    A = sum(1 for n in P.notices if n.num in members and n.eff <= g)
    return d, 1 + d['X'] + A + d['P'] + d['O']


def all_rule_literals(P):
    rs = list(P.rules.values()) + [n.rule for n in P.notices if n.rule is not None]
    for r in rs:
        for it in r.items:
            if it[0] in ('lit', 'not'):
                yield it[1]
            elif it[0] == 'kofn':
                yield from it[2]
            else:
                yield from it[1]


def critical_points(P, f):
    if f.typ == 'bool':
        return [True, False]
    if f.typ == 'cat':
        return list(f.values)
    if f.lo is None or f.hi is None:
        raise ParseError('unknown field without domain: %s' % f.key)
    step = f.step if f.typ == 'num' else timedelta(days=1)
    pts = {f.lo, f.hi}
    for L in all_rule_literals(P):
        if L[1] != f.key:
            continue
        for e in (L[2], L[3]):
            if e is not None:
                pts.update([e - step, e, e + step])
    return sorted(p for p in pts if f.lo <= p <= f.hi)


def case_env(P, case):
    """closed env or list of completions; returns (envs, unknown_keys, notrec_flag)."""
    pol = P.pol
    env = dict(case.vals)
    notrec = False
    if pol['world'] == 'missing':
        lst = set(pol['mfields'] or [])
        if case.notrec & lst:
            notrec = True
        elif case.notrec:
            raise ParseError('not recorded on a non-listed field')
    unknown = []
    for f in P.fields:
        if f.key in env:
            continue
        if pol['world'] == 'open':
            unknown.append(f)
        elif f.typ == 'bool':
            env[f.key] = False
        elif notrec and f.key in case.notrec:
            continue
        elif f.typ == 'date' and f.key != P.gov:
            env[f.key] = None
        else:
            raise ParseError('closed case lacks value for %s' % f.key)
    if len(unknown) > 2:
        raise ParseError('more than 2 unknown fields: %d' % len(unknown))
    envs = []
    for combo in itertools.product(*[critical_points(P, f) for f in unknown]):
        e = dict(env)
        for f, v in zip(unknown, combo):
            e[f.key] = v
        envs.append(e)
    return envs, [f.key for f in unknown], notrec


# ----------------------------------------------------------------------------------------------------------------
# 10. Row: question, options, answer
# ----------------------------------------------------------------------------------------------------------------
def build(row):
    P = parse_state(row['state'], row['meta'].get('domain_pack'))
    P.pol = parse_policy(policy_sentences([row.get('card') or '', row.get('instructions') or ''] + P.other))
    if P.pol['M']:
        P.pol['world'] = 'missing'
    P.base_order = list(P.rules)
    if P.tables:
        if len(P.tables) != 1 or P.rules:
            raise ParseError('table plus prose rules')
        rules, default = compile_table(P.tables[0], P.ctx)
        for r in rules:
            if r.id in P.rules:
                raise ParseError('dup table row')
            P.rules[r.id] = r
        P.base_order = [r.id for r in rules]
        if default is not None:
            if P.pol['default'] is not None and P.pol['default'] != default:
                raise ParseError('table default differs from stated default')
            P.pol['default'] = default
    for n in P.notices:
        if n.typ in ('replace', 'insert') and n.rule is None:
            raise ParseError('notice %s without text' % n.num)
    if P.pol['default'] is None:
        raise ParseError('no default')
    if P.pol['prim'] is None:
        raise ParseError('no precedence')
    if not P.cases:
        raise ParseError('no case')
    return P


def solve_case(P, case):
    envs, unknown, notrec = case_env(P, case)
    res = []
    for e in envs:
        g = e[P.gov]
        if g is None:
            raise ParseError('governing date unknown')
        d, dep = closed_eval(P, e, g, notrec)
        res.append((d, dep))
    return res, unknown


def source_of(res):
    """open-world aggregate gold source and basis key."""
    outs = {d['outcome'] for d, _ in res}
    if len(outs) > 1:
        return 'CBD', None
    srcs = {(d['source'], d['win']) for d, _ in res}
    if len(srcs) == 1:
        s, w = next(iter(srcs))
        return s, w
    return 'mixed', None


def outcome_names(P, row):
    names = set()
    for r in list(P.rules.values()) + [n.rule for n in P.notices if n.rule is not None]:
        if r.outcome:
            names.add(r.outcome)
    for k in ('default', 'fallback', 'M', 'escalate'):
        if P.pol[k]:
            names.add(P.pol[k])
    names.update(P.pol['strict'] or [])
    for t in (row.get('card') or '', row.get('instructions') or ''):
        for line in t.split('\n'):
            m = re.match(r'^\s*(?:[-*•]\s*)?([^:]{1,60}): (.+)$', line)
            if '?' in line:
                continue
            if m and len(m.group(1).split()) <= 8 and not re.search(r'[.?!]', m.group(1)) and (
                    P.entity is None or P.entity in m.group(2).lower()) and len(m.group(2)) < 80:
                names.add(m.group(1).strip())
    return names


def find_x(q, names, refs=()):
    hits = [n for n in names if re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', q)]
    hits = [h for h in hits if not any(h != o and h in o for o in hits)]
    if len(hits) == 0 and refs:
        x = x_from_frame(q, refs)
        if x:
            return x
    if len(hits) != 1:
        raise ParseError('question target not found (%d hits)' % len(hits))
    return hits[0]


def x_from_frame(q, refs):
    """X named only in the question (a card outcome that no rule, default or tie sentence names, e.g. escalate on a
    no-tie short card, section 1 outcome roles / 6.2). Read X off the question frame around 'final outcome'."""
    q = q.strip()
    for ref in sorted(refs, key=len, reverse=True):
        i = q.find(ref)
        if i < 0:
            continue
        after = q[i + len(ref):].strip()
        after = re.sub(r'\?\s*$', '', after).strip()
        if after:
            after = re.sub(r'^(?:is\s+)?(?:not\s+)*', '', after).strip()
            return after or None
        m = re.search(r'\b[Ii]s\s+(?:it\s+(?:not\s+)?true\s+that\s+)?(?:not\s+)*(.+?)\s+(?:not\s+)*the final outcome\b', q)
        if m:
            return m.group(1).strip()
    return None


def question_sentence(instr, must='final outcome'):
    qs = []
    for line in instr.split('\n'):
        for s in split_sentences(clean_line(line)):
            if '?' in s and must in s:
                qs.append(s)
    if not qs:
        raise ParseError('no question sentence')
    return qs[-1]


def answer(row):
    """returns dict(ans=<value comparable with row['gold']>, depth=int, note=str)."""
    if is_flow(row):
        return answer_flow(row)
    P = build(row)
    names = outcome_names(P, row)
    if row['qtype'] == 'noul':
        if len(P.cases) != 1:
            raise ParseError('Q3 with %d cases' % len(P.cases))
        q = question_sentence(row['instructions'])
        X = find_x(q, names, [c.ref for c in P.cases])
        nnot = len(re.findall(r"\bnot\b|n't\b", q))
        neg = nnot % 2 == 1
        res, unk = solve_case(P, P.cases[0])
        truth = {(d['outcome'] == X) != neg for d, _ in res}
        depth = max(dep for _, dep in res)
        if truth == {True}:
            return {'ans': 1, 'depth': depth, 'q': 'Q3', 'X': X, 'neg': neg}
        if truth == {False}:
            return {'ans': 0, 'depth': depth, 'q': 'Q3', 'X': X, 'neg': neg}
        return {'ans': 'UNDETERMINED_YESNO', 'depth': depth, 'q': 'Q3', 'X': X, 'neg': neg}
    opts = row['options']
    refs = {c.ref for c in P.cases}
    if refs & set(opts):
        return answer_q4(P, row, names, opts)
    res, unk = solve_case(P, P.cases[0]) if len(P.cases) == 1 else (None, None)
    if res is None:
        raise ParseError('choice row with %d cases' % len(P.cases))
    depth = max(dep for _, dep in res)
    outs = {d['outcome'] for d, _ in res}
    cbd = P.pol['cbd']
    if P.pol['codes'] or any(' basis ' in o for o in opts):
        src, win = source_of(res)
        if src == 'CBD':
            return {'ans': cbd, 'depth': depth, 'q': 'Q2'}
        o = next(iter(outs))
        if src in ('ONE',):
            want = (o, win)
        elif src in ('D', 'T', 'F', 'M'):
            want = (o, src)
        else:
            return {'ans': 'NO_Q2_ROW(%s)' % src, 'depth': depth, 'q': 'Q2'}
        for op in opts:
            if parse_q2_option(op, names, P.pol['codes'], cbd) == want:
                return {'ans': op, 'depth': depth, 'q': 'Q2'}
        return {'ans': 'Q2_PAIR_NOT_IN_OPTIONS%r' % (want,), 'depth': depth, 'q': 'Q2'}
    if len(outs) > 1:
        return {'ans': cbd if cbd in opts else 'CBD_NOT_OFFERED', 'depth': depth, 'q': 'Q1'}
    o = next(iter(outs))
    return {'ans': o if o in opts else 'OUTCOME_NOT_IN_OPTIONS(%s)' % o, 'depth': depth, 'q': 'Q1'}


def parse_q2_option(op, names, codes, cbd):
    if op == cbd:
        return 'CBD'
    pref = [n for n in names if op.startswith(n)]
    if not pref:
        return None
    o = max(pref, key=len)
    rest = op[len(o):].strip()
    for k, c in codes.items():
        if rest.endswith(c) or rest.endswith(re.sub(r'^code ', '', c)):
            return (o, k)
    m = re.search(r'(\d+)$', rest)
    if m:
        return (o, int(m.group(1)))
    return None


def answer_q4(P, row, names, opts):
    try:
        q = question_sentence(row['instructions'])
    except ParseError:
        q = question_sentence(row['instructions'], must='')
    X = find_x(q, names)
    none = P.pol['none']
    qual, depth = [], 0
    for c in P.cases:
        res, unk = solve_case(P, c)
        if unk:
            raise ParseError('Q4 case with unknown fields')
        d, dep = res[0]
        depth = max(depth, dep)
        if d['outcome'] == X:
            qual.append(c.ref)
    if len(qual) == 1:
        ans = qual[0]
    elif not qual:
        ans = none if none in opts else 'NONE_NOT_OFFERED'
    else:
        ans = 'MULTIPLE_QUALIFY(%d)' % len(qual)
    return {'ans': ans, 'depth': depth, 'q': 'Q4', 'X': X}


def gold_of(row):
    return row['gold']


# ----------------------------------------------------------------------------------------------------------------
# 11. S5 flowchart text (spec 3 S5, 11.6): solver B on the PARSED DAG.  Table-driven: the numbered steps become a
#     transition table {step: ('test', items, yes, no) | ('out', outcome)}; revision notes become a start-step table
#     keyed by effective date.  The DAG is checked (targets exist, acyclic from every start, every reachable step
#     defined), then walked for the closed case or every open-world completion (critical points of the step tests).
#     Depth is a property of the hidden section 2 structure (X, P, O are compiled away in the DAG), so it is not
#     re-derived for S5 rows (depth_b = None).
# ----------------------------------------------------------------------------------------------------------------
FLOW_Q = re.compile(r'^Step (\d+): Does it hold that (.+?)\?(?:\s*If yes, go to step (\d+); if no, go to step (\d+)\.?)?$')
FLOW_GOTO = re.compile(r'^If yes, go to step (\d+); if no, go to step (\d+)\.?$')
FLOW_OUT = re.compile(r'^Step (\d+): The outcome is (.+?)\.?$')
FLOW_START = re.compile(r'^The flowchart starts at step (\d+)\.?$')
FLOW_NOTE = re.compile(r'^(?:Revision note|Revised step note|Revision) (\d+)(?: from (.+?))? \((.*?)\): from its effective '
                       r'date the flowchart starts at step (\d+)\.?$')


def is_flow(row):
    return bool(re.search(r'(?m)Step \d+: (?:Does it hold that|The outcome is)', row.get('state') or ''))


class Flow:
    pass


def parse_flow(row):
    units, mode = normalize(row['state'])
    its = unit_texts(units)
    F = Flow()
    F.steps, F.start, F.notes = {}, None, []
    rest, pend = [], None
    for kind, p, sec in its:
        t = p if kind == 's' else (kv_as_sentence(*p) if kind == 'kv' else None)
        if t is None:
            rest.append((kind, p, sec))
            continue
        t = clean_line(t)
        if pend is not None:
            m = FLOW_GOTO.match(t)
            if not m:
                raise ParseError('flow step without go-to')
            F.steps[pend[0]] = ('test', pend[1], int(m.group(1)), int(m.group(2)))
            pend = None
            continue
        m = FLOW_Q.match(t)
        if m:
            sid = int(m.group(1))
            if sid in F.steps or (pend and pend[0] == sid):
                raise ParseError('duplicate step')
            if m.group(3):
                F.steps[sid] = ('test', m.group(2), int(m.group(3)), int(m.group(4)))
            else:
                pend = (sid, m.group(2))
            continue
        m = FLOW_OUT.match(t)
        if m:
            sid = int(m.group(1))
            if sid in F.steps:
                raise ParseError('duplicate step')
            F.steps[sid] = ('out', m.group(2).strip())
            continue
        m = FLOW_START.match(t)
        if m:
            if F.start is not None:
                raise ParseError('two start sentences')
            F.start = int(m.group(1))
            continue
        m = FLOW_NOTE.match(t)
        if m:
            iss, eff = parse_notice_dates(m.group(3))
            F.notes.append({'num': int(m.group(1)), 'body': m.group(2), 'eff': eff, 'iss': iss, 'start': int(m.group(4))})
            continue
        rest.append((kind, p, sec))
    if pend is not None:
        raise ParseError('flow step without go-to (end)')
    if F.start is None or not F.steps:
        raise ParseError('flowchart incomplete')
    P = parse_its(rest, mode, row['meta'].get('domain_pack'))
    P.pol = parse_policy(policy_sentences([row.get('card') or '', row.get('instructions') or ''] + P.other))
    return F, P


def flow_compile(F, P):
    ents = [e for e in [P.entity] if e]
    F.items = {}
    for sid, st in F.steps.items():
        if st[0] == 'test':
            F.items[sid] = parse_condition(st[1], P.ctx, ents)
    # inert notes (another body) never move the start step (row 42 meaning)
    F.live = [n for n in F.notes if n['body'] is None or n['body'] == P.body]
    starts = {F.start} | {n['start'] for n in F.live}
    for s0 in starts:                       # static DAG check from every possible start
        stack, onpath, done = [(s0, 0)], set(), set()
        while stack:
            s, state = stack.pop()
            if state == 1:
                onpath.discard(s); done.add(s)
                continue
            if s in done:
                continue
            if s in onpath:
                raise ParseError('flowchart cycle')
            st = F.steps.get(s)
            if st is None:
                raise ParseError('go-to names an undefined step')
            onpath.add(s)
            stack.append((s, 1))
            if st[0] == 'test':
                for nx in (st[2], st[3]):
                    if nx in onpath:
                        raise ParseError('flowchart cycle')
                    stack.append((nx, 0))
    # fake rules so the shared critical-point code sees every literal tested by a step
    P.rules = {sid: Rule(sid, 'gen', its) for sid, its in F.items.items()}
    P.notices = []
    return F


def flow_start(F, g):
    """start step on governing date g: the note group with the latest effective date <= g; notes with the same
    effective date take effect together (they must agree)."""
    eff = [n for n in F.live if n['eff'] <= g]
    if not eff:
        return F.start
    last = max(n['eff'] for n in eff)
    grp = {n['start'] for n in eff if n['eff'] == last}
    if len(grp) != 1:
        raise ParseError('same-date revision notes name different start steps')
    return grp.pop()


def flow_walk(F, s, env):
    seen = []
    while True:
        if s in seen:
            raise ParseError('cycle on walk')
        seen.append(s)
        st = F.steps[s]
        if st[0] == 'out':
            return st[1], seen
        s = st[2] if all(item_true(it, env) for it in F.items[s]) else st[3]


def flow_case(F, P, case):
    envs, unknown, notrec = case_env(P, case)
    outs = []
    for e in envs:
        g = e.get(P.gov)
        if g is None:
            raise ParseError('governing date unknown')
        o, path = flow_walk(F, flow_start(F, g), e)
        outs.append(o)
    return outs, unknown


def card_outcome_lines(row):
    names = []
    for t in (row.get('card') or '', row.get('instructions') or ''):
        for line in t.split('\n'):
            m = re.match(r'^\s*(?:[-*•+·>]\s*)?([^:?]{1,60}): (.+)$', line)
            if '?' in line:
                continue
            if m and len(m.group(1).split()) <= 8 and not re.search(r'[.?!]', m.group(1)):
                names.append(m.group(1).strip())
    return names


def answer_flow(row):
    F, P = parse_flow(row)
    flow_compile(F, P)
    if not P.cases:
        raise ParseError('no case')
    step_outs = {st[1] for st in F.steps.values() if st[0] == 'out'}
    names = set(step_outs) | set(card_outcome_lines(row))
    refs = [c.ref for c in P.cases]
    if row['qtype'] == 'noul':
        if len(P.cases) != 1:
            raise ParseError('Q3 with %d cases' % len(P.cases))
        q = question_sentence(row['instructions'])
        X = find_x(q, names, refs)
        neg = len(re.findall(r"\bnot\b|n't\b", q)) % 2 == 1
        outs, unk = flow_case(F, P, P.cases[0])
        truth = {(o == X) != neg for o in outs}
        ans = 1 if truth == {True} else (0 if truth == {False} else 'UNDETERMINED_YESNO')
        return {'ans': ans, 'depth': None, 'q': 'S5-Q3', 'X': X, 'neg': neg}
    opts = row['options']
    if set(refs) & set(opts):
        q = question_sentence(row['instructions'])
        X = find_x(q, names, refs)
        qual = []
        for c in P.cases:
            outs, unk = flow_case(F, P, c)
            if unk:
                raise ParseError('S5 Q4 case with unknown fields')
            if outs[0] == X:
                qual.append(c.ref)
        none = P.pol['none']
        ans = qual[0] if len(qual) == 1 else ('MULTIPLE_QUALIFY(%d)' % len(qual) if qual else (none if none in opts else 'NONE_NOT_OFFERED'))
        return {'ans': ans, 'depth': None, 'q': 'S5-Q4', 'X': X}
    if len(P.cases) != 1:
        raise ParseError('choice row with %d cases' % len(P.cases))
    outs, unk = flow_case(F, P, P.cases[0])
    if len(set(outs)) == 1:
        o = outs[0]
        return {'ans': o if o in opts else 'OUTCOME_NOT_IN_OPTIONS(%s)' % o, 'depth': None, 'q': 'S5-Q1'}
    cbd = P.pol['cbd']
    if cbd is None and P.pol['world'] == 'open':
        left = [o for o in opts if o not in names]
        cbd = left[0] if len(left) == 1 else None
    return {'ans': cbd if cbd in opts else 'CBD_NOT_OFFERED', 'depth': None, 'q': 'S5-Q1'}
