"""One canonicalizer (G0 F1 v7 section 4 "Canonical hash", F1R2-A20): structure hash of a row, names abstracted.

Covers: the canonical rule graph (kind, canonical items, outcome, tier, dates, exception target), the notices (type,
target, effective / notice dates, new text, S3 position), the card policy (world, precedence, tie rule and strictness
order, default / fallback / escalate / M roles, governing-date field), the facts (case values, unknown and not-recorded
sets, governing date; Q4: every listed case) and the query (question type, X, polarity). Left out: typed inert elements,
distractor dates (date fields no literal mentions, other than the governing date), the option set and the rendering.
Numbers are in step units, dates are day offsets from B. Every name is replaced by a positional id from one canonical
labelling: name-free labels -> labelled graph -> colour refinement -> individualization of the first non-singleton
class (lexicographically smallest serialization wins) -> sha256.
"""
from __future__ import annotations

import hashlib
from decimal import Decimal


def _tok(a, x, B):
    if a.type == "num":
        return f"n{(Decimal(x) / a.step).normalize():f}"
    if a.type == "date":
        return f"d{x - B}"
    if a.type == "bool":
        return "T" if x else "F"
    return None


def _canon_lit(lit, attrs):
    a = attrs[lit.attr]
    o, g = lit.op, tuple(lit.args)
    s = a.step if a.type == "num" else 1
    if a.type == "num":
        o, g = {"gt": ("ge", (g[0] + s,)), "lt": ("le", (g[0] - s,)), "within": ("le", g)}.get(o, (o, g))
    elif a.type == "date":
        o, g = {"before": ("le", (g[0] - 1,)), "onbefore": ("le", g), "after": ("ge", (g[0] + 1,)),
                "onafter": ("ge", g), "fromto": ("between", g)}[o]
    return o, g


class G:
    def __init__(self):
        self.lab = []
        self.adj = []
        self.radj = None

    def node(self, label):
        self.lab.append(label)
        self.adj.append([])
        return len(self.lab) - 1

    def edge(self, a, b, label):
        self.adj[a].append((label, b))


def build_graph(S, cases, q):
    P = S.policy
    B = P.B
    A = S.attrs
    g = G()
    referenced = set()
    all_rules = list(S.rules) + [n.rule for n in S.notices if n.rule is not None]
    for r in all_rules:
        for it in r.all_items():
            for m in it.mem:
                referenced.add(m.attr)
    keep = [k for k, a in A.items() if not (a.type == "date" and k != P.gov and k not in referenced)]
    an = {}
    cv = {}
    for k in keep:
        a = A[k]
        lab = f"attr|{a.type}|" + (f"{a.places}|{(a.step).normalize():f}|{_tok(a, a.lo, B)}|{_tok(a, a.hi, B)}"
                                   if a.type == "num" else f"{len(a.values)}" if a.type == "cat" else
                                   ("gov" if k == P.gov else ""))
        an[k] = g.node(lab)
        if a.type == "cat":
            for v in a.values:
                cv[(k, v)] = g.node("catval")
                g.edge(cv[(k, v)], an[k], "of")
        if a.type == "bool" and a.presup and a.presup in A:
            pass
    for k in keep:
        a = A[k]
        if a.type == "bool" and a.presup in an:
            g.edge(an[k], an[a.presup], "presup")
    # outcomes
    strict_rank = {o: i for i, o in enumerate(P.strict)}
    has_onlyif = any(r.kind == "onlyif" for r in all_rules)
    on = {}
    refd = {r.out for r in all_rules if r.out is not None} | {P.default}
    if P.tie == "esc" and P.prim != "ORDER":
        refd.add(P.escalate)
    if has_onlyif:
        refd.add(P.fallback)
    if P.world == "missing":
        refd.add(P.M)
    if P.tie == "strict":
        refd |= set(P.strict)
    if q.get("X") is not None:
        refd.add(q["X"])
    for o in sorted(refd, key=lambda x: (P.strict.index(x) if x in P.strict else -1, "")):
        if o is None:
            continue
        role = "other"
        if o == P.default:
            role = "default"
        elif P.tie == "esc" and P.prim != "ORDER" and o == P.escalate:
            role = "escalate"
        elif has_onlyif and o == P.fallback:
            role = "fallback"
        elif P.world == "missing" and o == P.M:
            role = "M"
        on[o] = g.node(f"out|{role}|{strict_rank.get(o, '-') if P.tie == 'strict' else '-'}")
    pol = g.node(f"policy|{P.world}|{P.prim}|{P.sec}|{P.tie if P.prim != 'ORDER' else '-'}")
    g.edge(pol, an[P.gov], "gov")
    for k in P.listed:
        if k in an:
            g.edge(pol, an[k], "listed")
    rank = {}
    if P.prim == "ORDER" and S.s3_rows is not None:
        rank = {rid: i for i, rid in enumerate(S.s3_rows)}

    def rule_node(r):
        lab = (f"rule|{r.kind}|{r.tier if r.tier is not None else '-'}|"
               f"{(r.date - B) if r.date is not None else '-'}|{(r.last - B) if r.last is not None else '-'}|"
               f"{rank.get(r.rid, '-') if P.prim == 'ORDER' else '-'}")
        rn = g.node(lab)
        for it in r.all_items():
            inode = g.node(f"item|{it.kind}|{it.k}")
            g.edge(rn, inode, "has")
            for m in it.mem:
                o, args = _canon_lit(m, A)
                a = A[m.attr]
                if a.type == "cat":
                    ln = g.node(f"lit|{o}")
                    for v in args:
                        g.edge(ln, cv[(m.attr, v)], "val")
                else:
                    ln = g.node(f"lit|{o}|" + ",".join(_tok(a, x, B) for x in args))
                g.edge(inode, ln, "mem")
                g.edge(ln, an[m.attr], "on")
        if r.out is not None and r.out in on:
            g.edge(rn, on[r.out], "out")
        return rn
    rn = {}
    for r in S.rules:
        rn[r.rid] = rule_node(r)
    for r in S.rules:
        if r.kind in ("pexc", "oexc") and r.target in rn:
            g.edge(rn[r.rid], rn[r.target], "exc_of")
    text_nodes = []
    for n in S.notices:
        nn = g.node(f"notice|{n.ntype}|{n.edate - B}|{n.ndate - B}|{n.pos[0] if n.pos else '-'}")
        if n.rule is not None:
            nr = rule_node(n.rule)
            g.edge(nn, nr, "text")
            if n.ntype == "insert":
                rn.setdefault(n.rule.rid, nr)
            text_nodes.append((n, nr))
    # second pass (order-free): exception links of notice texts, once every inserted rule has its node
    for n, nr in text_nodes:
        if n.rule.kind in ("pexc", "oexc") and n.rule.target in rn:
            g.edge(nr, rn[n.rule.target], "exc_of")
    # second pass for targets (rule ids known now)
    ni = [i for i, l in enumerate(g.lab) if l.startswith("notice|")]
    for idx, n in zip(ni, S.notices):
        if n.target is not None and n.target in rn:
            g.edge(idx, rn[n.target], "target")
        if n.pos and n.pos[0] == "after" and n.pos[1] in rn:
            g.edge(idx, rn[n.pos[1]], "anchor")
    # facts
    for c in cases:
        cn = g.node("case")
        for k in keep:
            a = A[k]
            if k in c.unknown:
                fn = g.node("fact|unknown")
            elif k in c.notrec:
                fn = g.node("fact|notrec")
            elif a.type == "cat":
                fn = g.node("fact|cat")
                g.edge(fn, cv[(k, c.vals[k])], "val")
            else:
                fn = g.node("fact|" + _tok(a, c.vals[k], B))
            g.edge(fn, an[k], "on")
            g.edge(cn, fn, "fact")
    qn = g.node(f"query|{q.get('qtype')}|{q.get('pol', '-')}")
    if q.get("X") is not None and q["X"] in on:
        g.edge(qn, on[q["X"]], "X")
    return g


