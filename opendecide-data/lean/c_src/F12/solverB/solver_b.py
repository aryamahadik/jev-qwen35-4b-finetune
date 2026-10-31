"""F12 solver B: independent declarative validator (G2).

Written from the frozen G0 spec (F12.G0.v7, sections 1-3, 5, 6, 8.1, 10) and the row format only; it never
imports or reads the generator (c_src/F12/gen/) or solver A.

Paradigm (spec section 5, solver B): the parsed structure of each row is loaded into in-memory sqlite3 tables
(tools, scope, roles, params, cons, returns, sources, fields, mentions, quals); match is SQL with NOT EXISTS, the
value in force is a window function over the user's mention rows, and the outcome is one SQL CASE decision table.
Acceptance, completeness and call validation compile each tool to a JSON Schema (Draft 2020-12) checked with the
`jsonschema` library; errors are classified through one fixed error table.

Input structure: the row's structure record (sidecar `S`, the canonical form behind structure_hash that G3 shows
equal to the parse of `state`), plus facts read from the rendered text itself: ID formats (controlled phrase),
precondition field words ("works only when <field> is <v>"), case-reference order (C-INV), option texts and
option-definition lines.  Solver A outputs in the sidecar (outcome, kind, gold_canon, near_miss, audit) are never
read as inputs; they are only compared at the end.

Output: solverB/mismatch.json (ids, both answers, spec item; no row text) and solverB/summary.json.
"""
import json, re, sqlite3, sys, datetime, collections, hashlib, os
from decimal import Decimal, InvalidOperation
from jsonschema import Draft202012Validator
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'common'))
import negcount  # shared XF02 counter (c_src/common/negcount.py)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'out')
MARKERS = {'not recorded', 'unknown'}
LIMIT = int(os.environ.get('F12B_LIMIT', '0'))
CLASS_PHRASE = {1: 'Tool name not listed', 2: 'Unknown parameter', 3: 'Missing needed value', 4: 'Wrong type',
                5: 'Not a listed choice', 6: 'Outside the limits', 7: 'Wrong ID format', 8: 'Only-if rule broken',
                9: 'Unless rule broken', 10: 'Exactly-one rule broken', 11: 'At-least-one rule broken',
                12: 'At-most-one rule broken'}
PAIR_CLASS = {'ONLY_IF': 8, 'UNLESS': 9, 'EXACTLY_ONE': 10, 'AT_LEAST_ONE': 11, 'AT_MOST_ONE': 12}


class Flag(Exception):
    pass


# ----------------------------------------------------------------------------------------------- value parsing
NUM_UNIT = re.compile(r'^(\d+(?:\.\d+)?) (\S(?:.*\S)?)$')
ISO_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
REL = [(re.compile(r'^today$'), lambda m: 0), (re.compile(r'^tomorrow$'), lambda m: 1),
       (re.compile(r'^yesterday$'), lambda m: -1), (re.compile(r'^in (\d+) days?$'), lambda m: int(m.group(1))),
       (re.compile(r'^(\d+) days? ago$'), lambda m: -int(m.group(1))),
       (re.compile(r'^in (\d+) weeks?$'), lambda m: 7 * int(m.group(1)))]


def rel_date(s, now):
    """SEM-32 closed list counted from the stated now; returns datetime.date or None."""
    for rx, f in REL:
        m = rx.match(s.strip())
        if m:
            return now.date() + datetime.timedelta(days=f(m))
    return None


def as_date(s, now):
    if isinstance(s, str) and ISO_DATE.match(s):
        try:
            return datetime.date.fromisoformat(s)
        except ValueError:
            return None
    if isinstance(s, str):
        return rel_date(s, now)
    return None


def same_unit(u, pu):
    return u == pu or u + 's' == pu or pu + 's' == u


def num_unit(s):
    m = NUM_UNIT.match(s) if isinstance(s, str) else None
    if not m:
        return None
    return Decimal(m.group(1)), m.group(2)


class Ctx:
    """Per-row facts from the text and the structure."""

    def __init__(self, row, S):
        self.row, self.S = row, S
        self.now = datetime.datetime.strptime(S['now'], '%Y-%m-%d %H:%M')
        st = row['state']
        # ID formats from the controlled phrase / regex forms (SEM-42), keyed by prefix + length
        self.idcs = {}
        for m in re.finditer(r'(\S*?) followed by exactly (\d+) (capital letters or digits|capital letters|digits)', st):
            cs = {'capital letters or digits': '[A-Z0-9]', 'capital letters': '[A-Z]', 'digits': '[0-9]'}[m.group(3)]
            self.idcs[(m.group(1).strip('"\'(`'), int(m.group(2)))] = cs
        for m in re.finditer(r'\^([A-Z]*-?)\[(0-9|A-Z0-9|A-Z)\]\{(\d+)\}\$', st):
            self.idcs[(m.group(1), int(m.group(3)))] = '[' + m.group(2) + ']'
        # precondition field words (SEM-21), per tool where the text allows, else the row's single field
        self.prefield = {}
        allf = set(m.group(1) for m in re.finditer(r'works only when ([a-z][a-z0-9 _]*?) is ', st))
        for t in S['tools']:
            if t.get('pre'):
                fw = None
                for m in re.finditer(re.escape(t['name']) + r'\b', st):
                    seg = st[m.end():m.end() + 700]
                    mm = re.search(r'works only when ([a-z][a-z0-9 _]*?) is ' + re.escape(t['pre']) + r'\b', seg)
                    if mm:
                        fw = mm.group(1)
                        break
                if fw is None and len(allf) == 1:
                    fw = next(iter(allf))
                if fw is None:
                    raise Flag('precondition field not found in text')
                self.prefield[t['name']] = fw.replace(' ', '_')

        # scope dimension of each restricted tool (SEM-03): "only for <dimension words> <v1> or <v2>"
        self.tdim = {}
        for t in S['tools']:
            if t.get('scope'):
                dw = None
                for m in re.finditer(re.escape(t['name']) + r'\b', st):
                    seg = st[m.end():m.end() + 900]
                    k = seg.find('only for ')
                    if k < 0:
                        continue
                    rest = seg[k + 9:]
                    pos = [rest.find(v) for v in t['scope'] if rest.find(v) >= 0]
                    if pos:
                        cand = rest[:min(pos)].strip(' :')
                        if re.match(r'^[a-z][a-z0-9 ]*$', cand):
                            dw = cand
                            break
                if dw is None:
                    raise Flag('scope dimension of %s not found in text' % t['name'])
                self.tdim[t['name']] = dw.replace(' ', '_')

    def qual_dim(self, v):
        dims = sorted(set(self.tdim.values()))
        if len(dims) <= 1:
            return dims[0] if dims else None
        st = self.row['state']
        hit = [d for d in dims if re.search(re.escape(d.replace('_', ' ')) + r'\W{0,3}(?:is |of |= |set to )?' +
                                             re.escape(v) + r'\b', st, re.I)]
        if len(hit) != 1:
            raise Flag('qualifier dimension not decidable from the text (%d dimensions)' % len(hit))
        return hit[0]

    def id_pattern(self, p):
        cs = self.idcs.get((p.get('prefix') or '', p['n']))
        if cs is None:
            raise Flag('ID format for %s not found in text' % p['name'])
        return '^(?:' + re.escape(p.get('prefix') or '') + cs + '{%d})$' % p['n']


