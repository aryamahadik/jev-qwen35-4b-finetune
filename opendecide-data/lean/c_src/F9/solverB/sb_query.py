# F9 solver B, part 3: question parser (closed grammar of G0 1.2 / section 2) -> AST.
# Written from G0_SPEC.md v7 only. Conditions become AST nodes; sb_eval.py compiles them to SQL.
import re, datetime
from fractions import Fraction
from sb_parse import ParseError, parse_number, parse_date, parse_datetime, date_rx, dt_rx, ALLMON
from sb_model import SCALE, fold, ID_RX

GE = ['at least', 'no fewer than', 'no less than']
LE = ['at most', 'no more than', 'not more than', 'up to']
GT = ['more than', 'greater than', 'higher than', 'over', 'above', 'exceeds']
LT = ['less than', 'fewer than', 'lower than', 'below', 'under']
PREFIX_OPS = [(p, '>=') for p in GE] + [(p, '<=') for p in LE] + [(p, '>') for p in GT] + [(p, '<') for p in LT] + \
             [('exactly', '='), ('not equal to', '!=')]
PREFIX_OPS.sort(key=lambda x: -len(x[0]))
SUFFIX_OPS = [('or more', '>='), ('or fewer', '<='), ('or less', '<=')]
ID_TOKEN = r'[A-Z][A-Z0-9]*-\d+'


def numrx(card):
    d = re.escape(card.dec)
    if card.thou:
        t = re.escape(card.thou)
        return r'-?(?:\d{1,3}(?:' + t + r'\d{3})+(?:' + d + r'\d+)?|\d+(?:' + d + r'\d+)?)'
    return r'-?\d+(?:' + d + r'\d+)?'


class Ctx:
    def __init__(self, model, card):
        self.m, self.card = model, card
        self.NUM = numrx(card)


# ---------------------------------------------------------------- literals --------------------------------------
def lit_num(text, col, ctx):
    """'<number> <unit>' -> scaled int; the unit must be the column's unit (no T28 factors on these cards)."""
    m = re.fullmatch('(' + ctx.NUM + r')(?: (.+))?', text.strip())
    if not m:
        raise ParseError('num literal: ' + text)
    v = parse_number(m.group(1), ctx.card) * SCALE
    unit = m.group(2)
    if unit is not None and col is not None and col.unit is not None and unit.strip() != col.unit:
        raise ParseError('unit %r vs column unit %r' % (unit, col.unit))
    if v.denominator != 1:
        raise ParseError('literal scale')
    return int(v)


def lit_count(text):
    if not re.fullmatch(r'\d+', text.strip()):
        raise ParseError('count literal: ' + text)
    return int(text)


def month_range(text):
    m = re.fullmatch(r'([A-Z][a-z]+) (\d{4})', text.strip())
    if not m or m.group(1).lower() not in ALLMON:
        raise ParseError('month ' + text)
    y, mo = int(m.group(2)), ALLMON[m.group(1).lower()]
    a = datetime.date(y, mo, 1).toordinal()
    b = (datetime.date(y + (mo == 12), mo % 12 + 1, 1)).toordinal() - 1
    return a, b


