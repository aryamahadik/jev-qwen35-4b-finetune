# F9 solver B, part 4: question templates (closed grammar), SQL compilation and evaluation, option mapping.
# Written from G0_SPEC.md v7 only (1.2, 1.3, section 2, 3.x). Paradigm: every answer is computed by sqlite queries
# on the tables parsed back from the rendered text; exact integer (scaled) arithmetic, no floats.
import re, itertools
from fractions import Fraction
from sb_parse import ParseError, parse_number, parse_date, parse_datetime, num_decimals
from sb_model import SCALE, fold, q, sqlstr, ID_RX, Col
from sb_query import (Ctx, PREFIX_OPS, SUFFIX_OPS, ID_TOKEN, parse_whose, parse_pred, parse_atom, find_col,
                      compile_terms, lit_num, lit_count, time_window, term_name, cat_values)

CMP_WORDS = sorted([p for p, _ in PREFIX_OPS], key=len, reverse=True)
OPMAP = dict(PREFIX_OPS)
SUFMAP = dict(SUFFIX_OPS)
PYOP = {'>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b, '>': lambda a, b: a > b, '<': lambda a, b: a < b,
        '=': lambda a, b: a == b, '!=': lambda a, b: a != b}
GROUP_CMP = [('at least as high as', '>='), ('at least as many as', '>='), ('at least as large as', '>='),
             ('the same as', '='), ('greater than', '>'), ('higher than', '>'), ('more than', '>'),
             ('less than', '<'), ('lower than', '<'), ('fewer than', '<'), ('at most as high as', '<='),
             ('no higher than', '<='), ('no greater than', '<='), ('no more than', '<='), ('no lower than', '>='),
             ('no less than', '>='), ('not more than', '<=')]


class Unsupported(Exception):
    pass


# ---------------------------------------------------------------- SQL compile -----------------------------------
def sqlval(v):
    if isinstance(v, str):
        return sqlstr(v)
    return str(int(v))


def to_sql(node, a, ctx, item_alias=None):
    k = node[0]
    if k == 'cmp':
        _, col, op, v = node
        return '%s.%s %s %s' % (a, q(col.name), op, sqlval(v))
    if k == 'in':
        _, col, vals = node
        return '%s.%s IN (%s)' % (a, q(col.name), ','.join(sqlval(v) for v in vals))
    if k == 'range':
        _, col, lo, li, hi, hi_i = node
        parts = []
        if lo is not None:
            parts.append('%s.%s %s %d' % (a, q(col.name), '>=' if li else '>', lo))
        if hi is not None:
            parts.append('%s.%s %s %d' % (a, q(col.name), '<=' if hi_i else '<', hi))
        return '(' + ' AND '.join(parts) + ')'
    if k == 'contains':
        _, col, s = node
        return 'instr(%s.%s, %s) > 0' % (a, q(col.name), sqlstr(s))
    if k == 'not':
        return 'NOT (' + to_sql(node[1], a, ctx) + ')'
    if k == 'and':
        return '(' + ' AND '.join(to_sql(x, a, ctx) for x in node[1]) + ')'
    if k == 'or':
        return '(' + ' OR '.join(to_sql(x, a, ctx) for x in node[1]) + ')'
    if k == 'xor':
        return '((%s) + (%s) = 1)' % (to_sql(node[1], a, ctx), to_sql(node[2], a, ctx))
    if k == 'term':
        gen, ovs = ctx.terms[node[1]]
        if not ovs:
            return to_sql(gen, a, ctx)
        s = 'CASE'
        for kc, kv, cond in ovs:
            s += ' WHEN %s.%s = %s THEN (%s)' % (a, q(kc.name), sqlstr(kv), to_sql(cond, a, ctx))
        return s + ' ELSE (%s) END' % to_sql(gen, a, ctx)
    if k in ('any', 'every', 'no'):
        _, lname, cond = node
        tn, icols = ctx.m.items[lname]
        inner = to_sql(cond, 'it', ctx)
        ex = 'EXISTS (SELECT 1 FROM %s it WHERE it._owner = %s._rid AND %s)' % (tn, a, inner)
        anyit = 'EXISTS (SELECT 1 FROM %s it WHERE it._owner = %s._rid)' % (tn, a)
        if k == 'any':
            return ex
        if k == 'no':
            return 'NOT ' + ex
        return '(%s AND NOT EXISTS (SELECT 1 FROM %s it WHERE it._owner = %s._rid AND NOT (%s)))' % (
            anyit, tn, a, inner)
    if k == 'true':
        return '1'
    raise Unsupported('sql node ' + k)


