"""GEN / LOGIC sub-block: Horn knowledge bases, arrangement puzzles. SOLVER A = unit propagation (BCP) / backtracking.

Why unit propagation is exact here: every rule body is a conjunction of POSITIVE atoms and every head is a single literal
(positive or negative), facts are literals. So every ground clause has at most one positive literal (Horn), where BCP is
refutation-complete. Entailment of a literal l is decided by assuming its complement and propagating to a conflict.
Solver B (exhaustive model enumeration; permutation brute force) is NOT here.

Forms: LG-L1 (entailed / contradicted / undetermined), LG-L2 (which statement must be true), LG-L3 (which arrangement
satisfies every constraint), LG-L4 (does the conclusion follow).
"""
import itertools

from gen_common import Doc, end_block, item_sep, join_names

CLASSES = ["Entailed", "Contradicted", "Undetermined"]
FLAWS = ["ignored_negation", "converse_fallacy", "over_chaining", "closed_world", "under_chaining", "forward_only", "stated_only", "polarity_misread"]
MAX_ATOMS = 16


# ------------------------------------------------------------------------------------------------
# Atoms, grounding, BCP
# ------------------------------------------------------------------------------------------------
def U(p, e):
    return ("P", p, e)


def R(e1, e2):
    return ("R", e1, e2)


def all_atoms(spec):
    n_e = len(spec["entities"])
    atoms = [U(p, e) for p in range(len(spec["preds"])) for e in range(n_e)]
    if spec["rel"]:
        atoms += [R(a, b) for a in range(n_e) for b in range(n_e) if a != b]
    return atoms


def ground_clauses(spec):
    """[(body_atoms tuple, head_literal)]  head_literal = (atom, sign)."""
    n_e = len(spec["entities"])
    out = []
    for r in spec["rules"]:
        hp, hs = r["head"]
        if r["kind"] == "unary":
            for e in range(n_e):
                out.append((tuple(U(p, e) for p in r["body"]), (U(hp, e), hs)))
        else:
            bp = r["body"][0]
            for x in range(n_e):
                for y in range(n_e):
                    if x != y:
                        out.append(((R(x, y), U(bp, x)), (U(hp, y), hs)))
    return out


def fact_lits(spec):
    return [(tuple(a) if isinstance(a, list) else a, s) for a, s in spec["facts"]]


def _norm_atom(a):
    return tuple(a)


def bcp(clauses, units):
    """Unit propagation. clauses: [(body, head)]; units: iterable of literals. Returns (assign dict atom->bool, conflict, steps)."""
    assign = {}
    steps = 0
    for a, s in units:
        if a in assign and assign[a] != s:
            return assign, True, steps
        assign[a] = s
    lits = [[(b, False) for b in body] + [head] for body, head in clauses]
    changed = True
    while changed:
        changed = False
        for cl in lits:
            sat = False
            unassigned = []
            for a, s in cl:
                v = assign.get(a)
                if v is None:
                    unassigned.append((a, s))
                elif v == s:
                    sat = True
                    break
            if sat:
                continue
            if not unassigned:
                return assign, True, steps
            if len(unassigned) == 1:
                a, s = unassigned[0]
                assign[a] = s
                steps += 1
                changed = True
    return assign, False, steps


def consistent(spec):
    return not bcp(ground_clauses(spec), fact_lits(spec))[1]


def entails(spec, lit, clauses=None, facts=None):
    clauses = clauses if clauses is not None else ground_clauses(spec)
    facts = facts if facts is not None else fact_lits(spec)
    a, s = lit
    _, conflict, _ = bcp(clauses, list(facts) + [(a, not s)])
    return conflict


def classify(spec, lit, clauses=None, facts=None):
    a, s = lit
    if entails(spec, (a, s), clauses, facts):
        return "Entailed"
    if entails(spec, (a, not s), clauses, facts):
        return "Contradicted"
    return "Undetermined"


def derived_steps(spec, lit):
    """BCP steps in the refutation of the complement of an entailed literal (difficulty signal)."""
    a, s = lit
    return bcp(ground_clauses(spec), fact_lits(spec) + [(a, not s)])[2]


