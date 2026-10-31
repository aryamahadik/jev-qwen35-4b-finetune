# F9 solver B, part 2: typed model + sqlite load. Written from G0_SPEC.md v7 (1.1, 1.6, section 2, 3.3-3.6) only.
import re, sqlite3, itertools
from fractions import Fraction
from sb_parse import (ParseError, parse_number, parse_date, parse_datetime, log_line, num_decimals, ALLMON)

SCALE = 10 ** 6
ID_RX = re.compile(r'^[A-Z][A-Z0-9]*-\d+$')
UNK_DEFAULT = {'unknown', 'not recorded'}


def fold(s):
    return s.strip().casefold()


class Col:
    def __init__(self, name, typ, unit=None):
        self.name, self.typ, self.unit = name, typ, unit
        self.dp = 0
        self.values = set()      # folded category values seen
        self.disp = {}           # folded -> display
        self.legend = None       # code -> meaning (masked)


def split_hdr(h):
    m = re.match(r'^(\S+?)\s*\((.+)\)$', h.strip())
    if m:
        return m.group(1), m.group(2)
    return h.strip(), None


def q(name):
    return '"' + name.replace('"', '""') + '"'


def sqlstr(s):
    return "'" + s.replace("'", "''") + "'"


class Model:
    pass


def _unk(card):
    return set(card.unk_tokens) | UNK_DEFAULT


def infer_type(vals, card, colname):
    """vals: list of raw values (str or native), UNKNOWN already removed."""
    if colname in card.bools:
        return 'bool'
    if not vals:
        return 'cat'
    if all(isinstance(v, bool) for v in vals):
        return 'bool'
    if all(isinstance(v, (int, Fraction)) and not isinstance(v, bool) for v in vals):
        return 'num'
    if all(isinstance(v, float) for v in vals) or all(isinstance(v, (int, float, Fraction)) and not isinstance(v, bool)
                                                      for v in vals):
        return 'num'
    if not all(isinstance(v, str) for v in vals):
        raise ParseError('mixed types in ' + colname)
    if all(ID_RX.match(v) for v in vals):
        return 'id'
    for typ, fn in (('date', parse_date), ('dt', parse_datetime), ('num', parse_number)):
        try:
            for v in vals:
                fn(v, card)
            return typ
        except (ParseError, ValueError):
            pass
    if all(v in ('true', 'false') for v in vals):
        return 'bool'
    return 'cat'


def conv(v, col, card):
    """raw -> sqlite value."""
    t = col.typ
    if t == 'num':
        if isinstance(v, str):
            col.dp = max(col.dp, num_decimals(v, card))
            f = parse_number(v, card)
        elif isinstance(v, float):
            f = Fraction(repr(v)); col.dp = max(col.dp, len(repr(v).split('.')[1]) if '.' in repr(v) else 0)
        elif isinstance(v, Fraction):
            f = v
        else:
            f = Fraction(v)
        x = f * SCALE
        if x.denominator != 1:
            raise ParseError('scale')
        return int(x)
    if t == 'date':
        return parse_date(v, card)
    if t == 'dt':
        return parse_datetime(v, card)
    if t == 'bool':
        if isinstance(v, bool):
            return int(v)
        if col.name in card.bools:
            tt, ff = card.bools[col.name]
            if v == tt:
                return 1
            if v == ff:
                return 0
            raise ParseError('bool token ' + v)
        return {'true': 1, 'false': 0}[v]
    if t == 'id':
        return v
    # category / text
    s = v if isinstance(v, str) else str(v)
    if col.legend:
        if s not in col.legend:
            raise ParseError('code not in legend ' + s)
        s = col.legend[s]
    col.values.add(fold(s)); col.disp.setdefault(fold(s), s)
    return fold(s)


def _flat_table(tab, card):
    """Return (cols list of Col, list of row dicts name->raw-or-None). Unit from header suffix or card."""
    unk = _unk(card)
    names, units = [], {}
    for h in tab.cols:
        n, u = split_hdr(h)
        names.append(n); units[n] = u
    rows = []
    for r in tab.rows:
        d = {}
        for h in tab.cols:
            n, _ = split_hdr(h)
            v = r[h]
            d[n] = None if (v is None or (isinstance(v, str) and v.strip() in unk)) else v
        rows.append(d)
    return names, units, rows


def make_cols(names, units, rows, card):
    cols = {}
    for n in names:
        vals = [r[n] for r in rows if r.get(n) is not None]
        t = infer_type(vals, card, n)
        c = Col(n, t, units.get(n) or card.units.get(n))
        if n in card.legend:
            c.legend = card.legend[n]
            c.typ = 'cat'
        cols[n] = c
    return cols


