"""F4 logic core and solver A (G0 spec sections 2-3, 7.2). Runs on the SAMPLED structure only.

Structure (as written): types, entities, rules (conditions keep their written operator and ends), statements with
provenance (sentence / table cell / attribution frame), unknown markers, closures, hedges, look-alike pairs, the
card's source map and flag vector.

Solver A:
  OW  ground rules over named entities by their one type; directed instances = each clause literal (the link-negating
      contrapositive never arises: links occur only positively and unstated links are pure); label by refutation with
      unit propagation (complete because the theory is Horn-renamable, checked by the 2-SAT renaming test);
      direct derivability and guards 9a/9b checked on UP(T).
  CW  stratified least model by recursive evaluation over the acyclic ground program (negation as failure on lower
      strata; negative-head rules and stated negative facts are constraints).
  Rivals: each rival builds its own reading (View) and is labelled with a small DPLL (OW-type readings) or the CW
      least model (CW-type readings), per G0 7.2.
Values use Decimal and datetime.date. Code shared with solver B: none (solver_b.py reads the parsed canonical form).
"""
from __future__ import annotations

import datetime as dt
import itertools
from dataclasses import dataclass, field
from decimal import Decimal

# ------------------------------------------------------------------------------------------------------- structure


@dataclass
class Rule:
    rid: str
    form: str                 # univ | neguniv | link | onlyif | kofn | or | xor
    typ: int                  # subject type index
    conds: tuple = ()         # written conditions (see cond kinds below); onlyif: ((lit, A, True),)
    head: tuple = None        # (pred, pos); onlyif: (A, True) (logic H -> A); neguniv: (H, False)
    ante: str = None          # onlyif: H
    exc: str = None           # exception predicate (univ / neguniv only)
    link: int = None          # link index (link rules)
    ptyp: int = None          # partner type index
    pcond: tuple = None       # (pred, pos) on the partner
    k: int = 0                # k of n
    where: str = "record"     # record | card (standing rule, clause 25a)
    style: dict = field(default_factory=dict)   # rendering hints only (quantifier, exception word, cue, phrases)

# condition kinds (as written):
#   ("lit", pred, pos)         ("cmp", qty, op, T)   op in >= > <= <, T Decimal
#   ("rng", qty, T1, T2)       ("dcmp", attr, op, D) D date        ("win", attr, D1, D2)


@dataclass
class Stmt:
    sid: str
    kind: str                 # lit | val | date | link | type
    e: str
    pred: str = None          # lit: predicate; val: quantity; date: attribute; link: link index (int)
    pos: bool = None          # lit: polarity; None = unknown marker ("not recorded" / null)
    value: object = None      # val: Decimal or None (marker); date: date or None; link: partner id
    src: str = None           # attribution source name (None = unattributed)
    frame: str = None         # colon | quote | reported
    via: str = "sent"         # sent | cell | attr
    tid: str = None           # table id when via == cell
    group: str = None         # sentence id for conjoined fact sentences / table row
    tag: str = None           # inert / carrier kind when this statement is an addition (I1, V3, V4 ...)


@dataclass
class Card:
    world: str                # OW | CW | None (short card)
    unless: str               # strict | listc | cw | none | None
    trust: tuple              # ("list", (names...)) | ("all",) | None
    clauses: frozenset        # printed clause ids
    short: bool = False


@dataclass
class Record:
    types: list               # [(sg, pl)]
    ents: dict                # id -> type index
    preds: dict               # pred -> type index (the one type that carries it)
    exc_preds: set
    rules: list
    stmts: list
    closures: list            # [(pred, typ, form("prose"|"column"), tid)]
    hedges: list = field(default_factory=list)    # [(kind, typ, (cpred, cpos), (hpred, hpos))]; kind most..notevery|exist
    ehedges: list = field(default_factory=list)   # [(kind, e, pred)]
    lookalikes: list = field(default_factory=list)
    links: list = field(default_factory=list)     # pack links [{"active","passive","from","to"}]
    qtys: dict = field(default_factory=dict)      # qty name -> {"unit", "dec"}
    dattrs: list = field(default_factory=list)
    blank_cells: list = field(default_factory=list)  # [(pred, e, tid)] blank cells of closed columns
    extras: dict = field(default_factory=dict)    # background, topic line, injection, tables (rendering)


# ------------------------------------------------------------------------------------------------------- views

@dataclass
class View:
    world: str                # OW | CW
    unless: str               # strict | listc | cw | none
    facts: dict               # atom -> bool (stated as fact)
    links: set                # {(li, e1, e2)}
    values: dict              # (e, qty) -> Decimal | None (missing)
    dates: dict               # (e, attr) -> date | None
    rules: list               # Rule objects (possibly rival-modified copies)
    closures: list            # [(pred, typ)] record-level closures
    ents: dict
    exc_preds: set
    missing_false: bool = False       # R10 / R1-on-OW: every written condition on a missing value is false
    marker_false: set = field(default_factory=set)   # atoms whose container marker reads as No (R10)
    ground_all: bool = False          # R31
    extra: list = field(default_factory=list)        # extra formulas: ("or_of_ands", [[lits]...]) etc.
    cw_mode: str = "plain"            # plain | conj (R3 CW) | strict (R5 CW)
    blank_unknown: bool = False       # R23 (blank closed cells become unknown) - closures dropped too
    markers: set = field(default_factory=set)        # atoms with a container unknown marker


def u(pred, e):
    return ("u", pred, e)


def lk(li, a, b):
    return ("l", li, a, b)


def cmp_literal(cond, e, view, flips=None):
    """(literal, const): const True/False when the written condition is decided by a known value (or forced false
    on a missing value under R10 / R1-OW), else (atom literal, None)."""
    kind = cond[0]
    if kind == "cmp":
        _, q, op, T = cond
        v = view.values.get((e, q), "absent")
        if v is None or v == "absent":
            if view.missing_false or view.world == "CW":
                return None, False
            ak = "gt" if op in (">", "<=") else "ge"
            pos = op in (">", ">=")
            return (("c", q, ak, T, e), pos), None
        res = {">": v > T, ">=": v >= T, "<": v < T, "<=": v <= T}[op]
        return None, res
    if kind == "rng":
        _, q, T1, T2 = cond[:4]
        inc = cond[4] if len(cond) > 4 else (True, True)
        v = view.values.get((e, q), "absent")
        if v is None or v == "absent":
            if view.missing_false or view.world == "CW":
                return None, False
            return (("r", q, T1, T2, inc[0], inc[1], e), True), None
        lo = v >= T1 if inc[0] else v > T1
        hi = v <= T2 if inc[1] else v < T2
        return None, lo and hi
    if kind == "dcmp":
        _, a, op, D = cond
        v = view.dates.get((e, a), "absent")
        if v is None or v == "absent":
            if view.missing_false or view.world == "CW":
                return None, False
            ak = "gt" if op in (">", "<=") else "ge"
            pos = op in (">", ">=")
            return (("d", a, ak, D, e), pos), None
        res = {">": v > D, ">=": v >= D, "<": v < D, "<=": v <= D}[op]
        return None, res
    if kind == "win":
        _, a, D1, D2 = cond[:4]
        inc = cond[4] if len(cond) > 4 else (True, True)
        v = view.dates.get((e, a), "absent")
        if v is None or v == "absent":
            if view.missing_false or view.world == "CW":
                return None, False
            return (("w", a, D1, D2, inc[0], inc[1], e), True), None
        lo = v >= D1 if inc[0] else v > D1
        hi = v <= D2 if inc[1] else v < D2
        return None, lo and hi
    raise ValueError(kind)


