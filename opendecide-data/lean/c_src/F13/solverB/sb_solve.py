"""Solver B (F13): question parse + declarative solving on the parsed facts.

Paradigm (different from solver A's forward replay + critical-point enumeration):
  * Q-P: rule resolution as a constraint table: every rule's applicability is a boolean literal; traced
    attributes and dates become interval partitions (one representative per maximal constant region);
    the answer set is the image of the resolution function over those regions.
  * Q-R (decisions, versions, life cycles): backward walks from the question date over sqlite-ordered events.
  * Q-T / AG-3 / counts: sqlite queries over the parsed rows.
  * Open world: answer sets with an 'other answers possible' flag driven by part traces (adversarial
    completion of a missing part of the label's type and scope only, SEM-02 / 2.4).
Returns a set of possible answers and a flag `more`.
"""
import itertools
import re
import sqlite3
from fractions import Fraction

import sb_core as C
from sb_facts import TR, Item

CONFLICT = '<CONFLICT>'
NOANS = '<NOANSWER>'
D = C.DATE_P
IDP = C.ID_P


class SolveError(Exception):
    pass


# ================================================================ question parsing
def _q(pat):
    return re.compile(pat)


CLAIMS = [
    ('dec', _q(r"^the decision on (.+?) (%s) for (.+?) is (not )?(.+) as of (%s)$" % (IDP, D))),
    ('holder', _q(r"^(.+?) is (not )?the holder of (.+?) (%s) for (.+?) as of (%s)$" % (IDP, D))),
    ('ver', _q(r"^version (\S+) of the (.+?) setting is (not )?in force for (.+?) as of (%s)$" % D)),
    ('stat', _q(r"^the status of (.+?) (%s) for (.+?) is (not )?(.+) as of (%s)$" % (IDP, D))),
    ('argmax', _q(r"^(?:(.+?) )?(%s) (has|does not have) the (highest|lowest) (.+?) in table (\S+) for (.+?) from (%s) "
                  r"through (%s)$" % (IDP, D, D))),
    ('cmp', _q(r"^the (.+?) of (?:[a-z][a-z ]*? )?(%s) is (not )?(higher|lower|greater|smaller|more|less) than that of "
               r"(?:[a-z][a-z ]*? )?(%s) in table (\S+) for (.+?) from (%s) through (%s)$" % (IDP, IDP, D, D))),
    ('crit', _q(r"^(?:(.+?) )?(%s) (has|does not have) (.+?) of (at least|at most|more than|less than) (.+?) in table "
                r"(\S+) for (.+?) from (%s) through (%s)$" % (IDP, D, D))),
    ('tp', _q(r"^(.+?) (%s) is (not )?(.+) for (%s) through (%s)$" % (IDP, D, D))),
    ('qp', _q(r"^the outcome for (.+)$")),
]


