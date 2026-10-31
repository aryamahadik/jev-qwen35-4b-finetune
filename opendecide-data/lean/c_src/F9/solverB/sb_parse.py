# F9 solver B, part 1: card-clause parser, container parsers, value parsers.
# Written from c_src/F9/G0_SPEC.md (v7, frozen sha 70e75711...) sections 1.1, 1.6, 1.10 and 2 and the row format only.
# It never imports or reads c_src/F9/gen/ (solver A). Paradigm: text -> typed cells -> sqlite (sb_eval.py).
import re, csv, io, json, datetime
from fractions import Fraction
from html.parser import HTMLParser
import yaml

MONTHS = {m.lower(): i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
     'November', 'December'])}
MON3 = {k[:3]: v for k, v in MONTHS.items()}
ALLMON = dict(MONTHS); ALLMON.update(MON3); ALLMON['sept'] = 9


class ParseError(Exception):
    pass


# ---------------------------------------------------------------- card clauses (T1-T41) -------------------------
class Card:
    def __init__(self):
        self.world = None            # 'T1' | 'T2'
        self.no_record = None        # T1 / T23 no-record option text
        self.unk_tokens = set()      # T3
        self.unk_mode = None         # 'T4' | 'T5'
        self.domains = {}            # T5: col -> ('set', [..]) | ('int', lo, hi, step) | ('date', d1, d2) | ('bool',)
        self.thou = ''               # T21
        self.dec = '.'
        self.date_fmt = 'YYYY-MM-DD'
        self.time_fmt = None
        self.csv_delim = ','
        self.units = {}              # T28 col -> unit
        self.bools = {}              # T34 col -> (true_tok, false_tok)
        self.tie_chain = None        # T24 key variant: [(col, 'min'|'max')]
        self.tie_option = None       # T24 option variant text
        self.dup_mode = None         # T25 'default' | 'dedup'
        self.terms = {}              # T7-T9: name -> dict(kind, parts...) (raw text conditions)
        self.overrides = {}          # T30: name -> [(key_value_text, cond_text)]
        self.legend = {}             # masked codes: col -> {code: meaning}
        self.levels = None           # T33 order list
        self.round_n = None          # T22 decimals
        self.footmark = None         # S5 footnote mark
        self.log_merged = False      # T32
        self.cbd = "cannot be determined"
        self.none_of = "none of these"
        self.flags = set()
        self.raw = ''


