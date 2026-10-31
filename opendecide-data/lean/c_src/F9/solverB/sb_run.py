# F9 solver B, part 5: execution on sqlite (T4 masks, T5 completion loop), option mapping. G0_SPEC.md v7 only.
import re, itertools
from fractions import Fraction
from sb_parse import ParseError, parse_number, parse_date, parse_datetime, fmt_date
from sb_model import SCALE, fold, q, sqlstr, ID_RX
from sb_query import cat_values, lit_num
from sb_eval import (to_sql, used_cols, notnull, line_sql, Unsupported, PYOP)

MAX_COMPLETIONS = 20000


class Undecided(Exception):
    pass


def one(db, sql):
    return db.execute(sql).fetchone()


def allrows(db, sql):
    return db.execute(sql).fetchall()


def frac(sumv, cnt):
    return Fraction(sumv, cnt * SCALE)


def rhu(x, n):
    """Display rounding (T22): halves away from zero, integer arithmetic."""
    p, qd = x.numerator, x.denominator
    sgn = -1 if p < 0 else 1
    v = (2 * abs(p) * 10 ** n + qd) // (2 * qd)
    return Fraction(sgn * v, 10 ** n)


# ---------------------------------------------------------------- T5 domains ------------------------------------
def parse_domains(card, cols_by_name):
    """card.domains_text -> {col: [storage values]} (T5)."""
    out, catvals = {}, {}
    t = getattr(card, 'domains_text', None)
    if not t:
        return out, catvals
    for sent in re.split(r'(?<=\.) (?=[a-z])', t.strip()):
        sent = sent.strip().rstrip('.')
        m = re.match(r'^(\S+) is one of (.+)$', sent)
        if m:
            vals = [fold(v) for v in m.group(2).split(', ')]
            out[m.group(1)] = vals; catvals[m.group(1)] = set(vals)
            continue
        m = re.match(r'^(\S+) is a whole number of (.+?) from (\S+) to (\S+)$', sent)
        if m:
            lo, hi = int(parse_number(m.group(3), card)), int(parse_number(m.group(4), card))
            out[m.group(1)] = [v * SCALE for v in range(lo, hi + 1)]
            continue
        m = re.match(r'^(\S+) is from (\S+) to (\S+) (.+?) in steps of (\S+)$', sent)
        if m:
            lo, hi, st = (parse_number(m.group(i), card) for i in (2, 3, 5))
            vals, v = [], lo
            while v <= hi:
                vals.append(int(v * SCALE)); v += st
            out[m.group(1)] = vals
            continue
        m = re.match(r'^(\S+) falls from (.+?) to (.+?), both dates included$', sent)
        if m:
            a, b = parse_date(m.group(2), card), parse_date(m.group(3), card)
            out[m.group(1)] = list(range(a, b + 1))
            continue
        raise ParseError('domain sentence: ' + sent[:60])
    return out, catvals


# ---------------------------------------------------------------- core ops --------------------------------------
def tie_order(m, ctx, alias, cols):
    """T24 key chain -> ORDER BY items (columns of the same table)."""
    ch = ctx.card.tie_chain or []
    out = []
    for cn, d in ch:
        if cn not in cols:
            raise ParseError('tie column %s not in table' % cn)
        out.append('%s.%s %s' % (alias, q(cn), 'ASC' if d == 'min' else 'DESC'))
    return out


