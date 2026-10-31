"""S3 fact-graph sampler (G0 section 5, S3): ground facts about invented entities, 2-6 strict universals ("Every <noun>
that is A is B", "No <noun> that is A is B"; no bare generics), explicit negative facts, 1-2 hops, distractors, an inert
sentence on 30% of bases. At most 18 ground atoms after grounding. Open 60% / closed 40%.

M = {world, noun, plural, ents [ids], preds {name: {"kind": adj|has, "word"}}, univ [{q: every|no, a, b}],
     facts [{e, p, val: True|False, form: pos|not|aff|lacks}], inert str|None, negs {adj: affixed}}
Predicates are named "adj:<w>" or "has:<t>". Solver A: forward chaining (closed: least model; "No" universals are
constraints) / unit propagation with contrapositives (open).
"""
from __future__ import annotations

import copy


def subj(M, e):
    return f"{M['noun']} {e}"


def lit_text(M, e, p, val, form):
    s = subj(M, e)
    kind, w = p.split(":", 1)
    if kind == "adj":
        if val:
            return f"{cap(s)} is {w}."
        return f"{cap(s)} is {M['negs'][w]}." if form == "aff" else f"{cap(s)} is not {w}."
    if val:
        return f"{cap(s)} has a {w}."
    return f"{cap(s)} lacks a {w}." if form == "lacks" else f"{cap(s)} does not have a {w}."


def cap(s):
    return s[:1].upper() + s[1:]


def pred_vp(p, M):
    kind, w = p.split(":", 1)
    return f"is {w}" if kind == "adj" else f"has a {w}"


def univ_text(M, u):
    q = "Every" if u["q"] == "every" else "No"
    return f"{q} {M['noun']} that {pred_vp(u['a'], M)} {pred_vp(u['b'], M)}."


def ground(M):
    return [(e, p) for e in M["ents"] for p in M["preds"]]


def acyclic(M):
    edges = {}
    for u in M["univ"]:
        edges.setdefault(u["a"], set()).add(u["b"])
    seen, stack = set(), set()

    def visit(x):
        if x in stack:
            return False
        if x in seen:
            return True
        stack.add(x)
        ok = all(visit(y) for y in edges.get(x, ()))
        stack.discard(x)
        seen.add(x)
        return ok
    return all(visit(x) for x in list(edges))


def closed_model(M):
    val = {(e, p): False for e, p in ground(M)}
    for f in M["facts"]:
        if f["val"]:
            val[(f["e"], f["p"])] = True
    layer = {k: (0 if v else None) for k, v in val.items()}
    changed, rnd = True, 0
    while changed:
        changed = False
        rnd += 1
        for u in M["univ"]:
            if u["q"] != "every":
                continue
            for e in M["ents"]:
                if val[(e, u["a"])] and not val[(e, u["b"])]:
                    val[(e, u["b"])] = True
                    layer[(e, u["b"])] = rnd
                    changed = True
    for f in M["facts"]:
        if not f["val"] and val[(f["e"], f["p"])]:
            raise ValueError("a stated negative fact is derived positive")
    for u in M["univ"]:
        if u["q"] == "no":
            for e in M["ents"]:
                if val[(e, u["a"])] and val[(e, u["b"])]:
                    raise ValueError("'No' universal violated")
    return val, layer


def open_model(M):
    val = {(e, p): None for e, p in ground(M)}
    layer = {}
    for f in M["facts"]:
        k = (f["e"], f["p"])
        if val[k] is not None and val[k] != f["val"]:
            raise ValueError("contradictory facts")
        val[k] = f["val"]
        layer[k] = 0
    clauses = []   # (premise atom, premise value, conclusion atom, conclusion value)
    for u in M["univ"]:
        for e in M["ents"]:
            a, b = (e, u["a"]), (e, u["b"])
            if u["q"] == "every":
                clauses.append((a, True, b, True))
                clauses.append((b, False, a, False))      # contrapositive
            else:
                clauses.append((a, True, b, False))
                clauses.append((b, True, a, False))
    changed, rnd = True, 0
    while changed:
        changed = False
        rnd += 1
        for pa, pv, ca, cv in clauses:
            if val[pa] == pv:
                if val[ca] is None:
                    val[ca] = cv
                    layer[ca] = rnd
                    changed = True
                elif val[ca] != cv:
                    raise ValueError("inconsistent")
    return val, layer


