"""Rules-kind structures (S1 forward rule base, S2 label-first witness pairs, S5 interview): policy draws, case
records, visible gaps and the per-form targets. Labels come from solver A only (solver B re-solves the parse, G2/G3).

Structure R (rules kind):
  D, world ('open'|'closed'|'local'), local (cid closed on a local card), marker, ev_tag {'tag','counts'} | None,
  attrs {aid: {name, kind 'num'|'cat', unit, lo, hi, vals}}, events {eid: {name}}, classes {cid: {name, plural}},
  subclass [[b, a]], notices {nid: {name, date}}, notice_order, rules [{rid, notice, conds, unless, out, exc}],
  table None | {rid, notice, A, B, rows, cols, cells {'a|b': oid}}, onlyif [{out, cond}], default, outcomes {oid: name},
  cases [labels], facts {case: {num, cat, ev, cls}}, lists {cid: [(label, 'v'|'m'|'tag')]}, case_noun.
"""
from __future__ import annotations

import itertools
import random

from . import solver_a as A
from .common import day

NOTICE_NAMES = ["the base policy", "Notice A", "Notice B", "Notice C"]


# ---------------------------------------------------------------- helpers

def ref_vars(R: dict) -> dict:
    """Every variable a rule, only-if, precedence test or table names -> its role ('cond', 'unless', 'onlyif',
    'class', 'table')."""
    roles = {}

    def add(at, role):
        k = A._atom_var(at)
        if k not in roles or roles[k] == "cond":
            roles[k] = role if role != "cond" or k not in roles else roles[k]
    for r in A.all_rules(R):
        for at in r["conds"]:
            add(at, "cond")
        if r.get("unless"):
            add(r["unless"], "unless")
    for o in R.get("onlyif", []):
        add(o["cond"], "onlyif")
    return roles


def visible_gaps(R: dict, case: str) -> list:
    """[(var, kind)] for one case: markers, non-counting tags, absences of named facts that do not close, unknown
    notice dates. Kind: gap:evidence | gap:order | gap:unless | gap:onlyif | gap:value."""
    roles = ref_vars(R)
    F = R["facts"][case]
    tag = R.get("ev_tag") or {}
    counts = bool(tag.get("counts"))
    out = []
    fixed_by_sub = set()
    for b, a in R.get("subclass", []):
        fb = F["cls"].get(b)
        if fb and "v" in fb and not fb.get("m") and (not fb.get("tag") or counts):
            fixed_by_sub.add(("cls", a))

    def kind_of(k, f):
        if f is not None and f.get("tag") and not counts:
            return "gap:evidence"
        role = roles.get(k)
        if role == "unless":
            return "gap:unless"
        if role == "onlyif":
            return "gap:onlyif"
        return "gap:value"
    for aid, a in R["attrs"].items():
        k = (a["kind"], aid)
        f = F["num" if a["kind"] == "num" else "cat"].get(aid)
        shown_unknown = f is not None and (f.get("m") or (f.get("tag") and not counts))
        absent = f is None and k in roles
        if shown_unknown or absent:
            out.append((k, kind_of(k, f)))
    for eid in R["events"]:
        k = ("ev", eid)
        f = F["ev"].get(eid)
        if f is not None and "plan" in f:
            if R["world"] != "closed":
                out.append((k, "gap:plan"))
            continue
        shown_unknown = f is not None and (f.get("m") or (f.get("tag") and not counts))
        absent = f is None and k in roles and R["world"] != "closed"
        if shown_unknown or absent:
            out.append((k, kind_of(k, f)))
    for cid in R["classes"]:
        k = ("cls", cid)
        if k in fixed_by_sub:
            continue
        f = F["cls"].get(cid)
        shown_unknown = f is not None and (f.get("m") or (f.get("tag") and not counts))
        closes = R["world"] == "closed" or (R["world"] == "local" and R.get("local") == cid)
        absent = f is None and k in roles and not closes
        if shown_unknown or absent:
            out.append((k, kind_of(k, f)))
    for nid, n in R["notices"].items():
        if n["date"]["k"] != "exact":
            out.append((("nd", nid), "gap:order"))
    return out


def gap_position(R: dict, case: str, var) -> str:
    """Position of a gap (the list, table or section that holds or would hold the fact)."""
    k = var[0]
    return {"num": "fields", "cat": "fields", "ev": "events", "cls": "lists", "nd": "notices"}[k]


