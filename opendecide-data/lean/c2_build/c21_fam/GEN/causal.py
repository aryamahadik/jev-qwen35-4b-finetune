"""GEN / CAUSAL sub-block. SOLVER A = direct SCM evaluation with intervention / abduction, role classification from direct
arrows, backdoor test by path rules, d-separation by ball passing. Solver B (independent SCM simulation, moralised
ancestral graph d-separation, exhaustive adjustment-set enumeration) is NOT here.

Forms: CA-C1 outcome under an intervention, CA-C2 counterfactual outcome, CA-C3 role of a variable, CA-C4 valid adjustment
set, CA-C5 must X and Y be independent given Z.
Binding condition C1 (Opus 18 Oct): C4 and C5 rows state that the variables without incoming arrows are independent random
inputs and give NO fixed exogenous values; gold = graph criteria. C1/C2 rows carry the full SCM.
"""
import itertools

from gen_common import Doc, end_block, item_sep, join_names, pick_options_ranked

M = 8                      # every variable takes a whole value 0..7
ROLES = ["confounder", "mediator", "collider", "none"]
FN_KINDS = ["sum", "min", "max", "thr", "xor", "wsum"]


# ------------------------------------------------------------------------------------------------
# DAG helpers (variables are 0..n-1 in topological order: every edge goes from a lower to a higher index)
# ------------------------------------------------------------------------------------------------
def children_of(parents, n):
    ch = {j: [] for j in range(n)}
    for j, ps in parents.items():
        for p in ps:
            ch[p].append(j)
    return ch


def descendants(parents, n, v):
    ch = children_of(parents, n)
    seen, stack = set(), [v]
    while stack:
        x = stack.pop()
        for c in ch[x]:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def ancestors(parents, v):
    seen, stack = set(), [v]
    while stack:
        x = stack.pop()
        for p in parents[x]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def random_dag(rng, n, p_edge, min_parents_after=0):
    parents = {j: [] for j in range(n)}
    for j in range(1, n):
        for i in range(j):
            if rng.random() < p_edge:
                parents[j].append(i)
        parents[j].sort()
    return parents


def edges_of(parents):
    return [(p, j) for j, ps in parents.items() for p in ps]


def parents_from_edges(n, edges):
    parents = {j: [] for j in range(n)}
    for a, b in edges:
        parents[b].append(a)
    for j in parents:
        parents[j].sort()
    return parents


def norm(spec):
    """JSON turns int dict keys into strings; restore them (idempotent)."""
    if all(isinstance(k, int) for k in spec["parents"]):
        return spec
    s = dict(spec)
    s["parents"] = {int(k): v for k, v in spec["parents"].items()}
    for key in ("fn", "roots", "obs"):
        if key in spec:
            s[key] = {int(k): v for k, v in spec[key].items()}
    return s


# ------------------------------------------------------------------------------------------------
# SCM functions
# ------------------------------------------------------------------------------------------------
def apply_fn(fn, pv):
    k = fn["kind"]
    if k == "sum":
        return sum(pv) % M
    if k == "min":
        return min(pv)
    if k == "max":
        return max(pv)
    if k == "thr":
        return 1 if sum(pv) >= fn["t"] else 0
    if k == "xor":
        r = 0
        for v in pv:
            r ^= v
        return r
    if k == "wsum":
        return max(0, min(M - 1, sum(w * v for w, v in zip(fn["w"], pv))))
    raise ValueError(k)


def random_fn(rng, n_parents):
    if n_parents == 1:
        kind = rng.choice(["wsum", "wsum", "thr"])
    else:
        kind = rng.choice(FN_KINDS)
    fn = {"kind": kind}
    if kind == "thr":
        fn["t"] = rng.randint(2, 4) if n_parents == 1 else rng.randint(3, 9)
    if kind == "wsum":
        if n_parents == 1:
            fn["w"] = [rng.choice([2, 3])]
        else:
            w = [rng.choice([1, 1, 2, -1, -2]) for _ in range(n_parents)]
            if all(x < 0 for x in w):
                w[0] = 1
            fn["w"] = w
    return fn


def fn_text(fn, names, noise=False):
    t = _fn_text(fn, names, noise)
    return "(%s)" % t if noise else t