def cond_literal(cond, e, view):
    if cond[0] == "lit":
        return (u(cond[1], e), cond[2]), None
    return cmp_literal(cond, e, view)


def ents_of(view, typ):
    if view.ground_all:
        return sorted(view.ents)
    return sorted(x for x, t in view.ents.items() if t == typ)


def subjects(view, r):
    skip = r.style.get("_skip", ()) if isinstance(r.style, dict) else ()
    return [x for x in ents_of(view, r.typ) if x not in skip]


def ground_bodies(rule, x, view):
    """[(body literals, exc literal or None, head literal)] for subject x; bodies with a false constant are dropped,
    true constants are removed. Each item also carries an instance kind tag."""
    out = []
    head = (u(rule.head[0], x), rule.head[1])

    def conj(conds):
        lits = []
        for c in conds:
            lit, const = cond_literal(c, x, view)
            if const is False:
                return None
            if const is True:
                continue
            lits.append(lit)
        return lits
    if rule.form in ("univ", "neguniv"):
        b = conj(rule.conds)
        if b is not None:
            out.append((b, (u(rule.exc, x), True) if rule.exc else None, head, "body"))
    elif rule.form == "link":
        for (li, a, y) in sorted(view.links):
            if li != rule.link or a != x:
                continue
            if not view.ground_all and view.ents.get(y) != rule.ptyp:
                continue
            if y not in view.ents:
                continue
            out.append(([(u(rule.pcond[0], y), rule.pcond[1])], None, head, f"link:{y}"))
    elif rule.form == "onlyif":
        out.append(([(u(rule.ante, x), True)], None, (u(rule.head[0], x), True), "onlyif"))
    elif rule.form == "kofn":
        for S in itertools.combinations(range(len(rule.conds)), rule.k):
            b = conj([rule.conds[i] for i in S])
            if b is not None:
                out.append((b, None, head, "kofn:" + ",".join(map(str, S))))
    elif rule.form == "or":
        for i, c in enumerate(rule.conds):
            b = conj([c])
            if b is not None:
                out.append((b, None, head, f"or:{i}"))
    elif rule.form == "xor":
        a, b_ = rule.conds
        for i, (p, q) in enumerate(((a, b_), (b_, a))):
            lp, cp = cond_literal(p, x, view)
            lq, cq = cond_literal(q, x, view)
            if cp is False or cq is True:
                continue
            body = []
            if cp is None:
                body.append(lp)
            if cq is None:
                body.append((lq[0], not lq[1]))
            out.append((body, None, head, f"xor:{i}"))
    elif rule.form == "xor_both_not":   # R18 addition: (A ^ B) -> not H
        b = conj(rule.conds)
        if b is not None:
            out.append((b, None, head, "xorboth"))
    elif rule.form == "exactk":         # R14 reading
        n = len(rule.conds)
        for S in itertools.combinations(range(n), rule.k):
            body = []
            ok = True
            for i in range(n):
                lit, const = cond_literal(rule.conds[i], x, view)
                want = i in S
                if const is not None:
                    if const != want:
                        ok = False
                        break
                    continue
                body.append(lit if want else (lit[0], not lit[1]))
            if ok:
                out.append((body, None, head, "exactk"))
    else:
        raise ValueError(rule.form)
    return out


def neg(lit):
    return (lit[0], not lit[1])


@dataclass
class Ground:
    units: dict               # atom -> bool
    clauses: list             # [(lits tuple, meta)]  meta = (rid, x, kind, head_index)
    view: View


def ground(view: View) -> Ground:
    units = {}
    for a, v in view.facts.items():
        units[a] = v
    # record-level closures: not C(e) for each named e of the closure type with no stated C fact
    for (pred, typ) in view.closures:
        for e, t in sorted(view.ents.items()):
            if t != typ:
                continue
            a = u(pred, e)
            if a not in view.facts:
                units[a] = False
    # list-complete: every exception predicate closed for every entity
    if view.unless == "listc":
        for r in view.rules:
            if r.exc:
                for e in view.ents:
                    a = u(r.exc, e)
                    if a not in view.facts and a not in units:
                        units[a] = False
    for a in view.marker_false:
        if a not in units:
            units[a] = False
    clauses = []
    for r in view.rules:
        for x in subjects(view, r):
            for body, exc, head, kind in ground_bodies(r, x, view):
                lits = [neg(b) for b in body]
                if exc is not None:
                    lits.append(exc)     # (C(x), True): the clause is  not body v C v head
                lits.append(head)
                clauses.append((tuple(lits), (r.rid, x, kind, len(lits) - 1, exc is not None)))
    return Ground(units, clauses, view)


# ------------------------------------------------------------------------------------------------------- UP

def unit_propagate(units: dict, clauses: list, extra: dict | None = None):
    """Returns (assign, conflict, reason) where reason[atom] = clause index that set it (None for units)."""
    assign = dict(units)
    reason = {a: None for a in assign}
    if extra:
        for a, v in extra.items():
            if a in assign and assign[a] != v:
                return assign, True, reason
            assign[a] = v
            reason[a] = "assume"
    watch = {}
    for i, (lits, _) in enumerate(clauses):
        for (a, _) in lits:
            watch.setdefault(a, []).append(i)
    queue = list(range(len(clauses)))
    inq = set(queue)
    while queue:
        i = queue.pop()
        inq.discard(i)
        lits = clauses[i][0]
        unassigned = None
        n_un = 0
        sat = False
        for (a, p) in lits:
            v = assign.get(a)
            if v is None:
                n_un += 1
                unassigned = (a, p)
                if n_un > 1:
                    break
            elif v == p:
                sat = True
                break
        if sat or n_un > 1:
            continue
        if n_un == 0:
            return assign, True, reason
        a, p = unassigned
        assign[a] = p
        reason[a] = i
        for j in watch.get(a, ()):
            if j not in inq:
                inq.add(j)
                queue.append(j)
    return assign, False, reason


def is_exc_atom(a, view):
    return a[0] == "u" and a[1] in view.exc_preds


def is_cmp_atom(a):
    return a[0] in ("c", "r", "d", "w")


def label_ow_up(g: Ground, claim):
    """Refutation label for claim literal ((atom), pos): F / R / O ; X when T itself is inconsistent."""
    base, conf, _ = unit_propagate(g.units, g.clauses)
    if conf:
        return "X"
    _, c1, _ = unit_propagate(g.units, g.clauses, {claim[0]: not claim[1]})
    _, c2, _ = unit_propagate(g.units, g.clauses, {claim[0]: claim[1]})
    if c1 and c2:
        return "X"
    if c1:
        return "F"
    if c2:
        return "R"
    return "O"