def depth_of(R: dict, case: str, claim=None) -> int:
    """Hops: one per rule application; +1 when some completion resolves a conflict among fired rules."""
    rules = A.all_rules(R)
    V = A.variables(R, case)
    regs = {k: A.regions(R, k, s, V["fixed"]) for k, s in V["var"].items()}
    names = list(regs)
    conflict = False
    for combo in itertools.islice(itertools.product(*[regs[k] for k in names]), 2000):
        asg = {**V["fixed"], **dict(zip(names, combo))}
        if not A._consistent(R, asg):
            continue
        st = A._statuses(R, rules, asg)
        rem = [r for r, s in zip(rules, st) if s is True]
        if len({r["out"] for r in rem}) > 1:
            conflict = True
            break
    return 1 + (1 if conflict else 0)


# ---------------------------------------------------------------- policy draw

class Profile(dict):
    """Card-level feature profile: fixed per card variant, so switch sentences never predict a label."""


def make_profile(rng: random.Random, pack: dict, schema: str, sampler: str, table: bool,
                 mode: str = "rich") -> Profile:
    """mode 'rich' (yes/no cards: the card is printed once), 'lean' (choice cards: instructions are counted twice
    against the 1,900-token cap, A16.1 (g)) or 'table' (lean outcome-table cards for large catalogs)."""
    case = rng.choice(pack["cases"])
    if mode == "rich":
        nq, nc, ne, na = 2, 1, 2, 2
        nfeat = rng.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
        nn = rng.choice([2, 2, 3]) if sampler != "S2" else rng.choice([1, 2, 3])
        tagp = 0.45
    elif mode == "lean":
        nq, nc, ne, na = rng.choice([1, 2]), 1, 1, 1
        if sampler == "S2":               # repair r1: witness, shared condition, two case-split traps + distractors
            nq, nc = 1, 2
        nfeat = rng.choice([0, 1, 1])
        nn = 2
        tagp = 0.3
    else:
        nq, nc, ne, na = 1, 1, 0, 0
        nfeat = 0
        nn = 2
        tagp = 0.0
    qty = [dict(q) for q in rng.sample(pack["qty"], min(len(pack["qty"]), nq))]
    for q in qty:                          # repair r1: card-level domains (a definition example cites them)
        if q["hi"] - q["lo"] > 400:
            q["lo"] = rng.randint(q["lo"], q["hi"] - 200)
            q["hi"] = q["lo"] + rng.randint(60, 200)
        q["lo"] = max(q["lo"], 2)
    cats = rng.sample(pack["cat"], min(len(pack["cat"]), nc))
    evs = rng.sample(pack["events"], min(len(pack["events"]), ne))
    adjs = rng.sample(pack["adjs"], min(len(pack["adjs"]), na))
    feats = ["unless", "onlyif", "exc", "sub"] if mode == "rich" else ["unless", "onlyif"]
    rng.shuffle(feats)
    on = set(feats[:nfeat])
    if "sub" in on and len(adjs) < 2:
        adjs = rng.sample(pack["adjs"], min(len(pack["adjs"]), 2))
    P = Profile(
        case_noun=case["noun"], case_plural=case["plural"], prefix=case["prefix"],
        qty=qty, cats=cats, evs=evs, adjs=adjs, mode=mode,
        world=rng.choice(["open", "closed", "local"]) if adjs else rng.choice(["open", "closed"]),
        marker=rng.choice(["not recorded", "unknown"]),
        ev_tag=({"tag": rng.choice(["unverified", "self-reported"]), "counts": rng.random() < 0.25}
                if rng.random() < tagp else None),
        unless="unless" in on and bool(evs or adjs), onlyif="onlyif" in on, exc="exc" in on,
        sub="sub" in on and len(adjs) >= 2,
        n_notices=nn,
        cmp=rng.choice([">=", ">"]) if rng.random() < 0.5 else rng.choice(["<=", "<"]),
        cmpw=None, table=table, schema=schema,
        year=rng.randint(2044, 2058), date_style=rng.choice(["iso", "iso", "name"]),
    )
    P["cmp_family"] = "incl" if P["cmp"] in (">=", "<=") else "excl"
    return P