# ------------------------------------------------------------------------------------------------
# Flawed solvers (forward chaining) -> trap types
# ------------------------------------------------------------------------------------------------
def flawed_closure(spec, flaw):
    n_e = len(spec["entities"])
    facts = set(fact_lits(spec))
    clauses = ground_clauses(spec)
    if flaw == "ignored_negation":
        facts = {f for f in facts if f[1]}
        clauses = [c for c in clauses if c[1][1]]
    derived = set(facts)
    if flaw == "stated_only":
        return derived
    max_rounds = 1 if flaw == "under_chaining" else 50
    if flaw == "converse_fallacy":
        extra = []
        for body, head in clauses:
            if head[1]:
                for b in body:
                    extra.append(((head[0],), (b, True)))
        clauses = clauses + extra
    for _ in range(max_rounds):
        new = set()
        for body, head in clauses:
            if flaw == "over_chaining" and len(body) >= 2:
                ok = any((b, True) in derived for b in body)
            else:
                ok = all((b, True) in derived for b in body)
            if ok and head not in derived:
                new.add(head)
        if not new:
            break
        derived |= new
    if flaw == "closed_world":
        for a in all_atoms(spec):
            if (a, True) not in derived and (a, False) not in derived:
                derived.add((a, False))
    return derived


def flawed_class(spec, flaw, lit, cache=None):
    if flaw == "polarity_misread":          # reads the statement with its polarity flipped
        t = classify(spec, lit)
        return {"Entailed": "Contradicted", "Contradicted": "Entailed"}.get(t, t)
    c = (cache or {}).get(flaw) or flawed_closure(spec, flaw)
    a, s = lit
    pos, neg = (a, s) in c, (a, not s) in c
    if pos and not neg:
        return "Entailed"
    if neg and not pos:
        return "Contradicted"
    return "Undetermined"


def flawed_outputs(spec, lit):
    cache = {f: flawed_closure(spec, f) for f in FLAWS if f != "polarity_misread"}
    return {f: flawed_class(spec, f, lit, cache) for f in FLAWS}


# ------------------------------------------------------------------------------------------------
# Knowledge-base generation
# ------------------------------------------------------------------------------------------------
def make_kb(rng, namer, form, bin_name="mid", vocab=None):
    for _ in range(300):
        n_e = rng.choice([3, 4])
        n_p = rng.choice([3, 4])
        rel = rng.random() < 0.35
        if rel:
            n_e, n_p = 3, rng.choice([2, 3])
        n_atoms = n_e * n_p + (n_e * (n_e - 1) if rel else 0)
        if n_atoms > MAX_ATOMS:
            continue
        spec = {"version": 1, "form": form, "entities": list(range(n_e)), "preds": list(range(n_p)), "rel": rel,
                "facts": [], "rules": [], "query": None, "options": None}
        # facts
        unary_atoms = [U(p, e) for p in range(n_p) for e in range(n_e)]
        rng.shuffle(unary_atoms)
        nf = rng.randint(3, min(7, len(unary_atoms)))
        seen = set()
        for a in unary_atoms[:nf]:
            spec["facts"].append([list(a), rng.random() < 0.65])
        # every entity must be visible in the stem: give each entity without a fact one fact
        have = {tuple(a)[2] for a, _ in spec["facts"] if tuple(a)[0] == "P"}
        for e in range(n_e):
            if e not in have:
                spec["facts"].append([list(U(rng.randrange(n_p), e)), rng.random() < 0.65])
        if rel:
            pairs = [(a, b) for a in range(n_e) for b in range(n_e) if a != b]
            rng.shuffle(pairs)
            for a, b in pairs[: rng.randint(1, 2)]:
                spec["facts"].append([list(R(a, b)), True])
        # rules
        nr = {"easy": 3, "mid": rng.randint(4, 5), "hard": rng.randint(6, 7)}[bin_name]
        tries = 0
        while len(spec["rules"]) < nr and tries < 60:
            tries += 1
            if rel and rng.random() < 0.35 and not any(r["kind"] == "rel" for r in spec["rules"]):
                bp = rng.randrange(n_p)
                hp = rng.randrange(n_p)
                r = {"kind": "rel", "body": [bp], "head": [hp, rng.random() < 0.6]}
            else:
                nb = 2 if (n_p >= 3 and rng.random() < 0.4) else 1
                body = rng.sample(range(n_p), nb)
                hp = rng.choice([p for p in range(n_p) if p not in body])
                r = {"kind": "unary", "body": sorted(body), "head": [hp, rng.random() < 0.65]}
            if r in spec["rules"]:
                continue
            spec["rules"].append(r)
        if len(spec["rules"]) < 3:
            continue
        if not consistent(spec):
            continue
        # names
        spec["ent_names"] = [namer.entity("e%d" % e) for e in range(n_e)]
        # G0-lite section 9: about half of the LOGIC rows take their predicates from the closed per-domain vocabulary, the rest use
        # nonsense stems from the namespace. The coin is drawn from the row rng, whether or not a vocabulary is supplied, so the stream
        # of draws (and every later random choice) does not depend on the vocabulary being present.
        use_vocab = rng.random() < 0.5
        if use_vocab and vocab and len(vocab) >= n_p:
            spec["pred_names"] = rng.sample(list(vocab), n_p)
            spec["pred_source"] = "vocab"
        else:
            spec["pred_names"] = [namer.lower("predicate", "p%d" % p) for p in range(n_p)]
            spec["pred_source"] = "ns"
        spec["rel_name"] = namer.lower("predicate", "rel") if rel else None
        return spec
    return None