# ------------------------------------------------------------------------------------------------------- DPLL

def dpll_sat(units: dict, clauses: list) -> bool:
    """Plain DPLL with unit propagation over clauses [(lits, meta)]."""
    assign, conf, _ = unit_propagate(units, clauses)
    if conf:
        return False
    # pick an unassigned atom from an unsatisfied clause
    for lits, _ in clauses:
        if any(assign.get(a) == p for a, p in lits):
            continue
        for a, p in lits:
            if a not in assign:
                for val in (p, not p):
                    u2 = dict(assign)
                    u2[a] = val
                    if dpll_sat(u2, clauses):
                        return True
                return False
    return True


def component(clauses, atoms):
    """Clauses connected (through shared free atoms) to any of `atoms`."""
    by_atom = {}
    for i, (lits, _) in enumerate(clauses):
        for a, _ in lits:
            by_atom.setdefault(a, []).append(i)
    seen_c, seen_a = set(), set(atoms)
    stack = list(atoms)
    while stack:
        a = stack.pop()
        for i in by_atom.get(a, ()):
            if i in seen_c:
                continue
            seen_c.add(i)
            for b, _ in clauses[i][0]:
                if b not in seen_a:
                    seen_a.add(b)
                    stack.append(b)
    return [clauses[i] for i in sorted(seen_c)]


def label_ow_dpll(units, clauses, claim):
    """Entailment label by DPLL: X if no model at all."""
    if not dpll_sat(units, clauses):
        return "X"
    comp = component(clauses, [claim[0]])
    u1 = dict(units)
    if claim[0] in u1:
        v = u1[claim[0]]
        return "F" if v == claim[1] else "R"
    sat_not = dpll_sat({**units, claim[0]: not claim[1]}, comp)
    sat_yes = dpll_sat({**units, claim[0]: claim[1]}, comp)
    if not sat_not and not sat_yes:
        return "X"
    if not sat_not:
        return "F"
    if not sat_yes:
        return "R"
    return "O"


# ------------------------------------------------------------------------------------------------------- Horn renaming

def horn_renamable(units: dict, clauses: list) -> bool:
    """2-SAT test: exists a renaming s.t. every clause (after removing assigned atoms) has <= 1 positive literal.
    Variable r_a = True means atom a is renamed (flipped). Literal (a, p) is positive after renaming iff p xor r_a."""
    assign, conf, _ = unit_propagate(units, clauses)
    if conf:
        return True
    imp = {}
    atoms = set()

    def add(x, y):   # implication x -> y over 2-SAT literals (atom, val)
        imp.setdefault(x, set()).add(y)
    for lits, _ in clauses:
        if any(assign.get(a) == p for a, p in lits):
            continue
        free = [(a, p) for a, p in lits if a not in assign]
        for (a, p), (b, q) in itertools.combinations(free, 2):
            # not (posA and posB): posA = (r_a != p)  ->  clause (r_a == p) or (r_b == q)
            # 2-SAT literals: ("r", a, val) meaning r_a == val
            la, lb = (a, p), (b, q)
            add((a, not p), lb)
            add((b, not q), la)
            atoms.add(a)
            atoms.add(b)
    # SCC check via Kosaraju
    nodes = [(a, v) for a in atoms for v in (True, False)]
    idx = {n: i for i, n in enumerate(nodes)}
    order, seen = [], set()
    for n in nodes:
        if n in seen:
            continue
        stack = [(n, iter(imp.get(n, ())))]
        seen.add(n)
        while stack:
            v, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                order.append(v)
            elif nxt not in seen:
                seen.add(nxt)
                stack.append((nxt, iter(imp.get(nxt, ()))))
    rev = {}
    for x, ys in imp.items():
        for y in ys:
            rev.setdefault(y, set()).add(x)
    comp = {}
    for n in reversed(order):
        if n in comp:
            continue
        stack = [n]
        comp[n] = n
        while stack:
            v = stack.pop()
            for w in rev.get(v, ()):
                if w not in comp:
                    comp[w] = n
                    stack.append(w)
    for a in atoms:
        if comp.get((a, True)) == comp.get((a, False)):
            return False
    return True


# ------------------------------------------------------------------------------------------------------- derivations

def derivation_costs(g: Ground, assign: dict, view: View):
    """Min proof size for every literal in UP(T): cost 0 for units (facts, closures, list-complete), 1 per rule
    instance. Returns cost dict lit -> (cost, clause index or None, body lits)."""
    cost = {}
    for a, v in g.units.items():
        cost[(a, v)] = (0, None, ())
    changed = True
    rounds = 0
    while changed and rounds < 200:
        changed = False
        rounds += 1
        for i, (lits, meta) in enumerate(g.clauses):
            for j, (a, p) in enumerate(lits):
                if assign.get(a) != p:
                    continue
                others = [neg(l) for k, l in enumerate(lits) if k != j]
                if not all(assign.get(o[0]) == o[1] for o in others):
                    continue
                if not all(o in cost for o in others):
                    continue
                c = 1 + sum(cost[o][0] for o in others)
                if (a, p) not in cost or c < cost[(a, p)][0]:
                    cost[(a, p)] = (c, (i, j), tuple(others))
                    changed = True
    return cost


def proof_instances(cost, lit):
    """Instances (clause index, conclusion position) used by the min-cost proof of lit."""
    out = []
    stack = [lit]
    seen = set()
    while stack:
        l = stack.pop()
        if l in seen or l not in cost:
            continue
        seen.add(l)
        c, inst, body = cost[l]
        if inst is not None:
            out.append(inst)
            stack.extend(body)
    return out, seen


def instance_kind(g: Ground, inst):
    """forward | contra | partner (link partner-side contrapositive) | exc (concludes the exception atom)."""
    i, j = inst
    lits, meta = g.clauses[i]
    rid, x, kind, head_pos, has_exc = meta
    if j == head_pos:
        return "forward"
    if has_exc and j == head_pos - 1:
        return "exc"
    if kind.startswith("link:"):
        return "partner"
    return "contra"


# ------------------------------------------------------------------------------------------------------- CW model

