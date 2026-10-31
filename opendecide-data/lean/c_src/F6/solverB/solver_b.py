#!/usr/bin/env python3
"""F6 independent solver B (written from G0_SPEC rev8 + row format only; never reads gen/ or solver A).

Paradigm: model enumeration / witness search over the PARSED TEXT of each row.  Every row's rendered
state (record), card (switch sentences, policy) and question are parsed back into facts, variables with
finite domains, rules and a claim; then the possible-outcome set P (or truth set T) is computed by
enumerating representative completions (one value per region cut by every threshold that appears), or by
constructing extremal witness completions where the model space factorises (tables, sums, dates).
Gold is re-derived from P / T with the section 1 form table and compared with the row's gold.
Output: mismatch ids + both answers + the spec item; never row text.
"""
import json, re, sys, os, itertools, datetime, collections, traceback

MONTHS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july',
                                            'august', 'september', 'october', 'november', 'december'])}
MON_RE = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
DATE_RE = r'(?:\d{4}-\d\d-\d\d|\d{1,2} ' + MON_RE + r' \d{4})'
INF = 10 ** 12


class ParseError(Exception):
    pass


def to_day(s):
    """Exact date string -> ordinal day number."""
    s = s.strip().rstrip('.')
    m = re.fullmatch(r'(\d{4})-(\d\d)-(\d\d)', s)
    if m:
        return datetime.date(int(m[1]), int(m[2]), int(m[3])).toordinal()
    m = re.fullmatch(r'(\d{1,2}) (' + MON_RE + r') (\d{4})', s)
    if m:
        return datetime.date(int(m[3]), MONTHS[m[2].lower()], int(m[1])).toordinal()
    raise ParseError('bad date %r' % s)


def month_dom(mon, year):
    y, mo = int(year), MONTHS[mon.lower()]
    a = datetime.date(y, mo, 1)
    b = datetime.date(y + (mo == 12), mo % 12 + 1, 1)
    return a.toordinal(), b.toordinal() - 1


def date_dom(v):
    """Event / notice date phrase -> (lo, hi) day domain, or None if not a date phrase."""
    v = v.strip().rstrip('.').strip()
    m = re.fullmatch(r'(?:on )?(?:one day )?from (' + DATE_RE + r') to (' + DATE_RE + r')', v)
    if m:
        return to_day(m[1]), to_day(m[2])
    m = re.fullmatch(r'(?:on )?(?:one day )?in (' + MON_RE + r') (\d{4})(?: \(\d+ days\))?', v)
    if m:
        return month_dom(m[1], m[2])
    m = re.fullmatch(r'(?:on )?(' + DATE_RE + r')', v)
    if m:
        d = to_day(m[1])
        return d, d
    return None


BULLET_RE = re.compile(r'^(?:>\s*)*(?:[-*•+·]\s+|\d+[.)]\s+(?!In )|\(\d+\)\s+(?!In )|[a-z][.)]\s+)?')


def clean(l):
    """Strip quote marks, bullets, markdown emphasis/heading marks and HTML tags from one line."""
    l = re.sub(r'<[^>]+>', ' ', l)
    l = l.strip()
    l = re.sub(r'^(?:>\s*)+', '', l)
    l = re.sub(r'^#+\s*', '', l)
    l = BULLET_RE.sub('', l, count=1)
    l = l.replace('**', '').replace('__', '')
    return re.sub(r'\s+', ' ', l).strip()


