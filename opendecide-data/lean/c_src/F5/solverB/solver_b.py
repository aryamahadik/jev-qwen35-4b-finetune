#!/usr/bin/env python3
"""F5 independent solver B (written from c_src/F5/G0_SPEC.md and the row format only).

Paradigm: parse the RENDERED row (card, state, instructions) back into facts, then re-derive gold by
  * S1 / S3: model enumeration (truth tables over every ground atom; closed cards add Clark completion,
    open cards keep every model of the parsed theory) -> gold = LF true in all models / false in all models;
  * S4: sqlite tables built from the parsed record container, LF compiled to SQL (COUNT / EXISTS);
  * S2: backward version-graph resolver (CORRECTION / VOID pointers followed from the query) over the parsed log;
  * S5: constraint check over the parsed thread (latest remaining statement per party and fact).
It never imports or reads the generator (c_src/F5/gen/) nor the generator's sidecars for labelling.
Output: solverB/mismatch.json (ids, both answers, spec item; no row text) and solverB/report.json.
"""
import json, re, sys, os, html, itertools, sqlite3, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'out')
FILES = ['candidates_r1.jsonl', 'qc_sample.jsonl', 'mixdev_S5.jsonl']


class Unparsed(Exception):
    """Solver B could not parse a part of the row (reported separately from mismatches)."""


class Undetermined(Exception):
    """KB + LF and KB + not-LF both satisfiable (or both unsat): spec section 2 item 5."""


# ---------------------------------------------------------------- question extraction
_LEAD = [r"What's the answer\?\s*", r"(?:Q|Question|The question to answer):\s*"]


def extract_question(instr):
    i = instr.rfind('?')
    if i < 0:
        raise Unparsed('no question mark')
    pre = instr[:i + 1]
    parts = re.split(r'(?:(?<=[.!])\s+|\n+)', pre)
    q = parts[-1].strip()
    changed = True
    while changed:
        changed = False
        for p in _LEAD:
            m = re.match(p, q)
            if m and m.end() < len(q):
                q = q[m.end():]
                changed = True
    return q


# ---------------------------------------------------------------- card facts
def card_world(card):
    # open-world line (SEM-03) says unstated facts are "unknown, not false"; the closed line never says unknown
    return 'open' if re.search(r'\bunknown\b', card, re.I) else 'closed'


def card_graded(card):
    """SEM-25 constants: <q> (hardly any / scarcely any / few = fewer than q) and <m> (barely)."""
    q = m = None
    mm = re.search(r'fewer than (\d+)\b', card[card.find('ardly any'):] if 'ardly any' in card else '')
    if mm:
        q = int(mm.group(1))
    mb = re.search(r'no more than (\d+(?:\.\d+)?) above', card)
    if mb:
        m = float(mb.group(1))
    return q, m


def card_valuesets(card):
    """SEM-17: attribute -> list of values (one line per value-set attribute)."""
    out = {}
    for mm in re.finditer(r'exactly one ([^,\n]+?)(?: at a time)?, one of: ([^\n]+?)\.(?:\s|$)', card):
        attr = mm.group(1).strip()
        vals = [v.strip() for v in re.split(r',\s*', mm.group(2))]
        vals = [re.sub(r'^(?:and|or)\s+', '', v) for v in vals]
        out[attr] = vals
    return out


def card_period(card):
    mm = re.search(r'covers (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', card)
    if mm:
        return D(mm.group(1)), D(mm.group(2))
    return None


def card_authority(card):
    mm = re.search(r'no named author are records by ([^.\n]+?)\.', card)
    if mm:
        return mm.group(1).strip()
    mm = re.search(r'Statements by ([^;.\n]+?) are true', card)
    if mm:
        return mm.group(1).strip()
    mm = re.search(r"Only ([^.\n]+?)'s messages make facts", card)
    if mm:
        return mm.group(1).strip()
    return None


def D(s):
    return datetime.date.fromisoformat(s)


def card_types(card):
    """Entity types the world line declares ('names every <type> [and every <type>] in the case')."""
    out = []
    for mm in re.finditer(r'names every (.+?) in the case', card):
        for t in re.split(r',? and every |, every ', mm.group(1)):
            t = t.strip().lower()
            if t and t != 'person' and t not in out:
                out.append(t)
    return out


# ---------------------------------------------------------------- generic state flattening
def _clean_markup(state):
    s = re.sub(r'```[A-Za-z]*', '\n', state)
    s = re.sub(r'<[^>]+>', '\n', s)
    s = html.unescape(s)
    s = s.replace('\\"', '"')
    return s


_SENT = re.compile(r"(?:(?<=^)|(?<=[\s\"'|>{(\[:,=*•-]))((?:[ERM]\d{1,3}\.\s+)?[A-Z][^\n\"|{}\[\]]*?\.)(?=[\s\"'|<}\],]|$)")


def prose_sentences(state):
    """All program-written sentences of a prose record (rules, facts, log entries, messages), in listed order.
    A sentence starts with a capital letter (optionally after an R1./E01./M01. label) and ends with a period that
    is not inside a number."""
    s = _clean_markup(state)
    out = []
    for line in s.split('\n'):
        line = line.strip()
        if not line:
            continue
        for mm in _SENT.finditer(line):
            t = mm.group(1).strip()
            # a period inside a decimal number does not end a sentence: _SENT requires whitespace/end after it
            out.append(t)
    return out


# ---------------------------------------------------------------- question frames (SEM-01; C2)
_SUFFIX = re.compile(r',?\s+(?:going by the text|according to the record|on the facts given|based on the record|'
                     r'based on the text|taking the record as given|from the record)$')
_ID_FRAMES = [
    r'Is it true that (?P<x>.+)',
    r'Is it the case that (?P<x>.+)',
    r'Is the statement that (?P<x>.+) true',
    r'Is this assertion true: (?P<x>.+)',
    r'Is the following statement true: (?P<x>.+)',
    r'Do the facts given establish that (?P<x>.+)',
    r'Does the record show that (?P<x>.+)',
    r'(?:Based on the (?:text|record)|Taking the record as given|According to the record|Going by the text|'
    r'On the facts given),? is it (?:true|the case) that (?P<x>.+)',
]
_NEG_FRAMES = [r'Is it false that (?P<x>.+)',
               r'(?:Based on the (?:text|record)|Taking the record as given|According to the record),? is it false that (?P<x>.+)']


def strip_frames(q):
    """Returns (n_outer_not, body, direct) where body is the embedded declarative (direct=False) or the
    direct interrogative without '?' (direct=True)."""
    q = q.strip()
    if q.endswith('?'):
        q = q[:-1]
    q = _SUFFIX.sub('', q)
    for f in _NEG_FRAMES:
        m = re.fullmatch(f, q)
        if m:
            return 1, m.group('x'), False
    for f in _ID_FRAMES:
        m = re.fullmatch(f, q)
        if m:
            return 0, m.group('x'), False
    return 0, q, True


def strip_embedded_neg(x):
    """C2 frames inside the declarative: 'it is not the case that', 'it is false that' (each = NOT)."""
    n = 0
    while True:
        m = re.match(r'(?:it is not the case that|it is false that) ', x)
        if not m:
            return n, x
        n += 1
        x = x[m.end():]


# ---------------------------------------------------------------- propositional engine (model enumeration)
# formulas: True / False / ('atom', key) / ('not', f) / ('and', [f...]) / ('or', [f...]) / ('iff', f, g)
#           / ('atleast', k, [f...]) / ('exactly', k, [f...])
def A(key):
    return ('atom', key)


def NOT(f):
    if f is True:
        return False
    if f is False:
        return True
    if f[0] == 'not':
        return f[1]
    return ('not', f)


def AND(*fs):
    fs = [f for f in fs if f is not True]
    if any(f is False for f in fs):
        return False
    if not fs:
        return True
    return fs[0] if len(fs) == 1 else ('and', fs)


def OR(*fs):
    fs = [f for f in fs if f is not False]
    if any(f is True for f in fs):
        return True
    if not fs:
        return False
    return fs[0] if len(fs) == 1 else ('or', fs)


def IMP(a, b):
    return OR(NOT(a), b)


def IFF(a, b):
    return ('iff', a, b)


def kleene(f, m):
    """Three-valued evaluation under a partial model m (dict atom -> bool)."""
    if f is True or f is False:
        return f
    t = f[0]
    if t == 'atom':
        return m.get(f[1])
    if t == 'not':
        v = kleene(f[1], m)
        return None if v is None else (not v)
    if t == 'and':
        unk = False
        for g in f[1]:
            v = kleene(g, m)
            if v is False:
                return False
            if v is None:
                unk = True
        return None if unk else True
    if t == 'or':
        unk = False
        for g in f[1]:
            v = kleene(g, m)
            if v is True:
                return True
            if v is None:
                unk = True
        return None if unk else False
    if t == 'iff':
        a, b = kleene(f[1], m), kleene(f[2], m)
        return None if a is None or b is None else (a == b)
    if t in ('atleast', 'exactly'):
        k = f[1]
        vals = [kleene(g, m) for g in f[2]]
        nt = sum(1 for v in vals if v is True)
        nu = sum(1 for v in vals if v is None)
        if t == 'atleast':
            if nt >= k:
                return True
            if nt + nu < k:
                return False
            return None
        if nt > k or nt + nu < k:
            return False
        return True if nu == 0 else None
    raise ValueError(t)


def atoms_of(f, acc=None):
    acc = set() if acc is None else acc
    if f is True or f is False:
        return acc
    if f[0] == 'atom':
        acc.add(f[1])
    elif f[0] == 'not':
        atoms_of(f[1], acc)
    elif f[0] in ('and', 'or'):
        for g in f[1]:
            atoms_of(g, acc)
    elif f[0] == 'iff':
        atoms_of(f[1], acc)
        atoms_of(f[2], acc)
    else:
        for g in f[2]:
            atoms_of(g, acc)
    return acc


def _component(constraints, seed_atoms):
    """Constraints and atoms connected to the seed atoms (other parts of the theory cannot change the goal)."""
    cat = [atoms_of(c) for c in constraints]
    atoms = set(seed_atoms)
    used = [False] * len(constraints)
    changed = True
    while changed:
        changed = False
        for i, s in enumerate(cat):
            if not used[i] and (s & atoms):
                used[i] = True
                atoms |= s
                changed = True
    return [c for i, c in enumerate(constraints) if used[i]], atoms


def satisfiable(constraints, goal=True):
    """Backtracking model search with three-valued pruning. True iff some total model satisfies all."""
    cons, atoms = _component(constraints, atoms_of(goal))
    cons = cons + [goal]
    occ = collections.defaultdict(list)
    for c in cons:
        for a in atoms_of(c):
            occ[a].append(c)
    order = sorted(atoms, key=lambda a: -len(occ[a]))
    m = {}
    for c in cons:
        if kleene(c, m) is False:
            return False

    def rec(i):
        if i == len(order):
            return True
        a = order[i]
        for val in (True, False):
            m[a] = val
            if all(kleene(c, m) is not False for c in occ[a]) and rec(i + 1):
                return True
        del m[a]
        return False
    return rec(0)


def consistent(constraints):
    """Whole-theory satisfiability, component by component."""
    left = list(constraints)
    while left:
        comp, _ = _component(left, atoms_of(left[0]))
        if not comp:
            comp = [left[0]]
        if not satisfiable(comp[1:], comp[0]):
            return False
        ids = set(map(id, comp))
        left = [c for c in left if id(c) not in ids]
    return True


