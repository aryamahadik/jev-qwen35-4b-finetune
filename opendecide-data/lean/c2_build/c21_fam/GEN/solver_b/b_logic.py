"""GEN solver B, LOGIC sub-block (LG-L1, LG-L2, LG-L3, LG-L4).

Method (G0-lite section 2, solver B column): exhaustive MODEL ENUMERATION. Ground atoms are the unary atoms pred(entity) over the
entities that appear in the text and, when a relation exists, rel(x, y) for ordered pairs of distinct entities. A literal is
entailed iff it is true in EVERY model of the facts and rules, contradicted iff its negation is entailed, else undetermined.
The enumeration is a complete backtracking search over the assignments (every full assignment is either rejected by a falsified
clause on the way or counted as a model), which is exact; it is not unit propagation.
LG-L3 (orderings): permutation brute force.

Relation atoms: a rel atom that is not stated appears only negatively in clauses (as a rule body), so setting it false never
falsifies a clause; "R free" and "R closed" give the same entailments for unary literals, and B carries no atom for unstated pairs.
"""
import itertools
import re

from b_questions import read_question
from bcommon import ParseFail, Reject, statements, pick_unique, norm_text, name_list, fnum

ENT = r"[A-Z][A-Za-z0-9_]*"
_STOP = r"(?!(?:is|a|an|and|not|to|that|it|if|then|something|anything)\b)"
PREDW = _STOP + r"[a-z][a-z0-9_'-]*"
PRED = PREDW + r"(?: " + PREDW + r")*"
RELW = r"[a-z][a-z0-9_]*"

# --- fact sentences ---------------------------------------------------------------------------------------------------
_FACT_PREFIX = r"(?:We are told |It is known that |It is given that |We know that )?"
FACT_POS = [re.compile(r"^" + _FACT_PREFIX + r"(%s) is a (%s)$" % (ENT, PRED)), re.compile(r"^(%s) counts as a (%s)$" % (ENT, PRED))]
FACT_NEG = [re.compile(r"^" + _FACT_PREFIX + r"(%s) is not a (%s)$" % (ENT, PRED)), re.compile(r"^(%s) does not count as a (%s)$" % (ENT, PRED))]
FACT_REL = re.compile(r"^" + _FACT_PREFIX + r"(%s) is (%s) to (%s)$" % (ENT, RELW, ENT))

# --- rule sentences: (regex with groups body, head) and the head sign. Bodies are parsed by parse_body --------------------
_B = r"(?P<body>.+?)"
RULE_FRAMES = [
    (re.compile(r"^Anything that " + _B + r" is a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^Anything that " + _B + r" is not a (?P<head>%s)$" % PRED), False),
    (re.compile(r"^All that " + _B + r" are a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^Every one that " + _B + r" is a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^If something " + _B + r", it is a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^If something " + _B + r", it is not a (?P<head>%s)$" % PRED), False),
    (re.compile(r"^If something " + _B + r", then it is a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^If something " + _B + r", then it is not a (?P<head>%s)$" % PRED), False),
    (re.compile(r"^Each thing that " + _B + r" is a (?P<head>%s)$" % PRED), True),
    (re.compile(r"^No one that " + _B + r" is a (?P<head>%s)$" % PRED), False),
    (re.compile(r"^None that " + _B + r" is a (?P<head>%s)$" % PRED), False),
    (re.compile(r"^Nothing that " + _B + r" is a (?P<head>%s)$" % PRED), False),
]
# relation rules: X is R to Y and X is a P  =>  Y is [not] a Q
_REL_BODY = r"X is (?P<rel>%s) to Y and X is a (?P<p>%s)" % (RELW, PRED)
_REL_HEAD = r"Y is (?P<neg>not )?a (?P<q>%s)" % PRED
REL_FRAMES = [
    re.compile(r"^Whenever " + _REL_BODY + r", it follows that " + _REL_HEAD + r"$"),
    re.compile(r"^For any two different ones X and Y, if " + _REL_BODY + r" then " + _REL_HEAD + r"$"),
    re.compile(r"^If " + _REL_BODY + r" \(X and Y distinct\), " + _REL_HEAD + r"$"),
    re.compile(r"^Whenever " + _REL_BODY + r", " + _REL_HEAD + r"$"),
    re.compile(r"^For distinct X and Y: if " + _REL_BODY + r", then " + _REL_HEAD + r"$"),
]