def low(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


# ----------------------------------------------------------------------------------------------
# B. Record (state) parsing: every container -> key/value pairs (+ section) and data tables
# ----------------------------------------------------------------------------------------------
class Table:
    def __init__(self, header, rows, caption=''):
        self.header = [h.strip() for h in header]
        self.rows = [[c.strip() for c in r] for r in rows]
        self.caption = caption


def _html_to_text(st, tables):
    def tab(m):
        body = m.group(0)
        trs = re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S)
        cells = [re.findall(r'<t([hd])[^>]*>(.*?)</t[hd]>', tr, re.S) for tr in trs]
        if not cells:
            return '\n'
        if '<thead' in body or (len(cells[0]) >= 3 and all(k == 'h' for k, _ in cells[0])):
            hdr = [re.sub(r'<[^>]+>', '', v) for _, v in cells[0]]
            rows = [[re.sub(r'<[^>]+>', '', v) for _, v in c] for c in cells[1:]]
            tables.append(Table(hdr, rows))
            return '\n'
        out = []
        for c in cells:
            vals = [re.sub(r'<[^>]+>', '', v).strip() for _, v in c]
            if len(vals) == 2:
                out.append('%s: %s' % (vals[0], vals[1]))
        return '\n' + '\n'.join(out) + '\n'
    st = re.sub(r'<table[^>]*>.*?</table>', tab, st, flags=re.S)
    st = re.sub(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', lambda m: '\n%s: %s\n' % (m[1].strip(), m[2].strip()), st, flags=re.S)
    st = re.sub(r'<h\d[^>]*>(.*?)</h\d>', lambda m: '\n## %s\n' % m[1].strip(), st, flags=re.S)
    st = re.sub(r'</?(p|div|section|li|ul|ol|br|dl|article|header|footer)[^>]*>', '\n', st)
    st = re.sub(r'<[^>]+>', '', st)
    return st


def _split_cells(line, delim):
    if delim == 'fw':
        return re.split(r'\s{2,}', line.strip())
    if delim == '|':
        t = line.strip()
        if t.startswith('|'):
            t = t[1:-1] if t.endswith('|') else t[1:]
        return t.split('|')
    return line.strip(' \r\n').split(delim)


def _fw_cells(line, starts):
    out = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else None
        out.append(line[s:e].strip() if s < len(line) else '')
    return out


ID_CELL = re.compile(r'^[A-Z]{1,5}-\d{2,6}$')


def _try_table(lines, i):
    """Detect a delimited / fixed-width data table whose first header cell ends with 'ID'. Returns (Table, next_i)."""
    raw = lines[i].rstrip()
    line = raw.strip()
    for delim in ('\t', ';', ',', '|', 'fw'):
        cells = _split_cells(line, delim)
        if len(cells) < 3 or not cells[0].strip().endswith('ID'):
            continue
        starts = None
        if delim == 'fw':
            ind = len(raw) - len(raw.lstrip())
            starts = [m.start() for m in re.finditer(r'(?:(?<=\s{2})|^)\S', raw[ind:])]
            starts = [s + ind for s in starts]
            if len(starts) != len(cells):
                continue
        rows, j = [], i + 1
        while j < len(lines):
            r = lines[j].rstrip(' \r\n') if delim != 'fw' else lines[j].rstrip()
            if not r.strip() or re.fullmatch(r'[\s=\-|:+]+', r):
                if rows and not r.strip():
                    break
                j += 1
                continue
            rc = _fw_cells(r, starts) if delim == 'fw' else _split_cells(r, delim)
            if len(rc) != len(cells) or not ID_CELL.match(rc[0].strip()):
                break
            rows.append(rc)
            j += 1
        if rows:
            return Table(cells, rows), j
    return None, i


def _kv(sent):
    s = sent.strip()
    m = re.match(r'^(.+?)\s*\.{2,}\s+(\S.*)$', s)
    if not m:
        m = re.match(r'^([^:]+?)\s*:\s*(.*)$', s)
    if not m:
        return None
    k, v = m.group(1).strip(), m.group(2).strip()
    v = re.sub(r'\.$', '', v).strip()
    m2 = re.fullmatch(r'\[\s*(.*?)\s*\]', v)
    if m2:
        v = m2.group(1)
    return k, v


def parse_transcript(st):
    """S5 interview: 'What is the <attr> of <ID>?' / 'Did <ID> have a "<ev>" event?' + the next answer line."""
    pairs, pend = [], None
    for raw in st.split('\n'):
        l = raw.strip()
        if not l:
            continue
        if l.count('|') >= 2:
            l = l.split('|')[-1].strip()
        m = re.search(r'What is the (.+?) of (\S+?)\?', l)
        if m:
            pend = (m[1], m[2], 'attr')
            continue
        m = re.search(r'Did (\S+) have an? "(.+?)" event\?', l)
        if m:
            pend = (m[2], m[1], 'event')
            continue
        if pend is None or not l.endswith('.') or re.match(r'(Sender|Subject|From|Sent|Message|Dear|Regards|Good morning|With thanks)', l):
            continue
        a = l[:-1].strip()
        if pend[2] == 'event':
            ma = re.fullmatch(r'Yes, on (.+)', a)
            if ma:
                a = ma.group(1)
            elif re.fullmatch(r'No', a):
                a = '__NO__'
            pairs.append(('%s for %s' % (pend[0], pend[1]), a, None))
        else:
            pairs.append((pend[0], a, None))
        pend = None
    return pairs


def parse_state(st, case_labels=()):
    tables = []
    st = '\n'.join(l for l in st.split('\n') if not l.strip().startswith('```'))
    s2 = st.strip()
    k = s2.find('[')
    if k >= 0 and re.match(r'\s*\{', s2[k + 1:]):
        try:
            arr = json.loads(s2[k:s2.rfind(']') + 1])
            hdr = list(arr[0].keys())
            tables.append(Table(hdr, [['' if e[h] is None else str(e[h]) for h in hdr] for e in arr]))
            tables[-1].nulls = [[e[h] is None for h in hdr] for e in arr]
            st = s2[:k] + s2[s2.rfind(']') + 1:]
        except Exception:
            pass
    if re.search(r'</?(table|tr|td|th|p|h\d|dl|dt|dd|div|section|li)\b', st):
        st = _html_to_text(st, tables)
    caselow = {low(c): c for c in case_labels}
    lines = st.split('\n')
    pairs, section, i = [], None, 0
    while i < len(lines):
        t, j = _try_table(lines, i)
        if t:
            tables.append(t)
            i = j
            continue
        line = lines[i]
        i += 1
        c = clean(line)
        if not c or re.fullmatch(r'[=\-^~*#_ ]+', c):
            continue
        hl = low(re.sub(r'[:.]$', '', c))
        if hl in caselow:
            section = caselow[hl]
            continue
        if line.strip().startswith('|'):
            cells = [x.strip() for x in line.strip().strip('|').split('|')]
            if len(cells) == 2 and not re.fullmatch(r'[-: ]+', cells[0]):
                pairs.append((cells[0], cells[1], section))
            continue
        sents = re.split(r'(?<=\.)\s+(?=[A-Z\[])', c) if c.count(': ') >= 2 and '..' not in c else [c]
        for s in sents:
            kv = _kv(s)
            if kv:
                pairs.append((kv[0], kv[1], section))
    return pairs, tables


# ----------------------------------------------------------------------------------------------
# C. Card parsing (switch sentences, domains, policy) from instructions + card field
# ----------------------------------------------------------------------------------------------
class Rule:
    def __init__(self, num, notice, outcome, conds, unless=None, exc_of=None, cell=None, kind='rule'):
        self.num, self.notice, self.outcome, self.conds = num, notice, outcome, conds
        self.unless, self.exc_of, self.cell, self.kind = unless, exc_of, cell, kind

    def __repr__(self):
        return 'R(%s,%s,%s,%s,unless=%s,exc=%s,cell=%s)' % (self.num, self.notice, self.outcome, self.conds,
                                                              self.unless, self.exc_of, self.cell)


class Card:
    def __init__(self):
        self.D = None
        self.world = None              # 'open' | 'closed' | 'local'
        self.closed_events = set()     # event names (lower) that close
        self.closed_all_lists = False
        self.local_list = None         # list heading (lower)
        self.local_event = None
        self.markers = set()
        self.blank = False
        self.null_unknown = False
        self.tag = None                # evidence tag (lower)
        self.tag_counts = None
        self.plan_words = ('scheduled', 'planned', 'expected', 'requested')
        self.num_dom = {}              # attr -> (lo, hi, smallest unit)
        self.cat_dom = {}              # attr -> (values, other_possible)
        self.ev_day_dom = {}           # (event, entity) -> (lo, hi)
        self.rounding = {}             # quantity -> (mark, R, unit)
        self.default_unit = {}         # quantity -> unit
        self.ambiguous = {}            # quantity -> (U, V)
        self.conv = {}                 # unit -> (factor, base unit)
        self.notices = {}              # notice name -> (lo, hi)
        self.rules = []
        self.onlyif = []               # (outcome, conds)
        self.otables = []              # (num, notice, A, B, {(a, b): outcome})
        self.default = None
        self.test_exception = False
        self.test_subclass = False
        self.test_date = False
        self.nei_opt = set()
        self.none_opt = set()
        self.nothing_opt = set()
        self.tie = None                # (key, mode)
        self.once_types = set()
        self.noshare_types = set()
        self.unknown_lines = []
        self.subclass = []             # (B, A)


def _quoted(s):
    return [low(x) for x in re.findall(r'"([^"]+)"', s)]


def _cat_values(s):
    s = s.strip().rstrip('.')
    other = False
    if s.endswith(', or another value') or s.endswith(' or another value'):
        other = True
        s = re.sub(r',? or another value$', '', s)
    parts = re.split(r', or |, | or ', s)
    return [low(p) for p in parts if p.strip()], other


CMP_OPS = {'at least': '>=', 'no fewer than': '>=', 'no less than': '>=', 'at most': '<=', 'no more than': '<=',
           'more than': '>', 'above': '>', 'exceeds': '>', 'fewer than': '<', 'less than': '<', 'below': '<'}
CMP_RE = r'(at least|at most|no fewer than|no less than|no more than|more than|above|exceeds|fewer than|less than|below)'


def parse_atom(a):
    a = a.strip().rstrip('.').strip()
    m = re.fullmatch(r'the (.+?) (?:is )?' + CMP_RE + r' (-?\d+(?:\.\d+)?)(?: (.+))?', a)
    if m:
        return ('cmp', low(m[1]), CMP_OPS[m[2]], m[3], (m[4] or '').strip())
    m = re.fullmatch(r'the (.+?) had an? "(.+?)" event', a)
    if m:
        return ('ev', low(m[1]), low(m[2]), True)
    m = re.fullmatch(r'the (.+?) did not have an? "(.+?)" event', a)
    if m:
        return ('ev', low(m[1]), low(m[2]), False)
    m = re.fullmatch(r'the (.+?) is (.+)', a)
    if m:
        return ('is', low(m[1]), m[2].strip())
    raise ParseError('atom %r' % a)


def parse_conds(s):
    s = s.strip().rstrip('.')
    unless = None
    m = re.search(r', unless (the .+)$', s)
    if m:
        unless = parse_atom(m[1])
        s = s[:m.start()]
    if re.search(r'\bor\b|\beither\b', s):
        raise ParseError('disjunction in rule %r' % s)
    return [parse_atom(p) for p in re.split(r' and (?=the )', s)], unless


RULE_RE = re.compile(r'^(?:Rule (\d+):|R(\d+)\.|(\d+)\.|\((\d+)\))?\s*In (the base policy|Notice [A-Z]), the outcome is "(.+?)" (if|exactly when) (.+)$')
EXC_RE = re.compile(r'^Exception to rule (\d+)(?:, cell (.+?) / (.+?))?: In (the base policy|Notice [A-Z]), the outcome is "(.+?)" if (.+)$')
OTAB_RE = re.compile(r'^(?:Rule (\d+):|R(\d+)\.|(\d+)\.|\((\d+)\))?\s*In (the base policy|Notice [A-Z]), the outcome table below gives the outcome by the (.+?) \(rows\) and the (.+?) \(columns\)\.?$')


def _parse_otable(lines, i):
    """Outcome table lines after the intro line: pipe, markdown or fixed-width (==== under the header)."""
    rows, j, starts = [], i, None
    unq = lambda x: re.sub(r'^\s*(?:>\s?)+', '', x.rstrip())
    while j < len(lines) and not unq(lines[j]).strip():
        j += 1
    hdr_raw = unq(lines[j]) if j < len(lines) else ''
    if '|' in hdr_raw:
        split = lambda r: [c.strip() for c in r.strip().strip('|').split('|')]
    else:
        ind = len(hdr_raw) - len(hdr_raw.lstrip())
        starts = [m.start() + ind for m in re.finditer(r'(?:(?<=\s{2})|^)\S', hdr_raw[ind:])]
        split = lambda r: _fw_cells(r, starts)
    hdr = split(hdr_raw)
    j += 1
    while j < len(lines):
        r = unq(lines[j])
        if not r.strip():
            break
        if re.fullmatch(r'[\s=\-|:+]+', r):
            j += 1
            continue
        c = split(r)
        if len(c) != len(hdr):
            break
        rows.append(c)
        j += 1
    if not rows:
        raise ParseError('empty outcome table')
    cells = {}
    for r in rows:
        for b, o in zip(hdr[1:], r[1:]):
            cells[(low(r[0]), low(b))] = o.strip()
    return cells, j


def parse_card(text):
    cd = Card()
    lines = text.split('\n')
    i, auto = 0, 100
    while i < len(lines):
        raw = lines[i]
        i += 1
        l = clean(raw)
        if not l:
            continue
        m = re.search(r'its as-of date, (' + DATE_RE + ')', l)
        if m:
            cd.D = to_day(m[1])
        if l.startswith('Use only this record. If it does not say whether something is true'):
            cd.world = 'open'; continue
        m = re.match(r'^This record is complete up to and including (' + DATE_RE + r'): (?:any (.+?) not listed did not happen, and )?every list names all its members', l)
        if m:
            cd.world = 'closed'; cd.closed_all_lists = True
            cd.closed_events |= set(_quoted(m[2] or '')); continue
        m = re.match(r'^This record names every "(.+?)" event up to and including (' + DATE_RE + r')\.', l)
        if m:
            cd.world = 'local'; cd.local_event = low(m[1]); cd.closed_events.add(low(m[1])); continue
        m = re.match(r'^The list under (.+?) names every (.+?) up to and including (' + DATE_RE + r')\.', l)
        if m:
            cd.world = 'local'; cd.local_list = low(m[1]); continue
        if re.search(r'means? the value is unknown', l) or 'on an event line means' in l:
            for q in re.findall(r"'([^']+)'", l.replace("don't", 'don’t').replace("can't", 'can’t')):
                q = q.replace('’', "'")
                if not q.startswith('(membership'):
                    cd.markers.add(low(q))
            if 'blank cell' in l:
                cd.blank = True
            continue
        m = re.search(r"only cells marked (.+?) are unknown", l)
        if m:
            for q in re.findall(r"'([^']+)'", m[1]):
                cd.markers.add(low(q))
            if 'left blank' in l:
                cd.blank = True
            continue
        if 'null values are unknown' in l or 'null means the value is unknown' in l:
            cd.null_unknown = True; continue
        m = re.match(r'^Only facts without the tag (.+?) count; (.+?) statements are treated as unknown', l)
        if m:
            cd.tag = low(m[1].strip("'\"")); cd.tag_counts = False; continue
        m = re.match(r'^(.+?) statements count as facts\.', l)
        if m:
            cd.tag = low(m[1].strip("'\"")); cd.tag_counts = True; continue
        m = re.match(r'^All (.+?) figures are whole (.+?); an unknown (.+?) can be any whole value from (-?\d+) to (-?\d+), both included\.', l)
        if m:
            cd.num_dom[low(m[1])] = (int(m[4]), int(m[5]), low(m[2])); continue
        m = re.match(r'^All (.+?) figures are whole (.+?)\.$', l)
        if m:
            cd.num_dom.setdefault(low(m[1]), (None, None, low(m[2]))); continue
        m = re.match(r'^An unknown (.+?) is one of (.+)$', l)
        if m:
            cd.cat_dom[low(m[1])] = _cat_values(m[2]); continue
        m = re.match(r'^If the (.+?) for (.+?) happened, its day can be any day from (' + DATE_RE + ') to (' + DATE_RE + r'), both included', l)
        if m:
            cd.ev_day_dom[(low(m[1]), low(m[2]))] = (to_day(m[3]), to_day(m[4])); continue
        m = re.match(r'^Figures marked (\S+) are rounded to the nearest (\d+) (.+?) \(halves round up\).*?\. (.+?) figures are whole', l)
        if m:
            cd.rounding[low(m[4])] = (m[1], int(m[2]), low(m[3])); continue
        m = re.match(r'^All (.+?) figures are in (.+?) unless another unit is written\.', l)
        if m:
            cd.default_unit[low(m[1])] = low(m[2]); continue
        m = re.match(r'^An? (.+?) figure written without a unit may be in (.+?) or in (.+?)\.$', l)
        if m:
            cd.ambiguous[low(m[1])] = (low(m[2]), low(m[3])); continue
        m = re.match(r'^1 (.+?) = (\d+) (.+?)\.$', l)
        if m:
            cd.conv[low(m[1])] = (int(m[2]), low(m[3])); continue
        m = re.match(r'^(The base policy|Notice [A-Z]) takes effect on (.+?)\.$', l)
        if m:
            dd = date_dom(m[2])
            if dd is None:
                raise ParseError('notice date %r' % m[2])
            cd.notices[low(m[1])] = dd; continue
        m = OTAB_RE.match(l)
        if m:
            num = int(next(g for g in m.groups()[:4] if g) if any(m.groups()[:4]) else auto)
            cells, i = _parse_otable(lines, i)
            cd.otables.append((num, low(m[5]), low(m[6]), low(m[7]), {k: low(v) for k, v in cells.items()}))
            continue
        m = RULE_RE.match(l)
        if m:
            g = [x for x in m.groups()[:4] if x]
            if g:
                num = int(g[0])
            else:
                auto += 1; num = auto
            conds, unless = parse_conds(m[8])
            cd.rules.append(Rule(num, low(m[5]), low(m[6]), conds, unless))
            if m[7] == 'exactly when':
                cd.onlyif.append((low(m[6]), conds))
            continue
        m = EXC_RE.match(l)
        if m:
            conds, unless = parse_conds(m[6])
            cell = (low(m[2]), low(m[3])) if m[2] else None
            cd.rules.append(Rule('x%d_%d' % (int(m[1]), len(cd.rules)), low(m[4]), low(m[5]), conds, unless,
                                 exc_of=int(m[1]), cell=cell, kind='exception'))
            continue
        m = re.match(r'^The outcome is "(.+?)" only if (.+)$', l)
        if m:
            conds, unless = parse_conds(m[2])
            if unless:
                raise ParseError('unless inside only-if')
            cd.onlyif.append((low(m[1]), conds)); continue
        m = re.match(r'^If no rule applies .*?, the outcome is "(.+?)"', l)
        if m:
            cd.default = low(m[1]); continue
        if 'an exception beats the rule it names' in l:
            cd.test_exception = True
        if 'with a later effective date beats' in l:
            cd.test_date = True
        if re.search(r'a rule about .* beats a rule about', l):
            cd.test_subclass = True
        if 'beats' in l:
            continue
        m = re.match(r"^'(.+?)' means the record does not settle the outcome", l)
        if m:
            cd.nei_opt.add(low(m[1])); continue
        m = re.match(r"^'(.+?)' means no listed outcome can be correct", l)
        if m:
            cd.none_opt.add(low(m[1])); continue
        m = re.search(r"'(.+?)' means the record already settles the answer", l)
        if m:
            cd.nothing_opt.add(low(m[1])); continue
        m = re.match(r'^If records tie on (.+?), the one with the (lower ID number|earlier .+?|later .+?) is chosen', l)
        if m:
            cd.tie = (low(m[1]), low(m[2])); continue
        m = re.match(r'^Each (.+) events? happens? at most once for each (.+?)\.$', l)
        if m:
            cd.once_types |= set(_quoted(m[1])); continue
        m = re.match(r'^No two (.+) events in this record happened on the same day\.', l)
        if m:
            cd.noshare_types |= set(_quoted(m[1])); continue
        m = re.match(r'^Every (.+?) is an? (.+?)\.$', l)
        if m and 'member' not in l:
            cd.subclass.append((low(m[1]), low(m[2]))); continue
        cd.unknown_lines.append(l)
    if cd.world is None:
        raise ParseError('no world rule')
    npol = sum(1 for x in lines if re.search(r'the outcome is "|the outcome table below', clean(x), re.I) and not clean(x).startswith(("'", 'If no rule')))
    if npol != len(cd.rules) + len([o for o in cd.onlyif if not any(o[1] is r.conds for r in cd.rules)]) + len(cd.otables):
        raise ParseError('policy lines %d vs parsed %d' % (npol, len(cd.rules) + len(cd.onlyif) + len(cd.otables)))
    for t in cd.otables:
        if not t[4]:
            raise ParseError('empty outcome table')
    return cd


# ----------------------------------------------------------------------------------------------
# D. Interpreting record values under the card (markers, tags, plans, units, rounding, closure)
# ----------------------------------------------------------------------------------------------
UNKNOWN = 'UNKNOWN'


def unorm(u):
    u = low(u)
    if u.endswith('ies') and len(u) > 4:          # repair r1 (parser only): 'entries' -> 'entry'
        return u[:-3] + 'y'
    return u[:-1] if u.endswith('s') and not u.endswith('ss') else u


def nnorm(s):
    s = low(s)
    s = re.sub(r'^(a|an|the) ', '', s)
    return ' '.join(unorm(w) for w in s.split())


class Facts:
    def __init__(self, card, pairs, tables):
        self.cd, self.pairs, self.tables = card, pairs, tables
        self.lists = {}
        for k, v, sec in pairs:
            if low(k) == 'as-of date' and self.cd.D is None:
                self.cd.D = to_day(v)

    # --- markers / tags ---------------------------------------------------------------------
    def split_tag(self, v):
        """-> (value without tag, tagged?)"""
        if self.cd.tag:
            m = re.fullmatch(r'(.*?)\s*\(' + re.escape(self.cd.tag) + r'\)', v.strip(), re.I)
            if m:
                return m.group(1).strip(), True
        m = re.fullmatch(r'(.*?)\s*\((self-reported|unverified|claimed by the applicant|unconfirmed)\)', v.strip(), re.I)
        if m:
            return m.group(1).strip(), True
        return v.strip(), False

    # --- lookup ------------------------------------------------------------------------------
    def get(self, attr, ent=None, section=None):
        attr = low(attr)
        hits = []
        for k, v, sec in self.pairs:
            lk = low(k)
            if ent is not None and lk == attr + ' for ' + low(ent):
                hits.append((v, sec))
            elif lk == attr and (section is None or sec == section or sec is None):
                hits.append((v, sec))
        if section is not None:
            own = [h for h in hits if h[1] == section]
            if own:
                return own[0][0]
        return hits[0][0] if hits else None

    # --- units -------------------------------------------------------------------------------
    def factor(self, unit, target):
        """How many `target` units in one `unit` (exact whole factor), via the card's conversion lines."""
        u, t = unorm(unit), unorm(target)
        if u == t:
            return 1
        conv = {unorm(a): (c, unorm(b)) for a, (c, b) in self.cd.conv.items()}
        seen, cur, f = set(), u, 1
        while cur in conv and cur not in seen:
            seen.add(cur)
            c, b = conv[cur]
            f *= c
            cur = b
            if cur == t:
                return f
        raise ParseError('no conversion %s -> %s' % (unit, target))

    def marker(self, v):
        lv = low(v)
        mk = self.cd.markers or {'not recorded', 'unknown'}
        if lv in mk:
            return True
        return lv == '' and (self.cd.blank or self.cd.null_unknown)

    def small_unit(self, attr):
        d = self.cd.num_dom.get(low(attr))
        return d[2] if d else None

    def num_dom(self, attr):
        d = self.cd.num_dom.get(low(attr))
        if not d or d[0] is None:
            raise ParseError('no number domain for %r' % attr)
        return [(d[0], d[1])]

    def num_value(self, attr, raw):
        """raw record figure -> list of (lo, hi) intervals in the smallest unit; None = unknown (use domain)."""
        if raw is None:
            return None
        v, tagged = self.split_tag(raw)
        if tagged and not self.cd.tag_counts:
            return None
        if self.marker(v):
            return None
        S = self.small_unit(attr)
        m = re.fullmatch(r'from (-?\d+(?:\.\d+)?) to (-?\d+(?:\.\d+)?)(?: (.+))?', v)
        if m:
            u = m[3] or self.cd.default_unit.get(low(attr)) or S
            f = self.factor(u, S or u)
            return [(self._int(float(m[1]) * f), self._int(float(m[2]) * f))]
        m = re.fullmatch(r'(-?\d+(?:\.\d+)?)\s*([^\w\s.]+)?(?:\s+(.+))?', v)
        if not m:
            raise ParseError('figure %r' % v)
        x, mark, u = float(m[1]), m[2], m[3]
        if u is None:
            if low(attr) in self.cd.ambiguous and not mark:
                U, V = self.cd.ambiguous[low(attr)]
                return [(self._int(x * self.factor(w, S or w)),) * 2 for w in (U, V)]
            u = self.cd.default_unit.get(low(attr)) or S
        f = self.factor(u, S or u) if u else 1
        if mark:
            rd = self.cd.rounding.get(low(attr))
            if rd is None:
                raise ParseError('rounded figure without rounding sentence %r' % attr)
            Rs = rd[1] * self.factor(rd[2], S or rd[2])
            xs = x * f
            return [(self._int(xs - Rs / 2), self._int(xs + Rs / 2) - 1)]
        return [(self._int(x * f),) * 2]

    @staticmethod
    def _int(x):
        if abs(x - round(x)) > 1e-9:
            raise ParseError('non-integer value %r' % x)
        return int(round(x))

    def cat_value(self, attr, raw):
        """-> list of possible values (lower; '__other__' for 'another value')."""
        if raw is not None:
            v, tagged = self.split_tag(raw)
            if not (tagged and not self.cd.tag_counts) and not self.marker(v):
                return [low(v)]
        d = self.cd.cat_dom.get(low(attr))
        if d is None:
            raise ParseError('no category domain for %r' % attr)
        return list(d[0]) + (['__other__'] if d[1] else [])

    def ev_closes(self, ev):
        return low(ev) in self.cd.closed_events

    def event(self, ev, ent):
        """-> dict(h=set of possible happened-by-D values, dom=(lo,hi) day domain if it happened, plan=day|None)."""
        ev = low(ev)
        D = self.cd.D
        sd = self.cd.ev_day_dom.get((ev, low(ent)), (-INF, D))
        raw = self.get(ev, ent)
        unk = {'h': {True, False}, 'dom': sd, 'plan': None}
        if raw is None:
            return {'h': {False}, 'dom': None, 'plan': None} if self.ev_closes(ev) else unk
        if raw == '__NO__':
            return {'h': {False}, 'dom': None, 'plan': None}
        v, tagged = self.split_tag(raw)
        if self.marker(v):
            return unk
        m = re.fullmatch(r'(?:' + '|'.join(self.cd.plan_words) + r')(?: for| on)? (.+)', low(v))
        if m:
            pd = date_dom(m[1])
            pdd = pd[0] if pd and pd[0] == pd[1] else None
            if self.ev_closes(ev):
                return {'h': {False}, 'dom': None, 'plan': pdd}
            return dict(unk, plan=pdd)
        dd = date_dom(v)
        if dd is None:
            raise ParseError('event value %r' % v)
        if tagged and not self.cd.tag_counts:
            return {'h': {True, False}, 'dom': dd, 'plan': None}
        return {'h': {True}, 'dom': dd, 'plan': None}

    def find_list(self, phrase):
        """List field whose heading matches the noun phrase ('a contested service attempt' / 'Weave Standards Desk')."""
        want = nnorm(phrase)
        cands = []
        for k, v, sec in self.pairs:
            if nnorm(k) == want:
                cands.append((k, v))
        if not cands:
            for k, v, sec in self.pairs:
                nk = nnorm(k)
                if want.startswith(nk) or nk.startswith(want):
                    cands.append((k, v))
        return cands[0] if cands else (None, None)

    def member(self, phrase, ent):
        k, v = self.find_list(phrase)
        closes = self.cd.closed_all_lists or (k is not None and self.cd.local_list is not None and
                                               nnorm(self.cd.local_list) == nnorm(k))
        if k is None or not v.strip():
            raise ParseError('named list not found in record (rows 2-3 say it is always shown)')
        for item in re.split(r',\s*(?![^()]*\))|\s+and\s+', v):
            item = item.strip().rstrip('.')
            m = re.fullmatch(r'(.+?)\s*\((.+?)\)', item)
            lab, ann = (m[1].strip(), low(m[2])) if m else (item, None)
            if low(lab) != low(ent):
                continue
            if ann is None:
                return {True}
            if ann.startswith('membership'):
                return {True, False}
            if self.cd.tag and ann == self.cd.tag:
                return {True} if self.cd.tag_counts else {True, False}
            raise ParseError('list annotation %r' % ann)
        return {False} if closes else {True, False}


# ----------------------------------------------------------------------------------------------
# E. Rule cards (S1, S2, S5): variables, completions and Out(c) by explicit enumeration
# ----------------------------------------------------------------------------------------------
def region_reps(intervals, breaks):
    """One representative per region of the union of `intervals`, cut at every break point b
    (a region boundary lies between b-1 and b)."""
    reps = []
    for lo, hi in intervals:
        cuts = sorted({b for b in breaks if lo < b <= hi})
        start = lo
        for b in cuts:
            reps.append(start)
            start = b
        reps.append(start)
    return sorted(set(reps))


class RuleModel:
    def __init__(self, facts, ent, section=None):
        self.f, self.cd, self.ent, self.sec = facts, facts.cd, ent, section
        if self.cd.subclass or self.cd.test_subclass:
            raise ParseError('subclass relations not modelled')
        self.atoms = []
        for r in self.cd.rules:
            self.atoms += r.conds + ([r.unless] if r.unless else [])
        for o, conds in self.cd.onlyif:
            self.atoms += conds
        self.keymap = {}
        for a in self.atoms:
            self.keymap[a] = self.var_of(a)
        for t in self.cd.otables:
            self.keymap[('tab', t[2])] = ('cat', t[2])
            self.keymap[('tab', t[3])] = ('cat', t[3])
        self.vars = {}
        for k in set(self.keymap.values()):
            self.vars[k] = self.values(k)
        for n, (lo, hi) in self.cd.notices.items():
            self.vars[('notice', n)] = None
        self._notice_values()

    def var_of(self, a):
        if a[0] == 'cmp':
            return ('num', a[1])
        if a[0] == 'ev':
            return ('ev', a[2])
        subj = a[1]
        if subj in self.cd.cat_dom or subj in self.cd.num_dom or self.f.get(subj, section=self.sec) is not None:
            return ('cat', subj)
        return ('mem', nnorm(a[2]), a[2])

    def threshold(self, a):
        S = self.f.small_unit(a[1])
        t = float(a[3])
        if a[4]:
            t *= self.f.factor(a[4], S or a[4])
        return Facts._int(t)

    def values(self, k):
        if k[0] == 'num':
            raw = self.f.get(k[1], section=self.sec)
            iv = self.f.num_value(k[1], raw)
            if iv is None:
                iv = self.f.num_dom(k[1])
            br = set()
            for a in self.atoms:
                if a[0] == 'cmp' and a[1] == k[1]:
                    t = self.threshold(a)
                    br.add(t if a[2] in ('>=', '<') else t + 1)
            return region_reps(iv, br)
        if k[0] == 'cat':
            return self.f.cat_value(k[1], self.f.get(k[1], section=self.sec))
        if k[0] == 'ev':
            return sorted(self.f.event(k[1], self.ent)['h'])
        if k[0] == 'mem':
            return sorted(self.f.member(k[2], self.ent))
        raise ParseError('var %r' % (k,))

    def _notice_values(self):
        nd = self.cd.notices
        exact = {n: lo for n, (lo, hi) in nd.items() if lo == hi}
        for n, (lo, hi) in nd.items():
            if lo == hi:
                self.vars[('notice', n)] = [lo]
                continue
            if self.cd.D is not None and hi > self.cd.D:
                raise ParseError('notice domain past D')
            pts = {lo, hi}
            for m, (l2, h2) in nd.items():
                if m != n:
                    pts |= {l2 - 1, l2 + 1, h2 - 1, h2 + 1}
            self.vars[('notice', n)] = sorted(p for p in pts if lo <= p <= hi and p not in exact.values())

    def holds(self, a, asg):
        k = self.keymap[a]
        v = asg[k]
        if a[0] == 'cmp':
            t = self.threshold(a)
            return {'>=': v >= t, '<=': v <= t, '>': v > t, '<': v < t}[a[2]]
        if a[0] == 'ev':
            return v == a[3]
        if k[0] == 'cat':
            return v == low(a[2])
        return v is True

    def completions(self):
        keys = sorted(self.vars, key=str)
        doms = [self.vars[k] for k in keys]
        if any(len(d) == 0 for d in doms):
            raise ParseError('empty domain (inconsistent record)')
        n = 1
        for d in doms:
            n *= len(d)
        if n > 400000:
            raise ParseError('too many completions %d' % n)
        nk = [k for k in keys if k[0] == 'notice']
        for combo in itertools.product(*doms):
            asg = dict(zip(keys, combo))
            days = [asg[k] for k in nk]
            if len(set(days)) != len(days):
                continue          # no two notices take effect on the same day (row 45)
            yield asg

    def fired(self, asg):
        out = []
        for r in self.cd.rules:
            if all(self.holds(a, asg) for a in r.conds) and not (r.unless and self.holds(r.unless, asg)):
                out.append(r)
        for num, notice, A, B, cells in self.cd.otables:
            key = (asg[('cat', A)], asg[('cat', B)])
            if key in cells:
                out.append(Rule(num, notice, cells[key], [], cell=key, kind='cell'))
        return out

    def beats(self, r, s, asg):
        if self.cd.test_exception:
            if r.kind == 'exception' and r.exc_of == s.num and (r.cell is None or r.cell == s.cell):
                return True
            if s.kind == 'exception' and s.exc_of == r.num and (s.cell is None or s.cell == r.cell):
                return False
        if self.cd.test_date and r.notice != s.notice:
            return asg[('notice', r.notice)] > asg[('notice', s.notice)]
        return None

    def linked(self, r, s):
        """Separated by test 1 (exception link)."""
        if not self.cd.test_exception:
            return False
        return (r.kind == 'exception' and r.exc_of == s.num and (r.cell is None or r.cell == s.cell)) or \
               (s.kind == 'exception' and s.exc_of == r.num and (s.cell is None or s.cell == r.cell))

    def out(self, asg):
        fired = self.fired(asg)
        blocked = {o for o, conds in self.cd.onlyif if not all(self.holds(a, asg) for a in conds)}
        rem = [r for r in fired if r.outcome not in blocked]
        if not rem:
            if self.cd.default is None:
                raise ParseError('no default outcome')
            return self.cd.default
        outs = {r.outcome for r in rem}
        if len(outs) == 1:
            return outs.pop()
        for r in rem:
            for s in rem:
                if r.outcome != s.outcome and r.notice == s.notice and not self.linked(r, s):
                    return ('DROP', 'ii')
        W = [r for r in rem if all(self.beats(r, s, asg) is True for s in rem if s.outcome != r.outcome)]
        wo = {r.outcome for r in W}
        if len(wo) != 1:
            return ('DROP', 'i')
        return wo.pop()


# ----------------------------------------------------------------------------------------------
# F. Question frames and claims S
# ----------------------------------------------------------------------------------------------
FRAMES = [
    ('cgap', r'Which one additional fact would settle (.+?)\?$'),
    ('ccase', r'Which of these cases (can|cannot) be decided from its record\?$'),
    ('cout', r'Which outcome applies to (.+?)\?$'),
    ('crec', r'Which record (.+?)\?$'),
    ('det', r'Is it not the case that the record leaves open whether (.+?)\?$'),
    ('det', r'Can it be determined whether (.+?)\?$'),
    ('open', r'Does the record leave open whether (.+?)\?$'),
    ('open', r'Is it impossible to tell from the record whether (.+?)\?$'),
    ('est', r'Does the record establish that (.+?)\?$'),
    ('est', r'Does the record show that (.+?)\?$'),
    ('est', r'Can it be determined that (.+?)\?$'),
    ('est', r'Is it true that (.+?)\?$'),
    ('plain', r'(?:^|[.!?:]\s+)((?:Is|Did|Does|Do) .+?)\?$'),
]


def find_question(instructions):
    best = None
    for raw in instructions.split('\n'):
        l = clean(raw)
        if not l or l.startswith("'") or l.startswith('"'):
            continue
        for kind, pat in FRAMES:
            m = re.search(pat, l)
            if m:
                best = (kind, m)
                break
    if best is None:
        raise ParseError('no question frame')
    return best


def plain_to_s(q):
    """Subject-auxiliary inversion -> declarative S (accepted by the claim parser)."""
    m = re.fullmatch(r'Did (.+?) happen (.+)', q)
    if m:
        return '%s happened %s' % (m[1], m[2])
    m = re.fullmatch(r'Is (\S+) on the (.+)', q)
    if m:
        return '%s is on the %s' % (m[1], m[2])
    m = re.fullmatch(r'Is the outcome for (.+?) (".+")', q)
    if m:
        return 'the outcome for %s is %s' % (m[1], m[2])
    m = re.fullmatch(r'Is (the total of .+?) ' + CMP_RE + r' (.+)', q)
    if m:
        return '%s is %s %s' % (m[1], m[2], m[3])
    m = re.fullmatch(r'(?:Does|Do) (.+?) have (.+)', q)
    if m:
        return '%s has %s' % (m[1], m[2])
    raise ParseError('plain question %r' % q)


def parse_pred(s):
    s = s.strip()
    m = re.fullmatch(CMP_RE + r' (-?\d+(?:\.\d+)?)(?: (.+))?', s)
    if m:
        return ('cmp', CMP_OPS[m[1]], float(m[2]), (m[3] or '').strip())
    return ('cat', low(s))


def parse_claim(S):
    S = S.strip()
    m = re.fullmatch(r'the outcome for (.+?) (is|is not) "(.+)"', S)
    if m:
        return ('outcome', m[1], low(m[3]), m[2] == 'is not')
    m = re.fullmatch(r'(\S+(?: \S+)?) (is|is not) on the (.+)', S)
    if m:
        return ('member', m[1], m[3], m[2] == 'is not')
    HAP = r'(happened|did not happen)'
    m = re.fullmatch(r'the (.+?) for (.+?) ' + HAP + r' before the (.+?) for (.+)', S)
    if m:
        return ('order', low(m[1]), m[2], low(m[4]), m[5], m[3] != 'happened')
    m = re.fullmatch(r'the (.+?) for (.+?) ' + HAP + r' at least (\d+) days after the (.+?) for (.+)', S)
    if m:
        return ('daycount', low(m[1]), m[2], int(m[4]), low(m[5]), m[6], m[3] != 'happened')
    m = re.fullmatch(r'the (.+?) for (.+?) ' + HAP + r' (by|on or before|no later than) (' + DATE_RE + ')', S)
    if m:
        return ('deadline', low(m[1]), m[2], to_day(m[5]), m[3] != 'happened')
    m = re.fullmatch(r'the total of (.+?) is ' + CMP_RE + r' (-?\d+(?:\.\d+)?) (.+)', S)
    if m:
        figs = re.split(r', | and ', m[1])
        out = []
        for fg in figs:
            mf = re.fullmatch(r'the (.+?) for (.+)', fg.strip())
            if not mf:
                raise ParseError('total figure %r' % fg)
            out.append((low(mf[1]), mf[2]))
        return ('total', out, CMP_OPS[m[2]], float(m[3]), m[4])
    FILT = r'(?: whose (.+?) is (.+?))?'
    m = re.fullmatch(CMP_RE + r' (\d+) (.+?) in the (\S+)' + FILT + r' (?:has|have) an? (.+?) of (.+)', S)
    if m:
        return ('count', CMP_OPS[m[1]], int(m[2]), low(m[3]), (low(m[5]), low(m[6])) if m[5] else None,
                low(m[7] + ' of ' + m[8]), None)
    m = re.fullmatch(r'(every|at least one|no) (.+?) in the (\S+)' + FILT + r' (?:has|have) an? (.+?) of (.+)', S)
    if m:
        return ('quant', m[1], low(m[2]), (low(m[4]), low(m[5])) if m[4] else None, low(m[6] + ' of ' + m[7]), None)
    raise ParseError('claim %r' % S)


def cmpv(v, op, t):
    return {'>=': v >= t, '<=': v <= t, '>': v > t, '<': v < t}[op]


# ----------------------------------------------------------------------------------------------
# G. Register tables (S3): one variable per unknown cell; per-record local models (records are
#    independent), so a claim's truth set is the set of truth values over all joint completions.
# ----------------------------------------------------------------------------------------------
class TableModel:
    def __init__(self, facts):
        self.f, self.cd = facts, facts.cd
        tabs = [t for t in facts.tables if len(t.header) >= 3]
        if not tabs:
            raise ParseError('no register table')
        self.t = max(tabs, key=lambda t: len(t.rows))
        self.cols = [self._colname(h) for h in self.t.header]
        self.nulls = getattr(self.t, 'nulls', None)
        ids = [r[0].strip() for r in self.t.rows]
        pre = re.match(r'([A-Z]+-)', ids[0]).group(1)
        listed = set()
        for k, v, sec in facts.pairs:
            listed |= set(re.findall(re.escape(pre) + r'\d+', v))
        seen = set(re.findall(r'(?<![\w-])' + re.escape(pre) + r'\d+', getattr(facts, 'state_text', '')))
        if (seen - listed) - set(ids) or len(set(ids)) != len(ids):
            raise ParseError('register table rows not all parsed')

    @staticmethod
    def _colname(h):
        h = re.sub(r'\s*\(.*?\)\s*$', '', h.strip())
        return low(h.replace('_', ' '))

    def col(self, name):
        name = low(name)
        if name in self.cols:
            return self.cols.index(name)
        c = [i for i, h in enumerate(self.cols) if h.startswith(name + ' ') or h == name]
        if len(c) == 1:
            self.cols[c[0]] = name
            return c[0]
        raise ParseError('column %r not in %r' % (name, self.cols))

    def unit_of(self, j):
        m = re.search(r'\((.+?)\)\s*$', self.t.header[j])
        return m[1] if m else None

    def cell_values(self, i, j, extra_breaks=()):
        """Candidate values of cell (i, j): exact -> [v]; unknown -> region reps over its stated domain."""
        raw = self.t.rows[i][j]
        name = self.cols[j]
        unknown = self.f.marker(raw) or (self.nulls is not None and self.nulls[i][j])
        if name in self.cd.num_dom and self.cd.num_dom[name][0] is not None or (not unknown and re.fullmatch(r'-?\d+(\.\d+)?', raw.strip())):
            if not unknown:
                v = raw.strip()
                u = self.unit_of(j)
                if re.fullmatch(r'-?\d+(\.\d+)?', v) and u:
                    v = v + ' ' + u
                iv = self.f.num_value(name, v) if name in self.cd.num_dom else [(int(float(raw)),) * 2]
            else:
                iv = self.f.num_dom(name)
            if unknown:
                return 'num', sorted(set(region_reps(iv, set(extra_breaks))) | {hi for lo, hi in iv})
            return 'num', [iv[0][0]]
        if unknown:
            d = self.cd.cat_dom.get(name)
            if d is None:
                raise ParseError('no domain for unknown cell in %r' % name)
            return 'cat', list(d[0]) + (['__other__'] if d[1] else [])
        return 'cat', [low(raw)]

    def pred_breaks(self, pred, j):
        if pred[0] != 'cmp':
            return ()
        t = self.threshold(pred, j)
        return (t, t + 1)

    def threshold(self, pred, j):
        name = self.cols[j]
        S = self.f.small_unit(name)
        t = pred[2]
        if pred[3] and S:
            t *= self.f.factor(pred[3], S)
        return Facts._int(t)

    def test(self, pred, j, v):
        if pred[0] == 'cmp':
            return cmpv(v, pred[1], self.threshold(pred, j))
        return v == pred[1]

    def split_tail(self, tail):
        """'<column> of <predicate>': the column is the longest table column name the tail starts with."""
        best = None
        for h in self.cols:
            if tail.startswith(h + ' of ') and (best is None or len(h) > len(best)):
                best = h
        if best is None:
            for h in self.cols:
                hh = h.split(' ')
                for k in range(len(hh), 0, -1):
                    p = ' '.join(hh[:k])
                    if tail.startswith(p + ' of ') and (best is None or len(p) > len(best)):
                        best = p
        if best is None:
            raise ParseError('no column for %r' % tail)
        return best, parse_pred(tail[len(best) + 4:])

    def record_states(self, i, filt, j, pred):
        """Set of (passes filter, qualifies) pairs over the local completions of record i."""
        cells = {}
        if filt:
            fj = self.col(filt[0])
            cells[fj] = self.cell_values(i, fj)[1]
        brk = self.pred_breaks(pred, j)
        kind, vals = self.cell_values(i, j, brk)
        cells[j] = vals if j not in cells else [v for v in cells[j] if v in vals]
        keys = sorted(cells)
        out = set()
        for combo in itertools.product(*[cells[k] for k in keys]):
            a = dict(zip(keys, combo))
            ps = True if not filt else a[self.col(filt[0])] == filt[1]
            out.add((ps, self.test(pred, j, a[j])))
        return out

    def claim_T(self, c):
        if c[0] == 'quant':
            _, q, noun, filt, colname, pred = c
        else:
            _, op, N, noun, filt, colname, pred = c
        colname, pred = self.split_tail(colname)
        j = self.col(colname)
        if filt:
            self.col(filt[0])
        st = [self.record_states(i, filt, j, pred) for i in range(len(self.t.rows))]
        if c[0] == 'quant':
            if q == 'every':
                t_ok = all(any((not p) or ql for p, ql in s) for s in st)
                f_ok = any(any(p and not ql for p, ql in s) for s in st)
            elif q == 'at least one':
                t_ok = any(any(p and ql for p, ql in s) for s in st)
                f_ok = all(any(not (p and ql) for p, ql in s) for s in st)
            else:
                t_ok = all(any(not (p and ql) for p, ql in s) for s in st)
                f_ok = any(any(p and ql for p, ql in s) for s in st)
            return {v for v, ok in ((True, t_ok), (False, f_ok)) if ok}
        lo = sum(1 for s in st if all(p and ql for p, ql in s))
        hi = sum(1 for s in st if any(p and ql for p, ql in s))
        return {cmpv(n, op, N) for n in range(lo, hi + 1)}

    def argext(self, filt, key, mode):
        """P for 'Which record [whose C is V] has the highest/lowest K?': record r is possible iff its
        best-case witness (r passes, r's key at its extreme, every other record failing the filter where it
        can, else at its opposite extreme) makes r the chosen record under the card's tie rule."""
        kj = self.col(key)
        fj = self.col(filt[0]) if filt else None
        tie = self.cd.tie
        if tie and tie[1] != 'lower id number':
            raise ParseError('tie rule %r' % (tie,))
        n = len(self.t.rows)
        info = []
        for i in range(n):
            pv = [True] if fj is None else sorted({v == filt[1] for v in self.cell_values(i, fj)[1]})
            kv = self.cell_values(i, kj)[1]
            idn = int(re.search(r'(\d+)$', self.t.rows[i][0].strip()).group(1))
            info.append((pv, min(kv), max(kv), idn))
        P = set()
        for r in range(n):
            if True not in info[r][0]:
                continue
            best = info[r][2] if mode == 'highest' else info[r][1]
            ok = True
            for s in range(n):
                if s == r or False in info[s][0]:
                    continue
                other = info[s][1] if mode == 'highest' else info[s][2]
                better = other > best if mode == 'highest' else other < best
                if better or (other == best and info[s][3] < info[r][3]):
                    ok = False
                    break
            if ok:
                P.add(low(self.t.rows[r][0].strip()))
        return P


# ----------------------------------------------------------------------------------------------
# H. Timelines and measurement sheets (S4): day-number and smallest-unit integer models
# ----------------------------------------------------------------------------------------------
def day_cands(lo, hi, marks):
    """Candidate days in [lo, hi]: every day when the span is small, else the boundary days around every
    comparison point (truth of every day comparison is constant between them)."""
    if hi - lo <= 400:
        return list(range(lo, hi + 1))
    pts = {hi}
    for p in marks:
        for q in (p - 1, p, p + 1):
            if lo <= q <= hi:
                pts.add(q)
    pts.add(max(lo, hi - 400))
    return sorted(pts)


def event_options(facts, ev, ent, marks):
    """Possible (happened-by-D, day) values of one (event type, entity): row 54 one occurrence."""
    st = facts.event(ev, ent)
    out = []
    if True in st['h']:
        lo, hi = st['dom']
        hi = min(hi, facts.cd.D)
        lo = max(lo, hi - 4000)
        out += [(True, d) for d in day_cands(lo, hi, marks)]
    if False in st['h']:
        out.append((False, None))
    return out


def recorded_events(facts):
    ev = []
    for k, v, sec in facts.pairs:
        m = re.fullmatch(r'(.+?) for (.+)', low(k))
        if m and (m[1], m[2]) not in ev:
            ev.append((m[1], m[2]))
    return ev


def s4_T(facts, c):
    """Truth set of an S4 claim over all completions of the day model: one happened flag + one day per
    (event type, entity); the row 46 no-shared-day sentence makes every happened event of its named types
    take a distinct day (over the whole record, not only the compared pair)."""
    cd = facts.cd
    D = cd.D
    if c[0] == 'total':
        return total_T(facts, c)
    if c[0] == 'order':
        _, eA, nA, eB, nB, neg = c
        focus = [(eA, low(nA)), (eB, low(nB))]
    elif c[0] == 'daycount':
        _, eA, nA, N, eB, nB, neg = c
        focus = [(eA, low(nA)), (eB, low(nB))]
    elif c[0] == 'deadline':
        _, e, n, DL, neg = c
        focus = [(e, low(n))]
    else:
        raise ParseError('s4 claim %r' % (c[0],))
    marks = [D] + ([DL] if c[0] == 'deadline' else [])
    ns = cd.noshare_types
    others = [x for x in recorded_events(facts) if x[0] in ns and x not in focus]
    oopts = [event_options(facts, e, n, marks) for e, n in others]
    for e, n in focus:
        st = facts.event(e, n)
        if st['dom'] and st['dom'][0] > -INF:
            marks += [st['dom'][0], st['dom'][1]]
    fopts = [event_options(facts, e, n, marks) for e, n in focus]

    def feasible(used, k=0):
        if k == len(oopts):
            return True
        for h, d in oopts[k]:
            if not h:
                if feasible(used, k + 1):
                    return True
            elif d not in used and feasible(used | {d}, k + 1):
                return True
        return False

    T = set()
    for combo in itertools.product(*fopts):
        used = set()
        okc = True
        for (e, n), (h, d) in zip(focus, combo):
            if h and e in ns:
                if d in used:
                    okc = False
                used.add(d)
        if not okc or not feasible(used):
            continue
        if c[0] in ('order', 'daycount'):
            (hA, dA), (hB, dB) = combo
            if not (hA and hB):
                raise ParseError('compared event not recorded as happened')
            v = dA < dB if c[0] == 'order' else dA >= dB + N
            T.add(v != neg)
        else:
            h, d = combo[0]
            vals = {d <= DL} if h else ({False, True} if DL > D else {False})
            T |= {v != neg for v in vals}
    return T


def total_T(facts, c):
    _, figs, op, t, unit = c
    q0 = figs[0][0]
    S = facts.small_unit(q0) or unit
    tt = Facts._int(t * facts.factor(unit, S))
    opts = []
    for q, ent in figs:
        iv = facts.num_value(q, facts.get(q, ent))
        if iv is None:
            iv = facts.num_dom(q)
        opts.append(iv)
    T = set()
    for combo in itertools.product(*opts):
        lo = sum(a for a, b in combo)
        hi = sum(b for a, b in combo)
        for cand in {lo, hi, tt - 1, tt, tt + 1}:
            if lo <= cand <= hi:
                T.add(cmpv(cand, op, tt))
    return T


# ----------------------------------------------------------------------------------------------
# I. Per-row solve: P / T, then gold by the section 1 form table
# ----------------------------------------------------------------------------------------------
class Drop(Exception):
    pass


def outcome_set(model):
    P, drops = set(), set()
    for asg in model.completions():
        o = model.out(asg)
        if isinstance(o, tuple):
            drops.add(o[1])
        else:
            P.add(o)
    if drops:
        raise Drop('formal core drop condition (%s)' % ','.join(sorted(drops)))
    if not P:
        raise ParseError('inconsistent record (no completion)')
    return P


def claim_T(facts, c, sec=None):
    if c[0] == 'outcome':
        model = RuleModel(facts, c[1], section=sec)
        P = outcome_set(model)
        return {(o == c[2]) != c[3] for o in P}, P
    if c[0] == 'member':
        return {v != c[3] for v in facts.member(c[2], c[1])}, None
    if c[0] in ('quant', 'count'):
        return TableModel(facts).claim_T(c), None
    return s4_T(facts, c), None


def choose(options, P, cd):
    """C-OUT / C-REC display rule: settled & listed -> it; P disjoint from L -> None; else NEI."""
    ab = cd.nei_opt | cd.none_opt
    L = {low(o): o for o in options if low(o) not in ab}
    nei = [o for o in options if low(o) in cd.nei_opt]
    non = [o for o in options if low(o) in cd.none_opt]
    hit = P & set(L)
    if len(P) == 1 and hit:
        return L[hit.pop()]
    if not hit:
        return non[0] if non else '__UNDISPLAYED_NONE__'
    return nei[0] if nei else '__UNDISPLAYED_NEI__'


def gap_key(opt, model):
    o = opt.strip()
    o = re.sub(r'^the value of the ', 'the ', o)              # repair r1: long option wordings (parser only)
    m2 = re.fullmatch(r'whether an? "(.+)" event happened for (.+)', o)
    if m2:
        return ('ev', low(m2[1]))
    o = re.sub(r'^(whether .+?) counts as (an? )', r'\1 is \2', o)
    m = re.fullmatch(r'the (.+?) of (.+)', o)
    if m:
        a = low(m[1])
        for k in model.vars:
            if k[0] in ('num', 'cat') and k[1] == a:
                return k
        return ('absent', a)
    m = re.fullmatch(r'whether (.+?) had an? "(.+)" event', o)
    if m:
        return ('ev', low(m[2]))
    m = re.fullmatch(r'whether (.+?) is an? (.+)', o)
    if m:
        for k in model.vars:
            if k[0] == 'mem' and k[1] == nnorm(m[2]):
                return k
        return ('absent', nnorm(m[2]))
    raise ParseError('gap option %r' % o)


def solve(row):
    """-> dict(answer=<derived gold>, kind=<frame kind>, info=<P/T summary for QC>)."""
    cd = parse_card(row['instructions'] + '\n' + (row['card'] or ''))
    opts = row['options'] or []
    kind, mq = find_question(row['instructions'])
    st = row['state']
    if re.search(r'What is the .+? of \S+\?|Did \S+ have an? ".+?" event\?', st):
        pairs, tables = parse_transcript(st), []
    else:
        pairs, tables = parse_state(st, opts if kind == 'ccase' else ())
    facts = Facts(cd, pairs, tables)
    facts.state_text = st
    if cd.D is None:
        raise ParseError('no as-of date')
    if kind in ('det', 'open', 'est', 'plain'):
        S = plain_to_s(mq.group(1)) if kind == 'plain' else mq.group(1)
        c = parse_claim(S)
        T, P = claim_T(facts, c)
        if kind == 'det':
            ans = 1 if len(T) == 1 else 0
        elif kind == 'open':
            ans = 1 if len(T) == 2 else 0
        else:
            ans = 1 if T == {True} else 0
        return {'answer': ans, 'kind': kind, 'claim': c[0], 'T': sorted(T), 'nP': None if P is None else len(P)}
    if kind == 'cout':
        model = RuleModel(facts, mq.group(1))
        catalog = {r.outcome for r in cd.rules} | {cd.default} | {o for t in cd.otables for o in t[4].values()}
        for o in opts:
            if low(o) not in catalog and low(o) not in cd.nei_opt | cd.none_opt:
                raise ParseError('displayed option is neither a catalog outcome nor an abstain option (s6)')
        P = outcome_set(model)
        return {'answer': choose(opts, P, cd), 'kind': kind, 'claim': 'outcome', 'nP': len(P)}
    if kind == 'crec':
        m = re.fullmatch(r'(?:whose (.+?) is (.+?) )?has the (highest|lowest) (.+)', mq.group(1))
        if not m:
            raise ParseError('crec question')
        filt = (low(m[1]), low(m[2])) if m[1] else None
        tm = TableModel(facts)
        ids = {low(r[0].strip()) for r in tm.t.rows}
        for o in opts:
            if low(o) not in ids and low(o) not in cd.nei_opt | cd.none_opt:
                raise ParseError('C-REC option is not a record ID of the table')
        P = tm.argext(filt, low(m[4]), m[3])
        return {'answer': choose(opts, P, cd), 'kind': kind, 'claim': 'argext', 'nP': len(P)}
    if kind == 'cgap':
        mo = re.fullmatch(r'which outcome applies to (.+)', mq.group(1))
        if not mo:
            raise ParseError('cgap question %r' % mq.group(1))
        model = RuleModel(facts, mo.group(1))
        comps = [(asg, model.out(asg)) for asg in model.completions()]
        if any(isinstance(o, tuple) for a, o in comps):
            raise Drop('formal core drop condition')
        P = {o for a, o in comps}
        nothing = [o for o in opts if low(o) in cd.nothing_opt]
        if len(P) == 1:
            return {'answer': nothing[0] if nothing else '__UNDISPLAYED_NOTHING__', 'kind': kind, 'claim': 'outcome',
                    'nP': 1, 'settling': 0}
        settling = []
        for o in opts:
            if low(o) in cd.nothing_opt:
                continue
            k = gap_key(o, model)
            if k not in model.vars:
                continue
            groups = collections.defaultdict(set)
            for a, out in comps:
                groups[a[k]].add(out)
            if all(len(g) == 1 for g in groups.values()):
                settling.append(o)
        if len(settling) != 1:
            raise Drop('C-GAP open row with %d settling listed gaps (row 51)' % len(settling))
        return {'answer': settling[0], 'kind': kind, 'claim': 'outcome', 'nP': len(P), 'settling': 1}
    if kind == 'ccase':
        want = mq.group(1)
        dec = {}
        for lab in opts:
            P = outcome_set(RuleModel(facts, lab, section=lab))
            dec[lab] = len(P) == 1
        pick = [lab for lab in opts if dec[lab] == (want == 'can')]
        if len(pick) != 1:
            raise Drop('C-CASE with %d cases of the asked property (row 52)' % len(pick))
        return {'answer': pick[0], 'kind': kind, 'claim': 'outcome', 'ndec': sum(dec.values())}
    raise ParseError('frame %r' % kind)


# ----------------------------------------------------------------------------------------------
# J. Runner: every row of the three files; mismatches -> mismatch.json (ids, answers, spec item; no row text)
# ----------------------------------------------------------------------------------------------
SPEC_ITEM = {
    ('det', 'outcome'): 's1 Q-DET + formal core Out(c) (rows 7-10, 24, 45, 53)',
    ('open', 'outcome'): 's1 Q-DET negated frame + formal core Out(c) (rows 7-10, 24, 37)',
    ('est', 'outcome'): 's1 Q-EST/Q-PLAIN truth frame + formal core Out(c) (rows 38-39)',
    ('plain', 'outcome'): 's1 Q-PLAIN + formal core Out(c)',
    ('cout', 'outcome'): 's1 C-OUT + rows 33-35, 50 (display rule s6) + formal core Out(c)',
    ('crec', 'argext'): 's1 C-REC + rows 23, 42 (argmax/argmin, ties, filter)',
    ('cgap', 'outcome'): 'row 51 C-GAP (settled first, then settling set)',
    ('ccase', 'outcome'): 'row 52 C-CASE (decidable = |P| = 1)',
    'member': 'rows 2-4, 26, 42 (list membership, closure, markers, evidence)',
    'quant': 'rows 28, 42 (quantifiers over a closed register, filter)',
    'count': 'rows 29, 42, 11-12 (counts over a closed register)',
    'order': 'rows 46, 54, 15, 17 (came first, no-shared-day, one occurrence)',
    'daycount': 'rows 47, 46, 54 (day counts)',
    'deadline': 'rows 16, 18, 27, 54 (deadlines, after D, plans)',
    'total': 'rows 48, 19-22 (totals, rounding, units)',
}


def show_answer(ans, row, cd_like=None):
    """Answer as a class + option index, never the option text."""
    if isinstance(ans, int):
        return 'Yes' if ans == 1 else 'No'
    if ans is None:
        return 'none'
    if ans.startswith('__'):
        return ans.strip('_')
    opts = row['options'] or []
    idx = opts.index(ans) if ans in opts else -1
    return 'opt[%d]' % idx


def gold_class(row, ans):
    return show_answer(ans, row)


def run(files, out_path, limit=None, log=None):
    mism, counts, t0 = [], collections.Counter(), datetime.datetime.now()
    per_file = {}
    for fp in files:
        n = agree = 0
        with open(fp) as fh:
            for ln, line in enumerate(fh):
                if limit and ln >= limit:
                    break
                row = json.loads(line)
                n += 1
                g = row['gold']
                item = None
                try:
                    res = solve(row)
                    a = res['answer']
                    item = SPEC_ITEM.get((res['kind'], res['claim'])) or SPEC_ITEM.get(res['claim'])
                    ok = (a == g)
                    note = ''
                except Drop as e:
                    a, ok, note, item = '__DROP__', False, str(e), 'formal core drop conditions (s1, s4 G2 keep/drop)'
                except Exception as e:
                    a, ok = '__PARSE_FAIL__', False
                    note = '%s: %s' % (type(e).__name__, str(e)[:160])
                    item = 's4 G3 round-trip parse (solver B could not re-read the row)'
                if ok:
                    agree += 1
                else:
                    mism.append({'id': row['id'], 'file': os.path.basename(fp), 'form': row['meta'].get('subtype'),
                                 'sampler': row['meta'].get('sampler'), 'gold': gold_class(row, g),
                                 'solver_b': gold_class(row, a) if not str(a).startswith('__') else a.strip('_'),
                                 'spec_item': item, 'note': note, 'edge': row['meta'].get('edge')})
                counts[(os.path.basename(fp), ok)] += 1
        per_file[os.path.basename(fp)] = {'rows': n, 'agree': agree}
        if log:
            log('%s: %d rows, %d agree, %d mismatch' % (os.path.basename(fp), n, agree, n - agree))
    total = sum(v['rows'] for v in per_file.values())
    agree = sum(v['agree'] for v in per_file.values())
    out = {'solver': 'F6 solver B (model enumeration on parsed text)', 'spec': 'F6.G0.rev8',
           'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'per_file': per_file,
           'rows_checked': total, 'agree': agree, 'agree_pct': round(100.0 * agree / max(total, 1), 3),
           'mismatches': len(mism), 'mismatch_rows': mism}
    with open(out_path, 'w') as fo:
        json.dump(out, fo, indent=1)
    return out


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mismatch.json'))
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('files', nargs='+')
    a = ap.parse_args()
    r = run(a.files, a.out, a.limit, log=lambda s: print(s, flush=True))
    print(json.dumps({k: v for k, v in r.items() if k != 'mismatch_rows'}))