def used_cols(node, ctx, out=None):
    """Columns a condition reads (T4): includes every column of a term (general, overrides and key)."""
    if out is None:
        out = set()
    k = node[0]
    if k in ('cmp', 'in', 'range', 'contains'):
        out.add(node[1].name)
    elif k == 'not':
        used_cols(node[1], ctx, out)
    elif k in ('and', 'or'):
        for x in node[1]:
            used_cols(x, ctx, out)
    elif k == 'xor':
        used_cols(node[1], ctx, out); used_cols(node[2], ctx, out)
    elif k == 'term':
        gen, ovs = ctx.terms[node[1]]
        used_cols(gen, ctx, out)
        for kc, kv, cond in ovs:
            out.add(kc.name); used_cols(cond, ctx, out)
    elif k in ('any', 'every', 'no'):
        out.add('_ls_' + node[1])
    return out


def notnull(cols, a='r'):
    cs = [c for c in cols if not c.startswith('_ls_')]
    ls = [c for c in cols if c.startswith('_ls_')]
    parts = ['%s.%s IS NOT NULL' % (a, q(c)) for c in sorted(cs)] + ["%s.%s != 'null'" % (a, q(c)) for c in sorted(ls)]
    return ' AND '.join(parts) if parts else '1'


# ---------------------------------------------------------------- trailing comparators ---------------------------
def split_trailing_cmp(text, litparse):
    """'<cond> <cmp phrase> <lit>' -> (cond, op, lit) using the LAST split whose literal parses."""
    cands = []
    for ph, op in PREFIX_OPS:
        for m in re.finditer(r'(?:^| )' + re.escape(ph) + ' ', text):
            cands.append((m.start(), m.end(), op, None))
    for ph, op in SUFFIX_OPS:
        if text.endswith(' ' + ph):
            body = text[:-len(ph) - 1]
            # literal is the tail of body; try progressively longer tails
            toks = body.split(' ')
            for i in range(len(toks) - 1, -1, -1):
                lit = ' '.join(toks[i:])
                try:
                    v = litparse(lit)
                except (ParseError, ValueError):
                    continue
                return ' '.join(toks[:i]), op, v
    cands.sort(key=lambda x: (-x[1], x[0]))   # latest end first; at one end, the longest phrase
    for s, e, op, _ in cands:
        lit = text[e:]
        try:
            v = litparse(lit)
        except (ParseError, ValueError):
            continue
        return text[:s].strip(), op, v
    raise ParseError('no trailing comparator: ' + text[-50:])


# ---------------------------------------------------------------- question normalisation ------------------------
def drop_main_is(d):
    """'the average X of the Y whose ... is lower than 7 people' -> drop the main-clause 'is' (the last ' is '
    followed by a comparator phrase or a group-comparison phrase)."""
    phrases = [p for p, _ in PREFIX_OPS] + [p for p, _ in GROUP_CMP]
    best = None
    for mm in re.finditer(r' is ', d):
        tail = d[mm.end():]
        if any(tail.startswith(p + ' ') for p in phrases) or re.match(r'\S+(?: \S+)? or (?:more|fewer|less)$', tail):
            best = mm
    if best is None:
        raise ParseError('negated aggregate form')
    return d[:best.start()] + ' ' + d[best.end():]