STATEMENT = re.compile(r"^(%s) is (not )?a (%s)$" % (ENT, PRED))
INSTR = re.compile(r"^(?:Use only the statements given|Reason only from the statements below|Use only the statements given below|Reason only from the statements listed here)$")


def parse_body(body):
    """'is a p' / 'is a p and is a q' -> ['p','q']"""
    parts = re.split(r"\s+and\s+(?=is a )", body.strip())
    preds = []
    for p in parts:
        m = re.match(r"^is a (%s)$" % PRED, p.strip())
        if not m:
            raise ParseFail("rule_body_shape", body)
        preds.append(m.group(1))
    return preds


def parse_rule(s):
    for rx in REL_FRAMES:
        m = rx.match(s)
        if m:
            return {"kind": "rel", "rel": m.group("rel"), "body": [m.group("p")], "head": {"pred": m.group("q"), "sign": m.group("neg") is None}}
    for rx, sign in RULE_FRAMES:
        m = rx.match(s)
        if m:
            return {"kind": "unary", "body": parse_body(m.group("body")), "head": {"pred": m.group("head"), "sign": sign}}
    return None


def parse_stmt_literal(text):
    m = STATEMENT.match(text.strip().rstrip("."))
    if not m:
        raise ParseFail("statement_shape", text)
    return {"entity": m.group(1), "pred": m.group(3)}, m.group(2) is None


def parse_kb(stmts):
    facts, rules, rest = [], [], []
    for s in stmts:
        if INSTR.match(s):
            continue
        done = False
        for rx in FACT_POS:
            m = rx.match(s)
            if m:
                facts.append({"atom": {"entity": m.group(1), "pred": m.group(2)}, "sign": True})
                done = True
                break
        if done:
            continue
        for rx in FACT_NEG:
            m = rx.match(s)
            if m:
                facts.append({"atom": {"entity": m.group(1), "pred": m.group(2)}, "sign": False})
                done = True
                break
        if done:
            continue
        r = parse_rule(s)
        if r is not None:
            rules.append(r)
            continue
        m = FACT_REL.match(s)
        if m:
            facts.append({"atom": {"from": m.group(1), "rel": m.group(2), "to": m.group(3)}, "sign": True})
            continue
        rest.append(s)
    return facts, rules, rest


# ---------------------------------------------------------------------------------------------------------------------
# model enumeration
#
# Ground atoms: pred(entity) for every entity in the text and every predicate. A stated relation fact R(x, y) makes every rel rule
# an ordinary clause on the unary atoms of x and y. A relation atom that is NOT stated appears only negatively in clauses
# (as the rule body), so setting it false never falsifies a clause and never changes whether a unary literal holds in some
# model: "R free" and "R closed" give the same entailments. B therefore carries no atom for unstated R pairs.

MODEL_LIMIT = 400000