def cw_model(view: View):
    """Least model of the stratified ground program. Returns (true atoms set, ok, support) where support[a] = list of
    (rid, kind, body lits) instances whose body holds. ok False when a constraint fails (no model)."""
    stated_pos = {a for a, v in view.facts.items() if v and a[0] == "u"}
    stated_neg = {a for a, v in view.facts.items() if not v and a[0] == "u"}
    by_head = {}
    neg_rules = []
    for r in view.rules:
        for x in subjects(view, r):
            for body, exc, head, kind in ground_bodies(r, x, view):
                if r.form == "onlyif":
                    continue   # OW only
                if head[1]:
                    by_head.setdefault(head[0], []).append((r, x, body, exc, kind))
                else:
                    neg_rules.append((r, x, body, exc, head, kind))
    memo = {}
    visiting = set()

    def exc_holds(exc):
        if exc is None:
            return False
        a = exc[0]
        if view.cw_mode == "strict":
            if a in stated_pos:
                return True
            if a in stated_neg:
                return False
            return None          # unsettled: rule unusable
        return a in stated_pos

    def val(a):
        if a[0] == "l":
            return (a[1], a[2], a[3]) in view.links
        if a[0] != "u":
            raise ValueError("free comparison atom in CW")
        if a in memo:
            return memo[a]
        if a in visiting:
            raise ValueError("cycle")
        visiting.add(a)
        res = a in stated_pos
        insts = by_head.get(a, [])
        if not res and insts:
            if view.cw_mode == "conj":
                # R3 CW: derived iff every rule for the head has a ground body that holds
                rids = {}
                for (r, x, body, exc, kind) in insts:
                    eh = exc_holds(exc)
                    ok = (eh is False) and all(val(b[0]) == b[1] for b in body)
                    rids[r.rid] = rids.get(r.rid, False) or ok
                rules_for = {r.rid for r in view.rules if r.head == (a[1], True) and r.form != "onlyif"
                             and (view.ground_all or view.ents.get(a[2]) == r.typ)}
                res = bool(rules_for) and all(rids.get(rid, False) for rid in rules_for)
            else:
                for (r, x, body, exc, kind) in insts:
                    eh = exc_holds(exc)
                    if eh is not False:
                        continue
                    if all(val(b[0]) == b[1] for b in body):
                        res = True
                        break
        visiting.discard(a)
        memo[a] = res
        return res
    try:
        ok = True
        for a in sorted(set(by_head) | stated_pos):
            val(a)
        for a in stated_neg:
            if val(a):
                ok = False
        for (r, x, body, exc, head, kind) in neg_rules:
            eh = exc_holds(exc)
            if eh is not False:
                continue
            if all(val(b[0]) == b[1] for b in body) and val(head[0]):
                ok = False
    except (ValueError, RecursionError):
        return set(), False, {}
    true_atoms = {a for a, v in memo.items() if v}
    return true_atoms, ok, by_head


def cw_val(view, true_atoms, a):
    if a[0] == "l":
        return (a[1], a[2], a[3]) in view.links
    return a in true_atoms


def cw_depth(view: View, claim_atom):
    """Least-model derivation hops for an atom in M (0 if stated)."""
    stated_pos = {a for a, v in view.facts.items() if v and a[0] == "u"}
    M, ok, by_head = cw_model(view)
    memo = {}

    def cost(a):
        if a[0] != "u":
            return 0
        if a in stated_pos:
            return 0
        if a in memo:
            return memo[a]
        best = None
        for (r, x, body, exc, kind) in by_head.get(a, []):
            if exc is not None and exc[0] in stated_pos:
                continue
            if not all(cw_val(view, M, b[0]) == b[1] for b in body):
                continue
            c = 1 + sum(cost(b[0]) for b in body if b[1] and b[0][0] == "u")
            if best is None or c < best:
                best = c
        memo[a] = best if best is not None else 10 ** 6
        return memo[a]
    return cost(claim_atom)


# ------------------------------------------------------------------------------------------------------- views from a record

def stmt_facts(rec: Record, trust, *, variant=None, claim_atoms=()):
    """facts (atom -> bool), links, values, dates, marker atoms from the record's statements under a trust reading.
    trust: ("list", names) | ("all",); variant: None | R9 | R9r | R9m | R20."""
    facts, links, values, dates, markers = {}, set(), {}, {}, set()
    conflict = False
    trusted = set(trust[1]) if trust and trust[0] == "list" else None

    def counts(s):
        if s.src is None:
            return True
        if variant == "R9":
            return True
        if variant == "R9r":
            return False
        if trust and trust[0] == "all":
            return True
        if s.src in (trusted or ()):
            return True
        if variant == "R9m" and s.kind == "lit" and u(s.pred, s.e) in claim_atoms:
            return True
        return False
    for s in rec.stmts:
        if not counts(s):
            continue
        if s.kind == "lit":
            a = u(s.pred, s.e)
            if s.pos is None:
                markers.add(a)
                continue
            if a in facts and facts[a] != s.pos:
                conflict = True
            facts[a] = s.pos
        elif s.kind == "link":
            links.add((s.pred, s.e, s.value))
        elif s.kind == "val":
            values[(s.e, s.pred)] = s.value
        elif s.kind == "date":
            dates[(s.e, s.pred)] = s.value
    if variant == "R20":
        rep = {}
        for s in rec.stmts:
            if s.src is not None and not counts(s) and s.kind == "lit" and s.pos is not None:
                rep.setdefault((u(s.pred, s.e), s.pos), set()).add(s.sid)
        for hi, (e_kind, e, p) in enumerate(rec.ehedges):
            rep.setdefault((u(p, e), True), set()).add(f"hedge{hi}")
        for (a, p), sids in rep.items():
            if len(sids) >= 2:
                if a in facts and facts[a] != p:
                    conflict = True
                facts[a] = p
    for (pred, e, tid) in rec.blank_cells:
        pass
    return facts, links, values, dates, markers, conflict


def base_view(rec: Record, card: Card, *, world=None, unless=None, trust=None, variant=None, claim_atoms=()):
    w = world or card.world or "OW"
    um = unless if unless is not None else (card.unless or ("cw" if w == "CW" else "strict"))
    if um in (None, "none"):
        um = "strict" if w == "OW" else "cw"
    if w == "CW" and um in ("strict", "listc"):
        um = "cw"
    if w == "OW" and um == "cw":
        um = "strict"
    tr = trust if trust is not None else (card.trust or ("all",))
    facts, links, values, dates, markers, conflict = stmt_facts(rec, tr, variant=variant, claim_atoms=claim_atoms)
    closures = [(p, t) for (p, t, form, tid) in rec.closures]
    v = View(world=w, unless=um, facts=facts, links=links, values=values, dates=dates,
             rules=[r for r in rec.rules], closures=closures, ents=dict(rec.ents), exc_preds=set(rec.exc_preds))
    v.extra = [("conflict",)] if conflict else []
    v.markers = markers
    return v


# ------------------------------------------------------------------------------------------------------- labels under a view

def view_label(view: View, claim, *, engine="auto"):
    """F / R / O / X for claim literal under a view."""
    if any(x[0] == "conflict" for x in view.extra):
        return "X"
    if view.world == "CW":
        M, ok, _ = cw_model(view)
        if not ok:
            return "X"
        v = cw_val(view, M, claim[0])
        return "F" if v == claim[1] else "R"
    g = ground(view)
    clauses = list(g.clauses)
    for x in view.extra:
        if x[0] == "cnf":
            clauses.extend(x[1])
    if engine == "up" and not any(x[0] == "cnf" for x in view.extra):
        return label_ow_up(g, claim)
    return label_ow_dpll(g.units, clauses, claim)