def parse_card(text, short=False):
    c = Card()
    c.raw = text or ''
    t = c.raw
    flat = re.sub(r'[ \t]+', ' ', t)
    if re.search(r'lists every', t):
        c.world = 'T1'; c.flags.add('T1')
    if re.search(r'may not list every', t):
        c.world = 'T2'; c.flags.add('T2')
    c.no_records = [x for x in re.findall(r"(?:has the answer|so the answer is) '([^']+)'", t)]
    c.no_record = c.no_records[0] if c.no_records else None
    for m in re.finditer(r"'([^']+)' means the value is not known", t):
        c.unk_tokens.add(m.group(1))
    if re.search(r'is left out of that question', t):
        c.unk_mode = 'T4'; c.flags.add('T4')
    if re.search(r'could be any allowed value', t):
        c.unk_mode = 'T5'; c.flags.add('T5')
    m = re.search(r'Allowed values: (.*?)Known values follow the same limits', flat, re.S)
    if m:
        c.domains_text = m.group(1)
    else:
        c.domains_text = None
    # T21
    m = re.search(r"'(.)' splits thousands, and '(.)' marks decimals", t)
    if m:
        c.thou, c.dec = m.group(1), m.group(2)
    m = re.search(r"No mark splits thousands, and '(.)' marks decimals", t)
    if m:
        c.thou, c.dec = '', m.group(1)
    m = re.search(r"A space splits thousands, and '(.)' marks decimals", t)
    if m:
        c.thou, c.dec = ' ', m.group(1)
    m = re.search(r'Dates are written ([DMY][DMY./ -]*[DMY])\.', t)
    if m:
        c.date_fmt = m.group(1)
    m = re.search(r'Times are written (HH:MM(?::SS)?)', t)
    if m:
        c.time_fmt = m.group(1)
    m = re.search(r'fields are separated by (commas|semicolons|tabs)', t)
    if m:
        c.csv_delim = {'commas': ',', 'semicolons': ';', 'tabs': '\t'}[m.group(1)]
    for m in re.finditer(r'\b([a-z][a-z0-9_.]*) is in ([^.\n]+?)\.(?=\s|$)', t):
        c.units[m.group(1)] = m.group(2).strip()
    for m in re.finditer(r'In ([a-z][a-z0-9_.]*), (\S+) means yes and (\S+) means no', t):
        c.bools[m.group(1)] = (m.group(2), m.group(3))
    # T24
    m = re.search(r"tie for the answer to a question that asks which [^,]+, answer '([^']+)'", t)
    if m:
        c.tie_option = m.group(1)
    m = re.search(r'tie, choose the one with the ([^.\n]+?)(?:\.|\n|$)', t)
    if m:
        chain = []
        for part in re.split(r'; if they still tie, the one with the ', m.group(1)):
            mm = re.match(r'(earliest|latest|lowest|highest) (\S+)', part.strip())
            if not mm:
                raise ParseError('tie chain: ' + part)
            chain.append((mm.group(2), 'min' if mm.group(1) in ('earliest', 'lowest') else 'max'))
        c.tie_chain = chain
    # T25
    if re.search(r'Each row is one [^,]+, even when two rows share', t):
        c.dup_mode = 'default'
    if re.search(r'Rows with the same \S+ are one', t):
        c.dup_mode = 'dedup'
        m = re.search(r'the row with the latest (\S+) is the current one', t)
        c.dedup_col = m.group(1) if m else None
    # T7-T9 terms (one sentence per term, condition text kept raw; compiled against the schema later)
    for m in re.finditer(r'A [a-z][a-z \-]*? counts as ([a-z][a-z \-]*?) exactly when all of the following hold: '
                         r'(.+?)\.(?= |\s*\||\s*$|\n|\))', t, re.M):
        c.terms[m.group(1)] = ('T9', [x.strip() for x in m.group(2).split(';')])
    for m in re.finditer(r'A [a-z][a-z \-]*? counts as ([a-z][a-z \-]*?) if (.+?), unless (.+?)\. No other', t):
        c.terms[m.group(1)] = ('T7', m.group(2).strip(), m.group(3).strip())
    for m in re.finditer(r'A [a-z][a-z \-]*? counts as ([a-z][a-z \-]*?) only if (.+?)\. Every [a-z][a-z \-]*? whose '
                         r'(.+?) counts as \1\. No other', t):
        c.terms[m.group(1)] = ('T8', m.group(2).strip(), m.group(3).strip())
    for m in re.finditer(r'For ([^,\n]+?), ([a-z][a-z \-]*?) means (.+?) instead\.', t):
        c.overrides.setdefault(m.group(2), []).append((m.group(1), m.group(3)))
    # masked-code legends
    for m in re.finditer(r'(?i)codes[ _]for[ _]([a-z][a-z0-9_.]*[a-z0-9])\W*\n(.*?)(?:\n[>\s]*\n|\Z)', t, re.S):
        col = m.group(1).lower()
        body = m.group(2)
        mp = {}
        for line in body.split('\n'):
            s = line.strip().strip('>').strip()
            s = s.strip('|').strip()
            if not s or set(s) <= set('=-| +') or re.match(r'(?i)code\b', s):
                continue
            mm = re.match(r'^([A-Z][A-Z0-9]*\d)\s*(?:\||\s{2,}|:|=|-)\s*(.+?)\s*\|?$', s)
            if mm:
                mp[mm.group(1)] = mm.group(2).strip()
        if mp:
            c.legend[col] = mp
    m = re.search(r'Levels from lowest to highest: ([A-Z]+(?: < [A-Z]+)+)', t)
    if m:
        c.levels = [x.strip() for x in m.group(1).split('<')]
    m = re.search(r'rounded to (\d+) decimal place', t)
    if m:
        c.round_n = int(m.group(1))
    m = re.search(r'Values marked (\S+) are left out', t)
    if m:
        c.footmark = m.group(1)
    if re.search(r'are merged and may be out of order', t):
        c.log_merged = True
    if short or not c.unk_tokens:
        pass
    return c


