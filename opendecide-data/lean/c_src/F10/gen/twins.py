"""Label-flip twins (defswap MR4, boundary MR10, exception toggle MR12; R2-13 emission rule) and relation units
(negation complement / equiv, attack inv, name-invariance equiv). Twin gold always comes from solver A."""
from __future__ import annotations

import copy

import model as M
from cardgen import draw_ranges
from solver_b import CardB


def row_answer(card, row, defs=None):
    """Solver A gold of a row spec on the (possibly swapped) definitions."""
    defs = defs or card["defs"]
    mc = M.Card(defs, card["order"])
    ordered = card["ctype"] in ("first", "dlist")
    if row["form"] == "inv":
        hits = [i for i, c in enumerate(row["records"]) if mc.meets(row["ask"], c)]
        return hits[0] if len(hits) == 1 else None
    case, om = row["case"], row.get("omitted", [])
    leg = card["legend"]
    if row["form"] == "yn":
        cc = {k: v for k, v in case.items() if k not in om}
        vals = M.possible_meets(mc, leg, cc, om, row["ask"], ordered, row["wkind"])
        if len(vals) != 1:
            return None
        return 1 if vals.pop() else 0
    if row["form"] == "choice":
        cc = {k: v for k, v in case.items() if k not in om}
        try:
            P = M.possible_answers(mc, leg, cc, om, ordered)
        except ValueError:
            return None
        shown = [o for o in row["options"] if o not in ("none", "cbd")]
        if len(P) == 1:
            p = next(iter(P))
            if p == "none":
                return "none" if "none" in row["options"] else None
            return p if p in shown else None
        if "cbd" in row["options"] and any(t in shown for t in P if t != "none"):
            return "cbd"
        return None
    if row["form"] == "inv":
        hits = [i for i, c in enumerate(row["records"]) if mc.meets(row["ask"], c)]
        return hits[0] if len(hits) == 1 else None
    raise ValueError(row["form"])


def target_of(row):
    if row["form"] == "yn" or row["form"] == "inv":
        return row["ask"]
    return row["gold"] if row["gold"] not in ("none", "cbd") else None


def swap_eligible(card, X, Y):
    defs = card["defs"]
    if X == Y or defs[X]["helper"] or defs[Y]["helper"]:
        return False
    for did, d in defs.items():
        refs = {r["to"] for r in M.walk_refs(d)}
        if did not in (X, Y) and (X in refs or Y in refs):
            return False
        if did in (X, Y) and ({X, Y} & refs):
            return False
    if card["sampler"] == "S4" and defs[X].get("section") != defs[Y].get("section"):
        return False
    return True


def swapped_defs(card, X, Y):
    defs = copy.deepcopy(card["defs"])
    dx, dy = defs[X], defs[Y]
    nx = dict(dy, id=X, section=dx.get("section"))
    ny = dict(dx, id=Y, section=dy.get("section"))
    defs[X], defs[Y] = nx, ny
    return defs


def twin_defswap(card, row, r):
    X = target_of(row)
    if X is None:
        return None
    gold0 = row_answer(card, row)
    cands = [Y for Y in card["order"] if swap_eligible(card, X, Y)]
    if row["form"] == "choice":
        cands = [Y for Y in cands if Y in row["options"]]
    r.shuffle(cands)
    for Y in cands:
        defs = swapped_defs(card, X, Y)
        g = row_answer(card, row, defs)
        if g is None or g == gold0:
            continue
        cb = CardB(card["legend"], defs, card["order"], card["ctype"])
        if cb.proofs(draw_ranges(card["legend"]), need_uncovered=card["ctype"] in ("amo", "first", "dlist")):
            continue
        tw = copy.deepcopy(row)
        tw.update({"swap": [X, Y], "gold": g, "twin_kind": "defswap"})
        if row["form"] == "inv":
            tw["gold_idx"] = g      # the inverted gold is the record index (emit reads gold_idx)
        return tw
    return None


def twin_boundary(card, row, r, cs):
    s = row.get("threshold")
    if s is None or row["form"] == "inv":
        return None
    gold0 = row_answer(card, row)
    deltas = [-1, 1]
    r.shuffle(deltas)
    for dlt in deltas:
        tw = copy.deepcopy(row)
        if isinstance(s, tuple):
            _, x, e = s
            if x in row.get("omitted", []) or e in row.get("omitted", []):
                continue
            tw["case"][x] = row["case"][x] + dlt
        else:
            if s in row.get("omitted", []):
                continue
            v = row["case"][s] + dlt
            if card["legend"][s]["type"] in ("count", "qty", "amount") and v < 0:
                continue
            tw["case"][s] = v
        g = row_answer(card, tw)
        if g is not None and g != gold0:
            tw.update({"gold": g, "twin_kind": "boundary", "threshold": None})
            return tw
    return None


def twin_exception(card, row, r, cs):
    X = target_of(row)
    if X is None or row["form"] == "inv":
        return None
    d = card["defs"][X]
    conds = []
    if d.get("exc") is not None and d["exc"]["k"] == "atom":
        conds.append(d["exc"])
    for it in d["body"]["items"]:
        if it["k"] == "item" and it.get("unless") is not None and it["unless"]["k"] == "atom":
            conds.append(it["unless"])
    gold0 = row_answer(card, row)
    r.shuffle(conds)
    for at in conds:
        s = at["a"]
        if s in row.get("omitted", []) or at["t"] == "rel":
            continue
        for v in cs.slot_reps(s, row["case"]):
            tw = copy.deepcopy(row)
            tw["case"][s] = v
            if M.eval_atom(at, tw["case"]) == M.eval_atom(at, row["case"]):
                continue
            g = row_answer(card, tw)
            if g is not None and g != gold0:
                tw.update({"gold": g, "twin_kind": "exception", "threshold": None})
                return tw
    return None
