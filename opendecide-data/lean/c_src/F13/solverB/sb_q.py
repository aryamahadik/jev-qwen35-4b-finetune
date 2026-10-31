"""Solver B (F13): record chains, life cycles, logs, tables (sqlite) and the row dispatcher."""
import re
import sqlite3
import itertools
from fractions import Fraction

import sb_core as C
from sb_facts import TR, Item, extract
from sb_solve import (SolveError, CONFLICT, NOANS, RuleBase, eq, unit_ok, parse_question, solve_case_outcome,
                      parse_case, split_case_outcome, CLAIMS, region_reps, cmp_op)

DAY = 1440


def _parts(f, types, unit=None, ent=None):
    out = []
    for p in f.parts:
        if p.ptype not in types:
            continue
        if unit is not None and p.unit is not None and eq(p.unit, unit):
            out.append(p)
        elif ent is not None and p.ent is not None and p.ent == ent:
            out.append(p)
    return out


def sec_unit(f, si):
    return f.secs[si].unit


# ================================================================ S2 decisions (notices)
def s2_decision(f, card, ent, unit, Dd):
    """Backward walk from the question date over the matter's notices (SEM-26, 27, 29, 50)."""
    entries = [n for n in f.notices if n.ent == ent and unit_ok(sec_unit(f, n.sec), unit)]
    voids = {(c.kind, c.date) for c in f.ncorr if c.ent == ent and c.void and unit_ok(sec_unit(f, c.sec), unit)}
    outc = {(c.kind, c.date): (c.new, c.old) for c in f.ncorr if c.ent == ent and not c.void
            and unit_ok(sec_unit(f, c.sec), unit)}
    con = sqlite3.connect(':memory:')
    con.execute("create table e(i int, kind text, date int, status text, outcome text)")
    for i, n in enumerate(entries):
        st = f.secs[n.sec].status or 'in force'
        con.execute("insert into e values(?,?,?,?,?)", (i, n.kind, n.date, st, n.outcome))
    rows = con.execute("select i, kind, date, status, outcome from e where date <= ? order by date desc", (Dd,)).fetchall()
    ans = None
    for i, kind, date, st, out in rows:
        if st != 'in force':
            continue
        if (kind, date) in voids:
            continue
        if (kind, date) in outc:
            out = outc[(kind, date)][0]
        ans = out
        break
    more = bool(_parts(f, ('decision notices', 'records', 'entries'), unit=unit, ent=ent))
    return ({ans} if ans is not None else {NOANS}), more


# ================================================================ S6 motions
def s6_decision(f, card, ent, unit, Dd):
    k = card.vote_k
    if k is None:
        raise SolveError('no vote rule')
    mot = []
    for m in f.motions:
        s = f.secs[m.sec]
        if m.ent != ent or not unit_ok(s.unit, unit) or s.meeting is None:
            continue
        if (s.status or 'in force') != 'in force':
            continue
        mot.append((s.meeting, m))
    voids = set()
    outc = {}
    for c in f.mcorr:
        s = f.secs[c.sec]
        if c.ent != ent or not unit_ok(s.unit, unit):
            continue
        if c.void:
            voids.add(({'decision': 'make', 'revision': 'revise', 'reversal': 'reverse'}[c.kind], c.date))
        else:
            outc[(c.mkind, c.mdate)] = c.new
    ans = None
    for date, m in sorted(mot, key=lambda x: -x[0]):
        if date > Dd:
            continue
        if m.yes < k:
            continue
        if (m.kind, date) in voids:
            continue
        ans = outc.get((m.kind, date), m.outcome)
        break
    more = bool(_parts(f, ('motions', 'decision notices', 'entries'), unit=unit, ent=ent))
    return ({ans} if ans is not None else {NOANS}), more


def action_state(a, Dd):
    holder = None
    open_ = False
    for verb, who, date in sorted(a.evs, key=lambda x: x[2]):
        if date > Dd:
            break
        if verb == 'assigned':
            holder, open_ = who, True
        elif verb == 'transferred':
            holder = who
        elif verb == 'closed':
            open_ = False
        elif verb == 'reopened':
            open_ = True
    return open_, holder


def s6_holder(f, aid, unit, Dd):
    its = [a for a in f.actions if a.aid == aid and unit_ok(sec_unit(f, a.sec), unit)]
    if not its:
        # item not in the copy: unknown when an action-items part of this unit is missing (SEM-02, A04)
        return {NOANS}, bool(_parts(f, ('action items',), unit=unit))
    o, h = action_state(its[0], Dd)
    more = bool(_parts(f, ('action items',), unit=unit))
    return {h if h else NOANS}, more


