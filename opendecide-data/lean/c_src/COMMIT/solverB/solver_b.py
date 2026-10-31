#!/usr/bin/env python3
"""COMMIT solver B (gate G2), written from the frozen G0 spec (COMMIT-G0-v7) and the row format only.

Never imports or reads c_src/COMMIT/gen/*.py, qc/*.py or any solver A code. Inputs:
  - the three outputs (out/candidates_r1, out/qc_sample, out/mixdev_S5): row text only (instructions, card, state,
    options, question); the sidecars are NOT read (they carry solver A's derived fields);
  - the hidden commit record (1.2) for the record-based types, looked up by meta.text_source.record_id in the
    record pool (gen/data/pool.jsonl.gz, data only; extracted once to tmp/sb/records.jsonl.gz). From a record B uses
    only the raw structure: message, file old/new paths, change kind, binary/mode flags and hunk lines. All counts are
    re-derived here by a hunk-header state machine (derivation B, 1.2); solver A's stored counts are only compared.

Paradigm per type (spec 2.4, 3.4, 4.4, 5.6, 6.4):
  route  : area table of folder prefixes parsed from the shown definition lines, per-file counts from the hunk-header
           state machine, sqlite GROUP BY area ORDER BY lines (+ 2.2 eligibility re-check).
  triage : hand-written character-scanner state machine (no regex) for the 3.1 EBNF on the record message; definition
           -> type map compiled from the card text; 3.2 file-class filters in sqlite (folder-segment equality join +
           GLOB on the lower-cased file name).
  score  : rubric parsed from the shown card text into per-level membership predicates, compiled to SQL over the
           recounted numstat table; exactly one level must be true.
  gate   : rule parsed from the shown card text into an AST, compiled to sqlite EXISTS / NOT EXISTS / count queries;
           frame parsed from the question; own negation count asserted equal to negcount.k_syn (R4-02); flip once per
           negation (SEM-38). Inverted rows: the same SQL over each case's shown diff headers.
  match  : shown text only (6.4): character scanner for code-shaped words (6.1) + literal case-insensitive boundary
           search over the shown diff's changed lines and header paths; frame + negation as for gate.
Writes solverB/mismatch.json (ids, both answers, spec item; never row text).
"""
import gzip
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)                      # c_src/COMMIT
LEAN = os.path.dirname(os.path.dirname(FAM))     # lean
sys.path.insert(0, os.path.join(LEAN, 'c_src', 'common'))
import negcount  # noqa: E402  (orchestrator-owned shared counter, XF02)