def decide(constraints, lf):
    """Gold by determinacy (spec section 2): Yes iff KB & not-LF unsat, No iff KB & LF unsat."""
    pos = satisfiable(constraints, lf)
    neg = satisfiable(constraints, NOT(lf))
    if pos and not neg:
        return 1
    if neg and not pos:
        return 0
    raise Undetermined('undetermined' if pos else 'inconsistent')


# ---------------------------------------------------------------- shared lexical layer (S1, S3, S5)
IDRE = r'[A-Z][A-Z0-9]{0,5}-\d{2,6}'
ENTRE = r'(?P<type>[A-Za-z][a-z-]*(?: [a-z-]+)*?) (?P<id>' + IDRE + r')'


def card_affixes(card):
    """SEM-18 lines: affixed word -> its base word (affixed = exactly 'not base')."""
    out = {}
    for mm in re.finditer(r'"([^"]+)" has two states only[:,]?(?: and)? "([^"]+)" means exactly "not ([^"]+)"', card):
        base, aff, base2 = mm.groups()
        if base2.strip() == base.strip():
            out[aff.strip()] = base.strip()
    return out


class Lex:
    def __init__(self, card):
        self.affix = card_affixes(card)
        types = card_types(card)
        self.ENT = (r'(?P<type>(?i:' + '|'.join(re.escape(t) for t in sorted(types, key=len, reverse=True)) + r')) (?P<id>'
                    + IDRE + r')') if types else ENTRE

    def adj(self, ent, word):
        """Atom for '<ent> is <word>'; an affixed word is the negation of its base (SEM-18)."""
        word = word.strip()
        m = re.fullmatch(r'among the cases that are (.+)', word)
        if m:
            word = m.group(1).strip()
        if word in self.affix:
            return NOT(A(('p', ent, self.affix[word])))
        return A(('p', ent, word))

    def has(self, ent, noun):
        noun = re.sub(r'^(?:an?|the) ', '', noun.strip())
        return A(('h', ent, noun))

    def pred(self, ent, s):
        """A predicate phrase after 'is' (or a bare 'has a Z' phrase) inside neither/nor or not only/but also."""
        s = s.strip()
        m = re.fullmatch(r'(?:has|have) (.+)', s)
        if m:
            return self.has(ent, m.group(1))
        m = re.fullmatch(r'(?:is |are )?(?:without|free of) (.+)', s)
        if m:
            return NOT(self.has(ent, m.group(1)))
        m = re.fullmatch(r'(?:is |are )?not (.+)', s)
        if m:
            return NOT(self.pred(ent, m.group(1)))
        m = re.fullmatch(r'(?:is|are) (.+)', s)
        if m:
            s = m.group(1)
        return self.adj(ent, s)

    def vp(self, ent, vp):
        """Verb phrase of a clause whose subject is <ent>. Returns a formula."""
        vp = vp.strip().rstrip('.')
        m = re.fullmatch(r'(?:is|are) not only (.+?) but also (.+)', vp)
        if m:
            return AND(self.pred(ent, m.group(1)), self.pred(ent, m.group(2)))
        m = re.fullmatch(r'(?:is|are) neither (.+?) nor (.+)', vp)
        if m:
            return AND(NOT(self.pred(ent, m.group(1))), NOT(self.pred(ent, m.group(2))))
        m = re.fullmatch(r'neither (.+?) nor (.+)', vp)
        if m:
            return AND(NOT(self.pred(ent, m.group(1))), NOT(self.pred(ent, m.group(2))))
        m = re.fullmatch(r'(?:does|do) not (?:lack|have no) (.+)', vp)
        if m:
            return self.has(ent, m.group(1))
        m = re.fullmatch(r'(?:does not have|do not have|lacks|lack|is without|are without|is free of|are free of) (.+)', vp)
        if m:
            return NOT(self.has(ent, m.group(1)))
        m = re.fullmatch(r'(?:has|have) (.+)', vp)
        if m:
            return self.has(ent, m.group(1))
        m = re.fullmatch(r'(?:is|are) not (.+)', vp)
        if m:
            return NOT(self.pred(ent, m.group(1)))
        m = re.fullmatch(r'(?:is|are) (.+)', vp)
        if m:
            return self.pred(ent, m.group(1))
        raise Unparsed('vp')


def literals(f):
    """Split a conjunction of literals into a list of literals."""
    if isinstance(f, tuple) and f[0] == 'and':
        out = []
        for g in f[1]:
            out += literals(g)
        return out
    return [f]


class KB:
    """Rules (body -> head literal), stated facts, and world-independent definitions."""

    def __init__(self, world):
        self.world = world
        self.rules = []      # (body formula, head literal)
        self.facts = []      # literals
        self.defs = []       # constraints in both worlds (deontic closure, domain axioms)
        self.defined = set() # atoms defined by self.defs (no completion for them)

    def add_rule(self, body, head):
        for lit in literals(head):
            self.rules.append((body, lit))

    def add_fact(self, f):
        self.facts += literals(f)

    def constraints(self, lf):
        cons = list(self.defs)
        if self.world == 'open':
            cons += [IMP(b, h) for b, h in self.rules]
            cons += list(self.facts)
            return cons
        support = collections.defaultdict(list)
        for b, h in self.rules:
            if h[0] == 'atom':
                support[h[1]].append(b)
            else:
                cons.append(IMP(b, h))
        for f in self.facts:
            if f is True or f is False:
                cons.append(f)
            elif f[0] == 'atom':
                support[f[1]].append(True)
            else:
                cons.append(f)
        allatoms = set()
        for c in cons:
            atoms_of(c, allatoms)
        for b, h in self.rules:
            atoms_of(b, allatoms)
            atoms_of(h, allatoms)
        atoms_of(lf, allatoms)
        allatoms |= set(support)
        for a in allatoms:
            if a in self.defined or a[0] == 'cmp':
                continue
            cons.append(IFF(A(a), OR(*support.get(a, []))))
        return cons

    def decide(self, lf):
        return decide(self.constraints(lf), lf)


def _sing(t):
    t = t.strip().lower()
    return t


def _plural_match(word, t):
    """Does the noun phrase `word` (singular or plural) name the type `t`?"""
    word, t = word.lower().strip(), t.lower().strip()
    return word in (t, t + 's', t + 'es', t[:-1] + 'ies' if t.endswith('y') else None)


def direct_to_decl(x):
    """Direct interrogative (no frame) -> declarative string. 'Is E P' -> 'E is P'; 'Does E have Z' -> 'E has Z'."""
    m = re.fullmatch(r'(Is|Are) (.+)', x)
    if m:
        return ('is', m.group(2))
    m = re.fullmatch(r'(Does|Do) (.+)', x)
    if m:
        return ('does', m.group(2))
    m = re.fullmatch(r'(Did) (.+)', x)
    if m:
        return ('did', m.group(2))
    m = re.fullmatch(r'(Was|Were) (.+)', x)
    if m:
        return ('was', m.group(2))
    m = re.fullmatch(r'(Has|Have) (.+)', x)
    if m:
        return ('has', m.group(2))
    raise Unparsed('direct form')


def quant_decl(x, lex, dom_of_type):
    """S3-style quantified claims over a named type 'in this record'. Returns formula or None."""
    m = re.fullmatch(r'(?P<q>no|every|some|not every|not all|all|any|none of the) (?P<t>.+?) in this record'
                     r'(?: other than ' + lex.ENT + r')? (?P<vp>(?:is|are|has|have|does|do|lacks|lack) .+)', x)
    if not m:
        return None
    dom = dom_of_type(m.group('t'))
    if not dom:
        raise Unparsed('quant type')
    if m.group('id'):
        dom = [e for e in dom if e != m.group('id')]
    vals = [lex.vp(e, m.group('vp')) for e in dom]
    q = m.group('q')
    if q in ('some', 'any'):
        return OR(*vals)
    if q in ('every', 'all'):
        return AND(*vals)
    if q in ('no', 'none of the'):
        return NOT(OR(*vals))
    if q in ('not every', 'not all'):
        return NOT(AND(*vals))
    raise Unparsed('quant')


# ---------------------------------------------------------------- S3 fact graph (model enumeration over grounded universals)
def parse_s3(row):
    card, world = row['card'], card_world(row['card'])
    lex = Lex(card)
    kb = KB(world)
    ents = collections.OrderedDict()   # id -> type
    universals = []
    n_fact = 0
    for s in prose_sentences(row['state']):
        s = s.rstrip('.')
        m = re.fullmatch(r'(?P<q>Every|No) (?P<t>.+?) that (?P<c>(?:is|has an?|does not have an?|lacks an?|is not) .+?) '
                         r'(?P<h>(?:is|has|does not have|lacks) .+)', s)
        if m:
            universals.append((m.group('q'), m.group('t').lower(), m.group('c'), m.group('h')))
            continue
        m = re.fullmatch(ENTRE + r' (?P<vp>(?:is|has|does|lacks) .+)', s)
        if m:
            eid = m.group('id')
            ents[eid] = m.group('type').lower()
            kb.add_fact(lex.vp(eid, m.group('vp')))
            n_fact += 1
            continue
        # inert sentences (no ID, no quantifier) carry no fact about the record's entities
    q = extract_question(row['instructions'].replace("What's the answer?", ' '))
    for mm in re.finditer(ENTRE, q):
        ents.setdefault(mm.group('id'), mm.group('type').lower())
    for qq, t, c, h in universals:
        for e, et in ents.items():
            if not (_plural_match(t, et) or t == et):
                continue
            body = lex.vp(e, c)
            head = lex.vp(e, h)
            if qq == 'No':
                head = NOT(head)
            kb.add_rule(body, head)
    if not n_fact:
        raise Unparsed('S3 no facts')
    return kb, lex, ents


def lf_entity(q, lex, ents, extra=None):
    """Question -> LF for entity-predicate samplers (S1, S3, S5 facts)."""
    nout, body, direct = strip_frames(q)
    if direct:
        body = re.sub(r'^Among the [^,]+? in this record, ', '', body)
        body = body[0].upper() + body[1:]
        kind, rest = direct_to_decl(body)
        if kind == 'is':
            body = None
            m = re.fullmatch(lex.ENT + r' (?P<p>.+)', rest)
            if m:
                return lex.vp(m.group('id'), 'is ' + m.group('p'))
            m = re.fullmatch(r'(?P<q>any|every|some) (?P<t>.+?) in this record(?P<o> other than (?:[a-z][a-z -]* )?' + IDRE + r')? (?P<p>.+)', rest)
            if m:
                x = '%s %s in this record%s is %s' % (m.group('q'), m.group('t'), m.group('o') or '', m.group('p'))
                return quant_decl(x, lex, lambda t: [e for e, et in ents.items() if _plural_match(t, et)])
            if extra:
                return extra('is ' + rest)
            raise Unparsed('direct is')
        if kind == 'does':
            m = re.fullmatch(lex.ENT + r' have (?P<z>.+)', rest)
            if m:
                return lex.has(m.group('id'), m.group('z'))
            m = re.fullmatch(r'(?P<q>any|some|every) (?P<t>.+?)(?P<o> other than (?:[a-z][a-z -]* )?' + IDRE + r')? have (?P<z>.+)', rest)
            if m:
                x = '%s %s in this record%s has %s' % (m.group('q'), m.group('t'), m.group('o') or '', m.group('z'))
                return quant_decl(x, lex, lambda t: [e for e, et in ents.items() if _plural_match(t, et)])
        if extra:
            return extra(kind + ' ' + rest)
        raise Unparsed('direct ' + kind)
    nin, x = strip_embedded_neg(body)
    f = decl_entity(x, lex, ents, extra)
    for _ in range(nout + nin):
        f = NOT(f)
    return f


