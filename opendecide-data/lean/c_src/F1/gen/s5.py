"""S5 flowchart text (held out; mix-tuning dev only; G0 F1 v7 section 3 S5, 11.6).

The section 2 structure is compiled into a decision DAG per rule version (numbered steps, each a yes/no test on one
canonical literal with a 'go to' for each answer, or an outcome); amendments become dated revision notes that move
the start step from their effective date. Steps are shared across versions (hash-consed). Gold: solver A on the
structure. Solver B (here: dag_eval) walks the PARSED flowchart over every completion of the unknown facts.
"""
from __future__ import annotations

import itertools
import re
from decimal import Decimal

import lexicon as L
import solver_a as A
from common import fmt_date, fmt_num
from model import Lit

S5_STATEMENTS = {
    "flow": "The flowchart starts at the step that applies on the case's {gov}; at each step the test is answered "
            "for the case and the flow goes to the step named for that answer; a step that names an outcome ends "
            "the flowchart.",
    "rev": "A revision note moves the start step for cases whose {gov} is on or after its effective date; the date "
           "the note was issued does not matter, even when it is later. Notes with the same effective date take "
           "effect together.",
    "missing": "A step that asks whether a field is marked 'not recorded' is answered yes only when the case file "
               "marks that field 'not recorded'.",
}


class DAG:
    def __init__(self):
        self.nodes = {}     # key -> step number
        self.steps = {}     # step number -> ("test", lit_key, yes, no) | ("out", outcome) | ("nr", field, yes, no)

    def node(self, content):
        if content in self.nodes:
            return self.nodes[content]
        n = len(self.steps) + 1
        self.nodes[content] = n
        self.steps[n] = content
        return n


def canon_key(S, m):
    return m.canon(S.attrs)


def versions(S):
    """Change points (notice effective dates) -> list of (from date, representative g)."""
    B = S.policy.B
    eds = sorted({n.edate for n in S.notices})
    pts = [B] + eds
    return pts


def _lits(S):
    seen = {}
    for lit in A.all_lits(S):
        k = canon_key(S, lit)
        seen.setdefault(k, lit)
    return seen


def _feasible(S, assign):
    """Is there a value per field consistent with the canonical literal truth assignment?"""
    by = {}
    for k, v in assign.items():
        by.setdefault(k[0], []).append((k, v))
    for attr, lst in by.items():
        a = S.attrs[attr]
        if a.type == "bool":
            vals = {x[1] for (x, v) in [(k, v) for k, v in lst] for x in [(k[2][0], v)]}
            want = {k[2][0] if v else (not k[2][0]) for k, v in lst}
            if len(want) > 1:
                return False
            continue
        if a.type == "cat":
            ok = [x for x in a.values if all(((x in k[2]) == (k[1] == "in")) == v for k, v in lst)]
            if not ok:
                return False
            continue
        lo, hi = a.lo, a.hi
        step = a.step if a.type == "num" else 1
        pts = {lo, hi}
        for k, v in lst:
            for t in k[2]:
                pts |= {t - step, t, t + step}
        if not any(lo <= x <= hi and all(_tv(k, x) == v for k, v in lst) for x in pts):
            return False
    return True


def _tv(k, x):
    op, args = k[1], k[2]
    if op == "ge":
        return x >= args[0]
    if op == "le":
        return x <= args[0]
    if op == "between":
        return args[0] <= x <= args[1]
    raise ValueError(op)


def compile_version(S, g, dag: DAG, order):
    """Root step of the DAG for the rule version in force at g."""
    lits = _lits(S)
    keys = order

    def outcome(assign):
        ov = {}
        for lit in A.all_lits(S):
            k = canon_key(S, lit)
            if k in assign:
                ov[id(lit)] = assign[k]
        vals = {S.policy.gov: g}
        for kk, a in S.attrs.items():
            if kk not in vals:
                vals[kk] = A.completion_points(S, kk)[0] if a.type != "bool" else False
        A.set_override(ov)
        try:
            r = A.solve_closed(S, vals)
        finally:
            A.set_override(None)
        return r["final"]

    def rec(i, assign):
        if i == len(keys):
            return dag.node(("out", outcome(assign)))
        k = keys[i]
        a1 = dict(assign)
        a1[k] = True
        a0 = dict(assign)
        a0[k] = False
        f1, f0 = _feasible(S, a1), _feasible(S, a0)
        if f1 and not f0:
            return rec(i + 1, a1)
        if f0 and not f1:
            return rec(i + 1, a0)
        y = rec(i + 1, a1)
        n = rec(i + 1, a0)
        if y == n:
            return y
        return dag.node(("test", k, y, n))
    return rec(0, {})