# ---------------------------------------------------------------- value parsers ---------------------------------
def parse_number(s, card):
    """Exact Fraction from a number written in the card's T21 format (JSON/YAML natives handled by caller)."""
    s = s.strip()
    neg = s.startswith('-')
    if neg:
        s = s[1:]
    if card.thou:
        th = re.escape(card.thou)
        dc = re.escape(card.dec)
        if not re.fullmatch(r'\d{1,3}(?:' + th + r'\d{3})*(?:' + dc + r'\d+)?|\d+(?:' + dc + r'\d+)?', s):
            raise ParseError('number ' + s)
        s = s.replace(card.thou, '')
    else:
        if not re.fullmatch(r'\d+(?:' + re.escape(card.dec) + r'\d+)?', s):
            raise ParseError('number ' + s)
    if card.dec != '.':
        s = s.replace(card.dec, '.')
    v = Fraction(s)
    return -v if neg else v


def num_decimals(s, card):
    s = s.strip()
    if card.dec in s:
        return len(s.split(card.dec)[-1])
    return 0


DATE_RX = {
    'YYYY-MM-DD': r'(?P<y>\d{4})-(?P<m>\d\d)-(?P<d>\d\d)',
    'YYYY/MM/DD': r'(?P<y>\d{4})/(?P<m>\d\d)/(?P<d>\d\d)',
    'DD.MM.YYYY': r'(?P<d>\d\d)\.(?P<m>\d\d)\.(?P<y>\d{4})',
    'D MMMM YYYY': r'(?P<d>\d{1,2}) (?P<mn>[A-Z][a-z]+) (?P<y>\d{4})',
    'D MMM YYYY': r'(?P<d>\d{1,2}) (?P<mn>[A-Z][a-z]{2}) (?P<y>\d{4})',
    'MM/DD/YYYY': r'(?P<m>\d\d)/(?P<d>\d\d)/(?P<y>\d{4})',
    'DD/MM/YYYY': r'(?P<d>\d\d)/(?P<m>\d\d)/(?P<y>\d{4})',
}


def date_rx(card):
    if card.date_fmt not in DATE_RX:
        raise ParseError('date format ' + card.date_fmt)
    return DATE_RX[card.date_fmt]


def _ymd(m):
    y = int(m.group('y')); d = int(m.group('d'))
    if 'mn' in m.groupdict() and m.group('mn') is not None:
        mn = m.group('mn').lower()
        if mn not in ALLMON:
            raise ParseError('month ' + mn)
        mo = ALLMON[mn]
    else:
        mo = int(m.group('m'))
    return datetime.date(y, mo, d).toordinal()


def parse_date(s, card):
    m = re.fullmatch(date_rx(card), s.strip())
    if not m:
        raise ParseError('date ' + s)
    return _ymd(m)


def dt_rx(card):
    return date_rx(card) + r' (?P<H>\d\d):(?P<M>\d\d)(?::(?P<S>\d\d))?'


def parse_datetime(s, card):
    m = re.fullmatch(dt_rx(card), s.strip())
    if not m:
        raise ParseError('datetime ' + s)
    return _ymd(m) * 86400 + int(m.group('H')) * 3600 + int(m.group('M')) * 60 + int(m.group('S') or 0)


def fmt_date(o, card):
    d = datetime.date.fromordinal(o)
    f = card.date_fmt
    if f == 'YYYY-MM-DD':
        return '%04d-%02d-%02d' % (d.year, d.month, d.day)
    if f == 'YYYY/MM/DD':
        return '%04d/%02d/%02d' % (d.year, d.month, d.day)
    if f == 'DD.MM.YYYY':
        return '%02d.%02d.%04d' % (d.day, d.month, d.year)
    if f == 'D MMMM YYYY':
        return '%d %s %04d' % (d.day, d.strftime('%B'), d.year)
    if f == 'D MMM YYYY':
        return '%d %s %04d' % (d.day, d.strftime('%b'), d.year)
    raise ParseError('fmt ' + f)


# ---------------------------------------------------------------- containers ------------------------------------
class Table:
    def __init__(self, title, cols, rows, kind):
        self.title = title          # e.g. 'Clients' (S3) or None
        self.cols = cols            # header names (raw, may carry a unit suffix)
        self.rows = rows            # list of dict col -> raw cell (str) or native (json/yaml)
        self.kind = kind            # md|csv|html|fw|kv|json|jsonl|yaml|log|pivot
        self.native = kind in ('json', 'jsonl', 'yaml')