def s6_count_open(f, unit, holder, Dd):
    n = 0
    for a in f.actions:
        mk = f.marks.get(('Action item', a.aid)) or sec_unit(f, a.sec)
        if mk is None or not eq(mk, unit):
            continue
        o, h = action_state(a, Dd)
        if o and h is not None and eq(h, holder):
            n += 1
    more = bool(_parts(f, ('action items',), unit=unit))
    return {n}, more


# ================================================================ S2 holds / conditions
def hold_active(h, Dd):
    if h.kind == 'Hold':
        st = h.ev.get('placed')
        end = h.ev.get('released')
    else:
        st = h.ev.get('imposed')
        ends = [h.ev.get('met'), h.ev.get('waived')]
        ends = [x for x in ends if x is not None]
        end = min(ends) if ends else None
    if st is None or st > Dd:
        return False
    if end is not None and end <= Dd:
        return False
    return True


def s2_count_holds(f, kind, ent, unit, Dd):
    K = 'Hold' if kind.startswith('hold') else 'Condition'
    n = 0
    for h in f.holds:
        if h.kind != K or h.ent != ent:
            continue
        mk = f.marks.get((K, h.hid)) or sec_unit(f, h.sec)
        if mk is None or not eq(mk, unit):
            continue
        if hold_active(h, Dd):
            n += 1
    more = bool(_parts(f, ('holds' if K == 'Hold' else 'conditions',), unit=unit, ent=ent))
    return {n}, more


# ================================================================ S1 / S4 AG-1 window-item counts
def count_exceptions(f, card, unit, Dd):
    rb = RuleBase(f, card)
    n = 0
    for e in f.exceptions.values():
        mk = rb.emark(e)
        if mk is None or not eq(mk, unit):
            continue
        if rb.e_active(e, Dd):
            n += 1
    more = bool(_parts(f, ('exceptions', 'exceptions_to'), unit=unit))
    return {n}, more


def count_exclusions(f, unit, Dd):
    n = 0
    for x in f.exclusions.values():
        if not eq(x.unit, unit):
            continue
        st = f.stat.get(('Exclusion', x.eid)) or 'in force'
        if st != 'in force':
            continue
        if x.eff > Dd:
            continue
        if x.end[0] == 'through' and Dd > x.end[1]:
            continue
        if x.end[0] == 'repealed' and Dd >= x.end[1]:
            continue
        n += 1
    more = bool(_parts(f, ('exclusions',), unit=unit))
    return {n}, more


# ================================================================ S1 Q-R version of a rule
def rule_version(f, card, rule, unit, Dd):
    rb = RuleBase(f, card)
    vers = rb.rules.get(rule, [])
    v = rb.in_force(vers, unit, Dd)
    more = any(p.arg == rule for p in _parts(f, ('versions',), unit=unit))
    return {v.vid if v else NOANS}, more


# ================================================================ S3 log replay (sqlite, backward)
class Log:
    def __init__(self, f, unit):
        self.f = f
        segs = [l for l in f.logs if unit_ok(sec_unit(f, l.sec), unit)]
        self.all = {l.no: l for l in f.logs}
        self.entries = segs

    def void_set(self, end):
        """Entries voided by a VOID entry counted at time `end` (VOIDs act on any entry they name)."""
        v = set()
        for l in self.f.logs:
            if l.kind == 'void' and (l.ts, l.no) <= (end, 10 ** 12):
                v.add(l.target)
        return v


def s3_status(f, ent, unit, Dd):
    end = (Dd + 1) * DAY - 1
    lg = Log(f, unit)
    vs = lg.void_set(end)
    con = sqlite3.connect(':memory:')
    con.execute("create table s(ts int, no int, status text)")
    for l in f.logs:
        if l.kind == 'status' and l.ent == ent and l.no not in vs and l.ts <= end:
            con.execute("insert into s values(?,?,?)", (l.ts, l.no, l.status))
    r = con.execute("select status from s order by ts desc, no desc limit 1").fetchone()
    more = bool(_parts(f, ('log entries', 'entries'), unit=unit, ent=ent))
    return {r[0] if r else NOANS}, more


def s3_config(f, setting, unit, Dd):
    end = (Dd + 1) * DAY - 1
    lg = Log(f, unit)
    vs = lg.void_set(end)
    vers = {}
    for l in lg.entries:
        if l.kind == 'version' and eq(l.setting, setting):
            vers[l.vid] = l
    events = []  # (ts, no, vid)
    for vid, l in vers.items():
        if l.no in vs:
            continue
        if l.vstatus == 'in force' and l.ts <= end:
            events.append((l.ts, l.no, vid))
    for l in lg.entries:
        if l.no in vs or l.ts > end:
            continue
        if l.kind == 'applied' and l.vid in vers:
            v = vers[l.vid]
            if v.no in vs or v.vstatus != 'proposed':
                continue
            events.append((l.ts, l.no, l.vid))
        elif l.kind == 'rollback' and eq(l.setting, setting) and l.vid in vers:
            events.append((l.ts, l.no, l.vid))
    more = bool(_parts(f, ('log entries', 'entries'), unit=unit))
    if not events:
        return None, more
    ts, no, vid = max(events)
    return vers[vid], more