def labels_for_view(view: View, claims: dict):
    """view_label for many claims with one grounding / one satisfiability check / one CW model."""
    if any(x[0] == "conflict" for x in view.extra):
        return {k: "X" for k in claims}
    if view.world == "CW":
        M, ok, _ = cw_model(view)
        if not ok:
            return {k: "X" for k in claims}
        return {k: ("F" if cw_val(view, M, cl[0]) == cl[1] else "R") for k, cl in claims.items()}
    g = ground(view)
    clauses = list(g.clauses)
    for x in view.extra:
        if x[0] == "cnf":
            clauses.extend(x[1])
    if not dpll_sat(g.units, clauses):
        return {k: "X" for k in claims}
    out = {}
    for k, claim in claims.items():
        if claim[0] in g.units:
            out[k] = "F" if g.units[claim[0]] == claim[1] else "R"
            continue
        comp = component(clauses, [claim[0]])
        sat_not = dpll_sat({**g.units, claim[0]: not claim[1]}, comp)
        sat_yes = dpll_sat({**g.units, claim[0]: claim[1]}, comp)
        if not sat_not and not sat_yes:
            out[k] = "X"
        elif not sat_not:
            out[k] = "F"
        elif not sat_yes:
            out[k] = "R"
        else:
            out[k] = "O"
    return out


def forward_label(view: View, claim, *, contra_ok=None):
    """R2 / R22: propagate forward instances (plus the contrapositives contra_ok(rule, kind) admits); FOLLOWS if the
    claim is derived, RULED_OUT if its negation is, X on a conflict."""
    g = ground(view)
    assign = dict(g.units)
    changed = True
    while changed:
        changed = False
        for lits, meta in g.clauses:
            rid, x, kind, head_pos, has_exc = meta
            rule = next(r for r in view.rules if r.rid == rid)
            for j, (a, p) in enumerate(lits):
                if j != head_pos:
                    if contra_ok is None or not contra_ok(rule, kind, j, head_pos, has_exc):
                        continue
                others = [l for k, l in enumerate(lits) if k != j]
                if all(assign.get(o[0]) == (not o[1]) for o in others):
                    if assign.get(a) is None:
                        assign[a] = p
                        changed = True
                    elif assign[a] != p:
                        return "X"
    v = assign.get(claim[0])
    if v is None:
        return "O"
    return "F" if v == claim[1] else "R"


def stated_label(rec: Record, card: Card, claim, trust):
    facts, *_ = stmt_facts(rec, trust)
    v = facts.get(claim[0])
    if v is None:
        return "O"
    return "F" if v == claim[1] else "R"


# ======================================================================================================= rivals (7.2)

import copy as _copy

RIVALS = ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8n", "R8d", "R9", "R9r", "R9m", "R10", "R11", "R12", "R13a",
          "R13b", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27",
          "R28", "R29", "R30", "R30s", "R31")
TAG = {"R9r": "R9", "R9m": "R9", "R13a": "R13", "R13b": "R13", "R30s": "R30"}
CORE_RIVALS = {"R1", "R2", "R3", "R19", "R22", "R24", "R25", "R30"}
NONCORE_RIVALS = {"R4", "R5", "R6", "R7", "R8n", "R8d", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R18",
                  "R20", "R23", "R28", "R29", "R31"}
ASSERT_RIVALS = {"R17", "R21", "R26"}


def ruled_out(rival: str, card: Card) -> bool:
    """Does the card print the clause that rules this rival out (7.2 'Ruled out by')?"""
    c = card.clauses
    t = TAG.get(rival, rival)
    w = card.world
    table = {
        "R1": ("1" in c and "3" in c) if w == "OW" else (("2" in c and "3c" in c) if w == "CW" else False),
        "R2": "4" in c, "R22": "4" in c,
        "R3": ("5" in c) if w == "OW" else ("5c" in c if w == "CW" else False),
        "R4": "6" in c,
        "R5": ("7a" in c or "7b" in c) if w == "OW" else ("2" in c if w == "CW" else False),
        "R6": "20" in c, "R7": "9" in c, "R18": "9" in c, "R8n": "12" in c, "R8d": "13" in c,
        "R9": "22" in c or "22b" in c, "R20": "22" in c,
        "R10": any(x in c for x in ("18.1", "18.2", "18.3", "18.4")),
        "R11": "19" in c, "R12": "8" in c, "R13": "11" in c and "16" in c, "R14": "10" in c, "R15": "17" in c,
        "R16": "21" in c, "R17": "27" in c, "R19": "3" in c or "3c" in c or "3s" in c, "R21": "28" in c,
        "R23": "18c" in c, "R24": "3c" in c, "R25": "26" in c, "R26": "18c" in c, "R27": False, "R28": "25a" in c,
        "R29": "18.5" in c, "R30": "5c" in c, "R31": "28" in c,
    }
    return bool(table.get(t, False))


def _rule_copy(r, **kw):
    r2 = _copy.copy(r)
    for k, v in kw.items():
        setattr(r2, k, v)
    return r2


def _tseitin(bodies, aux_key):
    """Clauses for  OR_i (AND body_i)  via aux atoms. Returns (clauses, disjunction literal list)."""
    cls, disj = [], []
    for i, body in enumerate(bodies):
        t = ("x", aux_key, i)
        for b in body:
            cls.append((((t, False), b), ("aux", None, "t", 1, False)))
        disj.append((t, True))
    return cls, disj


def _ground_for(view, r, x):
    return ground_bodies(r, x, view)


def r3_ow_cnf(view: View):
    """h(x) -> B_r(x) for every rule r and subject x (per-rule converse)."""
    cls = []
    for r in view.rules:
        for x in subjects(view, r):
            items = _ground_for(view, r, x)
            if r.form == "onlyif":
                h = (u(r.head[0], x), True)
                bodies = [[(u(r.ante, x), True)]]
            else:
                h = (u(r.head[0], x), r.head[1])
                bodies = []
                for body, exc, head, kind in items:
                    bodies.append(list(body) + ([(exc[0], False)] if exc else []))
            tc, disj = _tseitin(bodies, (r.rid, x))
            cls.extend(tc)
            cls.append((tuple([neg(h)] + disj), ("r3", r.rid, x, 0, False)))
    return cls


def r6_cnf(rec: Record, view: View):
    cls = []
    for hi, (kind, typ, cnd, hd) in enumerate(rec.hedges):
        es = [e for e, t in view.ents.items() if t == typ]
        bodies = []
        for e in es:
            a = (u(cnd[0], e), cnd[1])
            h = (u(hd[0], e), hd[1] if kind != "notevery" else not hd[1])
            bodies.append([a, h])
        tc, disj = _tseitin(bodies, ("r6", hi))
        cls.extend(tc)
        cls.append((tuple(disj), ("r6", hi, None, 0, False)))
    return cls