def run_single(Q, m, ctx, row):
    db, card = m.db, ctx.card
    op = Q['op']
    idc = q(m.idc) if m.idc else None
    if op == 'presence':
        n = one(db, 'SELECT COUNT(*) FROM r WHERE r.%s = %s' % (q(Q['col']), sqlstr(Q['id'])))[0]
        return ('bool', n > 0)
    if op == 'lookup_cond':
        u = used_cols(Q['cond'], ctx)
        rs = allrows(db, 'SELECT (%s), (%s) FROM r WHERE r.%s = %s' % (to_sql(Q['cond'], 'r', ctx), notnull(u), idc,
                                                                    sqlstr(Q['id'])))
        if not rs:
            if card.world == 'T2':
                return ('cbd',)
            return ('none',)
        if len(rs) > 1:
            raise ParseError('lookup of duplicated id')
        v, nn = rs[0]
        if not nn:
            raise Undecided('lookup reads an unknown cell (T4)')
        return ('bool', bool(v))
    if op == 'lookup_val':
        col = Q['col']
        rs = allrows(db, 'SELECT r.%s FROM r WHERE r.%s = %s' % (q(col.name), idc, sqlstr(Q['id'])))
        if not rs:
            return ('cbd',) if card.world == 'T2' else ('none',)
        if len(rs) > 1:
            raise ParseError('lookup of duplicated id')
        v = rs[0][0]
        if v is None:
            raise Undecided('lookup value unknown (T4)')
        return val_ans(v, col)
    cond = Q.get('cond', ('true',))
    u = used_cols(cond, ctx)
    W = '(%s) AND (%s)' % (notnull(u), to_sql(cond, 'r', ctx))
    if op == 'exists':
        return ('bool', one(db, 'SELECT COUNT(*) FROM r WHERE ' + W)[0] > 0)
    if op == 'forall':
        u2 = used_cols(Q['a'], ctx) | used_cols(Q['b'], ctx)
        nn = notnull(u2)
        na = one(db, 'SELECT COUNT(*) FROM r WHERE (%s) AND (%s)' % (nn, to_sql(Q['a'], 'r', ctx)))[0]
        if na == 0:
            raise Undecided('forall over empty set (T23 never generated)')
        bad = one(db, 'SELECT COUNT(*) FROM r WHERE (%s) AND (%s) AND NOT (%s)' % (
            nn, to_sql(Q['a'], 'r', ctx), to_sql(Q['b'], 'r', ctx)))[0]
        return ('bool', bad == 0)
    if op in ('count', 'count_val'):
        n = one(db, 'SELECT COUNT(*) FROM r WHERE ' + W)[0]
        if 'cmp' in Q:
            return ('bool', PYOP[Q['cmp'][0]](n, Q['cmp'][1]))
        return ('int', n)
    if op == 'count_distinct':
        col = Q['col']
        W2 = '(%s) AND (%s)' % (notnull(u | {col.name}), to_sql(cond, 'r', ctx))
        return ('int', one(db, 'SELECT COUNT(DISTINCT r.%s) FROM r WHERE %s' % (q(col.name), W2))[0])
    if op in ('sum', 'mean', 'maxv', 'minv'):
        col = Q['col']
        W2 = '(%s) AND (%s)' % (notnull(u | {col.name}), to_sql(cond, 'r', ctx))
        s, n, mx, mn = one(db, 'SELECT SUM(r.{0}), COUNT(r.{0}), MAX(r.{0}), MIN(r.{0}) FROM r WHERE {1}'.format(
            q(col.name), W2))
        if op == 'sum':
            v = Fraction(s or 0, SCALE)
            if 'cmp' in Q:
                return ('bool', PYOP[Q['cmp'][0]](v, Fraction(Q['cmp'][1], SCALE)))
            return ('num', v, 'exact', col)
        if n == 0:
            if 'cmp' in Q:
                raise Undecided('mean of empty set (T23)')
            return ('none',)
        if op == 'mean':
            v = frac(s, n)
            if 'cmp' in Q:
                return ('bool', PYOP[Q['cmp'][0]](v, Fraction(Q['cmp'][1], SCALE)))
            return ('num', v, 'mean', col)
        return val_ans(mx if op == 'maxv' else mn, col)
    if op in ('argmax', 'argmin'):
        col = Q['col']
        chain = [c for c, _ in (card.tie_chain or [])]
        W2 = '(%s) AND (%s)' % (notnull(u | {col.name} | set(chain)), to_sql(cond, 'r', ctx))
        order = ['r.%s %s' % (q(col.name), 'DESC' if op == 'argmax' else 'ASC')]
        rs = allrows(db, 'SELECT r.%s, r.%s FROM r WHERE %s ORDER BY %s' % (
            idc, q(col.name), W2, ', '.join(order + tie_order(m, ctx, 'r', m.cols))))
        if not rs:
            return ('none',)
        top = [x for x in rs if x[1] == rs[0][1]]
        if len(top) > 1:
            if card.tie_option:
                return ('tie',)
            if not card.tie_chain:
                raise Undecided('tie with no stated tie rule')
        return ('id', rs[0][0])
    if op == 'select':
        rs = allrows(db, 'SELECT r.%s FROM r WHERE %s' % (idc, W))
        return ('set', frozenset(x[0] for x in rs))
    if op == 'pick':
        opts = [o for o in row['options'] if ID_RX.match(o)]
        rs = allrows(db, 'SELECT DISTINCT r.%s FROM r WHERE %s AND r.%s IN (%s)' % (
            idc, W, idc, ','.join(sqlstr(o) for o in opts) or "''"))
        return ('pick', frozenset(x[0] for x in rs))
    if op == 'count_compare':
        na = one(db, 'SELECT COUNT(*) FROM r WHERE (%s) AND (%s)' % (notnull(used_cols(Q['a'], ctx)),
                                                                     to_sql(Q['a'], 'r', ctx)))[0]
        nb = one(db, 'SELECT COUNT(*) FROM r WHERE (%s) AND (%s)' % (notnull(used_cols(Q['b'], ctx)),
                                                                     to_sql(Q['b'], 'r', ctx)))[0]
        return ('bool', PYOP[Q['cmp']](na, nb))
    if op == 'compare':
        va = agg_value(m, ctx, Q['agg'], Q['col'], Q['a'])
        vb = agg_value(m, ctx, Q['agg2'], Q['col2'], Q['b'])
        return ('bool', PYOP[Q['cmp']](va, vb))
    raise Unsupported('op ' + op)