def s3_count(f, etype, status, unit, Dd):
    end = (Dd + 1) * DAY - 1
    lg = Log(f, unit)
    vs = lg.void_set(end)
    con = sqlite3.connect(':memory:')
    con.execute("create table s(no int, etype text, status text, ts int, unit text)")
    for l in f.logs:
        if l.kind == 'status':
            con.execute("insert into s values(?,?,?,?,?)", (l.no, C.norm(l.etype), C.norm(l.status), l.ts,
                                                           C.norm(sec_unit(f, l.sec) or '')))
    n = 0
    for (no,) in con.execute("select no from s where etype=? and status=? and ts<=? and unit=?",
                             (C.norm(etype), C.norm(status), end, C.norm(unit))):
        if no not in vs:
            n += 1
    more = bool(_parts(f, ('log entries', 'entries'), unit=unit))
    return {n}, more


# ================================================================ S4 tables (sqlite)
def col_match(header, name):
    nn = C.norm(name)
    best = None
    for j, h in enumerate(header):
        hn = C.norm(re.sub(r"\(.*?\)", "", h))
        hf = C.norm(h)
        if hn == nn or hf == nn:
            return j
        if (hf.startswith(nn) or nn.startswith(hn)) and best is None:
            best = j
    return best


def table_rows(f, name, unit, period):
    """All rows of table `name` for `unit` and `period`, over its parts. Returns (header, rows, parts, ok)."""
    name = name.upper()
    cands = [t for t in f.tables if t.name == name and unit_ok(sec_unit(f, t.sec), unit) and sec_unit(f, t.sec)]
    sel = []
    firsts = [t for t in cands if f.secs[t.sec].period == period]
    if not firsts:
        # first part missing (e.g. replaced by a part trace): keep the period-less continued parts of this unit
        pers_u = {f.secs[t.sec].period for t in cands if f.secs[t.sec].period is not None}
        firsts = [t for t in cands if t.continued and f.secs[t.sec].period is None and not pers_u]
        if not firsts:
            return None, [], [], False
    sel.extend(firsts)
    # continued parts without a stated period belong to the split table of the same unit
    pers = {f.secs[t.sec].period for t in cands if f.secs[t.sec].period is not None}
    for t in cands:
        if t in sel:
            continue
        if f.secs[t.sec].period is None and t.continued:
            if len(pers) == 1:
                sel.append(t)
            else:
                # ambiguous continued part: attach when no other split table of this unit exists
                others = [x for x in cands if x.part is not None and f.secs[x.sec].period not in (None, period)]
                if not others:
                    sel.append(t)
    header = sel[0].header
    rows = []
    for t in sel:
        hmap = [col_match(t.header, h) for h in header]
        for r in t.rows:
            rows.append([r[j] if j is not None and j < len(r) else '' for j in hmap])
    return header, rows, sel, True


def cell_val(x, marker):
    x = (x or '').strip()
    if marker and marker in x or re.match(r"^\[(not provided|illegible)", x):
        return TR
    p = C.parse_num(x)
    return p[0] if p else x


def s4_count(f, tname, unit, period, col, op, thr):
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found %s %s' % (tname, unit))
    j = col_match(header, col)
    if j is None:
        raise SolveError('column %s' % col)
    vals = [cell_val(r[j], f.marker) for r in rows]
    base = sum(1 for v in vals if v != TR and cmp_op(v, op, thr))
    ntr = sum(1 for v in vals if v == TR)
    ans = set(range(base, base + ntr + 1)) if ntr else {base}
    more = any(p.arg == tname.upper() for p in _parts(f, ('table',), unit=unit))
    return ans, more, rows, header


def s4_set(f, tname, unit, period, col, op, thr):
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found')
    j = col_match(header, col)
    vals = [(r[0], cell_val(r[j], f.marker)) for r in rows]
    fixed = frozenset(i for i, v in vals if v != TR and cmp_op(v, op, thr))
    tr = [i for i, v in vals if v == TR]
    ans = set()
    for k in range(len(tr) + 1):
        for sub in itertools.combinations(tr, k):
            ans.add(fixed | frozenset(sub))
    more = any(p.arg == tname.upper() for p in _parts(f, ('table',), unit=unit))
    return ans, more