def solve(M):
    if not acyclic(M):
        raise ValueError("cyclic universals")
    return closed_model(M) if M["world"] == "closed" else open_model(M)


def eval_lf(lf, M, val):
    op = lf[0]
    if op == "not":
        x = eval_lf(lf[1], M, val)
        return None if x is None else (not x)
    if op == "and":
        xs = [eval_lf(a, M, val) for a in lf[1:]]
        if any(x is False for x in xs):
            return False
        return True if all(x is True for x in xs) else None
    if op == "or":
        xs = [eval_lf(a, M, val) for a in lf[1:]]
        if any(x is True for x in xs):
            return True
        return False if all(x is False for x in xs) else None
    if op in ("adj", "has"):
        e = lf[1].rsplit(" ", 1)[1]
        return val.get((e, f"{op}:{lf[2]}"))
    if op == "grp":           # ["grp", Q, noun, pred, except_id|None]
        _, Q, noun, pred, exc = lf
        p = f"{pred[0]}:{pred[1]}"
        vs = [val.get((e, p)) for e in M["ents"] if e != exc]
        if Q == "every":
            if any(v is False for v in vs):
                return False
            return True if all(v is True for v in vs) else None
        if Q == "some":
            if any(v is True for v in vs):
                return True
            return False if all(v is False for v in vs) else None
    raise ValueError(op)


def solve_a(M, lfs):
    val, _ = solve(M)
    out = [eval_lf(lf, M, val) for lf in lfs]
    if any(o is None for o in out):
        raise ValueError("undetermined")
    return out


def sample(rng, card, world, depth, target_v, base_pred, n_ents=None):
    """Label-first: pick the base entity and predicate, build a proof of the target value of the given depth, then add
    distractor facts, universals and an inert sentence."""
    ent = card["ent"]
    ids = list(ent["ids"])
    rng.shuffle(ids)
    n_e = n_ents or rng.choice([3, 3, 4])
    preds = list(card["preds"])
    rng.shuffle(preds)
    preds = [p for p in preds if p != base_pred][:3] + [base_pred]
    rng.shuffle(preds)
    if len(preds) * n_e > 18:
        n_e = 18 // len(preds)
    M = {"world": world, "noun": ent["noun"], "plural": ent["plural"], "ents": ids[:n_e],
         "preds": {p: {} for p in preds}, "univ": [], "facts": [], "inert": None, "negs": dict(card["negs"])}
    E = M["ents"][0]
    others = [p for p in preds if p != base_pred]
    chain = rng.sample(others, min(len(others), depth))
    # proof: E has chain[0] (fact); chain[i] -> chain[i+1]; last -> base (every) or -> not base (no)
    hops = chain + [base_pred]
    M["facts"].append({"e": E, "p": chain[0], "val": True, "form": "pos"})
    for a, b in zip(hops[:-2], hops[1:-1]):
        M["univ"].append({"q": "every", "a": a, "b": b})
    last_a = hops[-2]
    if target_v:
        M["univ"].append({"q": "every", "a": last_a, "b": base_pred})
    else:
        if world == "open" or rng.random() < 0.5:
            M["univ"].append({"q": "no", "a": last_a, "b": base_pred})
        else:
            # closed: base not derivable; a universal into base from a predicate E does not have
            alt = [p for p in preds if p not in hops]
            if alt:
                M["univ"].append({"q": "every", "a": alt[0], "b": base_pred})
            else:
                M["univ"].append({"q": "no", "a": last_a, "b": base_pred})
    # distractors
    for _ in range(rng.choice([1, 2, 2, 3])):
        a, b = rng.sample(preds, 2)
        if any(u["a"] == a and u["b"] == b for u in M["univ"]):
            continue
        M["univ"].append({"q": rng.choice(["every", "every", "no"]), "a": a, "b": b})
    for e in M["ents"][1:]:
        for p in rng.sample(preds, rng.choice([1, 2])):
            v = rng.random() < 0.6
            M["facts"].append({"e": e, "p": p, "val": v, "form": "pos"})
    for f in M["facts"]:
        if not f["val"]:
            kind, w = f["p"].split(":", 1)
            r = rng.random()
            f["form"] = "aff" if kind == "adj" and M["negs"].get(w) and r < 0.35 else (
                "lacks" if kind == "has" and r < 0.5 else "not")
    if world == "closed":
        keep = [f for f in M["facts"] if f["val"] or rng.random() < 0.35]
        named = {f["e"] for f in keep}
        keep += [f for f in M["facts"] if f["e"] not in named and f not in keep][:1] if len(named) < len(
            M["ents"]) else []
        for e in M["ents"]:
            if e not in {f["e"] for f in keep}:
                keep += [f for f in M["facts"] if f["e"] == e][:1]
        M["facts"] = keep
    M["ents"] = [e for e in M["ents"] if any(f["e"] == e for f in M["facts"])]
    rng.shuffle(M["univ"])
    rng.shuffle(M["facts"])
    if rng.random() < 0.3 and card.get("inert"):
        M["inert"] = rng.choice(card["inert"])
    # text-side decoy (C16): two true positive adjective facts of one entity in one "not only ... but also" sentence
    if rng.random() < 0.4:
        by = {}
        for f in M["facts"]:
            if f["val"] and f["p"].startswith("adj:") and f["form"] == "pos":
                by.setdefault(f["e"], []).append(f)
        cands = [fs for fs in by.values() if len(fs) >= 2]
        if cands:
            fs = rng.choice(cands)[:2]
            for f in fs:
                f["form"] = "decoy"
            M["decoy_text"] = [fs[0]["e"], fs[0]["p"][4:], fs[1]["p"][4:]]
    return M, E


