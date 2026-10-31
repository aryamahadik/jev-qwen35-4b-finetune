#!/usr/bin/env python3
"""F11 independent solver B (gate G2).

Written from the frozen G0 spec (c_src/F11/G0_SPEC.md, F11.G0.v7, sha256 3512efba...) and the row format only.
It imports nothing from c_src/F11/gen/ (solver A, renderer, parser) and was written without reading it.

Paradigm (G0 section 3, "Solvers"): the card TEXT is parsed (sections 7 and 10), then compiled into a decision tree by
recursive splitting over the attributes (nominal values, presence, numeric and date bands at the parsed cuts; integer
scaling for numbers, day ordinals for dates); each leaf is labelled by running the parsed rules in the order of the
Assign procedure (steps 1-5b). The report text is read by an independent frame reader (SEM-05/06/07/43/47/50) and the
item vector is evaluated by walking the tree. S7 / S5 codebook arm: the parsed card definitions are evaluated on the
annotation vector re-read by record_id from the pinned records file by this file's own loader.

Usage: python solver_b.py [--files candidates_r1,qc_sample,mixdev_S5] [--limit N]
Writes solverB/mismatch.json (ids, both answers, spec item; no row text).
"""
import bisect
import datetime as _dt
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
CSRC = os.path.dirname(FAM)
sys.path.insert(0, os.path.join(CSRC, 'common'))
import negcount  # shared tool (allowed; not generator code)

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

SCALE = 10 ** 6          # integer scaling for every number (precision <= 2 decimals, unit factors terminating)
NS = '<not stated>'      # value of an unstated attribute (SEM-03 / SEM-04)


class ParseError(Exception):
    pass


# ----------------------------------------------------------------------------------------------- text utilities
TOKRE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*")


def toks(s):
    return [t.lower() for t in TOKRE.findall(s)]


def toks_raw(s):
    return TOKRE.findall(s)


def norm_line(line):
    s = line.strip()
    while s.startswith('>'):
        s = s[1:].strip()
    s = re.sub(r'^(?:[-*+•·‣◦▪●⁃∙])\s+', '', s)
    return s.strip()


def find_seq(hay, needle, start=0):
    """positions of token sequence needle in hay (lists of lowercase tokens)."""
    out = []
    n = len(needle)
    if n == 0:
        return out
    for i in range(start, len(hay) - n + 1):
        if hay[i:i + n] == needle:
            out.append(i)
    return out


def strip_marks(s):
    return re.sub(r'\s*\[[^\]]*\]', '', s).strip()


# ----------------------------------------------------------------------------------------------- numbers and dates
MONTHS = {m.lower(): i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
     'November', 'December'], 1)}
NUMRE = r'(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?'
DATERE = (r'(\d{4})-(\d{2})-(\d{2})|(\d{1,2}) (' + '|'.join(m.capitalize() for m in MONTHS) + r') (\d{4})|('
          + '|'.join(m.capitalize() for m in MONTHS) + r') (\d{1,2}), (\d{4})')


def scaled(intpart, frac):
    ip = int(intpart.replace(',', ''))
    frac = frac or ''
    if len(frac) > 6:
        raise ParseError('too many decimals')
    return ip * SCALE + (int(frac.ljust(6, '0')) if frac else 0)


def parse_date_m(m):
    g = m.groups()
    if g[0]:
        y, mo, d = int(g[0]), int(g[1]), int(g[2])
    elif g[3]:
        d, mo, y = int(g[3]), MONTHS[g[4].lower()], int(g[5])
    else:
        mo, d, y = MONTHS[g[6].lower()], int(g[7]), int(g[8])
    return _dt.date(y, mo, d).toordinal()


def parse_date(s):
    m = re.fullmatch(DATERE, s.strip())
    if not m:
        raise ParseError('bad date %r' % s[:30])
    return parse_date_m(m)


# ----------------------------------------------------------------------------------------------- card model
class Attr:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind          # nominal | presence | numeric | date | set
        self.values = []          # nominal: value names in card order
        self.terms = {}           # phrase(lower) -> value (nominal) ; presence: phrase -> True
        self.units = []           # numeric unit forms
        self.cuts = set()         # numeric / date cuts (scaled ints / ordinals)


class Card:
    def __init__(self):
        self.attrs = {}           # name -> Attr
        self.codes = {}           # ID -> dict(name, parts, unless, onlyif, residual_of)
        self.code_order = []
        self.names = {}           # lower name -> ID
        self.notes = []           # (k1, k2, winner)
        self.default = None       # (attr, value)
        self.code_mode = None     # (attr, U)
        self.groups = []          # S3: dict(name, attr, vals, leaves)
        self.scope = []           # (src, cond, dst)
        self.entries = None       # S6: list of (conds, ID); last is catch-all (None, ID)
        self.key = None           # S5: n -> dict(cond, a, b, group)
        self.key_kind = None      # 'program' | 'codebook'
        self.short = None         # list of attribute names (short program card)
        self.fields = {}          # attr -> field name (S4)
        self.hedges = set()
        self.hypo = set()
        self.cues = []            # quoted absence cue forms
        self.s7 = None            # 'xed' | 'acsa' | 'atsa'
        self.s7codes = {}         # ID -> list of vectors
        self.kind = 'flat'        # flat | s3 | s6 | s5 | s7
        self.legend = {}
        self.records = False

    # value-word phrases: list of (token tuple, attr, value or marker)
    def build_lexicon(self):
        lex = []
        for a in self.attrs.values():
            if a.kind in ('nominal', 'set'):
                for v in a.values:
                    lex.append((tuple(toks(v)), a.name, v))
                for t, v in a.terms.items():
                    lex.append((tuple(toks(t)), a.name, v))
            elif a.kind == 'presence':
                for t in a.terms:
                    lex.append((tuple(toks(t)), a.name, True))
            elif a.kind in ('numeric', 'date'):
                lex.append((tuple(toks(a.name)), a.name, '#name'))
                for t in a.terms:
                    lex.append((tuple(toks(t)), a.name, '#name'))
        lex.sort(key=lambda x: -len(x[0]))
        self.lexicon = lex


ORD = r'^(?:(?:\(|R|Rule )?(\d+)[.):]?\s+)?'
ID_RE = r'(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{2,6}'


def parse_terms(s):
    return re.findall(r"'([^']+)'", s)


