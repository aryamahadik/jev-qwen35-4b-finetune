"""Solver B (F13) core: dates, numbers, card lines, question, fact extraction.

Written from the frozen F13 G0 spec (F13.G0.v7, sections 2, 3, 4, 6, 11) and the observed row format only.
Shares no code with the generator (gen/ was never opened). Paradigm: declarative fact tables (sqlite in
sb_solve) + interval-partition reasoning over traces, backward version-graph walks.
"""
import re
import datetime
from fractions import Fraction

from sb_flat import flatten

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
          'november', 'december']
MON_RE = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
DATE_P = r"(?:\d{4}-\d\d-\d\d|\d{1,2} %s \d{4}|%s \d{1,2}, \d{4})" % (MON_RE, MON_RE)
TIME_P = r"(?:[T ]\d{1,2}:\d\d(?::\d\d)?Z?)"
TS_P = DATE_P + TIME_P
DATE_RE = re.compile(DATE_P)


def norm(s):
    return re.sub(r"[^a-z0-9%]+", " ", (s or '').lower()).strip()


def parse_date(s):
    s = s.strip().rstrip('.')
    m = re.match(r"^(\d{4})-(\d\d)-(\d\d)", s)
    if m:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).toordinal()
    m = re.match(r"^(\d{1,2}) (%s) (\d{4})" % MON_RE, s)
    if m:
        return datetime.date(int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1))).toordinal()
    m = re.match(r"^(%s) (\d{1,2}), (\d{4})" % MON_RE, s)
    if m:
        return datetime.date(int(m.group(3)), MONTHS.index(m.group(1).lower()) + 1, int(m.group(2))).toordinal()
    raise ValueError('bad date %r' % s)


def parse_ts(s):
    s = s.strip()
    m = re.match(r"^(%s)%s$" % (DATE_P, r"[T ](\d{1,2}):(\d\d)(?::(\d\d))?Z?"), s)
    if not m:
        raise ValueError('bad ts %r' % s)
    d = parse_date(m.group(1))
    return d * 1440 + int(m.group(2)) * 60 + int(m.group(3))


NUM_RE = re.compile(r"^(-?\d[\d,]*(?:\.\d+)?)\s*(.*)$")


def parse_num(s):
    """'1,234.5 kg' -> (Fraction, 'kg', decimals). None if not a number."""
    s = s.strip()
    m = NUM_RE.match(s)
    if not m:
        return None
    raw = m.group(1).replace(',', '')
    dec = len(raw.split('.')[1]) if '.' in raw else 0
    return Fraction(raw), m.group(2).strip(), dec


# ---------------------------------------------------------------- card
class Card:
    pass


def parse_card(text):
    c = Card()
    t = text
    c.closed = 'Treat the document as complete' in t
    c.open = 'is not given in this copy' in t
    m = re.search(r"shown as '(\[[^\]]+\])'", t)
    c.marker = m.group(1) if m else None
    m = re.search(r"'([^']+)' means the document settles the answer and none of the listed answers is correct", t)
    c.none_opt = m.group(1) if m else None
    m = re.search(r"'([^']+)' means the document does not settle the answer", t)
    c.nei_opt = m.group(1) if m else None
    m = re.search(r"If no rule gives an outcome for the case, the outcome is '([^']+)'", t)
    c.default = m.group(1) if m else None
    c.prec = None
    if re.search(r"A rule for a specific .+? overrides a rule with no .+? mark, whatever their dates", t):
        c.prec = 'specific'
    elif re.search(r"A rule with a later effective date overrides an earlier rule", t):
        c.prec = 'later'
    m = re.search(r"use the rules and versions in force on its (.+?), and read every record", t)
    c.gov_name = m.group(1).strip() if m else None
    m = re.search(r"marked for a (.+?) applies only to cases", t)
    c.scope_kind = m.group(1).strip() if m else None
    m = re.search(r"A motion carries if at least (\d+) members vote in favour", t)
    c.vote_k = int(m.group(1)) if m else None
    m = re.search(r"If two records tie on (.+?), choose the one with the (earlier|lower) (.+?)\.", t)
    c.tie = (m.group(2), m.group(3).strip()) if m else None
    m = re.search(r"The possible outcomes are (.+?)\.\s*(?:\n|$)", t)
    c.outcomes = _split_list(m.group(1)) if m else []
    m = re.search(r"The possible decision outcomes are (.+?)\.\s*(?:\n|$)", t)
    c.dec_outcomes = _split_list(m.group(1)) if m else []
    return c