def decl_entity(x, lex, ents, extra=None):
    f = quant_decl(x, lex, lambda t: [e for e, et in ents.items() if _plural_match(t, et)])
    if f is not None:
        return f
    m = re.fullmatch(lex.ENT + r' (?P<vp>(?:is|are|has|have|does|do|lacks|lack) .+)', x)
    if m:
        return lex.vp(m.group('id'), m.group('vp'))
    if extra:
        return extra(x)
    raise Unparsed('decl')


def solve_s3(row):
    kb, lex, ents = parse_s3(row)
    q = extract_question(row['instructions'].replace("What's the answer?", ' '))
    lf = lf_entity(q, lex, ents)
    return kb.decide(lf)


# ---------------------------------------------------------------- driver
SOLVERS = {}


def run(files=FILES, only=None, limit=None):
    res = collections.Counter()
    mism, unparsed = [], []
    for fn in files:
        for i, line in enumerate(open(os.path.join(OUT, fn))):
            if limit and i >= limit:
                break
            row = json.loads(line)
            smp = row['meta']['sampler']
            if only and smp not in only:
                continue
            fnc = SOLVERS.get(smp)
            try:
                if fnc is None:
                    raise Unparsed('no solver for sampler')
                g = fnc(row)
            except Unparsed as e:
                res[(smp, 'unparsed')] += 1
                unparsed.append({'file': fn, 'id': row['id'], 'sampler': smp, 'role': row['role'], 'why': str(e)})
                continue
            except Undetermined as e:
                res[(smp, 'undetermined')] += 1
                mism.append({'file': fn, 'id': row['id'], 'sampler': smp, 'role': row['role'], 'gold_A': row['gold'],
                             'gold_B': None, 'why': str(e)})
                continue
            if g == row['gold']:
                res[(smp, 'agree')] += 1
            else:
                res[(smp, 'mismatch')] += 1
                mism.append({'file': fn, 'id': row['id'], 'sampler': smp, 'role': row['role'], 'gold_A': row['gold'],
                             'gold_B': g, 'why': 'label differs'})
    return res, mism, unparsed


SOLVERS['S3'] = solve_s3


# ---------------------------------------------------------------- numbers, bounds (SEM-08)
_BOUNDS = [('no fewer than', '>='), ('not less than', '>='), ('at least', '>='), ('reaches', '>='), ('meets', '>='),
           ('no more than', '<='), ('not more than', '<='), ('at most', '<='), ('up to', '<='),
           ('more than', '>'), ('over', '>'), ('above', '>'), ('exceeds', '>'),
           ('fewer than', '<'), ('less than', '<'), ('under', '<'), ('below', '<'), ('exactly', '==')]
NUM = r'(?P<n>-?\d+(?:\.\d+)?)'


def parse_quantity(s):
    m = re.fullmatch(NUM + r'(?: (?P<u>.+))?', s.strip())
    if not m:
        return None
    return float(m.group('n')), (m.group('u') or '').strip(), m.group('n')


def parse_bound(s):
    """'at least 5 torv' -> ('>=', 5.0, 'torv', '5'); '5 torv or more' -> ('>=', ...); '216 meals' -> ('==', ...);
    'between 3 and 5 units' -> ('between', (3, 5), unit, ...). None if not numeric."""
    s = s.strip()
    m = re.fullmatch(r'between ' + NUM + r'(?: [a-z][^\d]*?)? and (?P<n2>-?\d+(?:\.\d+)?)(?: (?P<u>.+))?', s)
    if m:
        return ('between', (float(m.group('n')), float(m.group('n2'))), (m.group('u') or '').strip(), m.group('n'))
    m = re.fullmatch(r'(.+?) or more', s)
    if m and parse_quantity(m.group(1)):
        v, u, raw = parse_quantity(m.group(1))
        return ('>=', v, u, raw)
    m = re.fullmatch(r'(.+?) or (?:fewer|less)', s)
    if m and parse_quantity(m.group(1)):
        v, u, raw = parse_quantity(m.group(1))
        return ('<=', v, u, raw)
    for w, op in _BOUNDS:
        if s.startswith(w + ' '):
            pq = parse_quantity(s[len(w) + 1:])
            if pq:
                return (op, pq[0], pq[1], pq[2])
    pq = parse_quantity(s)
    if pq:
        return ('==', pq[0], pq[1], pq[2])
    return None


def cmp_num(v, op, t):
    if op == '>=':
        return v >= t
    if op == '<=':
        return v <= t
    if op == '>':
        return v > t
    if op == '<':
        return v < t
    if op == '==':
        return v == t
    if op == 'between':
        return t[0] <= v <= t[1]
    raise ValueError(op)


def step_of(raw):
    """One unit of the value's last displayed digit (SEM-08)."""
    return 10 ** -(len(raw.split('.')[1])) if '.' in raw else 1.0


_MODALS = ['is not permitted to', 'is permitted to', 'is not required to', 'is required to', 'does not have to',
           'must not', 'may not', 'need not', 'cannot', 'must', 'may']
_MODAL_KIND = {'must': 'req', 'is required to': 'req', 'must not': 'forb', 'may not': 'forb',
               'is not permitted to': 'forb', 'cannot': 'forb', 'may': 'perm', 'is permitted to': 'perm',
               'need not': 'notreq', 'does not have to': 'notreq', 'is not required to': 'notreq'}


# ---------------------------------------------------------------- S1 rule-case (model enumeration + SEM-04 test values)
class S1Base:
    def __init__(self, row):
        self.row = row
        card = row['card']
        self.world = card_world(card)
        self.lex = Lex(card)
        self.vsets = card_valuesets(card)
        self.q = extract_question(row['instructions'].replace("What's the answer?", ' '))
        sents = prose_sentences(row['state'])
        rule_txt = [s for s in sents if re.match(r'R\d+\.\s', s)]
        for mm in re.finditer(r'Rules? for this task: (.+)$', card, re.M):
            rule_txt += re.findall(r'R\d+\.\s.+?\.(?=\s+R\d+\.|\s*$)', mm.group(1).strip())
        self.types = card_types(card)
        if not self.types:
            raise Unparsed('S1 no entity type on card')
        self.T = '(?:' + '|'.join(re.escape(t) for t in self.types) + ')'
        self.ENT = r'(?P<type>(?i:' + self.T + r')) (?P<id>' + IDRE + r')'
        self.cases = collections.OrderedDict()
        for mm in re.finditer(r'Cases under review: (.+)$', card, re.M):
            for e in re.finditer(self.ENT, mm.group(1)):
                self.cases[e.group('id')] = e.group('type').lower()
        fact_txt = [s for s in sents if not re.match(r'R\d+\.\s', s) and re.search(IDRE, s)]
        for s in fact_txt + [self.q]:
            for e in re.finditer(self.ENT, s):
                self.cases.setdefault(e.group('id'), e.group('type').lower())
        if not self.cases:
            raise Unparsed('S1 no case')
        self.attr = {}         # (id, attr) -> ('num', v, unit, raw) | ('cat', s) | ('unrec',)
        self.adjusted = {}     # attr -> (op, v)  cap ('<=') / floor ('>=')
        self.cmp_atoms = set()
        self.kb = KB(self.world)
        self.deon = collections.defaultdict(lambda: {'req': [], 'forb': []})
        self.n_facts = 0
        for s in fact_txt:
            self._fact(s.rstrip('.'))
        self.rules = [self._parse_rule(re.sub(r'^R\d+\.\s+', '', s).rstrip('.')) for s in rule_txt]
        self._roles_table(row['state'])
        for e in self.cases:
            for r in self.rules:
                self._ground(r, e)
        for (role, act, e), d in self.deon.items():
            self.kb.defs.append(IFF(A(('req', role, act, e)), OR(*d['req'])))
            self.kb.defs.append(IFF(A(('forb', role, act, e)), OR(*d['forb'])))
            self.kb.defined |= {('req', role, act, e), ('forb', role, act, e)}

    # -- facts
    def _fact(self, s):
        m = re.fullmatch(r'The (?P<attr>.+?) of ' + self.ENT + r' is (?P<rest>.+)', s)
        if m:
            eid, attr, rest = m.group('id'), m.group('attr').lower(), m.group('rest').strip()
            if rest == 'not recorded':
                self.attr[(eid, attr)] = ('unrec',)
            else:
                pq = parse_quantity(rest)
                self.attr[(eid, attr)] = ('num',) + pq if pq else ('cat', rest)
            self.n_facts += 1
            return
        m = re.fullmatch(self.ENT + r' (?P<vp>(?:is|has|does|lacks) .+)', s)
        if m:
            self.kb.add_fact(self.lex.vp(m.group('id'), m.group('vp')))
            self.n_facts += 1

    # -- rules
    def _parse_rule(self, t):
        m = re.fullmatch(r'The adjusted (?P<a>.+?) of the ' + self.T + r' is the (?P<a2>.+?) of the ' + self.T +
                         r', but (?P<b>.+)', t)
        if m:
            b = parse_bound(m.group('b'))
            if not b or b[0] not in ('>=', '<='):
                raise Unparsed('adjusted bound')
            self.adjusted[m.group('a').lower()] = (m.group('a2').lower(), b[0], b[1])
            return None
        m = re.fullmatch(r'If (?P<c>.+?), then (?P<h>.+?)(?:,? (?P<ek>except when|unless) (?P<e>.+))?', t)
        if m:
            return ('if', self._conj(m.group('c')), m.group('h'), m.group('e'))
        m = re.fullmatch(r'(?P<h>.+?),? unless (?P<b>.+)', t)
        if m:
            return ('unless', self._conj(m.group('b')), m.group('h'), None)
        m = re.fullmatch(r'(?P<h>.+?) only if (?P<b>.+)', t)
        if m:
            return ('onlyif', self._conj(m.group('b')), m.group('h'), None)
        m = re.fullmatch(r'(?P<h>.+?), except when (?P<e>.+)', t)
        if m:
            return ('uncond', [], m.group('h'), m.group('e'))
        return ('uncond', [], t, None)

    def _conj(self, c):
        return re.split(r' and (?=(?:the |' + self.T + r' ' + IDRE + r'))', c)

    def _clause(self, s, e):
        """Condition or non-deontic head about case e -> formula (cmp atoms for attribute tests)."""
        s = s.strip()
        m = re.fullmatch(r'the (?P<adj>adjusted )?(?P<attr>.+?) of (?:the ' + self.T + r'|' + self.T + ' ' + IDRE +
                         r') is (?P<rest>.+)', s, re.I)
        if m:
            return self._cmp(e, m.group('attr').lower(), bool(m.group('adj')), m.group('rest'))
        m = re.fullmatch(r'(?:the ' + self.T + r'|' + self.T + ' ' + IDRE + r') (?P<vp>.+)', s, re.I)
        if m:
            return self.lex.vp(e, m.group('vp'))
        raise Unparsed('S1 clause')

    def _cmp(self, e, attr, adjusted, rest):
        rest = rest.strip()
        b = parse_bound(rest)
        if b:
            key = ('cmp', e, attr, adjusted, b[0], b[1])
        else:
            neg = False
            m = re.fullmatch(r'not (.+)', rest)
            if m:
                neg, rest = True, m.group(1)
            key = ('cmp', e, attr, adjusted, 'is', rest.strip().lower())
            self.cmp_atoms.add(key)
            return NOT(A(key)) if neg else A(key)
        self.cmp_atoms.add(key)
        return A(key)

    def _deontic(self, s):
        m = re.fullmatch(r'[Tt]he (?P<role>[A-Z][\w\' -]*?) (?P<modal>' + '|'.join(_MODALS) + r') (?P<act>.+)', s.strip())
        if not m:
            return None
        act = re.sub(r' the (?:' + self.T + r')$', '', m.group('act').strip(), flags=re.I)
        return m.group('role'), _MODAL_KIND[m.group('modal')], act

    def _ground(self, r, e):
        if r is None:
            return
        kind, conds, head, exc = r
        body = [self._clause(c, e) for c in conds]
        excf = AND(*[self._clause(x, e) for x in self._conj(exc)]) if exc else None
        if kind == 'if':
            app = AND(*(body + ([NOT(excf)] if excf is not None else [])))
        elif kind in ('unless', 'onlyif'):
            app = NOT(AND(*body))           # <B> false
        else:
            app = NOT(excf) if excf is not None else True
        d = self._deontic(head)
        if d:
            role, mk, act = d
            slot = self.deon[(role, act, e)]
            if kind == 'onlyif':
                if mk != 'perm':
                    raise Unparsed('only-if modal head')
                slot['forb'].append(app)    # "may X only if B": B false -> not permitted (SEM-06, SEM-24)
            elif mk == 'req':
                slot['req'].append(app)
            elif mk == 'forb':
                slot['forb'].append(app)
            return                          # may / need not heads neither require nor forbid
        h = self._clause(head, e)
        self.kb.add_rule(app, NOT(h) if kind == 'onlyif' else h)

    def _roles_table(self, state):
        cells = table_cells(state)
        actre = re.compile(r'[a-z]+(?: [a-z]+)? the (?:' + self.T + r')', re.I)
        i = 0
        while i + 2 < len(cells):
            w = cells[i:i + 3]
            kinds = [c.lower() in ('required', 'permitted', 'forbidden') for c in w]
            acts = [bool(actre.fullmatch(c)) for c in w]
            if sum(kinds) == 1 and sum(acts) == 1 and not (kinds[0] and acts[0]):
                k = [c for c, f in zip(w, kinds) if f][0].lower()
                a = [c for c, f in zip(w, acts) if f][0]
                role = [c for c, f, g in zip(w, kinds, acts) if not f and not g][0]
                act = re.sub(r' the (?:' + self.T + r')$', '', a, flags=re.I)
                for e in self.cases:
                    slot = self.deon[(role, act, e)]
                    if k == 'required':
                        slot['req'].append(True)
                    elif k == 'forbidden':
                        slot['forb'].append(True)
                i += 3
                continue
            i += 1