def lit_text(spec, lit):
    a, s = lit
    if a[0] == "P":
        return "%s is %sa %s" % (spec["ent_names"][a[2]], "" if s else "not ", spec["pred_names"][a[1]])
    raise ValueError("relation atoms are not used in statements")


def query_candidates(spec):
    """All unary literals not stated as facts. Returns [(lit, cls)]."""
    clauses, facts = ground_clauses(spec), fact_lits(spec)
    stated = {(a, s) for a, s in facts}
    stated_atoms = {a for a, _ in facts}
    out = []
    for p in spec["preds"]:
        for e in spec["entities"]:
            a = U(p, e)
            for s in (True, False):
                lit = (a, s)
                if lit in stated or (a in stated_atoms):
                    continue
                out.append((lit, classify(spec, lit, clauses, facts)))
    return out


def derivation_depth(spec, lit):
    """Forward-chaining level at which the literal appears (0 = fact); None if only reachable by refutation."""
    derived = {f: 0 for f in fact_lits(spec)}
    clauses = ground_clauses(spec)
    for level in range(1, 30):
        new = {}
        for body, head in clauses:
            if all((b, True) in derived for b in body) and head not in derived and head not in new:
                new[head] = level
        if not new:
            break
        derived.update(new)
    return derived.get(lit)


def difficulty_score(spec, lit=None):
    d = 0
    if lit is not None:
        d = derivation_depth(spec, lit) or 0
    return len(spec["rules"]) + 2 * d + (1 if spec["rel"] else 0)


def bin_of_score(score):
    return "easy" if score <= 5 else ("mid" if score <= 8 else "hard")


def bin_of_rules(spec):
    """Difficulty bin from the size of the rule base only, so the bin carries no information about the answer class."""
    n = len(spec["rules"])
    return "easy" if n <= 3 else ("mid" if n <= 5 else "hard")


def pick_query(spec, want_class, rng):
    cands = [(l, c) for l, c in query_candidates(spec) if c == want_class]
    if want_class != "Undetermined":
        cands = [(l, c) for l, c in cands if (derivation_depth(spec, l if c == "Entailed" else (l[0], not l[1])) or 0) >= 1]
    else:
        used = {p for r in spec["rules"] for p in r["body"]} | {r["head"][0] for r in spec["rules"]}
        cands = [(l, c) for l, c in cands if l[0][1] in used] or cands
    if not cands:
        return None
    return rng.choice(cands)[0]


# ------------------------------------------------------------------------------------------------
# L1 / L4 / L2 items
# ------------------------------------------------------------------------------------------------
def make_l1(rng, namer, bin_name, want, balancer, scope, vocab=None):
    for _ in range(120):
        spec = make_kb(rng, namer, "LG-L1", bin_name, vocab)
        if spec is None:
            continue
        q = pick_query(spec, want, rng)
        if q is None:
            continue
        score = difficulty_score(spec, q if want == "Entailed" else ((q[0], not q[1]) if want == "Contradicted" else None))
        if bin_of_rules(spec) != bin_name:
            continue
        spec["query"] = [list(q[0]), q[1]]
        outs = flawed_outputs(spec, q)
        wrong = [c for c in CLASSES if c != want]
        traps = assign_types(wrong, outs, balancer, scope)
        n_unmod = sum(1 for t in traps if t == "unmodelled")
        if n_unmod and rng.random() < 0.9:
            continue
        return {"spec": spec, "answer": want, "options": [{"text": want, "trap": None, "correct": True}] +
                [{"text": c, "trap": t, "correct": False} for c, t in zip(wrong, traps)], "score": score}
    return None


def assign_types(wrong_classes, outs, balancer, scope):
    res = []
    for w in wrong_classes:
        fl = [f for f, o in outs.items() if o == w]
        res.append(balancer.pick(scope, fl) if fl else "unmodelled")
    return res