def _fn_text(fn, names, noise=False):
    k = fn["kind"]
    if k == "sum":
        return "the sum of %s%s" % (join_names(names), "" if noise else ", mod 8")
    if k == "min":
        return "the %s of %s" % ("smaller" if len(names) == 2 else "smallest", join_names(names))
    if k == "max":
        return "the %s of %s" % ("larger" if len(names) == 2 else "largest", join_names(names))
    if k == "thr":
        s = names[0] if len(names) == 1 else " plus ".join(names)
        return "1 if %s is at least %d, otherwise 0" % (s, fn["t"])
    if k == "xor":
        return "%s combined by bitwise xor on their 3-bit values" % join_names(names)
    if k == "wsum":
        parts = []
        for i, (w, nm) in enumerate(zip(fn["w"], names)):
            sign = "-" if w < 0 else "+"
            term = "%d*%s" % (abs(w), nm)
            parts.append((("- " if w < 0 else "") + term) if i == 0 else "%s %s" % (sign, term))
        return "%s, limited to the range 0 to 7" % " ".join(parts)
    raise ValueError(k)


# ------------------------------------------------------------------------------------------------
# C1 / C2 : structural causal model
# ------------------------------------------------------------------------------------------------
def make_scm(rng, namer, form, bin_name):
    n = {"easy": 4, "mid": rng.choice([5, 6]), "hard": 7}[bin_name]
    for _ in range(200):
        parents = random_dag(rng, n, 0.45)
        for j in range(1, n):
            if not parents[j] and rng.random() < 0.8:
                parents[j] = [rng.randrange(j)]
            if len(parents[j]) > 3:
                parents[j] = parents[j][:3]
        roots = [j for j in range(n) if not parents[j]]
        if len(roots) > n - 2:
            continue
        fn = {j: random_fn(rng, len(parents[j])) for j in range(n) if parents[j]}
        spec = {"version": 1, "form": form, "n": n, "parents": {j: parents[j] for j in range(n)}, "fn": fn,
                "noise": form == "CA-C2", "var_names": [namer.lower("variable", "v%d" % j) for j in range(n)]}
        root_vals = {j: rng.randrange(M) for j in roots}
        if form == "CA-C1":
            spec["roots"] = root_vals
            obs = eval_scm(spec)
        else:
            u = {j: rng.randrange(M) for j in range(n) if parents[j]}
            tmp = dict(spec)
            tmp["roots"] = root_vals
            obs = eval_scm(tmp, u=u)
            spec["obs"] = obs
        # intervention
        cands = [(x, y) for x in range(n) for y in descendants(spec["parents"], n, x)]
        if not cands:
            continue
        x, y = rng.choice(cands)
        xv = rng.choice([v for v in range(M) if v != obs[x]])
        spec["do"] = {"var": x, "val": xv}
        spec["target"] = y
        ans = solve(spec)
        base = obs[y]
        if ans == base:
            continue
        spec["roots"] = root_vals if form == "CA-C1" else {j: obs[j] for j in roots}
        return spec
    return None


def eval_scm(spec, do=None, u=None, observed_for=None):
    """Forward evaluation. do: {var: val}. u: hidden inputs {var: val} (noise form). observed_for: {var: val} values
    to use for parents that are NOT recomputed (the no_propagation flaw)."""
    spec = norm(spec)
    n = spec["n"]
    parents = spec["parents"]
    vals = {}
    for j in range(n):
        if do and j in do:
            vals[j] = do[j]
            continue
        ps = parents[j]
        if not ps:
            vals[j] = spec["roots"][j]
            continue
        pv = [(observed_for[p] if (observed_for is not None and p in observed_for) else vals[p]) for p in ps]
        g = apply_fn(spec["fn"][j], pv)
        if spec["noise"]:
            g = (g + (u or {}).get(j, 0)) % M
        vals[j] = g
    return vals


def abduct(spec):
    """Hidden input of each non-root variable from the recorded world (noise form)."""
    spec = norm(spec)
    obs = spec["obs"]
    u = {}
    for j in range(spec["n"]):
        ps = spec["parents"][j]
        if ps:
            g = apply_fn(spec["fn"][j], [obs[p] for p in ps])
            u[j] = (obs[j] - g) % M
    return u