def table_cells(state):
    """Container-independent cell stream: markup removed, split on table / record delimiters, keys stripped."""
    s = _clean_markup(state)
    out = []
    for c in re.split(r'[|\n\t;{}\[\]]|,\s', s):
        c = c.strip().strip('"\'').strip()
        c = re.sub(r'^[A-Za-z_][\w ]*?\s*[:=]\s*', '', c) if re.match(r'^[a-z_]+\s*[:=]', c) else c
        c = c.strip().strip('"\'').strip()
        if c and not re.fullmatch(r'[-=:+ ]+', c):
            out.append(c)
    return out


def subst(f, fn):
    """Replace atoms for which fn(key) returns a bool by that constant."""
    if f is True or f is False:
        return f
    t = f[0]
    if t == 'atom':
        v = fn(f[1])
        return f if v is None else v
    if t == 'not':
        return NOT(subst(f[1], fn))
    if t == 'and':
        return AND(*[subst(g, fn) for g in f[1]])
    if t == 'or':
        return OR(*[subst(g, fn) for g in f[1]])
    if t == 'iff':
        a, b = subst(f[1], fn), subst(f[2], fn)
        if a is True or a is False:
            return b if a else NOT(b)
        if b is True or b is False:
            return a if b else NOT(a)
        return ('iff', a, b)
    return (t, f[1], [subst(g, fn) for g in f[2]])


def _s1_extra(base):
    def extra(x):
        x = x.strip()
        m = re.fullmatch(r'is (the (?:adjusted )?.+? of (?:the )?' + base.T + ' ' + IDRE + r') (?P<rest>.+)', x, re.I)
        if m:
            x = m.group(1) + ' is ' + m.group('rest')
        m = re.fullmatch(r'is (the [A-Z][\w\' -]*?) ((?:not )?(?:permitted|required) to .+)', x)
        if m:
            x = m.group(1) + ' is ' + m.group(2)
        m = re.fullmatch(r'the (?P<adj>adjusted )?(?P<attr>.+?) of (?:the )?' + base.T + ' (?P<id>' + IDRE + r') is (?P<rest>.+)', x, re.I)
        if m:
            return base._cmp(m.group('id'), m.group('attr').lower(), bool(m.group('adj')), m.group('rest'))
        d = base._deontic(x)
        if d:
            role, mk, act = d
            if len(base.cases) != 1:
                raise Unparsed('deontic question with several cases')
            e = list(base.cases)[0]
            base.deon[(role, act, e)]
            req, forb = A(('req', role, act, e)), A(('forb', role, act, e))
            return {'req': req, 'forb': forb, 'perm': NOT(forb), 'notreq': NOT(req)}[mk]
        raise Unparsed('S1 question form')
    return extra


def solve_s1(row):
    base = S1Base(row)
    lf = lf_entity(base.q, base.lex, base.cases, _s1_extra(base))
    for (role, act, e), d in base.deon.items():
        for k in ('req', 'forb'):
            key = (k, role, act, e)
            if key not in base.kb.defined:
                base.kb.defs.append(IFF(A(key), OR(*d[k])))
                base.kb.defined.add(key)
    # SEM-04: every (case, attribute) a comparison reads; unrecorded or unmentioned ones are free variables
    reads = sorted({(k[1], k[2], k[3]) for k in base.cmp_atoms}, key=str)
    free = {}
    for e, attr, adj in reads:
        src = base.adjusted[attr][0] if adj and attr in base.adjusted else attr
        if adj and attr not in base.adjusted:
            raise Unparsed('adjusted attribute without rule')
        v = base.attr.get((e, src))
        if v is None or v[0] == 'unrec':
            if v is None and base.world == 'closed':
                raise Unparsed('closed card omits attribute')
            free[(e, src)] = _test_values(base, e, src)
    keys = list(free)
    labels = set()
    for combo in itertools.product(*[free[k] for k in keys]):
        val = dict(zip(keys, combo))

        def fn(key):
            if key[0] != 'cmp':
                return None
            _, e, attr, adj, op, t = key
            src = base.adjusted[attr][0] if adj else attr
            v = val.get((e, src), base.attr.get((e, src)))
            if adj:
                _, aop, an = base.adjusted[attr]
                if v[0] != 'num':
                    raise Unparsed('adjusted non-number')
                v = ('num', max(v[1], an) if aop == '>=' else min(v[1], an))
            if op == 'is':
                if v[0] == 'num':
                    b = parse_bound(t)
                    return bool(b) and cmp_num(v[1], b[0], b[1])
                return v[1].lower() == t
            if v[0] != 'num':
                raise Unparsed('numeric test on category')
            return cmp_num(v[1], op, t)
        cons = [subst(c, fn) for c in base.kb.constraints(lf)]
        labels.add(decide(cons, subst(lf, fn)))
    if len(labels) != 1:
        raise Undetermined('SEM-04 test values disagree')
    return labels.pop()


def _test_values(base, e, attr):
    """SEM-04 test set for a free (unrecorded or unstated) value of case e's attribute."""
    vs = base.vsets.get(attr)
    others = [v for (e2, a2), v in base.attr.items() if a2 == attr and e2 != e and v[0] != 'unrec']
    th = []
    for k in base.cmp_atoms:
        a = base.adjusted[k[2]][0] if k[3] and k[2] in base.adjusted else k[2]
        if a != attr:
            continue
        if k[4] == 'is':
            b = parse_bound(k[5])
            th.append(('num', b[1]) if b and b[0] == '==' else ('cat', k[5]))
        elif k[4] == 'between':
            th += [('num', k[5][0]), ('num', k[5][1])]
        else:
            th.append(('num', k[5]))
    for a, (src, op, n) in base.adjusted.items():
        if src == attr:
            th.append(('num', n))
    nums = [t[1] for t in th if t[0] == 'num'] + [o[1] for o in others if o[0] == 'num']
    if vs and not nums:
        return [('cat', v) for v in vs]
    if nums or any(o[0] == 'num' for o in others):
        step = 1.0
        for k in base.cmp_atoms:
            pass
        out = set()
        for n in nums:
            st = 0.01 if abs(n - round(n)) > 1e-9 else step
            out |= {n - st, n, n + st}
        return [('num', v) for v in sorted(out)]
    cats = {t[1] for t in th if t[0] == 'cat'} | {o[1].lower() for o in others if o[0] == 'cat'}
    return [('cat', c) for c in sorted(cats)] + [('cat', '__fresh__')]


SOLVERS['S1'] = solve_s1


# ---------------------------------------------------------------- S4 record containers (own readers, no generator code)
def _norm_key(k):
    return re.sub(r'\s+', ' ', k.replace('_', ' ')).strip().lower()


def _cellval(v):
    """Raw cell -> ('blank',) | ('unrec',) | ('s', text)."""
    if v is None:
        return ('unrec',)
    v = str(v).strip().strip('"').strip("'").strip()
    if v == '':
        return ('blank',)
    if v.lower() in ('not recorded', 'null', 'none'):
        return ('unrec',)
    return ('s', v)


def _recs_ok(recs, idfield_ok):
    if len(recs) < 2:
        return False
    keys = list(recs[0].keys())
    return all(list(r.keys()) == keys for r in recs) and idfield_ok(recs)


def _from_json(state):
    s = re.sub(r'```[A-Za-z]*', '', state)
    i = min([x for x in (s.find('{'), s.find('[')) if x >= 0], default=-1)
    if i < 0:
        return None
    j = max(s.rfind('}'), s.rfind(']'))
    try:
        obj = json.loads(s[i:j + 1])
    except Exception:
        return None
    found = []

    def walk(o):
        if isinstance(o, list) and o and all(isinstance(x, dict) for x in o):
            found.append(o)
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        if isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    for lst in found:
        recs = [{_norm_key(k): _cellval(v) for k, v in d.items()} for d in lst]
        yield recs


def _split_row(line, sep):
    line = line.strip()
    if sep == '|' and line.startswith('|'):
        line = line[1:]
        if line.endswith('|'):
            line = line[:-1]
    return [c.strip() for c in line.split(sep)]