class CardParser:
    """Parses the card render (yes/no rows: `card`; choice rows: `instructions` + OPT_LINE lines)."""

    def __init__(self, text, opt_lines=None, bracket=None):
        self.text = text
        self.opt_lines = opt_lines or []
        self.bracket = bracket     # 'ID' | 'name' | None (masked)
        self.c = Card()

    # ---- conditions -------------------------------------------------------------------------------------
    def attr_prefix(self, s):
        sl = s.lower()
        best = None
        for a in self.c.attrs:
            al = a.lower()
            if sl.startswith(al + ' ') and (best is None or len(a) > len(best)):
                best = a
        return best

    def num(self, attr, s):
        m = re.fullmatch(NUMRE + r' (\S+)', s.strip())
        if not m:
            raise ParseError('bad number %r' % s[:40])
        unit = m.group(3)
        if unit.lower() not in [u.lower() for u in attr.units]:
            raise ParseError('unit %r not of %s' % (unit, attr.name))
        return scaled(m.group(1), m.group(2))

    def cond(self, s):
        s = s.strip().rstrip('.').strip()
        if s.startswith('either ') and s.endswith(', but not both'):
            inner = s[len('either '):-len(', but not both')]
            parts = self._split_or(inner)
            if not parts:
                raise ParseError('bad either %r' % s[:60])
            return ('xor', self.cond(parts[0]), self.cond(parts[1]))
        a = self.attr_prefix(s)
        if a is None:
            parts = self._split_or(s)
            if parts:
                return ('or', self.cond(parts[0]), self.cond(parts[1]))
            raise ParseError('no attribute in condition %r' % s[:60])
        rest = s[len(a) + 1:]
        try:
            return self._cond_attr(a, rest)
        except ParseError:
            parts = self._split_or(s)
            if parts:
                return ('or', self.cond(parts[0]), self.cond(parts[1]))
            raise

    def _split_or(self, s):
        for m in re.finditer(r' or ', s):
            l, r = s[:m.start()], s[m.end():]
            if l.endswith(' on') or r.startswith('after ') or r.startswith('more'):
                continue
            try:
                self.cond(l)
                self.cond(r)
                return (l, r)
            except ParseError:
                continue
        return None

    def _cond_attr(self, a, rest):
        A = self.c.attrs[a]
        if A.kind == 'nominal':
            if rest.startswith('is one of '):
                vals = [v.strip() for v in rest[len('is one of '):].split(', ')]
            elif rest.startswith('is '):
                vals = [rest[3:].strip()]
            else:
                raise ParseError('bad nominal cond %r' % rest[:40])
            for v in vals:
                if v not in A.values:
                    raise ParseError('unknown value %r of %s' % (v, a))
            return ('nom', a, frozenset(vals))
        if A.kind == 'presence':
            r = rest.strip()
            if r in ('present', 'is present'):
                return ('pres', a, True)
            if r in ('absent', 'is absent'):
                return ('pres', a, False)
            raise ParseError('bad presence cond %r' % r[:40])
        if A.kind == 'numeric':
            for op, kw in (('ge', 'at least '), ('ge', 'no fewer than '), ('lt', 'less than '), ('lt', 'fewer than '),
                           ('lt', 'under ')):
                if rest.startswith(kw):
                    v = self.num(A, rest[len(kw):])
                    A.cuts.add(v)
                    return ('num', a, op, v)
            raise ParseError('bad numeric cond %r' % rest[:40])
        if A.kind == 'date':
            if rest.startswith('on or after '):
                v = parse_date(rest[len('on or after '):])
                A.cuts.add(v)
                return ('num', a, 'ge', v)
            if rest.startswith('before '):
                v = parse_date(rest[len('before '):])
                A.cuts.add(v)
                return ('num', a, 'lt', v)
            raise ParseError('bad date cond %r' % rest[:40])
        raise ParseError('unsupported attribute kind %s' % A.kind)

    def parts(self, body):
        return [self.cond(p) for p in body.split(';') if p.strip()]

    # ---- glossary -----------------------------------------------------------------------------------------
    def glossary(self, lines):
        c = self.c
        for s in lines:
            m = re.match(r'^Glossary for (.+?): (.+)$', s)
            if m:
                A = Attr(m.group(1), 'nominal')
                for vm in re.finditer(r"\s*(.+?) \(shown by ((?:'[^']*'(?:, | or |,? or )?)+)\)(?:;|\.?$)", m.group(2)):
                    v = vm.group(1).strip()
                    A.values.append(v)
                    for t in parse_terms(vm.group(2)):
                        A.terms[t.lower()] = v
                if not A.values:
                    raise ParseError('empty glossary line')
                c.attrs[A.name] = A
                continue
            m = re.match(r"^(.+?) \(shown by (.+?)\): present or absent\.?$", s)
            if m:
                A = Attr(m.group(1), 'presence')
                for t in parse_terms(m.group(2)):
                    A.terms[t.lower()] = True
                c.attrs[A.name] = A
                continue
            m = re.match(r"^(.+?) \(shown by (.+?)\) is the date of (.+?)\.?$", s)
            if m:
                A = Attr(m.group(1), 'date')
                for t in parse_terms(m.group(2)):
                    A.terms[t.lower()] = '#name'
                c.attrs[A.name] = A
                continue
            m = re.match(r"^(.+?) \(shown by (.+?)\) in (\S+?)\.?$", s)
            if m:
                A = Attr(m.group(1), 'numeric')
                for t in parse_terms(m.group(2)):
                    A.terms[t.lower()] = '#name'
                A.units = m.group(3).split('/')
                c.attrs[A.name] = A
                continue

    # ---- main ---------------------------------------------------------------------------------------------
    def parse(self):
        c = self.c
        raw = self.text.split('\n')
        lines = [norm_line(l) for l in raw]
        joined = '\n'.join(lines)
        # reading rules: hedges, hypothetical marker, cue forms
        for s in lines:
            m = re.search(r"hedged \(([^)]*)\)", s)
            if m:
                c.hedges |= {x.lower() for x in parse_terms(m.group(1))}
            m = re.search(r"hypothetical \(([^)]*)\)", s)
            if m:
                c.hypo |= {x.lower() for x in parse_terms(m.group(1))}
            m = re.match(r"^For present-or-absent items, (.+?) mean absent\.", s)
            if m:
                c.cues = parse_terms(m.group(1))
        # S7 / codebook detection
        if re.search(r'Codes describe how human annotators judged|conditions describe how human annotators judged',
                     joined):
            return self.parse_s7(lines, joined)
        self.glossary(lines)
        # short program card
        for s in lines:
            m = re.match(r'^Names give (.+) in that order\.?$', s)
            if m:
                return self.parse_short(lines, m.group(1))
        for s in lines:
            if s.startswith('In a record, only the field'):
                c.records = True
            m = re.match(r'^In a record, (.+?) is recorded in field (\S+?)\.?$', s)
            if m:
                c.fields[m.group(1)] = m.group(2)
        if not c.attrs:
            raise ParseError('no glossary')
        if any(re.match(r'^\d+a .+ -> \S+$', s) for s in lines):
            return self.parse_key(lines)
        if any(re.search(r'\bIf .+ -> ' + ID_RE + r'$', s) for s in lines):
            return self.parse_entries(lines)
        if any(re.match(r'^Group .+ \(.+: .+\)', s) for s in lines):
            c.kind = 's3'
        self.parse_codes(raw, lines)
        self.parse_rules(lines)
        return c

    def code_line(self, s):
        """'ID NAME<sep> body' or 'ID<sep> body' (masked). Returns (id, name, body) or None."""
        # repair r1 (G2 mismatch F11qc-F11-S7-021-0024-0): a name never holds a separator character, so a body
        # holding ': ' (an 'Or:' alternative) after a ' | ' or ' = ' separator is not split at that colon
        m = re.match(r'^(' + ID_RE + r')(?: ([^:|=]+?))?\s*(?::|\s\||\s=)\s+(.+)$', s)
        if not m:
            return None
        return m.group(1), (m.group(2) or '').strip() or None, m.group(3)

    def is_def_body(self, body):
        b = strip_marks(body)
        if b.startswith('use only when'):
            return True
        try:
            self.cond(b.split(';')[0].split(', unless ')[0].split('. Use ')[0])
            return True
        except ParseError:
            return False

    def add_code(self, cid, name, body, group=None):
        c = self.c
        if cid in c.codes and c.codes[cid].get('parts') is not None:
            # a rule sentence below a table / repeated entry: attach rules only
            self.attach_rules(cid, body)
            return
        rec = {'name': name, 'parts': None, 'unless': None, 'onlyif': None, 'residual_of': None, 'group': group}
        c.codes[cid] = rec
        if cid not in c.code_order:
            c.code_order.append(cid)
        if name:
            c.names[name.lower()] = cid
        b = strip_marks(body)
        m = re.match(r'^use only when the .+? belongs to (.+?) and no other (.+?) code fits\.?$', b)
        if m:
            rec['residual_of'] = m.group(1)
            rec['parts'] = []
            return
        self.attach_rules(cid, b, base=True)

    def attach_rules(self, cid, b, base=False):
        rec = self.c.codes[cid]
        b = strip_marks(b)
        m = re.match(r'^(.+?), unless (.+?)\. If both (.+) and (.+?) hold, use (' + ID_RE + r')\.?$', b)
        if m:
            parts = self.parts(m.group(1))
            if rec['parts'] is None:
                rec['parts'] = parts
            elif rec['parts'] != parts and not rec.get('from_table'):
                raise ParseError('rule sentence parts differ from table row for %s' % cid)
            bcond = self.cond(m.group(2))
            if self.cond(m.group(4)) != bcond or (not rec.get('from_table') and self.parts(m.group(3)) != parts):
                raise ParseError('unless restatement mismatch')
            if rec['unless'] or rec['onlyif']:
                raise ParseError('two redirect rules on %s' % cid)
            rec['unless'] = (bcond, m.group(5))
            return
        m = re.match(r'^(.+?)\. Use (' + ID_RE + r') only if (.+?) also holds\. If (.+) holds but (.+?) does not, use ('
                     + ID_RE + r')\.?$', b)
        if m:
            if m.group(2) != cid:
                raise ParseError('only-if names another code')
            parts = self.parts(m.group(1))
            if rec['parts'] is None:
                rec['parts'] = parts
            elif rec['parts'] != parts and not rec.get('from_table'):
                raise ParseError('rule sentence parts differ from table row for %s' % cid)
            bcond = self.cond(m.group(3))
            if self.cond(m.group(5)) != bcond or (not rec.get('from_table') and self.parts(m.group(4)) != parts):
                raise ParseError('only-if restatement mismatch')
            if rec['unless'] or rec['onlyif']:
                raise ParseError('two redirect rules on %s' % cid)
            rec['onlyif'] = (bcond, m.group(6))
            return
        if not base:
            raise ParseError('unparsed rule sentence for %s: %r' % (cid, b[:60]))
        rec['parts'] = self.parts(b.rstrip('.'))

    def parse_codes(self, raw, lines):
        c = self.c
        cur_group = None
        i = 0
        n = len(lines)
        while i < n:
            s = lines[i]
            if not s or s.startswith('Example of') or 'shown by' in s or s.startswith('Glossary'):
                i += 1
                continue
            # S3 heading
            m = re.match(r'^Group (.+?) \((.+?): (.+?)\)(?: \[[^\]]*\])?$', s)
            if m:
                a = m.group(2)
                if a not in c.attrs:
                    raise ParseError('group attr unknown')
                vals = [v.strip() for v in m.group(3).split(', ')]
                for v in vals:
                    if v not in c.attrs[a].values:
                        raise ParseError('group value unknown')
                cur_group = {'name': m.group(1), 'attr': a, 'vals': frozenset(vals), 'leaves': []}
                c.groups.append(cur_group)
                i += 1
                continue
            # table?
            if self.table_header(lines, i):
                i = self.parse_table(raw, lines, i)
                continue
            cl = self.code_line(s)
            if cl and self.is_def_body(cl[2]):
                cid, name, body = cl
                self.add_code(cid, name, body, group=cur_group['name'] if cur_group else None)
                if cur_group is not None:
                    cur_group['leaves'].append(cid)
            i += 1
        # OPT_LINE codes (choice rows of one-line cards)
        for opt, other, body in self.opt_lines:
            if self.bracket == 'ID':
                cid, name = other, opt
            elif self.bracket == 'name':
                cid, name = opt, other
            else:
                cid, name = opt, None
            if not re.fullmatch(ID_RE, cid or ''):
                raise ParseError('option line without an ID')
            if cid in c.codes:
                raise ParseError('code listed twice')
            self.add_code(cid, name, body)
        if not c.codes:
            raise ParseError('no codes parsed')

    # ---- tables (SEM-48) ---------------------------------------------------------------------------------
    def table_header(self, lines, i):
        s = lines[i]
        cells = self.split_pipe(s) if '|' in s else None
        if cells and cells[0] in ('Code', 'ID') and len(cells) >= 3:
            return True
        if re.match(r'^(Code|ID)\s{2,}\S', s) and i + 1 < len(lines) and re.match(r'^=+(\s+=+)+$', lines[i + 1]):
            return True
        return False

    @staticmethod
    def split_pipe(s):
        t = s.strip()
        if t.startswith('|'):
            t = t[1:]
        if t.endswith('|'):
            t = t[:-1]
        return [x.strip() for x in t.split('|')]

    def parse_table(self, raw, lines, i):
        c = self.c
        s = lines[i]
        rows = []
        if '|' in s:
            header = self.split_pipe(s)
            j = i + 1
            while j < len(lines) and '|' in lines[j]:
                cells = self.split_pipe(lines[j])
                if not all(re.fullmatch(r':?-{2,}:?|=+', x) for x in cells):
                    rows.append(cells)
                j += 1
        else:
            # fixed width: spans from the ==== line (use the raw line with quote prefix removed consistently)
            sep = lines[i + 1]
            spans = [(m.start(), m.end()) for m in re.finditer(r'=+', sep)]

            def cut(line):
                out = []
                for k, (a, b) in enumerate(spans):
                    end = spans[k + 1][0] if k + 1 < len(spans) else len(line)
                    out.append(line[a:end].strip())
                return out
            header = cut(s)
            j = i + 2
            while j < len(lines) and lines[j].strip():
                rows.append(cut(lines[j]))
                j += 1
        cols = header
        has_name = len(cols) > 1 and cols[1] == 'Name'
        acols = cols[2:] if has_name else cols[1:]
        for a in acols:
            if a not in c.attrs:
                raise ParseError('table column %r is not an attribute' % a)
        for cells in rows:
            if len(cells) != len(cols):
                raise ParseError('table row width')
            cid = cells[0]
            name = strip_marks(cells[1]) if has_name else None
            parts = []
            for a, cell in zip(acols, cells[2:] if has_name else cells[1:]):
                p = self.cell(a, strip_marks(cell))
                if p is not None:
                    parts.append(p)
            rec = {'name': name, 'parts': parts, 'unless': None, 'onlyif': None, 'residual_of': None, 'group': None,
                   'from_table': True}
            if cid in c.codes:
                raise ParseError('table code twice')
            c.codes[cid] = rec
            c.code_order.append(cid)
            if name:
                c.names[name.lower()] = cid
        return j

    def cell(self, a, cell):
        A = self.c.attrs[a]
        if cell == 'any':
            return None
        if A.kind == 'nominal':
            vals = [v.strip() for v in cell.split(', ')]
            for v in vals:
                if v not in A.values:
                    raise ParseError('table value %r' % v)
            return ('nom', a, frozenset(vals))
        if A.kind == 'presence':
            if cell in ('present', 'absent'):
                return ('pres', a, cell == 'present')
            raise ParseError('presence cell %r' % cell)
        if A.kind == 'numeric':
            bands = []
            for b in cell.split(', '):
                m = re.fullmatch(r'under (.+)', b)
                if m:
                    hi = self.num(A, m.group(1))
                    A.cuts.add(hi)
                    bands.append((None, hi))
                    continue
                m = re.fullmatch(NUMRE + r' to under (.+)', b)
                if m:
                    hi = self.num(A, m.group(3))
                    unit = m.group(3).split(' ', 1)[1]
                    lo = self.num(A, (m.group(1) + ('.' + m.group(2) if m.group(2) else '')) + ' ' + unit)
                    A.cuts.update((lo, hi))
                    bands.append((lo, hi))
                    continue
                m = re.fullmatch(r'(.+) or more', b)
                if m:
                    lo = self.num(A, m.group(1))
                    A.cuts.add(lo)
                    bands.append((lo, None))
                    continue
                raise ParseError('band %r' % b)
            return ('bands', a, tuple(bands))
        if A.kind == 'date':
            m = re.fullmatch(r'on or after (.+); before (.+)', cell)
            if m:
                lo, hi = parse_date(m.group(1)), parse_date(m.group(2))
                A.cuts.update((lo, hi))
                return ('and', ('num', a, 'ge', lo), ('num', a, 'lt', hi))
            return self._cond_attr(a, cell)
        raise ParseError('cell kind')

    # ---- notes, missing rules, scope notes ----------------------------------------------------------------------
    def parse_rules(self, lines):
        c = self.c
        for s in lines:
            m = re.match(r'^If both (' + ID_RE + r') and (' + ID_RE + r') fit, use (' + ID_RE + r')\.$', s)
            if m:
                c.notes.append((m.group(1), m.group(2), m.group(3)))
                continue
            m = re.match(r'^If the .+? does not say (.+?), treat (.+?) as (.+?)\. ', s + ' ')
            if m:
                a = m.group(1)
                if a != m.group(2) or a not in c.attrs:
                    raise ParseError('default rule attr')
                v = m.group(3)
                A = c.attrs[a]
                if A.kind == 'nominal':
                    if v not in A.values:
                        raise ParseError('default value')
                elif A.kind == 'presence':
                    v = {'present': True, 'absent': False}[v]
                else:
                    raise ParseError('default on %s' % A.kind)
                c.default = (a, v)
                continue
            m = re.match(r'^If the .+? does not say (.+?), use (' + ID_RE + r')\. This rule comes before', s)
            if m:
                c.code_mode = (m.group(1), m.group(2))
                continue
            m = re.search(r'that would be in (.+?) but meet (.+?) belong to (.+?) instead\.', s)
            if m:
                c.scope.append((m.group(1), self.cond(m.group(2)), m.group(3)))
                continue
            if re.search(r'states more than one|corrects a detail|1 \S+ = |includes (any|all) of', s):
                raise ParseError('unsupported card rule (primary/correction/unit/set): %r' % s[:50])

    # ---- S6 entry list ---------------------------------------------------------------------------------------
    def parse_entries(self, lines):
        c = self.c
        c.kind = 's6'
        ents = []
        for s in lines:
            m = re.match(ORD + r'If (.+) -> (' + ID_RE + r')$', s)
            if m:
                ents.append((int(m.group(1)) if m.group(1) else len(ents) + 1,
                             [self.cond(x) for x in m.group(2).split(';')], m.group(3)))
                continue
            m = re.match(ORD + r'Otherwise -> (' + ID_RE + r')$', s)
            if m:
                ents.append((10 ** 6, None, m.group(2)))
                continue
            m = re.match(r'^(' + ID_RE + r'): (.+?)$', s)
            if m and not self.is_def_body(m.group(2)):
                c.legend[m.group(1)] = strip_marks(m.group(2))
        ords = [e[0] for e in ents]
        if ords != sorted(ords):
            raise ParseError('S6 entries out of order')
        if not ents or ents[-1][1] is not None:
            raise ParseError('S6 without catch-all last')
        c.entries = [(e[1], e[2]) for e in ents]
        for _, cid in c.entries:
            if cid not in c.codes:
                c.codes[cid] = {'name': c.legend.get(cid)}
                c.code_order.append(cid)
        for cid, nm in c.legend.items():
            if cid not in c.codes:
                raise ParseError('legend code without entry')
            c.names[nm.lower()] = cid
        return c

    # ---- S5 key -------------------------------------------------------------------------------------------
    def parse_key(self, lines, condf=None):
        c = self.c
        c.kind = 's5'
        condf = condf or self.cond
        key = {}
        nonempty = [s for s in lines if s]
        for idx, s in enumerate(nonempty):
            m = re.match(r'^(\d+)([ab]) (.+?) -> (\S+)$', s)
            if m:
                n = int(m.group(1))
                d = key.setdefault(n, {'group': None})
                if m.group(2) == 'a':
                    d['cond'] = condf(m.group(3))
                    d['a'] = m.group(4)
                else:
                    if m.group(3) != 'otherwise':
                        raise ParseError('b-branch not otherwise')
                    d['b'] = m.group(4)
                continue
            m = re.match(r'^(\d+)\. (.+?)$', s)
            if m and idx + 1 < len(nonempty) and nonempty[idx + 1].startswith(m.group(1) + 'a '):
                key.setdefault(int(m.group(1)), {'group': None})['group'] = strip_marks(m.group(2))
                continue
            m = re.match(r'^(' + ID_RE + r'): (.+?)$', s)
            if m:
                c.legend[m.group(1)] = strip_marks(m.group(2))
        for n, d in key.items():
            if 'cond' not in d or 'b' not in d:
                raise ParseError('incomplete couplet %d' % n)
        c.key = key
        targets = set()
        for d in key.values():
            for t in (d['a'], d['b']):
                if not t.isdigit():
                    targets.add(t)
                elif int(t) not in key:
                    raise ParseError('dangling couplet')
        for t in targets:
            c.codes[t] = {'name': c.legend.get(t)}
            c.code_order.append(t)
        for cid, nm in c.legend.items():
            c.names[nm.lower()] = cid
        if self.opt_lines:
            raise ParseError('option lines on a key card')
        return c

    # ---- short program card ------------------------------------------------------------------------------
    def parse_short(self, lines, attrspec):
        c = self.c
        c.kind = 'flat'
        names = [x.strip() for x in re.split(r', | and ', attrspec)]
        c.short = names
        for a in names:
            c.attrs[a] = Attr(a, 'nominal')
        started = False
        for s in lines:
            if s.startswith('Names give'):
                started = True
                continue
            if not started or not s:
                continue
            if ' / ' not in s:
                if c.codes:
                    break
                continue
            nm = strip_marks(s)
            vals = [v.strip() for v in nm.split(' / ')]
            if len(vals) != len(names):
                raise ParseError('short name arity')
            cid = nm
            c.codes[cid] = {'name': nm, 'parts': [('nom', a, frozenset([v])) for a, v in zip(names, vals)],
                            'unless': None, 'onlyif': None, 'residual_of': None, 'group': None}
            c.code_order.append(cid)
            c.names[nm.lower()] = cid
            for a, v in zip(names, vals):
                if v not in c.attrs[a].values:
                    c.attrs[a].values.append(v)
        if not c.codes:
            raise ParseError('short card without codes')
        return c

    # ---- S7 codebooks and S5 codebook-arm keys ---------------------------------------------------------------
    def parse_s7(self, lines, joined):
        c = self.c
        c.kind = 's7'
        if 'named aspect' in joined:
            c.s7 = 'acsa'
        elif 'named target' in joined:
            c.s7 = 'atsa'
        else:
            c.s7 = 'xed'
        if any(re.match(r'^\d+a .+ -> \S+$', s) for s in lines):
            c.key_kind = 'codebook'
            k = self.parse_key(lines, condf=self.s7cond)
            c.kind = 's5'
            return k
        for s in lines:
            cl = self.code_line(s)
            if cl:
                cid, name, body = cl
                vecs = self.s7body(strip_marks(body))
                if vecs is not None:
                    self.add_s7(cid, name, vecs)
                    continue
            nm = strip_marks(s)
            vecs = self.s7short(nm)
            if vecs is not None:
                self.add_s7(nm, nm, vecs)
        for opt, other, body in self.opt_lines:
            if self.bracket == 'ID':
                cid, name = other, opt
            elif self.bracket == 'name':
                cid, name = opt, other
            else:
                cid, name = opt, None
            vecs = self.s7body(strip_marks(body))
            if vecs is None or cid in c.s7codes:
                raise ParseError('bad S7 option line')
            self.add_s7(cid, name, vecs)
        if not c.s7codes:
            raise ParseError('no S7 codes')
        return c

    def add_s7(self, cid, name, vecs):
        c = self.c
        if cid in c.s7codes:
            raise ParseError('duplicate S7 code')
        c.s7codes[cid] = vecs
        c.codes[cid] = {'name': name}
        c.code_order.append(cid)
        if name:
            c.names[name.lower()] = cid

    @staticmethod
    def labelset(s):
        s = s.strip().rstrip('.')
        items = re.split(r', | and ', s)
        return frozenset(x.strip().lower() for x in items if x.strip())

    def s7body(self, b):
        b = b.rstrip('.').strip()
        m = re.match(r'^the labels are (.+)$', b)
        if m:
            out = []
            for alt in re.split(r', or |\. Or: the labels are ', m.group(1)):
                alt = alt.strip()
                if alt.endswith(' alone'):
                    out.append(frozenset([alt[:-len(' alone')].strip().lower()]))
                else:
                    out.append(self.labelset(alt))
            return out
        if b.startswith('the named '):
            out = []
            for alt in b.split('. Or: '):
                m = re.match(r'^the named (?:aspect|target) is (\w+); the other (?:aspects|targets) are (.+)$', alt.strip())
                if not m:
                    return None
                out.append((m.group(1).lower(), self.labelset(m.group(2))))
            return out
        return None

    def s7short(self, nm):
        m = re.match(r'^named (\w+) with others (.+)$', nm)
        if m:
            return [(m.group(1).lower(), self.labelset(m.group(2)))]
        if self.c.s7 == 'xed' and re.fullmatch(r'[A-Z][a-z]+(?: / [A-Z][a-z]+)*', nm):
            labs = frozenset(x.strip().lower() for x in nm.split(' / '))
            if labs <= XED_LABELS:
                return [labs]
        return None

    def s7cond(self, s):
        s = s.strip().rstrip('.')
        m = re.match(r'^the labels(?: of the other (?:targets|aspects))? include (any|all) of (.+)$', s)
        if m:
            where = 'others' if ' of the other ' in s else 'labels'
            items = frozenset(x.strip().lower() for x in re.split(r', | or | and ', m.group(2)) if x.strip())
            return ('s7set', where, m.group(1), items)
        m = re.match(r'^the named (?:target|aspect) is one of (.+)$', s)
        if m:
            return ('s7named', frozenset(x.strip().lower() for x in re.split(r', | or ', m.group(1))))
        m = re.match(r'^the named (?:target|aspect) is (\w+)$', s)
        if m:
            return ('s7named', frozenset([m.group(1).lower()]))
        raise ParseError('bad codebook key condition %r' % s[:50])