def agg_value(m, ctx, agg, col, cond):
    u = used_cols(cond, ctx) | {col.name}
    s, n = one(m.db, 'SELECT SUM(r.{0}), COUNT(r.{0}) FROM r WHERE ({1}) AND ({2})'.format(
        q(col.name), notnull(u), to_sql(cond, 'r', ctx)))
    if agg == 'total':
        return Fraction(s or 0, SCALE)
    if n == 0:
        raise Undecided('compare of an empty-group average (T23)')
    return frac(s, n)


def val_ans(v, col):
    if col.typ == 'num':
        return ('num', Fraction(v, SCALE), 'exact', col)
    if col.typ == 'date':
        return ('date', v)
    if col.typ == 'dt':
        return ('dt', v)
    if col.typ == 'bool':
        return ('boolv', v)
    if col.typ == 'id':
        return ('idv', v)
    return ('cat', v, col)


# ---------------------------------------------------------------- S3 ---------------------------------------------
def run_join(Q, m, ctx, row):
    db, card = m.db, ctx.card
    op = Q['op']
    K = q(m.key)
    dcond = Q.get('dcond', ('true',))
    fcond = Q.get('fcond', ('true',))
    ud, uf = used_cols(dcond, ctx), used_cols(fcond, ctx)
    Wd = '(%s) AND (%s)' % (notnull(ud, 'd'), to_sql(dcond, 'd', ctx))
    Wf = '(%s) AND (%s)' % (notnull(uf, 'f'), to_sql(fcond, 'f', ctx))
    ent = Q.get('ent')
    if ent is not None:
        if not one(db, 'SELECT COUNT(*) FROM d WHERE d.%s = %s' % (K, sqlstr(ent)))[0]:
            return ('none',) if op not in ('j_exists',) else ('bool', False)
        Wd += ' AND d.%s = %s' % (K, sqlstr(ent))
    if op in ('j_count', 'j_sum', 'j_mean', 'j_exists'):
        col = Q.get('col')
        cexpr = 'f.%s' % q(col.name) if col else 'NULL'
        extra = (' AND f.%s IS NOT NULL' % q(col.name)) if col else ''
        s, n = one(db, 'SELECT SUM(%s), COUNT(*) FROM f JOIN d ON f.%s = d.%s WHERE %s AND %s%s' % (
            cexpr, K, K, Wd, Wf, extra))
        if op == 'j_exists':
            return ('bool', n > 0)
        if op == 'j_count':
            if 'cmp' in Q:
                return ('bool', PYOP[Q['cmp'][0]](n, Q['cmp'][1]))
            return ('int', n)
        if op == 'j_sum':
            v = Fraction(s or 0, SCALE)
            if 'cmp' in Q:
                return ('bool', PYOP[Q['cmp'][0]](v, Fraction(Q['cmp'][1], SCALE)))
            return ('num', v, 'exact', col)
        if n == 0:
            if 'cmp' in Q:
                raise Undecided('mean of empty set')
            return ('none',)
        v = frac(s, n)
        if 'cmp' in Q:
            return ('bool', PYOP[Q['cmp'][0]](v, Fraction(Q['cmp'][1], SCALE)))
        return ('num', v, 'mean', col)
    if op == 'j_argmax':
        chain = [c for c, _ in (card.tie_chain or [])]
        col = Q['col']
        agg = 'COALESCE(SUM(f.%s), 0)' % q(col.name) if col else 'COUNT(f._rid)'
        fextra = (' AND f.%s IS NOT NULL' % q(col.name)) if col else ''
        sql = ('SELECT d.%s, %s AS v FROM d LEFT JOIN (SELECT * FROM f WHERE %s%s) f ON f.%s = d.%s '
               'WHERE %s AND (%s) GROUP BY d._rid ORDER BY v %s, %s') % (
            K, agg, Wf, fextra, K, K, Wd, notnull(set(chain), 'd'), 'DESC' if Q['ext'] == 'highest' else 'ASC',
            ', '.join(tie_order(m, ctx, 'd', m.dcols)) or 'd._rid')
        rs = allrows(db, sql)
        if not rs:
            return ('none',)
        if all(x[1] == 0 for x in rs):
            # never generated (T23, F9-R5-03); T29 zeros + T24 chain still define an answer: compute it, flag the row
            ctx.violations.add('T23/F9-R5-03: S3 group_argmax with every entity at 0 (never generated)')
        top = [x for x in rs if x[1] == rs[0][1]]
        if len(top) > 1:
            if card.tie_option:
                return ('tie',)
            if not card.tie_chain:
                raise Undecided('tie without tie rule')
        return ('id', rs[0][0])
    if op in ('j_select', 'j_pick'):
        sql = 'SELECT d.%s FROM d WHERE %s AND EXISTS (SELECT 1 FROM f WHERE f.%s = d.%s AND %s)' % (
            K, Wd, K, K, Wf)
        if op == 'j_pick':
            opts = [o for o in row['options'] if ID_RX.match(o)]
            sql += ' AND d.%s IN (%s)' % (K, ','.join(sqlstr(o) for o in opts) or "''")
            return ('pick', frozenset(x[0] for x in allrows(db, sql)))
        return ('set', frozenset(x[0] for x in allrows(db, sql)))
    raise Unsupported('join op ' + op)