def time_window(text, ctx, is_dt):
    """Closed time grammar (T15-T17). Returns (lo, lo_incl, hi, hi_incl) in column units (day ordinals or secs)."""
    s = text.strip()
    card = ctx.card
    DR = date_rx(card)
    DT = dt_rx(card)
    def strip_names(rx):
        return re.sub(r'\(\?P<[a-zA-Z]+>', '(?:', rx)
    D = strip_names(DR); T = strip_names(DT)

    def day(x):
        return parse_date(x, card)

    def dayspan(a, b):  # whole days [a, b] -> column units
        if is_dt:
            return (a * 86400, True, (b + 1) * 86400, False)
        return (a, True, b, True)
    m = re.fullmatch(r'from (' + T + r') up to but not including (' + T + r')', s)
    if m:
        if not is_dt:
            raise ParseError('T17 window on a date column')
        return (parse_datetime(m.group(1), card), True, parse_datetime(m.group(2), card), False)
    m = re.fullmatch(r'from (' + T + r') to (' + T + r'), both included', s)
    if m:
        if not is_dt:
            raise ParseError('T17 window on a date column')
        return (parse_datetime(m.group(1), card), True, parse_datetime(m.group(2), card), True)
    m = re.fullmatch(r'from (' + D + r') to (' + D + r')', s)
    if m:
        return dayspan(day(m.group(1)), day(m.group(2)))
    m = re.fullmatch(r'(?:in )?the (\d+) days ending on (' + D + r')', s)
    if m:
        n, d = int(m.group(1)), day(m.group(2))
        return dayspan(d - n + 1, d)
    m = re.fullmatch(r'in ([A-Z][a-z]+ \d{4})', s)
    if m:
        a, b = month_range(m.group(1))
        return dayspan(a, b)
    m = re.fullmatch(r'on or before (' + D + r')', s)
    if m:
        d = day(m.group(1))
        return (None, None, (d + 1) * 86400, False) if is_dt else (None, None, d, True)
    m = re.fullmatch(r'on or after (' + D + r')', s)
    if m:
        d = day(m.group(1))
        return (d * 86400, True, None, None) if is_dt else (d, True, None, None)
    m = re.fullmatch(r'before (' + D + r')', s)
    if m:
        d = day(m.group(1))
        return (None, None, d * 86400, False) if is_dt else (None, None, d, False)
    m = re.fullmatch(r'after (' + D + r')', s)
    if m:
        d = day(m.group(1))
        return ((d + 1) * 86400, True, None, None) if is_dt else (d, False, None, None)
    m = re.fullmatch(r'on (' + D + r')', s)
    if m:
        return dayspan(day(m.group(1)), day(m.group(1)))
    raise ParseError('time phrase: ' + s)


# ---------------------------------------------------------------- predicates ------------------------------------
def cat_values(col):
    vals = set(col.values)
    if col.legend:
        vals |= {fold(v) for v in col.legend.values()}
    return vals


def cat_lit(text, col, ctx, allow_unknown_value=False):
    # a question literal may name a value that no record holds (1.1 step 5), so unknown values are accepted
    return fold(text)


def split_or(text, col, ctx):
    """'A or B' / 'A, B or C' -> list of folded values (whole string tried first)."""
    vals = cat_values(col) | ctx.domvals.get(col.name, set())
    if fold(text) in vals:
        return [fold(text)]
    parts = re.split(r', | or ', text)
    return [fold(p) for p in parts]


def parse_pred(col, p, ctx):
    """'<pred>' after '<col> is' -> AST node over column object col."""
    p = p.strip()
    t = col.typ
    if t in ('num',):
        m = re.fullmatch(r'between (.+?) and (.+)', p)
        if m:
            return ('range', col, lit_num(m.group(1), col, ctx), True, lit_num(m.group(2), col, ctx), True)
        for ph, op in PREFIX_OPS:
            if p.startswith(ph + ' '):
                return ('cmp', col, op, lit_num(p[len(ph) + 1:], col, ctx))
        for ph, op in SUFFIX_OPS:
            if p.endswith(' ' + ph):
                return ('cmp', col, op, lit_num(p[:-len(ph) - 1], col, ctx))
        raise ParseError('num pred: ' + p)
    if t in ('date', 'dt'):
        lo, li, hi, hi_i = time_window(p, ctx, t == 'dt')
        return ('range', col, lo, li, hi, hi_i)
    if t == 'bool':
        raise ParseError('bool pred: ' + p)
    if t == 'id':
        if ID_RX.match(p):
            return ('cmp', col, '=', p)
        raise ParseError('id pred ' + p)
    # category / text
    m = re.fullmatch(r'neither (.+) nor (.+)', p)
    if m:
        return ('not', ('in', col, [cat_lit(m.group(1), col, ctx), cat_lit(m.group(2), col, ctx)]))
    m = re.fullmatch(r'not (.+)', p)
    if m and fold(p) not in cat_values(col):
        if m.group(1).startswith('equal to '):
            return ('not', ('in', col, [cat_lit(m.group(1)[9:], col, ctx)]))
        return ('not', ('in', col, [cat_lit(m.group(1), col, ctx)]))
    m = re.fullmatch(r'exactly (.+)', p)
    if m and fold(p) not in cat_values(col):
        return ('in', col, [cat_lit(m.group(1), col, ctx)])
    return ('in', col, split_or(p, col, ctx))