class _HT(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows = []; self.cur = None; self.cell = None

    def handle_starttag(self, tag, a):
        if tag == 'tr':
            self.cur = []
        elif tag in ('td', 'th'):
            self.cell = ''

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cur is not None:
            self.cur.append(self.cell.strip()); self.cell = None
        elif tag == 'tr' and self.cur is not None:
            self.rows.append(self.cur); self.cur = None

    def handle_data(self, d):
        if self.cell is not None:
            self.cell += d


def _md(lines):
    def split(l):
        l = l.strip()
        assert l.startswith('|') and l.endswith('|'), l
        parts = re.split(r'(?<!\\)\|', l[1:-1])
        return [p.strip().replace('\\|', '|') for p in parts]
    hdr = split(lines[0])
    if not re.fullmatch(r'\|(\s*:?-{3,}:?\s*\|)+', lines[1].strip().replace(' ', '')) and \
            not set(lines[1].strip()) <= set('|-: '):
        raise ParseError('md sep')
    rows = [split(l) for l in lines[2:]]
    for r in rows:
        if len(r) != len(hdr):
            raise ParseError('md width')
    return hdr, rows


def _fw(lines):
    hdr_line = lines[0]
    starts = [m.start() for m in re.finditer(r'(?:(?<=^)|(?<=\s\s))\S', hdr_line)]
    names = hdr_line.split()
    if len(starts) != len(names):
        raise ParseError('fw header')
    rows = []
    for l in lines[1:]:
        if not l.strip():
            continue
        cells = []
        for i, s in enumerate(starts):
            e = starts[i + 1] if i + 1 < len(starts) else None
            seg = l[s:e] if e is not None else l[s:]
            if s > 0 and l[s - 1:s].strip():
                raise ParseError('fw align')
            cells.append(seg.strip())
        rows.append(cells)
    return names, rows


def _kv(lines):
    recs, cur, order = [], {}, []
    for l in lines + ['']:
        if not l.strip():
            if cur:
                recs.append(cur); cur = {}
            continue
        if ': ' not in l:
            raise ParseError('kv line')
        k, v = l.split(': ', 1)
        k = k.strip()
        if k not in order:
            order.append(k)
        cur[k] = v.strip()
    return order, [[r.get(k) for k in order] for r in recs]


def find_containers(state, card):
    """Return list of Table. S3 tables carry their 'Title:' line; S5 pivots carry their caption."""
    out = []
    lines = state.split('\n')
    i, title = 0, None
    n = len(lines)
    while i < n:
        l = lines[i]
        s = l.strip()
        if not s:
            i += 1; continue
        if re.fullmatch(r'[A-Z][A-Za-z ]+:', s):
            title = s[:-1]; i += 1; continue
        m = re.fullmatch(r'(\S+) by (.+) and week, in (.+):', s)
        if m:
            title = ('pivot', m.group(1), m.group(2), m.group(3)); i += 1; continue
        if s.startswith('```'):
            lang = s[3:].strip()
            j = i + 1
            while j < n and lines[j].strip() != '```':
                j += 1
            body = lines[i + 1:j]
            out.append(_fenced(lang, body, card, title))
            title = None; i = j + 1; continue
        if s.startswith('<table'):
            j = i
            while j < n and '</table>' not in lines[j]:
                j += 1
            p = _HT(); p.feed('\n'.join(lines[i:j + 1]))
            hdr, rows = p.rows[0], p.rows[1:]
            out.append(Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'html'))
            title = None; i = j + 1; continue
        if s.startswith('|'):
            j = i
            while j < n and lines[j].strip().startswith('|'):
                j += 1
            hdr, rows = _md([x for x in lines[i:j]])
            if isinstance(title, tuple):
                out.append(Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'pivot'))
            else:
                out.append(Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'md'))
            title = None; i = j; continue
        if l.startswith('    '):
            j = i
            while j < n and (lines[j].startswith('    ') or not lines[j].strip()):
                j += 1
            body = [x[4:] for x in lines[i:j]]
            while body and not body[-1].strip():
                body.pop()
            out.append(_block(body, card, title))
            title = None; i = j; continue
        raise ParseError('unrecognised state line: ' + s[:40])
    return out