def create(db, tname, cols, rows, card, unknown_cells, extra=()):
    colnames = list(cols)
    db.execute('CREATE TABLE %s (_rid INTEGER PRIMARY KEY, %s)' % (
        tname, ', '.join([q(c) for c in colnames] + [q(e) for e in extra])))
    for i, r in enumerate(rows):
        vals = []
        for c in colnames:
            v = r.get(c)
            if v is None:
                vals.append(None); unknown_cells.append((tname, i, c))
            else:
                vals.append(conv(v, cols[c], card))
        vals += [r.get(e) for e in extra]
        db.execute('INSERT INTO %s VALUES (%s)' % (tname, ','.join(['?'] * (len(vals) + 1))), [i] + vals)


def id_col(cols):
    ids = [c for c in cols.values() if c.typ == 'id']
    for c in ids:
        if c.name.endswith('_id'):
            return c.name
    return ids[0].name if ids else None


def build(row, card, tables):
    m = Model()
    m.db = sqlite3.connect(':memory:')
    m.unknown = []
    m.card = card
    samp = row['meta']['sampler']
    m.sampler = samp
    if tables and tables[0].kind == 'log':
        return build_log(m, row, card, tables)
    if tables and tables[0].kind == 'pivot':
        return build_pivot(m, row, card, tables)
    if len(tables) == 2:
        return build_join(m, row, card, tables)
    if len(tables) != 1:
        raise ParseError('tables %d' % len(tables))
    t = tables[0]
    if t.native:
        return build_nested(m, row, card, t)
    names, units, rows = _flat_table(t, card)
    cols = make_cols(names, units, rows, card)
    m.kind = 'single'
    m.cols = cols
    m.idc = id_col(cols)
    create(m.db, 'r', cols, rows, card, m.unknown)
    m.items = {}
    return m


# ---------------------------------------------------------------- S4 nested ------------------------------------
def build_nested(m, row, card, t):
    unk = _unk(card)
    recs = t.rows
    if isinstance(recs, dict):
        raise ParseError('json top-level object')
    flat, items_raw, list_state = [], {}, []
    lists = {}
    for i, r in enumerate(recs):
        d, ls = {}, {}
        for k, v in r.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, (dict, list)):
                        raise ParseError('depth')
                    d[k + '.' + k2] = None if v2 is None or (isinstance(v2, str) and v2 in unk) else v2
            elif isinstance(v, list):
                lists.setdefault(k, [])
                ls[k] = 'empty' if not v else 'value'
                for j, it in enumerate(v):
                    if not isinstance(it, dict):
                        raise ParseError('list item not record')
                    lists[k].append((i, j, it))
            elif v is None:
                d[k] = None  # may be a null list or null scalar; resolved below
                ls.setdefault('__null__', []).append(k)
            else:
                d[k] = None if (isinstance(v, str) and v in unk) else v
        flat.append(d); list_state.append(ls)
    # null keys that are list fields elsewhere are null lists
    listnames = set(lists)
    for d, ls in zip(flat, list_state):
        for k in ls.pop('__null__', []):
            if k in listnames:
                ls[k] = 'null'; d.pop(k, None)
    names = []
    for d in flat:
        for k in d:
            if k not in names and k not in listnames:
                names.append(k)
    for d in flat:
        for k in names:
            if k not in d:
                raise ParseError('missing key %s (T6 not supported)' % k)
    cols = make_cols(names, {}, flat, card)
    m.kind = 'nested'
    m.cols = cols
    m.idc = id_col(cols)
    lstate_cols = ['_ls_' + k for k in listnames]
    for d, ls in zip(flat, list_state):
        for k in listnames:
            d['_ls_' + k] = ls.get(k, 'absent')
    create(m.db, 'r', cols, flat, card, m.unknown, extra=lstate_cols)
    m.items = {}
    for k, its in lists.items():
        inames = []
        for _, _, it in its:
            for kk in it:
                if kk not in inames:
                    inames.append(kk)
        irows = []
        for (i, j, it) in its:
            dd = {kk: (None if it.get(kk) is None else it.get(kk)) for kk in inames}
            dd['_owner'] = i
            irows.append(dd)
        icols = make_cols(inames, {}, irows, card)
        tn = 'it_' + re.sub(r'\W', '_', k)
        create(m.db, tn, icols, irows, card, m.unknown, extra=['_owner'])
        m.items[k] = (tn, icols)
    return m