def compile_flowchart(S, max_steps=60):
    """(dag, starts [(from_date, step)], notes [(notice, step)]). Missing-field tests come first."""
    lits = _lits(S)
    keys = sorted(lits, key=lambda k: (k[0], repr(k[1:])))
    dag = DAG()
    starts = []
    for i, d in enumerate(versions(S)):
        root = compile_version(S, d, dag, keys)
        if S.policy.world == "missing" and S.policy.listed:
            m = dag.node(("out", S.policy.M))
            for f in reversed(S.policy.listed):
                root = dag.node(("nr", f, m, root))
        starts.append((d, root))
        if len(dag.steps) > max_steps:
            raise A.Reject("flowchart too large")
    return dag, starts, lits


def render_flowchart(card, S, dag, starts, fm):
    """Text of the steps and the revision notes (base start = step of the first version)."""
    order = {}
    num = {}
    # renumber steps in a breadth-first order from the base start for readability
    seen = []
    q = [s for _, s in starts]
    while q:
        x = q.pop(0)
        if x in num:
            continue
        num[x] = len(num) + 1
        c = dag.steps[x]
        if c[0] in ("test", "nr"):
            q += [c[2], c[3]]
    lits = _lits(S)
    lines = []
    for x in sorted(num, key=lambda z: num[z]):
        c = dag.steps[x]
        n = num[x]
        if c[0] == "out":
            lines.append(f"Step {n}: The outcome is {card['display'][c[1]]}.")
        elif c[0] == "nr":
            lines.append(f"Step {n}: Is the {S.attrs[c[1]].name} marked 'not recorded'? If yes, go to step "
                         f"{num[c[2]]}; if no, go to step {num[c[3]]}.")
        else:
            lit = lits[c[1]]
            lines.append(f"Step {n}: Does it hold that {fm.lit(lit)}? If yes, go to step {num[c[2]]}; if no, go to "
                         f"step {num[c[3]]}.")
    notes = []
    base_start = num[starts[0][1]]
    eds = sorted({n.edate for n in S.notices})
    for d, st in starts[1:]:
        ns = [n for n in S.notices if n.edate == d]
        for n in sorted(ns, key=lambda n: n.num):
            notes.append(f"Revision note {n.num} (issued {fm.date(n.ndate)}; effective {fm.date(n.edate)}): from its "
                         f"effective date the flowchart starts at step {num[st]}.")
    head = f"The flowchart starts at step {base_start}."
    return head, lines, notes


# ---------------------------------------------------------------- parse + evaluate (solver B side)

STEP_RX = re.compile(r"Step (?P<n>\d+): (?:The outcome is (?P<o>[^.]+)\.|Is the (?P<nf>.+?) marked 'not recorded'\? If "
                     r"yes, go to step (?P<ny>\d+); if no, go to step (?P<nn>\d+)\.|Does it hold that (?P<t>.+?)\? If "
                     r"yes, go to step (?P<y>\d+); if no, go to step (?P<no>\d+)\.)")
NOTE_RX = re.compile(r"Revision note (?P<n>\d+) \(issued (?P<nd>[^;]+); effective (?P<ed>[^)]+)\): from its effective "
                     r"date the flowchart starts at step (?P<s>\d+)\.")
START_RX = re.compile(r"The flowchart starts at step (?P<s>\d+)\.")


def parse_flowchart(text, parser):
    """{step: content}, base start, [(effective date, start step)] from the state text, literals via the row parser."""
    from parse_f1 import pdate
    steps = {}
    for m in STEP_RX.finditer(text):
        n = int(m.group("n"))
        if m.group("o") is not None:
            steps[n] = ("out", m.group("o"))
        elif m.group("nf") is not None:
            steps[n] = ("nr", m.group("nf"), int(m.group("ny")), int(m.group("nn")))
        else:
            lit, j = parser.parse_lit(m.group("t"), 0)
            if j != len(m.group("t")):
                raise ValueError("step test not fully read")
            steps[n] = ("test", lit, int(m.group("y")), int(m.group("no")))
    sm = START_RX.search(text)
    base = int(sm.group("s"))
    notes = [(pdate(m.group("ed")), int(m.group("s"))) for m in NOTE_RX.finditer(text)]
    return steps, base, notes


def dag_eval(steps, base, notes, attrs, vals, notrec, g):
    start = base
    for d, s in sorted(notes):
        if g >= d:
            start = s
    cur = start
    for _ in range(500):
        c = steps[cur]
        if c[0] == "out":
            return c[1]
        if c[0] == "nr":
            cur = c[2] if c[1] in notrec else c[3]
            continue
        lit = c[1]
        a = attrs[lit.attr]
        import solver_b as SB
        cur = c[2] if SB.truth(lit, attrs, vals) else c[3]
    raise ValueError("flowchart loop")


# ---------------------------------------------------------------- S5 rows (dev only)