def normalise(qs):
    s = qs.strip()
    if s.endswith('?'):
        s = s[:-1]
    listed = False
    m = re.match(r'Among the listed ([^,]+), (.*)$', s)
    if m:
        listed = True
        s = m.group(2)
        s = s[0].upper() + s[1:]
    neg = 0
    while True:
        m = re.match(r'Is it not the case that (.*)$', s)
        if not m:
            break
        neg += 1
        d = m.group(1)
        rew = [
            (r'^there is (.*)$', r'Is there \1'),
            (r'^every (.*?) is also (.*)$', r'Is every \1 also \2'),
            (r'^(' + ID_TOKEN + r') does not count as (.*)$', r'Does \1 not count as \2'),
            (r'^(' + ID_TOKEN + r') counts as (.*)$', r'Does \1 count as \2'),
            (r'^(request ' + ID_TOKEN + r'|session ' + ID_TOKEN + r'|' + ID_TOKEN + r') has (.*)$', r'Does \1 have \2'),
            (r'^(request ' + ID_TOKEN + r'|session ' + ID_TOKEN + r'|' + ID_TOKEN + r') does not have (.*)$',
             r'Does \1 not have \2'),
            (r'^the (.+?) of (' + ID_TOKEN + r')( in Week \d+)? is (.*)$', r'Is the \1 of \2\3 \4'),
            (r'^every (.+?) of (' + ID_TOKEN + r') is (.*)$', r'Is every \1 of \2 \3'),
            (r'^the ((?:average|total|number) .*)$', None),
        ]
        for a, b in rew:
            if re.match(a, d):
                if b is None:
                    s = 'Is ' + drop_main_is(d)
                else:
                    s = re.sub(a, b, d)
                break
        else:
            raise ParseError('negated form: ' + d[:60])
    return s, listed, neg


# ---------------------------------------------------------------- query parse (tables) --------------------------
def P(rx, s):
    return re.fullmatch(rx, s)