XED_LABELS = frozenset(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust'])


# ----------------------------------------------------------------------------------------------- rule evaluation
def ev(cond, vec):
    k = cond[0]
    if k == 'nom':
        return vec[cond[1]] in cond[2]
    if k == 'pres':
        return vec[cond[1]] is cond[2]
    if k == 'num':
        x = vec[cond[1]]
        return x >= cond[3] if cond[2] == 'ge' else x < cond[3]
    if k == 'bands':
        x = vec[cond[1]]
        return any((lo is None or x >= lo) and (hi is None or x < hi) for lo, hi in cond[2])
    if k == 'or':
        return ev(cond[1], vec) or ev(cond[2], vec)
    if k == 'xor':
        return ev(cond[1], vec) != ev(cond[2], vec)
    if k == 'and':
        return ev(cond[1], vec) and ev(cond[2], vec)
    if k == 's7set':
        labs = vec['labels'] if cond[1] == 'labels' else vec['others']
        return bool(labs & cond[3]) if cond[2] == 'any' else cond[3] <= labs
    if k == 's7named':
        return vec['named'] in cond[1]
    raise ParseError('cond kind %s' % k)


def in_groups(card, vec):
    """S3 membership (SEM-33, SEM-49): set of group names the report belongs to (one level)."""
    out = set()
    for G in card.groups:
        g = vec[G['attr']]
        own = g in G['vals'] and not any(src == G['name'] and ev(cnd, vec) for src, cnd, dst in card.scope)
        moved_in = False
        for src, cnd, dst in card.scope:
            if dst == G['name'] and ev(cnd, vec):
                S = [x for x in card.groups if x['name'] == src]
                if not S:
                    raise ParseError('scope source unknown')
                if g in S[0]['vals']:
                    moved_in = True
        if own or moved_in:
            out.add(G['name'])
    return out


def assign_rules(card, vec):
    """Assign procedure (G0 section 3) on a full vector. Returns (code, trace) or raises."""
    tr = []
    if card.kind == 's6':
        for i, (conds, cid) in enumerate(card.entries):
            if conds is None or all(ev(x, vec) for x in conds):
                tr.append('S6 entry %d' % (i + 1) if conds is not None else 'S6 catch-all')
                return cid, tr
        raise ParseError('S6 no entry')
    if card.kind == 's5':
        n = 1
        seen = set()
        while True:
            if n in seen:
                raise ParseError('key loop')
            seen.add(n)
            d = card.key[n]
            t = d['a'] if ev(d['cond'], vec) else d['b']
            if t.isdigit():
                n = int(t)
                continue
            tr.append('S5 key walk')
            return t, tr
    # step 1: code mode
    if card.code_mode and vec.get(card.code_mode[0]) == NS:
        return card.code_mode[1], ['SEM-04']
    gates = None
    if card.kind == 's3':
        gates = in_groups(card, vec)
    F = []
    fit_self = {}
    for cid in card.code_order:
        r = card.codes[cid]
        if r.get('residual_of'):
            continue
        if gates is not None and r.get('group') not in gates:
            continue
        if r['parts'] is None:
            raise ParseError('code without definition %s' % cid)
        d = all(ev(p, vec) for p in r['parts'])
        if not d:
            continue
        if r['unless']:
            if ev(r['unless'][0], vec):
                F.append(r['unless'][1])
                tr.append('SEM-14 unless %s->%s' % (cid, r['unless'][1]))
            else:
                F.append(cid)
        elif r['onlyif']:
            if ev(r['onlyif'][0], vec):
                F.append(cid)
            else:
                F.append(r['onlyif'][1])
                tr.append('SEM-15 only-if %s->%s' % (cid, r['onlyif'][1]))
        else:
            F.append(cid)
    if card.kind == 's3':
        for cid in card.code_order:
            r = card.codes[cid]
            G = r.get('residual_of')
            if not G:
                continue
            if G in gates:
                leaves = [x['leaves'] for x in card.groups if x['name'] == G][0]
                if not any(f in leaves and not card.codes[f].get('residual_of') for f in F):
                    F.append(cid)
                    tr.append('SEM-32 residual')
    F = list(dict.fromkeys(F))
    if len(F) == 1:
        return F[0], tr
    if len(F) == 2:
        ns = [n for n in card.notes if {n[0], n[1]} == set(F)]
        if len(ns) != 1:
            raise ParseError('two codes fit without one note')
        tr.append('SEM-13 note')
        return ns[0][2], tr
    raise ParseError('|F|=%d' % len(F))


# ----------------------------------------------------------------------------------------------- decision tree
class Tree:
    """Recursive split over attributes; numeric/date attributes split at the parsed cuts (lower-closed bands)."""

    def __init__(self, card):
        self.card = card
        self.order = []
        self.dom = {}
        for a, A in card.attrs.items():
            if A.kind == 'nominal':
                d = list(A.values)
            elif A.kind == 'presence':
                d = [True, False]
            elif A.kind in ('numeric', 'date'):
                cuts = sorted(A.cuts)
                d = ([cuts[0] - 1] + cuts) if cuts else [0]
            else:
                raise ParseError('tree kind')
            if card.code_mode and card.code_mode[0] == a:
                d = d + [NS]
            self.order.append(a)
            self.dom[a] = d
        self.cuts = {a: sorted(A.cuts) for a, A in card.attrs.items() if A.kind in ('numeric', 'date')}
        self.nleaves = 0
        self.root = self.build(0, {})

    def build(self, i, part):
        if i == len(self.order):
            self.nleaves += 1
            try:
                return ('leaf', assign_rules(self.card, part))
            except ParseError as e:
                return ('leaf', ('!INVALID', [str(e)]))
        a = self.order[i]
        kids = {}
        for v in self.dom[a]:
            part[a] = v
            kids[v] = self.build(i + 1, part)
        del part[a]
        first = next(iter(kids.values()))
        if first[0] == 'leaf' and all(k == first for k in kids.values()):
            return first
        return ('node', a, kids)

    def key_of(self, a, x):
        if x == NS:
            return NS
        if a in self.cuts:
            cuts = self.cuts[a]
            if not cuts:
                return 0
            k = bisect.bisect_right(cuts, x)
            return cuts[0] - 1 if k == 0 else cuts[k - 1]
        return x

    def eval(self, vec):
        n = self.root
        while n[0] == 'node':
            a = n[1]
            if a not in vec:
                raise ParseError('vector lacks %s' % a)
            k = self.key_of(a, vec[a])
            if k not in n[2]:
                raise ParseError('value %r outside domain of %s' % (vec[a], a))
            n = n[2][k]
        code, tr = n[1]
        if code == '!INVALID':
            raise ParseError('tree leaf invalid: ' + tr[0])
        return code, tr


# ----------------------------------------------------------------------------------------------- report reading
HEDGE = {'believed', 'believes', 'believe', 'thought', 'thinks', 'think', 'suspected', 'suspects', 'suspect',
         'assumed', 'assumes', 'assume', 'claimed', 'claims', 'claim', 'alleged', 'alleges', 'guessed', 'guesses',
         'felt', 'feels', 'supposed', 'supposes', 'reportedly', 'apparently', 'supposedly', 'allegedly', 'seemingly',
         'presumably', 'probably', 'possibly', 'perhaps', 'maybe', 'may', 'might', 'could', 'must', 'seems', 'seemed',
         'appears', 'appeared', 'likely', 'doubted', 'doubts', 'speculated', 'imagined', 'expected', 'hoped',
         'feared', 'insisted', 'argued', 'asserted', 'contended', 'maintained'}
HYPO = {'hypothetically', 'would', 'if', 'suppose', 'supposing', 'imagine', 'were'}
EARLIER = {'earlier', 'prior', 'previous', 'previously', 'last', 'before', 'formerly', 'once', 'was', 'had', 'former',
           'ago', 'past', 'used'}
LATER = {'later', 'next', 'future', 'will', 'upcoming', 'subsequent', 'soon', 'tomorrow', 'eventually', 'shall',
         'planned', 'proposed'}
GENERAL = {'all', 'every', 'generally', 'typically', 'usually', 'common', 'commonly', 'most', 'always', 'often',
           'normally', 'sometimes', 'across'}
BANNED_IN_FOCAL = {'according', 'per', 'view'}
ATTRIB = re.compile(r"^(?:It (?:was|is|has been) (?:said|stated|reported|recorded|written|noted) that |"
                    r"(?:[A-Z][^\W\d_]*(?:[ '\-][A-Z][^\W\d_]*)*|The [a-z][a-z ]*?) "
                    r"(?:said|stated|reported|recorded|wrote|says|states|reports|records|writes) that )")
SUBJ_RE = re.compile(r"\b([A-Z][A-Za-z]{1,12}(?: [A-Z][A-Za-z]{1,12})?)\s*:\s*([A-Z]{1,4}-\d{2,6})\b")


def split_sentences(text):
    out = []
    for line in text.split('\n'):
        for s in re.split(r'(?<=[.?!])\s+', line):
            if s.strip():
                out.append(s.strip())
    return out


def find_subject(text):
    m = SUBJ_RE.search(text)
    if not m:
        raise ParseError('no subject line')
    return m.group(2)


def classify(sentence, card, foc):
    """Frame of a value-word sentence about `foc`: returns 'focal' or a non-counting kind."""
    s = sentence
    m = ATTRIB.match(s)
    attrib = False
    if m:
        s = s[m.end():]
        attrib = True
    raw = toks_raw(s)
    low = [t.lower() for t in raw]
    # mask value words, attribute names and the designator so they cannot act as markers
    mask = [False] * len(low)
    phrases = [p for p, _, _ in card.lexicon] + [tuple(toks(a)) for a in card.attrs] + [tuple(toks(foc))]
    for p in sorted(set(phrases), key=len, reverse=True):
        for i in find_seq(low, list(p)):
            if not any(mask[i:i + len(p)]):
                for j in range(i, i + len(p)):
                    mask[j] = True
    if attrib:
        pre = toks(sentence[:m.end()])
        if any(t in HEDGE for t in pre):
            return 'hedged'
    for i, (t, tl) in enumerate(zip(raw, low)):
        if mask[i]:
            continue
        if i > 0 and t[:1].isupper():
            continue  # capitalised mid-sentence words are names, not markers
        if tl in card.hedges or tl in HEDGE:
            return 'hedged'
        if tl in card.hypo or tl in HYPO:
            return 'hypothetical'
        if tl in EARLIER:
            return 'earlier'
        if tl in LATER:
            return 'later'
        if tl in GENERAL:
            return 'general'
        if tl in BANNED_IN_FOCAL:
            raise ParseError('prepositional attribution in value-word sentence')
    return 'focal'


def read_prose(text, card, foc):
    """Returns (vector of stated attributes, frame log)."""
    vec = {}
    log = []
    ftok = toks(foc)
    for sent in split_sentences(text):
        low = toks(sent)
        hits = []
        used = [False] * len(low)
        for p, a, v in card.lexicon:
            for i in find_seq(low, list(p)):
                if not any(used[i:i + len(p)]):
                    for j in range(i, i + len(p)):
                        used[j] = True
                    hits.append((i, a, v))
        if not hits:
            continue
        if not find_seq(low, ftok):
            log.append(('other_or_general', sorted({a for _, a, _ in hits})))
            continue
        others = {d for d in re.findall(r'\b[A-Z]{1,4}-\d{2,6}\b', sent) if d != foc}
        if others:
            raise ParseError('value-word sentence names the focal entity and another entity')
        kind = classify(sent, card, foc)
        if kind != 'focal':
            log.append((kind, sorted({a for _, a, _ in hits})))
            continue
        neg = negcount.k_all(sent) >= 1
        attrs_here = {a for _, a, _ in hits}
        for a in attrs_here:
            A = card.attrs[a]
            vals = {v for _, aa, v in hits if aa == a}
            if A.kind == 'nominal':
                if neg:
                    log.append(('negated', [a]))
                    continue
                if len(vals) != 1:
                    raise ParseError('two values of %s in one sentence' % a)
                val = vals.pop()
            elif A.kind == 'presence':
                val = not neg
            elif A.kind == 'numeric':
                if neg:
                    log.append(('negated', [a]))
                    continue
                units = '|'.join(re.escape(u) for u in sorted(A.units, key=len, reverse=True))
                nums = re.findall(r'(?<![\w.])' + NUMRE + r' (?:' + units + r')(?![\w-])', sent, flags=re.I)
                if len(nums) != 1:
                    raise ParseError('%d numbers for %s in one sentence' % (len(nums), a))
                val = scaled(nums[0][0], nums[0][1])
            elif A.kind == 'date':
                if neg:
                    log.append(('negated', [a]))
                    continue
                ds = list(re.finditer(DATERE, sent))
                if len(ds) != 1:
                    raise ParseError('%d dates for %s in one sentence' % (len(ds), a))
                val = parse_date_m(ds[0])
            else:
                raise ParseError('unsupported kind in report')
            if a in vec and vec[a] != val:
                raise ParseError('conflicting focal values of %s' % a)
            vec[a] = val
            log.append(('focal', [a]))
    return vec, log


# ---- records (SEM-50) --------------------------------------------------------------------------------------
def _scalar(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (_dt.date, _dt.datetime)):
        return v.isoformat()[:10]
    if isinstance(v, list):
        return v
    return str(v)


def _dict_records(obj, out):
    if isinstance(obj, dict):
        flat = {k: _scalar(v) for k, v in obj.items() if not isinstance(v, (dict,)) and
                not (isinstance(v, list) and v and isinstance(v[0], dict))}
        if flat:
            out.append(flat)
        for v in obj.values():
            if isinstance(v, (dict, list)):
                _dict_records(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _dict_records(v, out)


def parse_records(text):
    """Container-agnostic record reader. Returns a list of dicts field -> value string (or None for null)."""
    import csv
    import io
    body = re.sub(r'^\s*```.*$', '', text, flags=re.M)
    recs = []
    i = body.find('{')
    if i >= 0:  # JSON
        try:
            obj, _ = json.JSONDecoder().raw_decode(body[i:])
            _dict_records(obj, recs)
            if recs:
                return recs
        except ValueError:
            pass
    lines = [l.rstrip() for l in body.split('\n') if l.strip()]
    kvre = re.compile(r'^\s*-?\s*([A-Za-z_][\w.]*)\s*(?:\.{2,}|:|=)\s*(.*)$')
    pipe = [l for l in lines if '|' in l]
    if len(pipe) >= 3 and len(pipe) >= len(lines) - 2:  # pipe table (2-column key/value or one row per record)
        rows = []
        for l in pipe:
            t = l.strip()
            t = t[1:] if t.startswith('|') else t
            t = t[:-1] if t.endswith('|') else t
            cells = [x.strip() for x in t.split('|')]
            if all(re.fullmatch(r':?-{2,}:?|=+', x) for x in cells):
                continue
            rows.append(cells)
        return _table_records(rows)
    dotted = any(re.match(r'^\s*\w+ \.{2,} ', l) for l in lines)
    kvs = [l for l in lines if kvre.match(l)]
    if len(kvs) >= 3 and len(kvs) >= len(lines) - 2:
        if yaml is not None and not dotted:
            try:
                obj = yaml.safe_load(body)
                if isinstance(obj, (dict, list)):
                    _dict_records(obj, recs)
                    recs = [r for r in recs if len(r) >= 3]
                    if recs:
                        return recs
            except Exception:
                pass
        out, cur = [], {}
        for l in body.split('\n'):
            if not l.strip():
                if cur:
                    out.append(cur)
                    cur = {}
                continue
            m = kvre.match(l)
            if not m:
                continue
            k, v = m.group(1), m.group(2).strip()
            if k in cur:
                out.append(cur)
                cur = {}
            cur[k] = v
        if cur:
            out.append(cur)
        return [r for r in out if len(r) >= 3]
    if yaml is not None and not dotted:
        try:
            obj = yaml.safe_load(body)
            if isinstance(obj, (dict, list)):
                _dict_records(obj, recs)
                recs = [r for r in recs if len(r) >= 3]
                if recs:
                    return recs
        except Exception:
            pass
    for delim in (';', ',', '\t'):  # delimited tables
        cand = [l.strip() for l in lines if delim in l]
        if len(cand) >= 3 and len(cand) >= len(lines) - 2:
            head = next(csv.reader(io.StringIO(cand[0]), delimiter=delim))
            if len(head) == 2:
                rows = [[x.strip() for x in l.split(delim, 1)] for l in cand]
            else:
                rows = [[x.strip() for x in r] for r in csv.reader(io.StringIO('\n'.join(cand)), delimiter=delim)]
            return _table_records(rows)
    raise ParseError('record container not recognised')


HEADER_WORDS = {'field', 'attribute', 'key', 'name', 'setting', 'value'}


def _table_records(rows):
    if not rows:
        raise ParseError('empty record table')
    head = rows[0]
    if len(head) == 2 and all(len(r) == 2 for r in rows):
        body = rows[1:] if head[0].lower() in HEADER_WORDS else rows
        rec = {}
        for k, v in body:
            if k in rec:
                raise ParseError('repeated field in a key/value table')
            rec[k] = v
        return [rec]
    if any(len(r) != len(head) for r in rows):
        raise ParseError('ragged record table')
    return [dict(zip(head, r)) for r in rows[1:]]


def read_record(text, card, foc):
    recs = parse_records(text)
    focs = [r for r in recs if any(isinstance(v, str) and v.strip() == foc for v in r.values())]
    if len(focs) != 1:
        raise ParseError('%d focal records' % len(focs))
    rec = {k.strip().strip('"\''): v for k, v in focs[0].items()}
    vec = {}
    for a, A in card.attrs.items():
        f = card.fields.get(a, a)
        if f not in rec:
            alts = [k for k in rec if k.lower() == f.lower() or k.lower() == f.lower().replace(' ', '_')]
            if len(alts) != 1:
                raise ParseError('record lacks field for %s' % a)
            f = alts[0]
        v = rec[f]
        if 'corrected_' + f in rec:
            raise ParseError('corrected field (unsupported)')
        if v is None or (isinstance(v, str) and v.strip().lower() in ('null', 'unknown', 'not recorded')):
            continue  # not stated
        if isinstance(v, list):
            raise ParseError('list value on a non-set field')
        v = v.strip().strip('"')
        vl = v.lower()
        if A.kind == 'nominal':
            if v in A.values:
                vec[a] = v
            elif vl in A.terms:
                vec[a] = A.terms[vl]
            else:
                hit = [x for x in A.values if x.lower() == vl]
                if len(hit) != 1:
                    raise ParseError('field value %r is no value of %s' % (v[:20], a))
                vec[a] = hit[0]
        elif A.kind == 'presence':
            if vl in ('yes', 'true') or vl in A.terms:
                vec[a] = True
            elif vl in ('no', 'false', 'none'):
                vec[a] = False
            else:
                raise ParseError('presence field value %r' % v[:20])
        elif A.kind == 'numeric':
            m = re.fullmatch(NUMRE + r' (\S+)', v)
            if not m or m.group(3).lower() not in [u.lower() for u in A.units]:
                raise ParseError('numeric field without its unit')
            vec[a] = scaled(m.group(1), m.group(2))
        elif A.kind == 'date':
            vec[a] = parse_date(v)
        else:
            raise ParseError('unsupported record kind')
    return vec


def complete(card, vec):
    """Missing-attribute rules (Assign steps 1-2)."""
    out = dict(vec)
    for a in card.attrs:
        if a in out:
            continue
        if card.code_mode and card.code_mode[0] == a:
            out[a] = NS
        elif card.default and card.default[0] == a:
            out[a] = card.default[1]
        else:
            raise ParseError('attribute %s not stated and no missing rule' % a)
    return out


def read_report(text, card):
    foc = find_subject(text)
    if card.records:
        vec = read_record(text, card, foc)
        mode = 'record'
    else:
        vec, _ = read_prose(text, card, foc)
        mode = 'prose'
    return complete(card, vec), mode


# ----------------------------------------------------------------------------------------------- S7 records
class S7Store:
    FILES = {'xed': 'xed.jsonl', 'acsa': 'mams_acsa.jsonl', 'atsa': 'mams_atsa.jsonl'}
    PINNED = {'xed': '4318fc0033ae18b2e703348a81670551912ca46cc8be71fe46e1911a8598a097',
              'acsa': 'b91f1f8d46e88c7c302e49a7dba746b14420a2dc94bb42434db3ef44944b0188',
              'atsa': 'a1f10522db1f55d1babfa9cc24212a6e9a065f063efa4fabeeb7687b9724a8be'}

    def __init__(self):
        self.db = {}
        self.sha = {}
        d = os.path.join(CSRC, 'formats', 'formats-2', 'records')
        for k, f in self.FILES.items():
            p = os.path.join(d, f)
            data = open(p, 'rb').read()
            self.sha[k] = hashlib.sha256(data).hexdigest()
            idx = {}
            for line in data.decode('utf-8').split('\n'):
                if line.strip():
                    r = json.loads(line)
                    idx[str(r['record_id'])] = r
            self.db[k] = idx

    def vector(self, scheme, rid, named):
        r = self.db[scheme].get(str(rid))
        if r is None:
            raise ParseError('record not found')
        ann = r['ann']
        if scheme == 'xed':
            return {'labels': frozenset(x.lower() for x in ann['emotions'])}, r['text']
        if scheme == 'acsa':
            pairs = [(a.lower(), p.lower()) for a, p in ann['aspects']]
        else:
            pairs = [(t['term'].lower(), t['polarity'].lower()) for t in ann['terms']]
        hit = [p for a, p in pairs if a == named.lower()]
        if len(hit) != 1:
            raise ParseError('named %s found %d times' % (scheme, len(hit)))
        others = [p for a, p in pairs if a != named.lower()]
        return {'named': hit[0], 'others': frozenset(others), 'labels': frozenset(others)}, r['text']


def wsnorm(s):
    return re.sub(r'\s+', ' ', s).strip()


# ----------------------------------------------------------------------------------------------- questions
QPATS = [
    ('yn_code', 2, re.compile(r"Is it not the case that this (.+?) does not get code (.+?)(?: for the (aspect|target) '(.+?)')?\?")),
    ('yn_code', 1, re.compile(r"Is it true that this (.+?) does not get code (.+?)(?: for the (aspect|target) '(.+?)')?\?")),
    ('yn_code', 0, re.compile(r"[Dd]oes this (.+?) get code (.+?)(?: for the (aspect|target) '(.+?)')?\?")),
    ('yn_group', 2, re.compile(r"Is it not the case that this (.+?) does not belong to (.+?)\?")),
    ('yn_group', 1, re.compile(r"Is it true that this (.+?) does not belong to (.+?)\?")),
    ('yn_group', 0, re.compile(r"Does this (.+?) belong to (.+?)\?")),
    ('inverted', 0, re.compile(r"Which of these (.+?) gets code (.+?)\?")),
    ('coarse', 0, re.compile(r"Which group does this (.+?) belong to\?")),
    ('choice', 0, re.compile(r"Which code should this (.+?) get(?: for the (aspect|target) '(.+?)')?\?")),
]


def parse_question(instr):
    for kind, n, rx in QPATS:
        ms = list(rx.finditer(instr))
        if ms:
            m = ms[-1]
            return kind, n, m
    raise ParseError('no question')


def strip_rowlevel(instr):
    """Remove the question and row-level statements so they are not read as card lines."""
    return instr


def code_of(card, label):
    if label in card.codes:
        return label
    lid = card.names.get(label.lower())
    return lid


# ----------------------------------------------------------------------------------------------- per-row solve
CARD_CACHE = {}
TREE_CACHE = {}


def get_card(text, opt_lines, bracket):
    key = hashlib.sha1((text + '\x00' + json.dumps(opt_lines) + '\x00' + str(bracket)).encode()).hexdigest()
    if key not in CARD_CACHE:
        card = CardParser(text, opt_lines, bracket).parse()
        if card.kind != 's7' and not (card.kind == 's5' and card.key_kind == 'codebook'):
            card.build_lexicon()
        CARD_CACHE[key] = card
    return CARD_CACHE[key]


def get_tree(card):
    key = id(card)
    if key not in TREE_CACHE:
        TREE_CACHE[key] = Tree(card)
    return TREE_CACHE[key]


def opt_lines_of(row):
    out = []
    if row['qtype'] == 'choice' and row.get('card'):
        for line in row['card'].split('\n'):
            s = line.strip()
            while s.startswith('>'):
                s = s[1:].strip()
            if not s:
                continue
            m = re.match(r'^- (.+?): (?:\(([^)]+)\) )?(.+)$', s)
            if not m:
                raise ParseError('card line on a choice row is not an option line')
            out.append((m.group(1), m.group(2), m.group(3)))
    return out


def bracket_kind(instr):
    m = re.search(r"The label in brackets is that code's (ID|name)\.", instr)
    return m.group(1) if m else None


def solve_row(row, store):
    """Returns (gold_B, info dict)."""
    info = {'trace': []}
    opt_lines = opt_lines_of(row)
    instr = row['instructions']
    if row['qtype'] == 'noul':
        card_text = row['card']
    else:
        card_text = instr
    bracket = bracket_kind(instr) if opt_lines else None
    if opt_lines and bracket is None:
        # masked rows: no bracket statement, options are IDs
        for o, other, _ in opt_lines:
            if other is not None:
                raise ParseError('bracket without its statement')
    card = get_card(card_text, opt_lines, bracket)
    kind, n, m = parse_question(instr)
    info['qkind'] = kind
    info['card_kind'] = card.kind
    named = None
    if kind in ('yn_code', 'choice') and m.lastindex and m.lastindex >= 3:
        named = m.group(m.lastindex)

    def assign_state(text):
        if card.kind == 's7' or (card.kind == 's5' and card.key_kind == 'codebook'):
            src = row['meta'].get('text_source') or {}
            scheme = card.s7
            vec, rtext = store.vector(scheme, src.get('record_id'), named)
            if wsnorm(rtext) not in wsnorm(text):
                raise ParseError('shown text differs from the pinned record text')
            if card.kind == 's5':
                return assign_rules(card, vec)
            if scheme == 'xed':
                key = vec['labels']
            else:
                key = (vec['named'], vec['others'])
            hits = [cid for cid in card.code_order if key in card.s7codes[cid]]
            if len(hits) != 1:
                raise ParseError('S7 vector maps to %d codes' % len(hits))
            return hits[0], ['SEM-46 codebook']
        vec, mode = read_report(text, card)
        info['mode'] = mode
        tree = get_tree(card)
        code, tr = tree.eval(vec)
        # solver-B self check: the tree equals direct rule evaluation on the same parsed vector
        code2, _ = assign_rules(card, vec)
        if code2 != code:
            raise ParseError('tree != direct rules')
        info['vec'] = vec
        return code, tr

    if kind == 'yn_code':
        K = code_of(card, m.group(2).strip())
        if K is None:
            raise ParseError('asked code not on card')
        code, tr = assign_state(row['state'])
        info['trace'] = tr
        return int((code == K) != (n == 1)), info
    if kind == 'yn_group':
        G = m.group(2).strip()
        if card.kind == 's3':
            vec, _ = read_report(row['state'], card)
            names = [g['name'] for g in card.groups]
            if G not in names:
                raise ParseError('asked group not on card')
            inside = G in in_groups(card, vec)
        elif card.kind == 's5':
            gn = [k for k, d in card.key.items() if d['group'] == G]
            if len(gn) != 1:
                raise ParseError('asked couplet group not on card')
            inside = walk_passes(card, row, store, named, gn[0], assign_state)
        else:
            raise ParseError('group question on a card without groups')
        info['trace'] = ['SEM-33']
        return int(inside != (n == 1)), info
    opts = row['options'] or []
    if kind == 'coarse':
        if card.kind == 's3':
            vec, _ = read_report(row['state'], card)
            ins = in_groups(card, vec)
            hit = [o for o in opts if o in ins]
        elif card.kind == 's5':
            hit = []
            for o in opts:
                gn = [k for k, d in card.key.items() if d['group'] == o]
                if len(gn) != 1:
                    raise ParseError('coarse option is not a named couplet')
                if walk_passes(card, row, store, named, gn[0], assign_state):
                    hit.append(o)
        else:
            raise ParseError('coarse question without groups')
        if len(hit) != 1:
            raise ParseError('coarse: %d groups hold' % len(hit))
        info['trace'] = ['SEM-33']
        return hit[0], info
    if kind == 'inverted':
        K = code_of(card, m.group(2).strip())
        if K is None:
            raise ParseError('inverted asked code not on card')
        refs = [o for o in opts]
        blocks = {}
        cur = None
        for line in row['state'].split('\n'):
            ref = ref_of(line)
            if ref in refs:
                if ref in blocks:
                    raise ParseError('case reference twice')
                cur = ref
                blocks[cur] = []
                continue
            if cur is not None:
                blocks[cur].append(line)
        none_opts = [o for o in opts if o not in blocks]
        if len(none_opts) > 1:
            raise ParseError('more than one option without a report block')
        got = []
        for ref, ls in blocks.items():
            code, tr = assign_state('\n'.join(ls))
            if code == K:
                got.append(ref)
        if len(got) > 1:
            raise ParseError('two reports get K')
        info['trace'] = ['SEM-51']
        if got:
            return got[0], info
        if not none_opts:
            raise ParseError('no report gets K and no none option')
        return none_opts[0], info
    if kind == 'choice':
        code, tr = assign_state(row['state'])
        info['trace'] = tr
        hit = [o for o in opts if code_of(card, o) == code]
        if len(hit) > 1:
            raise ParseError('two options map to the code')
        if hit:
            return hit[0], info
        others = [o for o in opts if code_of(card, o) is None]
        if len(others) != 1:
            raise ParseError('assigned code not offered and %d non-code options' % len(others))
        info['trace'] = tr + ['SEM-34 none']
        return others[0], info
    raise ParseError('question kind')


def ref_of(line):
    t = line.strip()
    t = re.sub(r'^(?:>\s*)+', '', t)
    t = re.sub(r'^(?:#+\s*|[-*+\u2022]\s+|\d+\.\s+)', '', t)
    t = re.sub(r'^\*\*(.*)\*\*$', r'\1', t)
    t = re.sub(r'^\[(.*)\]$', r'\1', t)
    return t.strip().rstrip(':').strip()


def walk_passes(card, row, store, named, n_target, assign_state):
    """S5 group membership (R24): does the key walk from couplet 1 pass couplet n_target?"""
    if card.key_kind == 'codebook':
        src = row['meta'].get('text_source') or {}
        vec, _ = store.vector(card.s7, src.get('record_id'), named)
    else:
        vec, _ = read_report(row['state'], card)
    n = 1
    seen = set()
    while True:
        if n == n_target:
            return True
        if n in seen:
            raise ParseError('key loop')
        seen.add(n)
        d = card.key[n]
        t = d['a'] if ev(d['cond'], vec) else d['b']
        if not t.isdigit():
            return False
        n = int(t)


# ----------------------------------------------------------------------------------------------- spec items
def spec_item(row, info):
    m = row['meta']
    items = []
    q = info.get('qkind')
    items.append({'yn_code': 'SEM-39/SEM-40', 'yn_group': 'SEM-33/SEM-40', 'choice': 'Assign + SEM-34',
                  'coarse': 'SEM-33', 'inverted': 'SEM-51'}.get(q, 'question'))
    items += [t.split(' ')[0] for t in info.get('trace', [])]
    items.append({'S1': 'S1', 'S2': 'S2', 'S3': 'S3 group gate', 'S4': 'SEM-50 records', 'S6': 'SEM-11',
                  'S7': 'SEM-45/46', 'S5': 'Assign 5b key'}.get(m.get('sampler'), ''))
    return ', '.join(dict.fromkeys(i for i in items if i))


def err_item(msg):
    rules = [('subject', 'F11-R5-05 subject line'), ('record', 'SEM-50 records'), ('field', 'SEM-50 records'),
             ('number', 'SEM-21/R08 numbers'), ('unit', 'F11-R3-03 units'), ('stated', 'R13/SEM-03 missing'),
             ('conflict', 'SEM-06 frames'), ('S7', 'SEM-46 codebook'), ('note', 'SEM-13 note'),
             ('|F|', 'SEM-12 fit'), ('question', 'question forms'), ('option', 'F11-R5-A1 layout'),
             ('table', 'SEM-48 table'), ('glossary', 'SEM-43 glossary'), ('cond', 'section 7 grammar')]
    for k, v in rules:
        if k in msg:
            return v
    return 'section 7 parse'


# ----------------------------------------------------------------------------------------------- main
def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', default='candidates_r1,qc_sample,mixdev_S5')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out', default=os.path.join(HERE, 'mismatch.json'))
    args = ap.parse_args(argv)
    t0 = time.time()
    store = S7Store()
    for k, s in store.sha.items():
        if s != S7Store.PINNED[k]:
            print('WARNING: pinned sha differs for', k)
    report = {'solver': 'F11 solver B (independent; decision tree over parsed card + frame reader; S7 record reload)',
              'g0_sha256': hashlib.sha256(open(os.path.join(FAM, 'G0_SPEC.md'), 'rb').read()).hexdigest(),
              'solver_sha256': hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest(),
              'records_sha256': store.sha, 'files': {}, 'mismatches': []}
    for fname in args.files.split(','):
        path = os.path.join(FAM, 'out', fname + '.jsonl')
        data = open(path, 'rb').read()
        n = agree = 0
        by = Counter()
        cov = Counter()
        for line in data.decode('utf-8').split('\n'):
            if not line.strip():
                continue
            row = json.loads(line)
            n += 1
            try:
                gb, info = solve_row(row, store)
                err = None
            except (ParseError, KeyError, ValueError, IndexError) as e:
                gb, info, err = None, {'trace': []}, '%s: %s' % (type(e).__name__, e)
            if err is None:
                cov['q:' + str(info.get('qkind'))] += 1
                cov['card:' + str(info.get('card_kind'))] += 1
                if info.get('mode'):
                    cov['report:' + info['mode']] += 1
                for t in info.get('trace', []):
                    cov['rule:' + ' '.join(t.split(' ')[:2])] += 1
            if err is None and gb == row['gold']:
                agree += 1
                by[(row['meta'].get('sampler'), 'ok')] += 1
                continue
            by[(row['meta'].get('sampler'), 'mismatch')] += 1
            report['mismatches'].append({
                'file': fname, 'id': row['id'], 'sampler': row['meta'].get('sampler'), 'qtype': row['qtype'],
                'role': row['role'], 'twin_kind': row['meta'].get('twin_kind'),
                'gold_A': row['gold'], 'gold_B': gb,
                'spec_item': err_item(err) if err else spec_item(row, info),
                'error': err})
            if args.limit and len(report['mismatches']) >= args.limit:
                break
        report['files'][fname] = {'rows': n, 'agree': agree, 'mismatch': n - agree,
                                  'sha256': hashlib.sha256(data).hexdigest(),
                                  'by_sampler': {'%s:%s' % k: v for k, v in sorted(by.items())},
                                  'coverage': dict(sorted(cov.items()))}
        print('%s: rows %d agree %d mismatch %d (%.0fs)' % (fname, n, agree, n - agree, time.time() - t0),
              flush=True)
    report['total_rows'] = sum(f['rows'] for f in report['files'].values())
    report['total_mismatch'] = len(report['mismatches'])
    report['utc'] = _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(args.out, 'w') as f:
        json.dump(report, f, indent=1)
    print('total rows %d mismatches %d -> %s' % (report['total_rows'], report['total_mismatch'], args.out))


if __name__ == '__main__':
    main()