class KB(object):
    def __init__(self, facts, rules, extra_entities, extra_preds=()):
        ents, preds, rels = [], [], set()

        def add_ent(e):
            if e not in ents:
                ents.append(e)

        stated_pairs = []
        for f in facts:
            a = f["atom"]
            if "entity" in a:
                add_ent(a["entity"])
                if a["pred"] not in preds:
                    preds.append(a["pred"])
            else:
                add_ent(a["from"])
                add_ent(a["to"])
                rels.add(a["rel"])
                if a["from"] == a["to"]:
                    raise Reject("reflexive_relation_fact", "")
                stated_pairs.append((a["from"], a["to"]))
        for e in extra_entities:
            add_ent(e)
        for r in rules:
            for p in r["body"] + [r["head"]["pred"]]:
                if p not in preds:
                    preds.append(p)
            if r["kind"] == "rel":
                rels.add(r["rel"])
        for p in extra_preds:
            if p not in preds:
                preds.append(p)
        if len(rels) > 1:
            raise ParseFail("several_relations", sorted(rels))
        self.ents, self.preds = ents, preds
        self.rel = next(iter(rels)) if rels else None
        self.index = {}
        for e in ents:
            for p in preds:
                self.index[(e, p)] = len(self.index)
        self.n = len(self.index)
        cl = []
        for f in facts:
            a = f["atom"]
            if "entity" in a:
                cl.append(((self.index[(a["entity"], a["pred"])], f["sign"]),))
        for r in rules:
            if r["kind"] == "unary":
                for e in ents:
                    lits = [(self.index[(e, p)], False) for p in r["body"]]
                    lits.append((self.index[(e, r["head"]["pred"])], r["head"]["sign"]))
                    cl.append(tuple(lits))
            else:
                for (x, y) in stated_pairs:
                    lits = [(self.index[(x, p)], False) for p in r["body"]]
                    lits.append((self.index[(y, r["head"]["pred"])], r["head"]["sign"]))
                    cl.append(tuple(lits))
        self.clauses = cl
        # connected components of atoms through clauses
        parent = list(range(self.n))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for c in cl:
            for (ai, _v) in c[1:]:
                ra, rb = find(c[0][0]), find(ai)
                if ra != rb:
                    parent[ra] = rb
        comp = {}
        for i in range(self.n):
            comp.setdefault(find(i), []).append(i)
        self.comp_of = {}
        self.comps = []
        for k, (root, members) in enumerate(sorted(comp.items())):
            self.comps.append(members)
            for i in members:
                self.comp_of[i] = k
        self._models = {}

    def models(self, k):
        if k in self._models:
            return self._models[k]
        members = self.comps[k]
        local = dict((a, j) for j, a in enumerate(members))
        mset = set(members)
        clauses = [c for c in self.clauses if c[0][0] in mset]
        by_atom = dict((a, []) for a in members)
        for ci, c in enumerate(clauses):
            for (ai, _v) in c:
                by_atom[ai].append(ci)
        assign = {}
        out = []

        def falsified(ci):
            for (ai, v) in clauses[ci]:
                a = assign.get(ai)
                if a is None or a == v:
                    return False
            return True

        def rec(j):
            if j == len(members):
                out.append(tuple(assign[a] for a in members))
                if len(out) > MODEL_LIMIT:
                    raise Reject("too_many_models", "component of %d atoms" % len(members))
                return
            a = members[j]
            for v in (False, True):
                assign[a] = v
                if not any(falsified(ci) for ci in by_atom[a]):
                    rec(j + 1)
            del assign[a]

        rec(0)
        self._models[k] = out
        return out

    def status(self, entity, pred, sign):
        for k in range(len(self.comps)):
            if not self.models(k):
                raise Reject("inconsistent_knowledge_base", "")
        ai = self.index[(entity, pred)]
        k = self.comp_of[ai]
        j = self.comps[k].index(ai)
        ms = self.models(k)
        in_all_true = all(m[j] for m in ms)
        in_all_false = all(not m[j] for m in ms)
        if in_all_true:
            return "entailed" if sign else "contradicted"
        if in_all_false:
            return "contradicted" if sign else "entailed"
        return "undetermined"


def _parse_back(form, facts, rules, kb, query=None, options=None):
    pb = {"form": form,
          "entities": list(kb.ents), "preds": list(kb.preds), "rel": kb.rel,
          "facts": facts,
          "rules": [{"kind": r["kind"], "body": list(r["body"]), "head": dict(r["head"])} for r in rules]}
    if query is not None:
        pb["query"] = {"atom": query[0], "sign": query[1]}
    if options is not None:
        pb["options"] = [{"atom": a, "sign": s} for (a, s) in options]
    return pb