LOG_HINT = re.compile(r'^\s*(?:\[|time=")')


def _block(body, card, title, lang=None):
    """An unfenced indented block or a fenced block without a decisive language: log lines or fixed width."""
    if is_log(body, card):
        return Table(title, None, body, 'log')
    hdr, rows = _fw(body)
    return Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'fw')


def is_log(body, card):
    ls = [x for x in body if x.strip()]
    if not ls:
        return False
    return all(log_line(x, card) is not None for x in ls[:3])


def _fenced(lang, body, card, title):
    if lang == 'log':
        return Table(title, None, [x for x in body if x.strip()], 'log')
    if lang == 'csv':
        rd = list(csv.reader(io.StringIO('\n'.join(body)), delimiter=card.csv_delim))
        hdr = [h.strip() for h in rd[0]]
        rows = [r for r in rd[1:] if r]
        for r in rows:
            if len(r) != len(hdr):
                raise ParseError('csv width (delimiter %r)' % card.csv_delim)
        return Table(title, hdr, [dict(zip(hdr, [c.strip() for c in r])) for r in rows], 'csv')
    if lang == 'records':
        hdr, rows = _kv(body)
        return Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'kv')
    if lang == 'json':
        data = json.loads('\n'.join(body), parse_float=Fraction)
        return Table(title, None, data, 'json')
    if lang == 'jsonl':
        return Table(title, None, [json.loads(x, parse_float=Fraction) for x in body if x.strip()], 'jsonl')
    if lang == 'yaml':
        return Table(title, None, yaml.safe_load('\n'.join(body)), 'yaml')
    if lang in ('table', 'text', ''):
        if body and body[0].strip().startswith('|'):
            hdr, rows = _md(body)
            return Table(title, hdr, [dict(zip(hdr, r)) for r in rows], 'md')
        return _block(body, card, title)
    raise ParseError('fence ' + lang)


# ---------------------------------------------------------------- log lines (S6; four syntaxes, 3.5) ------------
def _dtpart(card):
    d = date_rx(card).replace('?P<', '?P<_')   # unnamed copy for embedding
    d = re.sub(r'\(\?P<_[a-zA-Z]+>', '(?:', d)
    return d + r' \d\d:\d\d(?::\d\d)?'


def log_syntaxes(card):
    dt = _dtpart(card)
    tail = r'(?P<rest>.*)'
    return [
        ('bracket_level', re.compile(r'^(?P<t>' + dt + r') (?P<c>[A-Z][A-Z0-9]*-\d+)\[(?P<l>[A-Z]+)\]: ' + tail + '$')),
        ('iso_comp', re.compile(r'^(?P<t>' + dt + r') (?P<c>[A-Z][A-Z0-9]*-\d+) (?P<l>[A-Z]+) ' + tail + '$')),
        ('syslog', re.compile(r'^\[(?P<t>' + dt + r')\] \[(?P<l>[A-Z]+)\] (?P<c>[A-Z][A-Z0-9]*-\d+): ' + tail + '$')),
        ('keyvalue', re.compile(r'^time="(?P<t>' + dt + r')" level=(?P<l>[A-Z]+) component=(?P<c>[A-Z][A-Z0-9]*-\d+) '
                                r'msg="(?P<msg>[^"]*)"(?P<rest>.*)$')),
    ]


def log_line(line, card):
    hits = []
    for name, rx in log_syntaxes(card):
        m = rx.match(line.strip())
        if m:
            hits.append((name, m))
    if len(hits) != 1:
        return None
    name, m = hits[0]
    rest = m.group('rest')
    if name == 'keyvalue':
        msg = m.group('msg'); kvtxt = rest
    else:
        mm = re.match(r'^(.*?)((?: [a-z_]+=\S+)*)$', ' ' + rest)
        msg = mm.group(1).strip(); kvtxt = mm.group(2)
    kv = dict(re.findall(r'([a-z_]+)=(\S+)', kvtxt))
    return dict(syntax=name, t=m.group('t'), level=m.group('l'), comp=m.group('c'), msg=msg, kv=kv)