# ---------------------------------------------------------------- S5 ---------------------------------------------
def run_pivot(Q, m, ctx, row):
    db, card = m.db, ctx.card
    op = Q['op']
    col = m.pcolobj
    if op in ('p_lookup', 'p_value'):
        rs = allrows(db, 'SELECT val, marked FROM c WHERE ent = %s AND week = %s' % (sqlstr(Q['id']),
                                                                                     sqlstr(Q['week'])))
        if not rs:
            return ('none',)
        v, mk = rs[0]
        if mk:
            raise Undecided('question names a marked cell (never generated)')
        if v is None:
            raise Undecided('unknown pivot cell')
        if op == 'p_value':
            return ('num', Fraction(v, SCALE), 'exact', col)
        c = Q['cond']
        return ('bool', bool(one(db, 'SELECT (%s) FROM (SELECT %d AS %s) r' % (to_sql(c, 'r', ctx), v,
                                                                              q(col.name)))[0]))
    if op == 'p_count':
        c = Q['cond']
        n = one(db, 'SELECT COUNT(*) FROM (SELECT ent, val AS %s FROM c WHERE week = %s AND marked = 0 AND val IS '
                    'NOT NULL) r WHERE %s' % (q(col.name), sqlstr(Q['week']), to_sql(c, 'r', ctx)))[0]
        return ('int', n)
    if op in ('p_argtotal', 'p_total'):
        rs = allrows(db, 'SELECT ent, SUM(CASE WHEN marked = 0 THEN val ELSE 0 END) AS v FROM c GROUP BY ent')
        if op == 'p_total':
            d = dict(rs)
            return ('num', Fraction(d[Q['id']], SCALE), 'exact', col)
        best = max(x[1] for x in rs) if Q['ext'] == 'highest' else min(x[1] for x in rs)
        top = sorted([x[0] for x in rs if x[1] == best])
        if len(top) > 1:
            if card.tie_option:
                return ('tie',)
            ch = card.tie_chain
            if not ch or len(ch) != 1:
                raise Undecided('pivot tie rule')
            return ('id', top[0] if ch[0][1] == 'min' else top[-1])
        return ('id', top[0])
    raise Unsupported('pivot op ' + op)