# ---------------------------------------------------------------- S3 join ---------------------------------------
def build_join(m, row, card, tables):
    parts = []
    for t in tables:
        names, units, rows = _flat_table(t, card)
        parts.append((t.title, names, units, rows))
    # dimension = table whose first id-format column is unique and named in the other table
    dim = fact = None
    for a, b in ((0, 1), (1, 0)):
        ta, na, ua, ra = parts[a]
        tb, nb, ub, rb = parts[b]
        key = na[0]
        vals = [r[key] for r in ra]
        if key in nb and len(set(vals)) == len(vals) and all(v and ID_RX.match(v) for v in vals):
            dim, fact = parts[a], parts[b]
            break
    if dim is None:
        raise ParseError('join: no dimension table')
    m.kind = 'join'
    m.key = dim[1][0]
    m.dcols = make_cols(dim[1], dim[2], dim[3], card)
    m.fcols = make_cols(fact[1], fact[2], fact[3], card)
    m.dtitle, m.ftitle = (dim[0] or '').lower(), (fact[0] or '').lower()
    create(m.db, 'd', m.dcols, dim[3], card, m.unknown)
    create(m.db, 'f', m.fcols, fact[3], card, m.unknown)
    m.cols = m.dcols
    m.idc = m.key
    m.items = {}
    return m


# ---------------------------------------------------------------- S5 pivot --------------------------------------
def build_pivot(m, row, card, tables):
    t = tables[0]
    _, colname, ent, unit = t.title
    hdr = t.cols
    weeks = hdr[1:]
    mark = card.footmark or '*'
    m.kind = 'pivot'
    m.pcol, m.pent, m.punit = colname, ent, unit
    m.db.execute('CREATE TABLE c (ent TEXT, week TEXT, val INTEGER, marked INTEGER, rowpos INTEGER)')
    m.db.execute('CREATE TABLE tot (label TEXT, week TEXT, val INTEGER, rowpos INTEGER)')
    m.ents = []
    m.pcolobj = Col(colname, 'num', unit)
    for pos, r in enumerate(t.rows):
        lab = r[hdr[0]].strip()
        for w in weeks:
            raw = r[w].strip()
            mk = 0
            if raw.endswith(mark):
                raw = raw[:-len(mark)].strip(); mk = 1
            if raw in _unk(card):
                v = None
            else:
                m.pcolobj.dp = max(m.pcolobj.dp, num_decimals(raw, card))
                v = int(parse_number(raw, card) * SCALE)
            if lab in ('Subtotal', 'Total'):
                m.db.execute('INSERT INTO tot VALUES (?,?,?,?)', (lab, w, v, pos))
            else:
                m.db.execute('INSERT INTO c VALUES (?,?,?,?,?)', (lab, w, v, mk, pos))
        if lab not in ('Subtotal', 'Total'):
            m.ents.append(lab)
    m.weeks = weeks
    m.cols = {}
    m.idc = None
    m.items = {}
    return m


# ---------------------------------------------------------------- S6 log ----------------------------------------
def build_log(m, row, card, tables):
    m.kind = 'log'
    m.db.execute('CREATE TABLE L (pos INTEGER, t INTEGER, level TEXT, lrank INTEGER, comp TEXT, req TEXT, '
                 'sess TEXT, msg TEXT, kv TEXT)')
    m.db.execute('CREATE TABLE KV (pos INTEGER, k TEXT, v TEXT)')
    levels = card.levels
    m.syntaxes = set()
    pos = 0
    for t in tables:
        for line in t.rows:
            p = log_line(line, card)
            if p is None:
                raise ParseError('log line')
            m.syntaxes.add(p['syntax'])
            secs = parse_datetime(p['t'], card)
            lr = levels.index(p['level']) if levels and p['level'] in levels else None
            m.db.execute('INSERT INTO L VALUES (?,?,?,?,?,?,?,?,?)',
                         (pos, secs, p['level'], lr, p['comp'], p['kv'].get('req'), p['kv'].get('sess'), p['msg'],
                          repr(sorted(p['kv'].items()))))
            for k, v in p['kv'].items():
                m.db.execute('INSERT INTO KV VALUES (?,?,?)', (pos, k, v))
            pos += 1
    if len(m.syntaxes) != 1:
        raise ParseError('log rows use %d syntaxes' % len(m.syntaxes))
    m.cols = {}
    m.idc = None
    m.items = {}
    return m