def _ids(rng, prefix, n, used=()):
    out = []
    while len(out) < n:
        x = f"{prefix}-{rng.randint(1000, 9999)}"
        if x not in out and x not in used:
            out.append(x)
    return out


def draw_policy(rng: random.Random, P: Profile, pack: dict, n_rules: int, n_out_min: int, table_shape=None) -> dict:
    """A policy over the card's attributes: notices, rules (+ unless / only-if / exception / subclass per the
    profile), default, and an outcome table when table_shape = (rows, cols)."""
    D = day(P["year"], rng.randint(3, 12), rng.randint(1, 28))
    attrs, attr_order = {}, []
    for i, q in enumerate(P["qty"]):
        aid = f"q{i}"
        lo, hi = q["lo"], q["hi"]
        attrs[aid] = {"name": q["name"], "kind": "num", "unit": q["unit"], "lo": max(lo, 2), "hi": hi}
        attr_order.append(aid)
    for i, c in enumerate(P["cats"]):
        aid = f"c{i}"
        attrs[aid] = {"name": c["name"], "kind": "cat", "vals": list(c["values"])[:6]}
        attr_order.append(aid)
    events = {f"e{i}": {"name": e} for i, e in enumerate(P["evs"])}
    classes = {f"k{i}": {"name": f"{adj} {P['case_noun']}", "plural": f"{adj} {P['case_plural']}"}
               for i, adj in enumerate(P["adjs"])}
    # outcome table attributes (S1 large catalogs): sites x a category
    T = None
    if table_shape:
        nr, nc = table_shape
        pl = list(pack["places"])
        if P.get("pure_table"):     # repair r1 v3c (length): the shorter place names (label-free)
            pl = sorted(pl, key=len)[:nr + 3]
        sites = rng.sample(pl, min(nr, len(pl)))
        nr = len(sites)
        attrs["cT"] = {"name": "site", "kind": "cat", "vals": sites}
        attr_order.append("cT")
        tb = max((a for a in attrs if attrs[a]["kind"] == "cat" and a != "cT"),
                 key=lambda a: len(attrs[a]["vals"]))
        if len(attrs[tb]["vals"]) < 2:
            raise ValueError("table column attribute too short")
        cols = attrs[tb]["vals"][:nc]
        T = {"rid": "T", "A": "cT", "B": tb, "rows": sites, "cols": cols, "cells": {}}
    n_not = P["n_notices"]
    base = D - rng.randint(200, 900)
    ndays = sorted(rng.sample(range(base, D - 5), n_not))
    notices = {f"n{i}": {"name": NOTICE_NAMES[i], "date": {"k": "exact", "d": d}} for i, d in enumerate(ndays)}
    pool = list(pack["outcomes"])
    rng.shuffle(pool)
    need = n_out_min
    if T:
        cells = len(T["rows"]) * len(T["cols"])
        comp = [f"{o} at {s}" for o in pack["outcomes"] for s in pack["places"]]
        rng.shuffle(comp)
        if P.get("pure_table"):     # repair r1 v3c (length): pure table cards take the shorter composite names
            comp.sort(key=len)      # (stable sort after the shuffle; names never depend on a label)
            comp = comp[:max(2 * (cells + 3), 12)]
            rng.shuffle(comp)
        pool = pool + [c for c in comp if c not in pool]
        need = max(need, cells + 3)
    outs = pool[:max(need, n_rules + 1)]
    if len(outs) < n_rules + 1:
        raise ValueError("outcome pool too small")
    oids = [f"o{i}" for i in range(len(outs))]
    outcomes = dict(zip(oids, outs))
    default = oids[0]
    free = oids[1:]
    rng.shuffle(free)
    R = {"kind": "rules", "D": D, "world": P["world"], "local": None, "marker": P["marker"],
         "ev_tag": P["ev_tag"], "attrs": attrs, "attr_order": attr_order, "events": events,
         "event_order": list(events), "classes": classes, "class_order": list(classes), "subclass": [],
         "notices": notices, "notice_order": list(notices), "rules": [], "table": None, "onlyif": [],
         "default": default, "outcomes": outcomes, "case_noun": P["case_noun"]}
    if T:
        k = 0
        for a in T["rows"]:
            for b in T["cols"]:
                T["cells"][f"{a}|{b}"] = free[k]
                k += 1
        R["table"] = T
        free = free[k:]
    qa = [a for a in attrs if attrs[a]["kind"] == "num"]
    ca = [a for a in attrs if attrs[a]["kind"] == "cat" and a != "cT"]
    ev = list(events)
    cl = list(classes)
    used_unless, used_oi = set(), set()

    def num_atom(aid=None):
        aid = aid or rng.choice(qa)
        a = attrs[aid]
        n = rng.randint(a["lo"] + 2, a["hi"] - 2)
        ops = [">=", "<="] if P["cmp_family"] == "incl" else [">", "<"]
        return {"t": "num", "a": aid, "op": rng.choice(ops), "n": n}

    def fix_op(at):
        return at

    def any_atom(exclude=(), no_cls=False):
        kinds = (["num"] * 3 if qa else []) + (["cat"] * 2 if ca else []) + (["ev"] * 2 if ev else []) + \
            (["cls"] if cl and not P["sub"] and not no_cls else [])
        if not kinds:
            raise ValueError("no attribute to build a condition from")
        for _ in range(40):
            k = rng.choice(kinds)
            if k == "num":
                at = num_atom()
            elif k == "cat":
                c = rng.choice(ca)
                at = {"t": "cat", "a": c, "v": rng.choice(attrs[c]["vals"])}
            elif k == "ev":
                at = {"t": "ev", "e": rng.choice(ev), "neg": rng.random() < 0.15}
            else:
                at = {"t": "cls", "c": rng.choice(cl)}
            if A._atom_var(at) not in exclude:
                return at
        raise ValueError("no fresh condition")

    rid = 0
    nrules_plain = n_rules - (1 if P["exc"] else 0)
    nrules_plain = max(nrules_plain, 0 if T else 2)   # repair r1: a table card may hold the table alone (length)
    if P["sub"]:
        b, a = cl[0], cl[1]
        R["subclass"].append([b, a])
    rot = rng.randrange(len(notices))
    if T:
        T["notice"] = list(notices)[rot % len(notices)]
        rot += 1
    for i in range(nrules_plain):
        rid += 1
        out = free[i % len(free)]
        nc = rng.choice([1, 2, 2])
        conds, seen = [], set()
        if P["sub"] and i < 2:
            conds.append({"t": "cls", "c": cl[i]})
            seen.add(("cls", cl[i]))
        while len(conds) < nc:
            at = any_atom(seen | used_unless | used_oi, no_cls=any(c["t"] == "cls" for c in conds))
            seen.add(A._atom_var(at))
            conds.append(at)
        nl = list(notices)
        r = {"rid": f"r{rid}", "notice": nl[(i + rot) % len(nl)], "conds": conds, "unless": None, "out": out,
             "exc": None}
        R["rules"].append(r)
    if P["unless"]:
        r = rng.choice(R["rules"])
        cand = [("ev", e) for e in ev] + [("cls", c) for c in cl if not P["sub"]]
        cand = [c for c in cand if c not in {A._atom_var(x) for rr in R["rules"] for x in rr["conds"]}]
        if cand:
            k = rng.choice(cand)
            r["unless"] = {"t": "ev", "e": k[1], "neg": False} if k[0] == "ev" else {"t": "cls", "c": k[1]}
            used_unless.add(k)
    if P["onlyif"]:
        outs_given = sorted({r["out"] for r in R["rules"]})
        o = rng.choice(outs_given)
        used = {A._atom_var(x) for rr in R["rules"] for x in rr["conds"] + ([rr["unless"]] if rr["unless"] else [])}
        cand = [("num", a) for a in qa] + [("cat", c) for c in ca]
        cand = [c for c in cand if c not in used]
        if cand:
            k = rng.choice(cand)
            if k[0] == "num":
                cond = fix_op(num_atom(k[1]))
            else:
                cond = {"t": "cat", "a": k[1], "v": rng.choice(attrs[k[1]]["vals"])}
            R["onlyif"].append({"out": o, "cond": cond})
    if P["exc"]:
        tgt = rng.choice(R["rules"])
        used = {A._atom_var(x) for x in tgt["conds"]}
        extra = any_atom(used | used_unless | used_oi, no_cls=True)
        rid += 1
        out = next((o for o in free if o != tgt["out"]), None)
        R["rules"].append({"rid": f"r{rid}", "notice": rng.choice(list(notices)),
                           "conds": [dict(x) for x in tgt["conds"]] + [extra],
                           "unless": dict(tgt["unless"]) if tgt["unless"] else None, "out": out, "exc": tgt["rid"]})
    return R