# ----------------------------------------------------------------------------------- typed forms (5 pre-pass)
def fwd_typed(p, v, ctx):
    """Forward-row typing of a user/record/default value for param p (step 1 of the pre-pass)."""
    t = p['type']
    if t in ('integer', 'decimal'):
        nu = num_unit(v)
        if nu is None:
            return v
        n, u = nu
        pu = p.get('unit')
        if pu is None or not same_unit(u, pu):
            return v                                    # other unit: raw string -> type error (not accepted)
        if t == 'decimal':
            n = n * (Decimal(10) ** p['places'])
        return int(n) if n == n.to_integral_value() else float(n)
    if t == 'date':
        d = as_date(v, ctx.now)
        return d.toordinal() if d else v
    if t == 'enum':
        for mbr in p['members']:
            if isinstance(v, str) and v.lower() == mbr.lower():
                return mbr
        return v
    if t == 'boolean':
        if isinstance(v, bool):
            return v
        return {'yes': True, 'no': False}.get(v, v)
    return v


def audit_typed(p, v, ctx):
    """Audit typing of a proposed-call value (no normalisation, R3-13)."""
    t = p['type'] if p else None
    if isinstance(v, dict) and 'num' in v:
        v = Decimal(v['num'])
    elif isinstance(v, int) and not isinstance(v, bool):
        v = Decimal(v)
    if t in ('integer', 'decimal') and isinstance(v, Decimal):
        if t == 'decimal':
            v = v * (Decimal(10) ** p['places'])
        return int(v) if v == v.to_integral_value() else float(v)
    if t == 'date' and isinstance(v, str) and ISO_DATE.match(v):
        return datetime.date.fromisoformat(v).toordinal()
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    return v


def lim(p, x):
    t = p['type']
    if t == 'integer':
        return int(x)
    if t == 'decimal':
        return int(Decimal(str(x)) * (Decimal(10) ** p['places']))
    if t == 'date':
        return datetime.date.fromisoformat(x).toordinal()
    raise Flag('limit on %s' % t)


def compile_schema(tool, ctx):
    props, req = {}, []
    for p in tool['params']:
        t = p['type']
        if t == 'enum':
            s = {'enum': list(p['members'])}
        elif t in ('integer', 'decimal', 'date'):
            s = {'type': 'integer'}
            if p.get('min'):
                s['minimum' if p['min'][1] else 'exclusiveMinimum'] = lim(p, p['min'][0])
            if p.get('max'):
                s['maximum' if p['max'][1] else 'exclusiveMaximum'] = lim(p, p['max'][0])
        elif t == 'string':
            s = {'type': 'string'}
            if p.get('minlen') is not None:
                s['minLength'] = p['minlen']
            if p.get('maxlen') is not None:
                s['maxLength'] = p['maxlen']
        elif t == 'id':
            s = {'type': 'string', 'pattern': ctx.id_pattern(p)}
        elif t == 'boolean':
            s = {'type': 'boolean'}
        else:
            raise Flag('param type %s' % t)
        props[p['name']] = s
        if p['required']:
            req.append(p['name'])
    sch = {'type': 'object', 'properties': props, 'required': req, 'additionalProperties': False}
    allof = []
    pmap = {p['name']: p for p in tool['params']}
    for c in tool.get('cons') or []:
        k, a, b = c['k'], c['p'], c['q']
        if k == 'ONLY_IF':
            allof.append({'dependentRequired': {a: [b]}})
        elif k == 'UNLESS':
            v = fwd_typed(pmap[b], c['v'], ctx) if b in pmap else c['v']
            allof.append({'if': {'required': [b], 'properties': {b: {'const': v}}}, 'then': {}, 'else': {'required': [a]}})
        elif k == 'EXACTLY_ONE':
            allof.append({'oneOf': [{'required': [a]}, {'required': [b]}]})
        elif k == 'AT_LEAST_ONE':
            allof.append({'anyOf': [{'required': [a]}, {'required': [b]}]})
        elif k == 'AT_MOST_ONE':
            allof.append({'not': {'required': [a, b]}})
    if allof:
        sch['allOf'] = allof
    return Draft202012Validator(sch)


def classify_errors(tool, inst, validator):
    """Return list of (kind, params, keyword) with kind in {'missing','bad'} (forward error table) plus raw info."""
    out = []
    for e in validator.iter_errors(inst):
        kw = e.validator
        sp = list(e.schema_path)
        if kw == 'required':
            miss = [r for r in e.validator_value if r not in inst]
            is_else = 'else' in sp
            for r in miss:
                out.append(('missing', (r,), 'else' if is_else else 'required', sp))
        elif kw == 'dependentRequired':
            for a, bs in e.validator_value.items():
                if a in inst:
                    for b in bs:
                        if b not in inst:
                            out.append(('missing', (a, b), 'dependentRequired', sp))
        elif kw in ('oneOf', 'anyOf'):
            mem = [x['required'][0] for x in e.validator_value]
            n = sum(1 for m in mem if m in inst)
            out.append(('missing' if n == 0 else 'bad', tuple(mem), kw, sp))
        elif kw == 'not':
            out.append(('bad', tuple(e.validator_value['required']), 'not', sp))
        elif kw == 'additionalProperties':
            extra = [k for k in inst if k not in validator.schema['properties']]
            for x in extra:
                out.append(('extra', (x,), kw, sp))
        else:
            out.append(('bad', (e.path[0],) if e.path else (), kw, sp))
    return out


# --------------------------------------------------------------------------------------------- the row solver
SCHEMA_SQL = """
CREATE TABLE tools(tid INTEGER, name TEXT, a TEXT, o INTEGER, pre TEXT, prefield TEXT, cost INTEGER, pref INTEGER,
                   dim TEXT, restricts INTEGER);
CREATE TABLE scope(tid INTEGER, val TEXT);
CREATE TABLE roles(tid INTEGER, role TEXT);
CREATE TABLE params(tid INTEGER, name TEXT, type TEXT, required INTEGER, dflt TEXT, ord INTEGER);
CREATE TABLE returns(tid INTEGER, p TEXT);
CREATE TABLE sources(sid INTEGER, kind TEXT, ts TEXT, about INTEGER, lookalike INTEGER);
CREATE TABLE fields(sid INTEGER, key TEXT, val TEXT);
CREATE TABLE mentions(seq INTEGER, p TEXT, v TEXT, alts TEXT, kind TEXT);
CREATE TABLE quals(dimkey TEXT, val TEXT, origin TEXT);
CREATE TABLE tstat(tid INTEGER, cand INTEGER, prov INTEGER, matches INTEGER, accepts INTEGER, complete INTEGER,
                   nmiss INTEGER, nbad INTEGER, nunclear INTEGER);
"""