def parse_question(qs, m, card, ctx, qtype):
    s, listed, neg = normalise(qs)
    Q = dict(listed=listed, neg=neg, raw=qs)
    kind = m.kind
    ID = '(?P<id>' + ID_TOKEN + ')'
    if kind == 'log':
        Q.update(parse_log_q(s, m, card, ctx))
        return Q
    if kind == 'pivot':
        Q.update(parse_pivot_q(s, m, card, ctx))
        return Q
    if kind == 'join':
        r = parse_join_q(s, m, card, ctx)
        if r is not None:
            Q.update(r)
            return Q
    cols = m.cols

    def cond(t):
        return parse_whose(t, cols, ctx)
    # ---- yes/no
    x = P(r'Is there (?P<qq>a|an|no) (?P<rec>.+?) with (?P<col>\S+) ' + ID, s)
    if x:
        Q.update(op='presence', id=x.group('id'), col=x.group('col'))
        if x.group('qq') == 'no':
            Q['neg'] += 1
        return Q
    x = P(r'Does ' + ID + r' (?P<n>not )?count as (?P<t>.+)', s)
    if x:
        Q.update(op='lookup_cond', id=x.group('id'), cond=('term', term_name(x.group('t'), ctx)))
        if x.group('n'):
            Q['neg'] += 1
        return Q
    x = P(r'Does ' + ID + r' (?P<n>not )?have (?P<qq>any|no) (?P<item>.+?) (?P<c>whose .+)', s)
    if x and kind == 'nested':
        lname = list_name(x.group('item'), m)
        ic = m.items[lname][1]
        node = (x.group('qq'), lname, parse_whose(x.group('c'), ic, ctx))
        Q.update(op='lookup_cond', id=x.group('id'), cond=node)
        if x.group('n'):
            Q['neg'] += 1
        return Q
    x = P(r'Is every (?P<item>.+?) of ' + ID + r' one (?P<c>whose .+)', s)
    if x and kind == 'nested':
        lname = list_name(x.group('item'), m)
        ic = m.items[lname][1]
        Q.update(op='lookup_cond', id=x.group('id'), cond=('every', lname, parse_whose(x.group('c'), ic, ctx)))
        return Q
    x = P(r'Is the (?P<rest>.+?) of ' + ID + r' (?P<pred>.+)', s)
    if x and not x.group('rest').startswith(('number of', 'total ', 'average ')):
        col, r2 = find_col(x.group('rest'), cols)
        if r2:
            raise ParseError('lookup col tail')
        Q.update(op='lookup_cond', id=x.group('id'), cond=parse_pred(col, x.group('pred'), ctx))
        return Q
    x = P(r'Is there (?P<qq>a|an|no) (?P<rec>.+?) (?P<c>(?:whose|that) .+)', s)
    if x:
        Q.update(op='exists', cond=cond(x.group('c')))
        if x.group('qq') == 'no':
            Q['neg'] += 1
        return Q
    x = P(r'Is every (?P<rec>.+?) (?P<a>(?:whose|that) .+?) also one (?P<b>(?:whose|that) .+)', s)
    if x:
        Q.update(op='forall', a=cond(x.group('a')), b=cond(x.group('b')))
        return Q
    x = P(r'Is the number of (?P<rest>.+)', s)
    if x:
        for ph, gop in sorted(GROUP_CMP, key=lambda z: -len(z[0])):
            mm = P(r'(?P<rec>.+?) (?P<a>(?:whose|that) .+?) ' + re.escape(ph) + r' the number of (?P<rec2>.+?) '
                   r'(?P<b>(?:whose|that) .+)', x.group('rest'))
            if mm:
                Q.update(op='count_compare', a=cond(mm.group('a')), b=cond(mm.group('b')), cmp=gop)
                return Q
        body, op, v = split_trailing_cmp(x.group('rest'), lit_count)
        mm = P(r'(?P<rec>.+?) (?P<c>(?:whose|that) .+)', body)
        Q.update(op='count', cond=cond(mm.group('c')) if mm else ('true',), cmp=(op, v))
        return Q
    x = P(r'Is the (?P<agg>average|total) (?P<rest>.+)', s)
    if x:
        r = parse_agg_compare_or_cmp(x.group('agg'), x.group('rest'), cols, ctx)
        Q.update(r)
        return Q
    # ---- choice
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the (?P<agg>total|average) (?P<rest>.+)', s)
    if x:
        col, r2 = find_col(x.group('rest'), cols)
        mm = P(r'of the (?P<rec>.+?) (?P<c>(?:whose|that) .+)', r2)
        if not mm:
            mm2 = P(r'of the (?P<rec>.+?)', r2)
            if not mm2:
                raise ParseError('agg value form')
        check_unit(x.group('unit'), col)
        Q.update(op='sum' if x.group('agg') == 'total' else 'mean', col=col,
                 cond=cond(mm.group('c')) if mm else ('true',))
        return Q
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the (?P<ext>highest|lowest|earliest|latest) (?P<rest>.+)', s)
    if x:
        col, r2 = find_col(x.group('rest'), cols)
        check_unit(x.group('unit'), col)
        mm = P(r'(?:of|among) the (?P<rec>.+?) (?P<c>(?:whose|that) .+)', r2)
        Q.update(op='maxv' if x.group('ext') in ('highest', 'latest') else 'minv', col=col,
                 cond=cond(mm.group('c')) if mm else ('true',))
        return Q
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the (?P<rest>.+?) of ' + ID, s)
    if x:
        col, r2 = find_col(x.group('rest'), cols)
        if r2:
            raise ParseError('lookup col tail')
        check_unit(x.group('unit'), col)
        Q.update(op='lookup_val', id=x.group('id'), col=col)
        return Q
    x = P(r'[Hh]ow many different (?P<rest>.+?) values do the (?P<rec>.+?) (?P<c>(?:whose|that) .+) have', s)
    if x:
        col, r2 = find_col(x.group('rest'), cols)
        Q.update(op='count_distinct', col=col, cond=cond(x.group('c')))
        return Q
    x = P(r'[Hh]ow many (?P<rec>.+?) (?:are there )?(?P<c>(?:whose|that) .+)', s)
    if x:
        Q.update(op='count_val', cond=cond(x.group('c')))
        return Q
    x = P(r'[Hh]ow many (?P<rec>.+?) count as (?P<t>.+)', s)
    if x:
        Q.update(op='count_val', cond=('term', term_name(x.group('t'), ctx)))
        return Q
    x = P(r'[Ww]hich (?P<rec>.+?)(?: (?P<c>(?:whose|that) .+?))? has the (?P<ext>highest|lowest|earliest|latest) '
          r'(?P<rest>.+)', s)
    if x and not x.group('rec').startswith('of these'):
        col, r2 = find_col(x.group('rest'), cols)
        if r2:
            raise ParseError('argmax tail')
        Q.update(op='argmax' if x.group('ext') in ('highest', 'latest') else 'argmin', col=col,
                 cond=cond(x.group('c')) if x.group('c') else ('true',))
        return Q
    x = P(r'[Ww]hich (?P<rec>.+?) are the ones (?P<c>(?:whose|that) .+)', s)
    if x:
        Q.update(op='select', cond=cond(x.group('c')))
        return Q
    x = P(r'[Ww]hich of these (?P<rec>.+?) (?:is one (?P<c>(?:whose|that) .+)|counts as (?P<t>.+))', s)
    if x:
        c = cond(x.group('c')) if x.group('c') else ('term', term_name(x.group('t'), ctx))
        Q.update(op='pick', cond=c)
        return Q
    x = P(r'[Ww]hich (?P<rec>.+?) count as (?P<t>.+)', s)
    if x:
        Q.update(op='select', cond=('term', term_name(x.group('t'), ctx)))
        return Q
    raise ParseError('no template: ' + s[:80])