def r21_cnf(view: View):
    """Other-type memberships as free atoms: every rule also grounded on other-type subjects under a free atom."""
    cls = []
    v2 = View(**{**view.__dict__, "ground_all": True})
    for r in view.rules:
        for x in sorted(view.ents):
            if view.ents[x] == r.typ:
                continue
            m = (("m", r.typ, x), False)
            for body, exc, head, kind in ground_bodies(r, x, v2):
                lits = [neg(b) for b in body] + ([exc] if exc else []) + [head, m]
                cls.append((tuple(lits), (r.rid, x, kind, len(lits) - 2, exc is not None)))
    return cls


def r15_view(view: View):
    """Drop, for x, every rule with the same head literal as an exception rule that is off for x."""
    off = set()
    for r in view.rules:
        if not r.exc:
            continue
        for x in ents_of(view, r.typ):
            a = u(r.exc, x)
            st = view.facts.get(a)
            if st is True:
                off.add((r.head, x))
            elif st is None and view.world == "OW" and view.unless == "strict":
                closed = any(p == r.exc and view.ents.get(x) == t for p, t in view.closures)
                if not closed:
                    off.add((r.head, x))
    v2 = View(**view.__dict__)
    keep = []
    for r in view.rules:
        bad = [x for (h, x) in off if h == r.head]
        if bad:
            keep.append(_rule_copy(r, style={**r.style, "_skip": set(bad)}))
        else:
            keep.append(r)
    v2.rules = keep
    return v2


def _apply_skip(view: View):
    """ground() honours style['_skip'] (subjects for which the rule is dropped) by filtering ents per rule."""
    return view


def merge_view(rec: Record, view: View):
    """R16: each marked look-alike pair merged (facts pooled; conflicting facts or values -> X)."""
    ren = {}
    for a, b in rec.lookalikes:
        ren[max(a, b)] = min(a, b)
    f2 = {}
    conflict = False
    for (k, p, e), v in [(a, v) for a, v in view.facts.items()]:
        e2 = ren.get(e, e)
        key = (k, p, e2)
        if key in f2 and f2[key] != v:
            conflict = True
        f2[key] = v
    links = {(li, ren.get(a, a), ren.get(b, b)) for li, a, b in view.links}
    vals, dts = {}, {}
    for (e, q), v in view.values.items():
        e2 = ren.get(e, e)
        if (e2, q) in vals and vals[(e2, q)] != v:
            conflict = True
        vals[(e2, q)] = v
    for (e, q), v in view.dates.items():
        e2 = ren.get(e, e)
        if (e2, q) in dts and dts[(e2, q)] != v:
            conflict = True
        dts[(e2, q)] = v
    ents = {e: t for e, t in view.ents.items() if e not in ren}
    v2 = View(**view.__dict__)
    v2.facts, v2.links, v2.values, v2.dates, v2.ents = f2, links, vals, dts, ents
    v2.extra = list(view.extra) + ([("conflict",)] if conflict else [])
    return v2, ren


def r27_links(links):
    out = set(links)
    for (li, a, b) in list(links):
        out.add((li, b, a))
    changed = True
    while changed:
        changed = False
        for (l1, a, b) in list(out):
            for (l2, c, d) in list(out):
                if l1 == l2 and b == c and (l1, a, d) not in out and a != d:
                    out.add((l1, a, d))
                    changed = True
    return out


def r24_label(view: View, claim):
    """CW claim-level reading of negative claims: TRUE iff 'not H(x)' is stated or is the head of a negative-head rule
    instance whose body holds in the least model; else FALSE. Positive claims keep the CW label."""
    M, ok, _ = cw_model(view)
    if not ok:
        return "X"
    if claim[1]:
        return "F" if cw_val(view, M, claim[0]) else "R"
    a = claim[0]
    if view.facts.get(a) is False:
        return "F"
    for r in view.rules:
        if r.head[1] or r.form == "onlyif":
            continue
        for x in subjects(view, r):
            for body, exc, head, kind in ground_bodies(r, x, view):
                if head[0] != a:
                    continue
                if exc is not None and view.facts.get(exc[0]) is True:
                    continue
                if all(cw_val(view, M, b[0]) == b[1] for b in body):
                    return "F"
    return "R"


R30_BUDGET = 2 ** 16


def r30_label(view: View, claims: dict, strict_only: bool):
    """CW affirming-the-consequent reading (R30, or R30s when strict_only). Returns {key: label} or 'BUDGET'."""
    M, ok, by_head = cw_model(view)
    if not ok:
        return {k: "X" for k in claims}
    stated_pos = {a for a, v in view.facts.items() if v and a[0] == "u"}
    choices = []   # list of lists of bodies (each body = list of (lit, kind))
    results = [(a, True) for a in sorted(M) if a[0] == "u"]
    results += [(a, False) for a, v in sorted(view.facts.items()) if v is False and a[0] == "u"]
    for (a, pol) in results:
        x = a[2]
        rules_for = [r for r in view.rules if r.form != "onlyif" and r.head == (a[1], pol)
                     and (view.ground_all or view.ents.get(x) == r.typ) and x not in r.style.get("_skip", ())]
        if not rules_for:
            continue
        per_rule = []
        for r in rules_for:
            bodies = []
            for body, exc, head, kind in ground_bodies(r, x, view):
                bodies.append((tuple(body), exc))
            per_rule.append(bodies)
        if strict_only:
            if not pol:
                holds_by_rule = False   # negative results hold only because they are stated in CW
            else:
                holds_by_rule = False
                for (r, xx, body, exc, kind) in by_head.get(a, []):
                    if exc is not None and exc[0] in stated_pos:
                        continue
                    if all(cw_val(view, M, b[0]) == b[1] for b in body):
                        holds_by_rule = True
                        break
            if holds_by_rule or (pol and a not in stated_pos):
                continue
            opts = [b for bodies in per_rule for b in bodies]
            choices.append(opts)
        else:
            for bodies in per_rule:
                choices.append(bodies)
    n = 1
    for c in choices:
        n *= max(1, len(c))
        if n > R30_BUDGET:
            return "BUDGET"
    if any(len(c) == 0 for c in choices):
        return {k: "X" for k in claims}
    res = {k: set() for k in claims}
    any_world = False
    for pick in itertools.product(*choices) if choices else [()]:
        f2 = dict(view.facts)
        neg_req = set()
        bad = False
        for body, exc in pick:
            for (atom, p) in body:
                if atom[0] == "u":
                    if p:
                        if f2.get(atom) is False:
                            bad = True
                        f2[atom] = True
                    else:
                        neg_req.add(atom)
                elif atom[0] == "l":
                    pass
                else:
                    bad = True   # a free comparison atom cannot arise in CW
            if exc is not None:
                neg_req.add(exc[0])
        if bad:
            continue
        v2 = View(**view.__dict__)
        v2.facts = f2
        M2, ok2, _ = cw_model(v2)
        if not ok2 or any(cw_val(v2, M2, a) for a in neg_req):
            continue
        any_world = True
        for k, cl in claims.items():
            res[k].add(cw_val(v2, M2, cl[0]) == cl[1])
    out = {}
    for k in claims:
        if not any_world:
            out[k] = "X"
        elif res[k] == {True}:
            out[k] = "F"
        elif res[k] == {False}:
            out[k] = "R"
        else:
            out[k] = "O"
    return out