def parse_question(instr):
    """Return dict(frame, fneg, claim / choice spec). Uses the last question in the text."""
    text = instr
    cands = []
    for m in re.finditer(r"(?:Under the report's criteria, )?[Dd]oes the document (fail to )?(establish that|settle whether) (.+?)\?", text):
        cands.append((m.start(), dict(frame='establish' if m.group(2).startswith('establish') else 'settle',
                                      fneg=bool(m.group(1)), claim=m.group(3))))
    for m in re.finditer(r"(?:Under the report's criteria, )?[Ii]s it (true|not the case) that (.+?)\?", text):
        cands.append((m.start(), dict(frame='yn', fneg=(m.group(1) == 'not the case'), claim=m.group(2))))
    pats = [
        ('qp_case', r"What is the outcome for (.+?)\?"),
        ('inv', r"Which of these cases meets rule (\S+)\?"),  # G0 3.1 inverted rows / SEM-56 (repair r5)
        ('tp_choice', r"Under the report's criteria, what is the outcome for (.+?) (%s) for (%s) through (%s)\?" % (IDP, D, D)),
        ('dec', r"What is the decision on (.+?) (%s) for (.+?) as of (%s)\?" % (IDP, D)),
        ('holder', r"Who is the holder of (.+?) (%s) for (.+?) as of (%s)\?" % (IDP, D)),
        ('ag1i', r"How many open action items for (.+?) have (.+?) as their holder as of (%s)\?" % D),
        ('ag1x', r"How many (exceptions|exclusions) for (.+?) are active as of (%s)\?" % D),
        ('ag1h', r"How many (holds|conditions) on (.+?) (%s) for (.+?) are active as of (%s)\?" % (IDP, D)),
        ('ver_rule', r"Which version of rule (\S+) is in force for (.+?) as of (%s)\?" % D),
        ('ver_set', r"Which version of the (.+?) setting is in force for (.+?) as of (%s)\?" % D),
        ('val_set', r"What is the value of the (.+?) setting in force for (.+?) as of (%s)\?" % D),
        ('stat', r"What is the status of (.+?) (%s) for (.+?) as of (%s)\?" % (IDP, D)),
        ('logcnt', r"How many (.+?) entries for (.+?) set the status of an? (.+?) to (.+?) as of (%s)\?" % D),
        ('total', r"What is the total (.+?) in table (\S+) for (.+?) from (%s) through (%s)\?" % (D, D)),
        ('argmax_c', r"Which (.+?) in table (\S+) for (.+?) from (%s) through (%s) (?:has|have) the (highest|lowest) (.+?)\?"
         % (D, D)),
        ('tcount', r"How many (.+?) in table (\S+) for (.+?) from (%s) through (%s) have (.+?) of (.+?)\?" % (D, D)),
        ('tset', r"Which (.+?) in table (\S+) for (.+?) from (%s) through (%s) have (.+?) of (.+?)\?" % (D, D)),
        # plain yes/no question forms (rewritten to claims)
        ('yn_qp', r"Is the outcome for (.+?)\?"),
        ('yn_dec', r"Is the decision on (.+?) (%s) for (.+?) as of (%s)( .+?)?\?" % (IDP, D)),
        ('yn_holder', r"Is (.+?) the holder of (.+?) (%s) for (.+?) as of (%s)\?" % (IDP, D)),
        ('yn_ver', r"Is version (\S+) of the (.+?) setting in force for (.+?) as of (%s)\?" % D),
        ('yn_stat', r"Is the status of (.+?) (%s) for (.+?) as of (%s)( .+?)?\?" % (IDP, D)),
        ('yn_tp', r"Under the report's criteria, is (.+?) (%s) (.+) for (%s) through (%s)\?" % (IDP, D, D)),
        ('yn_cmp', r"Is the (.+?) of (?:[a-z][a-z ]*? )?(%s) (higher|lower|greater|smaller|more|less) than that of (?:[a-z][a-z ]*? )?(%s) in table (\S+) for (.+?) "
                   r"from (%s) through (%s)\?" % (IDP, IDP, D, D)),
        ('yn_arg', r"Does (?:(.+?) )?(%s) have the (highest|lowest) (.+?) in table (\S+) for (.+?) from (%s) through (%s)\?"
         % (IDP, D, D)),
        ('yn_crit', r"Does (?:(.+?) )?(%s) have (.+?) of (at least|at most|more than|less than) (.+?) in table (\S+) for (.+?) "
                    r"from (%s) through (%s)\?" % (IDP, D, D)),
    ]
    for name, p in pats:
        for m in re.finditer(p, text):
            cands.append((m.start(), dict(frame='q', kind=name, m=m)))
    if not cands:
        raise SolveError('no question')
    maxpos = max(c[0] for c in cands)
    best = [c[1] for c in cands if c[0] == maxpos]
    # prefer the most specific pattern at that position
    order = ['establish', 'settle', 'yn']
    for b in best:
        if b['frame'] in order:
            return b
    pref = ['tp_choice', 'yn_tp', 'yn_dec', 'yn_holder', 'yn_ver', 'yn_stat', 'yn_cmp', 'yn_crit', 'yn_arg']
    for k in pref:
        for b in best:
            if b.get('kind') == k:
                return b
    return best[0]


# ================================================================ helpers
def eq(a, b):
    return C.norm(a) == C.norm(b)


def unit_ok(mark, unit):
    return mark is None or (unit is not None and eq(mark, unit))


def num_of(v):
    if v is None or v == TR:
        return v
    if isinstance(v, (Fraction, int)):
        return Fraction(v)
    p = C.parse_num(str(v))
    return p[0] if p else None