def _kb(facts, rules, literals):
    return KB(facts, rules, [a["entity"] for (a, _s) in literals], [a["pred"] for (a, _s) in literals])


def solve(form, stem, options):
    key, slots, remainder = read_question("q." + form, stem)
    if form == "LG-L3":
        return solve_l3(remainder, options)
    stmts = statements(remainder)
    facts, rules, rest = parse_kb(stmts)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    if form in ("LG-L1", "LG-L4"):
        q = parse_stmt_literal(slots["query"])
        kb = _kb(facts, rules, [q])
        st = kb.status(q[0]["entity"], q[0]["pred"], q[1])
        if form == "LG-L1":
            word = st
            idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == word], word)
            text = word.capitalize()
        else:
            want = "yes, it follows" if st == "entailed" else "no, it does not follow"
            idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
            text = "Yes, it follows" if st == "entailed" else "No, it does not follow"
        return {"answer_index": idx, "answer_text": text, "parse": _parse_back(form, facts, rules, kb, query=q), "info": {}}
    if form == "LG-L2":
        lits = []
        for o in options:
            m = STATEMENT.match(o.strip())
            if not m:
                raise ParseFail("option_not_a_statement", o)
            lits.append(({"entity": m.group(1), "pred": m.group(3)}, m.group(2) is None))
        kb = _kb(facts, rules, lits)
        sts = [kb.status(a["entity"], a["pred"], s) for (a, s) in lits]
        hits = [i for i, st in enumerate(sts) if st == "entailed"]
        idx = pick_unique(hits, "entailed option")
        return {"answer_index": idx, "answer_text": options[idx], "parse": _parse_back(form, facts, rules, kb, options=lits), "info": {}}
    raise ParseFail("not_a_logic_form", form)


# ---------------------------------------------------------------------------------------------------------------------
# LG-L3: ordering puzzles by permutation brute force

L3_ITEMS = [
    re.compile(r"^Arrange (?P<items>.+) in a row, one per position, with positions counted from (?P<start>\d+)$"),
    re.compile(r"^Arrange (?P<items>.+) in a row, one per position, positions counted from (?P<start>\d+)$"),
    re.compile(r"^Items (?P<items>.+) are placed in positions (?P<start>\d+), \d+, \d+ and so on, one item per position$"),
    re.compile(r"^There are positions (?P<start>\d+), \d+, \d+ and so on for the items (?P<items>.+); each item takes one position$"),
    re.compile(r"^The items (?P<items>.+) are lined up, one per position, from position (?P<start>\d+)$"),
]
_N = r"[A-Z][A-Za-z0-9_]*"
L3_CONS = [
    ("before", re.compile(r"^The position of (%s) is lower than the position of (%s)$" % (_N, _N)), (1, 2)),
    ("before", re.compile(r"^Position of (%s) is lower than position of (%s)$" % (_N, _N)), (1, 2)),
    ("before", re.compile(r"^(%s) comes earlier than (%s)$" % (_N, _N)), (1, 2)),
    ("before", re.compile(r"^(%s) is somewhere before (%s)$" % (_N, _N)), (1, 2)),
    ("before", re.compile(r"^(%s) is placed ahead of (%s)$" % (_N, _N)), (1, 2)),
    ("imm_before", re.compile(r"^(%s) comes right after (%s)$" % (_N, _N)), (2, 1)),
    ("imm_before", re.compile(r"^(%s) sits just before (%s)$" % (_N, _N)), (1, 2)),
    ("imm_before", re.compile(r"^(%s) is directly ahead of (%s), with nothing between$" % (_N, _N)), (1, 2)),
    ("imm_before", re.compile(r"^(%s) is immediately before (%s)$" % (_N, _N)), (1, 2)),
    ("pos_eq", re.compile(r"^(%s) takes position (\d+)$" % _N), (1, None)),
    ("pos_eq", re.compile(r"^(%s) is in position (\d+)$" % _N), (1, None)),
    ("pos_eq", re.compile(r"^(%s) is placed at position (\d+)$" % _N), (1, None)),
    ("pos_eq", re.compile(r"^Position (\d+) holds (%s)$" % _N), (2, None)),
    ("pos_neq", re.compile(r"^Position (\d+) does not hold (%s)$" % _N), (2, None)),
    ("pos_neq", re.compile(r"^(%s) is kept out of position (\d+)$" % _N), (1, None)),
    ("pos_neq", re.compile(r"^(%s) does not take position (\d+)$" % _N), (1, None)),
    ("pos_neq", re.compile(r"^(%s) is not in position (\d+)$" % _N), (1, None)),
    ("not_adjacent", re.compile(r"^(%s) and (%s) do not sit side by side$" % (_N, _N)), (1, 2)),
    ("not_adjacent", re.compile(r"^(%s) and (%s) are not next to each other$" % (_N, _N)), (1, 2)),
    ("not_adjacent", re.compile(r"^There is at least one item between (%s) and (%s)$" % (_N, _N)), (1, 2)),
    ("not_adjacent", re.compile(r"^(%s) is not adjacent to (%s)$" % (_N, _N)), (1, 2)),
    ("adjacent", re.compile(r"^(%s) is adjacent to (%s)$" % (_N, _N)), (1, 2)),
    ("adjacent", re.compile(r"^(%s) and (%s) sit side by side$" % (_N, _N)), (1, 2)),
    ("adjacent", re.compile(r"^(%s) and (%s) are next to each other$" % (_N, _N)), (1, 2)),
    ("adjacent", re.compile(r"^No item lies between (%s) and (%s)$" % (_N, _N)), (1, 2)),
]