def _from_lines(state):
    """Pipe / delimiter tables, HTML tables (rows -> pipe lines), fixed-width tables with ==== rules."""
    s = state
    if '<tr' in s:
        s = re.sub(r'</t[hd]>\s*<t[hd][^>]*>', '|', s)
        s = re.sub(r'<tr[^>]*>\s*<t[hd][^>]*>', '\n|', s)
        s = re.sub(r'</t[hd]>\s*</tr>', '|\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    lines = [l.rstrip('\r') for l in s.split('\n')]
    lines = [l.rstrip() if not l.rstrip().endswith('|') else l for l in lines]
    # fixed width with '====' rule lines
    for i, l in enumerate(lines):
        if re.fullmatch(r'\s*=+(?:\s{2,}=+)+\s*', l) and i > 0:
            spans = [(m.start(), m.end()) for m in re.finditer(r'=+', l)]
            def cut(x):
                out = []
                for k, (a, b) in enumerate(spans):
                    e = spans[k + 1][0] if k + 1 < len(spans) else len(x) + 1
                    out.append(x[a:e].strip())
                return out
            hdr = cut(lines[i - 1])
            rows = []
            for x in lines[i + 1:]:
                if not x.strip():
                    if rows:
                        break
                    continue
                if re.fullmatch(r'\s*=+(?:\s{2,}=+)*\s*', x):
                    continue
                rows.append(cut(x))
            yield [dict(zip([_norm_key(h) for h in hdr], [_cellval(c) for c in r])) for r in rows]
    # fixed width aligned on the header's column starts (2+ spaces between header names)
    for i, l in enumerate(lines):
        if i + 1 < len(lines) and re.match(r'\s*' + IDRE + r'\s', lines[i + 1] + ' ') and not re.search(IDRE, l) \
                and re.search(r'\S {2,}\S', l) and '|' not in l:
            starts = [m.start() for m in re.finditer(r'\S+(?: \S+)*', l)]
            def cut2(x):
                return [x[a:(starts[k + 1] if k + 1 < len(starts) else len(x))].strip() for k, a in enumerate(starts)]
            hdr = cut2(l)
            rows = []
            for x in lines[i + 1:]:
                if not re.match(r'\s*' + IDRE + r'\s', x + ' '):
                    break
                rows.append(cut2(x))
            yield [dict(zip([_norm_key(h) for h in hdr], [_cellval(c) for c in r])) for r in rows]
    for sep in ('|', ';', '\t', ','):
        cand = [l for l in lines if sep in l]
        if len(cand) < 3:
            continue
        rows = [_split_row(l, sep) for l in cand if not re.fullmatch(r'[\s|:=+-]*', l)]
        n = collections.Counter(len(r) for r in rows).most_common(1)[0][0]
        rows = [r for r in rows if len(r) == n]
        hi = [k for k, r in enumerate(rows) if not any(re.fullmatch(IDRE, c) for c in r)]
        if not hi or n < 2:
            continue
        hdr = rows[hi[0]]
        data = [r for r in rows[hi[0] + 1:] if any(re.fullmatch(IDRE, c) for c in r)]
        yield [dict(zip([_norm_key(h) for h in hdr], [_cellval(c) for c in r])) for r in data]


_KV = re.compile(r'^\s*(?:-\s+)?["\']?(?P<k>[A-Za-z][\w ]*?)["\']?\s*(?:\s\.{2,}|\.{2,}|:|=)\s*(?P<v>.*?)\s*,?\s*$')
_INLINE = re.compile(r'(?P<k>[A-Za-z][\w ]*?)\s*[:=]\s*(?P<v>"[^"]*"|\'[^\']*\'|[^,}]*?)\s*(?=,\s*[A-Za-z][\w ]*?\s*[:=]|\s*\}|$)')


def _from_kv(state, idkeys):
    """Key-value blocks (YAML-ish, key: value, key=value, dotted leaders, inline {k: v, ...}). A record starts
    at a key whose value is an ID."""
    s = re.sub(r'```[A-Za-z]*', '', state)
    recs, cur = [], None
    for line in s.split('\n'):
        pairs = []
        if '{' in line and '}' in line:
            body = line[line.find('{') + 1:line.rfind('}')]
            pairs = [(m.group('k'), m.group('v')) for m in _INLINE.finditer(body)]
        else:
            m = _KV.match(line)
            if m:
                pairs = [(m.group('k'), m.group('v'))]
        for k, v in pairs:
            k2 = _norm_key(k)
            vv = v.strip().strip('"').strip("'")
            if re.fullmatch(IDRE, vv) and (cur is None or k2 in idkeys or k2 == list(cur.keys())[0]):
                if cur:
                    recs.append(cur)
                cur = collections.OrderedDict()
            if cur is not None and v.strip() not in ('[', '{', '[]', '{}'):
                if k2 in cur:
                    continue
                cur[k2] = _cellval(v)
    if cur:
        recs.append(cur)
    if not recs:
        return
    # keep the field set shared by the records (drop trailing notes attached to the last record)
    common = [k for k in recs[0] if all(k in r for r in recs)]
    yield [collections.OrderedDict((k, r[k]) for k in common) for r in recs]


def parse_records(state, types):
    """-> (fields, id_field, records) or raise Unparsed."""
    idkeys = set(types)

    def ok(recs):
        if len(recs) < 2:
            return False
        keys = list(recs[0].keys())
        if not all(list(r.keys()) == keys for r in recs):
            return False
        idf = [k for k in keys if all(r[k][0] == 's' and re.fullmatch(IDRE, r[k][1]) for r in recs)]
        return bool(idf)
    for gen in (_from_json(state), _from_lines(state), _from_kv(state, idkeys)):
        if gen is None:
            continue
        for recs in gen:
            if recs and ok(recs):
                keys = list(recs[0].keys())
                idf = [k for k in keys if all(r[k][0] == 's' and re.fullmatch(IDRE, r[k][1]) for r in recs)][0]
                return keys, idf, recs
    raise Unparsed('S4 container')


# ---------------------------------------------------------------- S4 solver: sqlite + independent LF->SQL compiler
class S4Base:
    def __init__(self, row):
        self.row = row
        card = row['card']
        self.world = card_world(card)
        self.types = card_types(card)
        self.affix = card_affixes(card)
        self.vsets = card_valuesets(card)
        self.qcard, self.mcard = card_graded(card)
        self.fields, self.idf, self.recs = parse_records(row['state'], self.types)
        self.kind = {}
        for f in self.fields:
            vals = [r[f] for r in self.recs]
            ss = [v[1] for v in vals if v[0] == 's']
            if f == self.idf:
                self.kind[f] = 'id'
            elif all(x.lower() in ('yes', 'no') for x in ss):
                self.kind[f] = 'yn'
            elif ss and all(parse_quantity(x) for x in ss):
                self.kind[f] = 'num'
            else:
                self.kind[f] = 'cat'
            if self.kind[f] != 'yn' and any(v[0] == 'blank' for v in vals):
                raise Unparsed('blank in non yes/no field')
        self.col = {f: 'c%d' % i for i, f in enumerate(self.fields)}
        self.rule = None
        mm = re.search(r'Rules? for this task: R\d+\.\s+(.+?)\.?\s*$', card, re.M)
        if mm:
            self.rule = mm.group(1).rstrip('.')
        self.reads = set()          # fields the LF reads
        self.thresholds = collections.defaultdict(list)
        self.catvals = collections.defaultdict(set)
        self.q = extract_question(row['instructions'].replace("What's the answer?", ' '))
        self.T = '(?:' + '|'.join(re.escape(t) for t in sorted(self.types, key=len, reverse=True)) + ')'

    # -- names
    def field_named(self, s):
        s = _norm_key(s)
        for f in sorted(self.fields, key=len, reverse=True):
            if s == f:
                return f
        return None

    def pred_sql(self, word, alias='t'):
        """SQL boolean for '<record> is <word>' (a yes/no column, an affixed word, or the inverted card's outcome)."""
        word = re.sub(r'^among the cases that are ', '', word.strip())
        if word in self.affix:
            return 'NOT (%s)' % self.pred_sql(self.affix[word], alias)
        f = self.field_named(word)
        if f and self.kind[f] == 'yn':
            self.reads.add(f)
            return 'COALESCE(%s.%s, 0) = 1' % (alias, self.col[f])
        if self.rule:
            m = re.fullmatch(r'If (?P<c>.+?), then the ' + self.T + r' is (?P<o>[a-z-]+)', self.rule)
            if m and m.group('o') == word:
                conds = re.split(r' and (?=the )', m.group('c'))
                return '(' + ' AND '.join(self.cond_sql(c, alias) for c in conds) + ')'
        raise Unparsed('S4 predicate')

    def cond_sql(self, c, alias):
        c = c.strip()
        m = re.fullmatch(r'the (?P<f>.+?) of the ' + self.T + r' is (?P<rest>.+)', c)
        if m:
            f = self.field_named(m.group('f'))
            if not f:
                raise Unparsed('S4 rule field')
            return self.value_test(f, m.group('rest'), alias)
        m = re.fullmatch(r'the ' + self.T + r' is (?P<neg>not )?(?P<w>[a-z-]+)', c)
        if m:
            x = self.pred_sql(m.group('w'), alias)
            return 'NOT (%s)' % x if m.group('neg') else x
        raise Unparsed('S4 rule condition')

    def value_test(self, f, rest, alias):
        self.reads.add(f)
        col = '%s.%s' % (alias, self.col[f])
        rest = rest.strip()
        if self.kind[f] == 'num':
            b = parse_bound(rest)
            if not b:
                raise Unparsed('S4 numeric test')
            self.thresholds[f].append(b)
            op, v = b[0], b[1]
            if op == 'between':
                return '(%s BETWEEN %r AND %r)' % (col, v[0], v[1])
            return '(%s %s %r)' % (col, '=' if op == '==' else op, v)
        neg = False
        m = re.fullmatch(r'not (.+)', rest)
        if m:
            neg, rest = True, m.group(1)
        self.catvals[f].add(rest.lower())
        x = "(lower(%s) = %s)" % (col, _sqlstr(rest.lower()))
        return 'NOT %s' % x if neg else x


def _sqlstr(s):
    return "'" + s.replace("'", "''") + "'"


_QB = r'(?P<b>at least|at most|no fewer than|no more than|not more than|not less than|more than|fewer than|exactly)'
_PW = r'(?P<p>(?:not )?(?:among the cases that are )?[a-z][a-z-]*)'


def s4_group(base, g):
    """'<records> with <filters>[ other than <type> <ID>]' -> SQL WHERE over alias t."""
    g = g.strip()
    excl = None
    m = re.fullmatch(r'(?P<g>.+?) other than (?:the )?' + base.T + r' (?P<id>' + IDRE + r')', g)
    if m:
        g, excl = m.group('g'), m.group('id')
    m = re.fullmatch(r'(?P<n>[a-z][a-z -]*?) with (?P<f>.+)', g)
    if not m or not any(_plural_match(m.group('n'), t) for t in base.types):
        raise Unparsed('S4 group noun')
    parts = re.split(r' and (?=an? )', m.group('f'))
    conds = []
    for part in parts:
        mm = re.fullmatch(r'an? (?P<f>.+?) of (?P<b>.+)', part)
        if mm and base.field_named(mm.group('f')) and base.kind[base.field_named(mm.group('f'))] == 'num':
            conds.append(base.value_test(base.field_named(mm.group('f')), mm.group('b'), 't'))
            continue
        hit = None
        for f in sorted(base.fields, key=len, reverse=True):
            if part.lower().startswith(f + ' ') and base.kind[f] in ('cat', 'num'):
                hit = f
                break
        if not hit:
            raise Unparsed('S4 filter')
        conds.append(base.value_test(hit, part[len(hit) + 1:], 't'))
    if excl:
        conds.append('t.%s <> %s' % (base.col[base.idf], _sqlstr(excl)))
    return ' AND '.join(conds) if conds else '1'


def s4_pred(base, p):
    p = p.strip()
    m = re.fullmatch(r'not (.+)', p)
    if m:
        return 'NOT (%s)' % s4_pred(base, m.group(1))
    return base.pred_sql(p, 't')


def s4_quant(base, x):
    """Declarative quantified claim -> SQL boolean expression."""
    m = re.fullmatch(_QB + r' (?P<q>\d+) of the (?P<g>.+) (?:are|is) ' + _PW, x)
    if not m:
        m = re.fullmatch(r'(?P<b>more than|at least) (?P<q>half) of the (?P<g>.+) (?:are|is) ' + _PW, x)
    if m:
        W, P = s4_group(base, m.group('g')), s4_pred(base, m.group('p'))
        cnt = '(SELECT COUNT(*) FROM t WHERE %s AND (%s))' % (W, P)
        tot = '(SELECT COUNT(*) FROM t WHERE %s)' % W
        b = m.group('b')
        if m.group('q') == 'half':
            return '(2 * %s %s %s)' % (cnt, '>' if b == 'more than' else '>=', tot)
        op = {'at least': '>=', 'no fewer than': '>=', 'not less than': '>=', 'at most': '<=', 'no more than': '<=',
              'not more than': '<=', 'more than': '>', 'fewer than': '<', 'exactly': '='}[b]
        return '(%s %s %d)' % (cnt, op, int(m.group('q')))
    m = re.fullmatch(r'(?P<qu>all|every|some|any|no|not every|not all|none of the|hardly any|scarcely any|few) '
                     r'(?P<g>.+) (?:are|is) ' + _PW, x)
    if m:
        W, P = s4_group(base, m.group('g')), s4_pred(base, m.group('p'))
        ex = 'EXISTS (SELECT 1 FROM t WHERE %s AND (%s))' % (W, P)
        allq = 'NOT EXISTS (SELECT 1 FROM t WHERE %s AND NOT (%s))' % (W, P)
        qu = m.group('qu')
        if qu in ('some', 'any'):
            return ex
        if qu in ('all', 'every'):
            return allq
        if qu in ('no', 'none of the'):
            return 'NOT ' + ex
        if qu in ('not every', 'not all'):
            return 'NOT (%s)' % allq
        if base.qcard is None:
            raise Unparsed('graded cue without card q')
        return '((SELECT COUNT(*) FROM t WHERE %s AND (%s)) < %d)' % (W, P, base.qcard)
    return None


def s4_entity(base, x):
    m = re.fullmatch(r'(?:the )?' + base.T + r' (?P<id>' + IDRE + r') (?P<vp>.+)', x, re.I)
    if not m:
        return None
    eid, vp = m.group('id'), m.group('vp').strip()

    def P(w):
        return '(SELECT %s FROM t WHERE t.%s = %s)' % (s4_pred(base, w), base.col[base.idf], _sqlstr(eid))
    mm = re.fullmatch(r'(?:is|are) not only (.+?) but also (.+)', vp)
    if mm:
        return '(%s AND %s)' % (P(mm.group(1)), P(mm.group(2)))
    mm = re.fullmatch(r'(?:is|are) neither (.+?) nor (.+)', vp)
    if mm:
        return '(NOT %s AND NOT %s)' % (P(mm.group(1)), P(mm.group(2)))
    mm = re.fullmatch(r'(?:is|are) (.+)', vp)
    if mm:
        return P(mm.group(1))
    raise Unparsed('S4 entity vp')


def s4_lf_sql(base):
    nout, body, direct = strip_frames(base.q)
    if direct:
        body = re.sub(r'^Among the [^,]+?, ', '', body)
        body = body[0].upper() + body[1:]
        m = re.fullmatch(r'(?:Are|Is) ' + _QB + r' (?P<q>\d+) of the (?P<g>.+) ' + _PW, body)
        if not m:
            m = re.fullmatch(r'(?:Are|Is) (?P<b>more than|at least) (?P<q>half) of the (?P<g>.+) ' + _PW, body)
        if m:
            x = '%s %s of the %s are %s' % (m.group('b'), m.group('q'), m.group('g'), m.group('p'))
        else:
            m = re.fullmatch(r'(?:Are|Is) (?P<qu>all|every|any|some|hardly any|scarcely any|few) (?P<g>.+) ' + _PW, body)
            if m:
                x = '%s %s is %s' % (m.group('qu'), m.group('g'), m.group('p'))
            else:
                m = re.fullmatch(r'(?:Is|Are) (?P<e>(?:the )?' + base.T + ' ' + IDRE + r') (?P<p>.+)', body, re.I)
                if not m:
                    raise Unparsed('S4 direct form')
                x = '%s is %s' % (m.group('e'), m.group('p'))
        nin = 0
    else:
        nin, x = strip_embedded_neg(body)
    sql = s4_quant(base, x) or s4_entity(base, x)
    if sql is None:
        raise Unparsed('S4 claim form')
    for _ in range(nout + nin):
        sql = 'NOT (%s)' % sql
    return sql


def _s4_tests(base, f, rec):
    """SEM-04 test values for an unrecorded entry of field f (F5-R4-05)."""
    k = base.kind[f]
    if k == 'yn':
        return [0, 1]
    others = [r[f] for r in base.recs if r is not rec and r[f][0] == 's']
    if k == 'num':
        pts = [b[1] for b in base.thresholds[f] if b[0] != 'between']
        pts += [x for b in base.thresholds[f] if b[0] == 'between' for x in b[1]]
        pts += [parse_quantity(o[1])[0] for o in others]
        out = set()
        for n in pts:
            st = 0.01 if abs(n - round(n)) > 1e-9 else 1.0
            out |= {n - st, n, n + st}
        return sorted(out) or [0.0]
    vs = base.vsets.get(f)
    if vs:
        return [v.lower() for v in vs]
    return sorted(base.catvals[f] | {o[1].lower() for o in others} | {'__fresh__'})


def solve_s4(row):
    base = S4Base(row)
    if base.world != 'closed':
        raise Unparsed('S4 open card')
    sql = s4_lf_sql(base)
    db = sqlite3.connect(':memory:')
    cols = [base.col[f] for f in base.fields]
    db.execute('CREATE TABLE t (%s)' % ', '.join(cols))
    free = []
    for ri, r in enumerate(base.recs):
        vals = []
        for f in base.fields:
            v, k = r[f], base.kind[f]
            if v[0] == 'blank':
                vals.append(None)               # closed card: blank yes/no -> COALESCE(..., 0)
            elif v[0] == 'unrec':
                vals.append(None)
                if f in base.reads:
                    free.append((ri, f))
            elif k == 'yn':
                vals.append(1 if v[1].lower() == 'yes' else 0)
            elif k == 'num':
                vals.append(parse_quantity(v[1])[0])
            else:
                vals.append(v[1].lower() if k == 'cat' else v[1])
        db.execute('INSERT INTO t VALUES (%s)' % ', '.join('?' * len(vals)), vals)
    db.execute('CREATE TABLE r AS SELECT rowid AS rid, * FROM t')
    tests = [_s4_tests(base, f, base.recs[ri]) for ri, f in free]
    n = 1
    for t in tests:
        n *= len(t)
    if n > 50000:
        raise Unparsed('SEM-04 test space too large')
    labels = set()
    for combo in itertools.product(*tests):
        for (ri, f), v in zip(free, combo):
            db.execute('UPDATE t SET %s = ? WHERE rowid = ?' % base.col[f], (v, ri + 1))
        labels.add(int(bool(db.execute('SELECT ' + sql).fetchone()[0])))
        if len(labels) > 1:
            break
    db.close()
    if len(labels) != 1:
        raise Undetermined('SEM-04 test values disagree')
    return labels.pop()


SOLVERS['S4'] = solve_s4


# ---------------------------------------------------------------- S2 event log: backward version-graph resolver
DATERE = r'\d{4}-\d{2}-\d{2}'
_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
           'november', 'december']