def s4_total(f, tname, unit, period, measure):
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found')
    secs = {t.sec for t in parts}
    tots = {}
    for pt in f.ptotals:
        if pt.table == tname.upper() and pt.sec in secs and C.norm(pt.measure) == C.norm(measure):
            tots[pt.part] = pt.value
    more = any(p.arg == tname.upper() for p in _parts(f, ('table',), unit=unit))
    if not tots:
        # unsplit table: sum the rows
        j = col_match(header, measure)
        vals = [cell_val(r[j], f.marker) for r in rows]
        if any(v == TR for v in vals):
            return {'*'}, True
        return {sum(vals)}, more
    if any(v == TR for v in tots.values()):
        return {'*'}, True
    return {sum(C.parse_num(v)[0] for v in tots.values())}, more


def s4_argmax(f, tname, unit, period, col, hi=True):
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found')
    j = col_match(header, col)
    tie = f.card_tie
    tj = None
    if tie:
        tj = col_match(header, tie[1])
    recs = []
    for r in rows:
        v = cell_val(r[j], f.marker)
        key2 = r[tj] if tj is not None else r[0]
        if tj is not None:
            try:
                key2 = C.parse_date(key2)
            except Exception:
                key2 = r[tj]
        recs.append((r[0], v, key2))
    trs = [i for i, (rid, v, k2) in enumerate(recs) if v == TR]
    others = [v for rid, v, k2 in recs if v != TR]
    dims = [region_reps(set(others)) for _ in trs]
    ans = set()
    for combo in itertools.product(*dims) if dims else [()]:
        rr = list(recs)
        for i, x in zip(trs, combo):
            rr[i] = (rr[i][0], x, rr[i][2])
        best = max(x[1] for x in rr) if hi else min(x[1] for x in rr)
        tied = [x for x in rr if x[1] == best]
        if len(tied) > 1:
            if not tie:
                ans.add(CONFLICT)
                continue
            tied.sort(key=lambda x: x[2])
        ans.add(tied[0][0])
    more = any(p.arg == tname.upper() for p in _parts(f, ('table',), unit=unit))
    return ans, more


def s4_cmp(f, tname, unit, period, col, a, b, rel):
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found')
    j = col_match(header, col)
    va = vb = None
    for r in rows:
        if r[0] == a:
            va = cell_val(r[j], f.marker)
        if r[0] == b:
            vb = cell_val(r[j], f.marker)
    if va is None or vb is None:
        raise SolveError('cmp rows missing')
    hi = rel in ('higher', 'greater', 'more')
    if va == TR or vb == TR:
        return {True, False}, False
    return {(va > vb) if hi else (va < vb)}, False


def s4_crit(f, tname, unit, period, col, a, op, thr):
    """repair r6: criterion claim on one entity's cell ('<E> has <col> of <op> <thr>')."""
    header, rows, parts, ok = table_rows(f, tname, unit, period)
    if not ok:
        raise SolveError('table not found')
    j = col_match(header, col)
    va = None
    for r in rows:
        if r[0] == a:
            va = cell_val(r[j], f.marker)
    if va is None:
        raise SolveError('crit row missing')
    if va == TR:
        return {True, False}, False
    return {bool(cmp_op(va, op, thr))}, False


def s4_tp(f, card, ent, period, unit=None):
    rows = []
    for t in f.tables:
        s = f.secs[t.sec]
        per = s.period
        if per != period:
            continue
        for r in t.rows:
            if r and r[0] == ent:
                rows.append((t, r))
    if not rows:
        raise SolveError('tp row not found %s' % ent)
    t, r = rows[0]
    vals = {}
    crits = list(f.criteria.values())
    pts = {}
    from sb_solve import cond_points, eval_cond
    for c in crits:
        cond_points(c.cond, pts)
    for attr in pts:
        j = col_match(t.header, attr)
        if j is not None and j < len(r):
            vals[attr] = cell_val(r[j], f.marker)
    tv = [k for k, v in vals.items() if v == TR]
    dims = [region_reps(pts.get(k, set())) for k in tv]
    ans = set()
    for combo in itertools.product(*dims) if dims else [()]:
        vv = dict(vals)
        for k, x in zip(tv, combo):
            vv[k] = x
        app = []
        for c in crits:
            w = f.win.get(('Criterion', c.rid))
            miss = set()
            if eval_cond(c.cond, vv, miss):
                mk = f.marks.get(('Criterion', c.rid)) or f.secs[c.sec].unit
                app.append((c, mk, w[0] if w else 0, c.outcome))
        if not app:
            ans.add(card.default or NOANS)
            continue
        if card.prec == 'specific':
            spec = [a for a in app if a[1] is not None]
            grp = spec if spec else app
        elif card.prec == 'later':
            mx = max(a[2] for a in app)
            grp = [a for a in app if a[2] == mx]
        else:
            grp = app
        outs = {a[3] for a in grp}
        ans.add(outs.pop() if len(outs) == 1 else CONFLICT)
    return ans, False, len(rows)
