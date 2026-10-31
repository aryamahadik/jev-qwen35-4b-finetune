#!/usr/bin/env python3
"""F10 solver B (G2): independent re-derivation of gold from the row text.

Written from the frozen G0 spec (F10-G0-v7, sections 2, 4, 5, 9) and the row format only; it never imports or reads
the generator (c_src/F10/gen/) or solver A. Paradigm: REGION ALGEBRA on a card parsed from the row text.
  - every legend attribute is an axis in integer grid units (counts, cents, 10^-d, day ordinals, one axis d per
    relative-date pair) or a finite value set (category values, flag values, tag subsets);
  - every parsed definition compiles bottom-up (references -> the referenced raw region) to a union of boxes;
  - the case is a point (closed world) or a box (open world: omitted attributes span the full legend domain);
  - meets = box inside / outside the region; assigned = region minus the union of earlier regions; P = set of
    possible assigned answers; S6 = empty symmetric difference; S7 = codebook text parsed through the
    formats-2 field-value lexicon, evaluated on the released annotation vector (looked up by the coded text).
Inputs read: the rows (state, instructions, card, options, qtype, meta.sampler/domain_pack), the domain packs
(attribute lexicon for templated-prose records), formats-2 records + lexicon (S7), common/markers.json.
Usage: python solver_b.py [out_dir] [--only FILE] [--limit N] [--debug ID]
"""
import json, re, sys, os, itertools, datetime, collections
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
CSRC = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(CSRC, 'F10', 'out')
INF = 10 ** 15


class ParseError(Exception):
    pass


# ----------------------------------------------------------------------------------------------- text helpers
MONTHS = {m.lower(): i + 1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                  'August', 'September', 'October', 'November', 'December'])}
for _m, _i in list(MONTHS.items()):
    MONTHS[_m[:3]] = _i
MONTHS['sept'] = 9
MON_RE = r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?'
DATE_RES = [
    (re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})'), 'ymd'),
    (re.compile(r'(\d{4})/(\d{1,2})/(\d{1,2})'), 'ymd'),
    (re.compile(r'(\d{4})\.(\d{1,2})\.(\d{1,2})'), 'ymd'),
    (re.compile(r'(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day,?\s+)?(' + MON_RE + r')\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})', re.I), 'mdy'),
    (re.compile(r'(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day,?\s+)?(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(' + MON_RE + r'),?\s+(\d{4})', re.I), 'dmy'),
]


def parse_date(s):
    s = s.strip().strip('"\'`*_').strip()
    for rx, kind in DATE_RES:
        m = rx.fullmatch(s)
        if m:
            g = m.groups()
            if kind == 'ymd':
                y, mo, d = int(g[0]), int(g[1]), int(g[2])
            elif kind == 'mdy':
                mo, d, y = MONTHS[g[0].lower().rstrip('.')], int(g[1]), int(g[2])
            else:
                d, mo, y = int(g[0]), MONTHS[g[1].lower().rstrip('.')], int(g[2])
            return datetime.date(y, mo, d).toordinal()
    return None


def find_dates(s):
    """all date substrings (start, end, ordinal)."""
    out = []
    for rx, kind in DATE_RES:
        for m in rx.finditer(s):
            v = parse_date(m.group(0))
            if v is not None:
                out.append((m.start(), m.end(), v))
    out.sort(key=lambda t: (t[0], -(t[1] - t[0])))
    res, last = [], -1
    for a, b, v in out:
        if a >= last:
            res.append((a, b, v)); last = b
    return res


TAG_RE = re.compile(r'<[^<>]{1,200}>')


def strip_chrome(line):
    """remove quote markers, bullets, numbering, markdown emphasis, xml/html tags from a card or record line."""
    s = line
    s = TAG_RE.sub(' ', s)
    s = s.replace('**', '').replace('__', '').replace('`', '')
    s = s.strip()
    for _ in range(4):
        s0 = s
        s = re.sub(r'^>\s?', '', s).strip()
        s = re.sub(r'^#{1,6}\s+', '', s)
        s = re.sub(r'^(?:[-+*•·–—▪►▸◦○●■□✓✔☐☑]|\[[ xX]\])\s+', '', s)
        s = re.sub(r'^(?:\(?\d{1,3}[.):]|\(?[a-zA-Z][.)]|\(\d{1,3}\)|\(?[ivxIVX]{1,4}[.)])\s+', '', s)
        s = re.sub(r'^(?:Step|Item|Rule|No\.)\s*\d+[.:)]\s+', '', s)
        if s == s0:
            break
    return s.strip()