def find_col(text, cols):
    """Longest column name that starts text; returns (Col, rest)."""
    best = None
    for n, c in cols.items():
        if text == n or text.startswith(n + ' '):
            if best is None or len(n) > len(best.name):
                best = c
    if best is None:
        raise ParseError('no column at: ' + text[:40])
    return best, text[len(best.name):].strip()


def parse_atom(text, cols, ctx):
    """'<col> is <pred>' | '<col> contains "<s>"' | '<col> is not <cat>'."""
    col, rest = find_col(text.strip(), cols)
    m = re.fullmatch(r'contains "(.*)"', rest)
    if m:
        return ('contains', col, fold(m.group(1)))
    m = re.fullmatch(r'does not contain "(.*)"', rest)
    if m:
        return ('not', ('contains', col, fold(m.group(1))))
    if rest.startswith('is '):
        return parse_pred(col, rest[3:], ctx)
    raise ParseError('atom: ' + text[:60])


def parse_whose(text, cols, ctx):
    """'whose A and whose B ...' | 'that counts as T' | 'that count as T' -> AST."""
    s = text.strip()
    m = re.fullmatch(r'that (?:counts|count) as (.+)', s)
    if m:
        return ('term', term_name(m.group(1), ctx))
    m = re.fullmatch(r'that (?:does|do) not count as (.+)', s)
    if m:
        return ('not', ('term', term_name(m.group(1), ctx)))
    if not s.startswith('whose '):
        raise ParseError('cond: ' + s[:50])
    parts = s[6:].split(' and whose ')
    atoms = []
    for p in parts:
        sub = p.split(' or whose ')
        if len(sub) > 1:
            atoms.append(('or', [parse_atom(x, cols, ctx) for x in sub]))
        else:
            atoms.append(parse_atom(p, cols, ctx))
    return atoms[0] if len(atoms) == 1 else ('and', atoms)


def term_name(t, ctx):
    t = t.strip()
    if t in ctx.card.terms:
        return t
    raise ParseError('unknown term ' + t)


def parse_term_cond(text, cols, ctx):
    """Card-definition condition: 'its A is X' (T9 list item), 'its A is X and its B is Y', or a 'whose' chain."""
    s = text.strip()
    if s.startswith('its '):
        parts = re.split(r' and its | and whose ', s[4:])
        atoms = [parse_atom(p, cols, ctx) for p in parts]
        return atoms[0] if len(atoms) == 1 else ('and', atoms)
    if s.startswith('whose '):
        return parse_whose(s, cols, ctx)
    raise ParseError('term cond: ' + s[:60])


def compile_terms(ctx, cols):
    """card.terms -> {name: (general AST, [(key Col, folded value, AST)])}."""
    out = {}
    for name, d in ctx.card.terms.items():
        if d[0] == 'T9':
            atoms = [parse_term_cond(x, cols, ctx) for x in d[1]]
            gen = atoms[0] if len(atoms) == 1 else ('and', atoms)
        elif d[0] == 'T7':
            gen = ('and', [parse_term_cond(d[1], cols, ctx), ('not', parse_term_cond(d[2], cols, ctx))])
        elif d[0] == 'T8':
            gen = ('and', [parse_term_cond(d[1], cols, ctx), parse_whose('whose ' + d[2], cols, ctx)])
        ovs = []
        for keyval, cond in ctx.card.overrides.get(name, []):
            hits = []
            for c in cols.values():
                if c.typ == 'cat':
                    for v in cat_values(c) | ctx.domvals.get(c.name, set()):
                        if fold(keyval).startswith(v + ' '):
                            hits.append((len(v), c, v))
            hits.sort(key=lambda x: -x[0])
            if not hits or (len(hits) > 1 and hits[1][0] == hits[0][0]):
                raise ParseError('override key ' + keyval)
            ovs.append((hits[0][1], hits[0][2], parse_term_cond(cond, cols, ctx)))
        out[name] = (gen, ovs)
    return out