def check_unit(unit, col):
    if unit is not None and col.unit is not None and unit.strip() != col.unit:
        raise ParseError('answer unit %r vs column %r (no factor)' % (unit, col.unit))


def list_name(item_phrase, m):
    """'check' / 'checks' -> the list field whose name matches (singular or plural)."""
    ip = item_phrase.strip()
    for ln in m.items:
        base = ln.replace('_', ' ')
        if ip in (base, base.rstrip('s'), base[:-2] if base.endswith('es') else base) or ip + 's' == base \
                or ip + 'es' == base or (ip.endswith('y') and ip[:-1] + 'ies' == base):
            return ln
    if len(m.items) == 1:
        raise ParseError('list item phrase %r vs %s' % (ip, list(m.items)))
    raise ParseError('list item phrase ' + ip)


def parse_agg_compare_or_cmp(agg, rest, cols, ctx):
    """After 'Is the average|total': either a group compare or a comparison with a literal."""
    col, r2 = find_col(rest, cols)
    # group compare
    for ph, op in sorted(GROUP_CMP, key=lambda x: -len(x[0])):
        mm = re.fullmatch(r'of the (?P<rec>.+?) (?P<a>(?:whose|that) .+?) ' + re.escape(ph) +
                          r' the (?P<agg2>average|total) (?P<rest2>.+)', r2)
        if mm:
            col2, r3 = find_col(mm.group('rest2'), cols)
            mb = re.fullmatch(r'of the (?P<rec>.+?) (?P<b>(?:whose|that) .+)', r3)
            if not mb:
                continue
            return dict(op='compare', agg=agg, col=col, agg2=mm.group('agg2'), col2=col2,
                        a=parse_whose(mm.group('a'), cols, ctx), b=parse_whose(mb.group('b'), cols, ctx), cmp=op)
    body, op, v = split_trailing_cmp(r2, lambda t: lit_num(t, col, ctx))
    mm = re.fullmatch(r'of the (?P<rec>.+?) (?P<c>(?:whose|that) .+)', body)
    if mm:
        c = parse_whose(mm.group('c'), cols, ctx)
    elif re.fullmatch(r'of the (?P<rec>.+?)', body):
        c = ('true',)
    else:
        raise ParseError('agg cmp body')
    return dict(op='sum' if agg == 'total' else 'mean', col=col, cond=c, cmp=(op, v))