def make_l4(rng, namer, bin_name, want_yes, balancer, scope, rid=0, vocab=None):
    for _ in range(80):
        spec = make_kb(rng, namer, "LG-L4", bin_name, vocab)
        if spec is None:
            continue
        want = "Entailed" if want_yes else rng.choice(["Contradicted", "Undetermined"])
        q = pick_query(spec, want, rng)
        if q is None:
            continue
        score = difficulty_score(spec, q if want == "Entailed" else ((q[0], not q[1]) if want == "Contradicted" else None))
        if bin_of_rules(spec) != bin_name:
            continue
        spec["query"] = [list(q[0]), q[1]]
        outs = flawed_outputs(spec, q)
        wrong_ans = "No, it does not follow" if want_yes else "Yes, it follows"
        flaw_yes = {f: ("Yes, it follows" if o == "Entailed" else "No, it does not follow") for f, o in outs.items()}
        t = assign_types([wrong_ans], flaw_yes, balancer, scope)[0]
        yes_t, no_t = "Yes, it follows", "No, it does not follow"
        return {"spec": spec, "answer": "yes" if want_yes else "no", "truth_class": want,
                "options": [{"text": yes_t if want_yes else no_t, "trap": None, "correct": True},
                            {"text": wrong_ans, "trap": t, "correct": False}], "score": score}
    return None


def entailed_nonfact(spec):
    clauses, facts = ground_clauses(spec), fact_lits(spec)
    stated_atoms = {a for a, _ in facts}
    out, non = [], []
    for p in spec["preds"]:
        for e in spec["entities"]:
            a = U(p, e)
            if a in stated_atoms:
                continue
            for s in (True, False):
                c = classify(spec, (a, s), clauses, facts)
                (out if c == "Entailed" else non).append((a, s))
    return out, non


def make_l2(rng, namer, bin_name, balancer, scope, vocab=None):
    for _ in range(100):
        spec = make_kb(rng, namer, "LG-L2", bin_name, vocab)
        if spec is None:
            continue
        ent, non = entailed_nonfact(spec)
        ent = [l for l in ent if (derivation_depth(spec, l) or 0) >= 1]
        if not ent or len(non) < 3:
            continue
        gold = rng.choice(ent)
        score = difficulty_score(spec, gold)
        if bin_of_rules(spec) != bin_name:
            continue
        # flaw tags per candidate distractor
        cache = {f: flawed_closure(spec, f) for f in FLAWS if f != "polarity_misread"}
        tagged = []
        for l in non:
            fl = [f for f in FLAWS if flawed_class(spec, f, l, cache) == "Entailed"]
            tagged.append((l, fl))
        by_type = {}
        for l, fl in tagged:
            for f in fl:
                by_type.setdefault(f, []).append(l)
        unmod = [l for l, fl in tagged if not fl]
        chosen, used_lits = [], set()
        avail = [f for f in by_type]
        while len(chosen) < 3 and avail:
            f = balancer.pick(scope, avail)
            avail.remove(f)
            lits = [l for l in by_type[f] if l not in used_lits]
            if not lits:
                balancer.key_counts(scope)[f] -= 1
                continue
            l = rng.choice(lits)
            used_lits.add(l)
            chosen.append((l, f))
        if len(chosen) < 3:
            rest = [l for l in unmod if l not in used_lits]
            rng.shuffle(rest)
            for l in rest[: 3 - len(chosen)]:
                chosen.append((l, "unmodelled"))
        if len(chosen) < 3:
            continue
        spec["options"] = [[list(gold[0]), gold[1]]] + [[list(l[0]), l[1]] for l, _ in chosen]
        return {"spec": spec, "answer": lit_text(spec, gold), "options": [{"text": lit_text(spec, gold), "trap": None, "correct": True}] +
                [{"text": lit_text(spec, l), "trap": t, "correct": False} for l, t in chosen], "score": score}
    return None


def l2_entailed_options(spec):
    """SOLVER A for L2: the options that are entailed (must be exactly one)."""
    clauses, facts = ground_clauses(spec), fact_lits(spec)
    return [i for i, (a, s) in enumerate(spec["options"]) if entails(spec, (tuple(a), s), clauses, facts)]


def solve_l1(spec):
    a, s = spec["query"]
    return classify(spec, (tuple(a), s))


def solve_l4(spec):
    return "yes" if solve_l1(spec) == "Entailed" else "no"