def log_entries(state, label='E'):
    """[(label, date, text)] in listed order. The entry date is the date written in the entry's own record
    (the gap between the previous entry text and this label, or failing that right after the text)."""
    s = _clean_markup(state)
    ms = list(re.finditer(r'\b(' + label + r'\d{1,3})\.\s+(.+?\.)(?=\s*["\'|<}\],\n]|\s*$)', s))
    out = []
    for k, m in enumerate(ms):
        a = ms[k - 1].end() if k else 0
        gap = re.findall(DATERE, s[a:m.start()])
        if gap and (k == 0 or len(gap) == 1 or True):
            d = gap[-1]
        else:
            b = ms[k + 1].start() if k + 1 < len(ms) else len(s)
            after = re.findall(DATERE, s[m.end():b])
            if not after:
                raise Unparsed('entry without date')
            d = after[0]
        out.append((m.group(1), D(d), m.group(2).rstrip('.')))
    return out


def date_range(dw, period):
    """SEM-11 date phrase -> (lo, hi) inclusive day range (None = open end), or raise Unparsed."""
    dw = dw.strip()
    m = re.fullmatch(r'(?:between|from) (' + DATERE + r') (?:and|to) (' + DATERE + r')', dw)
    if m:
        return D(m.group(1)), D(m.group(2))
    m = re.fullmatch(r'(' + DATERE + r') through (' + DATERE + r')', dw)
    if m:
        return D(m.group(1)), D(m.group(2))
    m = re.fullmatch(r'within (\d+) days after (' + DATERE + r')', dw)
    if m:
        d0 = D(m.group(2))
        return d0 + datetime.timedelta(days=1), d0 + datetime.timedelta(days=int(m.group(1)))
    m = re.fullmatch(r'in (' + '|'.join(_MONTHS) + r') (\d{4})', dw, re.I)
    if m:
        mo, y = _MONTHS.index(m.group(1).lower()) + 1, int(m.group(2))
        nxt = datetime.date(y + (mo == 12), mo % 12 + 1, 1)
        return datetime.date(y, mo, 1), nxt - datetime.timedelta(days=1)
    m = re.fullmatch(r'in (\d{4})', dw)
    if m:
        y = int(m.group(1))
        return datetime.date(y, 1, 1), datetime.date(y, 12, 31)
    m = re.fullmatch(r'(on or before|by|no later than|not after|on or after|no earlier than|not before|before|after|on) (' + DATERE + r')', dw)
    if m:
        w, d0 = m.group(1), D(m.group(2))
        one = datetime.timedelta(days=1)
        return {'on or before': (None, d0), 'by': (None, d0), 'no later than': (None, d0), 'not after': (None, d0),
                'on or after': (d0, None), 'no earlier than': (d0, None), 'not before': (d0, None),
                'before': (None, d0 - one), 'after': (d0 + one, None), 'on': (d0, d0)}[w]
    raise Unparsed('date phrase')


NAME = r"[A-Z][\w'-]*(?: (?:[A-Z][\w'-]*|de|van|von|da|di|le|la|del|der|ter|ten|al))*"
_PAST = {'renew': 'renewed', 'report': 'reported', 'file': 'filed', 'fail': 'failed', 'neglect': 'neglected',
         'omit': 'omitted', 'manage': 'managed', 'confirm': 'confirmed', 'deny': 'denied', 'refuse': 'refused',
         'decline': 'declined'}