# ---------------------------------------------------------------- S3 join templates -----------------------------
def parse_join_q(s, m, card, ctx):
    ID = '(?P<id>' + ID_TOKEN + ')'
    D, F = m.dcols, m.fcols

    def dc(t):
        return parse_whose(t, D, ctx)

    def fc(t):
        return parse_whose(t, F, ctx)
    x = P(r'[Hh]ow many (?P<ev>.+?) belong to the (?P<ent>.+?) (?P<c>whose .+)', s)
    if x:
        return dict(op='j_count', dcond=dc(x.group('c')), fcond=('true',))
    x = P(r'[Hh]ow many (?P<ev>.+?) (?P<fc>whose .+?) belong to the (?P<ent>.+?) (?P<c>whose .+)', s)
    if x:
        return dict(op='j_count', dcond=dc(x.group('c')), fcond=fc(x.group('fc')))
    x = P(r'Is the number of (?P<rest>.+)', s)
    if x:
        body, op, v = split_trailing_cmp(x.group('rest'), lit_count)
        mm = P(r'(?P<ev>.+?) of the (?P<ent>.+?) (?P<c>whose .+)', body)
        if mm:
            return dict(op='j_count', dcond=dc(mm.group('c')), fcond=('true',), cmp=(op, v))
        mm = P(r'(?P<ev>.+?) of ' + ID + r'(?: (?P<c>whose .+))?', body)
        if mm:
            return dict(op='j_count', ent=mm.group('id'), dcond=('true',),
                        fcond=fc(mm.group('c')) if mm.group('c') else ('true',), cmp=(op, v))
        raise ParseError('join count form')
    x = P(r'[Ww]hich (?P<ent>.+?) has the (?P<ext>highest|lowest) total (?P<rest>.+)', s)
    if x:
        col, r2 = find_col(x.group('rest'), F)
        mm = P(r'over its (?P<ev>.+?)(?: (?P<c>whose .+))?', r2)
        if not mm:
            raise ParseError('group argmax form')
        return dict(op='j_argmax', agg='sum', col=col, ext=x.group('ext'),
                    fcond=fc(mm.group('c')) if mm.group('c') else ('true',))
    x = P(r'[Ww]hich (?P<ent>.+?) has the (?P<ext>most|fewest) (?P<ev>.+?)(?: (?P<c>whose .+))?', s)
    if x and not x.group('ent').startswith('of these'):
        return dict(op='j_argmax', agg='count', col=None, ext='highest' if x.group('ext') == 'most' else 'lowest',
                    fcond=fc(x.group('c')) if x.group('c') else ('true',))
    x = P(r'Does ' + ID + r' (?P<n>not )?have (?P<qq>any|no) (?P<ev>.+?) (?P<c>whose .+)', s)
    if x:
        r = dict(op='j_exists', ent=x.group('id'), fcond=fc(x.group('c')))
        if x.group('qq') == 'no':
            r['neg_extra'] = 1
        if x.group('n'):
            r['neg_extra'] = r.get('neg_extra', 0) + 1
        return r
    x = P(r'[Ww]hich of these (?P<ent>.+?) has any (?P<ev>.+?) (?P<c>whose .+)', s)
    if x:
        return dict(op='j_pick', fcond=fc(x.group('c')))
    x = P(r'[Ww]hich (?P<ent>.+?) have any (?P<ev>.+?) (?P<c>whose .+)', s)
    if x:
        return dict(op='j_select', fcond=fc(x.group('c')))
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the (?P<agg>total|average) (?P<rest>.+)', s)
    if x:
        col, r2 = find_col(x.group('rest'), F)
        check_unit(x.group('unit'), col)
        mm = P(r'of the (?P<ev>.+?) of ' + ID + r'(?: (?P<c>whose .+))?', r2)
        if mm:
            return dict(op='j_sum' if x.group('agg') == 'total' else 'j_mean', col=col, ent=mm.group('id'),
                        fcond=fc(mm.group('c')) if mm.group('c') else ('true',))
        mm = P(r'of the (?P<ev>.+?) of the (?P<ent>.+?) (?P<c>whose .+)', r2)
        if mm:
            return dict(op='j_sum' if x.group('agg') == 'total' else 'j_mean', col=col, dcond=dc(mm.group('c')),
                        fcond=('true',))
        raise ParseError('join sum form')
    x = P(r'Is the (?P<agg>total|average) (?P<rest>.+)', s)
    if x:
        col, r2 = find_col(x.group('rest'), F)
        body, op, v = split_trailing_cmp(r2, lambda t: lit_num(t, col, ctx))
        mm = P(r'of the (?P<ev>.+?) of ' + ID + r'(?: (?P<c>whose .+))?', body)
        if mm:
            return dict(op='j_sum' if x.group('agg') == 'total' else 'j_mean', col=col, ent=mm.group('id'),
                        fcond=fc(mm.group('c')) if mm.group('c') else ('true',), cmp=(op, v))
        mm = P(r'of the (?P<ev>.+?) of the (?P<ent>.+?) (?P<c>whose .+)', body)
        if mm:
            return dict(op='j_sum' if x.group('agg') == 'total' else 'j_mean', col=col, dcond=dc(mm.group('c')),
                        fcond=('true',), cmp=(op, v))
        raise ParseError('join agg cmp form')
    return None  # fall through to single-table templates on the dimension table


