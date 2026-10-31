"""Engine adapter for money cards (S1, S2): card building, row generation, twins, rendering."""
from __future__ import annotations

import copy
from decimal import Decimal

from . import assemble_money as AM, mbuild, mcard, mdoc, mgen, money
from .common import D, ONE, on_grid
from .mgen import var_sem
from .money import Reject
from .mrows import gen_entity_id, grid_ok

NAME = "money"


def make_card(card, pack, rng, **kw):
    mbuild.make_money_card(card, pack, rng, **kw)
    if card.get("instr") == "fewshot":
        blk, hashes = AM.build_fewshot(card, rng)
        if blk is None:
            card["instr"] = "std"
        else:
            card["fewshot_block"] = blk
            card["fewshot_hashes"] = hashes
    return card


def gen_row(card, rng, var=0, want=None):
    return mgen.gen_row(card, rng, var, want)


def to_row(card, spec, rng, **kw):
    return AM.to_row(card, spec, rng, **kw)


def new_eid(card, rng, used):
    return gen_entity_id(card, rng, used)


def can_negate(spec):
    return spec.get("qkind") in ("thr", "op")


def with_neg(spec, n):
    s = copy.deepcopy(spec)
    s["LP"]["q"]["neg"] = n
    s["neg"] = n
    s["gold"] = s["aff"] ^ (n % 2 == 1)
    s["tf"] = True
    return s


def _printed_same(card, spec, LP2):
    if not spec.get("printed"):
        return True
    v, tr = money.evaluate(LP2, {})
    names = mgen.node_names(card, LP2)
    now = {names[n]: x for n, x in tr.nodes if n in spec["printed"]}
    return now == spec["LP"].get("printed")


def boundary_twin(card, spec, rng):
    """Move one decisive input by one resolution unit so the label flips (A predicts; MR10)."""
    if spec.get("qkind") != "thr" or spec.get("printed"):
        return None
    LP = spec["LP"]
    m = card["m"]
    cands = []
    for ln in m["lines"]:
        if ln["p"] in ("mul", "perk"):
            q = D(LP["vals"][ln["q"]])
            step = D("0.25") if (q != q.to_integral_value()) else ONE
            cands += [(ln["q"], step), (ln["q"], -step)]
            cands += [(ln["r"], m["unit"]), (ln["r"], -m["unit"])]
        elif ln["p"] == "stated":
            cands += [(ln["a"], m["unit"]), (ln["a"], -m["unit"])]
    rng.shuffle(cands)
    a0 = spec["aff"]
    for lab, d in cands:
        LP2 = copy.deepcopy(LP)
        nv = D(LP2["vals"][lab]) + d
        if nv <= 0:
            continue
        LP2["vals"][lab] = nv
        try:
            if not grid_ok(LP2, card, card["shown"]):
                continue
            a2 = money.yn_label(LP2, {})[0]
        except (Reject, ArithmeticError):
            continue
        if a2 != a0:
            s = copy.deepcopy(spec)
            s["LP"] = LP2
            s["aff"] = a2
            s["gold"] = a2 ^ (spec["neg"] % 2 == 1)
            s["tags"] = [t for t in s["tags"] if not t.startswith(("boundary:", "dec:", "bind:", "has:"))]
            from .mrows import adj_tags, val_fn
            s["tags"] += adj_tags(LP2, "YN-T", lambda L, rd: money.yn_label(L, rd)[0], val_fn)
            dd = abs(money.compared_value(LP2, {}) - D(LP2["q"]["T"]))
            s["tags"].append("boundary:at" if dd == 0 else "boundary:above1" if dd <= card["res_unit"] else "boundary:far")
            return s
    return None


def flip_twin(card, spec, var):
    """The base row's values on the card's flip variant `var` (one SEM switch apart): label = A's alt-label, which must
    differ from the base's; no printed number changes; choice rows keep the base's option list (R1-21)."""
    if spec.get("qkind") not in ("thr", "op", "value") or card["world"] != "closed":
        return None
    LP = spec["LP"]
    sem2 = var_sem(card, var)
    LP2 = copy.deepcopy(LP)
    LP2["sem"] = {k: v for k, v in sem2.items() if k not in ("ORJ", "B1o")}
    for st in LP2["steps"]:
        if st["op"] in ("cap", "min") and "X4" in sem2 and st["id"] in sem2["X4"]:
            st["scope"] = sem2["X4"][st["id"]]
    if "ORJ" in sem2:
        for e in LP2["excs"]:
            if str(e["no"]) in sem2["ORJ"]:
                e["join"] = sem2["ORJ"][str(e["no"])]
    for d in card.get("omitted", []):
        LP2["sem"].pop(d, None)
    try:
        if not grid_ok(LP2, card, card["shown"]) or not _printed_same(card, spec, LP2):
            return None
        if spec["qkind"] in ("thr", "op"):
            a2 = money.yn_label(LP2, {})[0]
            if a2 == spec["aff"]:
                return None
            s = copy.deepcopy(spec)
            s["LP"] = LP2
            s["aff"] = a2
            s["gold"] = a2 ^ (spec["neg"] % 2 == 1)
            return s
        v2 = money.evaluate(LP2, {})[0]
        g2 = mcard.mstr(v2, card)
        if g2 == spec["gold"] or g2 not in spec["options"]:
            return None
        hk = mcard.hooks(LP2, card["shown"] | set(LP2["sem"]), v2)
        from .options import single_hook_values
        single = {mcard.mstr(v, card): e for v, e in single_hook_values(hk).items()}
        oerr = {}
        for o in spec["options"]:
            if o == g2:
                oerr[o] = "gold"
            elif o in single:
                oerr[o] = single[o]
            elif o == card.get("none_text"):
                oerr[o] = "abst"
            else:
                return None
        s = copy.deepcopy(spec)
        s["LP"] = LP2
        s["gold"] = g2
        s["opt_err"] = oerr
        return s
    except (Reject, ArithmeticError):
        return None


def inert_pair(card, spec, rng, used_labels):
    """An inert value line: a record line of a type no rule names (R3-12 (iii)); label and every printed number
    unchanged without it."""
    from .mdoc import INERT_LABELS
    labs = [x for x in INERT_LABELS if x.lower() not in used_labels]
    if not labs:
        return None
    lab = rng.choice(labs)
    m = card["m"]
    if lab in ("travel time logged",):
        val = f"{rng.randint(1, 9)} hours"
    elif lab in ("loyalty points balance", "courier slots booked", "visitor passes issued"):
        val = str(rng.randint(2, 400))
    elif lab == "previous invoice reference":
        val = f"{card['prefix']}-{rng.randint(1000, 9999)}"
    else:
        val = mcard.mstr(D(rng.randint(20, 900)), card)
    return (lab, val)


def labels_in(card):
    m = card["m"]
    out = {m["res"].lower()}
    for ln in m["lines"]:
        for k in ("q", "r", "a", "lc"):
            if ln.get(k):
                out.add(ln[k].lower())
    for st in m["steps"]:
        vs = st["v"] if isinstance(st.get("v"), list) else [st.get("v")]
        out |= {x.lower() for x in vs if x}
    for e in m["excs"]:
        out |= {e["v"].lower(), e["on"].lower()} | {c["f"].lower() for c in e["conds"]}
    return out