def _holds(t, pos, a, b, p):
    if t == "before":
        return pos[a] < pos[b]
    if t == "imm_before":
        return pos[b] == pos[a] + 1
    if t == "pos_eq":
        return pos[a] == p
    if t == "pos_neq":
        return pos[a] != p
    if t == "adjacent":
        return abs(pos[a] - pos[b]) == 1
    if t == "not_adjacent":
        return abs(pos[a] - pos[b]) != 1
    raise ParseFail("unknown_constraint", t)


def solve_l3(stem, options):
    stmts = statements(stem)
    items, start, cons, rest = None, None, [], []
    for s in stmts:
        done = False
        for rx in L3_ITEMS:
            m = rx.match(s)
            if m:
                items = name_list(m.group("items"))
                start = int(m.group("start"))
                done = True
                break
        if done:
            continue
        for t, rx, (ia, ib) in L3_CONS:
            m = rx.match(s)
            if m:
                if t in ("pos_eq", "pos_neq"):
                    if rx.pattern.startswith("^Position"):
                        a, p = m.group(2), int(m.group(1))
                    else:
                        a, p = m.group(1), int(m.group(2))
                    cons.append({"t": t, "a": a, "pos": p})
                else:
                    cons.append({"t": t, "a": m.group(ia), "b": m.group(ib)})
                done = True
                break
        if done:
            continue
        rest.append(s)
    if items is None or start is None:
        raise ParseFail("item_list_not_found", "")
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    if len(set(items)) != len(items):
        raise ParseFail("duplicate_items", "")
    for c in cons:
        for k in ("a", "b"):
            if k in c and c[k] not in items:
                raise ParseFail("constraint_names_unknown_item", c[k])

    def ok(order):
        pos = dict((it, start + i) for i, it in enumerate(order))
        return all(_holds(c["t"], pos, c["a"], c.get("b"), c.get("pos")) for c in cons)

    total = sum(1 for perm in itertools.permutations(items) if ok(perm))
    hits = []
    for i, o in enumerate(options):
        order = name_list(o)
        if sorted(order) != sorted(items):
            raise ParseFail("option_is_not_an_arrangement", o)
        if ok(order):
            hits.append(i)
    idx = pick_unique(hits, "arrangement satisfying all constraints")
    pb = {"form": "LG-L3", "items": list(items), "constraints": cons}
    return {"answer_index": idx, "answer_text": options[idx], "parse": pb, "info": {"solution_count": total}}