# ---------------------------------------------------------------- S5 pivot templates ----------------------------
def parse_pivot_q(s, m, card, ctx):
    ID = '(?P<id>' + ID_TOKEN + ')'
    col = m.pcolobj
    x = P(r'[Hh]ow many (?P<ent>.+?) have an? (?P<col>\S+) of (?P<pred>.+) in (?P<w>Week \d+)', s)
    if x:
        chk(x.group('col'), m)
        return dict(op='p_count', week=x.group('w'), cond=parse_pred(col, x.group('pred'), ctx))
    x = P(r'[Ww]hich (?P<ent>.+?) has the (?P<ext>lowest|highest) total (?P<col>\S+)', s)
    if x:
        chk(x.group('col'), m)
        return dict(op='p_argtotal', ext=x.group('ext'))
    x = P(r'Is the (?P<col>\S+) of ' + ID + r' in (?P<w>Week \d+) (?P<pred>.+)', s)
    if x:
        chk(x.group('col'), m)
        return dict(op='p_lookup', id=x.group('id'), week=x.group('w'), cond=parse_pred(col, x.group('pred'), ctx))
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the (?P<col>\S+) of ' + ID + r' in (?P<w>Week \d+)', s)
    if x:
        chk(x.group('col'), m)
        return dict(op='p_value', id=x.group('id'), week=x.group('w'))
    x = P(r'(?:In (?P<unit>[^,]+), )?[Ww]hat is the total (?P<col>\S+) of ' + ID, s)
    if x:
        chk(x.group('col'), m)
        return dict(op='p_total', id=x.group('id'))
    raise ParseError('pivot template: ' + s[:70])


def chk(c, m):
    if c != m.pcol:
        raise ParseError('pivot column %s vs %s' % (c, m.pcol))


# ---------------------------------------------------------------- S6 log templates ------------------------------
def parse_line_phrase(t, m, card, ctx):
    """Closed line-phrase list -> list of line atoms (all on one line). Returns (atoms, rest_after)."""
    s = t.strip()
    atoms = []
    lv = card.levels or []
    LV = '(?P<lv>' + '|'.join(re.escape(x) for x in lv) + ')' if lv else '(?P<lv>[A-Z]+)'
    x = re.match(r'(?:an? |no )?(?:line|lines) at ' + LV + r' or (?P<d>higher|lower)\b', s) or \
        re.match(r'(?:an? |no )?(?:line|lines) (?P<d>at least|at most|above|below) ' + LV + r'\b', s)
    if x:
        d = x.group('d')
        op = {'higher': '>=', 'lower': '<=', 'at least': '>=', 'at most': '<=', 'above': '>', 'below': '<'}[d]
        atoms.append(('lvlcmp', op, x.group('lv')))
        s = s[x.end():].strip()
    else:
        x = re.match(r'(?:an? |no )?(?P<lv>[A-Z]+) (?:line|lines)\b', s)
        if x:
            atoms.append(('lvl', x.group('lv')))
            s = s[x.end():].strip()
        else:
            x = re.match(r'(?:an? |no )?(?:line|lines)\b', s)
            if not x:
                raise ParseError('line phrase: ' + s[:40])
            s = s[x.end():].strip()
    x = re.match(r'from (?P<c>' + ID_TOKEN + r')\b', s)
    if x:
        atoms.append(('comp', x.group('c')))
        s = s[x.end():].strip()
    x = re.match(r'with (?P<k>[a-z_]+)=(?P<v>\S+)', s)
    if x:
        atoms.append(('kv', x.group('k'), x.group('v')))
        s = s[x.end():].strip()
    return atoms, s


def line_sql(atoms, card, a='L'):
    parts = []
    for at in atoms:
        if at[0] == 'lvl':
            parts.append("%s.level = %s" % (a, sqlstr(at[1])))
        elif at[0] == 'lvlcmp':
            if not card.levels or at[2] not in card.levels:
                raise ParseError('level order not stated')
            parts.append('%s.lrank %s %d' % (a, at[1], card.levels.index(at[2])))
        elif at[0] == 'comp':
            parts.append('%s.comp = %s' % (a, sqlstr(at[1])))
        elif at[0] == 'kv':
            parts.append('EXISTS (SELECT 1 FROM KV WHERE KV.pos = %s.pos AND KV.k = %s AND KV.v = %s)' % (
                a, sqlstr(at[1]), sqlstr(at[2])))
        elif at[0] == 'win':
            _, lo, li, hi, hi_i = at
            if lo is not None:
                parts.append('%s.t %s %d' % (a, '>=' if li else '>', lo))
            if hi is not None:
                parts.append('%s.t %s %d' % (a, '<=' if hi_i else '<', hi))
        else:
            raise Unsupported('line atom ' + at[0])
    return ' AND '.join(parts) if parts else '1'