def _split_list(s):
    s = s.strip()
    parts = re.split(r",\s+|\s+and\s+(?=[^,]*$)", s)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------- document facts
ID_P = r"[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9.\-]*[A-Z0-9]|[A-Z][A-Z0-9]*-[A-Z0-9]"
CMP_WORDS = [
    ('is at least', '>='), ('is no fewer than', '>='), ('is no less than', '>='),
    ('is at most', '<='), ('is no more than', '<='), ('is not exceeding', '<='), ('is up to', '<='),
    ('is more than', '>'), ('is over', '>'), ('is above', '>'), ('exceeds', '>'),
    ('is less than', '<'), ('is fewer than', '<'), ('is below', '<'), ('is under', '<'),
]
CMP_HAVE = [
    ('at least', '>='), ('no fewer than', '>='), ('no less than', '>='),
    ('at most', '<='), ('no more than', '<='), ('not exceeding', '<='), ('up to', '<='),
    ('more than', '>'), ('over', '>'), ('above', '>'),
    ('less than', '<'), ('fewer than', '<'), ('below', '<'), ('under', '<'),
]


def parse_atom(s):
    """'the guard gap is less than 66 mm' -> (attr, op, Fraction, unit)."""
    s = s.strip()
    s = re.sub(r"^the ", "", s)
    for w, op in CMP_WORDS:
        k = s.find(' ' + w + ' ')
        if k > 0:
            attr = s[:k].strip()
            num = parse_num(s[k + len(w) + 2:])
            if num is None:
                return None
            return (attr, op, num[0], num[1])
    return None


def parse_cond(s):
    """Condition tree: ('atom', attr, op, val, unit) | ('or', [..]) | ('and', [..])."""
    s = s.strip()
    m = re.match(r"^either (.+), but not both$", s)
    if m:
        a = re.split(r"\s+or\s+(?=the )", m.group(1))
        return ('xor', [parse_cond(x) for x in a])
    parts = re.split(r"\s+or\s+(?=the )", s)
    if len(parts) > 1:
        return ('or', [parse_cond(x) for x in parts])
    parts = re.split(r"\s+and\s+(?=the )", s)
    if len(parts) > 1:
        return ('and', [parse_cond(x) for x in parts])
    a = parse_atom(s)
    if a is None:
        return ('bad', s)
    return ('atom',) + a


def cond_attrs(c):
    if c[0] == 'atom':
        return {c[1]}
    if c[0] in ('or', 'and', 'xor'):
        out = set()
        for x in c[1]:
            out |= cond_attrs(x)
        return out
    return set()


class Doc:
    pass


R_RULE = re.compile(r"^Rule (\S+), version (\S+): if (.+), the outcome for the (.+?) is (.+)\.$")
R_AMEND = re.compile(r"^Amendment to rule (\S+): version (\S+) amends version (\S+); under version \S+, if (.+), "
                     r"the outcome for the (.+?) is (.+)\.$")
R_CRIT = re.compile(r"^Criterion (\S+): an? (.+?) is (.+?) if (.+)\.$")
R_VSTAT = re.compile(r"^(Version|Exception|Exclusion|Criterion) (\S+) status: (in force|draft|proposed|void)\.$")
R_VWIN = re.compile(r"^(Version|Exception|Exclusion|Criterion) (\S+): (?:effective (%s); )?(no end date|valid through (%s)|"
                    r"repealed with effect from (%s))\.$" % (DATE_P, DATE_P, DATE_P))
R_VREG = re.compile(r"^Version (\S+) of rule (\S+): effective (%s)\.$" % DATE_P)
R_VMARK = re.compile(r"^(Version|Exception|Hold|Condition|Exclusion|Criterion|Action item|Record) (\S+) is marked for (.+)\.$")
R_EXC = re.compile(r"^Exception (\S+) to (rule|exception) (\S+) covers every (.+?) whose (.+)\.$")
R_EXCL = re.compile(r"^Exclusion (\S+) for (.+?) (%s) is marked for (.+?); effective (%s); (no end date|valid through (%s)|"
                    r"repealed with effect from (%s))\.$" % (ID_P, DATE_P, DATE_P, DATE_P))