OUTS = ['candidates_r1', 'qc_sample', 'mixdev_S5']
REC_CACHE = os.path.join(FAM, 'tmp', 'sb', 'records.jsonl.gz')
POOL = os.path.join(FAM, 'gen', 'data', 'pool.jsonl.gz')   # data file only
TYPES10 = ['feat', 'fix', 'docs', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']


class ParseFail(Exception):
    pass


# ----------------------------------------------------------------------------------------------------------------
# text helpers
MARK = re.compile(r'^[\s>]*(?:(?:[-*•+]|\d+[.)]|\(\d+\))\s+)?')


def clean(line):
    s = MARK.sub('', line)
    s = s.replace('**', '').replace('__', '') if s.startswith('**') else s
    return s.strip()


def lines_of(text):
    return [clean(l) for l in (text or '').split('\n')]


# ----------------------------------------------------------------------------------------------------------------
# records: derivation B counts (hunk-header state machine, 1.2 A50)
def hunk_counts(header, lines):
    """Walk '@@ -a,b +c,d @@' and the body; return (added, removed, ok)."""
    h = header
    if h is None:
        # CommitChronicle whole-file add/delete: no hunk header; the body must be one-sided
        ms = Counter((ln[0] if isinstance(ln, (list, tuple)) else ln[:1]) for ln in lines)
        return ms['+'], ms['-'], (ms[' '] == 0 and (ms['+'] == 0 or ms['-'] == 0))
    if not h.startswith('@@ -'):
        return None
    i = 4
    def num(i):
        j = i
        while j < len(h) and h[j].isdigit():
            j += 1
        return int(h[i:j]) if j > i else None, j
    a, i = num(i)
    b = 1
    if i < len(h) and h[i] == ',':
        b, i = num(i + 1)
    if h[i:i + 2] != ' +':
        return None
    c, i = num(i + 2)
    d = 1
    if i < len(h) and h[i] == ',':
        d, i = num(i + 1)
    old = new = add = rem = 0
    for ln in lines:
        m = ln[0] if isinstance(ln, (list, tuple)) else ln[:1]
        if m == ' ':
            old += 1; new += 1
        elif m == '-':
            old += 1; rem += 1
        elif m == '+':
            new += 1; add += 1
        elif m == '\\':
            pass
        else:
            return None
    ctx = old - rem
    # CommitChronicle bodies may omit blank context lines; the header must still balance: the context it implies is
    # the same on both sides and covers the context lines present
    return add, rem, ((b - rem) == (d - add) and ctx <= b - rem and b >= rem and d >= add)


def record_files(rec):
    """List of dicts: old, new (None for absent side), added, removed, flags; plus count-agreement flag."""
    out = []
    agree = True
    for f in rec['files']:
        old = f.get('old') if f.get('ct') != 'ADD' else None
        new = f.get('new') if f.get('ct') != 'DELETE' else None
        if f.get('ct') == 'ADD' and not new:
            new = f.get('path')
        if f.get('ct') == 'DELETE' and not old:
            old = f.get('path')
        add = rem = 0
        for hk in f.get('hunks') or []:
            r = hunk_counts(hk['header'], hk['lines'])
            if r is None:
                agree = False
                continue
            add += r[0]; rem += r[1]
            if not r[2]:
                agree = False
        if f.get('binary') or f.get('mode_only'):
            add = rem = 0          # SEM-05 / SEM-07: binary and mode-only files have 0 lines
        if (add, rem) != (f.get('added'), f.get('removed')):
            agree = False
        out.append({'old': old, 'new': new, 'added': add, 'removed': rem,
                    'binary': bool(f.get('binary')), 'mode_only': bool(f.get('mode_only')),
                    'rename': bool(old and new and old != new)})
    return out, agree


# ----------------------------------------------------------------------------------------------------------------
# sqlite engine
DB = sqlite3.connect(':memory:')
DB.executescript('''
CREATE TABLE files(fid INTEGER, oldp TEXT, newp TEXT, added INTEGER, removed INTEGER, mode_only INTEGER);
CREATE TABLE segs(fid INTEGER, seg TEXT);
CREATE TABLE fnames(fid INTEGER, name TEXT);
CREATE TABLE cls(cname TEXT, kind TEXT, val TEXT);
CREATE TABLE areas(opt TEXT, folder TEXT);
CREATE VIEW infile AS
  SELECT DISTINCT fid, cname FROM (
    SELECT s.fid AS fid, c.cname AS cname FROM segs s JOIN cls c ON c.kind = 'F' AND s.seg = c.val
    UNION ALL
    SELECT n.fid, c.cname FROM fnames n JOIN cls c ON c.kind = 'P' AND n.name GLOB c.val);
''')


def load_files(files, classes=None):
    cur = DB.cursor()
    for t in ('files', 'segs', 'fnames', 'cls', 'areas'):
        cur.execute(f'DELETE FROM {t}')
    for i, f in enumerate(files):
        cur.execute('INSERT INTO files VALUES (?,?,?,?,?,?)',
                    (i, f['old'], f['new'], f['added'], f['removed'], int(f.get('mode_only', False))))
        for p in {f['old'], f['new']} - {None}:
            parts = p.split('/')
            for s in parts[:-1]:
                cur.execute('INSERT INTO segs VALUES (?,?)', (i, s.lower()))
            cur.execute('INSERT INTO fnames VALUES (?,?)', (i, parts[-1].lower()))
    for cname, (folders, pats) in (classes or {}).items():
        for v in folders:
            cur.execute('INSERT INTO cls VALUES (?,?,?)', (cname, 'F', v.lower()))
        for v in pats:
            cur.execute('INSERT INTO cls VALUES (?,?,?)', (cname, 'P', v.lower()))


def q(s):
    return "'" + s.replace("'", "''") + "'"


def sql1(expr):
    return DB.execute('SELECT ' + expr).fetchone()[0]


# ----------------------------------------------------------------------------------------------------------------
# class lists (SEM-08 printed lists)
CLS_RE = re.compile(r'([A-Za-z][A-Za-z ]*?) files: any file (.*)$')


def split_list(s):
    s = s.strip().rstrip('.')
    parts = []
    for chunk in s.split(', '):
        if ' or ' in chunk:
            parts.extend(chunk.split(' or '))
        else:
            parts.append(chunk)
    return [p.strip() for p in parts if p.strip()]


def parse_classes(text):
    classes = {}
    for raw in (text or '').split('\n'):
        l = clean(raw)
        m = CLS_RE.search(l)
        if not m:
            continue
        name, rest = m.group(1).strip(), m.group(2).strip()
        if rest.endswith('.'):
            rest = rest[:-1]
        folders, pats = [], []
        segs = rest.split('; or any file ')
        for sg in segs:
            sg = sg.strip()
            if sg.startswith('in a folder named '):
                folders = split_list(sg[len('in a folder named '):])
            elif sg.startswith('whose file name matches '):
                pats = split_list(sg[len('whose file name matches '):])
            else:
                raise ParseFail('class list segment: ' + name)
        classes[name] = (folders, pats)
    return classes


# ----------------------------------------------------------------------------------------------------------------
# atoms (gate 5.1, score RT4/RT5) -> SQL
CMP = {'more than': '>', 'at least': '>=', 'at most': '<=', 'fewer than': '<'}


def atom_sql(a, classes):
    a = a.strip().rstrip('.').strip()
    names = sorted(classes, key=len, reverse=True)
    def cl(x):
        for n in names:
            if x == n:
                return n
        raise ParseFail('unknown class ' + x)
    def anyc(c):
        return f'EXISTS(SELECT 1 FROM infile WHERE cname={q(c)})'
    m = re.fullmatch(r'any (.+?) file changes without any (.+?) file changing', a)
    if m:
        return f'({anyc(cl(m.group(1)))} AND NOT {anyc(cl(m.group(2)))})'
    m = re.fullmatch(r'any (.+?) file changes', a)
    if m:
        return anyc(cl(m.group(1)))
    m = re.fullmatch(r'the number of (.+?) is (more than|at least|at most|fewer than) (\d+)', a)
    if m:
        qty, op, t = m.group(1), CMP[m.group(2)], int(m.group(3))
        return f'({qty_sql(qty, classes)} {op} {t})'
    raise ParseFail('atom: ' + a[:60])


def qty_sql(qty, classes):
    names = sorted(classes, key=len, reverse=True)
    if qty in ('changed lines', 'lines changed'):
        return '(SELECT COALESCE(SUM(added+removed),0) FROM files)'
    if qty in ('changed files', 'files changed'):
        return '(SELECT COUNT(*) FROM files)'
    for n in names:
        if qty in (f'changed lines in {n} files', f'lines changed in {n} files'):
            return (f'(SELECT COALESCE(SUM(added+removed),0) FROM files WHERE fid IN '
                    f'(SELECT fid FROM infile WHERE cname={q(n)}))')
        if qty in (f'changed {n} files', f'{n} files changed'):
            return f'(SELECT COUNT(*) FROM files WHERE fid IN (SELECT fid FROM infile WHERE cname={q(n)}))'
    raise ParseFail('quantity: ' + qty)


def cond_sql(c, classes):
    """A condition: 'all of these are true: [1] ..; [2] ..' | 'any of these are true: ..' | atom [and|or atom]."""
    c = c.strip().rstrip('.').strip()
    m = re.match(r'(all|any) of these are true: (.*)$', c)
    if m:
        items = re.split(r'(?:^|;\s*)\[\d+\]\s*', m.group(2))
        items = [x.strip().rstrip(';').strip() for x in items if x.strip()]
        if len(items) < 2:
            raise ParseFail('list items')
        parts = [item_sql(x, classes) for x in items]
        return '(' + (' AND ' if m.group(1) == 'all' else ' OR ').join(parts) + ')'
    for j in (' and any ', ' or any '):
        if c.startswith('any ') and j in c:
            l, r = c.split(j, 1)
            return '(' + atom_sql(l, classes) + (' AND ' if 'and' in j else ' OR ') + atom_sql('any ' + r, classes) + ')'
    return atom_sql(c, classes)


def item_sql(x, classes):
    if x.startswith('(') and x.endswith(')'):
        return cond_sql(x[1:-1], classes)
    return cond_sql(x, classes) if re.match(r'(all|any) of these', x) else atom_sql(x, classes)


# ----------------------------------------------------------------------------------------------------------------
# frames (SEM-34, SEM-25, SEM-38): parse the frame question, count negations, assert vs negcount
NEG_SENT = 'it is not the case that '


def find_frame(instr, kind):
    sents = re.findall(r'[^?\n]*\?', instr or '')
    hits = []
    for s in sents:
        s0 = re.split(r'(?<=[.!])\s+', s.strip())[-1].strip()
        s1 = re.sub(r'^(?:Question|Q|The question to answer):\s*', '', s0)
        low = s1.lower()
        if kind == 'gate':
            if 'merge without review' in low:
                fr = 'pass'
            elif re.search(r'\bhold(s)?\b|\bheld\b', low) and 'rule' in low:
                fr = 'hold'
            else:
                continue
        else:
            if 'different change' in low or 'other change' in low:
                fr = 'other'
            elif 'describe' in low:
                fr = 'describes'
            else:
                continue
        hits.append((s1, fr))
    if not hits:
        raise ParseFail('no frame question')
    frs = {fr for _, fr in hits}
    if len(frs) > 1:
        raise ParseFail('two frames')
    # the framed question: the one with negations if any, else the last
    s1, fr = hits[-1]
    for h in hits:
        if h[0].lower().startswith('is it true that'):
            s1, fr = h
    low = s1.lower()
    own = 0
    if low.startswith('is it true that '):
        rest = low[len('is it true that '):]
        while rest.startswith(NEG_SENT):
            own += 1
            rest = rest[len(NEG_SENT):]
        own += len(re.findall(r'\b(does|do|is|was) not\b', rest))
    elif re.search(r'\bnot\b', low):
        raise ParseFail('negation outside truth frame')
    return fr, own, s1


# ----------------------------------------------------------------------------------------------------------------
# triage: character-scanner state machine for the 3.1 EBNF (no regex)
def is_ascii_letter(ch):
    return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')


def parse_header(msg):
    first = msg.split('\n', 1)[0]
    s = first
    n = len(s)
    state = 'TYPE'
    i = 0
    tstart = 0
    typ = scope = None
    bang = False
    while True:
        ch = s[i] if i < n else None
        if state == 'TYPE':
            if ch is not None and is_ascii_letter(ch):
                i += 1
                continue
            if i == tstart:
                return None
            typ = s[tstart:i].lower()
            if typ not in TYPES10:
                return None
            state = 'AFTER_TYPE'
            continue
        if state == 'AFTER_TYPE':
            if ch == '(':
                state = 'SCOPE'; i += 1; sstart = i
                continue
            state = 'BANG'
            continue
        if state == 'SCOPE':
            if ch is None or ch in '(:\n':
                return None
            if ch == ')':
                if i == sstart:
                    return None
                scope = s[sstart:i]; i += 1; state = 'BANG'
                continue
            i += 1
            continue
        if state == 'BANG':
            if ch == '!':
                bang = True; i += 1
            state = 'COLON'
            continue
        if state == 'COLON':
            if ch != ':':
                return None
            i += 1; state = 'SPACE1'
            continue
        if state == 'SPACE1':
            if ch != ' ':
                return None
            while i < n and s[i] == ' ':
                i += 1
            state = 'SUBJECT'
            continue
        if state == 'SUBJECT':
            subj = s[i:]
            if subj.strip(' ') == '':
                return None
            return {'type': typ, 'scope': scope, 'bang': bang, 'hlen': i, 'subject': subj}


# ----------------------------------------------------------------------------------------------------------------
# shown diff parsing (match, inverted gate)
def fences(state):
    """Return list of (start, end) line index pairs of ``` fenced blocks and the line list."""
    L = state.split('\n')
    out = []
    i = 0
    while i < len(L):
        if L[i].startswith('```'):
            j = i + 1
            while j < len(L) and not L[j].startswith('```'):
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out, L


def parse_diff(lines):
    """changed line texts (with marker) and header paths, from shown diff lines."""
    changed, paths = [], []
    files = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('--- ') and i + 1 < len(lines) and lines[i + 1].startswith('+++ '):
            a = l[4:].strip()
            b = lines[i + 1][4:].strip()
            pa = a[2:] if a.startswith('a/') else (None if a == '/dev/null' else a)
            pb = b[2:] if b.startswith('b/') else (None if b == '/dev/null' else b)
            for p in (pa, pb):
                if p:
                    paths.append(p)
            files.append({'old': pa, 'new': pb, 'added': 0, 'removed': 0})
            i += 2
            continue
        if l.startswith('+') or l.startswith('-'):
            changed.append(l)
            if files:
                files[-1]['added' if l[0] == '+' else 'removed'] += 1
        i += 1
    return changed, paths, files


# ----------------------------------------------------------------------------------------------------------------
# match: code names (6.1) and touched (SEM-25)
PUNCT = set(',;:!?()[]{}"\'')


def trim_word(w):
    used_dot = False
    while w and w[0] in PUNCT:
        w = w[1:]
    while w:
        if w[-1] in PUNCT:
            w = w[:-1]
        elif w[-1] == '.' and not used_dot:
            used_dot = True
            w = w[:-1]
        else:
            break
    return w


def code_names(msg):
    out = []
    for raw in msg.split():
        w = trim_word(raw)
        if len(w) >= 2 and w[0] == '`' and w[-1] == '`':
            inner = w[1:-1]
            if inner:
                out.append(inner)
            continue
        shaped = False
        for k, ch in enumerate(w):
            if ch in '/_':
                shaped = True; break
            if 'a' <= ch <= 'z' and k + 1 < len(w) and 'A' <= w[k + 1] <= 'Z':
                shaped = True; break
            if ch == '.' and 0 < k < len(w) - 1 and w[k - 1].isascii() and w[k - 1].isalnum() \
                    and w[k + 1].isascii() and w[k + 1].isalnum():
                shaped = True; break
        if shaped:
            out.append(w)
    return out


def is_word_char(ch):
    return ch.isascii() and (ch.isalnum() or ch == '_')


def touched(name, texts):
    nl = name.lower()
    for t in texts:
        tl = t.lower()
        start = 0
        while True:
            k = tl.find(nl, start)
            if k < 0:
                break
            before = tl[k - 1] if k > 0 else ''
            after = tl[k + len(nl)] if k + len(nl) < len(tl) else ''
            if not (before and is_word_char(before)) and not (after and is_word_char(after)):
                return True
            start = k + 1
    return False


def describes(msg, changed, paths):
    names = code_names(msg)
    if not names:
        raise ParseFail('message has no code name')
    texts = [c[1:] for c in changed] + paths
    return all(touched(n, texts) for n in names), names


# ----------------------------------------------------------------------------------------------------------------
class Solver:
    def __init__(self, recs):
        self.recs = recs
        self.tri_defs = defaultdict(dict)     # card_id -> def text -> type
        self.gate_hold = defaultdict(Counter)  # card_id -> rule value (0/1) on the record, before the frame
        self.tri_classes = None

    # ---------------- route (2.2, 2.4 B)
    def route(self, r, rec):
        files, agree = record_files(rec)
        if r['qtype'] == 'choice':
            defs = {}
            for l in lines_of(r['card']):
                m = re.match(r'^(.+?): files in the folder (\S+?): ', l)
                if m:
                    defs[m.group(1)] = m.group(2)
            opts = r['options']
            if set(opts) - set(defs):
                raise ParseFail('route option without definition')
            omap = {o: defs[o] for o in opts}
        else:
            omap = {}
            for l in lines_of(r['card']):
                m = re.match(r'^(.+?): files in the folder (\S+?): ', l)
                if m:
                    omap[m.group(1)] = m.group(2)
        # monorepo shift (2.1): the card names P ("Every area below is a folder inside the folder P.")
        mp = re.search(r'Every area below is a folder inside the folder (\S+?)\.(?:\s|$)',
                       r['instructions'] + '\n' + (r['card'] or ''))
        flags = []
        if mp:
            P = mp.group(1)
            for o, fo in list(omap.items()):
                top = [f for f in files if (f['new'] or f['old']).startswith(fo + '/')]
                if top:
                    flags.append('area_folder_outside_P(2.1 card text)')
                omap[o] = P + '/' + fo
        load_files(files)
        cur = DB.cursor()
        for o, fo in omap.items():
            cur.execute('INSERT INTO areas VALUES (?,?)', (o, fo))
        rows = DB.execute('''
            SELECT a.opt, SUM(f.added + f.removed) AS n FROM files f JOIN areas a
              ON substr(COALESCE(f.newp, f.oldp), 1, length(a.folder) + 1) = a.folder || '/'
            GROUP BY a.opt ORDER BY n DESC, a.opt''').fetchall()
        total = sql1('(SELECT COALESCE(SUM(added+removed),0) FROM files)')
        inarea = sum(n for _, n in rows)
        if not agree:
            flags.append('count_derivations_differ(1.2)')
        if inarea <= 0:
            return '<no offered area holds a changed line under the card text>', \
                '2.1/2.2 area folders as printed (monorepo P sentence)', flags
        top, ntop = rows[0]
        if ntop < 0.7 * inarea:
            flags.append('gold_share<70%(2.2)')
        if inarea < 0.8 * total:
            flags.append('in_area<80%(2.2)')
        # renames across areas (2.2)
        for f in files:
            if f['rename']:
                ao = [o for o, fo in omap.items() if f['old'].startswith(fo + '/')]
                an = [o for o, fo in omap.items() if f['new'].startswith(fo + '/')]
                if ao != an:
                    flags.append('rename_across_areas(2.2)')
        if r['qtype'] == 'choice':
            return top, '2.2 gold area', flags
        m = re.search(r'Is (\S+) the area this change mainly belongs to\?', r['instructions']) or \
            re.search(r'Does this change belong mainly to area (\S+)\?', r['instructions'])
        if not m:
            raise ParseFail('route per-label asked area')
        asked = m.group(1)
        if asked not in omap:
            raise ParseFail('asked area not on card')
        return (1 if omap[asked] == omap[top] else 0), '1.11/SEM-49 route per-label', flags

    # ---------------- triage (3.1-3.4)
    def triage_prepass(self, rows):
        for r in rows:
            if r['source'] != 'commit_triage':
                continue
            cid = r['meta']['card_id']
            if r['qtype'] == 'choice' and r['meta'].get('twin_kind') is None and set(r['options']) <= set(TYPES10):
                for l in (r['card'] or '').split('\n'):
                    l2 = clean(l)
                    if ': ' in l2:
                        o, d = l2.split(': ', 1)
                        if o in TYPES10:
                            self.tri_defs[cid].setdefault(d.strip(), set()).add(o)
            if r['qtype'] == 'noul':
                for l in (r['card'] or '').split('\n'):
                    l2 = clean(l)
                    if ': ' in l2:
                        o, d = l2.split(': ', 1)
                        if o in TYPES10:
                            self.tri_defs[cid].setdefault(d.strip(), set()).add(o)
            src = r['card'] if r['qtype'] == 'noul' else r['instructions']
            cl = parse_classes(src)
            if cl:
                key = json.dumps(cl, sort_keys=True)
                if self.tri_classes is None:
                    self.tri_classes = (key, cl)
                elif self.tri_classes[0] != key:
                    self.tri_class_conflict = True

    def triage(self, r, rec):
        h = parse_header(rec['msg'])
        if h is None:
            raise ParseFail('record message has no valid header')
        t = h['type']
        flags = []
        if parse_header(h['subject']) is not None:
            flags.append('subject_starts_with_header(3.1)')
        files, agree = record_files(rec)
        cl = self.tri_classes[1] if self.tri_classes else {}
        load_files(files, cl)
        nf = len(files)
        def allin(c):
            return sql1(f"(SELECT COUNT(DISTINCT fid) FROM infile WHERE cname={q(c)})") == nf and nf > 0
        def anyin(c):
            return sql1(f"EXISTS(SELECT 1 FROM infile WHERE cname={q(c)})")
        alls = {k: allin(c) for k, c in (('docs', 'docs'), ('test', 'test'), ('ci', 'CI')) if c in cl}
        for k, v in alls.items():
            if v and t != k:
                flags.append(f'all_{k}_but_gold_{t}(3.2)')
            if t == k and not v:
                flags.append(f'gold_{k}_not_all_{k}(3.2)')
        if sum(alls.values()) > 1:
            flags.append('two_all_rules(3.2)')
        if t == 'build' and 'build' in cl and not anyin('build'):
            flags.append('gold_build_no_build_file(3.2)')
        if any(f['mode_only'] for f in files):
            flags.append('mode_only_file(3.2)')
        for f in files:
            if f['rename']:
                load_files([{'old': f['old'], 'new': None, 'added': 0, 'removed': 0}], cl)
                a = {x[0] for x in DB.execute('SELECT cname FROM infile').fetchall()}
                load_files([{'old': None, 'new': f['new'], 'added': 0, 'removed': 0}], cl)
                b = {x[0] for x in DB.execute('SELECT cname FROM infile').fetchall()}
                if a != b:
                    flags.append('rename_cross_class(3.2)')
        # shown message must hold the stripped message start (3.2: header removed once)
        if h['subject'][:40].strip() and h['subject'][:40].strip().split()[0] not in r['state']:
            flags.append('stripped_subject_not_shown(3.2)')
        if rec['msg'].split('\n', 1)[0][:h['hlen']].strip() and \
                rec['msg'].split('\n', 1)[0] in r['state']:
            flags.append('header_not_stripped(3.2)')
        if r['qtype'] == 'noul':
            m = re.search(r'Was this change tagged (\w+) by its author\?', r['instructions']) or \
                re.search(r'Did the author tag this change as (\w+)\?', r['instructions'])
            if not m:
                raise ParseFail('triage per-label asked type')
            return (1 if m.group(1) == t else 0), '1.11/SEM-49 triage per-label', flags
        opts = r['options']
        named = set(opts) <= set(TYPES10) and r['meta'].get('twin_kind') != 'swapped_name'
        if named:
            return (t if t in opts else '<gold type not shown>'), '3.2 author tag', flags
        # masked / swapped: the definitions decide (SEM-27m, SEM-47)
        dmap = self.tri_defs.get(r['meta']['card_id'], {})
        best = []
        for l in (r['card'] or '').split('\n'):
            l2 = clean(l)
            if ': ' not in l2:
                continue
            o, d = l2.split(': ', 1)
            if o in opts:
                tys = dmap.get(d.strip())
                if tys is None:
                    raise ParseFail('definition not on the card text')
                if len(tys) != 1:
                    raise ParseFail('definition maps to two types')
                if t in tys:
                    best.append(o)
        if len(best) != 1:
            raise ParseFail('masked/swapped: %d options carry the gold definition' % len(best))
        return best[0], '3.2 author tag via definition (SEM-27m/47)', flags

    # ---------------- score (4.1-4.4)
    def score(self, r, rec):
        files, agree = record_files(rec)
        text = r['instructions'] + '\n' + (r['card'] or '')
        classes = parse_classes(text)
        load_files(files, classes)
        flags = [] if agree else ['count_derivations_differ(1.2)']
        opts = r['options']
        lv = {}
        for o in opts:
            m = re.match(r'^Level (\d+)(?: - .+)?$', o)
            if not m:
                raise ParseFail('level option text')
            lv[int(m.group(1))] = o
        K = len(opts)
        if sorted(lv) != list(range(1, K + 1)):
            raise ParseFail('levels not 1..K')
        L = lines_of(text)
        def band(desc):
            desc = desc.strip().rstrip('.;').strip()
            m = re.fullmatch(r'(.+?) from (\d+) up to (\d+)', desc)
            if m:
                qs = self.band_qty(m.group(1), classes)
                return f'({qs} >= {int(m.group(2))} AND {qs} < {int(m.group(3))})'
            m = re.fullmatch(r'(.+?) (\d+) or more', desc)
            if m:
                qs = self.band_qty(m.group(1), classes)
                return f'({qs} >= {int(m.group(2))})'
            raise ParseFail('band: ' + desc[:40])
        dl = [l for l in L if l.startswith('Decision list')]
        st = [l for l in L if l.startswith('Size table:')]
        pt = [l for l in L if l.startswith('Points table:')]
        rl = [l for l in L if l.startswith('Raise list:')]
        fl = [l for l in L if l.startswith('Class floor:')]
        card_lines = {}
        for l in lines_of(r['card']):
            m = re.match(r'^Level (\d+)(?: - [^:]+)?: (.+)$', l)
            if m:
                card_lines[int(m.group(1))] = m.group(2)
        preds = {}
        if dl:
            body = dl[0].split(':', 1)[1].strip()
            parts = re.split(r'(?<=\.)\s+(?=Level \d+ )', body)
            prev = []
            tmpl = 'RT4'
            for p in parts:
                m = re.fullmatch(r'Level (\d+) if (.+)\.', p.strip())
                m2 = re.fullmatch(r'Level (\d+) otherwise\.?', p.strip())
                if m:
                    c = cond_sql(m.group(2), classes)
                    preds[int(m.group(1))] = '(' + ' AND '.join([c] + [f'NOT {x}' for x in prev]) + ')'
                    prev.append(c)
                elif m2:
                    preds[int(m2.group(1))] = '(' + (' AND '.join(f'NOT {x}' for x in prev) or '1') + ')'
                else:
                    raise ParseFail('decision line')
        elif st:
            body = st[0].split(':', 1)[1]
            size = {}
            for seg in body.split(';'):
                m = re.match(r'\s*size level (\d+): (.+)$', seg.strip())
                if not m:
                    raise ParseFail('size table')
                size[int(m.group(1))] = band(m.group(2))
            nsize = sql1('(' + ' + '.join(f'({p})' for p in size.values()) + ')')
            if nsize != 1:
                raise ParseFail('size bands: %d true' % nsize)
            size_expr = 'CASE ' + ' '.join(f'WHEN {p} THEN {k}' for k, p in size.items()) + ' END'
            if rl and not fl:
                tmpl = 'RT2'
                names = split_list(rl[0].rsplit(':', 1)[1].replace(' and ', ', '))
                for n in names:
                    if n not in classes:
                        raise ParseFail('raise class')
                R = ' + '.join(f'(EXISTS(SELECT 1 FROM infile WHERE cname={q(n)}))' for n in names) or '0'
                final = f'MIN({K}, ({size_expr}) + {R})'
            elif fl and not rl:
                tmpl = 'RT3'
                terms = [f'({size_expr})']
                for l in fl:
                    m = re.fullmatch(r'Class floor: if any (.+?) file changes, the level is at least Level (\d+)\.?', l)
                    if not m or m.group(1) not in classes:
                        raise ParseFail('class floor')
                    terms.append(f'(CASE WHEN EXISTS(SELECT 1 FROM infile WHERE cname={q(m.group(1))}) '
                                 f'THEN {int(m.group(2))} ELSE 0 END)')
                final = 'MAX(' + ', '.join(terms) + ')' if len(terms) > 1 else terms[0]
            else:
                raise ParseFail('size table without exactly one of raise/floor')
            for k in range(1, K + 1):
                preds[k] = f'(({final}) = {k})'
        elif pt:
            tmpl = 'RT5'
            body = pt[0].split(':', 1)[1].strip().rstrip('.')
            cls_terms, size_terms = [], []
            for seg in body.split(';'):
                seg = seg.strip()
                m = re.fullmatch(r'(.+): (\d+) points?( per file)?', seg)
                if not m:
                    raise ParseFail('points line')
                what, pts, perfile = m.group(1), int(m.group(2)), m.group(3)
                m2 = re.fullmatch(r'any (.+?) file changes', what)
                if m2:
                    c = m2.group(1)
                    if c not in classes:
                        raise ParseFail('points class')
                    if perfile:
                        cls_terms.append(f'({pts} * (SELECT COUNT(*) FROM files WHERE fid IN '
                                         f'(SELECT fid FROM infile WHERE cname={q(c)})))')
                    else:
                        cls_terms.append(f'(CASE WHEN EXISTS(SELECT 1 FROM infile WHERE cname={q(c)}) '
                                         f'THEN {pts} ELSE 0 END)')
                else:
                    size_terms.append((band(what), pts))
            nb = sql1('(' + ' + '.join(f'({b})' for b, _ in size_terms) + ')')
            if nb != 1:
                raise ParseFail('points size lines: %d true' % nb)
            P = '(' + ' + '.join(cls_terms + [f'(CASE WHEN {b} THEN {p} ELSE 0 END)' for b, p in size_terms]) + ')'
            for k in range(1, K + 1):
                if k not in card_lines:
                    raise ParseFail('RT5 card line missing')
                d = card_lines[k].strip()
                m = re.fullmatch(r'points from (\d+) up to (\d+)', d)
                m2 = re.fullmatch(r'points (\d+) or more', d)
                if m:
                    preds[k] = f'({P} >= {int(m.group(1))} AND {P} < {int(m.group(2))})'
                elif m2:
                    preds[k] = f'({P} >= {int(m2.group(1))})'
                else:
                    raise ParseFail('RT5 level range')
        else:
            tmpl = 'RT1'
            for k in range(1, K + 1):
                if k not in card_lines:
                    raise ParseFail('RT1 card line missing')
                preds[k] = band(card_lines[k])
        if sorted(preds) != list(range(1, K + 1)):
            raise ParseFail('levels without predicate')
        sql = 'SELECT ' + ', '.join(f'CASE WHEN {preds[k]} THEN 1 ELSE 0 END' for k in range(1, K + 1))
        vals = DB.execute(sql).fetchone()
        true = [k for k, v in zip(range(1, K + 1), vals) if v]
        if len(true) != 1:
            raise ParseFail(f'{tmpl}: {len(true)} levels true')
        return lv[true[0]], f'4.2 {tmpl}', flags

    def band_qty(self, s, classes):
        s = s.strip()
        return qty_sql(s, classes)

    # ---------------- gate (5.1, 5.2, 5.6)
    def gate_rule(self, text):
        classes = parse_classes(text)
        L = lines_of(text)
        rule = exc = guard = None
        for l in L:
            k = l.find('the rule holds a change if ')
            if k >= 0 and rule is None:
                rule = l[k + len('the rule holds a change if '):]
            m = re.match(r'^Exception: this rule does not hold the change if (.+)$', l)
            if m:
                if exc is not None:
                    raise ParseFail('two exceptions')
                exc = m.group(1)
            m = re.match(r'^This rule applies only if (.+)$', l)
            if m:
                if guard is not None:
                    raise ParseFail('two guards')
                guard = m.group(1)
        if rule is None:
            raise ParseFail('no rule sentence')
        # exception / guard may share the rule's line
        for pat, nm in ((r'\s*Exception: this rule does not hold the change if .*$', 'e'),
                        (r'\s*This rule applies only if .*$', 'g')):
            rule = re.sub(pat, '', rule)
        expr = cond_sql(rule, classes)
        if exc is not None:
            expr = f'({expr} AND NOT {atom_sql(exc, classes)})'
        if guard is not None:
            expr = f'({expr} AND {atom_sql(guard, classes)})'
        return expr, classes

    def gate(self, r, rec):
        flags = []
        if r['qtype'] == 'choice':
            expr, classes = self.gate_rule(r['instructions'])
            fz, L = fences(r['state'])
            opts = r['options']
            held = []
            for o in opts:
                # the case's diff block follows a line naming '<ref> diff'
                blk = None
                for (a, b) in fz:
                    head = [clean(x) for x in L[max(0, a - 3):a] if x.strip()]
                    if head and re.fullmatch(re.escape(o) + r'\s*diff:?', head[-1].strip('*#: ')) is not None:
                        blk = (a, b)
                    elif head and head[-1].rstrip(':').strip('*# ') in (o + ' diff', o):
                        blk = (a, b)
                if blk is None:
                    raise ParseFail('inverted gate: no diff block for a case')
                _, _, files = parse_diff(L[blk[0] + 1:blk[1]])
                for f in files:
                    f['rename'] = bool(f['old'] and f['new'] and f['old'] != f['new'])
                load_files(files, classes)
                if sql1(expr):
                    held.append(o)
            if len(held) != 1:
                raise ParseFail(f'inverted gate: {len(held)} cases held')
            return held[0], 'SEM-44 inverted gate', flags
        files, agree = record_files(rec)
        if not agree:
            flags.append('count_derivations_differ(1.2)')
        expr, classes = self.gate_rule(r['card'])
        load_files(files, classes)
        hold = bool(sql1(expr))
        fr, own, qs = find_frame(r['instructions'], 'gate')
        ks = negcount.k_syn(qs)
        if ks != own:
            raise ParseFail(f'k_syn {ks} != template negations {own}')
        ans = hold if fr == 'hold' else (not hold)
        if own % 2:
            ans = not ans
        self.gate_hold[r['meta']['card_id']][int(hold)] += 1
        return int(ans), f'5.2 rule; frame {fr}; neg {own}', flags

    # ---------------- match (6.1, 6.2, 6.4)
    def match(self, r):
        fz, L = fences(r['state'])
        diffs = [(a, b) for a, b in fz if any(x.startswith('--- ') for x in L[a + 1:b])]
        if len(diffs) != 1:
            raise ParseFail('match: %d diff blocks' % len(diffs))
        a, b = diffs[0]
        changed, paths, _ = parse_diff(L[a + 1:b])
        outside = [x for i, x in enumerate(L) if not (a <= i <= b)]
        if r['qtype'] == 'noul':
            d, names = describes('\n'.join(outside), changed, paths)
            fr, own, qs = find_frame(r['instructions'], 'match')
            ks = negcount.k_syn(qs)
            if ks != own:
                raise ParseFail(f'k_syn {ks} != template negations {own}')
            ans = d if fr == 'describes' else (not d)
            if own % 2:
                ans = not ans
            return int(ans), f'6.2 SEM-25; frame {fr}; neg {own}', []
        opts = r['options']
        # split the non-diff text into messages by reference lines
        cur = None
        msgs = {o: [] for o in opts}
        lowopt = {o.lower(): o for o in opts}
        for x in outside:
            c = re.sub(r'^[^A-Za-z0-9]+|[^A-Za-z0-9]+$', '', clean(x))
            c = re.sub(r'^\d+[.)]?\s+', '', c)
            c = re.sub(r'^[^A-Za-z0-9]+|[^A-Za-z0-9]+$', '', c)
            if c.lower() in lowopt:
                cur = lowopt[c.lower()]
                continue
            if cur is not None:
                msgs[cur].append(x)
        if any(not v for v in msgs.values()):
            raise ParseFail('inverted match: case without message')
        good = []
        for o in opts:
            d, _ = describes('\n'.join(msgs[o]), changed, paths)
            if d:
                good.append(o)
        if len(good) != 1:
            raise ParseFail(f'inverted match: {len(good)} messages describe the diff')
        return good[0], 'SEM-26 inverted match', []


# ----------------------------------------------------------------------------------------------------------------
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''):
            h.update(ch)
    return h.hexdigest()