def solve(spec):
    """SOLVER A for C1 / C2: value of the target after the intervention."""
    spec = norm(spec)
    do = {spec["do"]["var"]: spec["do"]["val"]}
    if spec["noise"]:
        tmp = dict(spec)
        tmp["roots"] = {j: spec["obs"][j] for j in range(spec["n"]) if not spec["parents"][j]}
        return eval_scm(tmp, do=do, u=abduct(spec))[spec["target"]]
    return eval_scm(spec, do=do)[spec["target"]]


def scm_flaw_values(spec):
    """{trap_type: value}. Each is a plain mis-reading of the question."""
    spec = norm(spec)
    y, x, xv = spec["target"], spec["do"]["var"], spec["do"]["val"]
    n = spec["n"]
    correct = solve(spec)
    out = {}
    if spec["noise"]:
        tmp = dict(spec)
        tmp["roots"] = {j: spec["obs"][j] for j in range(n) if not spec["parents"][j]}
        obs = spec["obs"]
        u = abduct(spec)
        out["use_observed"] = obs[y]
        out["skip_abduction"] = eval_scm(tmp, do={x: xv}, u={})[y]
        out["no_propagation"] = eval_scm(tmp, do={x: xv}, u=u, observed_for={j: obs[j] for j in range(n) if j != x})[y]
        out["off_by_one_value"] = eval_scm(tmp, do={x: (xv + 1) % M}, u=u)[y]
        others = [w for w in range(n) if w not in (x, y)]
        if others:
            w = others[0]
            out["wrong_variable"] = eval_scm(tmp, do={w: xv}, u=u)[y]
    else:
        obs = eval_scm(spec)
        out["ignore_intervention"] = obs[y]
        out["no_propagation"] = eval_scm(spec, do={x: xv}, observed_for={j: obs[j] for j in range(n) if j != x})[y]
        out["off_by_one_value"] = eval_scm(spec, do={x: (xv + 1) % M})[y]
        others = [w for w in range(n) if w not in (x, y)]
        if others:
            out["wrong_variable"] = eval_scm(spec, do={others[0]: xv})[y]
    return {t: v for t, v in out.items() if v != correct}


def pick_value_options(spec_correct, flaws, k, rng, balancer, scope):
    return pick_options_ranked(spec_correct, {t: [v] for t, v in flaws.items()}, k, rng, balancer, scope)


def make_c1_c2(form, rng, namer, bin_name, balancer, scope):
    for _ in range(80):
        spec = make_scm(rng, namer, form, bin_name)
        if spec is None:
            continue
        ans = solve(spec)
        ch = pick_value_options(ans, scm_flaw_values(spec), 4, rng, balancer, scope)
        if ch is None:
            continue
        opts = [{"text": str(ans), "trap": None, "correct": True}] + [{"text": str(v), "trap": t, "correct": False} for v, t in ch]
        depth = len(descendants(spec["parents"], spec["n"], spec["do"]["var"]))
        return {"spec": spec, "answer": ans, "options": opts, "score": spec["n"] + depth}
    return None