def depth_of(M, E, p):
    val, layer = solve(M)
    return layer.get((E, p))


def doc_ir(M, attack=None):
    items = [univ_text(M, u) for u in M["univ"]]
    facts = [lit_text(M, f["e"], f["p"], f["val"], f["form"]) for f in M["facts"] if f["form"] != "decoy"]
    if M.get("decoy_text"):
        e, a, b = M["decoy_text"]
        facts.append(f"{cap(subj(M, e))} is not only {a} but also {b}.")
    if M.get("inert"):
        facts.append(M["inert"])
    if attack:
        facts.append(attack)
    return {"title": f"{cap(M['plural'])} on record",
            "blocks": [{"type": "section", "heading": "General statements", "blocks": [{"type": "items",
                                                                                         "items": items}]},
                       {"type": "section", "heading": "Facts", "blocks": [{"type": "items", "items": facts}]}]}


def perturb(M, rng):
    """Contrast-pair change (S3): one ground fact switched between stated and stated-negative (closed: also removed)."""
    out = []
    for i, f in enumerate(M["facts"]):
        if f["form"] == "decoy":
            continue
        M2 = copy.deepcopy(M)
        g = M2["facts"][i]
        g["val"] = not g["val"]
        g["form"] = "pos" if g["val"] else "not"
        out.append((f"fact {f['e']} {f['p']} -> {g['val']}", M2))
        # repair r2 (G5 flag, SEM-02 / F5-R1-04): a removal may never leave a named entity of B without a mention in
        # B''s record (the record names every <entity type>; the questions are B's), so the entity's only stated
        # fact is never the one removed
        still_named = any(j != i and h["e"] == f["e"] and h["form"] != "decoy" for j, h in enumerate(M["facts"])) \
            or (M.get("decoy_text") and M["decoy_text"][0] == f["e"])
        if M["world"] == "closed" and still_named:
            M3 = copy.deepcopy(M)
            del M3["facts"][i]
            out.append((f"remove fact {f['e']} {f['p']}", M3))
    rng.shuffle(out)
    return out