# ---------------------------------------------------------------- the case record

def full_case(rng: random.Random, R: dict, case: str) -> dict:
    """Every attribute, event and class of the case gets a value (the settled base)."""
    asg = {}
    for aid, a in R["attrs"].items():
        if a["kind"] == "num":
            cuts = A._cuts_num(R, aid)
            pts = [a["lo"], a["hi"]] + [c for c in cuts] + [c - 1 for c in cuts]
            pts = [p for p in pts if a["lo"] <= p <= a["hi"]]
            asg[("num", aid)] = rng.choice(pts) if rng.random() < 0.35 else rng.randint(a["lo"], a["hi"])
        else:
            asg[("cat", aid)] = rng.choice(a["vals"])
    for eid in R["events"]:
        asg[("ev", eid)] = rng.random() < 0.55
    for cid in R["classes"]:
        asg[("cls", cid)] = rng.random() < 0.5
    for b, a in R.get("subclass", []):
        if asg[("cls", b)]:
            asg[("cls", a)] = True
    return asg


def realise(rng: random.Random, R: dict, case: str, asg: dict, hidden: dict, distractors: list) -> dict:
    """Facts of the case from a full assignment and the hidden set {var: 'marker'|'absent'|'tag'}.
    Returns R with facts and lists filled. Events that happened get a date on or before D."""
    F = {"num": {}, "cat": {}, "ev": {}, "cls": {}, "inert": []}
    world, loc = R["world"], R.get("local")
    for aid, a in R["attrs"].items():
        k = (a["kind"], aid)
        h = hidden.get(k)
        slot = F["num" if a["kind"] == "num" else "cat"]
        if h == "absent":
            continue
        if h == "marker":
            slot[aid] = {"m": True}
        elif h == "tag":
            slot[aid] = {"v": asg[k], "tag": True}
        else:
            slot[aid] = {"v": asg[k]}
    roles = ref_vars(R)
    shown_cls = {k[1] for k in roles if k[0] == "cls"} | {c for bc in R.get("subclass", []) for c in bc} | \
        ({R["local"]} if R.get("local") else set())
    for eid in R["events"]:
        k = ("ev", eid)
        if k not in roles:
            continue
        h = hidden.get(k)
        d = R["D"] - rng.randint(3, 160)
        if h == "absent":
            continue
        if h == "plan":
            F["ev"][eid] = {"plan": R["D"] - rng.randint(1, 40) if world == "closed" else R["D"] + rng.randint(1, 40)}
            continue
        if h == "marker":
            F["ev"][eid] = {"m": True}
        elif h == "tag":
            if not asg[k]:
                raise ValueError("a tagged event must be listed as having happened")
            F["ev"][eid] = {"v": True, "date": d, "tag": True}
        elif asg[k]:
            F["ev"][eid] = {"v": True, "date": d}
        else:
            if world != "closed":
                raise ValueError("a false event cannot be shown on this card")
            if R.get("plans") and rng.random() < 0.3:
                F["ev"][eid] = {"plan": R["D"] - rng.randint(1, 40)}   # a plan on or before D: did not happen
    lists = {}
    for cid in R["classes"]:
        k = ("cls", cid)
        if cid not in shown_cls:
            continue
        h = hidden.get(k)
        ents = []
        if h == "marker":
            F["cls"][cid] = {"m": True}
            ents.append((case, "m"))
        elif h == "tag":
            if not asg[k]:
                raise ValueError("a tagged membership must be listed")
            F["cls"][cid] = {"v": True, "tag": True}
            ents.append((case, "tag"))
        elif h == "absent":
            pass
        elif asg[k]:
            F["cls"][cid] = {"v": True}
            ents.append((case, "v"))
        else:
            closes = world == "closed" or (world == "local" and loc == cid)
            if not closes:
                raise ValueError("a false membership cannot be shown on this card")
        others = rng.sample(distractors, rng.randint(1, 2))
        ents += [(o, "v") for o in others]
        rng.shuffle(ents)
        lists[cid] = ents
    R = dict(R)
    R["facts"] = {case: F}
    R["lists"] = lists
    R["cases"] = [case]
    return R