def take_window(s, ctx):
    """Optional trailing window phrase; returns (atom or None, rest)."""
    s = s.strip()
    if not s:
        return None, s
    lo, li, hi, hi_i = time_window(s, ctx, True)
    return ('win', lo, li, hi, hi_i), ''


def parse_log_q(s, m, card, ctx):
    x = P(r'[Hh]ow many (?P<lp>.+?) were logged(?: (?P<w>.+))?', s)
    if x:
        atoms, rest = parse_line_phrase(x.group('lp'), m, card, ctx)
        if rest:
            raise ParseError('line phrase tail ' + rest)
        if x.group('w'):
            atoms.append(take_window(x.group('w'), ctx)[0])
        return dict(op='l_count', atoms=atoms)
    x = P(r'Is the number of (?P<rest>.+)', s)
    if x:
        body, op, v = split_trailing_cmp(x.group('rest'), lit_count)
        atoms, rest = parse_line_phrase(body, m, card, ctx)
        rest = re.sub(r'^logged\b', '', rest).strip()
        if rest:
            atoms.append(take_window(rest, ctx)[0])
        return dict(op='l_count', atoms=atoms, cmp=(op, v))
    x = P(r'Is there (?P<lp>(?:an?|no) .+)', s)
    if x:
        neg = x.group('lp').startswith('no ')
        atoms, rest = parse_line_phrase(x.group('lp'), m, card, ctx)
        rest = re.sub(r'^logged\b', '', rest).strip()
        if rest:
            atoms.append(take_window(rest, ctx)[0])
        return dict(op='l_exists', atoms=atoms, neg_extra=1 if neg else 0)
    x = P(r'[Ww]hich (?P<cn>[a-z ]+?) logged the (?P<ext>most|fewest) (?P<lp>.+)', s)
    if x:
        atoms, rest = parse_line_phrase(x.group('lp'), m, card, ctx)
        if rest:
            atoms.append(take_window(rest, ctx)[0])
        return dict(op='l_comp_arg', atoms=atoms, ext=x.group('ext'))
    x = P(r'Does (?:request|session) (?P<id>' + ID_TOKEN + r') (?P<n>not )?have (?P<lp>.+)', s)
    if x:
        conds = parse_req_cond(x.group('lp'), m, card, ctx)
        return dict(op='l_req_has', id=x.group('id'), rcond=conds, neg_extra=1 if x.group('n') else 0)
    x = P(r'[Ww]hich (?:requests|sessions) have (?P<lp>.+)', s)
    if x:
        return dict(op='l_req_select', rcond=parse_req_cond(x.group('lp'), m, card, ctx))
    x = P(r'[Ww]hich of these (?:requests|sessions) has (?P<lp>.+)', s)
    if x:
        return dict(op='l_req_pick', rcond=parse_req_cond(x.group('lp'), m, card, ctx))
    x = P(r'(?:.*\. )?[Aa]t what time was the (?P<fl>first|last) (?P<lp>.+?) logged(?: (?P<w>.+))?', s)
    if x:
        atoms, rest = parse_line_phrase('a ' + x.group('lp'), m, card, ctx)
        if rest:
            raise ParseError('first/last tail')
        if x.group('w'):
            atoms.append(take_window(x.group('w'), ctx)[0])
        return dict(op='l_time', fl=x.group('fl'), atoms=atoms)
    raise ParseError('log template: ' + s[:80])


def parse_req_cond(t, m, card, ctx):
    """T41 request condition: line phrases joined by 'and' / 'or'; 'no <..> line' negates a lifted atom."""
    s = t.strip()
    parts = re.split(r' (and|or) (?=(?:an?|no) )', s)
    items, conns = [], []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            conns.append(p); continue
        neg = p.startswith('no ')
        atoms, rest = parse_line_phrase(p, m, card, ctx)
        if rest:
            raise ParseError('request phrase tail: ' + rest)
        items.append(('nolift' if neg else 'lift', atoms))
    if len(set(conns)) > 1:
        raise ParseError('mixed and/or')
    return (conns[0] if conns else 'and', items)
