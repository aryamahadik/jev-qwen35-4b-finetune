"""Dependency DAG builder and level algorithms (T54 S6 gold; T56 plan DAG).

Edge (u, v) means "v consumes the output of u" (u must finish before v can be issued).
Solver A uses Kahn's levels. `longest_path_levels` is a DIFFERENT algorithm (memoised depth) kept here only as a
CPU cross-check for tests; solver B writes its own.
"""
from collections import defaultdict, deque


class DagError(ValueError):
    pass


def _index(nodes, edges):
    nodes = list(nodes)
    ns = set(nodes)
    preds, succs = defaultdict(set), defaultdict(set)
    for u, v in edges:
        if u not in ns or v not in ns:
            raise DagError("edge %r -> %r names an unknown node" % (u, v))
        if u == v:
            raise DagError("self edge on %r" % u)
        preds[v].add(u)
        succs[u].add(v)
    return nodes, preds, succs


def kahn_levels(nodes, edges):
    """Topological levels: level 0 = nodes with no in-edge, level k+1 = nodes whose predecessors are all in levels <= k.
    Raises DagError on a cycle."""
    nodes, preds, succs = _index(nodes, edges)
    indeg = {n: len(preds[n]) for n in nodes}
    cur = deque(sorted(n for n in nodes if indeg[n] == 0))
    out, seen = [], 0
    while cur:
        out.append(sorted(cur))
        nxt = []
        for n in cur:
            seen += 1
            for s in sorted(succs[n]):
                indeg[s] -= 1
                if indeg[s] == 0:
                    nxt.append(s)
        cur = deque(sorted(nxt))
    if seen != len(nodes):
        raise DagError("cycle")
    return out


def longest_path_levels(nodes, edges):
    nodes, preds, _ = _index(nodes, edges)
    memo, stack = {}, set()

    def depth(n):
        if n in memo:
            return memo[n]
        if n in stack:
            raise DagError("cycle")
        stack.add(n)
        d = 0 if not preds[n] else 1 + max(depth(p) for p in preds[n])
        stack.discard(n)
        memo[n] = d
        return d

    return {n: depth(n) for n in nodes}


def remaining_dag(nodes, edges, done):
    """Sub-DAG of the nodes not yet completed (edges from completed nodes are satisfied and dropped)."""
    done = set(done)
    rest = [n for n in nodes if n not in done]
    rs = set(rest)
    return rest, [(u, v) for (u, v) in edges if u in rs and v in rs]


def ready_set(nodes, edges, done):
    """Calls that can be issued now: remaining nodes whose every dependency is already done. Kahn level 0 of the
    remaining DAG. (Solver A for S6.)"""
    rest, redges = remaining_dag(nodes, edges, done)
    if not rest:
        return []
    return kahn_levels(rest, redges)[0]


def canonical_set(node_to_group, ids):
    """Canonicalise a call set: substitutable tools collapse to their equivalence-group id (multiset, sorted)."""
    return tuple(sorted(node_to_group[i] for i in ids))


def build_layered_dag(rng, n_done, n_ready, n_blocked, extra_edge_prob=0.3):
    """Build (nodes, edges, done) with an exact ready-set shape:
       n_done completed nodes (a small chain/fork), n_ready remaining nodes whose deps are subsets of done, and
       n_blocked remaining nodes that each consume >= 1 ready node (or another blocked node). Node ids are n0..nK
       in a shuffled labelling so the id order carries no level information."""
    total = n_done + n_ready + n_blocked
    if n_ready < 1:
        raise DagError("need at least one ready node")
    ids = ["n%d" % i for i in range(total)]
    rng.shuffle(ids)
    done = ids[:n_done]
    ready = ids[n_done:n_done + n_ready]
    blocked = ids[n_done + n_ready:]
    edges = set()
    for i, d in enumerate(done):                       # completed nodes: a light internal structure
        if i > 0 and rng.random() < 0.5:
            edges.add((rng.choice(done[:i]), d))
    for r in ready:                                    # ready nodes may consume completed outputs only
        for d in done:
            if rng.random() < extra_edge_prob:
                edges.add((d, r))
    for i, b in enumerate(blocked):                    # blocked nodes consume at least one remaining node
        pool = ready + blocked[:i]
        edges.add((rng.choice(ready if i == 0 else pool), b))
        for p in pool:
            if rng.random() < extra_edge_prob / 2:
                edges.add((p, b))
        for d in done:
            if rng.random() < extra_edge_prob / 2:
                edges.add((d, b))
    nodes = sorted(ids)
    return nodes, sorted(edges), sorted(done)