def _radj(g):
    if getattr(g, "radj", None) is None:
        g.radj = [[] for _ in g.lab]
        for j, es in enumerate(g.adj):
            for l, t in es:
                g.radj[t].append((l, j))
    return g.radj


def _refine(g, colours):
    n = len(g.lab)
    radj = _radj(g)
    while True:
        sig = []
        for i in range(n):
            nb = sorted(f"{l}:{colours[j]}" for l, j in g.adj[i])
            rb = sorted(f"{l}<{colours[j]}" for l, j in radj[i])
            sig.append(f"{colours[i]}[{';'.join(nb)}][{';'.join(rb)}]")
        uniq = sorted(set(sig))
        idx = {s: k for k, s in enumerate(uniq)}
        new = [idx[s] for s in sig]
        if len(uniq) == len(set(colours)):
            return new
        colours = new


def _serialize(g, colours):
    order = sorted(range(len(g.lab)), key=lambda i: colours[i])
    pos = {i: k for k, i in enumerate(order)}
    parts = []
    for i in order:
        es = sorted(f"{l}>{pos[j]}" for l, j in g.adj[i])
        parts.append(f"{g.lab[i]}{{{','.join(es)}}}")
    return "|".join(parts)


class _Budget(Exception):
    pass


def _canon(g, colours, budget):
    colours = _refine(g, colours)
    classes = {}
    for i, c in enumerate(colours):
        classes.setdefault(c, []).append(i)
    multi = sorted(c for c, v in classes.items() if len(v) > 1)
    if not multi:
        return _serialize(g, colours)
    c = multi[0]
    best = None
    for i in classes[c]:
        budget[0] -= 1
        if budget[0] < 0:
            raise _Budget()
        nc = [2 * x + (1 if (x == c and j != i) else 0) for j, x in enumerate(colours)]
        s = _canon(g, nc, budget)
        if best is None or s < best:
            best = s
    return best


def _wl_certificate(g, colours):
    """Isomorphism-invariant certificate from the stable colour refinement (used only when individualization
    exceeds its budget; the search tree, hence the fallback, is the same for isomorphic graphs)."""
    colours = _refine(g, colours)
    parts = sorted(f"{g.lab[i]}#{colours[i]}{{{','.join(sorted(f'{l}>{colours[j]}' for l, j in g.adj[i]))}}}"
                   for i in range(len(g.lab)))
    return "WL|" + "|".join(parts)


def structure_hash(S, cases, q) -> str:
    g = build_graph(S, cases, q)
    lab_sorted = sorted(set(g.lab))
    li = {l: k for k, l in enumerate(lab_sorted)}
    colours = [li[l] for l in g.lab]
    try:
        ser = _canon(g, colours, [3000])
    except _Budget:
        ser = _wl_certificate(g, colours)
    return hashlib.sha256(ser.encode()).hexdigest()