# ------------------------------------------------------------------------------------------------
# L3 arrangement puzzles
# ------------------------------------------------------------------------------------------------
C_TYPES = ["before", "imm_before", "pos_eq", "pos_neq", "not_adjacent", "adjacent"]


def holds(c, perm):
    """perm: tuple of item indices in position order (position 0 first)."""
    t = c["t"]
    pos = {it: i for i, it in enumerate(perm)}
    if t == "before":
        return pos[c["a"]] < pos[c["b"]]
    if t == "imm_before":
        return pos[c["b"]] == pos[c["a"]] + 1
    if t == "pos_eq":
        return pos[c["a"]] == c["pos"] - 1
    if t == "pos_neq":
        return pos[c["a"]] != c["pos"] - 1
    if t == "not_adjacent":
        return abs(pos[c["a"]] - pos[c["b"]]) != 1
    if t == "adjacent":
        return abs(pos[c["a"]] - pos[c["b"]]) == 1
    raise ValueError(t)


def solve_arrangements(n, cons):
    """SOLVER A for L3: depth-first assignment of items to positions with early pruning. Returns all solutions."""
    sols = []
    pos_of = {}

    def ok_partial(c):
        t = c["t"]
        a, b = c["a"], c.get("b")
        if t in ("pos_eq", "pos_neq"):
            if a in pos_of:
                return (pos_of[a] == c["pos"] - 1) if t == "pos_eq" else (pos_of[a] != c["pos"] - 1)
            return True
        if a in pos_of and b in pos_of:
            pa, pb = pos_of[a], pos_of[b]
            if t == "before":
                return pa < pb
            if t == "imm_before":
                return pb == pa + 1
            if t == "not_adjacent":
                return abs(pa - pb) != 1
            return abs(pa - pb) == 1
        return True

    def rec(position, used):
        if position == n:
            perm = [None] * n
            for it, p in pos_of.items():
                perm[p] = it
            sols.append(tuple(perm))
            return
        for it in range(n):
            if it in used:
                continue
            pos_of[it] = position
            if all(ok_partial(c) for c in cons):
                rec(position + 1, used | {it})
            del pos_of[it]

    rec(0, frozenset())
    return sols


def _rand_constraint(rng, n, target):
    t = rng.choice(C_TYPES)
    a, b = rng.sample(range(n), 2)
    pos = {it: i for i, it in enumerate(target)}
    c = {"t": t, "a": a, "b": b}
    if t == "before" and pos[a] > pos[b]:
        c["a"], c["b"] = b, a
    if t == "imm_before":
        # pick a consecutive pair in the target
        i = rng.randrange(n - 1)
        c["a"], c["b"] = target[i], target[i + 1]
    if t in ("pos_eq", "pos_neq"):
        c = {"t": t, "a": a}
        if t == "pos_eq":
            c["pos"] = pos[a] + 1
        else:
            c["pos"] = rng.choice([p for p in range(1, n + 1) if p != pos[a] + 1])
    if t == "adjacent":
        i = rng.randrange(n - 1)
        c["a"], c["b"] = target[i], target[i + 1]
    if t == "not_adjacent":
        pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if abs(pos[x] - pos[y]) != 1]
        if not pairs:
            return None
        c["a"], c["b"] = rng.choice(pairs)
    return c


def mutate_constraint(c, kind):
    c2 = dict(c)
    if kind == "reversed_relation":
        if c["t"] == "before":
            c2["a"], c2["b"] = c["b"], c["a"]
        elif c["t"] == "imm_before":
            c2["a"], c2["b"] = c["b"], c["a"]
        elif c["t"] == "adjacent":
            c2["t"] = "not_adjacent"
        elif c["t"] == "not_adjacent":
            c2["t"] = "adjacent"
        elif c["t"] == "pos_eq":
            c2["t"] = "pos_neq"
        else:
            c2["t"] = "pos_eq"
        return c2
    if kind == "weakened_relation":
        if c["t"] == "imm_before":
            c2["t"] = "before"
            return c2
        if c["t"] == "adjacent":
            return None
        return None
    return None