def s5_statements(card, S):
    from cards import fill_statement
    out = []
    w, q = card["world"], card["qtype"]
    rows = []
    if w == "closed":
        rows.append(1)
    elif w == "open":
        rows += ["2a"] + (["2cbd"] if q == "Q1" else []) + (["2yn"] if q == "Q3" else [])
    else:
        rows += [1, 3]
    rows += [4] + ([38] if (w == "open" and q == "Q1") else []) + [39, 40]
    ops = set()
    for lit in A.all_lits(S):
        a = S.attrs[lit.attr]
        if a.type == "num":
            ops.add({"ge": 8, "le": 9, "gt": 10, "lt": 11, "between": 12, "within": 18}[lit.op])
        elif a.type == "date":
            ops.add(16)
        elif a.type == "cat":
            ops.add(15)
    for r in rows:
        out.append((r, "answer", fill_statement(card, r)))
    for r in sorted(ops, key=str):
        out.append((r, "policy", fill_statement(card, r)))
    gov = S.attrs[S.policy.gov].name
    out.append(("flow", "policy", S5_STATEMENTS["flow"].format(gov=gov)))
    if S.notices:
        out.append(("rev", "policy", S5_STATEMENTS["rev"].format(gov=gov)))
    if w == "missing":
        out.append(("missing", "policy", S5_STATEMENTS["missing"]))
    out.append((36, "policy", fill_statement(card, 36)))
    out.append((37, "policy", fill_statement(card, 37)))
    return out


def s5_doc(card, S, case, fm, rng, stmts, attack=None):
    from render_f1 import policy_header
    dag, starts, lits = S._s5
    head, steps, notes = render_flowchart(card, S, dag, starts, fm)
    T = card["titles"]
    blocks = [{"type": "para", "text": policy_header(card, S)}]
    if card["qtype"] != "Q3":
        pol = [t for r, g, t in stmts if g == "policy"]
        blocks.append({"type": "section", "heading": T["interp"], "blocks": [{"type": "items", "items": pol}]})
    blocks.append({"type": "section", "heading": T["fields"], "blocks": [{"type": "items",
                                                                       "items": fm.fields_items()}]})
    blocks.append({"type": "section", "heading": "Flowchart", "blocks": [{"type": "para", "text": head},
                                                                        {"type": "items", "items": steps}]})
    if notes:
        blocks.append({"type": "section", "heading": "Revision notes", "blocks": [{"type": "items", "items": notes}]})
    sents = fm.case_sentences(case, rng, include_false=(S.policy.world == "open"))
    blocks.append({"type": "section", "heading": T["case"], "blocks": [{"type": "items", "items": sents}]})
    return {"title": f"{card['body']}: {card['subj']} flowchart", "blocks": blocks}


def gate_s5(out_row, vocab, gold_canon, card):
    """Parse the S5 row back (header, fields, flowchart, case, question) and walk the parsed flowchart over every
    completion of the unknown facts (solver B side); the result must equal the row gold."""
    import parse_f1 as PF
    P = PF.Parser(out_row, vocab)
    shown, short = P.find_statements()
    hdr = PF.HEADER_RX.search(P.state_flat)
    if not hdr:
        raise PF.ParseError("header")
    attrs = P.parse_fields()
    P.setup_lexicon(attrs)
    gov = hdr.group("gov")
    steps, base, notes = parse_flowchart("\n".join(P.lines), P)
    world = "open" if "2a" in shown else ("missing" if 3 in shown else "closed")
    q = P._question()
    P.q = q
    P.none_label = None
    from model import Policy, Struct
    S = Struct(attrs=attrs, rules=[], notices=[], inert=[], policy=Policy(
        world=world, prim="SPEC", sec=None, tie="esc", strict=(), outcomes=(), roles={}, valence={}, default="",
        escalate="", fallback=None, M=None, gov=gov, body="", B=PF.pdate(hdr.group("B"))))
    cases = P._cases(S, world)
    case = cases[0]
    # completions of the unknown facts: one value per region cut by the flowchart's tests
    keys = sorted(case.unknown)
    cand = []
    for k in keys:
        a = attrs[k]
        if a.type == "bool":
            cand.append([True, False])
        elif a.type == "cat":
            cand.append(list(a.values))
        else:
            st = a.step if a.type == "num" else 1
            pts = {a.lo, a.hi}
            for c in steps.values():
                if c[0] == "test" and c[1].attr == k:
                    for t in c[1].args:
                        pts |= {t - st, t, t + st}
            cand.append(sorted(x for x in pts if a.lo <= x <= a.hi))
    finals = set()
    g = case.vals[gov]
    for combo in itertools.product(*cand) if keys else [()]:
        v = dict(case.vals)
        v.update(zip(keys, combo))
        finals.add(dag_eval(steps, base, notes, attrs, v, case.notrec, g))
    if q["qtype"] == "Q3":
        X = q["X"]
        if q["pol"] in ("aff", "dneg"):
            ans = 1 if finals == {X} else 0 if X not in finals else None
        else:
            ans = 1 if X not in finals else 0 if finals == {X} else None
        return ans
    cbd = shown.get("2cbd", {}).get("cbd")
    return finals.pop() if len(finals) == 1 else cbd