class Row:
    def __init__(self, row, side, pack_read):
        self.row, self.side, self.S = row, side, side['S']
        self.ctx = Ctx(row, self.S)
        self.pol = self.S['pol']
        self.read_action = pack_read
        self.db = sqlite3.connect(':memory:')
        self.db.executescript(SCHEMA_SQL)
        self.tools = self.S['tools']
        self.tbyname = {t['name']: t for t in self.tools}
        self._validators = {}
        self.notes = []
        q = self.db.execute
        for i, t in enumerate(self.tools):
            q('INSERT INTO tools VALUES(?,?,?,?,?,?,?,?,?,?)', (i, t['name'], t['a'], t['o'], t.get('pre'),
              self.ctx.prefield.get(t['name']), t.get('cost'), 1 if t.get('pref') else 0,
              self.ctx.tdim.get(t['name']), 1 if t.get('scope') else 0))
            for v in t.get('scope') or []:
                q('INSERT INTO scope VALUES(?,?)', (i, v))
            for r in t.get('roles') or []:
                q('INSERT INTO roles VALUES(?,?)', (i, r))
            for j, p in enumerate(t['params']):
                q('INSERT INTO params VALUES(?,?,?,?,?,?)', (i, p['name'], p['type'], 1 if p['required'] else 0,
                  None if p.get('default') is None else json.dumps(p['default']), j))
            for r in t.get('returns') or []:
                q('INSERT INTO returns VALUES(?,?)', (i, r[0] if isinstance(r, list) else r))

    # ---------------------------------------------------------------- step 0: which request, kind, intent
    def request(self, conv=None, case=None):
        """Return (req_stmt, mentions-in-walk-order, quals) for the current request (section 3 step 0)."""
        if case is not None:
            req = [s for s in case if s['t'] == 'req']
            walk = []
            for s in case:
                if s['t'] == 'req':
                    if s.get('ref') and s['ref'][0] == 'id':
                        walk.append({'t': 'ref', 'v': s['ref'][1], 'p': None, '_named': True})
                else:
                    walk.append(s)
            return req[0], walk, []
        conv = self.S['conv']
        users = [i for i, t in enumerate(conv) if t['who'] == 'user']
        if not users:
            raise Flag('no user turn')
        cur = [users[-1]]
        ask_param = {}
        i = users[-1]
        while True:
            sts = conv[i].get('st', [])
            if sts and sts[0]['t'] == 'cont':
                j = i - 1
                if j < 0 or conv[j]['who'] != 'assistant' or not conv[j].get('ask'):
                    raise Flag('continuation without an assistant question')
                ask_param[i] = conv[j]['ask']
                k = max([u for u in users if u < j], default=None)
                if k is None:
                    raise Flag('continuation with no earlier request')
                cur.insert(0, k)
                i = k
            else:
                break
        reqs = [s for s in conv[cur[0]].get('st', []) if s['t'] == 'req']
        if len(reqs) != 1:
            raise Flag('request turn without exactly one request statement')
        # earlier user turns that make no request and hold fact statements (R4-02)
        facts = [i for i in users if i < cur[0] and all(s['t'] == 'fact' for s in conv[i].get('st', []))
                 and conv[i].get('st')]
        walk = []
        for i in sorted(facts + cur):
            for s in conv[i].get('st', []):
                if s['t'] == 'req':
                    if s.get('ref') and s['ref'][0] == 'id':
                        walk.append({'t': 'ref', 'v': s['ref'][1], 'p': None, '_named': True})
                    continue
                s2 = dict(s)
                if s['t'] == 'cont':
                    s2['p'] = ask_param[i]
                    s2['_named'] = True
                if s['t'] == 'fact':
                    s2['_fact'] = True
                if i not in cur and s['t'] != 'fact':
                    continue
                walk.append(s2)
        return reqs[0], walk, conv

    def kind(self, req, walk):
        """Ordered kind test (section 3 step 0, R1-06)."""
        named_value = any(s['t'] in ('val', 'qual', 'cont', 'ref') for s in walk if not s.get('_fact'))
        if req.get('cue') == 'catalog' and not req.get('ref') and not named_value:
            return 'catalog'
        if self.read_action is not None and req['a'] == self.read_action:
            return 'info'
        return 'action'

    # ---------------------------------------------------------------- sources about the target entity (SEM-43)
    def load_sources(self, req, walk, conv, with_context=True):
        q = self.db.execute
        q('DELETE FROM sources'); q('DELETE FROM fields')
        srcs = []
        if with_context:
            for r in self.S['records']:
                srcs.append(('record', None, r['fields']))
            for t in (conv or []):
                if t['who'] == 'tool':
                    srcs.append(('tool', t['ts'], t['fields']))
            for b in self.S['stored']:
                srcs.append(('stored', b['ts'], b['fields']))
        ref = req.get('ref')
        self.unclear_entity = False
        about = [False] * len(srcs)
        if ref:
            kind, val = ref
            if kind == 'id':
                eid = val
                for i, (_, _, f) in enumerate(srcs):
                    if any(k.endswith('_id') and v == eid for k, v in f):
                        about[i] = True
            else:
                nm = [i for i, (_, _, f) in enumerate(srcs) if any(k.endswith('_name') and v == nm_ for k, v in f
                                                                    for nm_ in [val])]
                ids = set()
                for i in nm:
                    ids |= {v for k, v in srcs[i][2] if k.endswith('_id') and self._is_id_key_of(k, srcs[i][2])}
                if len(ids) >= 2:
                    self.unclear_entity = True
                    for i in nm:
                        about[i] = True
                else:
                    for i in nm:
                        about[i] = True
                    for i, (_, _, f) in enumerate(srcs):
                        if any(k.endswith('_id') and v in ids for k, v in f):
                            about[i] = True
        self.srcs = srcs
        self.about = about
        for i, (k, ts, f) in enumerate(srcs):
            q('INSERT INTO sources VALUES(?,?,?,?,?)', (i, k, ts, 1 if about[i] else 0, 0 if about[i] else 1))
            for key, v in f:
                q('INSERT INTO fields VALUES(?,?,?)', (i, key, v if isinstance(v, str) else json.dumps(v)))

    def _is_id_key_of(self, k, fields):
        return True

    # ---------------------------------------------------------------- candidate tools, providers, mentions
    def candidates(self, req, kind):
        if kind == 'catalog':
            return []
        rows = self.db.execute('SELECT tid FROM tools WHERE a=? AND o=? ORDER BY tid', (req['a'], req['o'])).fetchall()
        return [r[0] for r in rows]

    def providers(self, cands):
        if not cands:
            return []
        ph = ','.join('?' * len(cands))
        rows = self.db.execute(
            'SELECT DISTINCT r.tid FROM returns r WHERE r.tid NOT IN (%s) AND r.p IN '
            '(SELECT name FROM params WHERE tid IN (%s)) ORDER BY r.tid' % (ph, ph), cands + cands).fetchall()
        return [r[0] for r in rows]

    def form_ok(self, p, v):
        """NG-19 form test (R5-10): type, unit, ID format or enum membership; limits excluded."""
        t = p['type']
        if t in ('integer', 'decimal'):
            nu = num_unit(v)
            if not nu or not p.get('unit') or not same_unit(nu[1], p['unit']):
                return False
            return t == 'decimal' or nu[0] == nu[0].to_integral_value()
        if t == 'date':
            return as_date(v, self.ctx.now) is not None
        if t == 'id':
            return re.match(self.ctx.id_pattern(p), v or '') is not None
        if t == 'enum':
            return any((v or '').lower() == m.lower() for m in p['members'])
        return False

    def load_mentions(self, walk, tids):
        q = self.db.execute
        q('DELETE FROM mentions')
        self.unattributed = []
        allp = [p for i in tids for p in self.tools[i]['params']]
        for seq, s in enumerate(walk):
            if s['t'] == 'ref':
                # the target named by its ID next to its entity-type word: a named value of e's ID-key param
                ks = {pp['name'] for pp in allp if pp['type'] == 'id' and pp.get('prefix') and
                      s['v'].startswith(pp['prefix'])}
                if len(ks) != 1:
                    ow = {self.tools[i].get('oword') for i in tids if self.tools[i]['o'] == self.req['o']}
                    ks = {w.replace(' ', '_') + '_id' for w in ow if w} & {pp['name'] for pp in allp}
                if len(ks) == 1:
                    q('INSERT INTO mentions VALUES(?,?,?,?,?)', (seq, ks.pop(), json.dumps(s['v']), None, 'val'))
                continue
            if s['t'] == 'val' or s['t'] == 'cont' or s['t'] == 'fact':
                p = s.get('p')
                if p is None:
                    names = {pp['name'] for pp in allp if s.get('v') is not None and self.form_ok(pp, s['v'])}
                    if s.get('alts'):
                        names = {pp['name'] for pp in allp if all(self.form_ok(pp, a) for a in s['alts'])}
                    if len(names) != 1:
                        self.unattributed.append(s.get('v'))
                        continue
                    p = names.pop()
                if s['t'] == 'fact' and not self.fact_about_e(s):
                    continue
                if self.req.get('field') and p == self.req['field'] and self._kind == 'info':
                    continue                                # a statement of the asked field f answers; it fills no param
                q('INSERT INTO mentions VALUES(?,?,?,?,?)', (seq, p, None if s.get('v') is None else json.dumps(s['v']),
                  json.dumps(s['alts']) if s.get('alts') else None, s['t']))
            elif s['t'] == 'retract':
                q('INSERT INTO mentions VALUES(?,?,?,?,?)', (seq, s.get('p'), None, None, 'retract'))

    def fact_about_e(self, s):
        ref = self.req.get('ref')
        if not ref:
            return False
        if ref[0] == 'name':
            return s.get('name') == ref[1]
        # ref by ID: the fact names e by a name that a source about e carries, or states e's ID itself
        names = {v for i, (_, _, f) in enumerate(self.srcs) if self.about[i] for k, v in f if k.endswith('_name')}
        return s.get('name') in names or s.get('v') == ref[1]

    def quals(self, walk):
        q = self.db.execute
        q('DELETE FROM quals')
        for s in walk:
            if s['t'] == 'qual' and not s.get('_fact'):
                d = self.ctx.qual_dim(s['v'])
                if d is not None:
                    q('INSERT INTO quals VALUES(?,?,?)', (d, s['v'], 'user'))
        # record-shown qualifiers about e (tool outputs never hold a dimension field, NG-33)
        q("INSERT INTO quals SELECT f.key, f.val, 'record' FROM fields f JOIN sources s ON s.sid=f.sid "
          "WHERE s.about=1 AND s.kind='record' AND f.key IN (SELECT dim FROM tools WHERE dim IS NOT NULL)")

    # ---------------------------------------------------------------- step 1: values (window function)
    def resolve(self, pnames):
        """Per param name: ('given', raw, rank, kind) | ('unclear', ...) | ('absent',)."""
        q = self.db.execute
        res = {}
        user = {r[0]: r for r in q(
            "SELECT p, v, alts, kind FROM (SELECT p, v, alts, kind, ROW_NUMBER() OVER (PARTITION BY p ORDER BY seq DESC)"
            " AS rn FROM mentions) WHERE rn=1")}
        recs = collections.defaultdict(set)
        if not self.unclear_entity:
            for k, v, kd in q("SELECT f.key, f.val, s.kind FROM fields f JOIN sources s ON s.sid=f.sid WHERE s.about=1"):
                if v.lower() not in MARKERS:
                    recs[k].add((v, kd))
        for p in pnames:
            if p in user:
                _, v, alts, kd = user[p]
                if kd == 'retract':
                    res[p] = ('absent',)
                elif alts:
                    res[p] = ('unclear', 'open choice', json.loads(alts))
                else:
                    res[p] = ('given', json.loads(v), 'user', kd)
                continue
            if p in recs:
                vals = {v for v, _ in recs[p]}
                if len(vals) > 1:
                    raise Flag('two sources about e disagree on %s (NG-13)' % p)
                kinds = {kd for _, kd in recs[p]}
                res[p] = ('given', vals.pop(), 'source', 'record' if 'record' in kinds else 'tool')
                continue
            if self.unclear_entity and p in self.e_id_keys:
                res[p] = ('unclear', 'two matching sources', None)
                continue
            res[p] = ('absent',)
        return res

    # ---------------------------------------------------------------- steps 2-6 per tool
    def tool_eval(self, tid, values):
        t = self.tools[tid]
        key = t['name']
        if key not in self._validators:
            self._validators[key] = compile_schema(t, self.ctx)
        val = self._validators[key]
        inst, unclear, given_raw = {}, [], {}
        for p in t['params']:
            r = values.get(p['name'], ('absent',))
            if r[0] == 'given':
                inst[p['name']] = fwd_typed(p, r[1], self.ctx)
                given_raw[p['name']] = r
            elif r[0] == 'unclear':
                unclear.append(p['name'])
        for p in t['params']:                               # default fill (pre-pass step 4)
            if p['name'] not in inst and p['name'] not in unclear and p.get('default') is not None:
                inst[p['name']] = fwd_typed(p, p['default'], self.ctx)
        errs = classify_errors(t, inst, val)
        bad = [e for e in errs if e[0] == 'bad']
        miss = [e for e in errs if e[0] == 'missing']
        return {'inst': inst, 'bad': bad, 'miss': miss, 'unclear': unclear, 'errs': errs}

    def match_sql(self, tids):
        """Match (step 2) as SQL: capability is pre-filtered; scope via NOT EXISTS; precondition; role."""
        if not tids:
            return {}
        role = self.S.get('role')
        rows = self.db.execute(
            "SELECT t.tid,"
            " NOT EXISTS (SELECT 1 FROM quals q WHERE t.restricts=1 AND q.dimkey=t.dim AND q.val NOT IN"
            "   (SELECT val FROM scope s WHERE s.tid=t.tid)) AS scope_ok,"
            " (t.pre IS NULL OR EXISTS (SELECT 1 FROM fields f JOIN sources s ON s.sid=f.sid WHERE s.about=1 AND"
            "   s.kind='record' AND f.key=t.prefield AND f.val=t.pre)) AS pre_ok,"
            " (? = 0 OR EXISTS (SELECT 1 FROM roles r WHERE r.tid=t.tid AND r.role=?)) AS role_ok"
            " FROM tools t WHERE t.tid IN (%s)" % ','.join('?' * len(tids)),
            [1 if self.pol.get('role') else 0, role] + list(tids)).fetchall()
        return {r[0]: (bool(r[1]), bool(r[2]), bool(r[3])) for r in rows}

    def unclear_entity_pre_check(self):
        if not self.unclear_entity:
            return
        # R3-08: matching records hold the same precondition and scope values; tool outputs never match here
        keys = {r[0] for r in self.db.execute('SELECT prefield FROM tools WHERE prefield IS NOT NULL')} | \
               {r[0] for r in self.db.execute('SELECT dim FROM tools WHERE dim IS NOT NULL')}
        for k in keys:
            vals = {r[0] for r in self.db.execute(
                'SELECT f.val FROM fields f JOIN sources s ON s.sid=f.sid WHERE s.about=1 AND f.key=?', (k,))}
            if len(vals) > 1:
                raise Flag('matching sources differ on %s (NG-28)' % k)

    # ---------------------------------------------------------------- the decision table
    def solve(self, case=None, with_context=True):
        req, walk, conv = self.request(case=case)
        self.req = req
        kind = self.kind(req, walk)
        self._kind = kind
        if kind == 'info':
            extra = [x['t'] for x in walk if not x.get('_fact') and x['t'] in ('qual', 'val')
                     and not (x['t'] == 'val' and x.get('p') == req.get('field'))]
            if extra:
                self.notes.append('NG-55: info question states %s besides f, e and f\'s value' % '+'.join(sorted(set(extra))))
        self.load_sources(req, walk, conv, with_context)
        self.unclear_entity_pre_check()
        cands = self.candidates(req, kind)
        provs = self.providers(cands)
        self.load_mentions(walk, cands + provs)
        self.quals(walk)
        # e's ID key(s): ID-type params named <type>_id whose value a source about e shows, or the ref's key
        self.e_id_keys = set()
        for i in cands + provs:
            for p in self.tools[i]['params']:
                if p['type'] == 'id':
                    for j, (_, _, f) in enumerate(self.srcs):
                        if self.about[j] and any(k == p['name'] for k, _ in f):
                            self.e_id_keys.add(p['name'])
        self._provs = provs
        pnames = sorted({p['name'] for i in cands + provs for p in self.tools[i]['params']})
        values = self.resolve(pnames)
        m = self.match_sql(cands + provs)
        ev = {i: self.tool_eval(i, values) for i in cands + provs}
        q = self.db.execute
        q('DELETE FROM tstat')
        for i in cands + provs:
            sc, pr, ro = m[i]
            e = ev[i]
            matches = sc and pr and ro
            accepts = not e['bad']
            q('INSERT INTO tstat VALUES(?,?,?,?,?,?,?,?,?)', (i, 1 if i in cands else 0, 1 if i in provs else 0,
              int(matches), int(accepts), int(matches and accepts and not e['miss']), len(e['miss']), len(e['bad']),
              len(e['unclear'])))
        inv = self.pol.get('invalid', 'A')
        fit_sql = "cand=1 AND matches=1" + (" AND accepts=1" if inv == 'B' else "")
        # ANSWER check (step 4)
        answer = False
        if kind == 'catalog':
            answer = True
        elif kind == 'info':
            answer = self.answer_shown(req, walk)
        row = q(
            "SELECT CASE"
            " WHEN :answer=1 THEN 'ANSWER'"
            " WHEN (SELECT COUNT(*) FROM tstat WHERE %s)=0 THEN 'UNABLE'"
            " WHEN (SELECT COUNT(*) FROM tstat WHERE %s AND complete=1)>=1 THEN 'CALL'"
            " ELSE 'ASK_OR_CHAIN' END" % (fit_sql, fit_sql), {'answer': 1 if answer else 0}).fetchone()[0]
        fitting = [r[0] for r in q('SELECT tid FROM tstat WHERE %s ORDER BY tid' % fit_sql)]
        out = {'kind': kind, 'cands': cands, 'provs': provs, 'fitting': fitting, 'values': values, 'ev': ev,
               'match': m, 'req': req, 'walk': walk, 'chain': False}
        if row == 'CALL':
            comp = [r[0] for r in q('SELECT tid FROM tstat WHERE %s AND complete=1 ORDER BY tid' % fit_sql)]
            if len(comp) > 1:
                if not self.pol.get('tie'):
                    raise Flag('tie without POL-TIE (NG-06)')
                best = q('SELECT MIN(cost) FROM tools WHERE tid IN (%s)' % ','.join(map(str, comp))).fetchone()[0]
                tier = [r[0] for r in q('SELECT tid FROM tools WHERE cost=? AND tid IN (%s)' % ','.join(map(str, comp)),
                                        (best,))]
                if len(tier) > 1:
                    tier = [r[0] for r in q('SELECT tid FROM tools WHERE pref=1 AND tid IN (%s)' %
                                            ','.join(map(str, tier)))]
                if len(tier) != 1:
                    raise Flag('tie left after the preferred check (NG-06)')
                comp = tier
                out['tie'] = True
            out['outcome'], out['tool'] = 'CALL', self.tools[comp[0]]['name']
            out['T'] = comp[0]
            stated = {r[0] for r in q("SELECT DISTINCT p FROM mentions WHERE kind IN ('val','cont')")}
            lost = stated - {p['name'] for p in self.tools[comp[0]]['params']}
            if lost:
                anyc = any(p['name'] in lost for i in cands + provs for p in self.tools[i]['params'])
                self.notes.append('NG-29%s: complete tool has no param for %d stated value(s)%s' %
                                  (' (C-INV case)' if case is not None else '', len(lost),
                                   '' if anyc else ' (param of no candidate tool or provider)'))
        elif row == 'ASK_OR_CHAIN':
            out['outcome'] = 'ASK'
            if self.pol.get('chain') and len(fitting) == 1:
                P = self.chain(fitting[0], ev, values, m)
                if P is not None:
                    out['outcome'], out['tool'], out['T'], out['chain'] = 'CALL', self.tools[P]['name'], P, True
        else:
            out['outcome'] = row
        return out

    def chain(self, F, ev, values, m):
        e = ev[F]
        if e['bad'] or e['unclear'] or len(e['miss']) != 1:
            return None
        kindm, ps, kw, _ = e['miss'][0]
        if kw not in ('required', 'else', 'dependentRequired'):
            return None                                     # a missing one-of pair never triggers a chain
        p = ps[-1]
        if values.get(p, ('absent',))[0] != 'absent':
            return None
        elig = []
        for P in self._provs:
            rets = [r[0] for r in self.db.execute('SELECT p FROM returns WHERE tid=?', (P,))]
            if p not in rets:
                continue
            if P not in ev:
                continue
            sc, pr, ro = m[P]
            pe = ev[P]
            if sc and pr and ro and not pe['bad'] and not pe['miss'] and not pe['unclear']:
                elig.append(P)
        if len(elig) == 1:
            return elig[0]
        if len(elig) > 1:
            raise Flag('two eligible providers (NG-02)')
        return None

    def near_misses(self, out):
        """Near-miss set (section 2, A59, R2-13): sorted (tool, component) pairs over the row's own-pack tools."""
        req = out['req']
        own = [i for i, t in enumerate(self.tools) if not t.get('borrowed')]
        excl = set()
        if out['outcome'] == 'CALL':
            excl.add(out['T'])
        if out['chain']:
            excl.add(out['fitting'][0])
        names = sorted({p['name'] for i in own for p in self.tools[i]['params']})
        vals = self.resolve(names)
        mode = os.environ.get('F12B_NM_VALUES', 'user')
        if mode == 'user':          # a non-candidate tool uses only the user's values (and defaults), never e's records
            vals = {k: v for k, v in vals.items() if v[0] != 'given' or v[2] == 'user'}
        elif mode == 'none':
            vals = {}
        m = self.match_sql(own)
        inv = self.pol.get('invalid', 'A')
        stated = {r[0] for r in self.db.execute("SELECT DISTINCT p FROM mentions WHERE kind IN ('val','cont')")}
        res = []
        for i in own:
            if i in excl:
                continue
            t = self.tools[i]
            e = out['ev'][i] if i in out['ev'] else self.tool_eval(i, vals)
            fails = [c for c, bad in (('action', t['a'] != req['a']), ('object', t['o'] != req['o']),
                                      ('scope', not m[i][0]), ('precondition', not m[i][1]),
                                      ('role', not m[i][2])) if bad]
            badu = {x[1] for x in e['bad']}                  # one non-accepted value = one param (or one pair)
            if inv == 'B' and badu:
                fails.append('value' if len(badu) == 1 else 'values')
            if len(fails) == 1 and fails[0] != 'values':
                res.append((t['name'], fails[0]))
                continue
            if not fails and out['outcome'] == 'CALL' and i in out['cands']:
                probs = [('miss', x) for x in e['miss']] + [('unclear', x) for x in e['unclear']]
                if inv == 'A':
                    probs += [('bad', x) for x in sorted(badu)]
                if len(probs) == 1:
                    k, x = probs[0]
                    if k == 'miss' and stated - {p['name'] for p in t['params']}:
                        res.append((t['name'], 'needed parameter'))
                    elif k == 'bad':            # spec section 2 (line 225): CALL-row kind under POL-INVALID A
                        res.append((t['name'], 'non-accepted value'))
        return sorted(res)

    def answer_shown(self, req, walk):
        f = req.get('field')
        if not f:
            raise Flag('info question without an asked field')
        # user statements of f (step-1 walk)
        last = None
        for s in walk:
            if s.get('p') == f and s['t'] in ('val', 'fact', 'cont'):
                if s['t'] == 'fact' and not self.fact_about_e(s):
                    continue
                last = s
            if s['t'] == 'retract' and s.get('p') == f:
                last = None
        if last is not None and last.get('v') is not None and str(last['v']).lower() not in MARKERS:
            return True
        if self.unclear_entity:
            return False
        N = self.pol.get('fresh')
        for i, (k, ts, flds) in enumerate(self.srcs):
            if not self.about[i]:
                continue
            for key, v in flds:
                if key == f and isinstance(v, str) and v.lower() not in MARKERS:
                    if k == 'record' or N is None:
                        return True
                    age = (self.ctx.now - datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M')).total_seconds() / 60
                    if 0 <= age <= N:
                        return True
        return False


# ----------------------------------------------------------------------------------------- forms and display
def outcome_class(text):
    s = text.lower()
    if 'cannot' in s or 'unable' in s:
        return 'UNABLE'
    if 'directly' in s or s.startswith('answer'):
        return 'ANSWER'
    if 'ask' in s or 'request the missing' in s:
        return 'ASK'
    if 'call' in s or 'tool' in s:
        return 'CALL'
    return None


def card_defs(row):
    d = {}
    for line in (row.get('card') or '').split('\n'):
        if line.startswith('- ') and ': ' in line:
            a, b = line[2:].split(': ', 1)
            d[a] = b
    return d


def display_outcome(row, outcome):
    defs = card_defs(row)
    hits = []
    for o in row['options']:
        cls = outcome_class(defs[o]) if o in defs else outcome_class(o)
        if cls == outcome:
            hits.append(o)
    return hits


def display_act(row, act):
    """act = ('call', T) | ('ask', p) | ('unable',) | ('answer',)."""
    defs = card_defs(row)
    hits = []
    for o in row['options']:
        d = defs.get(o)
        cls = outcome_class(d) if d is not None else outcome_class(o)
        if act[0] == 'call' and cls == 'CALL' and (o.endswith(' ' + act[1])):
            hits.append(o)
        elif act[0] == 'ask' and cls == 'ASK' and o.endswith(' ' + act[1]):
            hits.append(o)
        elif act[0] == 'unable' and cls == 'UNABLE':
            hits.append(o)
        elif act[0] == 'answer' and cls == 'ANSWER':
            hits.append(o)
    return hits


def yn(base, framing, neg, nmean):
    """framing table (section 8) then T-NEG polarity."""
    v = nmean if framing == 'N' else base
    if neg == 1:
        v = not v
    return 1 if v else 0


class Audit:
    """Schema-only validation of the proposed call (SEM-28, SEM-29, SEM-45)."""

    def __init__(self, R):
        self.R = R

    def defects(self, call):
        R = self.R
        t = R.tbyname.get(call['tool'])
        if t is None:
            return [(1, ())]
        pmap = {p['name']: p for p in t['params']}
        inst = {}
        for k, v in call['args']:
            inst[k] = audit_typed(pmap.get(k), v, R.ctx)
        for p in t['params']:
            if p['name'] not in inst and p.get('default') is not None:
                inst[p['name']] = fwd_typed(p, p['default'], R.ctx)
        val = compile_schema(t, R.ctx)
        out = []
        for e in val.iter_errors(inst):
            kw = e.validator
            sp = list(e.schema_path)
            if kw == 'additionalProperties':
                for x in inst:
                    if x not in pmap:
                        out.append((2, (x,)))
            elif kw == 'required':
                for r in e.validator_value:
                    if r not in inst:
                        if 'else' in sp:
                            c = self.cons_of(t, 'UNLESS', r)
                            out.append((9, (c['p'], c['q'])))
                        else:
                            out.append((3, (r,)))
            elif kw == 'dependentRequired':
                for a, bs in e.validator_value.items():
                    out.append((8, (a, bs[0])))
            elif kw in ('oneOf', 'anyOf'):
                mem = tuple(x['required'][0] for x in e.validator_value)
                out.append((10 if kw == 'oneOf' else 11, mem))
            elif kw == 'not':
                out.append((12, tuple(e.validator_value['required'])))
            elif kw == 'type':
                p = pmap[e.path[0]]
                if p['type'] == 'decimal' and isinstance(e.instance, float):
                    out.append((6, (p['name'],)))
                else:
                    out.append((4, (p['name'],)))
            elif kw == 'enum':
                out.append((5, (e.path[0],)))
            elif kw in ('minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum', 'minLength', 'maxLength',
                        'minItems', 'maxItems'):
                out.append((6, (e.path[0],)))
            elif kw == 'pattern':
                out.append((7, (e.path[0],)))
            elif kw == 'const':
                pass
            else:
                out.append((0, (kw,)))
        return out

    @staticmethod
    def cons_of(t, k, p):
        for c in t.get('cons') or []:
            if c['k'] == k and c['p'] == p:
                return c
        raise Flag('no %s constraint on %s' % (k, p))


def same_value(p, call_v, res_v, ctx):
    """Y-CORRECT value equality: call value (audit typing) vs step-1 value (forward typing) in T's form."""
    a = audit_typed(p, call_v, ctx)
    b = fwd_typed(p, res_v, ctx)
    if isinstance(a, list) and isinstance(b, list):
        return sorted(map(str, a)) == sorted(map(str, b))
    if type(a) is bool or type(b) is bool:
        return a is b
    return a == b


def needed_set(t, inst, ctx):
    pm = {p['name']: p for p in t['params']}
    need = set(p['name'] for p in t['params'] if p['required'])
    for c in t.get('cons') or []:
        if c['k'] == 'UNLESS':
            if c['q'] not in inst or inst[c['q']] != fwd_typed(pm[c['q']], c['v'], ctx):
                need.add(c['p'])
        elif c['k'] == 'ONLY_IF' and c['p'] in inst:
            need.add(c['q'])
    return need


def correct(R, out, call):
    """SEM-28b (section 3 step 9): CALL(T), names T, valid, and exactly the needed + user-asked values."""
    if out['outcome'] != 'CALL' or call['tool'] != out['tool']:
        return False
    if Audit(R).defects(call):
        return False
    t = R.tbyname[call['tool']]
    e = out['ev'][out['T']]
    vals = out['values']
    args = dict((k, v) for k, v in call['args'])
    need = needed_set(t, e['inst'], R.ctx)
    for p in t['params']:
        nm = p['name']
        r = vals.get(nm, ('absent',))
        dflt = p.get('default')
        if nm in need:
            if r[0] != 'given' or nm not in args or not same_value(p, args[nm], r[1], R.ctx):
                return False
        elif r[0] == 'given' and r[2] == 'user':
            if nm in args:
                if not same_value(p, args[nm], r[1], R.ctx):
                    return False
            elif not (dflt is not None and fwd_typed(p, r[1], R.ctx) == fwd_typed(p, dflt, R.ctx)):
                return False
        elif r[0] == 'given':
            raise Flag('optional param %s with a non-user value (NG-30)' % nm)
        else:
            if nm in args and not (dflt is not None and same_value(p, args[nm], dflt, R.ctx)):
                return False
    return True


# ------------------------------------------------------------------------------------------------ form golds
SPEC_ITEM = {'C-OUT': '1.2 C-OUT; section 3 steps 4-8; SEM-04', 'C-ACT': '1.2 C-ACT; SEM-35; section 3',
             'C-TOOL': '1.2 C-TOOL; SEM-46; SEM-19/23', 'C-PARAM': '1.2 C-PARAM; SEM-35; SEM-46',
             'C-DEFECT': '1.2 C-DEFECT; SEM-45; section 5 error table', 'C-VALUE': '1.2 C-VALUE; SEM-46 (R1-01)',
             'C-INV': '1.2 C-INV; SEM-46 (R2-15)', 'Y-CALLX': '8 framing table Y-CALLX',
             'Y-ASK': '8 framing table Y-ASK', 'Y-FIT': '8 framing table Y-FIT; SEM-36',
             'Y-DIRECT': '8 framing table Y-DIRECT', 'Y-VALID': '8 framing table Y-VALID; SEM-28',
             'Y-CORRECT': '8 framing table Y-CORRECT; SEM-28b'}
NONE_TOOL = 'None of the listed tools can do this'
NOTHING_MISSING = 'Nothing is missing'
NO_VALUE = 'No usable value, so ask the user'
CALL_VALID = 'Nothing, the call is valid'


def ask_target(R, out):
    if len(out['fitting']) != 1:
        raise Flag('ASK target with %d fitting tools (SEM-35)' % len(out['fitting']))
    e = out['ev'][out['fitting'][0]]
    ps = set(e['unclear'])
    for _, prs, kw, _ in e['miss']:
        if kw in ('required', 'else'):
            ps.add(prs[0])
        elif kw == 'dependentRequired':
            ps.add(prs[1])
        else:
            raise Flag('one-of pair missing on an ASK-target row (SEM-41)')
    if R.pol.get('invalid', 'A') == 'A':
        for _, prs, kw, _ in e['bad']:
            if len(prs) != 1:
                raise Flag('pair not accepted on an ASK-target row (SEM-41)')
            ps.add(prs[0])
    if len(ps) != 1:
        raise Flag('ASK target not unique: %d problems (SEM-35, NG-07)' % len(ps))
    return ps.pop()


def one(hits, what):
    if len(hits) != 1:
        raise Flag('%s: %d matching options' % (what, len(hits)))
    return hits[0]


def question_neg(row, side):
    """T-NEG count read from the question text itself: k_syn of the shared negcount (XF02)."""
    qt = side.get('question') or ''
    if row['qtype'] == 'choice':
        return side.get('neg') or 0
    if not qt or not (qt in row['instructions'] or qt in (row.get('card') or '')):
        raise Flag('yes/no question text not found in the row')
    return negcount.count(qt).k_syn


def form_gold(R, row, side, out):
    form = side['form']
    fr, neg = side.get('framing'), question_neg(row, side)
    if row['qtype'] != 'choice' and neg != (side.get('neg') or 0):
        raise Flag('negation count of the question %d != sidecar neg %s' % (neg, side.get('neg')))
    o = out['outcome']
    qd = side.get('q') or {}
    if form == 'C-OUT':
        return one(display_outcome(row, o), 'C-OUT outcome option')
    if form == 'C-ACT':
        act = {'CALL': lambda: ('call', out['tool']), 'ASK': lambda: ('ask', ask_target(R, out)),
               'UNABLE': lambda: ('unable',), 'ANSWER': lambda: ('answer',)}[o]()
        return one(display_act(row, act), 'C-ACT action option')
    if form == 'C-TOOL':
        if o == 'CALL':
            return one([x for x in row['options'] if x == out['tool']], 'C-TOOL tool option')
        if o == 'UNABLE':
            return one([x for x in row['options'] if x == NONE_TOOL], 'C-TOOL None option')
        raise Flag('C-TOOL on a %s row' % o)
    if form == 'C-PARAM':
        if o == 'CALL':
            return one([x for x in row['options'] if x == NOTHING_MISSING], 'C-PARAM Nothing option')
        if o == 'ASK':
            p = ask_target(R, out)
            return one([x for x in row['options'] if x == p], 'C-PARAM param option')
        raise Flag('C-PARAM on a %s row' % o)
    if form == 'C-VALUE':
        T = R.tbyname[qd['tool']]
        pm = {p['name']: p for p in T['params']}
        p = pm[qd['param']]
        r = out['values'].get(p['name'], ('absent',))
        v = r[1] if r[0] == 'given' else (p.get('default') if r[0] == 'absent' else None)
        if v is None:
            return one([x for x in row['options'] if x == NO_VALUE], 'C-VALUE no-value option')
        want = fwd_typed(p, v, R.ctx)
        return one([x for x in row['options'] if x != NO_VALUE and fwd_typed(p, x, R.ctx) == want
                    and type(fwd_typed(p, x, R.ctx)) == type(want)], 'C-VALUE value option')
    if form == 'C-DEFECT':
        d = Audit(R).defects(R.S['call'])
        if not d:
            return one([x for x in row['options'] if x == CALL_VALID], 'C-DEFECT valid option')
        if len(d) != 1:
            raise Flag('C-DEFECT call raises %d errors (SEM-33)' % len(d))
        cls, ps = d[0]
        if cls == 1:
            texts = [CLASS_PHRASE[1]]
        elif len(ps) == 1:
            texts = ['%s on %s' % (CLASS_PHRASE[cls], ps[0])]
        else:
            texts = ['%s on %s and %s' % (CLASS_PHRASE[cls], ps[0], ps[1]),
                     '%s on %s and %s' % (CLASS_PHRASE[cls], ps[1], ps[0])]
        return one([x for x in row['options'] if x in texts], 'C-DEFECT defect option')
    if form == 'C-INV':
        T = qd['tool']
        refs = sorted(row['options'], key=lambda x: row['state'].find(x))
        if any(row['state'].find(x) < 0 for x in refs) or len(refs) != len(side['cases']):
            raise Flag('C-INV case references not all in state')
        good = []
        for ref, case in zip(refs, side['cases']):
            co = R.solve(case=case, with_context=False)
            if co['outcome'] == 'CALL' and co['tool'] == T and not co.get('tie') and not co['chain']:
                good.append(ref)
        return one(good, 'C-INV request whose outcome is CALL(T)')
    if form == 'Y-CALLX':
        base = o == 'CALL' and out['tool'] == qd['tool']
        return yn(base, fr, neg, not base)
    if form == 'Y-ASK':
        if o not in ('CALL', 'ASK'):
            raise Flag('Y-ASK on a %s row (SEM-36)' % o)
        return yn(o == 'CALL', fr, neg, o == 'ASK')
    if form == 'Y-FIT':
        if o == 'ANSWER':
            raise Flag('Y-FIT on an ANSWER row (SEM-36)')
        return yn(o in ('CALL', 'ASK'), fr, neg, o == 'UNABLE')
    if form == 'Y-DIRECT':
        return yn(o == 'ANSWER', fr, neg, o != 'ANSWER')
    if form == 'Y-VALID':
        v = not Audit(R).defects(R.S['call'])
        return yn(v, fr, neg, not v)
    if form == 'Y-CORRECT':
        c = correct(R, out, R.S['call'])
        return yn(c, fr, neg, not c)
    raise Flag('unknown form %s' % form)


def pack_reads(files):
    """Pre-pass: the pack's one read action (R5-03) = the action of its requests that ask for a field."""
    reads = collections.defaultdict(set)
    card_pack = {}
    for name in files:
        with open(os.path.join(OUT, name + '.jsonl')) as fr, open(os.path.join(OUT, 'side', name + '.side.jsonl')) as fs:
            for lr, ls in zip(fr, fs):
                side = json.loads(ls)
                pk = json.loads(lr)['meta']['domain_pack']
                card_pack[side['card']] = pk
                sts = [s for t in side['S']['conv'] for s in t.get('st', [])] + \
                      [s for c in (side.get('cases') or []) for s in c]
                for s in sts:
                    if s['t'] == 'req' and s.get('field'):
                        reads[pk].add(s['a'])
    bad = {k: sorted(v) for k, v in reads.items() if len(v) != 1}
    return {k: next(iter(v)) for k, v in reads.items() if len(v) == 1}, bad


def check_file(name, reads):
    res = {'rows': 0, 'gold_mismatch': 0, 'outcome_mismatch': 0, 'kind_mismatch': 0, 'near_miss_mismatch': 0,
           'neg_mismatch': 0, 'structure_notes': 0, 'flags': 0,
           'by_form': collections.Counter()}
    mism = []
    with open(os.path.join(OUT, name + '.jsonl')) as fr, open(os.path.join(OUT, 'side', name + '.side.jsonl')) as fs:
        for lr, ls in zip(fr, fs):
            if LIMIT and res['rows'] >= LIMIT:
                break
            row, side = json.loads(lr), json.loads(ls)
            if row['id'] != side['id']:
                raise SystemExit('row/sidecar order differs in %s' % name)
            res['rows'] += 1
            form = side['form']
            res['by_form'][form] += 1
            base = {'file': name, 'id': row['id'], 'form': form, 'sampler': row['meta']['sampler'],
                    'card': side['card']}
            try:
                R = Row(row, side, reads.get(row['meta']['domain_pack']))
                if form == 'C-INV':
                    out = None
                    g = form_gold(R, row, side, {'outcome': None})
                else:
                    out = R.solve()
                    g = form_gold(R, row, side, out)
            except Flag as ex:
                res['flags'] += 1
                mism.append(dict(base, what='flag', solver_b=str(ex), row_gold=row['gold'],
                                 spec_item=SPEC_ITEM.get(form)))
                continue
            for note in R.notes:
                res['structure_notes'] += 1
                mism.append(dict(base, what='structure', solver_b=note, spec_item=note.split(':')[0]))
            if g != row['gold']:
                res['gold_mismatch'] += 1
                mism.append(dict(base, what='gold', solver_b=g, row_gold=row['gold'], solver_a_outcome=side.get('outcome'),
                                 solver_b_outcome=out and out['outcome'], spec_item=SPEC_ITEM.get(form)))
            if out is not None:
                if out['outcome'] != side.get('outcome'):
                    res['outcome_mismatch'] += 1
                    mism.append(dict(base, what='outcome', solver_b=out['outcome'] + ('(%s)' % out['tool'] if out['outcome'] == 'CALL' else ''),
                                     solver_a=side.get('outcome') + ('(%s)' % side.get('tool') if side.get('outcome') == 'CALL' else ''),
                                     spec_item='section 3 (SEM-04 decision table)'))
                elif out['outcome'] == 'CALL' and out['tool'] != side.get('tool'):
                    res['outcome_mismatch'] += 1
                    mism.append(dict(base, what='outcome', solver_b='CALL(%s)' % out['tool'],
                                     solver_a='CALL(%s)' % side.get('tool'), spec_item='section 3 steps 6-7'))
                try:
                    nm = [list(x) for x in R.near_misses(out)]
                except Flag as ex:
                    nm = 'flag: %s' % ex
                if nm != sorted([list(x) for x in side.get('near_miss') or []]):
                    res['near_miss_mismatch'] += 1
                    mism.append(dict(base, what='near_miss', solver_b=nm, solver_a=side.get('near_miss'),
                                     spec_item='section 2 near-miss (A59, R2-13); section 5 derived meta'))
                if out['kind'] != {'action': 'action', 'info': 'info', 'catalog': 'catalog'}.get(side.get('kind')):
                    res['kind_mismatch'] += 1
                    mism.append(dict(base, what='kind', solver_b=out['kind'], solver_a=side.get('kind'),
                                     spec_item='section 3 step 0 (R1-06)'))
    res['by_form'] = dict(res['by_form'])
    return res, mism


def main(argv):
    files = argv[1:] or ['candidates_r1', 'qc_sample', 'mixdev_S5']
    reads, bad = pack_reads(['candidates_r1', 'qc_sample', 'mixdev_S5'])
    summary = {'solver': 'F12 solver B (sqlite3 + jsonschema, declarative)', 'g0_sha256': hashlib.sha256(
        open(os.path.join(os.path.dirname(HERE), 'G0_SPEC.md'), 'rb').read()).hexdigest(),
        'read_action_conflicts': bad, 'files': {}}
    allm = []
    for name in files:
        res, mism = check_file(name, reads)
        summary['files'][name] = res
        allm += mism
        print(name, json.dumps({k: v for k, v in res.items() if k != 'by_form'}), flush=True)
    g2 = [m for m in allm if m['what'] != 'structure']
    viol = collections.defaultdict(lambda: {'rows': 0, 'by_sampler': collections.Counter(), 'by_file': collections.Counter(),
                                            'ids': [], 'detail': collections.Counter()})
    for m in allm:
        if m['what'] == 'structure':
            v = viol[m['spec_item']]
            v['rows'] += 1
            v['by_sampler'][m['sampler']] += 1
            v['by_file'][m['file']] += 1
            v['ids'].append(m['id'])
            v['detail'][m['solver_b']] += 1
    summary['total_rows'] = sum(r['rows'] for r in summary['files'].values())
    summary['g2_mismatch_entries'] = len(g2)
    summary['g2_mismatch_rows'] = len({(m['file'], m['id']) for m in g2})
    summary['gold_mismatch_rows'] = len({(m['file'], m['id']) for m in g2 if m['what'] in ('gold', 'flag')})
    summary['spec_violation_rows'] = {k: v['rows'] for k, v in viol.items()}
    summary['inputs_sha256'] = {}
    for name in files:
        for pth in (os.path.join(OUT, name + '.jsonl'), os.path.join(OUT, 'side', name + '.side.jsonl')):
            summary['inputs_sha256'][os.path.relpath(pth, os.path.dirname(HERE))] = hashlib.sha256(open(pth, 'rb').read()).hexdigest()
    summary['near_miss_value_mode'] = os.environ.get('F12B_NM_VALUES', 'user')
    with open(os.path.join(HERE, 'mismatch.json' if not LIMIT else 'mismatch_partial.json'), 'w') as f:
        json.dump({'summary': summary, 'mismatches': g2,
                   'spec_violations': {k: dict(v, by_sampler=dict(v['by_sampler']), by_file=dict(v['by_file']),
                                               detail=dict(v['detail'])) for k, v in viol.items()}}, f, indent=1)
    print(json.dumps({k: summary[k] for k in ('total_rows', 'g2_mismatch_rows', 'gold_mismatch_rows',
                                              'spec_violation_rows')}))


if __name__ == '__main__':
    main(sys.argv)