R_CORR_VOID = re.compile(r"^Correction: (\S+) is void\.$")
R_PART = re.compile(r"^(.+?) \((.+)\): not included in this copy\.$")
R_HOLD = re.compile(r"^(Hold|Condition) (\S+) on (.+?) (%s): (.+)\.$" % ID_P)
R_DECN = re.compile(r"^Decision notice on (.+?) (%s), dated (%s): the outcome is (.+)\.$" % (ID_P, DATE_P))
R_REVN = re.compile(r"^(Revision|Reversal) notice on (.+?) (%s), dated (%s): the decision is (revised|reversed); "
                    r"the outcome is (.+)\.$" % (ID_P, DATE_P))
R_NCORR_VOID = re.compile(r"^Correction to the (decision|revision|reversal) notice on (.+?) (%s) dated (%s): "
                          r"the notice is void\.$" % (ID_P, DATE_P))
R_NCORR_OUT = re.compile(r"^Correction to the (decision|revision|reversal) notice on (.+?) (%s) dated (%s): "
                         r"the outcome is (.+), not (.+)\.$" % (ID_P, DATE_P))
R_MOTION = re.compile(r"^Motion to (make|revise|reverse) the decision on (.+?) (%s) so that \2 \3 is (.+): "
                      r"in favour (\d+), against (\d+), abstain (\d+)\.$" % ID_P)
R_MCORR_VOID = re.compile(r"^Correction to the minutes of (%s): the (decision|revision|reversal) on (.+?) (%s) made at "
                          r"the meeting of (%s) is void\.$" % (DATE_P, ID_P, DATE_P))
R_MCORR_OUT = re.compile(r"^Correction to the minutes of (%s): in the motion to (make|revise|reverse) the decision on "
                         r"(.+?) (%s), the outcome is (.+), not (.+)\.$" % (DATE_P, ID_P))
R_PROPOSAL = re.compile(r"^Proposal to revise the decision on (.+?) (%s) so that .+ is (.+)\.$" % ID_P)
R_ACTION = re.compile(r"^Action item (\S+): (.+)\.$")
R_MEETING = re.compile(r"^Meeting date: (%s)\.$" % DATE_P)
R_STATUS_LINE = re.compile(r"^Status: (in force|draft|proposed|void)\.$")
R_PERIOD = re.compile(r"^Reporting period: (%s) through (%s)\.$" % (DATE_P, DATE_P))
R_PTOTAL = re.compile(r"^Part total for part (\d+) of table (\S+) \((.+?)\): (.+)\.$")
R_LOG = re.compile(r"^(%s) \| (\d+) \| (.+?) \| (.+)$" % TS_P)
ATTACK = re.compile(r"^(Message for the reader|Instruction from the records desk|Note to whoever reads|Reminder for the "
                    r"reader|Desk instruction)")


def doc_sections(state):
    return flatten(state)


def records_of(sec):
    """Yield (caption, [(field, value)]) for record-like elements of a section."""
    els = sec.els
    i = 0
    out = []
    while i < len(els):
        e = els[i]
        if e[0] == 'T':
            cap, header, rows = e[1], e[2], e[3]
            if header and len(header) == 2 and all(len(r) == 2 for r in rows) and \
                    (cap and re.search(r"record", cap, re.I) or norm(header[0]) in ('field', 'attribute', 'item', 'key',
                                                                                   'name', 'property')):
                if norm(header[0]) in ('field', 'attribute', 'item', 'key', 'name', 'property'):
                    out.append((cap, [(r[0], r[1]) for r in rows]))
                else:
                    out.append((cap, [(header[0], header[1])] + [(r[0], r[1]) for r in rows]))
        elif e[0] == 'C' and re.search(r"record", e[1], re.I):
            pairs = []
            j = i + 1
            while j < len(els) and els[j][0] == 'K':
                pairs.append((els[j][1], els[j][2]))
                j += 1
            if pairs:
                out.append((e[1], pairs))
                i = j
                continue
        i += 1
    # bare K groups with no caption (struct dict under a record key handled above)
    return out


def record_id(caption):
    """Extract the record ID from a caption like 'Machine record MC-7V07' or 'small_claim_record_scm_6awq'."""
    if not caption:
        return None
    m = re.search(r"record (%s)$" % ID_P, caption.strip())
    if m:
        return m.group(1)
    n = norm(caption)
    m = re.search(r"record ([a-z0-9]+) ([a-z0-9 ]+)$", n)
    if m:
        return (m.group(1) + '-' + m.group(2).replace(' ', '-')).upper()
    return None