def norm_key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def wnorm(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


# ----------------------------------------------------------------------------------------------- packs
_PACKS = None


def packs():
    global _PACKS
    if _PACKS is None:
        _PACKS = {}
        for sub in ('packs-1/packs.jsonl', 'packs-2/packs.jsonl', 'packs-3/packs-3.jsonl', 'packs-4/packs.jsonl'):
            fn = os.path.join(CSRC, 'packs', sub)
            if not os.path.exists(fn):
                continue
            for l in open(fn):
                try:
                    p = json.loads(l)
                except Exception:
                    continue
                pid = p.get('id') or p.get('pack_id')
                if pid and pid not in _PACKS:
                    _PACKS[pid] = p
    return _PACKS


class AttrInfo:
    """pack-side information about one attribute (used for name anchoring, units and prose statements)."""

    def __init__(self, label):
        self.label = label
        self.aliases = set()
        self.ptype = None          # int/dec/money/cat/boolean/date/tag
        self.values = []
        self.unit = None
        self.unit_syn = set()
        self.places = None
        self.statements = {}       # value/pos/neg/none -> list of templates
        self.entity_words = set()


def pack_attrs(pid):
    """label(lower) -> list[AttrInfo]; plus entity phrases."""
    p = packs().get(pid)
    res = collections.defaultdict(list)
    ents = set()
    if p is None:
        return res, ents
    for e in p.get('entity_types', []) or []:
        for k in ('singular', 'noun', 'plural', 'key'):
            if isinstance(e.get(k), str):
                ents.add(e[k].lower())
        for a in e.get('aliases', []) or []:
            if isinstance(a, str):
                ents.add(a.lower())
        for a in (e.get('attributes') or []):
            lab = a.get('label') or a.get('name')
            if not lab:
                continue
            ai = AttrInfo(lab.lower())
            ai.aliases = set(x.lower() for x in (a.get('aliases') or []) if isinstance(x, str))
            t = a.get('type')
            ai.ptype = {'int': 'int', 'dec1': 'dec', 'dec2': 'dec', 'num': 'dec', 'money': 'money', 'cat': 'cat',
                        'ord': 'cat', 'boolean': 'boolean', 'bool': 'boolean', 'date': 'date',
                        'tag': 'tag'}.get(t, t)
            if ai.ptype == 'dec' and a.get('quantity_kind') == 'money':
                ai.ptype = 'money'
            ai.values = [v for v in (a.get('values') or a.get('enum') or []) if isinstance(v, str)]
            ai.unit = a.get('unit')
            ai.unit_syn = set(x for x in (a.get('unit_synonyms') or []) if isinstance(x, str))
            ai.places = a.get('places', a.get('decimals'))
            lx = a.get('lexicon') or {}
            st = lx.get('statements') or {}
            for k, v in st.items():
                if isinstance(v, str):
                    ai.statements.setdefault(k, []).append(v)
            if a.get('pos_statement'):
                ai.statements.setdefault('pos', []).append(a['pos_statement'])
            if a.get('neg_statement'):
                ai.statements.setdefault('neg', []).append(a['neg_statement'])
            if a.get('none_statement'):
                ai.statements.setdefault('none', []).append(a['none_statement'])
            res[ai.label].append(ai)
        for f in (e.get('fields') or []):
            w = f.get('word')
            if w:
                ai = AttrInfo(w.lower()); res[ai.label].append(ai)
    # packs-4 style typed lists
    for q in p.get('quantities', []) or []:
        ai = AttrInfo(q['name'].lower()); ai.ptype = 'dec' if q.get('decimals') else 'int'
        ai.unit = q.get('unit'); ai.places = q.get('decimals')
        for u in p.get('units', []) or []:
            if u.get('name') == ai.unit:
                ai.unit_syn = set(x for x in (u.get('plural'), u.get('abbr')) if x)
        cur = p.get('currency') or {}
        if isinstance(cur, dict) and cur.get('name') == ai.unit:
            ai.ptype = 'money'; ai.unit_syn = set(x for x in (cur.get('plural'),) if x)
        res[ai.label].append(ai)
    for b in p.get('bool_fields', []) or []:
        ai = AttrInfo(b['name'].lower()); ai.ptype = 'boolean'
        ai.aliases = set(x.lower() for x in b.get('aliases', []) or [])
        res[ai.label].append(ai)
    for c in p.get('cat_fields', []) or []:
        ai = AttrInfo(c['name'].lower()); ai.ptype = 'cat'
        ai.values = [v['name'] if isinstance(v, dict) else v for v in c.get('values', [])]
        res[ai.label].append(ai)
    for k in ('items',):
        pass
    return res, ents


# ----------------------------------------------------------------------------------------------- region algebra
class Space:
    """axes: key -> ('int', lo, hi) or ('set', frozenset)."""

    def __init__(self):
        self.axes = {}

    def full(self, k):
        a = self.axes[k]
        return (a[1], a[2]) if a[0] == 'int' else a[1]

    def is_int(self, k):
        return self.axes[k][0] == 'int'


def c_inter(sp, k, a, b):
    if sp.is_int(k):
        return (max(a[0], b[0]), min(a[1], b[1]))
    return a & b


def c_empty(sp, k, c):
    if sp.is_int(k):
        return c[0] > c[1]
    return len(c) == 0


def c_compl(sp, k, c):
    if sp.is_int(k):
        lo, hi = sp.full(k)
        out = []
        if c[0] > lo:
            out.append((lo, c[0] - 1))
        if c[1] < hi:
            out.append((c[1] + 1, hi))
        return out
    r = sp.full(k) - c
    return [r] if r else []


def box_and(sp, a, b):
    r = dict(a)
    for k, v in b.items():
        if k in r:
            w = c_inter(sp, k, r[k], v)
            if c_empty(sp, k, w):
                return None
            r[k] = w
        else:
            r[k] = v
    return r


def _bkey(b):
    return tuple(sorted((k, (v if isinstance(v, tuple) else tuple(sorted(map(repr, v))))) for k, v in b.items()))


def reg_and(sp, R1, R2):
    out, seen = [], set()
    for a in R1:
        for b in R2:
            c = box_and(sp, a, b)
            if c is not None:
                kk = _bkey(c)
                if kk not in seen:
                    seen.add(kk); out.append(c)
    return out


def reg_or(R1, R2):
    return R1 + R2


def box_not(sp, b):
    out, prefix = [], {}
    for k, v in b.items():
        for c in c_compl(sp, k, v):
            nb = dict(prefix); nb[k] = c
            out.append(nb)
        prefix[k] = v
    return out


def reg_not(sp, R):
    res = [{}]
    for b in R:
        res = reg_and(sp, res, box_not(sp, b))
        if not res:
            break
    return res


def reg_minus(sp, R1, R2):
    return reg_and(sp, R1, reg_not(sp, R2)) if R2 else list(R1)


FULL = [{}]
EMPTY = []


# ----------------------------------------------------------------------------------------------- card model
class Attr:
    def __init__(self, name, typ):
        self.name = name          # legend name (lower)
        self.typ = typ            # count/amount/qty/cat/flag/date/tag
        self.dec = 0
        self.values = []          # cat values / tag vocab (original case)
        self.unit = None
        self.unit_names = set()   # lower unit spellings for U2
        self.info = None          # AttrInfo

    @property
    def scale(self):
        return 10 ** self.dec


class Card:
    def __init__(self):
        self.attrs = []           # legend order
        self.byname = {}
        self.conv = []            # (u1 names set, k Fraction, u2 names set)
        self.defs = collections.OrderedDict()   # term name -> Def (card order)
        self.helpers = {}         # (word, section or None) -> Def
        self.def_section = {}     # term -> section label
        self.open_world = False
        self.ctype = None
        self.none_text = set()
        self.cbd_text = set()
        self.entity = None
        self.problems = []
        self.table_codes = []


class Def:
    def __init__(self, name, body_text):
        self.name = name
        self.body_text = body_text
        self.body = None
        self.onlyif = []
        self.exc = []
        self.section = None
        self.faq = []


# ----------------------------------------------------------------------------------------------- legend
TYPE_KW = re.compile(r'yes|no\b|date|tag|one of|one value|values|whole|number|count|amount|money|sum|decimal|'
                     r'figure|measured|negative|0 or more|zero|calendar|in |true|false|value', re.I)


def legend_parse(lines, pid, card):
    pa, ents = pack_attrs(pid)
    labels = sorted(pa.keys(), key=len, reverse=True)
    alias_map = {}
    for lab, lst in pa.items():
        for ai in lst:
            for al in ai.aliases:
                alias_map.setdefault(al, lab)
    seen = set()
    for ln in lines:
        s = strip_chrome(ln)
        hit = None
        for s2 in (s, re.sub(r'^(?:(?:The value of|Each|For|The|Its|A|An|Every|Field|Attribute)\s+)+', '', s, flags=re.I),
                   re.sub(r'^(?:The value of|Each|For|The|Its|A|An|Every)\s+', '', s, flags=re.I)):
            sl = s2.lower()
            for lab in labels:
                if sl.startswith(lab) and (len(sl) == len(lab) or sl[len(lab)] in ' (:,;'):
                    hit = lab; break
            if hit:
                break
        if hit is None:
            continue
        rest = s2[len(hit):]
        # a legend line describes a type; definition atoms ("x is between ...") are excluded
        if re.match(r'^\s*(is|are)\s+(between|from \d|at least|at most|more|fewer|less|under|over|above|below|up to|'
                    r'no |not |on or|before|after|within|exceeds|one of [^:]*;|yes\.?$|no\.?$)', rest, re.I) and \
                not re.search(r'yes or no|yes and no|calendar date|0 or more|zero or|whole number|decimals?\b|'
                              r'one of these|values?\b|negative', rest, re.I):
            continue
        if ':' in rest and re.search(r'of the following', rest):
            continue
        if not TYPE_KW.search(rest):
            continue
        if hit in seen:
            continue
        cand = pa[hit]
        typ, ai = classify_legend(rest, cand)
        if typ is None:
            card.problems.append('legend_type:' + hit)
            continue
        a = Attr(hit, typ)
        a.info = ai
        if typ in ('cat', 'tag'):
            vals = list(ai.values) if ai else []
            # keep values in legend order, as written in the line
            low = rest.lower()
            pos = []
            for v in vals:
                m = re.search(r'(?<![\w-])' + re.escape(v.lower()) + r'(?![\w-])', low)
                if m:
                    pos.append((m.start(), v))
            if len(pos) < len(vals):
                card.problems.append('legend_values:' + hit)
            a.values = [v for _, v in sorted(pos)] or vals
        if typ in ('count', 'amount', 'qty'):
            m = re.search(r'(?:at most|up to|no more than|with)\s+(\d)\s+decimal', rest, re.I) or \
                re.search(r'(\d)\s+decimal places?', rest, re.I)
            if m:
                a.dec = int(m.group(1))
            elif typ == 'amount':
                a.dec = 2
            elif re.search(r'whole', rest, re.I) or typ == 'count':
                a.dec = 0
            elif ai is not None and ai.places is not None:
                a.dec = int(ai.places)
            if ai is not None and ai.unit:
                a.unit = ai.unit
                a.unit_names = unit_forms(ai.unit) | set().union(*[unit_forms(u) for u in ai.unit_syn]) if ai.unit_syn else unit_forms(ai.unit)
        seen.add(hit)
        card.attrs.append(a)
        card.byname[hit] = a
    card.entity_words = ents


def unit_forms(u):
    u = u.lower().strip()
    out = {u}
    if u.endswith('s'):
        out.add(u[:-1])
    else:
        out.add(u + 's')
    if u.endswith('y'):
        out.add(u[:-1] + 'ies')
    if u.endswith('ies'):
        out.add(u[:-3] + 'y')
    return out


def classify_legend(rest, cand):
    r = rest.lower()
    pmap = {'int': 'count', 'dec': 'qty', 'money': 'amount', 'cat': 'cat', 'boolean': 'flag', 'date': 'date',
            'tag': 'tag'}
    kws = set()
    if re.search(r'\btags?\b', r):
        kws.add('tag')
    if re.search(r'yes or no|yes and no|yes/no|yes, no|true or false', r):
        kws.add('flag')
    if re.search(r'calendar date|\bdates?\b', r):
        kws.add('date')
    if re.search(r'one of|one value|values?\b|exactly one', r):
        kws.add('cat')
    if re.search(r'amount|money|\bsum\b|dollars|currency', r):
        kws.add('amount')
    if re.search(r'whole|count', r):
        kws.add('count')
    if re.search(r'decimal|measured|figure|non-negative|0 or more|zero|\bin [a-z]', r):
        kws.add('num')
    types = []
    for ai in cand:
        pt = pmap.get(ai.ptype)
        if pt and (pt, ai) not in types:
            types.append((pt, ai))
    distinct = set(t for t, _ in types)
    pick = None
    if len(distinct) == 1:
        pick = types[0]
    elif types:
        for t, ai in types:
            if t in kws or (t in ('count', 'qty', 'amount') and 'num' in kws):
                pick = (t, ai); break
    if pick is None:
        for k in ('tag', 'flag', 'cat', 'date', 'amount', 'count'):
            if k in kws:
                return k, (cand[0] if cand else None)
        if 'num' in kws:
            return 'qty', (cand[0] if cand else None)
        return None, None
    pt, ai = pick
    if pt in ('count', 'qty'):
        if re.search(r'whole', r) and not re.search(r'decimal', r):
            pt = 'count'
        elif re.search(r'decimal', r):
            pt = 'qty'
    return pt, ai


# ----------------------------------------------------------------------------------------------- values
NUM_RE = re.compile(r'^\s*(?P<cur>[$£€])?\s*(?P<num>-?\d+(?:\.\d+)?)\s*(?P<unit>.*?)\s*$')


def value_num(card, a, text):
    """numeric text (with optional unit) -> integer grid units of attribute a (U2)."""
    t = text.strip().strip('"\'').strip()
    t = re.sub(r'\s+', ' ', t)
    m = NUM_RE.match(t)
    if not m:
        raise ParseError('num:' + t[:40])
    v = Fraction(m.group('num'))
    u = m.group('unit').strip().rstrip('.').lower()
    if u:
        ok = (not a.unit_names) or u in a.unit_names or any(u == x for x in a.unit_names)
        if not ok:
            hit = False
            for u1, k, u2 in card.conv:
                if u in u1 and (not a.unit_names or (u2 & a.unit_names)):
                    v = v * k; hit = True; break
            if not hit:
                # currency words, unit synonyms not in the pack list: accept only if no conversion names the unit
                if any(u in u1 for u1, _, _ in card.conv):
                    raise ParseError('unit:' + u)
                card.problems.append('unit_unknown:' + a.name + ':' + u)
    g = v * a.scale
    if g.denominator != 1:
        raise ParseError('offgrid:%s:%s' % (a.name, t))
    return int(g)


def find_values(a, text):
    """category / tag values named in a list text, in order; the rest must be separators only."""
    low = ' ' + text.lower().strip().rstrip('.') + ' '
    vals = sorted(a.values, key=len, reverse=True)
    found = []
    used = [False] * len(low)
    for v in vals:
        for m in re.finditer(r'(?<![\w-])' + re.escape(v.lower()) + r'(?![\w-])', low):
            if any(used[m.start():m.end()]):
                continue
            for i in range(m.start(), m.end()):
                used[i] = True
            found.append((m.start(), v))
    rest = ''.join(ch if not used[i] else ' ' for i, ch in enumerate(low))
    rest = re.sub(r'\b(and|or|the|tags?|values?|of|either)\b', ' ', rest)
    rest = re.sub(r'[\s,;/&+]+', '', rest)
    return [v for _, v in sorted(found)], rest


# ----------------------------------------------------------------------------------------------- atoms
def num_c(card, a, txt):
    return value_num(card, a, txt)


def date_c(txt):
    v = parse_date(txt.strip().rstrip('.'))
    if v is None:
        raise ParseError('date:' + txt[:30])
    return v


GE = r'(?:is |are )?(?:at least|no fewer than|not fewer than|not less than|no less than|greater than or equal to|a minimum of|not below|not under|no lower than)'
LE = r'(?:is |are )?(?:at most|no more than|not more than|up to|no greater than|a maximum of|not above|not over|not greater than|no higher than|not exceeding)'
GT = r'(?:is |are )?(?:more than|over|above|greater than|higher than|exceeds|in excess of)'
LT = r'(?:is |are )?(?:fewer than|less than|under|below|lower than|short of)'


def atom_numeric(card, a, rest):
    r = rest.strip().rstrip('.').strip()
    m = re.fullmatch(r'(?:is )?between (.+?) and (.+)', r)
    if m:
        return ('iv', num_c(card, a, m.group(1)), num_c(card, a, m.group(2)))
    m = re.fullmatch(r'(?:is )?from (.+?) up to but not including (.+)', r)
    if m:
        return ('iv', num_c(card, a, m.group(1)), num_c(card, a, m.group(2)) - 1)
    m = re.fullmatch(r'(?:is )?from (.+?) (?:to|through) (.+)', r)
    if m:
        return ('iv', num_c(card, a, m.group(1)), num_c(card, a, m.group(2)))
    m = re.fullmatch(GE + r' (.+)', r) or re.fullmatch(r'(?:is )?(.+?) or (?:more|above|greater|higher|over|larger)', r)
    if m:
        return ('iv', num_c(card, a, m.group(1)), INF)
    m = re.fullmatch(LE + r' (.+)', r) or re.fullmatch(r'(?:is )?(.+?) or (?:less|fewer|below|under|lower|smaller)', r)
    if m:
        return ('iv', -INF, num_c(card, a, m.group(1)))
    m = re.fullmatch(GT + r' (.+)', r)
    if m:
        return ('iv', num_c(card, a, m.group(1)) + 1, INF)
    m = re.fullmatch(LT + r' (.+)', r)
    if m:
        return ('iv', -INF, num_c(card, a, m.group(1)) - 1)
    m = re.fullmatch(r'is not (?:equal to )?(.+)', r)
    if m:
        c = num_c(card, a, m.group(1))
        return ('niv', c, c)
    m = re.fullmatch(r'is (?:exactly |equal to )?(.+)', r)
    if m:
        c = num_c(card, a, m.group(1))
        return ('iv', c, c)
    raise ParseError('numop:' + a.name + ':' + r[:60])


def atom_date(card, a, rest):
    r = rest.strip().rstrip('.').strip()
    m = re.fullmatch(r'(?:is |falls )?within (\d+) (?:calendar )?days? (after|before) (?:the |its )?(.+)', r)
    if m:
        n = int(m.group(1)); e = m.group(3).strip().lower()
        e = re.sub(r'^(?:date of |the date of )', '', e)
        ea = card.byname.get(e)
        if ea is None:
            ea = match_attr(card, e, full=True)
        if ea is None:
            raise ParseError('rel_event:' + e)
        if m.group(2) == 'after':
            return ('rel', ea.name, 1, n)
        return ('rel', ea.name, -n, -1)
    m = re.fullmatch(r'(?:is |falls )?between (.+?) and (.+)', r)
    if m:
        return ('iv', date_c(m.group(1)), date_c(m.group(2)))
    m = re.fullmatch(r'(?:is |falls )?(?:from|in the window from) (.+?) (?:to|through|until) (.+)', r)
    if m:
        return ('iv', date_c(m.group(1)), date_c(m.group(2)))
    m = re.fullmatch(r'(?:is |falls )?(?:on or before|no later than|not after) (.+)', r)
    if m:
        return ('iv', -INF, date_c(m.group(1)))
    m = re.fullmatch(r'(?:is |falls )?(?:on or after|no earlier than|not before) (.+)', r)
    if m:
        return ('iv', date_c(m.group(1)), INF)
    m = re.fullmatch(r'(?:is |falls )?(?:before|earlier than|prior to) (.+)', r)
    if m:
        return ('iv', -INF, date_c(m.group(1)) - 1)
    m = re.fullmatch(r'(?:is |falls )?(?:after|later than) (.+)', r)
    if m:
        return ('iv', date_c(m.group(1)) + 1, INF)
    m = re.fullmatch(r'is not (?:on )?(.+)', r)
    if m:
        c = date_c(m.group(1)); return ('niv', c, c)
    m = re.fullmatch(r'is (?:on )?(.+)', r)
    if m:
        c = date_c(m.group(1)); return ('iv', c, c)
    raise ParseError('dateop:' + a.name + ':' + r[:60])


def atom_cat(card, a, rest):
    r = rest.strip().rstrip('.').strip()
    neg = False
    m = re.fullmatch(r'(?:is|are) (?:any value |anything |any |a value )?(?:other than|except|but|apart from|besides) (.+)', r)
    if m:
        neg, lst = True, m.group(1)
    else:
        m = re.fullmatch(r'(?:is|are) not (?:one of |any of |among |in )?(.+)', r)
        if m:
            neg, lst = True, m.group(1)
        else:
            m = re.fullmatch(r'(?:is|are) (?:one of |any of |among |in )?(.+)', r)
            if not m:
                raise ParseError('catop:' + a.name + ':' + r[:60])
            lst = m.group(1)
    vals, left = find_values(a, lst)
    if not vals or left:
        raise ParseError('catvals:' + a.name + ':' + lst[:60])
    return ('cat', frozenset(vals), neg)


def atom_flag(card, a, rest):
    r = rest.strip().rstrip('.').strip().lower()
    if r in ('is yes', 'is true', 'is set', 'holds', 'is yes (true)', 'was yes'):
        return ('flag', True)
    if r in ('is no', 'is false', 'is not set', 'is no (false)', 'was no'):
        return ('flag', False)
    raise ParseError('flagop:' + a.name + ':' + r[:40])


def atom_tag(card, a, rest):
    r = rest.strip().rstrip('.').strip()
    m = re.fullmatch(r'(?:has|includes|lists|contains|carries) at least (\d+) tags?', r)
    if m:
        return ('tagcount', None, int(m.group(1)))
    m = re.fullmatch(r'(?:has|includes|lists|contains|carries) at least (\d+) of (?:the tags |these tags |the following tags |the tags: )?(.+)', r)
    if m:
        vals, left = find_values(a, m.group(2))
        if not vals or left:
            raise ParseError('tagvals:' + m.group(2)[:50])
        return ('tagcount', frozenset(vals), int(m.group(1)))
    for kw, op in (('any', 'any'), ('all', 'all'), ('none', 'none')):
        m = re.fullmatch(r'(?:has|includes|lists|contains|carries) ' + kw + r' of (?:the tags |these tags |the following tags |the tags: )?(.+)', r)
        if m:
            vals, left = find_values(a, m.group(1))
            if not vals or left:
                raise ParseError('tagvals:' + m.group(1)[:50])
            return ('tagset', frozenset(vals), op)
    m = re.fullmatch(r'(?:has|includes|lists|contains|carries) (?:the )?(?:tag )?(.+)', r)
    if m:
        vals, left = find_values(a, m.group(1))
        if len(vals) == 1 and not left:
            return ('tagset', frozenset(vals), 'any')
    m = re.fullmatch(r'(?:does not have|does not include|lacks) (?:the )?(?:tag )?(.+)', r)
    if m:
        vals, left = find_values(a, m.group(1))
        if len(vals) == 1 and not left:
            return ('tagset', frozenset(vals), 'none')
    raise ParseError('tagop:' + a.name + ':' + r[:60])


def match_attr(card, s, full=False):
    sl = s.lower().strip()
    sl = re.sub(r"^(?:the |its |the record's |their )", '', sl)
    for a in sorted(card.attrs, key=lambda x: len(x.name), reverse=True):
        if full:
            if sl == a.name:
                return a
        elif sl.startswith(a.name + ' ') or sl == a.name:
            return a
    return None


def parse_atom(card, s, attr=None):
    s = s.strip()
    if attr is None:
        sl = s.lower()
        sl2 = re.sub(r"^(?:the |its |the record's |their )", '', sl)
        off = len(sl) - len(sl2)
        a = None
        for x in sorted(card.attrs, key=lambda x: len(x.name), reverse=True):
            if sl2.startswith(x.name + ' '):
                a = x; break
        if a is None:
            raise ParseError('noattr:' + s[:50])
        rest = s[off + len(a.name):].strip()
    else:
        a, rest = attr, s
    rest = re.sub(r'^(?:value |entry |figure )', '', rest)
    if a.typ in ('count', 'amount', 'qty'):
        at = atom_numeric(card, a, rest)
    elif a.typ == 'date':
        at = atom_date(card, a, rest)
    elif a.typ == 'cat':
        at = atom_cat(card, a, rest)
    elif a.typ == 'flag':
        at = atom_flag(card, a, rest)
    elif a.typ == 'tag':
        at = atom_tag(card, a, rest)
    else:
        raise ParseError('atomtype')
    return ('atom', a.name) + at


# ----------------------------------------------------------------------------------------------- definitions
LIST_HEAD = re.compile(r'^(all|any|none|not all) of the following(?: conditions?)?(?: hold| holds| apply| applies)?\s*:\s*(.*)$', re.I)


class DefParser:
    def __init__(self, card, names):
        self.card = card
        self.names = names            # set of defined names (terms and helper words)

    def ref(self, s):
        t = s.strip().rstrip('.').strip()
        t = re.sub(r"^(?:it|the record|this record|the case|the item|they|that record)\s+", '', t, flags=re.I)
        ents = getattr(self.card, 'entity_words', set())
        tl = t.lower()
        for e in sorted(ents, key=len, reverse=True):
            for pre in ('the ' + e + ' ', 'this ' + e + ' ', e + ' '):
                if tl.startswith(pre):
                    t = t[len(pre):]; tl = t.lower(); break
        m = re.fullmatch(r'(?:is|meets the definition of|qualifies as) (not )?(?:an? )?(.+)', t, flags=re.I) or \
            re.fullmatch(r'(?:does) (not) (?:meet the definition of|qualify as) (?:an? )?(.+)', t, flags=re.I)
        if m:
            nm = m.group(2).strip()
            if nm in self.names:
                return ('ref', nm, bool(m.group(1)))
            for n in self.names:
                if n.lower() == nm.lower():
                    return ('ref', n, bool(m.group(1)))
        raise ParseError('ref:' + s[:50])

    def atom_or_ref(self, s):
        try:
            return parse_atom(self.card, s)
        except ParseError as e1:
            try:
                return self.ref(s)
            except ParseError:
                raise e1

    def item(self, s):
        s = s.strip()
        m = re.match(r'^(.*?),?\s+unless\s+(.+)$', s)
        if m:
            a = parse_atom(self.card, m.group(1))
            b = self.atom_or_ref(m.group(2))
            return ('unless', a, b)
        return self.atom_or_ref(s)

    def body(self, s):
        s = s.strip()
        s = re.sub(r'\.$', '', s).strip()
        m = LIST_HEAD.match(s)
        if m:
            head = m.group(1).lower()
            items = [x for x in re.split(r';\s+', m.group(2)) if x.strip()]
            if not items:
                raise ParseError('emptylist')
            its = [self.item(x) for x in items]
            return ({'all': 'all', 'any': 'any', 'none': 'notany', 'not all': 'notall'}[head], its)
        m = re.match(r'^either (.+), but not both$', s, flags=re.I) or re.match(r'^either (.+) but not both$', s, flags=re.I)
        if m:
            inner = m.group(1)
            for mm in re.finditer(r' or ', inner):
                a, b = inner[:mm.start()], inner[mm.end():]
                try:
                    return ('xor', [self.atom_or_ref(a), self.atom_or_ref(b)])
                except ParseError:
                    continue
            raise ParseError('xor:' + s[:60])
        m = re.match(r'^neither (.+)$', s, flags=re.I)
        if m:
            inner = m.group(1)
            for mm in re.finditer(r' nor ', inner):
                a, b = inner[:mm.start()], inner[mm.end():]
                try:
                    return ('notany', [self.atom_or_ref(a), self.atom_or_ref(b)])
                except ParseError:
                    continue
            raise ParseError('neither:' + s[:60])
        return ('all', [self.item(s)])


ONLYIF_RE = re.compile(r'^(?:A|a) (?:record|case) (?:is|counts as|qualifies as) an? (?P<n>.+?) only if (?P<c>.+)$')
EXC_RE = re.compile(r'^Exception:\s*(?:a|any) (?:record|case) (?:with|where|in which|whose) (?P<b>.+) is not an? (?P<n>.+)$|'
                    r'^Exception:\s*(?:a|any) (?:record|case) (?:that|which) (?P<b2>.+) is not an? (?P<n2>.+)$')


def split_sentences(text):
    text = re.sub(r'\s*\((?:e\.g\.|for example|example:?)\s[^()]*(?:\([^()]*\)[^()]*)*\)', '', text)
    parts = re.split(r'(?<=\.)\s+(?=[A-Z"\'«(\[])', text.strip())
    return [p.strip() for p in parts if p.strip()]


HEAD_RES = [
    re.compile(r'^(?:A|a) (?:record|case) is an? (?P<n>.+?) exactly when (?P<b>.+)$'),
    re.compile(r'^(?:A|a) (?:record|case) counts as an? (?P<n>.+?) exactly when (?P<b>.+)$'),
    re.compile(r'^(?P<n>[^:|=]{1,60}?) means (?P<b>.+)$'),
    re.compile(r'^(?P<n>[^:|=]{1,60}?)\s*(?::|=|\||—|–|->|→|::)\s+(?P<b>.+)$'),
]
HELPER_RES = [
    re.compile(r'^In section (?P<s>.+?) only,\s*(?P<w>.+?) means (?P<b>.+)$', re.I),
    re.compile(r'^(?:Within|Inside|For) section (?P<s>.+?) only,\s*(?P<w>.+?) means (?P<b>.+)$', re.I),
    re.compile(r'^(?:In|Within|Throughout|Across|For|Elsewhere in|Everywhere in|Outside[^,]*?in) (?:this|the) [^,]{1,60},\s*(?P<w>.+?) means (?P<b>.+)$', re.I),
]
SECTION_RE = re.compile(r'^(?:Part|Section|Chapter|Clause|Article|Annex|Schedule|Division|Unit)\s+(?P<s>[A-Z0-9]{1,3})\b', re.I)
NON_NAME = re.compile(r"^(?:example|exception|note|q|a|answer|outcome|question|result|reader|for|when|if|the|this|"
                      r"each|every|in|attributes?|what|dates?|numbers?|values?)\b", re.I)


def parse_card_defs(card, lines, sampler):
    """find definitions (term heads), helpers, sections, only-if and exception sentences."""
    cands = []            # (name, body_text, section, line_index)
    helpers = []          # (word, section, body_text)
    extra = []            # sentences (only-if / exception) seen anywhere
    faq = []              # (name, answer sentence)
    section = None
    prev_name_line = None
    for i, raw in enumerate(lines):
        mt = re.match(r'^\s*>?\s*<\s*(/)?\s*(?:section|part|sec)[_\s-]*([A-Za-z0-9]{0,3})\s*>\s*$', raw, re.I)
        if mt:
            section = None if mt.group(1) else (mt.group(2).upper() or None)
            continue
        s = strip_chrome(raw)
        if not s:
            continue
        msec = SECTION_RE.match(s.strip('[]()*_:# '))
        if msec and len(s) < 60 and ':' not in s[:-1] and ' means ' not in s:
            section = msec.group('s').upper()
            continue
        hm = None
        for rx in HELPER_RES:
            hm = rx.match(s)
            if hm:
                break
        if hm:
            sents = split_sentences(hm.group('b'))
            sec = hm.groupdict().get('s')
            helpers.append((hm.group('w').strip(), sec.strip().upper() if sec else None, sents[0] if sents else ''))
            continue
        if s.startswith('Q:') or ' Q: ' in s:
            pass
        found = None
        for rx in HEAD_RES:
            m = rx.match(s)
            if m:
                nm = m.group('n').strip().strip('"\'')
                if NON_NAME.match(nm) and not re.fullmatch(r'[A-Z]\d{1,2}', nm):
                    continue
                if len(nm.split()) > 4 or not nm:
                    continue
                found = (nm, m.group('b'))
                break
        if found is None and prev_name_line is not None:
            nm = prev_name_line
            found = (nm, s)
        prev_name_line = None
        if found is None:
            if re.fullmatch(r"[A-Za-z][\w'-]{0,30}(?: [\w'-]{1,20}){0,2}", s) and not NON_NAME.match(s):
                prev_name_line = s
            for sent in split_sentences(s):
                extra.append(sent)
            continue
        nm, rest = found
        # FAQ answers (S5): "... Q: question? A: answer."
        qa = re.split(r'\s+Q:\s+', rest)
        rest = qa[0]
        for q in qa[1:]:
            mm = re.search(r'\?\s+A:\s+(.+)$', q)
            if mm:
                faq.append((nm, mm.group(1).strip()))
        sents = split_sentences(rest)
        if not sents:
            continue
        cands.append((nm, sents[0], section, i))
        for sent in sents[1:]:
            extra.append(sent)
    return cands, helpers, extra, faq


def build_card(card, lines, sampler):
    cands, helpers, extra, faq = parse_card_defs(card, lines, sampler)
    names = set(n for n, _, _, _ in cands) | set(w for w, _, _ in helpers)
    dp = DefParser(card, names)
    ok_defs = collections.OrderedDict()
    for nm, body, sec, i in cands:
        try:
            b = dp.body(body)
        except ParseError as e:
            card.problems.append('defparse:%s:%s' % (nm, e))
            continue
        if nm in ok_defs:
            # the same definition printed twice (option line + moved block): must agree
            if repr(ok_defs[nm].body) != repr(b):
                card.problems.append('dupdef:' + nm)
            continue
        d = Def(nm, body); d.body = b; d.section = sec
        ok_defs[nm] = d
    names = set(ok_defs) | set(w for w, _, _ in helpers)
    dp.names = names
    # re-parse bodies that failed only because a name was not known yet (forward references)
    for nm, body, sec, i in cands:
        if nm not in ok_defs:
            try:
                b = dp.body(body)
                d = Def(nm, body); d.body = b; d.section = sec
                ok_defs[nm] = d
                card.problems = [p for p in card.problems if not p.startswith('defparse:%s:' % nm)]
            except ParseError:
                pass
    for w, sec, body in helpers:
        try:
            d = Def(w, body); d.body = dp.body(body); d.section = sec
            card.helpers[(w, sec)] = d
        except ParseError as e:
            card.problems.append('helperparse:%s:%s' % (w, e))
    for sent in extra:
        s = sent.strip()
        m = ONLYIF_RE.match(s.rstrip('.'))
        if m and m.group('n') in ok_defs:
            try:
                ok_defs[m.group('n')].onlyif.append(dp.atom_or_ref(m.group('c')))
            except ParseError as e:
                card.problems.append('onlyif:%s' % e)
            continue
        m = EXC_RE.match(s.rstrip('.'))
        if m:
            n = m.group('n') or m.group('n2')
            b = m.group('b') if m.group('b') is not None else m.group('b2')
            if n in ok_defs:
                try:
                    if m.group('b2') is not None:
                        ok_defs[n].exc.append(dp.ref(b))
                    else:
                        ok_defs[n].exc.append(dp.atom_or_ref(b))
                except ParseError as e:
                    card.problems.append('exc:%s' % e)
            continue
    for nm, ans in faq:
        if nm not in ok_defs:
            continue
        for sent in split_sentences(ans):
            s = sent.rstrip('.')
            m = EXC_RE.match(s)
            if m and (m.group('n') or m.group('n2')) == nm:
                b = m.group('b') if m.group('b') is not None else m.group('b2')
                try:
                    ok_defs[nm].exc.append(dp.ref(b) if m.group('b2') is not None else dp.atom_or_ref(b))
                except ParseError as e:
                    card.problems.append('faqexc:%s' % e)
                continue
            m = ONLYIF_RE.match(s)
            if m and m.group('n') == nm:
                try:
                    ok_defs[nm].onlyif.append(dp.atom_or_ref(m.group('c')))
                except ParseError as e:
                    card.problems.append('faqonly:%s' % e)
                continue
            ok_defs[nm].faq.append(s)
    card.defs = ok_defs
    return card


# ----------------------------------------------------------------------------------------------- compile to regions
def make_space(card):
    sp = Space()
    rel_attrs = set()
    for a in card.attrs:
        if a.typ in ('count', 'amount', 'qty'):
            sp.axes[a.name] = ('int', 0, INF)
        elif a.typ == 'date':
            sp.axes[a.name] = ('int', -INF, INF)
        elif a.typ == 'flag':
            sp.axes[a.name] = ('set', frozenset([True, False]))
        elif a.typ == 'cat':
            sp.axes[a.name] = ('set', frozenset(a.values))
        elif a.typ == 'tag':
            subs = []
            for r in range(len(a.values) + 1):
                for c in itertools.combinations(a.values, r):
                    subs.append(frozenset(c))
            sp.axes[a.name] = ('set', frozenset(subs))
    return sp


def atom_region(sp, at):
    _, an, kind = at[0], at[1], at[2]
    if kind == 'iv':
        lo, hi = at[3], at[4]
        return [{an: (lo, hi)}] if lo <= hi else []
    if kind == 'niv':
        return box_not(sp, {an: (at[3], at[4])})
    if kind == 'rel':
        ev, lo, hi = at[3], at[4], at[5]
        key = 'rel|%s|%s' % (an, ev)
        if key not in sp.axes:
            sp.axes[key] = ('int', -INF, INF)
        return [{key: (lo, hi)}]
    if kind == 'cat':
        vals, neg = at[3], at[4]
        s = (sp.full(an) - vals) if neg else (sp.full(an) & vals)
        return [{an: frozenset(s)}] if s else []
    if kind == 'flag':
        return [{an: frozenset([at[3]])}]
    if kind == 'tagset':
        S, op = at[3], at[4]
        full = sp.full(an)
        if op == 'any':
            s = [x for x in full if x & S]
        elif op == 'all':
            s = [x for x in full if S <= x]
        else:
            s = [x for x in full if not (x & S)]
        return [{an: frozenset(s)}] if s else []
    if kind == 'tagcount':
        S, k = at[3], at[4]
        full = sp.full(an)
        s = [x for x in full if len(x if S is None else (x & S)) >= k]
        return [{an: frozenset(s)}] if s else []
    raise ParseError('atomkind:' + str(kind))


class Compiler:
    def __init__(self, card, sp):
        self.card, self.sp = card, sp
        self.cache = {}

    def term(self, name, section=None, stack=()):
        key = (name, section)
        if key in self.cache:
            return self.cache[key]
        if name in stack:
            raise ParseError('cycle:' + name)
        card = self.card
        if name in card.defs:
            d = card.defs[name]
            sec = d.section
        else:
            d = card.helpers.get((name, section)) or card.helpers.get((name, None))
            if d is None:
                raise ParseError('undef:' + name)
            sec = d.section if d.section else section
        st = stack + (name,)
        R = self.node(d.body, sec, st)
        for c in d.onlyif:
            R = reg_and(self.sp, R, self.node(c, sec, st))
        for b in d.exc:
            R = reg_minus(self.sp, R, self.node(b, sec, st))
        self.cache[key] = R
        return R

    def node(self, n, sec, st):
        sp = self.sp
        k = n[0]
        if k == 'atom':
            return atom_region(sp, n)
        if k == 'ref':
            R = self.term(n[1], sec, st)
            return reg_not(sp, R) if n[2] else R
        if k == 'unless':
            return reg_minus(sp, self.node(n[1], sec, st), self.node(n[2], sec, st))
        items = [self.node(x, sec, st) for x in n[1]]
        if k == 'all':
            R = FULL
            for x in items:
                R = reg_and(sp, R, x)
            return R
        if k == 'any':
            R = []
            for x in items:
                R = reg_or(R, x)
            return R
        if k == 'notany':
            R = []
            for x in items:
                R = reg_or(R, x)
            return reg_not(sp, R)
        if k == 'notall':
            R = FULL
            for x in items:
                R = reg_and(sp, R, x)
            return reg_not(sp, R)
        if k == 'xor':
            a, b = items
            return reg_or(reg_minus(sp, a, b), reg_minus(sp, b, a))
        raise ParseError('node:' + k)


# ----------------------------------------------------------------------------------------------- reading rules
def read_rules(card, text):
    t = text
    m = None
    for mm in re.finditer(r"(?:\b1|\b[Oo]ne|\b[Ee]ach|\b[Ee]very|\bAn?|\ban?) ([A-Za-z][A-Za-z./²³%°-]{0,20}(?: [A-Za-z./²³%°-]{1,20})?) "
                          r"(?:=|equals|is equal to|is the same as|corresponds to|makes|converts to|is) (\d+(?:\.\d+)?) "
                          r"([A-Za-z][A-Za-z./²³%°-]{0,20}(?: [A-Za-z./²³%°-]{1,20})?)(?=[).,;:]|\s+before|\s+when|\s*$)", t):
        u1, k, u2 = mm.group(1).strip().lower(), Fraction(mm.group(2)), mm.group(3).strip().lower()
        ent = (frozenset(unit_forms(u1)), k, frozenset(unit_forms(u2)))
        if ent not in card.conv:
            card.conv.append(ent)
    low = t.lower()
    card.open_world = bool(re.search(r"leave facts out|left-out fact|leaves? (?:some )?facts? out|may omit|left out|"
                                     r"not every fact|facts? (?:may be|can be) (?:missing|omitted|left out)", low))
    # quoted option texts in the abstain sentences
    for sent in re.split(r'(?<=[.!?])\s+', t):
        sl = sent.lower()
        qs = re.findall(r"'([^']{3,80})'", sent)
        if 'if it is an option' in sl or 'meets the definition of no term' in sl or 'no term on this card' in sl \
                or 'none of the terms' in sl or 'is an option' in sl:
            for q in qs:
                if re.search(r'\bnone\b|\bno term\b|\bnot any\b', q.lower()):
                    card.none_text.add(q)
        if 'only if different possible values' in sl or 'different possible values' in sl:
            if qs:
                card.cbd_text.add(qs[0])
        if sl.startswith('if both are shown') and len(qs) >= 2:
            pass


# ----------------------------------------------------------------------------------------------- records
def _markers():
    try:
        m = json.load(open(os.path.join(CSRC, 'common', 'markers.json')))
        w = set(x.lower() for x in m['classes']['unknown']['words'])
    except Exception:
        w = set()
    return w | {'not recorded', 'unknown', 'null', '~'}


MARKERS = _markers()


def parse_value(card, a, raw):
    """value text or typed value -> axis value; returns ('omit',) for an omission marker."""
    if raw is None:
        return ('omit',)
    if isinstance(raw, bool):
        if a.typ == 'flag':
            return raw
        raise ParseError('bool_for:' + a.name)
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        raw = repr(raw) if isinstance(raw, float) else str(raw)
    if isinstance(raw, list):
        if a.typ == 'tag':
            vals = []
            for x in raw:
                v, left = find_values(a, str(x))
                if len(v) != 1 or left:
                    raise ParseError('tagitem:' + str(x)[:30])
                vals.append(v[0])
            return frozenset(vals)
        raise ParseError('list_for:' + a.name)
    s = str(raw).strip().strip('"\'').strip().rstrip('.').strip()
    if re.fullmatch(r'\[\s*[^\[\]]*?\s*\]', s) or re.fullmatch(r'\(\s*[^()]*?\s*\)', s):
        s = s[1:-1].strip()
    if s.lower() in MARKERS:
        return ('omit',)
    if a.typ == 'flag':
        sl = s.lower()
        if sl in ('yes', 'true', 'y', '✓', 'x', 'checked', '[x]', '☑'):
            return True
        if sl in ('no', 'false', 'n', '☐', '[ ]', 'unchecked'):
            return False
        raise ParseError('flagval:' + s[:30])
    if a.typ == 'date':
        v = parse_date(s)
        if v is None:
            raise ParseError('dateval:' + s[:30])
        return v
    if a.typ == 'cat':
        vals, left = find_values(a, s)
        if len(vals) != 1 or left:
            raise ParseError('catval:%s:%s' % (a.name, s[:30]))
        return vals[0]
    if a.typ == 'tag':
        if s.lower() in ('none', 'no tags', '(none)'):
            return frozenset()
        vals, left = find_values(a, s)
        if not vals or left:
            raise ParseError('tagval:%s:%s' % (a.name, s[:40]))
        return frozenset(vals)
    return value_num(card, a, s)


def attr_by_key(card, k):
    nk = norm_key(k)
    for a in card.attrs:
        if norm_key(a.name) == nk:
            return a
    return None


def kv_from_json(card, text):
    out = {}
    starts = [i for i, ch in enumerate(text) if ch in '{[']
    for st in starts[:3]:
        for en in range(len(text), st, -1):
            if text[en - 1] not in '}]':
                continue
            try:
                obj = json.loads(text[st:en])
            except Exception:
                continue

            def walk(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        a = attr_by_key(card, k) if isinstance(k, str) else None
                        if a is not None and not isinstance(v, dict):
                            out.setdefault(a.name, []).append(v)
                        else:
                            walk(v)
                elif isinstance(o, list):
                    for x in o:
                        walk(x)
            walk(obj)
            return out
    return out


SEP_RE = r'\s*(?:::|:|=|\||—|–|->|→|\.{2,}|…+|\s-\s|\t)\s*'


def kv_from_lines(card, text):
    """key/value pairs from labelled lines, inline 'key: value.' sentences, '[key] value', 'The key is value.'"""
    out = {}
    names = sorted(card.attrs, key=lambda a: len(a.name), reverse=True)
    segs = []
    for raw in text.split('\n'):
        line = strip_chrome(raw.replace('\t', ' | '))
        if not line:
            continue
        for seg in re.split(r'(?<=[A-Za-z)\]"\'%])\.\s+|(?<=\d)\.\s+(?=[A-Za-z])|;\s+(?=[A-Za-z])', line):
            segs.append(seg.strip())
    for seg in segs:
        sg = seg.strip().strip('|').strip()
        sg = re.sub(r'^\[([^\]]+)\]\s*', r'\1: ', sg)
        low = sg.lower()
        low2 = re.sub(r'^(?:the|its)\s+', '', low)
        off = len(low) - len(low2)
        for a in names:
            for form in (a.name, a.name.replace(' ', '_'), a.name.replace(' ', '-')):
                if low2.startswith(form):
                    rest = sg[off + len(form):]
                    m = re.match(SEP_RE + r'(.+)$', rest) or re.match(r'\s+(?:is|was|are|were)\s+(.+)$', rest)
                    if m:
                        val = m.group(1).strip().rstrip('.').strip().strip('|').strip()
                        out.setdefault(a.name, []).append(val)
                        break
            else:
                # camelCase / snake keys
                mk = re.match(r'^([A-Za-z0-9_ -]{2,60}?)' + SEP_RE + r'(.+)$', sg)
                if mk and norm_key(mk.group(1)) == norm_key(a.name):
                    out.setdefault(a.name, []).append(mk.group(2).strip().rstrip('.').strip())
                    break
                continue
            break
    return out


def kv_from_table(card, text):
    out = {}
    lines = [l for l in text.split('\n')]
    for i, raw in enumerate(lines):
        l = TAG_RE.sub(' ', raw).strip()
        if not l:
            continue
        # header candidates: pipes, commas, semicolons, tabs, 2+ spaces
        for kind in ('pipe', 'tab', 'csv', 'semi', 'ws'):
            cells = split_cells(l, kind)
            if cells is None or len(cells) < 2:
                continue
            ats = [attr_by_key(card, c) for c in cells]
            if sum(1 for x in ats if x is not None) < 2:
                continue
            # find the next data line
            for j in range(i + 1, min(i + 4, len(lines))):
                d = TAG_RE.sub(' ', lines[j]).strip()
                if not d or re.fullmatch(r'[|+:\-= ]+', d):
                    continue
                if kind == 'ws':
                    vals = fixed_cells(raw, lines[j], cells)
                else:
                    vals = split_cells(d, kind)
                if vals is None or len(vals) != len(cells):
                    break
                for a, v in zip(ats, vals):
                    if a is not None:
                        out.setdefault(a.name, []).append(v)
                break
            if out:
                return out
    return out


def split_cells(l, kind):
    if kind == 'pipe':
        if '|' not in l:
            return None
        s = l.strip()
        if s.startswith('|'):
            s = s[1:]
        if s.endswith('|'):
            s = s[:-1]
        return [c.strip() for c in s.split('|')]
    if kind == 'tab':
        return [c.strip() for c in l.split('\t')] if '\t' in l else None
    if kind in ('csv', 'semi'):
        import csv
        d = ',' if kind == 'csv' else ';'
        if d not in l:
            return None
        try:
            return [c.strip() for c in next(csv.reader([l], delimiter=d, skipinitialspace=True))]
        except Exception:
            return None
    if kind == 'ws':
        return [c.strip() for c in re.split(r'\s{2,}', l.strip())]
    return None


def fixed_cells(header_raw, data_raw, cells):
    pos = []
    p = 0
    for c in cells:
        k = header_raw.find(c, p)
        if k < 0:
            return None
        pos.append(k); p = k + len(c)
    out = []
    for n, k in enumerate(pos):
        e = pos[n + 1] if n + 1 < len(pos) else len(data_raw) + 1
        out.append(data_raw[k:e].strip() if k < len(data_raw) else '')
    return out


def kv_from_html(card, text):
    out = {}
    dl = re.findall(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', text, re.S | re.I)
    for k, v in dl:
        a = attr_by_key(card, TAG_RE.sub('', k))
        if a:
            out.setdefault(a.name, []).append(TAG_RE.sub('', v).strip())
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', text, re.S | re.I)
    if rows:
        cells = [[TAG_RE.sub('', c).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S | re.I)] for r in rows]
        # header row + data row, or key/value rows
        for i, cl in enumerate(cells):
            ats = [attr_by_key(card, c) for c in cl]
            if sum(1 for x in ats if x) >= 2 and i + 1 < len(cells) and len(cells[i + 1]) == len(cl):
                for a, v in zip(ats, cells[i + 1]):
                    if a:
                        out.setdefault(a.name, []).append(v)
                break
            if len(cl) == 2 and attr_by_key(card, cl[0]):
                out.setdefault(attr_by_key(card, cl[0]).name, []).append(cl[1])
    for k, v in re.findall(r'<(?:li|p|div|span)[^>]*>\s*(?:<[^>]+>)*([^<:]{2,60}?)(?:</[^>]+>)*\s*:\s*(.*?)</(?:li|p|div|span)>', text, re.S | re.I):
        a = attr_by_key(card, k)
        if a:
            out.setdefault(a.name, []).append(TAG_RE.sub('', v).strip())
    for k, v in re.findall(r'<([a-z_][\w-]*)>([^<]*)</\1>', text, re.I):
        a = attr_by_key(card, k)
        if a:
            out.setdefault(a.name, []).append(v.strip())
    return out


def kv_from_prose(card, text):
    """templated statements from the pack attribute lexicon."""
    out = {}
    sents = []
    for ln in TAG_RE.sub(' ', text).split('\n'):
        ln = re.sub(r'\s+', ' ', ln).strip()
        sents += [s.strip() for s in re.split(r'(?<=[.!?])\s+', ln) if s.strip()]
    for a in card.attrs:
        ai = a.info
        if ai is None:
            continue
        for kind, temps in ai.statements.items():
            for tp in temps:
                rx = re.escape(tp.rstrip('.'))
                rx = rx.replace(re.escape('{E}'), r'(?:[A-Z][\w\'’ -]{0,60}?|[Ii]t|[Tt]his|[Tt]he record)')
                rx = rx.replace(re.escape('{v}'), r'(?P<v>.+?)')
                for s in sents:
                    s2 = strip_chrome(s).rstrip('.')
                    m = re.fullmatch(rx, s2)
                    if m:
                        if kind == 'value':
                            out.setdefault(a.name, []).append(m.group('v'))
                        elif kind in ('pos', 'positive', 'true', 'yes'):
                            out.setdefault(a.name, []).append(True)
                        elif kind in ('neg', 'negative', 'false', 'no'):
                            out.setdefault(a.name, []).append(False)
                        elif kind == 'none':
                            out.setdefault(a.name, []).append('none')
    return out


def parse_record(card, text, need_all):
    found = {}
    if '<' in text and re.search(r'</\w+>', text):
        for k, v in kv_from_html(card, text).items():
            found.setdefault(k, v)
    if '{' in text:
        for k, v in kv_from_json(card, text).items():
            found.setdefault(k, v)
    if len(found) < len(card.attrs):
        for k, v in kv_from_table(card, text).items():
            found.setdefault(k, v)
    if len(found) < len(card.attrs):
        for k, v in kv_from_lines(card, text).items():
            found.setdefault(k, v)
    if len(found) < len(card.attrs):
        for k, v in kv_from_prose(card, text).items():
            found.setdefault(k, v)
    vals, omitted = {}, set()
    for a in card.attrs:
        if a.name not in found:
            omitted.add(a.name)
            continue
        cand = found[a.name]
        pv = None
        errs = []
        for c in cand:
            try:
                pv = parse_value(card, a, c)
                break
            except ParseError as e:
                errs.append(str(e))
        if pv is None:
            raise ParseError('value:' + ';'.join(errs)[:120])
        if pv == ('omit',):
            omitted.add(a.name)
        else:
            vals[a.name] = pv
    return vals, omitted


def case_box(card, sp, vals, omitted):
    b = {}
    for a in card.attrs:
        if a.name in vals:
            v = vals[a.name]
            if sp.is_int(a.name):
                b[a.name] = (v, v)
            else:
                b[a.name] = frozenset([v])
    for key in list(sp.axes):
        if key.startswith('rel|'):
            _, x, e = key.split('|')
            if x in vals and e in vals:
                d = vals[x] - vals[e]
                b[key] = (d, d)
    return b


# ----------------------------------------------------------------------------------------------- questions
NEG_RE = re.compile(r"\bnot\b|n't\b|\bnever\b|\bfalse that\b")


def question_sentences(instr):
    """candidate question sentences, last first."""
    out = []
    for raw in instr.split('\n'):
        l = strip_chrome(raw)
        if '?' not in l:
            continue
        parts = re.split(r'(?<=[.?!:])\s+', l)
        cur = ''
        for p in parts:
            cur = (cur + ' ' + p).strip() if cur and not cur.endswith(('?', '.', '!', ':')) else p
            if p.endswith('?'):
                out.append(p)
    return out[::-1]


def find_name(text, names):
    """the defined name mentioned in a question (longest exact match on token boundaries)."""
    best = None
    for n in sorted(names, key=len, reverse=True):
        if re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', text):
            best = n; break
    return best


def classify_q(q):
    ql = q.lower()
    kinds = []
    if re.search(r'\bdefines?\b|\bdefined\b', ql):
        kinds.append('defines')
    if re.search(r'\b(meets?|met|appl(?:y|ies)|match(?:es)?|fits?|satisf(?:y|ies)|qualif(?:y|ies))\b', ql):
        kinds.append('meets')
    if re.search(r'\b(assigns?|assigned|gets?|is given|given|receives?)\b', ql):
        kinds.append('assigned')
    if re.search(r'^(?:is|does) (?:it|the|this|that)?.*? an? ', ql) and not kinds:
        kinds.append('meets')
    return kinds


def neg_count(q, target):
    t = q.replace(target, ' ') if target else q
    return len(NEG_RE.findall(t.lower()))


# ----------------------------------------------------------------------------------------------- solving (programs)
def solve_program(row, dbg=False):
    smp = row['meta']['sampler']
    card = Card()
    text = (row.get('card') or '') + '\n' + row['instructions']
    lines = text.split('\n')
    legend_parse(lines, row['meta']['domain_pack'], card)
    if not card.attrs:
        raise ParseError('nolegend')
    read_rules(card, text)
    build_card(card, lines, smp)
    if smp == 'S3':
        parse_table(card, lines)
    if not card.defs:
        raise ParseError('nodefs')
    sp = make_space(card)
    comp = Compiler(card, sp)
    regions = collections.OrderedDict()
    for nm in card.defs:
        regions[nm] = comp.term(nm)
    names = list(card.defs)
    qtype = row['qtype']
    options = row.get('options') or []
    qs = question_sentences(row['instructions'])
    info = {'card': card, 'regions': regions}
    if smp == 'S6':
        return solve_s6(row, card, sp, comp, regions, qs, info)
    # inverted rows
    if qtype == 'choice' and options and all(o not in card.defs for o in options) and \
            any('exactly one of the records' in q.lower() or 'which record' in q.lower() for q in qs) or \
            (qtype == 'choice' and options and all(re.search(r'\b(?:case|record|item|file)\b', o, re.I) for o in options)
             and all(o not in card.defs for o in options)):
        return solve_inverted(row, card, sp, regions, qs, info)
    vals, omitted = parse_record(card, row['state'], True)
    info['omitted'] = sorted(omitted)
    if omitted and not card.open_world:
        card.problems.append('omitted_on_closed:' + ','.join(sorted(omitted)))
    box = case_box(card, sp, vals, omitted)
    # possible assigned answers in card order (meets regions; earlier regions subtracted)
    P = []
    earlier = []
    for nm in names:
        R = regions[nm]
        A = reg_minus(sp, R, earlier) if earlier else R
        if reg_and(sp, A, [box]):
            P.append(nm)
        earlier = earlier + R
    if reg_minus(sp, [box], earlier):
        P.append('__none__')
    info['P'] = P
    met = [nm for nm in names if reg_and(sp, regions[nm], [box]) and not reg_minus(sp, [box], regions[nm])]
    info['n_met'] = len(met)
    info['rel'] = any(k.startswith('rel|') for k in sp.axes)
    info['conv'] = bool(card.conv)
    info['tags'] = any(a.typ == 'tag' for a in card.attrs)
    info['helpers'] = bool(card.helpers)
    low = text.lower()
    info['first_listed'] = bool(re.search(r'listed first|first (?:listed|one listed|term listed|in card order)|card order|'
                                          r'earliest|comes first|first row|first matching', low))
    if qtype == 'noul':
        tgt, kind, neg = None, None, 0
        for q in qs:
            nm = find_name(q, names)
            ks = classify_q(q)
            if nm and ks:
                tgt, kind, neg = nm, ks[0], neg_count(q, nm)
                if 'assigned' in ks and kind != 'assigned':
                    kind = 'assigned' if re.search(r'\b(assigns?|assigned|gets?|given|receives?)\b', q.lower()) and \
                        not re.search(r'\b(meets?|appl(?:y|ies)|satisf(?:y|ies)|fits?|match(?:es)?|qualif(?:y|ies))\b', q.lower()) else kind
                info['q'] = q
                break
        if tgt is None:
            raise ParseError('noq')
        R = regions[tgt]
        if kind == 'assigned':
            idx = names.index(tgt)
            prev = []
            for nm in names[:idx]:
                prev = prev + regions[nm]
            R = reg_minus(sp, R, prev) if prev else R
        inside = not reg_minus(sp, [box], R)
        outside = not reg_and(sp, R, [box])
        if inside == outside:
            raise ParseError('undetermined_yesno')
        ans = inside
        if neg % 2 == 1:
            ans = not ans
        info.update(kind=kind, target=tgt, neg=neg)
        return (1 if ans else 0), info
    # choice
    shown_terms = [o for o in options if o in card.defs]
    abst = [o for o in options if o not in card.defs]
    none_opt = cbd_opt = None
    for o in abst:
        if o in card.none_text or re.search(r'\bnone\b|\bno term\b|\bno code\b|\bnot any\b|\bno defined\b|\bneither\b', o.lower()):
            none_opt = o
        else:
            cbd_opt = o
    info['abstain'] = (none_opt, cbd_opt)
    if len(P) == 1:
        g = P[0]
        gold = none_opt if g == '__none__' else g
        if gold is None or (g != '__none__' and g not in shown_terms):
            info['rule'] = 'determined_not_shown'
    else:
        gold = cbd_opt
        if not any(p in shown_terms for p in P):
            info['rule'] = 'xf15_no_shown_term'
        if cbd_opt is None:
            info['rule'] = 'undetermined_no_cbd'
    return gold, info


def solve_inverted(row, card, sp, regions, qs, info):
    names = list(card.defs)
    tgt = None
    tail = [strip_chrome(l) for l in row['instructions'].split('\n')]
    sents = [x for l in tail for x in re.split(r'(?<=[.?!])\s+', l) if re.search(r'exactly one|which record|records? below', x, re.I)]
    for q in sents[::-1] + qs:
        tgt = find_name(q, names)
        if tgt:
            break
    if tgt is None:
        raise ParseError('inv_noq')
    recs = split_records(row['state'], row['options'])
    R = regions[tgt]
    hits = []
    for o in row['options']:
        vals, om = parse_record(card, recs[o], True)
        if om:
            raise ParseError('inv_omitted:%s' % sorted(om))
        b = case_box(card, sp, vals, om)
        if reg_and(sp, R, [b]):
            hits.append(o)
    info['hits'] = hits
    info['target'] = tgt
    if len(hits) != 1:
        info['rule'] = 'inverted_hits_%d' % len(hits)
        return (hits[0] if hits else None), info
    return hits[0], info


def split_records(state, labels):
    if '{' in state:
        st = state.find('{')
        en = state.rfind('}')
        try:
            obj = json.loads(state[st:en + 1])
        except Exception:
            obj = None
        if obj is not None:
            found = {}

            def walk(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        for lab in labels:
                            if isinstance(k, str) and norm_key(k) == norm_key(lab) and isinstance(v, (dict, list)):
                                found[lab] = json.dumps(v)
                        walk(v)
                elif isinstance(o, list):
                    for x in o:
                        if isinstance(x, dict):
                            for kk, vv in x.items():
                                if isinstance(vv, str) and any(norm_key(vv) == norm_key(l) for l in labels):
                                    lab = [l for l in labels if norm_key(vv) == norm_key(l)][0]
                                    found[lab] = json.dumps(x)
                        walk(x)
            walk(obj)
            if len(found) == len(labels):
                return found
    pos = []
    for lab in labels:
        words = re.findall(r'[A-Za-z0-9]+', lab)
        rx = r'(?<![A-Za-z0-9])' + r'[\s_-]*'.join(re.escape(w) for w in words) + r'(?![A-Za-z0-9])'
        ms = [m for m in re.finditer(rx, state, re.I)]
        if not ms:
            raise ParseError('inv_label:' + lab)
        pos.append((ms[0].start(), lab, ms[0].end()))
    pos.sort()
    out = {}
    for i, (p, lab, pe) in enumerate(pos):
        e = pos[i + 1][0] if i + 1 < len(pos) else len(state)
        out[lab] = state[pe:e]
    return out


def solve_s6(row, card, sp, comp, regions, qs, info):
    st = row['state']
    flat = ' '.join(strip_chrome(l) for l in st.split('\n') if strip_chrome(l))
    # the description: the text after its frame, read with the same body grammar
    body = None
    for sent in split_sentences(flat):
        mm = re.search(r'(?:for which|in which|where|when|whenever|if|such that|whose|that)\s*(?:,\s*)?(.+)$', sent)
        cands = []
        m2 = re.search(r'\b(?:not all|all|any|none) of the following\b', sent)
        if m2:
            cands.append(sent[m2.start():])
        if mm:
            cands.append(mm.group(1))
        for c in cands:
            try:
                body = DefParser(card, set(card.defs) | set(w for w, _ in card.helpers)).body(c)
                break
            except ParseError:
                continue
        if body is not None:
            break
    if body is None:
        # an atom-led description: find the first attribute name and parse from there
        low = flat.lower()
        best = None
        for a in card.attrs:
            k = low.find(a.name + ' ')
            if k >= 0 and (best is None or k < best):
                best = k
        if best is not None:
            seg = flat[best:]
            seg = re.split(r'(?<=\.)\s', seg)[0]
            try:
                body = DefParser(card, set(card.defs)).body(seg)
            except ParseError as e:
                raise ParseError('s6desc:%s' % e)
    if body is None:
        raise ParseError('s6nodesc')
    D = comp.node(body, None, ())
    eq = []
    for nm, R in regions.items():
        if not reg_minus(sp, D, R) and not reg_minus(sp, R, D):
            eq.append(nm)
    info['equiv'] = eq
    if row['qtype'] == 'noul':
        tgt = None
        for q in qs:
            tgt = find_name(q, list(card.defs))
            if tgt:
                neg = neg_count(q, tgt); break
        if tgt is None:
            raise ParseError('s6noq')
        ans = tgt in eq
        if neg % 2:
            ans = not ans
        return (1 if ans else 0), info
    shown = [o for o in row['options'] if o in eq]
    if len(shown) != 1:
        info['rule'] = 's6_equiv_%d' % len(shown)
        return (shown[0] if shown else None), info
    return shown[0], info


# ----------------------------------------------------------------------------------------------- S3 tables
def parse_table(card, lines):
    """S3 code table: header 'code | attr ... | rule', one row per code, ALL-only rows (ST51)."""
    hdr = None
    for i, raw in enumerate(lines):
        l = TAG_RE.sub(' ', raw).rstrip()
        s = strip_chrome(l)
        for kind in ('pipe', 'tab', 'csv', 'ws'):
            cells = split_cells(s if kind != 'ws' else l.strip(), kind)
            if not cells or len(cells) < 3:
                continue
            if cells[0].strip().lower() not in ('code', 'codes', 'row', 'id', 'term', 'name') or cells[-1].strip().lower() not in ('rule', 'rules', 'rule column', 'extra rule'):
                continue
            ats = [match_attr(card, c, full=True) for c in cells[1:-1]]
            if any(a is None for a in ats):
                card.problems.append('table_header')
                continue
            hdr = (i, kind, cells, ats, l)
            break
        if hdr:
            break
    if hdr is None:
        return
    i0, kind, cells, ats, hraw = hdr
    names = set()
    rows = []
    for raw in lines[i0 + 1:]:
        l = TAG_RE.sub(' ', raw).rstrip()
        s = strip_chrome(l) if kind != 'ws' else l.strip()
        if not s.strip():
            if rows:
                break
            continue
        if re.fullmatch(r'[|+:\-= ]+', s.strip()):
            continue
        if kind == 'ws':
            vals = split_cells(s, 'ws')
            if len(vals) != len(cells):
                vals = fixed_cells(hraw, l, cells)
        else:
            vals = split_cells(s, kind)
        if vals is None or len(vals) != len(cells):
            if rows:
                break
            continue
        rows.append(vals)
    defs = collections.OrderedDict()
    dp = DefParser(card, set(r[0].strip() for r in rows))
    for vals in rows:
        code = vals[0].strip()
        items = []
        try:
            for a, c in zip(ats, vals[1:-1]):
                c = c.strip()
                if c.lower() in ('any', 'any value', '(any)'):
                    continue
                items.append(parse_atom(card, c, attr=a))
            d = Def(code, '')
            d.body = ('all', items) if items else ('all', [])
            rule = vals[-1].strip().rstrip('.')
            if rule.lower() not in ('no extra rule',):
                for part in re.split(r';\s*', rule):
                    pl = part.strip()
                    m = re.match(r'^only if\s+(.+)$', pl, re.I)
                    if m:
                        d.onlyif.append(parse_atom(card, m.group(1)))
                        continue
                    m = re.match(r'^exception:?\s+(.+)$', pl, re.I)
                    if m:
                        d.exc.append(parse_atom(card, m.group(1)))
                        continue
                    raise ParseError('rulecell:' + pl[:40])
            defs[code] = d
        except ParseError as e:
            card.problems.append('tablerow:%s:%s' % (code, e))
    if defs:
        card.defs = defs


# ----------------------------------------------------------------------------------------------- S7
_S7 = None


def s7_data():
    global _S7
    if _S7 is None:
        base = os.path.join(CSRC, 'formats', 'formats-2')
        recs = {}
        for fn in ('xed', 'mams_acsa', 'mams_atsa', 'ghc', 'edos'):
            p = os.path.join(base, 'records', fn + '.jsonl')
            for l in open(p):
                r = json.loads(l)
                recs.setdefault((r['scheme'], r['text']), []).append(r)
                recs.setdefault((r['scheme'], wnorm(r['text'])), []).append(r)
        lex = json.load(open(os.path.join(base, 'codebooks', 'lexicon.json')))
        _S7 = (recs, {lx['scheme']: lx for lx in lex['lexicons']})
    return _S7


def _ann(r):
    a = r['ann']
    if isinstance(a, str):
        import ast
        a = ast.literal_eval(a)
    return a


def s7_scheme(row, text):
    dp = row['meta']['domain_pack']
    if dp.startswith('xed'):
        return 'xed'
    if dp.startswith('ghc'):
        return 'ghc'
    if dp.startswith('edos'):
        return 'edos'
    if 'atsa' in dp:
        return 'mams_atsa'
    if 'acsa' in dp:
        return 'mams_acsa'
    if re.search(r'asked target', text, re.I):
        return 'mams_atsa'
    return 'mams_acsa'


def s7_phrase_rx(lexs, scheme):
    lx = lexs[scheme]
    vals = [v['value'] for v in lx['values']]
    names = lx.get('names') or {}
    out = []
    for t in lx['templates']:
        tp = t['template']
        rx = re.escape(tp)
        slots = re.findall(r'\{(\w)\}', tp)
        for sl in set(slots):
            if sl == 'f':
                alts = sorted(set(list(names.values()) + list(names.keys())), key=len, reverse=True)
            else:
                alts = sorted(vals, key=len, reverse=True)
            grp = '(?P<%s>%s)' % (sl, '|'.join(re.escape(a) for a in alts))
            parts = rx.split(re.escape('{%s}' % sl))
            if len(parts) > 1:
                rx = parts[0] + grp + parts[1] + ''.join('(?P=%s)' % sl + p for p in parts[2:])
        out.append((re.compile('^' + rx + '$', re.I), t['form'], names))
    return out


def s7_parse_phrase(prx, s):
    s = s.strip().rstrip('.').strip()
    for rx, form, names in prx:
        m = rx.match(s)
        if m:
            g = m.groupdict()
            if 'f' in g and g['f'] is not None:
                inv = {v.lower(): k for k, v in names.items()}
                g['f'] = inv.get(g['f'].lower(), g['f'].lower())
            return (form, {k: (v.lower() if isinstance(v, str) else v) for k, v in g.items()})
    raise ParseError('s7phrase:' + s[:60])


def s7_eval(scheme, atom, ann, ctx):
    form, g = atom
    pos = not form.endswith('-') and '-' not in form.split('+')[0][-1:] and not form.endswith('-neutral')
    base = form.replace('+', '').replace('-', '')
    neg = '-' in form
    if scheme == 'xed':
        emos = [e.lower() for e in ann.get('emotions', [])]
        if base == 'EMOneutral':
            val = (len(emos) == 0 or emos == ['neutral'])
        else:
            val = g['v'] in emos
    elif scheme == 'mams_acsa':
        pairs = [(c.lower(), p.lower()) for c, p in ann['aspects']]
        if base == 'PAIR':
            val = (g['c'], g['p']) in pairs
        elif base == 'CAT':
            val = any(c == g['c'] for c, _ in pairs)
        elif base == 'POL':
            val = any(p == g['p'] for _, p in pairs)
        else:
            raise ParseError('acsaform')
    elif scheme == 'mams_atsa':
        tp, others = ctx
        if base == 'TPOL':
            val = tp == g['p']
        elif base == 'OTHER':
            val = g['p'] in others
        else:
            raise ParseError('atsaform')
    elif scheme == 'ghc':
        val = int(ann.get(g['f'], 0)) == 1
    elif scheme == 'edos':
        if base == 'SEXIST':
            val = ann['label_sexist'] == 'sexist'
        elif base == 'CAT':
            val = str(ann['label_category']).lower().startswith(g['c'] + '.') or str(ann['label_category']).lower() == g['c']
        elif base == 'VEC':
            val = str(ann['label_vector']).lower().startswith(g['v'] + ' ') or str(ann['label_vector']).lower() == g['v']
        else:
            raise ParseError('edosform')
    else:
        raise ParseError('scheme')
    return (not val) if neg else val


CODE_FORMS = [('«', '»'), ('"', '"'), ("'", "'"), ('[', ']'), ('“', '”'), ('‘', '’'), ('<', '>'), ('⟨', '⟩')]


def solve_s7(row, dbg=False):
    recs, lexs = s7_data()
    text = (row.get('card') or '') + '\n' + row['instructions']
    scheme = s7_scheme(row, text)
    prx = s7_phrase_rx(lexs, scheme)
    codes = collections.OrderedDict()
    residual = None
    for raw in text.split('\n'):
        s = strip_chrome(raw)
        for lq, rq in CODE_FORMS:
            if not s.startswith(lq):
                continue
            k = s.find(rq + ':', 1)
            if k < 0:
                continue
            name = s[:k + 1]
            body = s[k + 2:].strip()
            if name in codes or name == residual:
                break
            sents = split_sentences(body)
            b0 = sents[0].rstrip('.') if sents else ''
            if re.search(r'\bcodes?\b', b0, re.I) and re.search(r'\b(other|remaining|earlier|above|before|preceding|previous|rest)\b', b0, re.I) \
                    and re.search(r'\b(none|no|not|fails?|neither)\b', b0, re.I) and not LIST_HEAD.match(b0):
                residual = name
                break
            m = LIST_HEAD.match(b0)
            try:
                if m:
                    head = m.group(1).lower()
                    if head not in ('all', 'any'):
                        raise ParseError('s7head:' + head)
                    items = [s7_parse_phrase(prx, x) for x in re.split(r';\s+', m.group(2)) if x.strip()]
                    codes[name] = (head, items)
                else:
                    codes[name] = ('all', [s7_parse_phrase(prx, b0)])
            except ParseError as e:
                raise ParseError('s7code:%s:%s' % (name, e))
            break
    if not codes:
        raise ParseError('s7nocodes')
    st = row['state']
    cand = recs.get((scheme, st)) or recs.get((scheme, wnorm(st)))
    if not cand:
        raise ParseError('s7norecord')
    anns = set(json.dumps(_ann(r), sort_keys=True) for r in cand)
    if len(anns) != 1:
        raise ParseError('s7multiann')
    ann = _ann(cand[0])
    ctx = None
    qs = question_sentences(row['instructions'])
    if scheme == 'mams_atsa':
        full = ' '.join(strip_chrome(l) for l in row['instructions'].split('\n'))
        terms = ann['terms']
        T = None
        for t in sorted(terms, key=lambda t: len(t['term']), reverse=True):
            if re.search(r'asked target(?: is| was|:|,| =)?\s*["\'“«]?' + re.escape(t['term']) + r'(?![\w-])', full, re.I):
                T = t['term']; break
        if T is None:
            raise ParseError('atsa_frame')
        tp = [t['polarity'].lower() for t in terms if t['term'] == T]
        if len(tp) != 1:
            raise ParseError('atsa_T')
        others = [t['polarity'].lower() for t in terms if t['term'] != T]
        ctx = (tp[0], set(others))
    fits = collections.OrderedDict()
    for name, (head, items) in codes.items():
        vs = [s7_eval(scheme, it, ann, ctx) for it in items]
        fits[name] = all(vs) if head == 'all' else any(vs)
    first = next((n for n, f in fits.items() if f), residual)
    info = {'fits': [n for n, f in fits.items() if f], 'first': first}
    if row['qtype'] == 'noul':
        tgt = None
        for q in qs:
            for name in sorted(codes, key=len, reverse=True):
                if name in q:
                    tgt = name; break
            if tgt:
                neg = neg_count(q, tgt); break
        if tgt is None:
            raise ParseError('s7noq')
        ans = fits[tgt]
        if neg % 2:
            ans = not ans
        return (1 if ans else 0), info
    opts = row['options']
    if first in opts:
        return first, info
    # option texts may drop the quote marks
    for o in opts:
        if first is not None and o.strip('«»"\'[]“”‘’<>⟨⟩') == first.strip('«»"\'[]“”‘’<>⟨⟩'):
            return o, info
    info['rule'] = 's7_first_not_shown'
    return first, info


# ----------------------------------------------------------------------------------------------- main
def solve_row(row, dbg=False):
    if row['meta']['sampler'] == 'S7':
        return solve_s7(row, dbg)
    return solve_program(row, dbg)


def main():
    args = sys.argv[1:]
    out_dir = OUT
    files = ['candidates_r1', 'qc_sample', 'mixdev_S5']
    limit = None
    debug = None
    if '--only' in args:
        files = [args[args.index('--only') + 1]]
    if '--limit' in args:
        limit = int(args[args.index('--limit') + 1])
    if '--debug' in args:
        debug = args[args.index('--debug') + 1]
    report = {'solver': 'F10 solver B (region algebra on the parsed row text; written from G0 F10-G0-v7 only)',
              'files': {}, 'mismatches': [], 'parse_failures': [], 'rule_flags': []}
    tot = 0
    cov = collections.Counter()
    for f in files:
        n = mm = pf = 0
        fails = collections.Counter()
        for k, l in enumerate(open(os.path.join(out_dir, f + '.jsonl'))):
            if limit and k >= limit:
                break
            row = json.loads(l)
            if debug and row['id'] != debug:
                continue
            n += 1
            try:
                g, info = solve_row(row)
            except ParseError as e:
                pf += 1
                key = str(e).split(':')[0]
                fails[(row['meta']['sampler'], key)] += 1
                report['parse_failures'].append({'file': f, 'id': row['id'], 'sampler': row['meta']['sampler'],
                                                 'error': str(e)[:160]})
                if debug:
                    raise
                continue
            except Exception as e:  # noqa
                pf += 1
                fails[(row['meta']['sampler'], 'EXC:' + type(e).__name__)] += 1
                report['parse_failures'].append({'file': f, 'id': row['id'], 'sampler': row['meta']['sampler'],
                                                 'error': ('EXC %s: %s' % (type(e).__name__, e))[:160]})
                if debug:
                    raise
                continue
            if debug:
                c = info.get('card')
                print('GOLD', row['gold'], 'B', g, {k: v for k, v in info.items() if k not in ('card', 'regions')})
                if c is not None:
                    print('ATTRS', [(a.name, a.typ, a.dec, a.values[:4]) for a in c.attrs])
                    print('DEFS', list(c.defs), 'HELP', list(c.helpers), 'OPEN', c.open_world, 'PROB', c.problems[:6])
            if info.get('rule'):
                report['rule_flags'].append({'file': f, 'id': row['id'], 'flag': info['rule']})
            smp = row['meta']['sampler']
            cov[(smp, 'rows')] += 1
            cov[(smp, row['qtype'])] += 1
            if 'P' in info:
                P = info['P']
                cov[(smp, 'open_world')] += bool(info.get('omitted'))
                cov[(smp, 'omitted_2')] += len(info.get('omitted') or []) == 2
                cov[(smp, 'P_ge2_cbd')] += len(P) >= 2
                cov[(smp, 'P_none')] += P == ['__none__']
                cov[(smp, 'met_ge2')] += info.get('n_met', 0) >= 2
                cov[(smp, 'firstlisted_met_ge2')] += info.get('n_met', 0) >= 2 and info.get('first_listed', False)
                cov[(smp, 'relative_date_card')] += info.get('rel', False)
                cov[(smp, 'conversion_card')] += info.get('conv', False)
                cov[(smp, 'tag_card')] += info.get('tags', False)
                cov[(smp, 'helper_card')] += info.get('helpers', False)
                if info.get('n_met', 0) >= 2 and not info.get('first_listed', False) and smp != 'S3':
                    report['rule_flags'].append({'file': f, 'id': row['id'], 'flag': 'met_ge2_without_first_listed_rule'})
                if info.get('kind'):
                    cov[(smp, 'yesno_' + info['kind'])] += 1
                    cov[(smp, 'yesno_negated')] += info.get('neg', 0) % 2 == 1
                    cov[(smp, 'yesno_double_neg')] += info.get('neg', 0) >= 2
            if 'hits' in info:
                cov[(smp, 'inverted')] += 1
            if 'equiv' in info:
                cov[(smp, 'S6_rows')] += 1
            if 'fits' in info:
                cov[(smp, 'S7_residual_gold')] += info.get('first') is not None and info.get('first') == g and len(info['fits']) == 0
            if g != row['gold']:
                mm += 1
                c = info.get('card')
                report['mismatches'].append({
                    'file': f, 'id': row['id'], 'sampler': row['meta']['sampler'], 'qtype': row['qtype'],
                    'gold_A': row['gold'], 'gold_B': g,
                    'spec_item': spec_item(row, info),
                    'card_problems': (c.problems[:4] if c is not None else [])})
        report['files'][f] = {'rows': n, 'mismatches': mm, 'parse_failures': pf,
                              'failure_kinds': {'%s/%s' % k: v for k, v in fails.most_common(30)}}
        tot += n
        print(f, report['files'][f]['rows'], 'mm', mm, 'pf', pf, dict(fails.most_common(12)), flush=True)
    report['rows_checked'] = tot
    report['coverage'] = {'%s/%s' % k: v for k, v in sorted(cov.items())}
    report['n_mismatches'] = len(report['mismatches'])
    report['n_parse_failures'] = len(report['parse_failures'])
    report['n_rule_flags'] = len(report['rule_flags'])
    import hashlib
    report['inputs_sha256'] = {f + '.jsonl': hashlib.sha256(open(os.path.join(out_dir, f + '.jsonl'), 'rb').read()).hexdigest()
                               for f in files}
    report['solver_sha256'] = hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
    report['written_utc'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    if not debug:
        dst = os.path.join(HERE, 'mismatch.json' if not limit and '--only' not in args else 'mismatch_partial.json')
        json.dump(report, open(dst, 'w'), indent=1)
        print('wrote', dst)


def spec_item(row, info):
    smp = row['meta']['sampler']
    if smp == 'S7':
        return 'section 3 S7 / section 4 S7 (first fit on the parsed codebook; ST44, ST45)'
    if smp == 'S6':
        return 'section 4 S6 / ST43 (grid equivalence)'
    if row['qtype'] == 'noul':
        return 'section 4 yes/no (%s kind, ST41 negation; ST3, ST28, ST49)' % info.get('kind')
    if 'hits' in info:
        return 'ST42 inverted'
    P = info.get('P') or []
    if len(P) >= 2:
        return 'section 4 choice gold, |P|>=2 -> cannot be determined (ST5, XF15, R3-01, R5-04)'
    if P == ['__none__']:
        return 'section 4 choice gold, P={none} (ST29)'
    return 'section 4 choice gold, P={T} (ST28 card order / ST27)'


if __name__ == '__main__':
    main()