class S2Base:
    def __init__(self, row):
        card = row['card']
        self.world = card_world(card)
        self.types = card_types(card)
        self.period = card_period(card)
        if not self.period:
            raise Unparsed('S2 no covered period')
        self.S = card_authority(card)
        self.T = '(?i:' + '|'.join(re.escape(t) for t in sorted(self.types, key=len, reverse=True)) + ')'
        self.ITEM = self.T + r' (?P<item>' + IDRE + r')'
        self.q = extract_question(row['instructions'].replace("What's the answer?", ' '))
        self.entries = collections.OrderedDict()
        for lab, d, txt in log_entries(row['state']):
            if lab in self.entries:
                raise Unparsed('duplicate entry label')
            self.entries[lab] = self._parse_entry(d, txt)

    def obj(self, s):
        """'<item>' | 'a <Z> for <item>' | 'the <Z> for <item>' -> (z, item)."""
        s = s.strip()
        m = re.fullmatch(r'(?:an?|the) (?P<z>.+?) for ' + self.ITEM, s)
        if m:
            return m.group('z').lower(), m.group('item')
        m = re.fullmatch(self.ITEM, s)
        if m:
            return '', m.group('item')
        raise Unparsed('S2 object')

    def _parse_entry(self, d, t):
        e = {'date': d, 'kind': None}
        I = self.ITEM
        pats = [
            ('create', I + r' was created for (?P<h>' + NAME + r')(?:, valid for (?P<n>\d+) days)?'),
            ('renew', r'(?P<a>' + NAME + r') renewed ' + I + r' for (?P<n>\d+) days?'),
            ('transfer', r'(?P<a>' + NAME + r') transferred ' + I + r' to (?P<h>' + NAME + r')'),
            ('report', r'(?P<a>' + NAME + r') reported (?:an?) (?P<z>.+?) for ' + I),
            ('file', r'(?P<a>' + NAME + r') filed the (?P<z>.+?) for ' + I),
            ('status', r'The status of ' + I + r' was set to (?P<v>.+)'),
            ('void', r'VOID of (?P<t>E\d+)'),
            ('corr', r'CORRECTION of (?P<t>E\d+): the (?P<f>number of days|status|holder|value) is (?P<v>.+)'),
            ('fail', r'(?P<a>' + NAME + r') (?P<c>failed|neglected|omitted|refused|declined|did not manage) to '
                     r'(?P<verb>renew|report|file) (?P<o>.+?)(?: by (?P<by>' + DATERE + r'))?'),
            ('fail', r'(?P<a>' + NAME + r') was prevented from (?P<verb>renewing|reporting|filing) (?P<o>.+?)'
                     r'(?: by (?P<by>' + DATERE + r'))?'),
            ('noevent', r'No (?P<verb>renewal|report|filing) of (?P<o>.+?) by (?P<a>' + NAME + r') took place '
                        r'from (?P<d1>' + DATERE + r') to (?P<d2>' + DATERE + r')'),
            ('notice', r'(?P<x>' + NAME + r') (?P<sv>stated|denied|confirmed) that (?P<claim>.+)'),
            ('notice', r'(?P<x>' + NAME + r') (?P<sv>ruled out) (?P<claim>.+)'),
        ]
        for kind, p in pats:
            m = re.fullmatch(p, t)
            if m:
                e['kind'] = kind
                e.update({k: v for k, v in m.groupdict().items() if v is not None})
                break
        if e['kind'] is None:
            raise Unparsed('S2 entry form')
        if e['kind'] == 'fail' or e['kind'] == 'noevent':
            verb = e['verb']
            e['ev'] = {'renewing': 'renew', 'reporting': 'report', 'filing': 'file', 'renewal': 'renew',
                       'filing ': 'file'}.get(verb, verb)
            if e['ev'] == 'renewal':
                e['ev'] = 'renew'
            e['z'], e['item'] = self.obj(e['o'])
        if 'z' in e:
            e['z'] = e['z'].lower()
        return e

    # -- backward version graph (SEM-16)
    def removed(self, lab, depth=0):
        if depth > 6:
            raise Unparsed('VOID chain too deep')
        for l2, e2 in self.entries.items():
            if e2['kind'] == 'void' and e2['t'] == lab and not self.removed(l2, depth + 1):
                return True
        return False

    def value(self, lab, field):
        e = self.entries[lab]
        for l2, e2 in self.entries.items():
            if e2['kind'] == 'corr' and e2['t'] == lab and not self.removed(l2):
                if field == 'n' and e2['f'] == 'number of days':
                    return int(re.match(r'\d+', e2['v']).group(0))
                if field == 'v' and e2['f'] == 'status':
                    return e2['v']
                if field == 'h' and e2['f'] == 'holder':
                    return e2['v']
        v = e.get(field)
        return int(v) if field == 'n' and v is not None else v

    def events(self, ev, item, actor, z):
        """Remaining listed events of the asked kind (actor None = agent-free)."""
        out = []
        for lab, e in self.entries.items():
            if e['kind'] != ev or e.get('item') != item:
                continue
            if actor is not None and e.get('a') != actor:
                continue
            if ev != 'renew' and e.get('z', '') != z:
                continue
            if not self.removed(lab):
                out.append(e['date'])
        return out

    def event_in_range(self, ev, item, actor, z, lo, hi):
        lo = max(lo or self.period[0], self.period[0])
        hi = min(hi or self.period[1], self.period[1])
        if any(lo <= d <= hi for d in self.events(ev, item, actor, z)):
            return True
        if self.world == 'closed':
            return False
        # open card: No only from an explicit statement by the authority covering every day of the range
        covered = set()
        for lab, e in self.entries.items():
            if self.removed(lab):
                continue
            if e['kind'] in ('fail', 'noevent') and e['ev'] == ev and e['item'] == item and e['z'] == z and \
                    (actor is None or e['a'] == actor):
                if e['kind'] == 'noevent':
                    a, b = D(e['d1']), D(e['d2'])
                else:
                    a, b = self.period[0], D(e['by']) if e.get('by') else self.period[1]
                covered.add((a, b))
        day = lo
        while day <= hi:
            if not any(a <= day <= b for a, b in covered):
                raise Undetermined('open card: event range not decided')
            day += datetime.timedelta(days=1)
        return False

    def valid_on(self, item, day):
        best = None
        for lab, e in self.entries.items():
            if e.get('item') != item or self.removed(lab):
                continue
            if e['kind'] == 'renew' or (e['kind'] == 'create' and e.get('n')):
                if e['date'] <= day and (best is None or e['date'] > best[0]):
                    best = (e['date'], self.value(lab, 'n'))
        if best is None:
            return False
        return day <= best[0] + datetime.timedelta(days=best[1])

    # -- question -> truth value (operators applied directly; NOT chain counted by the frame parser)
    def claim(self, x):
        x = x.strip()
        I = self.ITEM
        m = re.fullmatch(I + r' is (?P<asp>not |still |no longer )?valid(?: as of (?P<d>' + DATERE + r'))?', x)
        if m:
            if self.world == 'open':
                raise Undetermined('open card: state needs an as-of statement by the authority')
            day = D(m.group('d')) if m.group('d') else self.period[1]
            now = self.valid_on(m.group('item'), day)
            asp = (m.group('asp') or '').strip()
            before = any(self.valid_on(m.group('item'), self.period[0] + datetime.timedelta(days=k))
                         for k in range((day - self.period[0]).days))
            return {'': now, 'not': not now, 'still': before and now, 'no longer': before and not now}[asp]
        m = re.fullmatch(I + r' was (?P<neg>not )?(?P<v>renewed) by (?P<a>' + NAME + r')(?: (?P<dw>(?:on|before|after|by|no|not|between|from|within|in|' + DATERE + r').*))?', x)
        if m:
            lo, hi = date_range(m.group('dw'), self.period) if m.group('dw') else (None, None)
            r = self.event_in_range('renew', m.group('item'), m.group('a'), '', lo, hi)
            return (not r) if m.group('neg') else r
        m = re.fullmatch(r'(?P<a>' + NAME + r') (?P<c>did not fail to |did not manage to |managed to |failed to |neglected to |'
                         r'omitted to |never |did not )?(?P<v>renew|renewed|report|reported|file|filed) (?P<rest>.+)', x)
        if m:
            v = m.group('v')
            ev = {'renewed': 'renew', 'reported': 'report', 'filed': 'file'}.get(v, v)
            mm = re.fullmatch(r'(?P<o>.*?' + IDRE + r')(?: (?P<dw>.+))?', m.group('rest'))
            if not mm:
                raise Unparsed('S2 event object')
            z, item = self.obj(mm.group('o'))
            c = (m.group('c') or '').strip()
            dw = mm.group('dw')
            if c in ('failed to', 'neglected to', 'omitted to', 'did not manage to', 'did not fail to', 'managed to'):
                if dw and not re.fullmatch(r'by ' + DATERE, dw):
                    raise Unparsed('C3 with another time')
                hi = D(dw[3:]) if dw else self.period[1]
                happened = self.event_in_range(ev, item, m.group('a'), z, None, hi)
                return happened if c in ('did not fail to', 'managed to') else (not happened)
            if c == 'never':
                if dw and not re.fullmatch(r'as of ' + DATERE, dw):
                    raise Unparsed('never with another time')
                hi = D(dw[6:]) if dw else self.period[1]
                return not self.event_in_range(ev, item, m.group('a'), z, None, hi)
            lo, hi = date_range(dw, self.period) if dw else (None, None)
            r = self.event_in_range(ev, item, m.group('a'), z, lo, hi)
            return (not r) if c == 'did not' else r
        raise Unparsed('S2 claim form')


def s2_direct(x):
    """Direct S2 interrogative -> declarative."""
    m = re.fullmatch(r'Did (?P<a>' + NAME + r') (?P<v>renew|report|file|fail|neglect|omit|manage) (?P<rest>.+)', x)
    if m:
        v = _PAST[m.group('v')]
        return '%s %s %s' % (m.group('a'), v, m.group('rest'))
    m = re.fullmatch(r'Was (?P<i>.+?) (?P<v>renewed) by (?P<rest>.+)', x)
    if m:
        return '%s was renewed by %s' % (m.group('i'), m.group('rest'))
    m = re.fullmatch(r'Is (?P<i>.+?) (?P<p>(?:still |no longer )?valid.*)', x)
    if m:
        return '%s is %s' % (m.group('i'), m.group('p'))
    raise Unparsed('S2 direct form')


def solve_s2(row):
    base = S2Base(row)
    nout, body, direct = strip_frames(base.q)
    if direct:
        x, nin = s2_direct(body), 0
    else:
        nin, x = strip_embedded_neg(body)
    v = base.claim(x)
    if (nout + nin) % 2:
        v = not v
    return int(v)


SOLVERS['S2'] = solve_s2