def make_l3(rng, namer, bin_name, balancer, scope):
    n_range = {"easy": (4, 4), "mid": (5, 5), "hard": (6, 6)}[bin_name]
    for _ in range(300):
        n = rng.randint(*n_range)
        target = list(range(n))
        rng.shuffle(target)
        m = rng.randint(max(3, n - 1), n + 2)
        cons, tries = [], 0
        while len(cons) < m and tries < 60:
            tries += 1
            c = _rand_constraint(rng, n, target)
            if c is None or c in cons or not holds(c, tuple(target)):
                continue
            cons.append(c)
        if len(cons) < 3:
            continue
        sols = solve_arrangements(n, cons)
        if not (1 <= len(sols) <= 12):
            continue
        # every constraint must matter
        redundant = False
        for i in range(len(cons)):
            if len(solve_arrangements(n, cons[:i] + cons[i + 1:])) == len(sols):
                redundant = True
                break
        if redundant:
            continue
        allp = list(itertools.permutations(range(n)))
        sol_set = set(sols)
        models = {}
        for i, c in enumerate(cons):
            rest = cons[:i] + cons[i + 1:]
            ps = [p for p in solve_arrangements(n, rest) if p not in sol_set]
            if ps:
                models.setdefault("dropped_constraint", []).extend(ps)
            for kind in ("reversed_relation", "weakened_relation"):
                c2 = mutate_constraint(c, kind)
                if c2 is None:
                    continue
                ps2 = [p for p in solve_arrangements(n, rest + [c2]) if p not in sol_set]
                if ps2:
                    models.setdefault(kind, []).extend(ps2)
        gold = rng.choice(sols)
        swaps = []
        for i in range(n - 1):
            q = list(gold)
            q[i], q[i + 1] = q[i + 1], q[i]
            q = tuple(q)
            if q not in sol_set:
                swaps.append(q)
        if swaps:
            models["swap_adjacent"] = swaps
        types = [t for t, v in models.items() if v]
        if len(types) < 3:
            continue
        chosen, used = [], set()
        avail = list(types)
        while len(chosen) < 3 and avail:
            t = balancer.pick(scope, avail)
            avail.remove(t)
            opts = [p for p in models[t] if p not in used]
            if not opts:
                balancer.key_counts(scope)[t] -= 1
                continue
            p = rng.choice(opts)
            used.add(p)
            chosen.append((p, t))
        if len(chosen) < 3:
            continue
        score = n + len(cons)
        names = [namer.entity("i%d" % i) for i in range(n)]
        spec = {"version": 1, "form": "LG-L3", "n": n, "item_names": names, "constraints": cons,
                "options": [list(gold)] + [list(p) for p, _ in chosen]}
        txt = lambda p: ", ".join(names[i] for i in p)
        return {"spec": spec, "answer": txt(gold),
                "options": [{"text": txt(gold), "trap": None, "correct": True}] + [{"text": txt(p), "trap": t, "correct": False} for p, t in chosen],
                "score": score}
    return None


def solve_l3(spec):
    sols = set(solve_arrangements(spec["n"], spec["constraints"]))
    return [i for i, p in enumerate(spec["options"]) if tuple(p) in sols]


# ------------------------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------------------------
def _pred_phrase(spec, p):
    return "is a %s" % spec["pred_names"][p]


def _body_text(spec, r):
    if r["kind"] == "unary":
        return " and ".join(_pred_phrase(spec, p) for p in r["body"])
    return "X %s Y and X is a %s" % (spec["rel_phrase"], spec["pred_names"][r["body"][0]])


def make_rel_phrase(spec):
    return "is %s to" % spec["rel_name"] if spec.get("rel_name") else None


def render_kb(spec, pool, rng, doc, carrier, start_idx=0):
    spec["rel_phrase"] = make_rel_phrase(spec)
    idx = start_idx
    en, pn = spec["ent_names"], spec["pred_names"]
    for a, s in spec["facts"]:
        a = tuple(a)
        item_sep(doc, carrier, idx)
        idx += 1
        if a[0] == "P":
            doc.sentence(pool.get("lg.fact.pos" if s else "lg.fact.neg", rng.randrange(1 << 20)),
                         {"e": (en[a[2]], "entity", "name"), "pred": (pn[a[1]], "entity", "name")})
        else:
            if not s:
                raise ValueError("a negated relation fact has no wording; the stem would state the opposite of the spec")
            doc.sentence(pool.get("lg.rel.fact", rng.randrange(1 << 20)),
                         {"e1": (en[a[1]], "entity", "name"), "rel": (spec["rel_phrase"], "entity", "rule"), "e2": (en[a[2]], "entity", "name")})
    for r in spec["rules"]:
        item_sep(doc, carrier, idx)
        idx += 1
        hp, hs = r["head"]
        if r["kind"] == "unary":
            doc.sentence(pool.get("lg.rule.pos" if hs else "lg.rule.neg", rng.randrange(1 << 20)),
                         {"body": (_body_text(spec, r), "entity", "rule"), "head": (pn[hp], "entity", "name")})
        else:
            head = "Y is %sa %s" % ("" if hs else "not ", pn[hp])
            doc.sentence(pool.get("lg.rule.rel", rng.randrange(1 << 20)),
                         {"body": (_body_text(spec, r), "entity", "rule"), "head": (head, "entity", "rule")})
    return idx


