"""UCI Car Evaluation + Nursery: exact hierarchical (DEX) rule tables recovered from the complete truth tables.

Both UCI files enumerate the whole attribute space of a published DEX model (car.names / nursery.names: "instances
completely cover the attribute space"), so the class column IS the published model's output. The concept hierarchy is
the one printed in the .names files. For every intermediate concept we recover its minimal value partition by
function decomposition (Zupan et al. 1997, cited in car.names, showed this reconstructs the original model): two
bound-set assignments get the same intermediate value iff they give the same final class for every assignment of the
free attributes. The top concept is then a table over the intermediate values. `verify()` re-evaluates the recovered
hierarchy on every record and must reproduce 100% of the published classes (solver A = hierarchy, solver B = the
published record class).
"""
from __future__ import annotations

import itertools
from collections import OrderedDict

from p2_common import RAW

CAR = {
    "attrs": OrderedDict([
        ("buying", ["vhigh", "high", "med", "low"]),
        ("maint", ["vhigh", "high", "med", "low"]),
        ("doors", ["2", "3", "4", "5more"]),
        ("persons", ["2", "4", "more"]),
        ("lug_boot", ["small", "med", "big"]),
        ("safety", ["low", "med", "high"]),
    ]),
    "classes": ["unacc", "acc", "good", "vgood"],  # worst -> best
    # hierarchy from car.names: CAR(PRICE(buying, maint), TECH(COMFORT(doors, persons, lug_boot), safety))
    "concepts": OrderedDict([
        ("PRICE", ["buying", "maint"]),
        ("COMFORT", ["doors", "persons", "lug_boot"]),
        ("TECH", ["COMFORT", "safety"]),
    ]),
    "top": ["PRICE", "TECH"],
    "file": "car.data",
}

NURSERY = {
    "attrs": OrderedDict([
        ("parents", ["usual", "pretentious", "great_pret"]),
        ("has_nurs", ["proper", "less_proper", "improper", "critical", "very_crit"]),
        ("form", ["complete", "completed", "incomplete", "foster"]),
        ("children", ["1", "2", "3", "more"]),
        ("housing", ["convenient", "less_conv", "critical"]),
        ("finance", ["convenient", "inconv"]),
        ("social", ["nonprob", "slightly_prob", "problematic"]),
        ("health", ["recommended", "priority", "not_recom"]),
    ]),
    "classes": ["not_recom", "recommend", "very_recom", "priority", "spec_prior"],
    # hierarchy from nursery.names: NURSERY(EMPLOY(parents, has_nurs), STRUCT_FINAN(STRUCTURE(form, children),
    # housing, finance), SOC_HEALTH(social, health))
    "concepts": OrderedDict([
        ("EMPLOY", ["parents", "has_nurs"]),
        ("STRUCTURE", ["form", "children"]),
        ("STRUCT_FINAN", ["STRUCTURE", "housing", "finance"]),
        ("SOC_HEALTH", ["social", "health"]),
    ]),
    "top": ["EMPLOY", "STRUCT_FINAN", "SOC_HEALTH"],
    "file": "nursery.data",
}


def load(model):
    names = list(model["attrs"])
    recs = []
    with open(RAW / model["file"]) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            assert len(parts) == len(names) + 1, line
            rec = dict(zip(names, parts[:-1]))
            for a, v in rec.items():
                assert v in model["attrs"][a], (a, v)
            recs.append((i, rec, parts[-1]))
    return recs


def decompose(model, recs):
    """Return {concept: {bound tuple: value index}} with value index 0 = best (by mean class rank)."""
    attrs = model["attrs"]
    cls_rank = {c: i for i, c in enumerate(model["classes"])}
    f = {tuple(r[a] for a in attrs): c for _, r, c in recs}
    assert len(f) == len(recs) == len(list(itertools.product(*attrs.values()))), "not a complete truth table"
    # expansion of a concept to its leaf attributes
    leaves = {}

    def leaf(c):
        if c in attrs:
            return [c]
        if c not in leaves:
            leaves[c] = [x for ch in model["concepts"][c] for x in leaf(ch)]
        return leaves[c]

    tables = {}
    names = list(attrs)
    for concept, children in model["concepts"].items():
        bound = leaf(concept)
        free = [a for a in names if a not in bound]
        # vector of final classes over all free assignments, for each bound assignment
        vec = {}
        for bvals in itertools.product(*[attrs[a] for a in bound]):
            bd = dict(zip(bound, bvals))
            v = []
            for fvals in itertools.product(*[attrs[a] for a in free]):
                full = dict(bd)
                full.update(zip(free, fvals))
                v.append(f[tuple(full[a] for a in names)])
            vec[bvals] = tuple(v)
        groups = {}
        for b, v in vec.items():
            groups.setdefault(v, []).append(b)
        # order groups best -> worst by mean class rank (higher rank = better for both models' class lists)
        order = sorted(groups, key=lambda v: -sum(cls_rank[c] for c in v) / len(v))
        val_of_vec = {v: i for i, v in enumerate(order)}
        # the concept is a function of its CHILDREN's values: check that the children's values determine it
        child_tab = {}
        for bvals, v in vec.items():
            bd = dict(zip(bound, bvals))
            key = tuple(child_value(model, tables, ch, bd) for ch in children)
            val = val_of_vec[v]
            assert child_tab.setdefault(key, val) == val, f"{concept} not a function of its children"
        tables[concept] = {"children": children, "n_values": len(order), "table": child_tab}
    # top concept over the top children
    top = {}
    for _, r, c in recs:
        key = tuple(child_value(model, tables, ch, r) for ch in model["top"])
        assert top.setdefault(key, c) == c, "top concept not a function of its children"
    tables["__top__"] = {"children": model["top"], "table": top}
    return tables


def child_value(model, tables, child, rec):
    if child in model["attrs"]:
        return rec[child]
    t = tables[child]
    key = tuple(child_value(model, tables, ch, rec) for ch in t["children"])
    return t["table"][key]


def evaluate(model, tables, rec):
    """Solver A: evaluate the recovered hierarchy bottom-up."""
    return tables["__top__"]["table"][tuple(child_value(model, tables, ch, rec) for ch in model["top"])]


def verify(model, recs, tables):
    bad = sum(1 for _, r, c in recs if evaluate(model, tables, r) != c)
    return bad


if __name__ == "__main__":
    for name, m in (("car", CAR), ("nursery", NURSERY)):
        recs = load(m)
        t = decompose(m, recs)
        bad = verify(m, recs, t)
        print(name, len(recs), "records; mismatches", bad)
        for c, tt in t.items():
            if c == "__top__":
                print("  TOP over", tt["children"], "entries", len(tt["table"]))
            else:
                print(" ", c, "values", tt["n_values"], "entries", len(tt["table"]))