def perturb_scm(item, rng, balancer, scope):
    spec = item["spec"]
    old = solve(spec)
    vals = [v for v in range(M) if v != spec["do"]["val"]]
    rng.shuffle(vals)
    for v in vals:
        s2 = dict(spec)
        s2["do"] = {"var": spec["do"]["var"], "val": v}
        ans = solve(s2)
        if ans == old:
            continue
        ch = pick_value_options(ans, scm_flaw_values(s2), 4, rng, balancer, scope)
        if ch is None:
            continue
        return {"spec": s2, "answer": ans, "options": [{"text": str(ans), "trap": None, "correct": True}] +
                [{"text": str(x), "trap": t, "correct": False} for x, t in ch], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# C3 : role of a variable
# ------------------------------------------------------------------------------------------------
def role_direct(parents, n, z, t, o):
    ps = parents
    if z in ps[t] and z in ps[o]:
        return "confounder"
    if t in ps[z] and z in ps[o]:
        return "mediator"
    if t in ps[z] and o in ps[z]:
        return "collider"
    return "none"


def role_reachability(parents, n, z, t, o):
    anc_t, anc_o = ancestors(parents, t), ancestors(parents, o)
    desc_t, desc_o = descendants(parents, n, t), descendants(parents, n, o)
    if z in anc_t and z in anc_o:
        return "confounder"
    if z in desc_t and z in anc_o:
        return "mediator"
    if z in desc_t and z in desc_o:
        return "collider"
    return "none"


def c3_flaws(spec):
    parents, n, z, t, o = spec["parents"], spec["n"], spec["z"], spec["t"], spec["o"]
    parents = {int(k): v for k, v in parents.items()}
    out = {}
    rev_edges = [(b, a) for a, b in edges_of(parents)]
    rp = parents_from_edges(n, rev_edges)
    out["reversed_arrows"] = {role_direct(rp, n, z, t, o)}
    out["swap_t_o"] = {role_direct(parents, n, z, o, t)}
    out["indirect_as_direct"] = {role_reachability(parents, n, z, t, o)}
    miss = set()
    for e in edges_of(parents):
        p2 = parents_from_edges(n, [x for x in edges_of(parents) if x != e])
        miss.add(role_direct(p2, n, z, t, o))
    out["missed_edge"] = miss
    adj = lambda a, b: a in parents[b] or b in parents[a]
    out["direction_ignored"] = {"confounder", "mediator", "collider"} if (adj(z, t) and adj(z, o)) else {"none"}
    loose = set()
    if z in parents[t] or z in parents[o]:
        loose.add("confounder")
    if t in parents[z] or z in parents[o]:
        loose.add("mediator")
    if t in parents[z] or o in parents[z]:
        loose.add("collider")
    out["one_arrow_enough"] = loose or {"none"}
    return out


def make_c3(rng, namer, bin_name, want, balancer, scope):
    n = {"easy": 4, "mid": 5, "hard": 6}[bin_name]
    for _ in range(300):
        order = list(range(n))        # topological = index order, T/O/Z roles are random indices
        t, o, z = rng.sample(order, 3)
        edges = set()

        def add(a, b):
            lo, hi = (a, b) if a < b else (b, a)
            return (lo, hi)
        # plant by rank: need directions consistent with index order; so choose roles by rank
        ranks = sorted(rng.sample(order, 3))
        if want == "confounder":
            z, t, o = ranks[0], ranks[1], ranks[2]
            if rng.random() < 0.5:
                t, o = o, t
            edges |= {(z, t), (z, o)}
        elif want == "mediator":
            t, z, o = ranks
            edges |= {(t, z), (z, o)}
        elif want == "collider":
            a, b, z = ranks
            t, o = (a, b) if rng.random() < 0.5 else (b, a)
            edges |= {(t, z), (o, z)}
        else:
            z, t, o = rng.sample(order, 3)
        # extra edges kept only if the role is unchanged
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in edges]
        rng.shuffle(pairs)
        target_edges = rng.randint(max(3, n - 1), n + 2)
        for a, b in pairs:
            if len(edges) >= target_edges:
                break
            e2 = edges | {(a, b)}
            p2 = parents_from_edges(n, sorted(e2))
            if role_direct(p2, n, z, t, o) == want:
                edges = e2
        parents = parents_from_edges(n, sorted(edges))
        if role_direct(parents, n, z, t, o) != want or len(edges) < 3:
            continue
        spec = {"version": 1, "form": "CA-C3", "n": n, "parents": {j: parents[j] for j in range(n)}, "z": z, "t": t, "o": o,
                "var_names": [namer.lower("variable", "v%d" % j) for j in range(n)]}
        fl = c3_flaws(spec)
        wrong = [r for r in ROLES if r != want]
        traps = []
        for w in wrong:
            ft = [f for f, outs in fl.items() if w in outs]
            traps.append(balancer.pick(scope, ft) if ft else "unmodelled")
        if sum(1 for x in traps if x == "unmodelled") and rng.random() < 0.95:
            continue
        return {"spec": spec, "answer": want, "options": [{"text": want, "trap": None, "correct": True}] +
                [{"text": w, "trap": tr, "correct": False} for w, tr in zip(wrong, traps)], "score": n + len(edges) - 3}
    return None


def solve_c3(spec):
    parents = {int(k): v for k, v in spec["parents"].items()}
    return role_direct(parents, spec["n"], spec["z"], spec["t"], spec["o"])