def render(item, pool, widx, rng, domain, carrier="TXT-PROSE"):
    spec = item["spec"]
    form = spec["form"]
    doc = Doc()
    doc.sentence(pool.get("scene." + domain, rng.randrange(1 << 20)), {})
    if form == "LG-L3":
        item_sep(doc, carrier, 0)
        doc.sentence(pool.get("lg.l3.intro", rng.randrange(1 << 20)),
                     {"items": (join_names(spec["item_names"]), "entity", "name")})
        nm = spec["item_names"]
        for i, c in enumerate(spec["constraints"]):
            item_sep(doc, carrier, i + 1)
            t = c["t"]
            vals = {"a": (nm[c["a"]], "entity", "name")}
            if "b" in c:
                vals["b"] = (nm[c["b"]], "entity", "name")
            if "pos" in c:
                vals["pos"] = (str(c["pos"]), "number", "number")
            doc.sentence(pool.get("lg.l3.c." + t, rng.randrange(1 << 20)), vals)
        end_block(doc, carrier)
        doc.sentence(pool.get("q.LG-L3", widx), {})
        return doc.text(), doc.spans
    item_sep(doc, carrier, 0)
    doc.sentence(pool.get("lg.rules_only", rng.randrange(1 << 20)), {})
    render_kb(spec, pool, rng, doc, carrier, 1)
    end_block(doc, carrier)
    if form in ("LG-L1", "LG-L4"):
        a, s = spec["query"]
        doc.sentence(pool.get("q." + form, widx), {"query": (lit_text(spec, (tuple(a), s)), "entity", "statement")})
    else:
        doc.sentence(pool.get("q.LG-L2", widx), {})
    return doc.text(), doc.spans


# ------------------------------------------------------------------------------------------------
# Minimal pairs: edit one slot so the answer changes
# ------------------------------------------------------------------------------------------------
def _edits(spec, rng):
    """Yield single-edit variants of the KB (facts/rules), query and options untouched."""
    out = []
    for i in range(len(spec["facts"])):
        # a relation fact has only a positive wording (lg.rel.fact): flipping its sign would put a statement in the spec that the stem
        # cannot say (the stem would still read as positive), so only unary facts are flipped. (Skeptic fix 18 Oct: LG-L1/L4 pair rows.)
        if tuple(spec["facts"][i][0])[0] == "P":
            out.append(("flip_fact", i))
        out.append(("drop_fact", i))
    for i in range(len(spec["rules"])):
        out.append(("drop_rule", i))
        out.append(("flip_head", i))
    n_e, n_p = len(spec["entities"]), len(spec["preds"])
    stated = {tuple(a) for a, _ in spec["facts"]}
    for p in range(n_p):
        for e in range(n_e):
            if U(p, e) not in stated:
                out.append(("add_fact_pos", (p, e)))
                out.append(("add_fact_neg", (p, e)))
    rng.shuffle(out)
    return out


def _apply(spec, edit):
    s = {k: (list(v) if isinstance(v, list) else v) for k, v in spec.items()}
    s["facts"] = [list(f) for f in spec["facts"]]
    s["rules"] = [dict(r) for r in spec["rules"]]
    kind, arg = edit
    if kind == "flip_fact":
        s["facts"][arg][1] = not s["facts"][arg][1]
    elif kind == "drop_fact":
        del s["facts"][arg]
    elif kind == "drop_rule":
        del s["rules"][arg]
        if len(s["rules"]) < 2:
            return None
    elif kind == "flip_head":
        s["rules"][arg]["head"] = [s["rules"][arg]["head"][0], not s["rules"][arg]["head"][1]]
    elif kind in ("add_fact_pos", "add_fact_neg"):
        s["facts"].append([list(U(*arg)), kind == "add_fact_pos"])
    if len(s["facts"]) < 3:
        return None
    return s