def main():
    t0 = time.time()
    rows = []
    for fn in OUTS:
        with open(os.path.join(FAM, 'out', fn + '.jsonl')) as f:
            for line in f:
                r = json.loads(line)
                r['_file'] = fn
                rows.append(r)
    need = {(r['meta'].get('text_source') or {}).get('record_id') for r in rows} - {None}
    recs = {}
    src = REC_CACHE if os.path.exists(REC_CACHE) else POOL
    with gzip.open(src, 'rt') as f:
        for line in f:
            k = line.find('"rid": "')
            rid = line[k + 8:line.find('"', k + 8)]
            if rid in need:
                recs[rid] = json.loads(line)
    missing = need - set(recs)
    if missing and src == REC_CACHE:
        with gzip.open(POOL, 'rt') as f:
            for line in f:
                k = line.find('"rid": "')
                rid = line[k + 8:line.find('"', k + 8)]
                if rid in missing:
                    recs[rid] = json.loads(line)
    S = Solver(recs)
    S.triage_prepass(rows)
    res = {'by_type': defaultdict(Counter), 'by_file': defaultdict(Counter), 'by_item': Counter()}
    mism, pfail, flagged = [], [], []
    for r in rows:
        typ = r['source'].replace('commit_', '')
        rid = (r['meta'].get('text_source') or {}).get('record_id')
        rec = recs.get(rid)
        try:
            if typ != 'match' and rec is None:
                raise ParseFail('record not found')
            b, item, flags = getattr(S, typ)(r, rec) if typ != 'match' else S.match(r)
        except ParseFail as e:
            res['by_type'][typ]['parse_fail'] += 1
            res['by_file'][r['_file']]['parse_fail'] += 1
            pfail.append({'id': r['id'], 'file': r['_file'], 'type': typ, 'gold_A': r['gold'], 'gold_B': None,
                          'spec_item': 'parse', 'detail': str(e)[:120]})
            continue
        res['by_type'][typ]['rows'] += 1
        res['by_item'][re.sub(r'; neg \d', '', item)] += 1
        res['by_file'][r['_file']]['rows'] += 1
        if b != r['gold']:
            res['by_type'][typ]['mismatch'] += 1
            res['by_file'][r['_file']]['mismatch'] += 1
            mism.append({'id': r['id'], 'card_id': r['meta']['card_id'], 'file': r['_file'], 'type': typ,
                         'qtype': r['qtype'],
                         'view': r['meta'].get('input_view'), 'twin_kind': r['meta'].get('twin_kind'),
                         'gold_A': r['gold'], 'gold_B': b, 'spec_item': item})
        else:
            res['by_type'][typ]['agree'] += 1
        if flags:
            res['by_type'][typ]['eligibility_flag'] += 1
            flagged.append({'id': r['id'], 'file': r['_file'], 'type': typ, 'flags': flags})
    n = len(rows)
    out = {
        'gate': 'G2', 'family': 'COMMIT', 'solver': 'c_src/COMMIT/solverB/solver_b.py',
        'solver_sha256': sha(os.path.abspath(__file__)),
        'spec': {'file': 'c_src/COMMIT/G0_SPEC.md', 'sha256': sha(os.path.join(FAM, 'G0_SPEC.md'))},
        'inputs': {fn: sha(os.path.join(FAM, 'out', fn + '.jsonl')) for fn in OUTS},
        'independence': 'written from G0 spec + row format only; reads no gen/*.py, qc/*.py, sidecar or solver A '
                        'field; record pool used only for raw message/paths/hunks (counts re-derived)',
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'rows_total': n, 'rows_checked': n - len(pfail),
        'mismatches_n': len(mism), 'parse_fail_n': len(pfail), 'eligibility_flag_n': len(flagged),
        'by_type': {k: dict(v) for k, v in res['by_type'].items()},
        'by_file': {k: dict(v) for k, v in res['by_file'].items()},
        'eligibility_flag_counts': dict(Counter(f for x in flagged for f in x['flags'])),
        'by_spec_item': dict(res['by_item']),
        'gate_rule_value_by_card': {k: {'holds': v[1], 'not_held': v[0]} for k, v in sorted(S.gate_hold.items())},
        'gate_cards_rule_never_holds': sorted(k for k, v in S.gate_hold.items() if v[1] == 0),
        'gate_cards_rule_always_holds': sorted(k for k, v in S.gate_hold.items() if v[0] == 0),
        'mismatch_by_card': dict(Counter(x['card_id'] for x in mism)),
        'mismatch_by_item': dict(Counter(x['spec_item'] for x in mism)),
        'mismatches': mism, 'parse_fail': pfail, 'eligibility_flags': flagged,
        'secs': round(time.time() - t0, 1),
    }
    with open(os.path.join(HERE, 'mismatch.json'), 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in ('rows_total', 'rows_checked', 'mismatches_n', 'parse_fail_n',
                                          'eligibility_flag_n', 'by_type', 'secs')}))
    print('SOLVER_B_DONE')


if __name__ == '__main__':
    main()
