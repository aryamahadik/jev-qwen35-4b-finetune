"""Solver B (F13): fact tables from the flattened document (text side only).

Every fact is read from rendered text; section-level marks (scope unit, status, meeting date, period) are read
from mark lines in the section body (G0 2.1, A22). Written from the G0 spec; no generator code consulted.
"""
import re
from fractions import Fraction

import sb_core as C

TR = 'TRACE'
TI_LABELS = {'contact list', 'staff directory', 'telephone and e mail list'}


class Item(dict):
    __getattr__ = dict.get
    __hash__ = object.__hash__

    def __eq__(self, other):
        return self is other


class Facts:
    pass


def _end(kind_txt, d1, d2):
    if kind_txt == 'no end date':
        return ('none', None)
    if kind_txt.startswith('valid through'):
        return ('through', C.parse_date(d1))
    return ('repealed', C.parse_date(d2))


def _val(raw, marker):
    raw = (raw or '').strip().strip('"')
    if marker and marker in raw or re.match(r"^\[(not provided|illegible)", raw):
        return TR
    return raw


def extract(secs, card, row_marker=None):
    f = Facts()
    f.secs = secs
    marker = card.marker or row_marker
    f.marker = marker
    sk = C.norm(card.scope_kind) if card.scope_kind else None
    f.versions = {}
    f.stat = {}
    f.win = {}
    f.reg = {}
    f.marks = {}
    f.voided = set()
    f.exceptions = {}
    f.parts = []
    f.records = {}
    f.records_list = []
    f.holds = []
    f.notices = []
    f.ncorr = []
    f.motions = []
    f.mcorr = []
    f.proposals = []
    f.actions = []
    f.logs = []
    f.criteria = {}
    f.exclusions = {}
    f.tables = []
    f.ptotals = []
    f.units = set()
    f.unparsed = []
    for si, s in enumerate(secs):
        s.unit = None
        s.status = None
        s.meeting = None
        s.period = None
        # section-level marks first
        for e in s.els:
            if e[0] != 'L':
                continue
            t = e[1]
            m = re.match(r"^([A-Z][^:]{0,60}): (.+)\.$", t)
            if m and sk and C.norm(m.group(1)) == sk:
                s.unit = m.group(2).strip()
                f.units.add(s.unit)
                continue
            m = C.R_STATUS_LINE.match(t)
            if m:
                s.status = m.group(1)
                continue
            m = C.R_MEETING.match(t)
            if m:
                s.meeting = C.parse_date(m.group(1))
                continue
            m = C.R_PERIOD.match(t)
            if m:
                s.period = (C.parse_date(m.group(1)), C.parse_date(m.group(2)))
        for ei, e in enumerate(s.els):
            if e[0] == 'L':
                _line(f, card, s, si, e[1], marker)
            elif e[0] == 'T':
                cap = e[1] or ''
                n = C.norm(cap)
                if re.search(r"\btable\b", n) and not re.search(r"\brecord\b", n):
                    m = re.match(r"^(?:part (\d+) of )?table ([a-z0-9]+)(?: continued)?$", n)
                    if m:
                        f.tables.append(Item(name=m.group(2).upper(), part=int(m.group(1)) if m.group(1) else None,
                                             continued='continued' in n, sec=si, header=e[2], rows=e[3]))
                        continue
                    f.unparsed.append(('table-cap', cap))
        for cap, pairs in C.records_of(s):
            rid = C.record_id(cap)
            if rid is None:
                f.unparsed.append(('record-cap', cap))
                continue
            fields = {}
            for k, v in pairs:
                fields[C.norm(k)] = _val(v, marker)
            it = Item(id=rid, caption=cap, fields=fields, sec=si)
            f.records_list.append(it)
            f.records.setdefault(rid.upper(), []).append(it)
    return f