# ---------------------------------------------------------------- S6 ---------------------------------------------
def lifted(rcond, rid, ctx):
    conn, items = rcond
    parts = []
    for kind, atoms in items:
        e = 'EXISTS (SELECT 1 FROM L WHERE L.req = %s AND %s)' % (rid, line_sql(atoms, ctx.card))
        parts.append(e if kind == 'lift' else 'NOT ' + e)
    return '(' + (' AND ' if conn == 'and' else ' OR ').join(parts) + ')'


def run_log(Q, m, ctx, row):
    db, card = m.db, ctx.card
    op = Q['op']
    if op in ('l_count', 'l_exists'):
        n = one(db, 'SELECT COUNT(*) FROM L WHERE ' + line_sql(Q['atoms'], card))[0]
        if op == 'l_exists':
            return ('bool', (n > 0) != bool(Q.get('neg_extra')))
        if 'cmp' in Q:
            return ('bool', PYOP[Q['cmp'][0]](n, Q['cmp'][1]))
        return ('int', n)
    if op == 'l_comp_arg':
        rs = allrows(db, 'SELECT c.comp, (SELECT COUNT(*) FROM L WHERE L.comp = c.comp AND %s) AS v FROM '
                         '(SELECT DISTINCT comp FROM L) c' % line_sql(Q['atoms'], card))
        if all(x[1] == 0 for x in rs):
            ctx.violations.add('T23/F9-R5-03: S6 component pick with every component at 0 (never generated)')
        best = max(x[1] for x in rs) if Q['ext'] == 'most' else min(x[1] for x in rs)
        top = sorted(x[0] for x in rs if x[1] == best)
        if len(top) > 1:
            if card.tie_option:
                return ('tie',)
            ch = card.tie_chain
            if not ch:
                raise Undecided('component tie without rule')
            return ('id', top[0] if ch[0][1] == 'min' else top[-1])
        return ('id', top[0])
    if op.startswith('l_req') and not Q.get('_alt'):
        conn, items = Q['rcond']
        if any(len(at) > 1 for k, at in items):
            # outside the closed T41 line-phrase list (1.2, F9-R2-03): a compound condition on one line.
            new = []
            for k, at in items:
                new += [(k, [x]) for x in at] if (len(at) > 1 and k == 'lift') else [(k, at)]
            Q2 = dict(Q, rcond=('and' if len(items) == 1 else conn, new), _alt=1)
            same = run_log(Q2, m, ctx, row) == run_log(dict(Q, _alt=1), m, ctx, row)
            ctx.notes.add('1.2/F9-R2-03: compound one-line phrase in a request condition (outside the closed '
                          'line-phrase list); same-line and per-atom readings %s' % ('agree' if same else 'DIFFER'))
            # G0 1.2 (line 192) / F9-R2-03: "a compound condition on one line ... is never asked": always a
            # never-generated violation, whether or not the two readings agree (G2 repair r03)
            ctx.violations.add('1.2/F9-R2-03: compound one-line request phrase (never asked)%s'
                               % ('' if same else '; label depends on the reading'))
    if op == 'l_req_has':
        if not one(db, 'SELECT COUNT(*) FROM L WHERE req = %s' % sqlstr(Q['id']))[0]:
            raise Undecided('request id not in log')
        v = one(db, 'SELECT ' + lifted(Q['rcond'], sqlstr(Q['id']), ctx))[0]
        return ('bool', bool(v) != bool(Q.get('neg_extra')))
    if op in ('l_req_select', 'l_req_pick'):
        sql = 'SELECT r.req FROM (SELECT DISTINCT req FROM L WHERE req IS NOT NULL) r WHERE ' + lifted(
            Q['rcond'], 'r.req', ctx)
        ids = frozenset(x[0] for x in allrows(db, sql))
        if op == 'l_req_pick':
            return ('pick', frozenset(i for i in ids if i in row['options']))
        return ('set', ids)
    if op == 'l_time':
        v = one(db, 'SELECT %s(t) FROM L WHERE %s' % ('MIN' if Q['fl'] == 'first' else 'MAX',
                                                       line_sql(Q['atoms'], card)))[0]
        if v is None:
            return ('none',)
        return ('dt', v)
    raise Unsupported('log op ' + op)


