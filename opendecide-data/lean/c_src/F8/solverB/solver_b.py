#!/usr/bin/env python3
"""F8 solver B (G2), written from c_src/F8/G0_SPEC.md (draft 7, frozen) and C_DATA_SPEC 2.4 / 6 only.

It never imports or reads generator, renderer or solver A code (c_src/F8/gen/ is never opened).
Input: the rendered row fields only (card, instructions, state, options). It parses them back into facts
(G3-style parse, written from spec sections 2, 5 and 7) and re-derives the gold in other paradigms (spec 4):
  bayes / PRED     integer population counting (lcm of all denominators; cross-multiplied comparisons)
  expected / DEC   integer ledger (common denominator; integer totals; ties by parsed ID number)
  points / matrix  relational evaluation in an in-memory sqlite3 database, one SQL stage per SEM-15 step
  rank             pairwise tournament with integer cross-multiplication
  open world       witness / counter-witness search: a witness answer a1, then an exact search for an allowed
                   point whose answer differs (z3 is not installed in the project venv; the search is an exact
                   rational optimisation of each multilinear comparison over the closed box, plus full
                   enumeration of Boolean unknowns).
No floats anywhere: every number is an int or fractions.Fraction.
Rows are compared with the row's gold (solver A's label), abstain decision and PRED gold_probs.
"""
import json, re, sys, sqlite3, hashlib, itertools, math, os
from fractions import Fraction as F

ID_RE = r'[A-Z][A-Z0-9]{0,6}-\d+'
CBD_TXT = 'Cannot be determined from the information given'
NOTA_TXT = 'None of these'


class ParseError(Exception):
    pass


# ---------------------------------------------------------------- numbers (spec 5 number grammar)
def _dec(s):
    s = s.replace(',', '')
    neg = s.startswith('-')
    if neg:
        s = s[1:]
    if '.' in s:
        a, b = s.split('.')
        v = F(int(a or '0') * 10 ** len(b) + int(b), 10 ** len(b))
    else:
        v = F(int(s))
    return -v if neg else v


NUM_TOKEN = r'-?\d[\d,]*(?:\.\d+)?'


def parse_chance(s):
    """Percent (<=1 decimal), decimal, fraction, '<a> in <b>', '<a> out of <b>'. Returns Fraction."""
    t = s.strip().strip('"').strip()
    m = re.fullmatch(r'(' + NUM_TOKEN + r')\s*%', t)
    if m:
        return _dec(m.group(1)) / 100
    m = re.fullmatch(r'(\d[\d,]*)\s*/\s*(\d[\d,]*)', t)
    if m:
        return F(int(m.group(1).replace(',', '')), int(m.group(2).replace(',', '')))
    m = re.fullmatch(r'(\d[\d,]*)\s+(?:in|out of)\s+(\d[\d,]*)', t)
    if m:
        return F(int(m.group(1).replace(',', '')), int(m.group(2).replace(',', '')))
    m = re.fullmatch(NUM_TOKEN, t)
    if m:
        return _dec(t)
    raise ParseError('chance? ' + s[:40])


def parse_amount(s):
    """Amount with optional unit words after it; 'None' or '0' = 0 (SEM-03). Returns Fraction."""
    t = s.strip().strip('"').strip()
    if re.fullmatch(r'none', t, re.I):
        return F(0)
    m = re.match(r'(' + NUM_TOKEN + r')(?:\s+[A-Za-z][A-Za-z \-]*)?$', t)
    if not m:
        raise ParseError('amount? ' + s[:40])
    return _dec(m.group(1))


def parse_count(s):
    t = s.strip().strip('"').strip()
    if not re.fullmatch(r'\d[\d,]*', t):
        raise ParseError('count? ' + s[:40])
    return int(t.replace(',', ''))


def is_nr(s):
    return s is not None and s.strip().strip('"').strip().lower() == 'not recorded'


def normkey(s):
    """Key / factor-name canonical form: camelCase split, lower case, non-alphanumerics to one space."""
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s.strip())
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return s.strip()


def id_num(x):
    m = re.search(r'-(\d+)$', x)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- comparators (SEM-06)
COMP_WORDS = [
    ('no fewer than', '>='), ('no less than', '>='), ('no more than', '<='), ('at least', '>='),
    ('at most', '<='), ('more than', '>'), ('less than', '<'), ('exceeds', '>'), ('above', '>'),
    ('below', '<'), ('under', '<'), ('over', '>'),
]
COMP_RE = '(' + '|'.join(re.escape(w) for w, _ in COMP_WORDS) + ')'
COMP_OP = dict(COMP_WORDS)


def cmp_frac(a, op, b):
    """Integer cross-multiplication comparison of two Fractions (denominators are positive)."""
    l = a.numerator * b.denominator
    r = b.numerator * a.denominator
    if op == '>=':
        return l >= r
    if op == '<=':
        return l <= r
    if op == '>':
        return l > r
    if op == '<':
        return l < r
    if op == '=':
        return l == r
    raise ValueError(op)


# ---------------------------------------------------------------- container flattening (C_DATA_SPEC 6 containers)
# Output items: ('sent', text) | ('kv', key, value) | ('row', {col: value}) | ('rec', {key: value})
import html as _html


def strip_fences(text):
    return '\n'.join(l for l in text.split('\n') if not re.match(r'^\s*```', l))