def view_for(rec: Record, card: Card, rival: str, claim_atoms=()):
    """The View for one rival (None when the rival is computed by a special engine)."""
    W = card.world or "OW"
    v = base_view(rec, card, world=W)
    if rival == "R1":
        if W == "OW":
            v = base_view(rec, card, world="CW")
            v.missing_false = True
        else:
            v = base_view(rec, card, world="OW", unless="strict")
        return v
    if rival == "R3" and W == "CW":
        v.cw_mode = "conj"
        return v
    if rival == "R3":
        v.extra = list(v.extra) + [("cnf", r3_ow_cnf(v))]
        return v
    if rival == "R4":
        add = []
        for r in v.rules:
            if r.exc:
                add.append(Rule(rid=r.rid + "~R4", form="univ", typ=r.typ, conds=(("lit", r.exc, True),),
                                head=(r.head[0], not r.head[1])))
        v.rules = list(v.rules) + add
        return v
    if rival == "R5":
        if W == "OW":
            v = base_view(rec, card, world="OW", unless={"strict": "listc", "listc": "strict"}.get(v.unless, v.unless))
        else:
            v.cw_mode = "strict"
        return v
    if rival == "R6":
        if W == "OW" and rec.hedges:
            v.extra = list(v.extra) + [("cnf", r6_cnf(rec, v))]
        return v
    if rival == "R7":
        v.rules = [_rule_copy(r, form="xor") if r.form == "or" else r for r in v.rules]
        return v
    if rival == "R8n":
        v.rules = [_rule_copy(r, conds=tuple((c[0], c[1], c[2], c[3], (False, False)) if c[0] == "rng" else c
                                             for c in r.conds)) for r in v.rules]
        return v
    if rival == "R8d":
        fl = {"<": "<=", "<=": "<", ">": ">=", ">=": ">"}
        v.rules = [_rule_copy(r, conds=tuple(
            ("dcmp", c[1], fl[c[2]], c[3]) if c[0] == "dcmp" else
            (("win", c[1], c[2], c[3], (False, False)) if c[0] == "win" else c) for c in r.conds)) for r in v.rules]
        return v
    if rival in ("R9", "R9r", "R9m", "R20"):
        return base_view(rec, card, world=W, variant=rival, claim_atoms=claim_atoms)
    if rival == "R10":
        v.missing_false = True
        v.marker_false = set(getattr(v, "markers", set()))
        return v
    if rival == "R11":
        add = []
        for i, (kind, typ, cnd, hd) in enumerate(rec.hedges):
            if kind in ("most", "many", "usually", "often"):
                add.append(Rule(rid=f"~R11h{i}", form="univ", typ=typ, conds=(("lit", cnd[0], cnd[1]),), head=hd))
        v.rules = list(v.rules) + add
        f2 = dict(v.facts)
        for (kind, e, p) in rec.ehedges:
            a = u(p, e)
            if f2.get(a) is False:
                v.extra = list(v.extra) + [("conflict",)]
            f2[a] = True
        v.facts = f2
        return v
    if rival == "R12":
        v.rules = [Rule(rid=r.rid + "~R12", form="univ", typ=r.typ, conds=(("lit", r.head[0], True),),
                        head=(r.ante, True)) if r.form == "onlyif" else r for r in v.rules]
        return v
    if rival in ("R13a", "R13b"):
        fl = {">": ">=", "<": "<="} if rival == "R13a" else {">=": ">", "<=": "<"}
        v.rules = [_rule_copy(r, conds=tuple(("cmp", c[1], fl.get(c[2], c[2]), c[3]) if c[0] == "cmp" else c
                                             for c in r.conds)) for r in v.rules]
        return v
    if rival == "R14":
        v.rules = [_rule_copy(r, form="exactk") if r.form == "kofn" else r for r in v.rules]
        return v
    if rival == "R15":
        return r15_view(v)
    if rival == "R16":
        v2, _ = merge_view(rec, v)
        return v2
    if rival == "R17":
        return v
    if rival == "R18":
        add = [Rule(rid=r.rid + "~R18", form="xor_both_not", typ=r.typ, conds=r.conds, head=(r.head[0], False))
               for r in v.rules if r.form == "xor"]
        v.rules = list(v.rules) + add
        return v
    if rival == "R21":
        if W == "OW":
            v.extra = list(v.extra) + [("cnf", r21_cnf(v))]
        return v
    if rival == "R23":
        v.closures = []
        return v
    if rival == "R26":
        v.closures = [(p, t2) for (p, t) in v.closures for t2 in range(len(rec.types))]
        return v
    if rival == "R27":
        v.links = r27_links(v.links)
        return v
    if rival == "R28":
        v.rules = [r for r in v.rules if r.where != "card"]
        return v
    if rival == "R29":
        rev = set()
        for s in rec.stmts:
            if s.kind == "link" and s.via == "cell":
                rev.add((s.pred, s.e, s.value))
        v.links = {(li, b, a) if (li, a, b) in rev else (li, a, b) for (li, a, b) in v.links}
        return v
    if rival == "R31":
        v.ground_all = True
        return v
    return v


def rival_labels(rec: Record, card: Card, claims: dict):
    """{rival: {claim key: F/R/O/X}} for every rival in RIVALS (R25 copies the base labels; the answer mapping
    applies it). 'BUDGET' for R30/R30s when over the world budget."""
    W = card.world or "OW"
    atoms = tuple(c[0] for c in claims.values())
    base = base_view(rec, card, world=W)
    out = {}
    cache = {}

    def lab_view(v):
        key = (v.world, v.unless, tuple(sorted(v.facts.items())), tuple(sorted(v.links)),
               tuple(sorted((k, str(x)) for k, x in v.values.items())),
               tuple(sorted((k, str(x)) for k, x in v.dates.items())),
               tuple((r.rid, r.form, r.conds, r.head, r.ante, r.exc, r.link, r.ptyp, r.pcond, r.k,
                      tuple(sorted(r.style.get("_skip", ())))) for r in v.rules),
               tuple(v.closures), v.missing_false, tuple(sorted(v.marker_false)), v.ground_all, v.cw_mode,
               tuple(sorted(v.ents.items())), repr(v.extra)[:20000])
        if key not in cache:
            cache[key] = labels_for_view(v, claims)
        return cache[key]
    for rv in RIVALS:
        if rv == "R2":
            if W == "OW":
                out[rv] = {k: forward_label(base, cl) for k, cl in claims.items()}
            else:
                out[rv] = lab_view(base)
            continue
        if rv == "R22":
            if W == "OW":
                def ok22(rule, kind, j, hp, has_exc):
                    if has_exc and j == hp - 1:
                        return False
                    if rule.form == "univ" and rule.head[1]:
                        return True
                    return rule.form in ("or", "xor", "onlyif")
                out[rv] = {k: forward_label(base, cl, contra_ok=ok22) for k, cl in claims.items()}
            else:
                out[rv] = lab_view(base)
            continue
        if rv == "R19":
            tr = card.trust or ("all",)
            out[rv] = {k: stated_label(rec, card, cl, tr) for k, cl in claims.items()}
            continue
        if rv == "R24":
            if W == "CW":
                out[rv] = {k: r24_label(base, cl) for k, cl in claims.items()}
            else:
                out[rv] = lab_view(base)
            continue
        if rv in ("R30", "R30s"):
            if W == "CW":
                out[rv] = r30_label(base, claims, rv == "R30s")
            else:
                out[rv] = lab_view(base)
            continue
        if rv == "R25":
            out[rv] = lab_view(base)
            continue
        v = view_for(rec, card, rv, claim_atoms=atoms)
        if rv == "R16":
            ren = {max(a, b): min(a, b) for a, b in rec.lookalikes}
            cl2 = {k: (("u", c[0][1], ren.get(c[0][2], c[0][2])), c[1]) for k, c in claims.items()}
            out[rv] = labels_for_view(v, cl2)
            continue
        out[rv] = lab_view(v)
    return out