def run_once(Q, m, ctx, row):
    if m.kind == 'log':
        a = run_log(Q, m, ctx, row)
    elif m.kind == 'pivot':
        a = run_pivot(Q, m, ctx, row)
    elif m.kind == 'join' and Q['op'].startswith('j_'):
        a = run_join(Q, m, ctx, row)
    else:
        if m.kind == 'join':
            # single-table templates on S3 address the dimension table
            m.db.execute('DROP VIEW IF EXISTS r')
            m.db.execute('CREATE TEMP VIEW r AS SELECT * FROM d')
        a = run_single(Q, m, ctx, row)
    if a[0] == 'bool':
        n = Q.get('neg', 0) + (Q.get('neg_extra', 0) if m.kind in ('join',) else 0)
        if n % 2:
            a = ('bool', not a[1])
    return a


# ---------------------------------------------------------------- columns read (T4 / T5) ------------------------
def read_cells(Q, m, ctx):
    """Unknown cells that can change the answer: those in columns Q reads (and, for lookups, on that row only)."""
    cols = set()
    for k in ('cond', 'a', 'b', 'dcond', 'fcond'):
        if k in Q:
            cols |= used_cols(Q[k], ctx)
    for k in ('col', 'col2'):
        if Q.get(k) is not None and hasattr(Q[k], 'name'):
            cols.add(Q[k].name)
    if Q['op'] in ('argmax', 'argmin', 'j_argmax'):
        cols |= {c for c, _ in (ctx.card.tie_chain or [])}
    cells = [c for c in m.unknown if c[2] in cols]
    if Q['op'] in ('lookup_cond', 'lookup_val'):
        rids = {x[0] for x in m.db.execute('SELECT _rid FROM %s WHERE %s = %s' % (
            'd' if m.kind == 'join' else 'r', q(m.idc), sqlstr(Q['id'])))}
        cells = [c for c in cells if c[1] in rids]
    return cells