def l3_type_of(p, cons, gold, n):
    """Trap type of a wrong arrangement p under constraint set cons (used to tag minimal-pair rows)."""
    p = tuple(p)
    gold = tuple(gold)
    for i in range(n - 1):
        q = list(gold)
        q[i], q[i + 1] = q[i + 1], q[i]
        if tuple(q) == p:
            return "swap_adjacent"
    bad = [i for i, c in enumerate(cons) if not holds(c, p)]
    if len(bad) == 1:
        c = cons[bad[0]]
        for kind in ("reversed_relation", "weakened_relation"):
            c2 = mutate_constraint(c, kind)
            if c2 is not None and holds(c2, p):
                return kind
        return "dropped_constraint"
    return "unmodelled"


def l2_tag(spec, lit, balancer, scope, cache=None):
    cache = cache or {f: flawed_closure(spec, f) for f in FLAWS if f != "polarity_misread"}
    fl = [f for f in FLAWS if flawed_class(spec, f, lit, cache) == "Entailed"]
    return balancer.pick(scope, fl) if fl else "unmodelled"


def perturb(item, rng, balancer, scope):
    """Same query/options, one KB edit, new answer. Returns a new item or None."""
    spec = item["spec"]
    form = spec["form"]
    if form == "LG-L3":
        cons = spec["constraints"]
        n = spec["n"]
        opts = [tuple(p) for p in spec["options"]]
        old = tuple(solve_l3(spec))
        order = list(range(len(cons)))
        rng.shuffle(order)
        for i in order:
            for kind in ("reversed_relation", "weakened_relation"):
                c2 = mutate_constraint(cons[i], kind)
                if c2 is None:
                    continue
                new = cons[:i] + [c2] + cons[i + 1:]
                s2 = dict(spec)
                s2["constraints"] = new
                sol = tuple(solve_l3(s2))
                if len(sol) == 1 and sol != old:
                    names = spec["item_names"]
                    txt = lambda p: ", ".join(names[x] for x in p)
                    ans = sol[0]
                    opt_items = [{"text": txt(p), "trap": None if k == ans else l3_type_of(p, new, opts[ans], n), "correct": k == ans}
                                 for k, p in enumerate(opts)]
                    return {"spec": s2, "answer": txt(opts[ans]), "options": opt_items, "score": item["score"]}
        return None
    for edit in _edits(spec, rng):
        s2 = _apply(spec, edit)
        if s2 is None or not consistent(s2):
            continue
        if form in ("LG-L1", "LG-L4"):
            a, s = s2["query"]
            c2 = classify(s2, (tuple(a), s))
            c1 = classify(spec, (tuple(a), s))
            outs = flawed_outputs(s2, (tuple(a), s))
            if form == "LG-L1" and c2 != c1:
                wrong = [c for c in CLASSES if c != c2]
                traps = assign_types(wrong, outs, balancer, scope)
                opts = [{"text": c2, "trap": None, "correct": True}] + [{"text": c, "trap": t, "correct": False} for c, t in zip(wrong, traps)]
                return {"spec": s2, "answer": c2, "options": opts, "score": item["score"]}
            if form == "LG-L4" and (c2 == "Entailed") != (c1 == "Entailed"):
                yes = c2 == "Entailed"
                yes_t, no_t = "Yes, it follows", "No, it does not follow"
                wrong_ans = no_t if yes else yes_t
                flaw_yes = {f: (yes_t if o == "Entailed" else no_t) for f, o in outs.items()}
                t = assign_types([wrong_ans], flaw_yes, balancer, scope)[0]
                return {"spec": s2, "answer": "yes" if yes else "no", "truth_class": c2,
                        "options": [{"text": yes_t if yes else no_t, "trap": None, "correct": True}, {"text": wrong_ans, "trap": t, "correct": False}],
                        "score": item["score"]}
        else:
            ents = l2_entailed_options(s2)
            old = l2_entailed_options(spec)
            if len(ents) == 1 and ents != old:
                k = ents[0]
                cache = {f: flawed_closure(s2, f) for f in FLAWS if f != "polarity_misread"}
                opts = []
                for i, (a, sg) in enumerate(s2["options"]):
                    lit = (tuple(a), sg)
                    opts.append({"text": lit_text(s2, lit), "trap": None if i == k else l2_tag(s2, lit, balancer, scope, cache), "correct": i == k})
                return {"spec": s2, "answer": opts[k]["text"], "options": opts, "score": item["score"]}
    return None


def item_bin(item):
    spec = item["spec"]
    if spec["form"] == "LG-L3":
        return {4: "easy", 5: "mid"}.get(spec["n"], "hard")
    return bin_of_rules(spec)