def short_pair_labels(rec: Record, card: Card, claims: dict):
    """Pairs among R1, R2, R22, R3, R17 (+ R1 with R24 and R1 with R30) for short cards (7.4)."""
    out = {}
    cw = base_view(rec, card, world="CW")
    cw.missing_false = True
    ow = base_view(rec, card, world="OW")
    cwc = View(**cw.__dict__)
    cwc.cw_mode = "conj"
    labcw = {k: view_label(cw, cl) for k, cl in claims.items()}
    out["R1+R2"] = labcw
    out["R1+R22"] = labcw
    out["R1+R17"] = labcw
    out["R1+R3"] = {k: view_label(cwc, cl) for k, cl in claims.items()}
    out["R1+R24"] = {k: r24_label(cw, cl) for k, cl in claims.items()}
    r30 = r30_label(cw, claims, False)
    out["R1+R30"] = r30 if r30 != "BUDGET" else {k: "BUDGETX" for k in claims}
    fw = {k: forward_label(ow, cl) for k, cl in claims.items()}
    out["R2+R17"] = fw
    out["R2+R22"] = fw

    def ok22(rule, kind, j, hp, has_exc):
        if has_exc and j == hp - 1:
            return False
        if rule.form == "univ" and rule.head[1]:
            return True
        return rule.form in ("or", "xor", "onlyif")
    out["R22+R17"] = {k: forward_label(ow, cl, contra_ok=ok22) for k, cl in claims.items()}
    # R3 combined with forward-only readings: converse instances usable forward when a rule has one ground body
    conv = r3_ow_cnf(ow)
    ow3 = View(**ow.__dict__)
    ow3.extra = list(ow.extra) + [("cnf", conv)]
    out["R3+R17"] = {k: view_label(ow3, cl) for k, cl in claims.items()}
    out["R2+R3"] = {k: forward_conv_label(ow, cl, None) for k, cl in claims.items()}
    out["R22+R3"] = {k: forward_conv_label(ow, cl, ok22) for k, cl in claims.items()}
    return out


def forward_conv_label(view: View, claim, contra_ok):
    """Forward propagation plus converse instances h(x) -> each condition, for rules with exactly one ground body."""
    g = ground(view)
    conv = []
    for r in view.rules:
        for x in subjects(view, r):
            items = ground_bodies(r, x, view)
            if r.form == "onlyif" or len(items) != 1:
                continue
            body, exc, head, kind = items[0]
            for b in body:
                conv.append((head, b))
            if exc is not None:
                conv.append((head, (exc[0], False)))
    assign = dict(g.units)
    changed = True
    while changed:
        changed = False
        for lits, meta in g.clauses:
            rid, x, kind, head_pos, has_exc = meta
            rule = next(r for r in view.rules if r.rid == rid)
            for j, (a, p) in enumerate(lits):
                if j != head_pos and (contra_ok is None or not contra_ok(rule, kind, j, head_pos, has_exc)):
                    continue
                others = [l for k, l in enumerate(lits) if k != j]
                if all(assign.get(o[0]) == (not o[1]) for o in others):
                    if assign.get(a) is None:
                        assign[a] = p
                        changed = True
                    elif assign[a] != p:
                        return "X"
        for (h, b) in conv:
            if assign.get(h[0]) == h[1]:
                if assign.get(b[0]) is None:
                    assign[b[0]] = b[1]
                    changed = True
                elif assign[b[0]] != b[1]:
                    return "X"
    v = assign.get(claim[0])
    if v is None:
        return "O"
    return "F" if v == claim[1] else "R"


# ======================================================================================================= answers

YN_FORMS = ("YN-F", "YN-R", "YN-O", "YN-T", "YN-nF", "YN-nR", "YN-dn")
MAP = {  # mapped label -> answer per yes/no form ('yes' / 'no')
    "YN-F": {"F": "yes", "R": "no", "O": "no"}, "YN-dn": {"F": "yes", "R": "no", "O": "no"},
    "YN-R": {"F": "no", "R": "yes", "O": "no"}, "YN-O": {"F": "no", "R": "no", "O": "yes"},
    "YN-T": {"F": "yes", "R": "no", "O": "no"}, "YN-nF": {"F": "no", "R": "yes", "O": "yes"},
    "YN-nR": {"F": "yes", "R": "no", "O": "yes"},
}


def answer(form, labels: dict, *, r25=False, gold_slot=None, none_shown=False):
    """The answer under a label set. labels: {claim key: F/R/O/X}. Yes/no and CH-3 / CH-2 use key 'c'.
    CH-claim keys are option indexes (claims), CH-entity keys option indexes (entities). Returns the answer
    ('yes'/'no', an option index, 'NONE', or 'PIVOT' when no single option qualifies / no model)."""
    if form in MAP:
        lab = labels["c"]
        if lab == "X" or lab.startswith("BUDGET"):
            return "PIVOT"
        return MAP["YN-F" if r25 else form][lab]
    if form == "CH-3":
        lab = labels["c"]
        return "PIVOT" if lab == "X" or lab.startswith("BUDGET") else lab
    if form == "CH-2":
        lab = labels["c"]
        if lab == "X" or lab == "O" or lab.startswith("BUDGET"):
            return "PIVOT"
        return lab
    if form == "CH-claim":
        if any(v == "X" or str(v).startswith("BUDGET") for v in labels.values()):
            return "PIVOT"
        q = [k for k, v in labels.items() if v == "F"]
        if not q:
            return "NONE" if none_shown else "PIVOT"
        return q[0] if len(q) == 1 else "PIVOT"
    if form == "CH-entity":
        if any(v == "X" or str(v).startswith("BUDGET") for v in labels.values()):
            return "PIVOT"
        q = [k for k, v in labels.items() if v == "F"]
        return q[0] if len(q) == 1 else "PIVOT"
    raise ValueError(form)