def evaluate(Q, m, ctx, row, mapper):
    """Returns the mapped answer (option text or 0/1). T5 cards: every completion of the read unknown cells."""
    card = ctx.card
    cells = read_cells(Q, m, ctx) if card.unk_mode == 'T5' else []
    if not cells:
        return mapper(run_once(Q, m, ctx, row))
    doms = []
    for (tn, rid, cn) in cells:
        if cn not in ctx.domains:
            raise ParseError('T5 unknown cell in %s without a stated domain' % cn)
        doms.append(ctx.domains[cn])
    total = 1
    for d in doms:
        total *= len(d)
    if total > MAX_COMPLETIONS:
        raise Undecided('completion product %d > 20000' % total)
    seen = set()
    for combo in itertools.product(*doms):
        for (tn, rid, cn), v in zip(cells, combo):
            m.db.execute('UPDATE %s SET %s = ? WHERE _rid = ?' % (tn, q(cn)), (v, rid))
        try:
            seen.add(mapper(run_once(Q, m, ctx, row)))
        except Undecided as e:
            seen.add('UNDECIDED:' + str(e))
        if len(seen) > 1:
            break
    for (tn, rid, cn) in cells:
        m.db.execute('UPDATE %s SET %s = NULL WHERE _rid = ?' % (tn, q(cn)), (rid,))
    if len(seen) == 1:
        v = seen.pop()
        if isinstance(v, str) and v.startswith('UNDECIDED:'):
            raise Undecided(v)
        return v
    if row['qtype'] == 'noul':
        raise Undecided('T5 yes/no row not decided by the completions')
    if card.cbd in row['options']:
        return card.cbd
    raise Undecided('T5 answer varies but no cannot-be-determined option')


# ---------------------------------------------------------------- option mapping --------------------------------
def make_mapper(row, m, ctx, Q):
    card = ctx.card
    opts = row['options'] or []

    def special(name):
        if name == 'none':
            hits = [t for t in card.no_records if t in opts]
            if len(set(hits)) > 1:
                raise Undecided('two no-record options shown')
            return hits[0] if hits else None
        t = {'cbd': card.cbd, 'none_of': card.none_of, 'tie': card.tie_option}[name]
        return t if t in opts else None

    def fallback():
        if card.none_of in opts:
            return card.none_of
        raise Undecided('answer not among options and no none-of-these')

    def mapper(a):
        if row['qtype'] == 'noul':
            if a[0] != 'bool':
                raise Undecided('yes/no row got %s' % a[0])
            return 1 if a[1] else 0
        k = a[0]
        if k == 'bool':
            raise Undecided('choice row got a yes/no answer')
        if k in ('cbd', 'none', 'tie'):
            s = special(k)
            if s is None:
                if k == 'none':
                    return fallback()
                raise Undecided('%s answer but option not shown' % k)
            return s
        if k == 'id':
            return a[1] if a[1] in opts else fallback()
        if k == 'set':
            if not a[1]:
                s = special('none')
                return s if s else fallback()
            for o in opts:
                ids = re.findall(r'[A-Z][A-Z0-9]*-\d+', o)
                if ids and o.endswith(' only') and frozenset(ids) == a[1]:
                    return o
            return fallback()
        if k == 'pick':
            if len(a[1]) == 1:
                return next(iter(a[1]))
            if not a[1]:
                if card.none_of in opts:
                    return card.none_of
                s = special('none')
                if s:
                    return s
                raise Undecided('condition pick: no option meets')
            raise Undecided('condition pick: %d options meet' % len(a[1]))
        hits = [o for o in opts if opt_equals(o, a, ctx)]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            raise Undecided('value matches %d options' % len(hits))
        return fallback()
    return mapper


def opt_equals(o, a, ctx):
    card = ctx.card
    k = a[0]
    try:
        if k == 'int':
            return re.fullmatch(r'\d+', o.strip()) is not None and int(o) == a[1]
        if k == 'num':
            v = parse_number(o, card)
            g = a[1]
            if a[2] == 'mean' and card.round_n is not None:
                g = rhu(g, card.round_n)
            return v == g
        if k == 'date':
            return parse_date(o, card) == a[1]
        if k == 'dt':
            return parse_datetime(o, card) == a[1]
        if k == 'cat':
            col = a[2]
            if fold(o) == a[1]:
                return True
            if col.legend and o in col.legend and fold(col.legend[o]) == a[1]:
                return True
            return False
        if k == 'idv':
            return o == a[1]
        if k == 'boolv':
            return False
    except (ParseError, ValueError):
        return False
    return False