def cmp_op(a, op, b):
    if op == '>=':
        return a >= b
    if op == '<=':
        return a <= b
    if op == '>':
        return a > b
    if op == '<':
        return a < b
    raise SolveError('op ' + op)


def eval_cond(c, vals, missing):
    k = c[0]
    if k == 'atom':
        _, attr, op, val, unit = c
        v = vals.get(C.norm(attr))
        if v is None:
            missing.add(attr)
            return False
        if v == TR:
            raise SolveError('unassigned trace ' + attr)
        return cmp_op(v, op, val)
    if k == 'or':
        return any(eval_cond(x, vals, missing) for x in c[1])
    if k == 'and':
        return all(eval_cond(x, vals, missing) for x in c[1])
    if k == 'xor':
        return sum(1 for x in c[1] if eval_cond(x, vals, missing)) == 1
    raise SolveError('bad cond %r' % (c,))


def cond_points(c, acc):
    if c[0] == 'atom':
        acc.setdefault(C.norm(c[1]), set()).add(c[3])
    elif c[0] in ('or', 'and', 'xor'):
        for x in c[1]:
            cond_points(x, acc)


def region_reps(points, step=Fraction(1), lo=Fraction(0)):
    """One representative per maximal region on which every predicate 'x op p' is constant (x >= lo)."""
    pts = sorted(set(p for p in points))
    reps = set()
    if not pts:
        return [lo]
    # points themselves and the open intervals between them, below the first and above the last
    for p in pts:
        if p >= lo:
            reps.add(p)
    edges = [lo - 1] + pts
    for a, b in zip(edges, edges[1:] + [pts[-1] + 3 * step]):
        # a value strictly between a and b on the step grid
        x = (a // step + 1) * step
        if x <= a:
            x += step
        if x < b and x >= lo:
            reps.add(x)
    reps.add(max(lo, pts[-1] + step))
    reps.add(lo)
    return sorted(reps)


# ================================================================ rule base (Q-P)
class RuleBase:
    def __init__(self, f, card):
        self.f = f
        self.card = card
        self.rules = {}
        for vid, v in f.versions.items():
            self.rules.setdefault(v.rule, []).append(v)

    def vmark(self, v):
        m = self.f.marks.get(('Version', v.vid))
        if m is None:
            m = self.f.secs[v.sec].unit
        return m

    def vstatus(self, v):
        if v.vid in self.f.voided:
            return 'void'
        s = self.f.stat.get(('Version', v.vid))
        if s is None:
            s = self.f.secs[v.sec].status or 'in force'
        return s

    def veff(self, v):
        w = self.f.win.get(('Version', v.vid))
        if w and w[0] is not None:
            return w[0]
        r = self.f.reg.get(v.vid)
        return r[0] if r else None

    def vend(self, v):
        w = self.f.win.get(('Version', v.vid))
        return (w[1], w[2]) if w else ('none', None)

    @staticmethod
    def rev(vid):
        m = re.search(r"\.(\d+)$", vid)
        return int(m.group(1)) if m else 0

    def in_force(self, vers, unit, G):
        cands = [v for v in vers if unit_ok(self.vmark(v), unit) and self.vstatus(v) == 'in force'
                 and self.veff(v) is not None and self.veff(v) <= G]
        if not cands:
            return None
        best = max(cands, key=lambda v: (self.veff(v), self.rev(v.vid)))
        ek, ed = self.vend(best)
        if ek == 'through' and G > ed:
            return None
        if ek == 'repealed' and G >= ed:
            return None
        return best

    # exceptions
    def emark(self, e):
        m = self.f.marks.get(('Exception', e.eid))
        if m is None:
            m = self.f.secs[e.sec].unit
        return m

    def e_active(self, e, G):
        if e.eid in self.f.voided:
            return False
        st = self.f.stat.get(('Exception', e.eid)) or self.f.secs[e.sec].status or 'in force'
        if st != 'in force':
            return False
        w = self.f.win.get(('Exception', e.eid))
        if not w or w[0] is None:
            return False
        if w[0] > G:
            return False
        if w[1] == 'through' and G > w[2]:
            return False
        if w[1] == 'repealed' and G >= w[2]:
            return False
        return True

    def switched_off(self, vals, unit, G, missing):
        """Set of rule ids switched off for this case (SEM-25, one level of exceptions to exceptions)."""
        act = [e for e in self.f.exceptions.values() if self.e_active(e, G) and unit_ok(self.emark(e), unit)
               and eval_cond(e.cond, vals, missing)]
        dead = {e.target for e in act if e.tkind == 'exception'}
        off = set()
        for e in act:
            if e.tkind == 'rule' and e.eid not in dead:
                off.add(e.target)
        return off

    def resolve(self, vals, unit, G, force_off=(), force_on=(), extra=(), missing=None):
        if missing is None:
            missing = set()
        off = self.switched_off(vals, unit, G, missing)
        off = (off | set(force_off)) - set(force_on)
        app = []
        for R, vers in self.rules.items():
            v = self.in_force(vers, unit, G)
            if v is None or R in off:
                continue
            if eval_cond(v.cond, vals, missing):
                app.append((v, self.vmark(v), self.veff(v), v.outcome))
        for x in extra:
            app.append(x)
        if not app:
            return self.card.default if self.card.default else NOANS
        if self.card.prec == 'specific':
            spec = [a for a in app if a[1] is not None]
            grp = spec if spec else app
        elif self.card.prec == 'later':
            mx = max(a[2] for a in app)
            grp = [a for a in app if a[2] == mx]
        else:
            grp = app
        outs = {a[3] for a in grp}
        if len(outs) == 1:
            return outs.pop()
        return CONFLICT

    def applicable_true(self, vals, unit, G):
        miss = set()
        out = []
        for R, vers in self.rules.items():
            v = self.in_force(vers, unit, G)
            if v is not None and eval_cond(v.cond, vals, miss):
                out.append(R)
        return out


def solve_case_outcome(f, card, case):
    """case: Item(vals: {normattr: Fraction|TR|str}, unit, gov: ord|TR). Returns (answers, more, info)."""
    rb = RuleBase(f, card)
    pts = {}
    for v in f.versions.values():
        cond_points(v.cond, pts)
    for e in f.exceptions.values():
        cond_points(e.cond, pts)
    tvars = [k for k, v in case.vals.items() if v == TR]
    dims = []
    for k in tvars:
        dims.append((k, region_reps(pts.get(k, set()))))
    if case.gov == TR:
        dpts = set()
        for v in f.versions.values():
            e = rb.veff(v)
            if e is not None:
                dpts.add(Fraction(e))
            ek, ed = rb.vend(v)
            if ed is not None:
                dpts.add(Fraction(ed))
        for (kind, i), w in f.win.items():
            if w[0] is not None:
                dpts.add(Fraction(w[0]))
            if w[2] is not None:
                dpts.add(Fraction(w[2]))
        dims.append(('__gov', region_reps(dpts, lo=Fraction(1))))
    answers = set()
    more = False
    missing = set()
    unit = case.unit
    rel_parts = [p for p in f.parts if p.ptype not in ('ti',) and
                 ((p.unit is not None and unit is not None and eq(p.unit, unit)) or
                  (p.ent is not None and case.ent is not None and p.ent == case.ent))]
    for combo in itertools.product(*[d[1] for d in dims]) if dims else [()]:
        vals = dict(case.vals)
        G = case.gov
        for (k, _), x in zip(dims, combo):
            if k == '__gov':
                G = int(x)
            else:
                vals[k] = x
        base = rb.resolve(vals, unit, G, missing=missing)
        answers.add(base)
        for p in rel_parts:
            if p.ptype == 'versions':
                if p.arg in rb.switched_off(vals, unit, G, missing):
                    continue
                more = True
            elif p.ptype == 'exceptions_to':
                answers.add(rb.resolve(vals, unit, G, force_off={p.arg}, missing=missing))
            elif p.ptype == 'exceptions':
                rules_true = rb.applicable_true(vals, unit, G)
                offs = rb.switched_off(vals, unit, G, missing)
                cand = sorted(set(rules_true) | offs)
                for r in range(len(cand) + 1):
                    for sub in itertools.combinations(cand, r):
                        answers.add(rb.resolve(vals, unit, G, force_off=set(sub), force_on=offs - set(sub),
                                               missing=missing))
            elif p.ptype in ('rules', 'amendments'):
                more = True
    return answers, more, dict(missing=missing, tvars=tvars)


# ---------------------------------------------------------------- case from text
def case_from_record(f, card, rid):
    recs = f.records.get(rid.upper())
    if not recs:
        raise SolveError('record not found %s' % rid)
    rec = recs[0]
    return _case(f, card, rec.fields, rid)


def _case(f, card, fields, rid):
    vals = {}
    unit = None
    gov = None
    gname = C.norm(card.gov_name) if card.gov_name else None
    sk = C.norm(card.scope_kind) if card.scope_kind else None
    for k, v in fields.items():
        if gname and k == gname:
            gov = TR if v == TR else C.parse_date(v)
            continue
        if sk and k == sk:
            unit = v
            continue
        if v == TR:
            vals[k] = TR
            continue
        n = C.parse_num(v)
        if n is not None and not C.DATE_RE.match(v):
            vals[k] = n[0]
        else:
            vals[k] = v
    if gov is None:
        # fall back: a field ending in 'date'
        for k, v in fields.items():
            if k.endswith(' date'):
                gov = TR if v == TR else C.parse_date(v)
    return Item(vals=vals, unit=unit, gov=gov, ent=rid)


def case_from_desc(f, card, desc):
    """'a machine with guard gap 30 mm, lost work days 7 days, mill area planer mill and machine date 21 April 2051'"""
    m = re.match(r"^an? (.+?) with (.+)$", desc.strip())
    if not m:
        raise SolveError('case desc ' + desc[:60])
    body = m.group(2)
    gname = card.gov_name
    mg = re.search(r"(?:,| and) %s (%s)$" % (re.escape(gname), D), body) if gname else None
    fields = {}
    if mg:
        fields[C.norm(gname)] = mg.group(1)
        body = body[:mg.start()]
    known = set()
    for v in f.versions.values():
        known |= {C.norm(a) for a in C.cond_attrs(v.cond)}
    for e in f.exceptions.values():
        known |= {C.norm(a) for a in C.cond_attrs(e.cond)}
    if card.scope_kind:
        known.add(C.norm(card.scope_kind))
    for r in f.records_list:
        known |= set(r.fields.keys())
    pieces = re.split(r", | and ", body)
    for pc in pieces:
        pc = pc.strip()
        best = None
        for k in known:
            if C.norm(pc).startswith(k + ' ') and (best is None or len(k) > len(best)):
                best = k
        if best is not None:
            toks = pc.split()
            nw = len(best.split())
            for i in range(1, len(toks) + 1):
                if C.norm(' '.join(toks[:i])) == best:   # attribute names with hyphens ('small-end diameter')
                    nw = i
                    break
            raw = ' '.join(toks[nw:])
            fields[best] = raw
        else:
            mm = re.match(r"^(.+?) (\d[\d,.]*.*)$", pc)
            if mm:
                fields[C.norm(mm.group(1))] = mm.group(2)
            elif fields:
                # continuation of the previous value (a name containing ' and ')
                lk = list(fields.keys())[-1]
                fields[lk] = fields[lk] + ' and ' + pc
    return _case(f, card, fields, None)


def parse_case(f, card, s):
    s = s.strip()
    m = re.match(r"^(.+?) record (%s)$" % IDP, s)
    if m:
        return case_from_record(f, card, m.group(2))
    return case_from_desc(f, card, s)


def split_case_outcome(f, card, s):
    """'<case> is (not )?<X>' or '<case> <X>' -> (case_text, neg, X)."""
    m = re.match(r"^(.+? record %s) is (not )?(.+)$" % IDP, s)
    if m:
        return m.group(1), bool(m.group(2)), m.group(3)
    m = re.match(r"^(.+? record %s) (.+)$" % IDP, s)
    if m:
        return m.group(1), False, m.group(2)
    gname = card.gov_name or 'date'
    m = re.match(r"^(an? .+? %s %s) is (not )?(.+)$" % (re.escape(gname), D), s)
    if m:
        return m.group(1), bool(m.group(2)), m.group(3)
    m = re.match(r"^(an? .+? %s %s) (.+)$" % (re.escape(gname), D), s)
    if m:
        return m.group(1), False, m.group(2)
    raise SolveError('case/outcome split ' + s[:80])