def _cell(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', _html.unescape(s)).strip()


def html_to_text(text):
    def tr(m):
        cells = re.findall(r'<(t[hd])[^>]*>(.*?)</t[hd]>', m.group(0), re.S)
        if len(cells) == 2 and cells[0][0] == 'th' and cells[1][0] == 'td':
            return '\n' + _cell(cells[0][1]) + ': ' + _cell(cells[1][1]) + '\n'
        return '\n|' + '|'.join(_cell(c) for _, c in cells) + '|\n'
    t = re.sub(r'<tr[^>]*>.*?</tr>', tr, text, flags=re.S)
    t = re.sub(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>',
               lambda m: '\n' + _cell(m.group(1)) + ': ' + _cell(m.group(2)) + '\n', t, flags=re.S)
    t = re.sub(r'</?(?:li|p|div|h\d|ul|ol|section|article|header|footer|br|table|thead|tbody|dl|dt|dd|'
               r'blockquote|pre|tr|main|aside|span class="[^"]*")[^>]*>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    return _html.unescape(t)


def _walk(obj, out):
    if isinstance(obj, dict):
        scal = {}
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                continue
            scal[str(k)] = '' if v is None else str(v)
        if scal:
            out.append(('rec', scal))
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                _walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                _walk(v, out)
            elif v is not None:
                out.append(('sent', str(v)))
    elif obj is not None:
        out.append(('sent', str(obj)))


SEP_LINE = re.compile(r'^\s*\|?\s*[-=:|+ ]{3,}\s*$')
HEADER_FIRST = {'reference', 'class', 'tier', 'likelihood level', 'impact level', 'case', 'action', 'id'}


def _split_cells(line, delim):
    s = line.strip()
    if delim == '|':
        s = s.strip('|')
        return [c.strip() for c in s.split('|')]
    if delim == ';':
        return [c.strip() for c in s.split(';')]
    if delim == '\t':
        return [c.strip() for c in s.split('\t')]
    if delim == ',':
        import csv
        return [c.strip() for c in next(csv.reader([s]))]
    return [c.strip() for c in re.split(r'\s{2,}', s)]


def _header_delim(line):
    s = line.strip()
    for d in ('|', ';', '\t', ','):
        if d in s:
            cells = _split_cells(s, d)
            if len(cells) >= 2 and normkey(cells[0]) in HEADER_FIRST and all(cells):
                return d, cells
    cells = _split_cells(s, 'ws')
    if len(cells) >= 2 and normkey(cells[0]) in HEADER_FIRST:
        return 'ws', cells
    return None, None


KV_RE = re.compile(r'^(?P<k>[A-Za-z][A-Za-z0-9 _\'\-/()&]{0,60}?)\s*(?::|=|\s\.{2,}|\.{2,})\s*'
                   r'(?P<v>.*?)\s*$')


def _line_items(text, out, rules=False):
    lines = [re.sub(r'^\s*(?:>\s?)+', '', l) for l in text.split('\n')]
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue
        d, hdr = _header_delim(s)
        if d:
            j = i + 1
            rows = []
            while j < n:
                t = lines[j].strip()
                if not t:
                    if d == '|':
                        k2 = j
                        while k2 < n and not lines[k2].strip():
                            k2 += 1
                        if k2 < n and lines[k2].strip().startswith('|'):
                            j = k2
                            continue
                    break
                if SEP_LINE.match(t):
                    j += 1
                    continue
                cells = _split_cells(t, d)
                if len(cells) != len(hdr):
                    if d == 'ws':
                        break
                    break
                rows.append(dict(zip(hdr, cells)))
                j += 1
            if rows:
                for r in rows:
                    out.append(('row', r))
                i = j
                continue
        # YAML / python-ish flow mapping "- {a: b, c: "d"}"
        m = re.match(r'^(?:[-*+•]\s*)?\{(.*)\}\s*,?$', s)
        if m and ':' in m.group(1):
            rec = {}
            for part in re.findall(r'([^,{}:]+?):\s*("[^"]*"|\'[^\']*\'|[^,{}]*)\s*(?:,|$)', m.group(1)):
                rec[part[0].strip().strip('"\'')] = part[1].strip().strip('"\'')
            out.append(('rec', rec))
            i += 1
            continue
        # strip list bullets / numbering / quote marks
        body = re.sub(r'^(?:>\s*)+', '', s)
        body = re.sub(r'^(?:[-*+•·§]\s+|\d+(?:\.\d+)*[.)]\s+|\(\d+\)\s+|Step \d+:\s+|§\s*\d+\s+)', '', body)
        if rules:
            body = re.sub(r"^\d+(?:\.\d+)*\s+(?=[A-Z'])", '', body)
        body = body.strip().strip(',').strip()
        if body.startswith('"') and body.endswith('"') and len(body) > 1:
            body = body[1:-1]
        if not body:
            i += 1
            continue
        if _looks_fact_sentence(body):
            out.append(('sent', body))
        else:
            m = KV_RE.match(body)
            if m and not re.search(r'[.?!]$', m.group('v') or '') or (m and re.fullmatch(r'\[?\s*' + ID_RE + r'\s*\]?', (m.group('v') or ''))):
                v = m.group('v').strip()
                v = re.sub(r'^\[\s*(.*?)\s*\]$', r'\1', v).strip().strip('"\'')
                out.append(('kv', m.group('k').strip(), v))
            else:
                out.append(('sent', body))
        i += 1


def _looks_fact_sentence(body):
    return bool(re.search(ID_RE + r"[ ,]|'[^']+'|\b(?:classed|show|shows)\b", body)) and \
        bool(re.search(r'[.?!]\s*$', body)) and not re.match(r'^[A-Za-z _]{1,40}:\s', body)


def _yaml_ok(obj, text):
    """Accept a YAML reading only when every key and scalar sits inside one source line."""
    lines = text.split('\n')
    leaves = []
    bad = []

    def rec(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if not re.fullmatch(r'[A-Za-z0-9_ \-]{1,50}', str(k)):
                    bad.append(k)
                leaves.append(str(k))
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
        elif o is not None:
            leaves.append(str(o))
    rec(obj)
    if bad:
        return False
    for lf in leaves:
        if lf and not any(lf in l for l in lines):
            return False
    return True


def _dup_top_keys(t):
    import textwrap
    keys = []
    for l in t.split('\n'):
        m = re.match(r'^(\s*)([A-Za-z_][^:]*):', l)
        if m and not l.strip().startswith('#'):
            keys.append((len(m.group(1)), m.group(2).strip()))
    if not keys:
        return False
    mi = min(k[0] for k in keys)
    top = [k for i, k in keys if i == mi]
    return len(top) != len(set(top))


def flatten(text):
    """State / document text -> list of items."""
    if not text:
        return []
    t = strip_fences(text)
    st = t.strip()
    out = []
    if st[:1] in '{[':
        try:
            obj = json.loads(st, parse_float=str, parse_int=str)
            _walk(obj, out)
            return out
        except Exception:
            pass
    if re.search(r'<(?:li|tr|td|th|h\d|p|div|ul|dl|section|article)\b', t):
        t = html_to_text(t)
        st = t.strip()
    first = next((l for l in st.split('\n') if l.strip() and not l.strip().startswith('#')), '')
    if re.match(r'^\s*[A-Za-z_][\w \-]*:(\s|$)', first) and '|' not in first and not _dup_top_keys(t):
        try:
            import yaml
            import textwrap
            obj = yaml.load(textwrap.dedent(t).strip('\n'), Loader=yaml.BaseLoader)
            if isinstance(obj, (dict, list)) and _yaml_ok(obj, t):
                _walk(obj, out)
                return out
        except Exception:
            pass
    _line_items(t, out)
    return out


def split_sentences(s):
    """Split a text item into sentences (never inside quotes or numbers)."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z0-9\[(<'\"])", s.strip())
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------- document model (section 2 fields)
CH = r"(?:\d[\d,]*(?:\.\d+)?\s*%|\d[\d,]*\s*/\s*\d[\d,]*|\d[\d,]*\s+(?:in|out of)\s+\d[\d,]*|\d[\d,]*(?:\.\d+)?)"
AMT = r"(?:-?\d[\d,]*(?:\.\d+)?(?:\s+[A-Za-z][A-Za-z \-]*?)?|None)"
Q = r"'([^']+)'"


class Outcome:
    __slots__ = ('p', 'p_nr', 'p_rng', 'a', 'a_nr', 'a_rng', 'kind')

    def __init__(self):
        self.p = None; self.p_nr = False; self.p_rng = None
        self.a = None; self.a_nr = False; self.a_rng = None
        self.kind = None


class Ent:
    def __init__(self, eid):
        self.id = eid
        self.facts = {}          # normkey -> ('bool', True|False) | ('str', raw) | ('nr',)
        self.rng = {}            # normkey -> (lo_raw, hi_raw)
        self.outcomes = {}       # event -> Outcome (insertion order kept)
        self.own = None          # raw string | 'NR'
        self.own_rng = None
        self.name = None         # action name
        self.nev = None          # (n, chance) for SEM-24
        self.order = 0


class Doc:
    def __init__(self):
        self.ents = {}
        self.base = {}           # H -> chance
        self.cond = {}           # (H, E) -> chance | 'NR'
        self.cond_rng = {}       # (H, E) -> (lo, hi)
        self.cnt = {}            # (H, E) -> (n_show, n_not)
        self.cnt_e = {}          # (E, shows) -> {H: n}, total
        self.cnt_e_tot = {}
        self.joint = {}          # (H, E) -> share of all
        self.tbl_sign = None
        self.tbl_rows = []       # [(H, n_show, n_not)]
        self.hyp_order = []
        self.unparsed = []
        self.inert = 0

    def ent(self, eid):
        if eid not in self.ents:
            e = Ent(eid)
            e.order = len(self.ents)
            self.ents[eid] = e
        return self.ents[eid]

    def hyp(self, h):
        if h not in self.hyp_order:
            self.hyp_order.append(h)


PREF = r"(?:The [^']*? )?"
S_PATTERNS = [
    ('bool1', rf"^{PREF}(?P<id>{ID_RE}) shows {Q}\.?$"),
    ('bool0', rf"^{PREF}(?P<id>{ID_RE}) does not show {Q}\.?$"),
    ('boolnr', rf"^Whether (?P<id>{ID_RE}) shows {Q} was not recorded\.?$"),
    ('action', rf"^Action (?P<id>{ID_RE}) is {Q}\.?$"),
    ('own1', rf"^(?P<id>{ID_RE}) has an own cost of (?P<v>{AMT})\.?$"),
    ('own_nr1', rf"^The own cost of (?P<id>{ID_RE}) was not recorded\.?$"),
    ('own_rng', rf"^The own cost of (?P<id>{ID_RE}) is at least (?P<lo>{AMT}) and at most (?P<hi>{AMT})\.?$"),
    ('own2', rf"^The own cost of (?P<id>{ID_RE}) is (?P<v>{AMT})\.?$"),
    ('attr_rng', rf"^The (?P<a>[^']+?) of (?P<id>{ID_RE}) is at least (?P<lo>{AMT}) and at most (?P<hi>{AMT})\.?$"),
    ('attr_cat', rf"^The (?P<a>[^']+?) of (?P<id>{ID_RE}) is {Q}\.?$"),
    ('attr_num', rf"^The (?P<a>[^']+?) of (?P<id>{ID_RE}) is (?P<v>{AMT})\.?$"),
    ('attr_nr', rf"^The (?P<a>[^']+?) of (?P<id>{ID_RE}) was not recorded\.?$"),
    ('o_pa', rf"^For (?P<id>{ID_RE}), the chance of {Q} is (?P<p>{CH}),? with an? (?P<k>loss|net amount) of (?P<a>{AMT})\.?$"),
    ('o_pa2', rf"^For (?P<id>{ID_RE}), {Q} has a chance of (?P<p>{CH}) and would (?P<k>cost) (?P<a>{AMT})\.?$"),
    ('o_rng', rf"^For (?P<id>{ID_RE}), the chance of {Q} is at least (?P<lo>{CH}) and at most (?P<hi>{CH})\.?$"),
    ('o_p', rf"^For (?P<id>{ID_RE}), the chance of {Q} is (?P<p>{CH})\.?$"),
    ('o_arng', rf"^For (?P<id>{ID_RE}), the (?P<k>loss|net amount) if '(?P<ev>[^']+)' happens is at least (?P<lo>{AMT}) and at most (?P<hi>{AMT})\.?$"),
    ('o_a', rf"^For (?P<id>{ID_RE}), the (?P<k>loss|net amount) if '(?P<ev>[^']+)' happens is (?P<a>{AMT})\.?$"),
    ('o_pnr_a', rf"^For (?P<id>{ID_RE}), the chance of {Q} was not recorded; the (?P<k>loss|net amount) if it happens is (?P<a>{AMT})\.?$"),
    ('o_p_anr', rf"^For (?P<id>{ID_RE}), the chance of {Q} is (?P<p>{CH}); the (?P<k>loss|net amount) if it happens was not recorded\.?$"),
    ('o_pnr', rf"^For (?P<id>{ID_RE}), the chance of {Q} was not recorded\.?$"),
    ('o_anr', rf"^For (?P<id>{ID_RE}), the (?P<k>loss|net amount) if '(?P<ev>[^']+)' happens was not recorded\.?$"),
    ('nev', rf"^(?P<id>{ID_RE}) has (?P<n>\d[\d,]*) (?P<things>[^;']+?); for each one, the chance of {Q} is (?P<p>{CH})\.?$"),
    ('base', rf"^(?:Over past years, )?(?P<p>{CH}) of (?P<pop>[^']+?) (?:are|have been) classed {Q}\.?$"),
    ('joint', rf"^(?P<p>{CH}) of all (?P<pop>[^']+?) are classed {Q} and show {Q}\.?$"),
    ('cnt', rf"^(?:Of|Among) past (?P<pop>[^']+?) classed {Q}, (?P<n1>\d[\d,]*) show {Q} and (?P<n0>\d[\d,]*) do not\.?$"),
    ('cnt_e', rf"^Of the (?P<tot>\d[\d,]*) past (?P<pop>[^']+?) that (?P<neg>do not )?show {Q}, (?P<n>\d[\d,]*) (?:are|is) classed {Q}\.?$"),
    ('cond_nr', rf"^(?:Among|Of the) (?P<pop>[^']+?) classed {Q}, the share that show {Q} was not recorded\.?$"),
    ('cond_rng', rf"^(?:Among|Of the) (?P<pop>[^']+?) classed {Q}, the share that show {Q} is at least (?P<lo>{CH}) and at most (?P<hi>{CH})\.?$"),
    ('cond', rf"^(?:Among|Of the) (?P<pop>[^']+?) classed {Q}, (?P<p>{CH}) show {Q}\.?$"),
    ('tbl', rf"^The table below counts past (?P<pop>[^']+?) by (?:class and by )?whether they show {Q}\.?$"),
]
S_PATTERNS = [(n, re.compile(p)) for n, p in S_PATTERNS]


def apply_sentence(doc, s):
    """Match one sentence against the fact grammar. Returns True when it is a fact."""
    for name, rx in S_PATTERNS:
        m = rx.match(s)
        if not m:
            continue
        g = m.groups()
        gd = m.groupdict()
        if name in ('bool1', 'bool0', 'boolnr'):
            e = doc.ent(gd['id'])
            e.facts[normkey(g[1])] = ('bool', name == 'bool1') if name != 'boolnr' else ('nr',)
        elif name == 'action':
            doc.ent(gd['id']).name = g[1]
        elif name in ('own1', 'own2'):
            doc.ent(gd['id']).own = gd['v']
        elif name == 'own_nr1':
            doc.ent(gd['id']).own = 'NR'
        elif name == 'own_rng':
            doc.ent(gd['id']).own_rng = (gd['lo'], gd['hi'])
        elif name in ('attr_cat', 'attr_num'):
            a = normkey(gd['a'])
            if a == 'own cost':
                doc.ent(gd['id']).own = gd['v'] if name == 'attr_num' else None
            else:
                doc.ent(gd['id']).facts[a] = ('str', g[2] if name == 'attr_cat' else gd['v'])
        elif name == 'attr_nr':
            a = normkey(gd['a'])
            if a == 'own cost':
                doc.ent(gd['id']).own = 'NR'
            else:
                doc.ent(gd['id']).facts[a] = ('nr',)
        elif name == 'attr_rng':
            a = normkey(gd['a'])
            if a == 'own cost':
                doc.ent(gd['id']).own_rng = (gd['lo'], gd['hi'])
            else:
                doc.ent(gd['id']).rng[a] = (gd['lo'], gd['hi'])
        elif name.startswith('o_'):
            e = doc.ent(gd['id'])
            ev = gd.get('ev') or g[1]
            o = e.outcomes.setdefault(ev, Outcome())
            if gd.get('k'):
                o.kind = 'net' if gd['k'] == 'net amount' else 'loss'
            if name in ('o_pa', 'o_pa2'):
                o.p = parse_chance(gd['p']); o.a = parse_amount(gd['a'])
            elif name == 'o_rng':
                o.p_rng = (parse_chance(gd['lo']), parse_chance(gd['hi']))
            elif name == 'o_p':
                o.p = parse_chance(gd['p'])
            elif name == 'o_arng':
                o.a_rng = (parse_amount(gd['lo']), parse_amount(gd['hi']))
            elif name == 'o_a':
                o.a = parse_amount(gd['a'])
            elif name == 'o_pnr_a':
                o.p_nr = True; o.a = parse_amount(gd['a'])
            elif name == 'o_p_anr':
                o.p = parse_chance(gd['p']); o.a_nr = True
            elif name == 'o_pnr':
                o.p_nr = True
            elif name == 'o_anr':
                o.a_nr = True
        elif name == 'nev':
            doc.ent(gd['id']).nev = (parse_count(gd['n']), parse_chance(gd['p']), g[3])
        elif name == 'base':
            h = g[2]; doc.hyp(h); doc.base[h] = parse_chance(gd['p'])
        elif name == 'joint':
            h, ev = g[2], g[3]; doc.hyp(h); doc.joint[(h, ev)] = parse_chance(gd['p'])
        elif name == 'cnt':
            h, ev = g[1], g[3]; doc.hyp(h)
            doc.cnt[(h, ev)] = (parse_count(gd['n1']), parse_count(gd['n0']))
        elif name == 'cnt_e':
            ev = g[3]; h = g[5]; doc.hyp(h)
            key = (ev, not gd['neg'])
            doc.cnt_e.setdefault(key, {})[h] = parse_count(gd['n'])
            doc.cnt_e_tot[key] = parse_count(gd['tot'])
        elif name == 'cond_nr':
            h, ev = g[1], g[2]; doc.hyp(h); doc.cond[(h, ev)] = 'NR'
        elif name == 'cond_rng':
            h, ev = g[1], g[2]; doc.hyp(h)
            doc.cond_rng[(h, ev)] = (parse_chance(gd['lo']), parse_chance(gd['hi']))
        elif name == 'cond':
            h, ev = g[1], g[3]; doc.hyp(h); doc.cond[(h, ev)] = parse_chance(gd['p'])
        elif name == 'tbl':
            doc.tbl_sign = g[1]
        return True
    return False


REF_KEYS = {'reference', 'ref', 'id', 'case', 'case id', 'reference number', 'ref no'}
STRUCT_KEYS = REF_KEYS | {'title', 'name', 'branch', 'from', 'to', 'subject', 'memo', 'form', 'event', 'chance',
                          'loss', 'net amount', 'amount', 'own cost', 'action', 'class', 'showed the sign',
                          'did not show the sign', 'cost', 'note', 'notes', 'outline', 'items', 'points',
                          'entries', 'rows', 'case details', 'reading rules', 'type', 'kind', 'date', 'sent',
                          'cc', 'heading', 'section', 'document'}


def _fact_val(v):
    t = v.strip().strip('"').strip()
    tl = t.lower()
    if tl == 'yes':
        return ('bool', True)
    if tl == 'no':
        return ('bool', False)
    if tl == 'not recorded':
        return ('nr',)
    return ('str', t)


def apply_record(doc, rec):
    k = {}
    for a, b in rec.items():
        k[normkey(a)] = b.strip() if isinstance(b, str) else str(b)
    if 'class' in k and 'showed the sign' in k and 'did not show the sign' in k:
        doc.hyp(k['class'])
        doc.tbl_rows.append((k['class'], parse_count(k['showed the sign']), parse_count(k['did not show the sign'])))
        return True
    ref = None
    for x in REF_KEYS:
        if x in k and re.fullmatch(ID_RE, k[x].strip('[] ')):
            ref = k[x].strip('[] ')
            break
    if not ref:
        for v in k.values():
            if isinstance(v, str) and re.search(ID_RE, v) and re.search(r'[.]$', v):
                for s in split_sentences(v):
                    apply_sentence(doc, s)
        return False
    e = doc.ent(ref)
    if 'action' in k and not re.fullmatch(ID_RE, k['action']):
        e.name = k['action'].strip("'")
    if 'own cost' in k:
        e.own = 'NR' if is_nr(k['own cost']) else k['own cost']
    if 'event' in k and 'chance' in k:
        o = e.outcomes.setdefault(k['event'].strip("'"), Outcome())
        if is_nr(k['chance']):
            o.p_nr = True
        else:
            o.p = parse_chance(k['chance'])
        for ak, kind in (('loss', 'loss'), ('net amount', 'net'), ('amount', None), ('cost', 'loss')):
            if ak in k:
                o.kind = kind or o.kind
                if is_nr(k[ak]):
                    o.a_nr = True
                else:
                    o.a = parse_amount(k[ak])
                break
    for key, v in k.items():
        if key in STRUCT_KEYS:
            continue
        e.facts[key] = _fact_val(v)
    return True


def build_doc(state):
    doc = Doc()
    items = flatten(state or '')
    cur = None
    recs = []
    for it in items:
        if it[0] == 'kv':
            kk = normkey(it[1])
            if kk in REF_KEYS:
                if cur:
                    recs.append(cur)
                cur = {it[1]: it[2]}
            elif cur is not None:
                cur[it[1]] = it[2]
            continue
        if it[0] in ('row', 'rec'):
            recs.append(it[1])
            continue
        if it[0] == 'sent':
            for s in split_sentences(it[1]):
                ok = False
                try:
                    ok = apply_sentence(doc, s)
                except ParseError as ex:
                    doc.unparsed.append('ERR ' + str(ex))
                    ok = True
                if not ok and re.search(r'[.?]$', s) and (re.search(ID_RE, s) or re.search(r"(?:classed|show|chance of|loss if) '", s)):
                    doc.unparsed.append(s)
                elif not ok:
                    doc.inert += 1
    if cur:
        recs.append(cur)
    for r in recs:
        apply_record(doc, r)
    return doc, items


# ---------------------------------------------------------------- card rules (sections 1, 2, 7)
class Rules:
    def __init__(self):
        self.lines = []          # (points, cond, unless_cond)
        self.floor = None
        self.cap = None
        self.tiers = []          # (name, rangetext) lowest -> highest
        self.only_if = {}        # tier -> cond
        self.overrides = []      # (cond, tier)
        self.actions = {}        # action -> cond
        self.inv = None          # cond
        self.risk = None         # ('loss',) | ('chance', E) | ('score',) | ('tec',) | ('value',)
        self.lik = []            # (name, rangetext)
        self.lik_event = None
        self.imp = []            # (name, rangetext)
        self.imp_kind = None
        self.grid = {}           # lik -> {imp: rating}
        self.rating_order = []
        self.net = False
        self.tie_lower = False
        self.indep = False
        self.dup_actions = []
        self.floorcap_sem14 = None


def parse_part(t):
    t = t.strip()
    m = re.fullmatch(r"it shows '([^']+)'", t)
    if m:
        return ('bool', normkey(m.group(1)))
    m = re.fullmatch(r"it requires '([^']+)'", t)
    if m:
        return ('req', m.group(1))
    m = re.fullmatch(r"its (.+?) is '([^']+)'", t)
    if m:
        return ('cat', normkey(m.group(1)), m.group(2))
    m = re.fullmatch(r"its (.+?) is " + COMP_RE + r" (.+)", t)
    if m:
        return ('cmp', m.group(1).strip(), COMP_OP[m.group(2)], m.group(3).strip())
    m = re.fullmatch(r"its (.+?) " + r"(exceeds) (.+)", t)
    if m:
        return ('cmp', m.group(1).strip(), '>', m.group(3).strip())
    raise ParseError('part? ' + t[:60])


def parse_cond(text):
    t = text.strip()
    conn = None
    m = re.match(r'^exactly one of (.+)$', t, re.I)
    if m:
        conn = 'one'
        t = m.group(1)
    t = t[0].lower() + t[1:]
    quoted = []

    def mask(mm):
        quoted.append(mm.group(0))
        return '\x00%d\x00' % (len(quoted) - 1)
    tm = re.sub(r"'[^']*'", mask, t)
    pieces = re.split(r',\s+(?:(and|or)\s+)?(?=its?\s)|\s+(and|or)\s+(?=its?\s)', tm)
    parts = []
    seps = []
    i = 0
    toks = pieces
    parts.append(toks[0])
    j = 1
    while j < len(toks):
        a, b = toks[j], toks[j + 1]
        seps.append(a or b or ',')
        parts.append(toks[j + 2])
        j += 3
    words = {s for s in seps if s != ','}
    if conn == 'one':
        if words - {'and'}:
            raise ParseError('mixed exactly-one')
    else:
        if len(words) > 1:
            raise ParseError('mixed connectives')
        conn = words.pop() if words else ('and' if len(parts) == 1 else None)
        if conn is None:
            raise ParseError('no connective')
    unmask = lambda s: re.sub(r'\x00(\d+)\x00', lambda mm: quoted[int(mm.group(1))], s)
    return (conn, [parse_part(unmask(p)) for p in parts])


RULE_RX = [
    ('sc', re.compile(r"^(?P<cond>(?:It|Its|Exactly one of) .+?): (?P<pts>[+\-−]?\d+) points?(?:, unless (?P<unl>.+?))?\.$")),
    ('fc', re.compile(r"^The score floor is (?P<f>-?\d+) and the score cap is (?P<m>-?\d+)\.?$")),
    ('oi', re.compile(r"^Tier '(?P<t>[^']+)' only if (?P<cond>.+?)\.$")),
    ('ov', re.compile(r"^Override: if (?P<cond>.+?), the tier is '(?P<t>[^']+)'\.$")),
    ('ar', re.compile(r"^'(?P<a>[^']+)' is required when (?P<cond>.+?)\.$")),
    ('inv', re.compile(r"^The rule: an? (?P<noun>.+?) meets the rule when (?P<cond>.+?)\.$")),
    ('risk', re.compile(r"^Here, the risk of an? (?P<noun>.+?) means its (?P<q>.+?)\.$")),
    ('rat', re.compile(r"^Ratings (?:are )?(?:listed )?from lowest to highest: (?P<l>.+?)\.?$")),
    ('lik', re.compile(r"Likelihood means the chance of '(?P<e>[^']+)'\.")),
    ('imp', re.compile(r"Impact means (?:the |its )?(?P<x>.+?)\.(?: |$)")),
    ('net', re.compile(r"Amounts are net values")),
    ('tie', re.compile(r"lower reference number|lower ID number|lower [a-z ]*number")),
    ('indep', re.compile(r"occur independently")),
    ('sem14', re.compile(r"a total below (?P<f>-?\d+) becomes (?P=f),? and a total above (?P<m>-?\d+) becomes (?P=m)")),
]


def _apply_rule_line(R, s):
    hit = False
    for name, rx in RULE_RX:
        m = rx.search(s) if name in ('lik', 'imp', 'net', 'tie', 'indep', 'sem14') else rx.match(s)
        if not m:
            continue
        hit = True
        if name == 'sc':
            pts = int(m.group('pts').replace('−', '-').replace('+', ''))
            R.lines.append((pts, parse_cond(m.group('cond')), parse_cond(m.group('unl')) if m.group('unl') else None))
        elif name == 'fc':
            R.floor, R.cap = int(m.group('f')), int(m.group('m'))
        elif name == 'oi':
            R.only_if[m.group('t')] = parse_cond(m.group('cond'))
        elif name == 'ov':
            R.overrides.append((parse_cond(m.group('cond')), m.group('t')))
        elif name == 'ar':
            if m.group('a') in R.actions:
                R.dup_actions.append(m.group('a'))
            R.actions[m.group('a')] = parse_cond(m.group('cond'))
        elif name == 'inv':
            R.inv = parse_cond('its ' + m.group('cond')[4:] if m.group('cond').startswith('its ') else m.group('cond'))
        elif name == 'risk':
            q = m.group('q')
            mm = re.fullmatch(r"chance of '([^']+)'", q)
            if mm:
                R.risk = ('chance', mm.group(1))
            elif q == 'expected loss':
                R.risk = ('loss',)
            elif q == 'score':
                R.risk = ('score',)
            elif q == 'total expected cost':
                R.risk = ('tec',)
            elif q == 'expected value':
                R.risk = ('value',)
            else:
                raise ParseError('risk? ' + q)
        elif name == 'rat':
            R.rating_order = re.findall(r"'([^']+)'", m.group('l'))
        elif name == 'lik':
            R.lik_event = m.group('e')
        elif name == 'imp':
            R.imp_kind = m.group('x')
        elif name == 'net':
            R.net = True
        elif name == 'tie':
            R.tie_lower = True
        elif name == 'indep':
            R.indep = True
        elif name == 'sem14':
            R.floorcap_sem14 = (int(m.group('f')), int(m.group('m')))
    return hit


def _apply_table(R, rows):
    hdr = list(rows[0].keys())
    h0 = normkey(hdr[0])
    if h0 == 'tier':
        R.tiers = [(r[hdr[0]], r[hdr[1]]) for r in rows]
    elif h0 == 'likelihood level' and normkey(hdr[1]).startswith('chance'):
        R.lik = [(r[hdr[0]], r[hdr[1]]) for r in rows]
    elif h0 == 'impact level':
        R.imp = [(r[hdr[0]], r[hdr[1]]) for r in rows]
    elif h0 == 'likelihood level':
        R.grid_cols = hdr[1:]
        for r in rows:
            R.grid[r[hdr[0]]] = {c: r[c] for c in hdr[1:]}


def build_rules(texts):
    R = Rules()
    R.grid_cols = []
    seen = set()
    for text in texts:
        if not text:
            continue
        t = strip_fences(text)
        if re.search(r'<(?:li|tr|td|th|h\d|p|div|ul|dl|section|article)\b', t):
            t = html_to_text(t)
        items = []
        if t.strip()[:1] in '{[':
            try:
                _walk(json.loads(t.strip(), parse_float=str, parse_int=str), items)
            except Exception:
                _line_items(t, items, rules=True)
        else:
            _line_items(t, items, rules=True)
        rows = []
        for it in items + [('end',)]:
            if it[0] == 'row':
                if rows and list(rows[-1].keys()) != list(it[1].keys()):
                    _apply_table(R, rows)
                    rows = []
                rows.append(it[1])
                continue
            if rows:
                _apply_table(R, rows)
                rows = []
            if it[0] == 'end':
                break
            if it[0] == 'kv':
                line = it[1] + ': ' + it[2]
            elif it[0] == 'sent':
                line = it[1]
            else:
                continue
            if line in seen:
                continue
            seen.add(line)
            if not _apply_rule_line(R, line):
                for s in split_sentences(line):
                    _apply_rule_line(R, s)
    return R


# ---------------------------------------------------------------- question (section 2 Question; section 1 forms)
QSUBJ = (r"(?P<subj>the score of (?P<id1>" + ID_RE + r")|the risk of (?P<id2>" + ID_RE + r")"
         r"|the expected (?P<ev>loss|value) for (?P<id3>" + ID_RE + r")"
         r"|the total expected cost (?:of|for) (?P<id4>" + ID_RE + r")"
         r"|the expected number of '(?P<ne>[^']+)' for (?P<id5>" + ID_RE + r")"
         r"|the chance that (?P<id6>" + ID_RE + r") is classed '(?P<h>[^']+)')")
YN_RX = re.compile(r"Is (?:(?P<outer>it true that|it not the case that) )?" + QSUBJ +
                   r"(?: is(?P<neg> not)?)? " + COMP_RE + r" (?P<val>[^?]+?)\?")
ACT_RX = re.compile(r"(?:Does (?P<id>" + ID_RE + r") require '(?P<a>[^']+)'"
                    r"|Is (?P<outer>it true that|it not the case that) (?P<id2>" + ID_RE +
                    r") does not require '(?P<a2>[^']+)')\?")
CHOICE_RX = [
    ('BIN', re.compile(r"(?:In which range is|Which range contains) the chance that (?P<id>" + ID_RE +
                       r") is classed '(?P<h>[^']+)'\?")),
    ('TIER', re.compile(r"(?:Which tier is (?P<id>" + ID_RE + r") in|In which tier does (?P<id2>" + ID_RE + r") fall)\?")),
    ('MAT', re.compile(r"(?:Which rating does (?P<id>" + ID_RE + r") get|What rating does (?P<id2>" + ID_RE + r") receive)\?")),
    ('RANK-top', re.compile(r"Which (?P<noun>[^?]+?) has the (?P<dir>highest|lowest) (?P<q>risk|expected loss|total expected cost|expected value|score|chance of '[^']+')\?")),
    ('RANK-order', re.compile(r"Which ordering, highest to lowest (?P<q>risk|expected loss|total expected cost|score|chance of '[^']+'), is correct\?")),
    ('DEC', re.compile(r"Which action does the rule for choosing an action select for (?P<id>" + ID_RE + r")\?")),
    ('PRED', re.compile(r"(?:Predict which outcome (?P<id>" + ID_RE + r") will have, using only the chances given"
                        r"|Using only the chances given, predict which outcome (?P<id2>" + ID_RE + r") will have)")),
    ('INV', re.compile(r"(?:Which listed (?P<n1>[^?]+?)|Which of these (?P<n2>[^?]+?)) meets the rule\?")),
]


def parse_question(instr):
    """The row's own question is the last question match in `instructions` (worked examples come first)."""
    best = None
    for m in YN_RX.finditer(instr):
        best = (m.start(), 'YN', m)
    for m in ACT_RX.finditer(instr):
        if best is None or m.start() > best[0]:
            best = (m.start(), 'ACT', m)
    for form, rx in CHOICE_RX:
        for m in rx.finditer(instr):
            if best is None or m.start() > best[0]:
                best = (m.start(), form, m)
    if best is None:
        raise ParseError('no question')
    _, form, m = best
    gd = m.groupdict()
    q = {'form': form}
    if form == 'YN':
        pol = 1
        if gd['outer'] and not gd['neg']:
            raise ParseError('outer frame without inner negation')
        if gd['neg']:
            pol = -pol
        if gd['outer'] == 'it not the case that':
            pol = -pol
        q['pol'] = pol
        q['op'] = COMP_OP[m.group(len(m.groups()) - 1)]   # the comparator group sits just before 'val'
        q['val'] = gd['val'].strip()
        if gd['id1']:
            q['qty'], q['id'] = 'score', gd['id1']
        elif gd['id2']:
            q['qty'], q['id'] = 'risk', gd['id2']
        elif gd['id3']:
            q['qty'], q['id'] = ('loss' if gd['ev'] == 'loss' else 'value'), gd['id3']
        elif gd['id4']:
            q['qty'], q['id'] = 'tec', gd['id4']
        elif gd['id5']:
            q['qty'], q['id'], q['event'] = 'nev', gd['id5'], gd['ne']
        else:
            q['qty'], q['id'], q['h'] = 'post', gd['id6'], gd['h']
    elif form == 'ACT':
        q['form'] = 'YN'
        q['qty'] = 'action'
        if gd['id']:
            q['id'], q['action'], q['pol'] = gd['id'], gd['a'], 1
        else:
            q['id'], q['action'] = gd['id2'], gd['a2']
            q['pol'] = -1 if gd['outer'] == 'it true that' else 1
    else:
        q['id'] = gd.get('id') or gd.get('id2')
        if form == 'BIN':
            q['h'] = gd['h']
        if form == 'RANK-top':
            q['dir'] = gd['dir']
            q['q'] = gd['q']
        if form == 'RANK-order':
            q['q'] = gd['q']
    return q


# ---------------------------------------------------------------- ranges (SEM-06, SEM-11, SEM-16)
def parse_range(text, kind):
    """'below b' | 'at least a and below b' | 'at least c' | 'above a and at most b' | 'at least a and at most b'
    -> (lo, lo_op, hi, hi_op); None = unbounded. kind: 'chance' | 'amount' | 'score'."""
    pv = {'chance': parse_chance, 'amount': parse_amount, 'score': lambda x: F(int(x.strip()))}[kind]
    t = text.strip().strip("'")
    m = re.fullmatch(r'(at least|above|no less than|more than|over) (.+?) and (below|at most|under|less than|no more than) (.+)', t)
    if m:
        return (pv(m.group(2)), COMP_OP[m.group(1)], pv(m.group(4)), COMP_OP[m.group(3)])
    m = re.fullmatch(r'(below|at most|under|less than|no more than) (.+)', t)
    if m:
        return (None, None, pv(m.group(2)), COMP_OP[m.group(1)])
    m = re.fullmatch(r'(at least|above|no less than|more than|over) (.+)', t)
    if m:
        return (pv(m.group(2)), COMP_OP[m.group(1)], None, None)
    raise ParseError('range? ' + t[:50])


def in_range(v, rg):
    lo, lop, hi, hop = rg
    if lo is not None and not cmp_frac(v, lop, lo):
        return False
    if hi is not None and not cmp_frac(v, hop, hi):
        return False
    return True


# ---------------------------------------------------------------- points and tiers: relational engine (sqlite3)
_OPS_SQL = {'>=': '>=', '<=': '<=', '>': '>', '<': '<'}


class PointsDB:
    """In-memory sqlite3 database holding the card's scorecard, cut table, 'only if' limits and overrides.
    Each SEM-15 stage is one SQL query over the per-case fact table."""

    def __init__(self, R):
        self.R = R
        db = sqlite3.connect(':memory:')
        self.db = db
        db.executescript("""
        CREATE TABLE cond(cid INTEGER PRIMARY KEY, conn TEXT, n INTEGER);
        CREATE TABLE part(cid INTEGER, idx INTEGER, kind TEXT, key TEXT, op TEXT, sval TEXT, vn INTEGER, vd INTEGER);
        CREATE TABLE line(lid INTEGER PRIMARY KEY, pts INTEGER, cid INTEGER, ucid INTEGER);
        CREATE TABLE tier(idx INTEGER PRIMARY KEY, name TEXT, lo_n INTEGER, lo_op TEXT, hi_n INTEGER, hi_op TEXT);
        CREATE TABLE onlyif(tidx INTEGER, cid INTEGER);
        CREATE TABLE override(oid INTEGER PRIMARY KEY, cid INTEGER, tidx INTEGER);
        CREATE TABLE fact(key TEXT, kind TEXT, sval TEXT, vn INTEGER, vd INTEGER);
        CREATE TABLE param(name TEXT PRIMARY KEY, v INTEGER);
        """)
        self._ncid = 0
        self.qty_parts = set()
        for lid, (pts, c, u) in enumerate(R.lines):
            db.execute('INSERT INTO line VALUES (?,?,?,?)', (lid, pts, self._add_cond(c), self._add_cond(u) if u else None))
        for i, (name, rt) in enumerate(R.tiers):
            lo, lop, hi, hop = parse_range(rt, 'score')
            db.execute('INSERT INTO tier VALUES (?,?,?,?,?,?)',
                       (i, name, None if lo is None else int(lo), lop, None if hi is None else int(hi), hop))
        tidx = {name: i for i, (name, _) in enumerate(R.tiers)}
        self.tidx = tidx
        for t, c in R.only_if.items():
            db.execute('INSERT INTO onlyif VALUES (?,?)', (tidx[t], self._add_cond(c)))
        for i, (c, t) in enumerate(R.overrides):
            db.execute('INSERT INTO override VALUES (?,?,?)', (i, self._add_cond(c), tidx[t]))
        self.action_cids = {a: self._add_cond(c) for a, c in R.actions.items()}
        self.inv_cid = self._add_cond(R.inv) if R.inv else None
        if R.floor is not None:
            db.execute("INSERT INTO param VALUES ('floor', ?)", (R.floor,))
            db.execute("INSERT INTO param VALUES ('cap', ?)", (R.cap,))
        db.executescript("""
        CREATE VIEW parttruth AS
          SELECT p.cid, p.idx,
            CASE p.kind
              WHEN 'bool' THEN EXISTS(SELECT 1 FROM fact f WHERE f.key=p.key AND f.kind='bool' AND f.sval='yes')
              WHEN 'cat'  THEN EXISTS(SELECT 1 FROM fact f WHERE f.key=p.key AND f.kind='str' AND f.sval=p.sval)
              WHEN 'cmp'  THEN EXISTS(SELECT 1 FROM fact f WHERE f.key=p.key AND f.kind='num' AND (
                   (p.op='>=' AND f.vn*p.vd >= p.vn*f.vd) OR (p.op='<=' AND f.vn*p.vd <= p.vn*f.vd) OR
                   (p.op='>'  AND f.vn*p.vd >  p.vn*f.vd) OR (p.op='<'  AND f.vn*p.vd <  p.vn*f.vd)))
              WHEN 'req'  THEN EXISTS(SELECT 1 FROM fact f WHERE f.key=p.key AND f.kind='req' AND f.sval='yes')
            END AS truth
          FROM part p;
        CREATE VIEW condtruth AS
          SELECT c.cid,
            CASE c.conn WHEN 'and' THEN SUM(t.truth) = c.n
                        WHEN 'or'  THEN SUM(t.truth) >= 1
                        WHEN 'one' THEN SUM(t.truth) = 1 END AS holds
          FROM cond c JOIN parttruth t ON t.cid = c.cid GROUP BY c.cid;
        """)

    def _add_cond(self, c):
        conn, parts = c
        cid = self._ncid
        self._ncid += 1
        self.db.execute('INSERT INTO cond VALUES (?,?,?)', (cid, conn, len(parts)))
        for i, p in enumerate(parts):
            if p[0] == 'bool':
                row = (cid, i, 'bool', p[1], None, None, None, None)
            elif p[0] == 'cat':
                row = (cid, i, 'cat', p[1], None, p[2], None, None)
            elif p[0] == 'req':
                row = (cid, i, 'req', normkey(p[1]), None, None, None, None)
            else:
                qname = normkey(p[1])
                self.qty_parts.add((qname, p[3]))
                v = value_for_part(qname, p[3])
                row = (cid, i, 'cmp', qname, p[2], None, v.numerator, v.denominator)
            self.db.execute('INSERT INTO part VALUES (?,?,?,?,?,?,?,?)', row)
        return cid

    def load_facts(self, facts):
        """facts: normkey -> True/False (Boolean presence), str (category) or Fraction (number)."""
        self.db.execute('DELETE FROM fact')
        for k, v in facts.items():
            if isinstance(v, bool):
                self.db.execute("INSERT INTO fact VALUES (?, 'bool', ?, NULL, NULL)", (k, 'yes' if v else 'no'))
            elif isinstance(v, F):
                self.db.execute("INSERT INTO fact VALUES (?, 'num', NULL, ?, ?)", (k, v.numerator, v.denominator))
            elif isinstance(v, tuple) and v[0] == 'req':
                self.db.execute("INSERT INTO fact VALUES (?, 'req', ?, NULL, NULL)", (k, 'yes' if v[1] else 'no'))
            else:
                self.db.execute("INSERT INTO fact VALUES (?, 'str', ?, NULL, NULL)", (k, v))

    def cond_holds(self, cid):
        r = self.db.execute('SELECT holds FROM condtruth WHERE cid=?', (cid,)).fetchone()
        return bool(r[0])

    def score(self):
        # stage 1: applying lines (condition holds and its 'unless' exception does not)
        # stage 2: sum; stage 3: final clamp (SEM-14)
        raw = self.db.execute("""
            SELECT COALESCE(SUM(l.pts), 0) FROM line l
            JOIN condtruth c ON c.cid = l.cid
            LEFT JOIN condtruth u ON u.cid = l.ucid
            WHERE c.holds = 1 AND (l.ucid IS NULL OR u.holds = 0)""").fetchone()[0]
        sc = self.db.execute("""
            SELECT MAX((SELECT v FROM param WHERE name='floor'), MIN((SELECT v FROM param WHERE name='cap'), ?))""",
                             (raw,)).fetchone()[0]
        return raw, sc

    def tier(self, sc):
        # stage 4: cut table lookup (explicit end comparisons)
        rows = self.db.execute("""
            SELECT idx FROM tier WHERE
              (lo_n IS NULL OR (lo_op='>=' AND ? >= lo_n) OR (lo_op='>' AND ? > lo_n)) AND
              (hi_n IS NULL OR (hi_op='<' AND ? < hi_n) OR (hi_op='<=' AND ? <= hi_n))""", (sc, sc, sc, sc)).fetchall()
        if len(rows) != 1:
            raise ParseError('cut table does not place score %s (%d tiers)' % (sc, len(rows)))
        t = rows[0][0]
        # stage 5: 'only if' move-down (SEM-05): highest lower tier with no 'only if' or whose 'only if' holds
        blocked = self.db.execute("""
            SELECT 1 FROM onlyif o JOIN condtruth c ON c.cid=o.cid WHERE o.tidx=? AND c.holds=0""", (t,)).fetchone()
        if blocked:
            r = self.db.execute("""
                SELECT MAX(t.idx) FROM tier t WHERE t.idx < ? AND NOT EXISTS (
                  SELECT 1 FROM onlyif o JOIN condtruth c ON c.cid=o.cid WHERE o.tidx=t.idx AND c.holds=0)""",
                                (t,)).fetchone()
            t = r[0]
        # stage 6: overrides; conflict -> highest tier in cut-table order
        r = self.db.execute("""
            SELECT MAX(o.tidx) FROM override o JOIN condtruth c ON c.cid=o.cid WHERE c.holds=1""").fetchone()
        if r[0] is not None:
            t = r[0]
        return self.R.tiers[t][0]


def value_for_part(qname, raw):
    """Comparison value of a condition part, read by the quantity it is compared with (SEM-06 / section 1)."""
    if qname == 'score':
        return F(int(raw.replace(',', '')))
    if qname.startswith('chance'):
        return parse_chance(raw)
    if qname.startswith('expected number'):
        return _dec(raw.split()[0])
    return parse_amount(raw)


# ---------------------------------------------------------------- multilinear forms over the open-world box
INF = 'inf'
BIG = F(10) ** 15


def ml_const(c):
    return {frozenset(): F(c)} if c else {}


def ml_var(v):
    return {frozenset([v]): F(1)}


def ml_add(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, F(0)) + v
        if r[k] == 0:
            del r[k]
    return r


def ml_scale(a, c):
    return {k: v * c for k, v in a.items() if v * c != 0}


def ml_mul(a, b):
    r = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            if k1 & k2:
                raise ParseError('non-multilinear product')
            k = k1 | k2
            r[k] = r.get(k, F(0)) + v1 * v2
    return {k: v for k, v in r.items() if v != 0}


def ml_vars(a):
    s = set()
    for k in a:
        s |= k
    return s


def ml_subst(a, var, val):
    r = {}
    for k, v in a.items():
        if var in k:
            k2 = k - {var}
            r[k2] = r.get(k2, F(0)) + v * val
        else:
            r[k] = r.get(k, F(0)) + v
    return {k: v for k, v in r.items() if v != 0}


def ml_const_val(a):
    if ml_vars(a):
        raise ValueError('not constant')
    return a.get(frozenset(), F(0))


def ml_ext(a, bounds, sense):
    """Exact max (sense=+1) or min (sense=-1) of a multilinear form over the closed box; may return +-INF."""
    vs = sorted(ml_vars(a), key=repr)
    if not vs:
        return a.get(frozenset(), F(0))
    v = vs[0]
    lo, hi = bounds[v]
    f1 = {}
    for k, c in a.items():
        if v in k:
            f1[k - {v}] = f1.get(k - {v}, F(0)) + c
    if hi is None:
        e1 = ml_ext(f1, bounds, sense)
        if (sense > 0 and (e1 == INF or (e1 != ('-' + INF) and e1 > 0))) or \
           (sense < 0 and (e1 == '-' + INF or (e1 != INF and e1 < 0))):
            return INF if sense > 0 else '-' + INF
        return ml_ext(ml_subst(a, v, lo), bounds, sense)
    c1 = ml_ext(ml_subst(a, v, lo), bounds, sense)
    c2 = ml_ext(ml_subst(a, v, hi), bounds, sense)
    return _ext_pick(c1, c2, sense)


def _ext_pick(c1, c2, sense):
    def key(x):
        if x == INF:
            return (1, 0)
        if x == '-' + INF:
            return (-1, 0)
        return (0, x)
    return max(c1, c2, key=key) if sense > 0 else min(c1, c2, key=key)


def ext_cmp(x, op, t):
    """Compare an extended value (Fraction or +-INF) with a Fraction."""
    if x == INF:
        return op in ('>', '>=')
    if x == '-' + INF:
        return op in ('<', '<=')
    return cmp_frac(x, op, t)


NEG = {'>': '<=', '>=': '<', '<': '>=', '<=': '>'}


def ml_always(a, op, t, bounds):
    """True when 'a op t' holds at every allowed point (counter-witness search over the box)."""
    if op in ('>', '>='):
        return ext_cmp(ml_ext(a, bounds, -1), op, t)
    return ext_cmp(ml_ext(a, bounds, +1), op, t)


def ml_truthset(a, op, t, bounds):
    s = set()
    if ml_always(a, op, t, bounds):
        s.add(True)
    elif ml_always(a, NEG[op], t, bounds):
        s.add(False)
    else:
        s = {True, False}
    return s


# ---------------------------------------------------------------- quantities: integer ledger + open-world variables
def _num_or_str(raw):
    t = raw.strip().strip('"').strip()
    if re.fullmatch(r'-?\d[\d,]*(?:\.\d+)?(?:\s+[A-Za-z][A-Za-z \-]*)?', t) or t.lower() == 'none':
        return parse_amount(t)
    return t


class World:
    def __init__(self, doc, R):
        self.doc = doc
        self.R = R
        self.bounds = {}

    def _p_ml(self, e, ev, o):
        if o.p is not None and not o.p_nr:
            return ml_const(o.p)
        if not o.p_nr:
            raise ParseError('chance missing for %s' % ev)
        others = sum((x.p for k, x in e.outcomes.items() if k != ev and x.p is not None and not x.p_nr), F(0))
        lo, hi = o.p_rng if o.p_rng else (F(0), F(1))
        hi = min(hi, F(1) - others)        # SEM-19 / section 2: [0, 1 - other listed chances] cut by the range
        var = ('p', e.id, ev)
        self.bounds[var] = (lo, hi)
        return ml_var(var)

    def _a_ml(self, e, ev, o):
        if o.a is not None and not o.a_nr:
            return ml_const(o.a)
        if not o.a_nr:
            raise ParseError('amount missing for %s' % ev)
        var = ('a', e.id, ev)
        if o.a_rng:
            self.bounds[var] = o.a_rng
        else:
            if self.R.net:
                raise ParseError('net-mode amount without range')
            self.bounds[var] = (F(0), None)
        return ml_var(var)

    def expected(self, e):
        tot = {}
        for ev, o in e.outcomes.items():
            tot = ml_add(tot, ml_mul(self._p_ml(e, ev, o), self._a_ml(e, ev, o)))
        return tot

    def own(self, e):
        if e.own is None:
            raise ParseError('own cost missing for %s' % e.id)
        if e.own == 'NR' or is_nr(e.own):
            var = ('own', e.id)
            self.bounds[var] = e.own_rng and (parse_amount(e.own_rng[0]), parse_amount(e.own_rng[1])) or (F(0), None)
            return ml_var(var)
        return ml_const(parse_amount(e.own))

    def chance(self, e, ev):
        if ev not in e.outcomes:
            raise ParseError('no chance of %s for %s' % (ev, e.id))
        return self._p_ml(e, ev, e.outcomes[ev])

    def quantity(self, e, qname):
        """qname: normalised quantity text (section 1 lexicon) -> multilinear form."""
        if qname == 'risk':
            rk = self.R.risk
            if rk is None:
                raise ParseError('risk without SEM-22')
            if rk[0] == 'loss':
                return self.expected(e)
            if rk[0] == 'chance':
                return self.chance(e, rk[1])
            if rk[0] == 'tec':
                return ml_add(self.own(e), self.expected(e))
            if rk[0] == 'value':
                return self.expected(e)
            raise ParseError('risk kind %s' % (rk,))
        if qname in ('expected loss', 'expected value'):
            return self.expected(e)
        if qname == 'total expected cost':
            return ml_add(self.own(e), self.expected(e))
        m = re.fullmatch(r"chance of '(.+)'", qname)
        if m:
            return self.chance(e, m.group(1))
        m = re.fullmatch(r"expected number of '(.+)'", qname)
        if m:
            if not e.nev:
                raise ParseError('expected number missing')
            return ml_const(e.nev[0] * e.nev[1])
        raise ParseError('quantity? ' + qname)


def ledger_compare(vals, ids):
    """Integer ledger: scale exact amounts to integers by the common denominator, then order (value, ID)."""
    den = 1
    for v in vals.values():
        den = den * v.denominator // math.gcd(den, v.denominator)
    return {k: int(v * den) for k, v in vals.items()}, den


# ---------------------------------------------------------------- bayes: integer population counting
def case_sign(doc, case_id, ev):
    e = doc.ents.get(case_id)
    if e is None:
        raise ParseError('case %s has no facts' % case_id)
    f = e.facts.get(normkey(ev))
    if f is None:
        raise ParseError('sign %s not stated for case' % ev)
    if f[0] != 'bool':
        raise ParseError('sign %s not Boolean' % ev)
    return f[1]


def bayes_weights(doc, case_id, world):
    """-> (hyps, {H: multilinear weight}). Closed world weights are constants (integer counts after scaling)."""
    hyps = list(doc.hyp_order)
    W = {}
    if doc.tbl_rows:
        e = doc.ents.get(case_id)
        sign = doc.tbl_sign
        if sign is None:
            bools = [k for k, v in e.facts.items() if v[0] == 'bool']
            if len(bools) != 1:
                raise ParseError('count table sign unknown')
            obs = e.facts[bools[0]][1]
        else:
            obs = case_sign(doc, case_id, sign)
        for h, n1, n0 in doc.tbl_rows:
            W[h] = ml_const(n1 if obs else n0)
        return [h for h, _, _ in doc.tbl_rows], W
    if doc.cnt:
        signs = sorted({ev for (_, ev) in doc.cnt})
        if len(signs) != 1:
            raise ParseError('multi-sign counts')
        obs = case_sign(doc, case_id, signs[0])
        for h in hyps:
            n1, n0 = doc.cnt[(h, signs[0])]
            W[h] = ml_const(n1 if obs else n0)
        return hyps, W
    if doc.cnt_e:
        evs = sorted({ev for (ev, _) in doc.cnt_e})
        if len(evs) != 1:
            raise ParseError('multi-sign evidence counts')
        obs = case_sign(doc, case_id, evs[0])
        tab = doc.cnt_e.get((evs[0], obs))
        if tab is None:
            raise ParseError('evidence count row missing')
        if sum(tab.values()) != doc.cnt_e_tot[(evs[0], obs)]:
            raise ParseError('evidence counts do not add up to the stated total')
        for h in hyps:
            W[h] = ml_const(tab[h])
        return hyps, W
    if doc.joint:
        evs = sorted({ev for (_, ev) in doc.joint})
        if len(evs) != 1:
            raise ParseError('multi-sign joint shares')
        obs = case_sign(doc, case_id, evs[0])
        for h in hyps:
            j = doc.joint[(h, evs[0])]
            if obs:
                W[h] = ml_const(j)
            else:
                if h not in doc.base:
                    raise ParseError('joint shares without base rates for a not-shown sign')
                W[h] = ml_const(doc.base[h] - j)
        return hyps, W
    if doc.base:
        evs = []
        for (h, ev) in list(doc.cond.keys()) + list(doc.cond_rng.keys()):
            if ev not in evs:
                evs.append(ev)
        if sum(doc.base.values()) != 1:
            raise ParseError('base rates do not sum to 1')
        for h in hyps:
            w = ml_const(doc.base[h])
            for ev in evs:
                obs = case_sign(doc, case_id, ev)
                c = doc.cond.get((h, ev))
                if c is None and (h, ev) not in doc.cond_rng:
                    raise ParseError('missing P(E|H)')
                if c == 'NR' or c is None:
                    var = ('c', h, ev)
                    world.bounds[var] = doc.cond_rng.get((h, ev), (F(0), F(1)))
                    f = ml_var(var) if obs else ml_add(ml_const(1), ml_scale(ml_var(var), -1))
                else:
                    f = ml_const(c if obs else 1 - c)
                w = ml_mul(w, f)
            W[h] = w
        return hyps, W
    raise ParseError('no chance model')


def int_counts(W):
    """Integer population: N = lcm of all denominators; counts per hypothesis cell."""
    vals = {h: ml_const_val(w) for h, w in W.items()}
    N = 1
    for v in vals.values():
        N = N * v.denominator // math.gcd(N, v.denominator)
    return {h: int(v * N) for h, v in vals.items()}, N


# ---------------------------------------------------------------- case evaluation (points, rules) with unknowns
LEX_Q = re.compile(r"^(?:expected loss|expected value|total expected cost|risk|chance of .+|expected number of .+)$")


class CaseEval:
    def __init__(self, P, world, R, e):
        self.P, self.world, self.R, self.e = P, world, R, e
        known, unk = {}, []
        for k, v in e.facts.items():
            if v[0] == 'bool':
                known[k] = v[1]
            elif v[0] == 'str':
                known[k] = _num_or_str(v[1])
            else:
                unk.append(k)
        self.known, self.unk = known, unk
        bool_keys = set(r[0] for r in P.db.execute("SELECT key FROM part WHERE kind='bool'"))
        num_keys = set(r[0] for r in P.db.execute("SELECT key FROM part WHERE kind='cmp'"))
        cat_keys = set(r[0] for r in P.db.execute("SELECT key FROM part WHERE kind='cat'"))
        self.ub = [k for k in unk if k in bool_keys]
        self.un = [k for k in unk if k in num_keys]
        if any(k in cat_keys for k in unk):
            raise ParseError('unknown categorical fact')
        # numeric quantities a condition compares (lexicon quantities of the case)
        self.qty = {}
        for qn, _ in P.qty_parts:
            if LEX_Q.match(qn):
                raw = qn
                m = re.fullmatch(r'(chance of|expected number of) (.+)', qn)
                if m:
                    ev = self._event_by_key(m.group(2))
                    raw = "%s '%s'" % (m.group(1), ev) if ev else None
                if raw is not None:
                    try:
                        self.qty[qn] = world.quantity(e, raw)
                    except ParseError:
                        pass

    def _event_by_key(self, key):
        for ev in list(self.e.outcomes.keys()) + ([self.e.nev[2]] if self.e.nev else []):
            if normkey(ev) == key:
                return ev
        if self.e.nev:
            return None
        return None

    def scenarios(self):
        """Every Boolean assignment of the unknown factors x every corner of each uncertain numeric quantity."""
        for bits in itertools.product([False, True], repeat=len(self.ub)):
            f = dict(self.known)
            for k, b in zip(self.ub, bits):
                f[k] = b
            numopts = []
            for k in self.un:
                lo, hi = self.e.rng.get(k, ('0', None))
                lo = parse_amount(lo) if isinstance(lo, str) else lo
                hi = (parse_amount(hi) if isinstance(hi, str) else hi) if hi is not None else BIG
                numopts.append([(k, lo), (k, hi)])
            for qn, form in self.qty.items():
                if ml_vars(form):
                    mn = ml_ext(form, self.world.bounds, -1)
                    mx = ml_ext(form, self.world.bounds, +1)
                    mn = -BIG if mn == '-' + INF else mn
                    mx = BIG if mx == INF else mx
                    numopts.append([(qn, mn), (qn, mx)])
                else:
                    f[qn] = ml_const_val(form)
            for combo in itertools.product(*numopts) if numopts else [()]:
                g = dict(f)
                for k, v in combo:
                    g[k] = v
                yield g

    def eval_all(self, what):
        """what: 'score' | ('cond', cid) | 'tier'. Returns the set of results over all allowed scenarios."""
        out = set()
        for f in self.scenarios():
            self.P.load_facts(f)
            raw, sc = (None, None)
            if self.R.lines:
                raw, sc = self.P.score()
                self.P.db.execute("INSERT INTO fact VALUES ('score','num',NULL,?,1)", (sc,))
            if what == 'score':
                out.add(sc)
            elif what == 'tier':
                out.add(self.P.tier(sc))
            else:
                for a, acid in self.P.action_cids.items():
                    self.P.db.execute("INSERT INTO fact VALUES (?,'req',?,NULL,NULL)",
                                      (normkey(a), 'yes' if self.P.cond_holds(acid) else 'no'))
                out.add(self.P.cond_holds(what[1]))
        return out


# ---------------------------------------------------------------- solve one row
def threshold_value(qty, raw, R):
    if qty == 'score' or (qty == 'risk' and R.risk == ('score',)):
        return F(int(raw.replace(',', '')))
    if qty == 'post' or (qty == 'risk' and R.risk and R.risk[0] == 'chance'):
        return parse_chance(raw)
    if qty == 'nev':
        return _dec(raw.strip())
    return parse_amount(raw)


def is_open(row):
    txt = ' '.join(x for x in (row.get('state'), row.get('card'), row.get('instructions')) if x)
    return bool(re.search(r'not recorded', row.get('state') or '', re.I))


def solve(row):
    """-> dict(answer=<gold-format answer>, abstain=bool, probs={opt: Fraction} | None, note=str)"""
    doc, _ = build_doc(row['state'])
    R = build_rules([row.get('card'), row.get('instructions'), row.get('state')])
    q = parse_question(row['instructions'])
    world = World(doc, R)
    opts = row.get('options') or []
    abst = [o for o in opts if o in (CBD_TXT, NOTA_TXT)]
    real = [o for o in opts if o not in (CBD_TXT, NOTA_TXT)]
    form = q['form']
    res = {'form': form, 'probs': None, 'abstain': False}

    if form == 'YN':
        P = PointsDB(R)
        e = doc.ents.get(q['id']) or doc.ent(q['id'])
        qty = q['qty']
        if qty in ('score', 'action') or (qty == 'risk' and R.risk == ('score',)):
            ce = CaseEval(P, world, R, e)
            if qty == 'action':
                vals = ce.eval_all(('cond', P.action_cids[q['action']]))
                ans = vals
            else:
                T = threshold_value(qty, q['val'], R)
                ans = {cmp_frac(F(v), q['op'], T) for v in ce.eval_all('score')}
        elif qty == 'post':
            T = parse_chance(q['val'])
            hyps, W = bayes_weights(doc, q['id'], world)
            tot = {}
            for h in hyps:
                tot = ml_add(tot, W[h])
            if not ml_vars(tot) and not ml_vars(W[q['h']]):
                cnt, N = int_counts(W)
                c_t, c_all = cnt[q['h']], sum(cnt.values())
                ans = {cmp_frac(F(c_t * T.denominator), q['op'], F(T.numerator * c_all))}
            else:
                g = ml_add(W[q['h']], ml_scale(tot, -T))     # P(H|E) op T  <=>  w_H - T * sum w  op 0
                ans = ml_truthset(g, q['op'], F(0), world.bounds)
        else:
            if qty == 'nev':
                if not e.nev or e.nev[2] != q['event']:
                    raise ParseError('no expected-number fact')
                form_ = ml_const(e.nev[0] * e.nev[1])
            elif qty == 'loss' or qty == 'value':
                form_ = world.expected(e)
            elif qty == 'tec':
                form_ = ml_add(world.own(e), world.expected(e))
            else:
                form_ = world.quantity(e, 'risk')
            T = threshold_value(qty, q['val'], R)
            ans = ml_truthset(form_, q['op'], T, world.bounds)
        if len(ans) != 1:
            res.update(answer='UNDETERMINED', abstain=True)
            return res
        a = ans.pop()
        if q['pol'] < 0:
            a = not a
        res['answer'] = 1 if a else 0
        return res
    return solve_choice(row, doc, R, q, world, opts, abst, real, res)


def witness_point(bounds):
    return {v: lo for v, (lo, hi) in bounds.items()}


def ml_at(form, pt):
    v = F(0)
    for k, c in form.items():
        t = c
        for x in k:
            t *= pt[x]
        v += t
    return v


def tournament(forms, ids, best, bounds):
    """Pairwise tournament (SEM-12 ties by lower ID number). best: 'high' | 'low'.
    Step 1: witness answer a1 at one allowed point. Step 2: counter-witness search: a1 is the answer at every
    allowed point iff it beats every other option everywhere. Returns a1 or None (abstain)."""
    pt = witness_point(bounds)
    keys = list(forms)
    val = {k: ml_at(forms[k], pt) for k in keys}

    def beats(a, b, va, vb):
        if va == vb:
            return id_num(ids[a]) < id_num(ids[b])
        return va > vb if best == 'high' else va < vb
    a1 = keys[0]
    for k in keys[1:]:
        if beats(k, a1, val[k], val[a1]):
            a1 = k
    for b in keys:
        if b == a1:
            continue
        d = ml_add(forms[a1], ml_scale(forms[b], -1))
        lower = id_num(ids[a1]) < id_num(ids[b])
        if best == 'high':
            ok = ml_always(d, '>=' if lower else '>', F(0), bounds)
        else:
            ok = ml_always(d, '<=' if lower else '<', F(0), bounds)
        if not ok:
            return None
    return a1


def matrix_lookup(R, lik, imp):
    """Risk matrix lookup as SQL over level tables and the grid (row = likelihood, column = impact)."""
    db = sqlite3.connect(':memory:')
    db.executescript("""CREATE TABLE lvl(axis TEXT, name TEXT, lo_n INT, lo_d INT, lo_op TEXT, hi_n INT, hi_d INT, hi_op TEXT);
                        CREATE TABLE grid(lik TEXT, imp TEXT, rating TEXT);""")
    for axis, levels, kind in (('L', R.lik, 'chance'), ('I', R.imp, 'amount')):
        for name, rt in levels:
            lo, lop, hi, hop = parse_range(rt, kind)
            db.execute('INSERT INTO lvl VALUES (?,?,?,?,?,?,?,?)', (axis, name,
                       None if lo is None else lo.numerator, None if lo is None else lo.denominator, lop,
                       None if hi is None else hi.numerator, None if hi is None else hi.denominator, hop))
    for l, row in R.grid.items():
        for i, r in row.items():
            db.execute('INSERT INTO grid VALUES (?,?,?)', (l, i, r))
    q = """SELECT name FROM lvl WHERE axis=? AND
           (lo_n IS NULL OR (lo_op='>=' AND ?*lo_d >= lo_n*?) OR (lo_op='>' AND ?*lo_d > lo_n*?)) AND
           (hi_n IS NULL OR (hi_op='<' AND ?*hi_d < hi_n*?) OR (hi_op='<=' AND ?*hi_d <= hi_n*?))"""
    out = []
    for axis, v in (('L', lik), ('I', imp)):
        a, b = v.numerator, v.denominator
        rows = db.execute(q, (axis, a, b, a, b, a, b, a, b)).fetchall()
        if len(rows) != 1:
            raise ParseError('level lookup %s gave %d levels' % (axis, len(rows)))
        out.append(rows[0][0])
    r = db.execute('SELECT rating FROM grid WHERE lik=? AND imp=?', tuple(out)).fetchall()
    if len(r) != 1:
        raise ParseError('grid cell missing')
    return r[0][0]


def solve_choice(row, doc, R, q, world, opts, abst, real, res):
    form = q['form']
    openw = is_open(row)
    if form in ('BIN', 'PRED'):
        hyps, W = bayes_weights(doc, q['id'], world)
        tot = {}
        for h in hyps:
            tot = ml_add(tot, W[h])
        if form == 'PRED':
            if ml_vars(tot):
                raise ParseError('open-world PRED')
            cnt, N = int_counts(W)
            c_all = sum(cnt.values())
            if set(real) != set(hyps):
                raise ParseError('PRED options != hypotheses')
            probs = {h: F(cnt[h], c_all) for h in hyps}
            best = max(hyps, key=lambda h: cnt[h])
            if sum(1 for h in hyps if cnt[h] == cnt[best]) > 1:
                raise ParseError('PRED tie')
            res.update(answer=best, probs=probs)
            return res
        bins = [(o, parse_range(o, 'chance')) for o in real]
        if not ml_vars(tot) and not ml_vars(W[q['h']]):
            cnt, N = int_counts(W)
            v = F(cnt[q['h']], sum(cnt.values()))
            hit = [o for o, rg in bins if in_range(v, rg)]
            if len(hit) != 1:
                raise ParseError('posterior in %d bins' % len(hit))
            res['answer'] = hit[0]
            return res
        pt = witness_point(world.bounds)
        v = ml_at(W[q['h']], pt) / ml_at(tot, pt)
        hit = [(o, rg) for o, rg in bins if in_range(v, rg)]
        if len(hit) != 1:
            raise ParseError('witness posterior in %d bins' % len(hit))
        o1, (lo, lop, hi, hop) = hit[0]
        ok = True
        if lo is not None:
            ok &= ml_always(ml_add(W[q['h']], ml_scale(tot, -lo)), lop, F(0), world.bounds)
        if hi is not None:
            ok &= ml_always(ml_add(W[q['h']], ml_scale(tot, -hi)), hop, F(0), world.bounds)
        if ok:
            res['answer'] = o1
        else:
            res.update(answer=CBD_TXT if CBD_TXT in abst else 'CBD(not shown)', abstain=True)
        return res

    if form == 'TIER':
        P = PointsDB(R)
        ce = CaseEval(P, world, R, doc.ents.get(q['id']) or doc.ent(q['id']))
        tiers = ce.eval_all('tier')
        if len(tiers) != 1:
            raise ParseError('tier not determined')
        res['answer'] = tiers.pop()
        return res

    if form == 'MAT':
        e = doc.ents[q['id']]
        lik = ml_const_val(world.chance(e, R.lik_event))
        ik = R.imp_kind or ''
        m = re.fullmatch(r"loss if '(.+)' happens", ik)
        if m:
            o = e.outcomes[m.group(1)]
            imp = ml_const_val(world._a_ml(e, m.group(1), o))
        elif ik.startswith('expected loss'):
            imp = ml_const_val(world.expected(e))
        else:
            raise ParseError('impact definition? ' + ik)
        res['answer'] = matrix_lookup(R, lik, imp)
        return res

    if form in ('RANK-top', 'RANK-order', 'DEC', 'INV'):
        ids = {}
        forms = {}
        if form == 'RANK-order':
            items = [x.strip() for x in real[0].split(',')]
            for it in items:
                ids[it] = it
        elif form == 'DEC':
            byname = {e.name: e for e in doc.ents.values() if e.name}
            for o in real:
                if o not in byname:
                    raise ParseError('action option without action fact')
                ids[o] = byname[o].id
        else:
            for o in real:
                if not re.fullmatch(ID_RE, o):
                    raise ParseError('option is not an ID')
                ids[o] = o
        if form == 'INV':
            return solve_inv(doc, R, world, ids, abst, openw, res)
        qn = 'total expected cost' if form == 'DEC' else normkey_q(q['q'])
        if qn == 'score':
            P = PointsDB(R)
            for o, eid in ids.items():
                sc = CaseEval(P, world, R, doc.ents[eid]).eval_all('score')
                if len(sc) != 1:
                    raise ParseError('open-world score rank')
                forms[o] = ml_const(sc.pop())
        else:
            for o, eid in ids.items():
                if eid not in doc.ents:
                    raise ParseError('no facts for ' + eid)
                forms[o] = world.quantity(doc.ents[eid], qn)
        if form == 'RANK-order':
            if ml_vars(forms[next(iter(forms))]) or any(ml_vars(f) for f in forms.values()):
                raise ParseError('open-world RANK-order')
            vals = {k: ml_const_val(f) for k, f in forms.items()}
            led, den = ledger_compare(vals, ids)
            if len(set(led.values())) != len(led):
                raise ParseError('tie in RANK-order')
            order = sorted(led, key=lambda k: -led[k])
            txt = ', '.join(order)
            if txt in real:
                res['answer'] = txt
            elif NOTA_TXT in abst:
                res.update(answer=NOTA_TXT)
            else:
                raise ParseError('true order not shown and no NOTA')
            return res
        best = 'low' if form == 'DEC' or q.get('dir') == 'lowest' else 'high'
        a1 = tournament(forms, ids, best, world.bounds)
        if a1 is None:
            res.update(answer=CBD_TXT if CBD_TXT in abst else 'CBD(not shown)', abstain=True)
        else:
            res['answer'] = a1
        return res
    raise ParseError('form? ' + form)


def normkey_q(qtext):
    m = re.fullmatch(r"chance of '(.+)'", qtext)
    if m:
        return qtext
    return qtext


def solve_inv(doc, R, world, ids, abst, openw, res):
    """SEM-32: closed world 0 or 1 case meets (NOTA when none); open world shapes (i) and (ii) (CBD)."""
    P = PointsDB(R)
    status = {}
    for o, eid in ids.items():
        e = doc.ents.get(eid) or doc.ent(eid)
        ce = CaseEval(P, world, R, e)
        status[o] = ce.eval_all(('cond', P.inv_cid))
    sure = [o for o, s in status.items() if s == {True}]
    und = [o for o, s in status.items() if len(s) == 2]
    if not openw:
        if und:
            raise ParseError('undetermined case on a closed-world INV row')
        if len(sure) > 1:
            raise ParseError('closed INV: %d cases meet' % len(sure))
        res.update(answer=sure[0] if sure else NOTA_TXT, abstain=not sure)
        return res
    if len(sure) == 1 and not und:
        res['answer'] = sure[0]
    elif not sure and und:
        res.update(answer=CBD_TXT, abstain=True)
    else:
        res.update(answer='SHAPE(sure=%d,und=%d)' % (len(sure), len(und)), abstain=True)
    return res


# ---------------------------------------------------------------- runner: every row of the three outputs
def check_row(row, side):
    """Compare solver B with solver A's label (row gold), abstain decision and PRED gold_probs."""
    try:
        res = solve(row)
    except (ParseError, KeyError, ValueError, ZeroDivisionError, IndexError, TypeError, sqlite3.Error) as ex:
        return {'id': row['id'], 'status': 'PARSE_FAIL', 'b': None, 'a': row['gold'],
                'why': type(ex).__name__ + ': ' + str(ex)[:120]}
    gold = row['gold']
    b = res['answer']
    out = {'id': row['id'], 'form': res['form'], 'a': gold, 'b': b}
    a_abst = gold in (CBD_TXT, NOTA_TXT)
    b_abst = b in (CBD_TXT, NOTA_TXT) or (isinstance(b, str) and b.startswith(('CBD', 'SHAPE', 'UNDET')))
    if b != gold:
        out['status'] = 'LABEL_MISMATCH' if a_abst == b_abst else 'ABSTAIN_MISMATCH'
        return out
    if res.get('probs') is not None:
        ex = (side or {}).get('gold_probs_exact')
        gp = (row.get('meta') or {}).get('gold_probs')
        if not ex:
            out['status'] = 'PROBS_MISSING'
            return out
        mine = {k: v for k, v in res['probs'].items()}
        theirs = {k: F(v) for k, v in ex.items()}
        if mine != theirs:
            out['status'] = 'PROBS_MISMATCH'
            return out
        if gp is None or set(gp) != set(mine) or any(abs(float(mine[k]) - gp[k]) > 1e-12 for k in gp):
            out['status'] = 'PROBS_ROW_MISMATCH'
            return out
        out['probs_checked'] = True
    out['status'] = 'OK'
    return out


def run_file(base, name, resdir):
    side = {}
    sp = os.path.join(base, 'f8_controls_%s.jsonl' % name)
    if os.path.exists(sp):
        for l in open(sp):
            s = json.loads(l)
            side[s['id']] = s
    outp = os.path.join(resdir, 'results_%s.jsonl' % name)
    n = 0
    with open(outp, 'w') as fo:
        for l in open(os.path.join(base, name + '.jsonl')):
            row = json.loads(l)
            r = check_row(row, side.get(row['id']))
            r['file'] = name + '.jsonl'
            fo.write(json.dumps(r, default=str) + '\n')
            n += 1
    return outp, n


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(here, '..', 'out')
    resdir = os.path.join(here, '..', 'tmp', 'solverB')
    names = sys.argv[1:] or ['candidates_r1', 'qc_sample', 'mixdev_S5']
    for nm in names:
        p, n = run_file(base, nm, resdir)
        print(nm, n, p, flush=True)