def _line(f, card, s, si, t, marker):
    if C.ATTACK.match(t):
        return
    m = C.R_RULE.match(t)
    if m:
        f.versions[m.group(2)] = Item(vid=m.group(2), rule=m.group(1), cond=C.parse_cond(m.group(3)),
                                      entity=m.group(4), outcome=m.group(5), sec=si, amends=None, raw=t)
        return
    m = C.R_AMEND.match(t)
    if m:
        f.versions[m.group(2)] = Item(vid=m.group(2), rule=m.group(1), cond=C.parse_cond(m.group(4)),
                                      entity=m.group(5), outcome=m.group(6), sec=si, amends=m.group(3), raw=t)
        return
    m = C.R_CRIT.match(t)
    if m:
        f.criteria[m.group(1)] = Item(rid=m.group(1), entity=m.group(2), outcome=m.group(3),
                                      cond=C.parse_cond(m.group(4)), sec=si)
        return
    m = C.R_VSTAT.match(t)
    if m:
        f.stat[(m.group(1), m.group(2))] = m.group(3)
        return
    m = C.R_VWIN.match(t)
    if m:
        eff = C.parse_date(m.group(3)) if m.group(3) else None
        f.win[(m.group(1), m.group(2))] = (eff,) + _end(m.group(4), m.group(5), m.group(6))
        return
    m = C.R_VREG.match(t)
    if m:
        f.reg[m.group(1)] = (C.parse_date(m.group(3)), m.group(2), si)
        return
    m = C.R_VMARK.match(t)
    if m:
        f.marks[(m.group(1), m.group(2))] = m.group(3).strip()
        f.units.add(m.group(3).strip())
        return
    m = C.R_EXC.match(t)
    if m:
        f.exceptions[m.group(1)] = Item(eid=m.group(1), tkind=m.group(2), target=m.group(3), entity=m.group(4),
                                        cond=C.parse_cond(m.group(5)), sec=si)
        return
    m = C.R_EXCL.match(t)
    if m:
        eff = C.parse_date(m.group(5))
        f.exclusions[m.group(1)] = Item(eid=m.group(1), etype=m.group(2), ent=m.group(3), unit=m.group(4).strip(),
                                        eff=eff, end=_end(m.group(6), m.group(7), m.group(8)), sec=si)
        f.units.add(m.group(4).strip())
        return
    m = C.R_CORR_VOID.match(t)
    if m:
        f.voided.add(m.group(1))
        return
    m = C.R_PART.match(t)
    if m:
        f.parts.append(_part(m.group(1), m.group(2), card, si))
        return
    m = C.R_HOLD.match(t)
    if m:
        ev = {}
        for seg in m.group(5).split('; '):
            mm = re.match(r"^(placed|released|imposed|met|waived) on (%s)$" % C.DATE_P, seg.strip())
            if mm:
                ev[mm.group(1)] = C.parse_date(mm.group(2))
            else:
                f.unparsed.append(('hold-ev', seg))
        f.holds.append(Item(kind=m.group(1), hid=m.group(2), etype=m.group(3), ent=m.group(4), ev=ev, sec=si))
        return
    m = C.R_DECN.match(t)
    if m:
        f.notices.append(Item(kind='decision', etype=m.group(1), ent=m.group(2), date=C.parse_date(m.group(3)),
                              outcome=m.group(4), sec=si))
        return
    m = C.R_REVN.match(t)
    if m:
        f.notices.append(Item(kind=m.group(1).lower(), etype=m.group(2), ent=m.group(3),
                              date=C.parse_date(m.group(4)), outcome=m.group(6), sec=si))
        return
    m = C.R_NCORR_VOID.match(t)
    if m:
        f.ncorr.append(Item(kind=m.group(1), ent=m.group(3), date=C.parse_date(m.group(4)), void=True, sec=si))
        return
    m = C.R_NCORR_OUT.match(t)
    if m:
        f.ncorr.append(Item(kind=m.group(1), ent=m.group(3), date=C.parse_date(m.group(4)), void=False,
                            new=m.group(5), old=m.group(6), sec=si))
        return
    m = C.R_MOTION.match(t)
    if m:
        f.motions.append(Item(kind=m.group(1), etype=m.group(2), ent=m.group(3), outcome=m.group(4),
                              yes=int(m.group(5)), no=int(m.group(6)), abst=int(m.group(7)), sec=si))
        return
    m = C.R_MCORR_VOID.match(t)
    if m:
        f.mcorr.append(Item(mdate=C.parse_date(m.group(1)), kind=m.group(2), ent=m.group(4),
                            date=C.parse_date(m.group(5)), void=True, sec=si))
        return
    m = C.R_MCORR_OUT.match(t)
    if m:
        f.mcorr.append(Item(mdate=C.parse_date(m.group(1)), mkind=m.group(2), ent=m.group(4), void=False,
                            new=m.group(5), old=m.group(6), sec=si))
        return
    m = C.R_PROPOSAL.match(t)
    if m:
        f.proposals.append(Item(ent=m.group(2), outcome=m.group(3), sec=si))
        return
    m = C.R_ACTION.match(t)
    if m:
        evs = []
        for seg in m.group(2).split('; '):
            seg = seg.strip()
            mm = re.match(r"^(assigned|transferred) to (.+) on (%s)$" % C.DATE_P, seg)
            if mm:
                evs.append((mm.group(1), mm.group(2).strip(), C.parse_date(mm.group(3))))
                continue
            mm = re.match(r"^(closed|reopened) on (%s)$" % C.DATE_P, seg)
            if mm:
                evs.append((mm.group(1), None, C.parse_date(mm.group(2))))
                continue
            f.unparsed.append(('action-ev', seg))
        f.actions.append(Item(aid=m.group(1), evs=evs, sec=si))
        return
    m = C.R_PTOTAL.match(t)
    if m:
        f.ptotals.append(Item(part=int(m.group(1)), table=m.group(2).upper(), measure=m.group(3),
                              value=_val(m.group(4), marker), sec=si))
        return
    m = C.R_LOG.match(t)
    if m:
        f.logs.append(_log(m, si))
        return