# ---------------------------------------------------------------- S5 thread: constraint check over parsed statements
def thread_messages(state):
    s = _clean_markup(state)
    out = collections.OrderedDict()
    for m in re.finditer(r'\b(M\d+)\.\s+(' + DATERE + r'),\s+(.+?) wrote:\s+(.+?\.)(?=\s*(?:["\'|<}\],\n]|M\d+\.\s|$))', s):
        lab = m.group(1)
        if lab in out:
            raise Unparsed('duplicate message label')
        out[lab] = (D(m.group(2)), m.group(3).strip(), m.group(4).strip().rstrip('.'))
    n = len(set(re.findall(r'\bM\d+\.\s+' + DATERE, s)))
    if not out or n != len(out):
        raise Unparsed('S5 message layout')
    return out


class S5Base:
    def __init__(self, row):
        card = row['card']
        self.world = card_world(card)
        self.lex = Lex(card)
        self.S = card_authority(card)
        self.period = card_period(card)
        if not self.S or not self.period:
            raise Unparsed('S5 card constants')
        self.q = extract_question(row['instructions'].replace("What's the answer?", ' '))
        self.msgs = thread_messages(row['state'])
        self.stmts = {}       # label -> (date, sender, entity, adj, polarity) after own corrections; retracted removed
        retracted, corrected = set(), {}
        for lab, (d, snd, txt) in self.msgs.items():
            m = re.fullmatch(r'I retract (M\d+)', txt)
            if m:
                tgt = m.group(1)
                if tgt not in self.msgs or self.msgs[tgt][1] != snd:
                    raise Unparsed('retraction of another sender')
                retracted.add(tgt)
                continue
            m = re.fullmatch(r'Correction to (M\d+): (.+)', txt)
            if m:
                tgt = m.group(1)
                if tgt not in self.msgs or self.msgs[tgt][1] != snd:
                    raise Unparsed('correction of another sender')
                corrected[tgt] = m.group(2)
                continue
        for lab, (d, snd, txt) in self.msgs.items():
            if lab in retracted or re.match(r'(?:I retract|Correction to) ', txt):
                continue
            txt = corrected.get(lab, txt)
            m = re.fullmatch(self.lex.ENT + r' (?P<vp>is .+)', txt)
            if not m:
                raise Unparsed('S5 message content')
            f = self.lex.vp(m.group('id'), m.group('vp'))
            pol = True
            if f[0] == 'not':
                f, pol = f[1], False
            if f[0] != 'atom':
                raise Unparsed('S5 compound message')
            self.stmts[lab] = (d, snd, f[1], pol)

    def latest(self, sender, key, day):
        cand = [(d, pol) for (d, snd, k, pol) in self.stmts.values() if snd == sender and k == key and d <= day]
        if not cand:
            return None
        dmax = max(d for d, _ in cand)
        pols = {p for d, p in cand if d == dmax}
        if len(pols) != 1:
            raise Unparsed('two same-day statements')
        return pols.pop()

    def fact(self, f, day):
        """Evaluate a formula over fact atoms by <S>'s latest remaining message per fact."""
        def fn(key):
            v = self.latest(self.S, key, day)
            if v is None and self.world == 'closed':
                return False                # SEM-02: an unstated positive statement is false
            return v                        # open card: unknown stays an atom (every model considered)
        g = subst(f, fn)
        v = kleene(g, {})
        if v is None:
            # open world: the formula is determined only if every assignment of the unknown atoms agrees
            free = sorted(atoms_of(g), key=str)
            vals = {kleene(g, dict(zip(free, bits))) for bits in itertools.product([True, False], repeat=len(free))}
            if len(vals) != 1:
                raise Undetermined('open card: no authority message decides the claim')
            v = vals.pop()
        return v


def solve_s5(row):
    base = S5Base(row)
    day = base.period[1]
    nout, body, direct = strip_frames(base.q)
    nin = 0
    if direct:
        m = re.fullmatch(r'Did (?P<x>' + NAME + r') (?P<v>confirm|deny) that (?P<c>.+)', body)
        if m:
            x = '%s %s that %s' % (m.group('x'), _PAST[m.group('v')], m.group('c'))
        else:
            x = None
    else:
        nin, x = strip_embedded_neg(body)
    stance = re.fullmatch(r'(?P<x>' + NAME + r') (?P<neg>did not )?(?P<v>denied|deny|confirmed|confirm|ruled out|rule out)'
                          r'(?: that)? (?P<c>.+)', x) if x else None
    if stance:
        if base.world != 'closed':
            raise Unparsed('stance question on open card')
        party = stance.group('x')
        if party == base.S:
            raise Unparsed('stance question names the authority')
        mc = re.fullmatch(base.lex.ENT + r' (?P<vp>is .+)', stance.group('c'))
        if not mc:
            raise Unparsed('S5 stance claim')
        c = base.lex.vp(mc.group('id'), mc.group('vp'))
        cpol = True
        if c[0] == 'not':
            c, cpol = c[1], False
        if c[0] != 'atom':
            raise Unparsed('S5 compound stance claim')
        last = base.latest(party, c[1], day)
        v = stance.group('v')
        if last is None:
            val = False
        elif v.startswith('confirm'):
            val = (last == cpol)
        else:
            val = (last != cpol)
        if stance.group('neg'):
            val = not val
    else:
        f = lf_entity(base.q, base.lex, collections.OrderedDict(
            (mm.group('id'), mm.group('type').lower()) for mm in re.finditer(base.lex.ENT, base.q)))
        g = base.fact(f, day)
        if g is not True and g is not False:
            raise Unparsed('S5 fact formula not closed')
        return int(g)
    if (nout + nin) % 2:
        val = not val
    return int(val)


SOLVERS['S5'] = solve_s5


# ---------------------------------------------------------------- spec item labels (for the mismatch file; no row text)
_SAMPLER_ITEM = {
    'S1': 'G0 5 S1 rule-case (SEM-02/03 world, SEM-05/06/07/15 rules, SEM-24 deontic closure, SEM-04 test values)',
    'S2': 'G0 5 S2 event log (SEM-11 date words, SEM-16 CORRECTION/VOID, SEM-19 C3, SEM-33 validity, open-card No rule)',
    'S3': 'G0 5 S3 fact graph (SEM-22 quantifiers, SEM-02/03 world, universals grounded over named entities)',
    'S4': 'G0 5 S4 records (SEM-08/09/22/23/25 compiled to SQL, SEM-04 test values, blank yes/no = no)',
    'S5': 'G0 5 S5 thread (SEM-31 latest remaining authority message, SEM-20 stance)',
}
_CUES = [('C2', r'\bit is (?:not the case|false) that\b|^Is it false that'), ('C3', r'\b(?:failed|neglected|omitted|did not manage|did not fail) to\b|\bnever\b'),
         ('C5', r'\b(?:lacks?|without|free of|does not have)\b'), ('C8', r'\b(?:no|not every|not all|every|all|some|any)\b'),
         ('C9', r'\b(?:at least|at most|no fewer than|no more than|more than|fewer than|half)\b'),
         ('C10', r'\b(?:by|before|after|on or before|on or after|no later than|no earlier than|not before|not after|between|within|through)\b \d{4}'),
         ('C11', r'\b(?:other than|only)\b'), ('C12', r'\b(?:must|may|need not|required to|permitted to|have to)\b'),
         ('C13', r'\bneither\b|\bnot both\b'), ('C14', r'\b(?:hardly any|scarcely any|few|barely)\b'),
         ('C16', r'\bnot only\b'), ('C7', r'\b(?:denied|confirmed|confirm|deny|ruled out)\b'), ('C1', r'\bnot\b')]


def spec_item(row):
    q = extract_question(row['instructions'].replace("What's the answer?", ' '))
    fams = [c for c, p in _CUES if re.search(p, q)]
    return _SAMPLER_ITEM.get(row['meta']['sampler'], '?') + '; question cues ' + (','.join(fams) or 'none')


# ---------------------------------------------------------------- S2 boundary checks (F5-R4-02 one side; F5-R5-02 at least one event)
def s2_flags(row):
    """Spec assertions solver B re-checks on its own parse. Returns list of flag names (empty = clean)."""
    try:
        base = S2Base(row)
    except Unparsed:
        return []
    nout, body, direct = strip_frames(base.q)
    x = s2_direct(body) if direct else strip_embedded_neg(body)[1]
    m = re.fullmatch(r'(?P<a>' + NAME + r') (?:did not |never )?(?P<v>renew|renewed|report|reported|file|filed) (?P<o>.*?' + IDRE +
                     r') (?P<dw>(?:on|before|after|no|not|between|from|within|in|' + DATERE + r').*)', x)
    if not m:
        m2 = re.fullmatch(base.ITEM + r' was renewed by (?P<a>' + NAME + r') (?P<dw>.+)', x)
        if not m2:
            return []
        ev, actor, z, item, dw = 'renew', m2.group('a'), '', m2.group('item'), m2.group('dw')
    else:
        v = m.group('v')
        ev = {'renewed': 'renew', 'reported': 'report', 'filed': 'file'}.get(v, v)
        actor, dw = m.group('a'), m.group('dw')
        z, item = base.obj(m.group('o'))
    try:
        lo, hi = date_range(dw, base.period)
    except Unparsed:
        return []
    ds = base.events(ev, item, actor, z)
    flags = []
    if not ds:
        flags.append('F5-R5-02 no remaining listed event of the asked kind')
    if lo is not None and len({d < lo for d in ds}) > 1:
        flags.append('F5-R4-02 events on both sides of the lower boundary')
    if hi is not None and len({d <= hi for d in ds}) > 1:
        flags.append('F5-R4-02 events on both sides of the upper boundary')
    return flags


def main():
    t0 = datetime.datetime.now(datetime.timezone.utc)
    res, mism, unparsed = run()
    rowmeta = {}
    flags = collections.Counter()
    flag_ids = collections.defaultdict(list)
    per_file = collections.Counter()
    for fn in FILES:
        for line in open(os.path.join(OUT, fn)):
            row = json.loads(line)
            per_file[fn] += 1
            rowmeta[(fn, row['id'])] = spec_item(row)
            if row['meta']['sampler'] == 'S2':
                for f in s2_flags(row):
                    flags[f] += 1
                    flag_ids[f].append(row['id'])
    for m in mism:
        m['spec_item'] = rowmeta[(m['file'], m['id'])]
    for u in unparsed:
        u['spec_item'] = rowmeta[(u['file'], u['id'])]
    total = sum(per_file.values())
    agree = sum(v for (s, k), v in res.items() if k == 'agree')
    out = {
        'solver': 'F5 solver B (model enumeration / sqlite / backward version graph / thread constraints)',
        'spec': 'c_src/F5/G0_SPEC.md (frozen sha256 in G0_FROZEN.json)',
        'utc': t0.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'files': dict(per_file),
        'rows_checked': total,
        'agree': agree,
        'agree_pct': round(100.0 * agree / total, 3) if total else 0.0,
        'n_mismatch': len([m for m in mism if m['gold_B'] is not None]),
        'n_undetermined': len([m for m in mism if m['gold_B'] is None]),
        'n_unparsed': len(unparsed),
        'by_sampler': {'%s:%s' % k: v for k, v in sorted(res.items())},
        'mismatches': mism,
        'unparsed': unparsed,
        'spec_flags': {k: {'count': v, 'ids': flag_ids[k][:200]} for k, v in flags.items()},
    }
    with open(os.path.join(HERE, 'mismatch.json'), 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in ('rows_checked', 'agree', 'agree_pct', 'n_mismatch', 'n_undetermined',
                                          'n_unparsed', 'by_sampler')}, indent=1))
    print('spec_flags', dict(flags))


if __name__ == '__main__':
    main()