def perturb_c3(item, rng, balancer, scope):
    spec = item["spec"]
    n = spec["n"]
    parents = {int(k): v for k, v in spec["parents"].items()}
    edges = edges_of(parents)
    old = solve_c3(spec)
    cand = [("del", e) for e in edges] + [("add", (a, b)) for a in range(n) for b in range(a + 1, n) if (a, b) not in edges]
    rng.shuffle(cand)
    for kind, e in cand:
        e2 = [x for x in edges if x != e] if kind == "del" else edges + [e]
        p2 = parents_from_edges(n, e2)
        s2 = dict(spec)
        s2["parents"] = {j: p2[j] for j in range(n)}
        new = solve_c3(s2)
        if new == old or len(e2) < 3:
            continue
        fl = c3_flaws(s2)
        wrong = [r for r in ROLES if r != new]
        traps = []
        for w in wrong:
            ft = [f for f, outs in fl.items() if w in outs]
            traps.append(balancer.pick(scope, ft) if ft else "unmodelled")
        return {"spec": s2, "answer": new, "options": [{"text": new, "trap": None, "correct": True}] +
                [{"text": w, "trap": tr, "correct": False} for w, tr in zip(wrong, traps)], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# C4 : backdoor / adjustment sets   (SOLVER A: path rules)
# ------------------------------------------------------------------------------------------------
def undirected_paths(parents, n, s, t):
    """All simple paths s..t in the skeleton. Returns lists of nodes."""
    nbr = {j: set() for j in range(n)}
    for b, ps in parents.items():
        for a in ps:
            nbr[a].add(b)
            nbr[b].add(a)
    out = []

    def rec(path):
        v = path[-1]
        if v == t:
            out.append(list(path))
            return
        for w in sorted(nbr[v]):
            if w not in path:
                path.append(w)
                rec(path)
                path.pop()
    rec([s])
    return out


def path_blocked(parents, n, path, Z, desc_cache):
    for i in range(1, len(path) - 1):
        a, m, b = path[i - 1], path[i], path[i + 1]
        into_m_from_a = a in parents[m]
        into_m_from_b = b in parents[m]
        collider = into_m_from_a and into_m_from_b
        if collider:
            if m not in Z and not (desc_cache[m] & Z):
                return True
        else:
            if m in Z:
                return True
    return False


def backdoor_valid(spec, Z):
    parents = {int(k): v for k, v in spec["parents"].items()}
    n, t, o = spec["n"], spec["t"], spec["o"]
    Z = set(Z)
    desc = {j: descendants(parents, n, j) for j in range(n)}
    if Z & desc[t]:
        return False
    for path in undirected_paths(parents, n, t, o):
        if len(path) >= 2 and path[1] in parents[t]:       # first edge points INTO t
            if not path_blocked(parents, n, path, Z, desc):
                return False
    return True


def c4_invalid_type(spec, Z, valid_sets=None):
    parents = {int(k): v for k, v in spec["parents"].items()}
    n, t, o = spec["n"], spec["t"], spec["o"]
    Z = set(Z)
    desc = {j: descendants(parents, n, j) for j in range(n)}
    bad_desc = Z & desc[t]
    if bad_desc:
        anc_o = ancestors(parents, o)
        return "includes_mediator" if any(z in anc_o for z in bad_desc) else "includes_descendant"
    if not Z:
        return "empty_set"
    # a path blocked at the empty set but open with Z -> a conditioned collider opened it
    for path in undirected_paths(parents, n, t, o):
        if len(path) >= 2 and path[1] in parents[t]:
            if path_blocked(parents, n, path, set(), desc) and not path_blocked(parents, n, path, Z, desc):
                return "collider_opened"
    if valid_sets is not None:
        others = [j for j in range(n) if j not in (t, o) and j not in Z]
        if any(frozenset(Z | {x}) in valid_sets for x in others):
            return "one_short"
        return "several_short"
    return "incomplete"


def set_text(spec, Z):
    names = sorted(spec["var_names"][j] for j in Z)
    return "{" + ", ".join(names) + "}" if names else "{}"


def c4_pick_options(spec, rng, balancer, scope, prefer=(), forbid_gold=()):
    """Returns (gold frozenset, [(Z, type)]) or None. `prefer`: option sets to keep when still invalid / valid."""
    n, t, o = spec["n"], spec["t"], spec["o"]
    others = [j for j in range(n) if j not in (t, o)]
    subsets = [frozenset(c) for r in range(len(others) + 1) for c in itertools.combinations(others, r)]
    valid = [Z for Z in subsets if backdoor_valid(spec, Z) and Z not in forbid_gold]
    invalid = [Z for Z in subsets if not backdoor_valid(spec, Z)]
    if not valid or len(invalid) < 3:
        return None
    pv = [Z for Z in valid if Z in prefer]
    gold = rng.choice(pv or valid)
    vset = set(valid)
    keep = [Z for Z in invalid if Z in prefer]
    rng.shuffle(keep)
    chosen = [(Z, c4_invalid_type(spec, Z, vset)) for Z in keep[:3]]
    if len(chosen) < 3:
        by_type = {}
        for Z in invalid:
            if Z not in [c for c, _ in chosen]:
                by_type.setdefault(c4_invalid_type(spec, Z, vset), []).append(Z)
        have = {tt for _, tt in chosen}
        avail = [tt for tt in by_type if tt not in have] or list(by_type)
        while len(chosen) < 3 and avail:
            tt = balancer.pick(scope, avail)
            avail.remove(tt)
            Z = rng.choice(by_type[tt])
            chosen.append((Z, tt))
    if len(chosen) < 3:
        return None
    return gold, chosen


def make_c4(rng, namer, bin_name, balancer, scope):
    n = {"easy": 5, "mid": 6, "hard": 7}[bin_name]
    for _ in range(300):
        parents = random_dag(rng, n, 0.4)
        t, o = rng.sample(range(n), 2)
        spec = {"version": 1, "form": "CA-C4", "n": n, "parents": {j: parents[j] for j in range(n)}, "t": t, "o": o,
                "var_names": [namer.lower("variable", "v%d" % j) for j in range(n)]}
        has_bd = any(len(p) >= 2 and p[1] in parents[t] for p in undirected_paths(parents, n, t, o))
        if not has_bd and rng.random() < 0.8:
            continue
        r = c4_pick_options(spec, rng, balancer, scope)
        if r is None:
            continue
        gold, chosen = r
        spec["options"] = [sorted(gold)] + [sorted(Z) for Z, _ in chosen]
        score = n + len(edges_of(parents)) - 3
        return {"spec": spec, "answer": set_text(spec, gold),
                "options": [{"text": set_text(spec, gold), "trap": None, "correct": True}] +
                [{"text": set_text(spec, Z), "trap": tt, "correct": False} for Z, tt in chosen], "score": score}
    return None


def solve_c4(spec):
    return [i for i, Z in enumerate(spec["options"]) if backdoor_valid(spec, Z)]


def perturb_c4(item, rng, balancer, scope):
    """One edge toggled; the valid set changes; as many of the old option sets as stay meaningful are kept."""
    spec = item["spec"]
    n = spec["n"]
    parents = {int(k): v for k, v in spec["parents"].items()}
    edges = edges_of(parents)
    old = solve_c4(spec)
    old_gold = frozenset(spec["options"][old[0]])
    old_opts = {frozenset(Z) for Z in spec["options"]}
    cand = [("del", e) for e in edges] + [("add", (a, b)) for a in range(n) for b in range(a + 1, n) if (a, b) not in edges]
    rng.shuffle(cand)
    for kind, e in cand:
        e2 = [x for x in edges if x != e] if kind == "del" else edges + [e]
        p2 = parents_from_edges(n, e2)
        s2 = dict(spec)
        s2["parents"] = {j: p2[j] for j in range(n)}
        r = c4_pick_options(s2, rng, balancer, scope, prefer=old_opts, forbid_gold=(old_gold,))
        if r is None:
            continue
        gold, chosen = r
        s2["options"] = [sorted(gold)] + [sorted(Z) for Z, _ in chosen]
        return {"spec": s2, "answer": set_text(s2, gold),
                "options": [{"text": set_text(s2, gold), "trap": None, "correct": True}] +
                [{"text": set_text(s2, Z), "trap": tt, "correct": False} for Z, tt in chosen], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# C5 : must X and Y be independent given Z   (SOLVER A: ball passing)
# ------------------------------------------------------------------------------------------------
def dsep_ballpass(parents, n, x, y, Z):
    Z = set(Z)
    ch = children_of(parents, n)
    anc = set(Z)
    for z in Z:
        anc |= ancestors(parents, z)
    visited, reach = set(), set()
    stack = [(x, "up")]
    while stack:
        v, d = stack.pop()
        if (v, d) in visited:
            continue
        visited.add((v, d))
        if v not in Z:
            reach.add(v)
        if d == "up" and v not in Z:
            for p in parents[v]:
                stack.append((p, "up"))
            for c in ch[v]:
                stack.append((c, "down"))
        elif d == "down":
            if v not in Z:
                for c in ch[v]:
                    stack.append((c, "down"))
            if v in anc:
                for p in parents[v]:
                    stack.append((p, "up"))
    return y not in reach


def c5_flaw_answers(spec):
    """{flaw: 'Yes'|'No'} what a mis-reading says to 'must X and Y be independent given Z'."""
    parents = {int(k): v for k, v in spec["parents"].items()}
    n, x, y, Z = spec["n"], spec["x"], spec["y"], set(spec["z"])
    out = {}
    out["ignore_conditioning"] = "Yes" if dsep_ballpass(parents, n, x, y, set()) else "No"
    # collider treated like a chain: independent iff every undirected path has a conditioned inner node
    paths = undirected_paths(parents, n, x, y)
    out["collider_as_chain"] = "Yes" if all(any(m in Z for m in p[1:-1]) for p in paths) else "No"
    out["direct_edge_only"] = "No" if (x in parents[y] or y in parents[x]) else "Yes"
    out["ancestor_only"] = "No" if (x in ancestors(parents, y) or y in ancestors(parents, x)) else "Yes"
    return out


def make_c5(rng, namer, bin_name, want_yes, balancer, scope):
    """Graph first, query second: the graph (and so the stem length) is drawn independently of the answer."""
    n = {"easy": 4, "mid": 5, "hard": 7}[bin_name]
    for _ in range(300):
        parents = random_dag(rng, n, rng.choice([0.3, 0.4, 0.5]))
        if len(edges_of(parents)) < 3:
            continue
        cands = []
        for x in range(n):
            for y in range(x + 1, n):
                others = [j for j in range(n) if j not in (x, y)]
                for r in range(0, min(3, len(others)) + 1):
                    for z in itertools.combinations(others, r):
                        if dsep_ballpass(parents, n, x, y, z) == want_yes:
                            cands.append((x, y, list(z)))
        if not cands:
            continue
        x, y, z = rng.choice(cands)
        if rng.random() < 0.5:
            x, y = y, x
        spec = {"version": 1, "form": "CA-C5", "n": n, "parents": {j: parents[j] for j in range(n)}, "x": x, "y": y, "z": z,
                "var_names": [namer.lower("variable", "v%d" % j) for j in range(n)]}
        ans = dsep_ballpass(parents, n, x, y, z)
        correct, wrong = ("Yes", "No") if ans else ("No", "Yes")
        fl = c5_flaw_answers(spec)
        ft = [f for f, a in fl.items() if a == wrong]
        trap = balancer.pick(scope, ft) if ft else "unmodelled"
        if trap == "unmodelled" and rng.random() < 0.95:
            continue
        return {"spec": spec, "answer": correct.lower(),
                "options": [{"text": correct, "trap": None, "correct": True}, {"text": wrong, "trap": trap, "correct": False}],
                "score": n + len(edges_of(parents)) - 3}
    return None


def solve_c5(spec):
    parents = {int(k): v for k, v in spec["parents"].items()}
    return "yes" if dsep_ballpass(parents, spec["n"], spec["x"], spec["y"], spec["z"]) else "no"


def perturb_c5(item, rng, balancer, scope):
    spec = item["spec"]
    n = spec["n"]
    parents = {int(k): v for k, v in spec["parents"].items()}
    edges = edges_of(parents)
    old = solve_c5(spec)
    cand = [("del", e) for e in edges] + [("add", (a, b)) for a in range(n) for b in range(a + 1, n) if (a, b) not in edges]
    others = [j for j in range(n) if j not in (spec["x"], spec["y"])]
    for j in others:
        cand.append(("zflip", j))
    rng.shuffle(cand)
    for kind, e in cand:
        s2 = dict(spec)
        if kind == "zflip":
            z2 = sorted(set(spec["z"]) ^ {e})
            s2["z"] = z2
        else:
            e2 = [x for x in edges if x != e] if kind == "del" else edges + [e]
            p2 = parents_from_edges(n, e2)
            s2["parents"] = {j: p2[j] for j in range(n)}
            if len(e2) < 3:
                continue
        new = solve_c5(s2)
        if new == old:
            continue
        correct, wrong = ("Yes", "No") if new == "yes" else ("No", "Yes")
        fl = c5_flaw_answers(s2)
        ft = [f for f, a in fl.items() if a == wrong]
        trap = balancer.pick(scope, ft) if ft else "unmodelled"
        return {"spec": s2, "answer": new, "options": [{"text": correct, "trap": None, "correct": True}, {"text": wrong, "trap": trap, "correct": False}],
                "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------------------------
def _nm(spec, j):
    return (spec["var_names"][j], "entity", "name")


def render(item, pool, widx, rng, domain, carrier="TXT-PROSE"):
    spec = item["spec"]
    form = spec["form"]
    doc = Doc()
    doc.sentence(pool.get("scene." + domain, rng.randrange(1 << 20)), {})
    idx = 0
    item_sep(doc, carrier, idx)
    idx += 1
    doc.sentence(pool.get("ca.intro", rng.randrange(1 << 20)), {"vars": (join_names(spec["var_names"]), "entity", "name")})
    parents = {int(k): v for k, v in spec["parents"].items()}
    names = spec["var_names"]
    if form in ("CA-C1", "CA-C2"):
        spec = norm(spec)
        parents = spec["parents"]
        for j in range(spec["n"]):
            if not parents[j]:
                if form == "CA-C1":
                    item_sep(doc, carrier, idx)
                    idx += 1
                    doc.sentence(pool.get("ca.root", rng.randrange(1 << 20)), {"v": _nm(spec, j), "val": (str(spec["roots"][j]), "number", "number")})
                continue
            item_sep(doc, carrier, idx)
            idx += 1
            key = "ca.fn.noise" if form == "CA-C2" else "ca.fn"
            doc.sentence(pool.get(key, rng.randrange(1 << 20)),
                         {"v": _nm(spec, j), "fn": (fn_text(spec["fn"][j], [names[p] for p in parents[j]], noise=form == "CA-C2"), "entity", "rule")})
        if form == "CA-C2":
            for j in range(spec["n"]):
                item_sep(doc, carrier, idx)
                idx += 1
                doc.sentence(pool.get("ca.obs", rng.randrange(1 << 20)), {"v": _nm(spec, j), "val": (str(spec["obs"][j]), "number", "number")})
        item_sep(doc, carrier, idx)
        idx += 1
        doc.sentence(pool.get("ca.model_closed", rng.randrange(1 << 20)), {})
        end_block(doc, carrier)
        doc.sentence(pool.get("q." + form, widx), {"target": _nm(spec, spec["target"]), "do_var": _nm(spec, spec["do"]["var"]),
                                                  "do_val": (str(spec["do"]["val"]), "number", "number")})
        return doc.text(), doc.spans
    # graph forms
    edges = edges_of(parents)
    rng.shuffle(edges)
    for a, b in edges:
        item_sep(doc, carrier, idx)
        idx += 1
        doc.sentence(pool.get("ca.edge", rng.randrange(1 << 20)), {"a": _nm(spec, a), "b": _nm(spec, b)})
    item_sep(doc, carrier, idx)
    idx += 1
    if form == "CA-C3":
        doc.sentence(pool.get("ca.def_roles", rng.randrange(1 << 20)), {})
    else:
        doc.sentence(pool.get("ca.indep", rng.randrange(1 << 20)), {})
    end_block(doc, carrier)
    if form == "CA-C3":
        doc.sentence(pool.get("q.CA-C3", widx), {"z": _nm(spec, spec["z"]), "t": _nm(spec, spec["t"]), "o": _nm(spec, spec["o"])})
    elif form == "CA-C4":
        doc.sentence(pool.get("q.CA-C4", widx), {"t": _nm(spec, spec["t"]), "o": _nm(spec, spec["o"])})
    else:
        zt = join_names([names[j] for j in spec["z"]]) if spec["z"] else "nothing"
        doc.sentence(pool.get("q.CA-C5", widx), {"x": _nm(spec, spec["x"]), "y": _nm(spec, spec["y"]), "zset": (zt, "entity", "name")})
    return doc.text(), doc.spans