def _log(m, si):
    ts = C.parse_ts(m.group(1))
    no = int(m.group(2))
    txt = m.group(4).strip()
    it = Item(ts=ts, no=no, actor=m.group(3), text=txt, sec=si, kind='other')
    mm = re.match(r"^Status of (.+?) (%s) set to (.+)\.$" % C.ID_P, txt)
    if mm:
        it.update(kind='status', etype=mm.group(1), ent=mm.group(2), status=mm.group(3))
        return it
    mm = re.match(r"^Version (\S+) of the (.+?) setting recorded; status (in force|proposed|draft|void); value (.+)\.$",
                  txt)
    if mm:
        it.update(kind='version', vid=mm.group(1), setting=mm.group(2), vstatus=mm.group(3), value=mm.group(4))
        return it
    mm = re.match(r"^(\S+) applied\.$", txt)
    if mm:
        it.update(kind='applied', vid=mm.group(1))
        return it
    mm = re.match(r"^(.+?) setting rolled back to (\S+)\.$", txt)
    if mm:
        it.update(kind='rollback', setting=mm.group(1), vid=mm.group(2))
        return it
    mm = re.match(r"^VOID entry (\d+)\.$", txt)
    if mm:
        it.update(kind='void', target=int(mm.group(1)))
        return it
    mm = re.match(r"^(Comment added to the record of|Record of) ", txt)
    if mm:
        it.update(kind='noop')
        return it
    it.update(kind='unknown')
    return it


def _part(label, scope, card, si):
    nl = C.norm(label)
    sk = C.norm(card.scope_kind) if card.scope_kind else None
    ns = C.norm(scope)
    unit = None
    ent = None
    m = re.match(r"^(.+?) (%s)$" % C.ID_P, scope.strip())
    if m:
        ent = m.group(2)
    elif sk and ns.startswith(sk + ' '):
        unit = scope.strip()[len(card.scope_kind) + 1:].strip()
    else:
        unit = scope.strip()
    if nl in TI_LABELS:
        ptype, arg = 'ti', None
    else:
        m = re.match(r"^versions of rule (\S+)$", label.strip().lower())
        if m:
            ptype, arg = 'versions', label.strip().split()[-1]
        elif re.match(r"^exceptions to rule (\S+)$", label.strip().lower()):
            ptype, arg = 'exceptions_to', label.strip().split()[-1]
        elif re.match(r"^exceptions to exception (\S+)$", label.strip().lower()):
            ptype, arg = 'exceptions_to_exc', label.strip().split()[-1]
        elif nl == 'exceptions':
            ptype, arg = 'exceptions', None
        elif nl in ('holds', 'conditions', 'log entries', 'action items', 'motions', 'exclusions',
                    'decision notices', 'criteria', 'amendments', 'rules', 'records', 'entries'):
            ptype, arg = nl, None
        elif re.match(r"^table [a-z0-9]+$", nl):
            ptype, arg = 'table', nl.split()[-1].upper()
        elif re.match(r"^part \d+ of table [a-z0-9]+$", nl):
            # one part of a split table missing: covers that table's rows for the scope (SEM-38, A04)
            ptype, arg = 'table', nl.split()[-1].upper()
        else:
            ptype, arg = 'other', label
    return Item(ptype=ptype, arg=arg, unit=unit, ent=ent, label=label, scope=scope, sec=si)
