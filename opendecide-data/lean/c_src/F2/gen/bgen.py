"""S3 row generation: CH-B (which band; computed banding amount near an edge), CH-V (total charge), YN-T (charge
vs T, half near / half far), CL (which case pays more than T), open-world CH-V (X10 category not recorded)."""
from __future__ import annotations

import random

import copy
import itertools

from . import bandeval as BE, bcard, options as O
from .common import D, ONE, ZERO, on_grid, quant
from .money import Reject
from .mrows import thr_place_far, near_family, near_op


def var_sem(card, var):
    sem = dict(card["b"]["sem"])
    if var:
        sem.update(card["variants"][var - 1]["over"])
    return sem


def grid_ok(LP, card):
    try:
        v, tr = BE.evaluate(LP, {})
    except (Reject, ArithmeticError):
        return False
    u = D(LP["unit"])
    if v < 0 or not on_grid(v, u):
        return False
    if "R1" not in LP["sem"]:
        for n, x in tr.nodes:
            if not on_grid(x, u if not n.startswith("part") and n != "amount" else ONE if LP.get("count") else u):
                return False
    return True


def set_limit(card, LP, rng):
    s = card["b"]
    if not s["minmax"]:
        return
    LP2 = copy.deepcopy(LP)
    LP2["steps"] = []
    c, _ = BE.evaluate(LP2, {})
    unit = s["unit"]
    bind = rng.random() < 0.5
    f = D(str(rng.uniform(0.6, 0.95))) if (bind == (s["minmax"] == "cap")) else D(str(rng.uniform(1.05, 1.6)))
    lim = quant(c * f, unit * (100 if s["dec2"] else 10), "half_up")
    if lim <= 0:
        lim = unit * 100
    LP["vals"][s["lim"]] = lim


def depth_of(LP):
    v, tr = BE.evaluate(LP, {})
    return tr


def printing(card, LP, rng):
    """Row group: marginal rows touching two bands print the part and the band charges (group c) or nothing (deep d)."""
    tr = depth_of(LP)
    ops = tr.ops
    if ops <= 2:
        return {}, {}, ("a" if ops == 1 else "b"), ops
    inter = tr.nodes[:-1]
    names = {}
    for n, x in inter:
        if n.startswith("part"):
            names[n] = f"{LP['bands'][int(n[4:])]['name']} part"
        elif n.startswith("bandcharge"):
            names[n] = f"{LP['bands'][int(n[10:])]['name']} charge"
        elif n == "amount":
            names[n] = LP["amt"].get("a") if LP["amt"]["kind"] == "stated" else _amt_label(LP)
    if all(names.get(n) for n, x in inter) and ops <= 5 and rng.random() < 0.7:
        u = D(LP["unit"])
        if all(on_grid(x, ONE if (n.startswith("part") and LP.get("count")) else u) for n, x in inter):
            return {names[n]: x for n, x in inter}, {names[n]: n for n, x in inter}, "c", ops
    if ops <= 4:
        return {}, {}, "d", ops
    raise Reject("too deep")


def _amt_label(LP):
    return LP.get("_amt_label")


def adj_tags(LP, lab_fn):
    tests = []
    if LP.get("x10"):
        tests.append(("exc", {"err": "E-exc"}))
    for st in LP.get("steps", []):
        tests.append(("cap" if st["op"] == "cap" else "floor", {"err": "E-cap" if st["op"] == "cap" else "E-floor"}))
    if "R1" in LP["sem"]:
        tests.append(("round", {"norround": True}))
    tags = []
    v0 = BE.evaluate(LP, {})[0]
    l0 = lab_fn(LP, {})
    for x, rd in tests:
        tags.append(f"has:{x}")
        try:
            if BE.evaluate(LP, rd)[0] != v0:
                tags.append(f"bind:{x}")
            if lab_fn(LP, rd) != l0:
                tags.append(f"dec:{x}")
        except (Reject, ArithmeticError):
            pass
    return tags


def gen_row(card, rng, var=0, want=None):
    from .mgen import predraw
    want = predraw(card, rng, dict(want or {}))
    sch = card["schema"]
    global _SWEEP
    _SWEEP = want.get("sweep")
    for attempt in range(300):
        want["_attempt"] = attempt
        try:
            if sch == "CH-B":
                r = _band_row(card, rng, var, want)
            elif sch == "CL":
                r = _cl_row(card, rng, var, want)
            elif card["world"] == "open":
                r = _open_row(card, rng, var, want)
            elif sch == "CH-V":
                r = _value_row(card, rng, var, want)
            else:
                r = _yn_row(card, rng, var, want)
            if r is not None:
                return r
        except (Reject, ArithmeticError):
            continue
    raise Reject(f"no band row ({card['card_id']})")


def _base(card, rng, var, want, place=None, want_band=None):
    sem = var_sem(card, var)
    d = bcard.draw(card, rng, want_band=want_band, place=place)
    LP = bcard.make_lp(card, d, {"kind": "value"}, sem)
    set_limit(card, LP, rng)
    if not grid_ok(LP, card):
        return None, None
    return LP, d


_SWEEP = None


def _finish(card, LP, rng, extra):
    if _SWEEP:
        extra["_sweep"] = _SWEEP
    if extra.get("_sweep"):
        tr0 = depth_of(LP)
        if tr0.ops != extra["_sweep"]:
            raise Reject("sweep depth")
        pr, pn, grp, ops = {}, {}, ("a" if tr0.ops == 1 else "b" if tr0.ops == 2 else "d"), tr0.ops
    else:
        pr, pn, grp, ops = printing(card, LP, rng)
    if pr:
        LP["printed"], LP["printed_nodes"] = pr, pn
    tr = depth_of(LP)
    depth = ops - len(pr)
    if depth < 1:
        raise Reject("no unstated op")
    out = {"LP": LP, "group": grp, "depth": depth, "ops": ops, "sel": tr.sel, "deep": grp == "d", "printed": set(pn.values())}
    extra.pop("_sweep", None)
    tags = extra.get("tags", [])
    tags.append("b1:" + LP["sem"]["B1"])
    if card.get("named"):
        tags.append("named:" + card["named"])
    if card["b"]["sem"]["B2"] == "flat" and extra.get("falling"):
        tags.append("cliff")
    extra["tags"] = tags
    out.update(extra)
    return out


def _band_row(card, rng, var, want):
    nb = card["b"]["nb"]
    tb = want.get("band", rng.randrange(nb))
    r = rng.random()
    place = "edge" if r < 0.30 else ("below" if r < 0.65 else "above")
    LP, d = _base(card, rng, var, want, place=place, want_band=tb)
    if LP is None:
        return None
    LP["q"] = {"kind": "band"}
    gname = BE.band_of(LP, {})
    names = [b["name"] for b in LP["bands"]]
    gi = names.index(gname)
    elig = bcard.band_hooks(LP, card["shown"], gname)
    _b = [n for n in elig if names.index(n) < gi]
    _a = [n for n in elig if names.index(n) > gi]
    k = O.held_k(want, [2, 3, 4, 4, 5, 6], O.kmax_all_ranks_list(_b, _a), rng)   # repair r2
    if k is None:
        return None
    if k < 2:
        return None
    rr = O.held_rank(want, k, rng)
    below = [n for n in elig if names.index(n) < gi]
    above = [n for n in elig if names.index(n) > gi]
    if rr > len(below) or k - 1 - rr > len(above):
        return None
    pick = rng.sample(below, rr) + rng.sample(above, k - 1 - rr)
    chosen = sorted(pick + [gname], key=names.index)
    oerr = {n: elig[n] for n in pick}
    oerr[gname] = "gold"
    amt = BE.amount(LP, BE.Tr())
    on_edge = any(amt == D(b[k_]) for b in LP["bands"] for k_ in ("lo", "hi") if b.get(k_) is not None)
    tags = [f"err:{e}" for e in oerr.values() if e != "gold"] + (["boundary:at"] if on_edge else ["boundary:above1" if place == "above" else "boundary:below1"])
    return _finish(card, LP, rng, {"qkind": "band", "gold": gname, "options": chosen, "opt_err": oerr, "tags": tags,
                                   "k": len(chosen), "rank": rr, "on_edge": on_edge, "falling": d["falling"]})


def _value_row(card, rng, var, want):
    LP, d = _base(card, rng, var, want)
    if LP is None:
        return None
    gold, tr = BE.evaluate(LP, {})
    hk = bcard.hooks(LP, card["shown"], gold)
    single = O.single_hook_values(hk)
    show_none = want.get("show_none", False)
    kmax = min(1 + len(single), O.kmax_all_ranks(gold, single)) + (1 if show_none else 0)   # repair r2
    choices = [x for x in card.get("k_choices", [2, 3, 4, 4, 5, 6, 7, 8, 9]) if x <= kmax and (not show_none or x >= 3)]
    if not choices:
        return None
    kp = want.get("k_pref")
    if kp and want.get("_attempt", 0) < 150:
        if kp > kmax or (show_none and kp < 3):
            return None
        k = kp
    else:
        k = choices[min(int(want.get("u_k", rng.random()) * len(choices)), len(choices) - 1)]   # repair r1.1
    k_ord = k - (1 if show_none else 0)
    r = O.held_rank(want, k_ord, rng)
    if O.pick_ranked(rng, gold, single, k_ord, r) is None or (show_none and len(single) < k_ord):
        return None
    gold_none = show_none and rng.random() < O.abst_p("none", k)          # repair r2
    if gold_none:
        if len(single) < k_ord:
            return None
        pick = sorted(rng.sample(sorted(single), k_ord))
        opts = [bcard.mstr(v, card) for v in pick] + [card["none_text"]]
        oerr = {bcard.mstr(v, card): single[v] for v in pick}
        gold_txt = card["none_text"]
        oerr[gold_txt] = "gold"
    else:
        pr = O.pick_ranked(rng, gold, single, k_ord, r)
        if pr is None:
            return None
        vals_ord, errs = pr
        opts = [bcard.mstr(v, card) for v in vals_ord]
        gold_txt = bcard.mstr(gold, card)
        oerr = {bcard.mstr(v, card): errs[v] for v in errs}
        oerr[gold_txt] = "gold"
        if show_none:
            opts.append(card["none_text"])
            oerr[card["none_text"]] = "abst"
    LP["q"] = {"kind": "value"}
    tags = adj_tags(LP, lambda L, rd: BE.evaluate(L, rd)[0]) + [f"err:{e}" for e in oerr.values() if e not in ("gold", "abst")]
    if show_none:
        tags.append("abst:none")
    return _finish(card, LP, rng, {"qkind": "value", "gold": gold_txt, "options": opts, "opt_err": oerr, "tags": tags,
                                   "k": len(opts), "rank": r, "falling": d["falling"]})


def _yn_row(card, rng, var, want):
    LP, d = _base(card, rng, var, want)
    if LP is None:
        return None
    neg = want.get("neg", 0)
    aff = want["aff"] if "aff" in want else (rng.random() < card["yes_rate"])
    # repair r1.1: label-side draws (question kind, near / far, delta, comparator family) come from a stream seeded
    # by the held uniform u_side, so structure retries never correlate them with the held label
    rs = random.Random(want["u_side"]) if "u_side" in want else rng
    R = BE.compared(LP, {})
    unit = card["b"]["unit"]
    near = rs.random() < 0.5
    if near:
        r = rs.random()
        delta = 0 if r < 0.3 else (-1 if r < 0.65 else 1)
        fam = near_family(rs, delta, aff)
        op = near_op(rs, delta, aff, fam)
        T = R - delta * unit
        place = {"near": True, "delta": delta, "mech": None}
    else:
        op, T = thr_place_far(rs, R, unit, aff)
        place = {"near": False, "delta": None, "mech": None}
    if T <= 0 or not on_grid(T, unit):
        return None
    LP["q"] = {"kind": "thr", "cmp": op, "T": T, "neg": neg}
    if BE.aff(LP, {}) != aff:
        return None
    tags = adj_tags(LP, lambda L, rd: BE.aff(L, rd))
    dd = abs(R - T)
    tags.append("boundary:at" if dd == 0 else ("boundary:above1" if R > T else "boundary:below1") if dd <= unit else "boundary:far")
    tags.append("cmp:" + ("incl" if op in ("ge", "le") else "excl"))
    return _finish(card, LP, rng, {"qkind": "thr", "aff": aff, "neg": neg, "gold": aff ^ (neg % 2 == 1), "tags": tags,
                                   "placement": place, "op": op, "T": T, "falling": d["falling"]})


def _cl_row(card, rng, var, want):
    """Which case pays more / less than T: per case the banding amount (or q, p) and the X10 category; the band table
    and limits are shared."""
    s = card["b"]
    sem = var_sem(card, var)
    base_d = bcard.draw(card, rng)
    keys = [s["q"], s["p"]] if s["computed"] else [s["amt"]]
    if s["x10"]:
        keys.append(s["x10"]["f"])
    base = bcard.make_lp(card, base_d, {"kind": "value"}, sem)
    set_limit(card, base, rng)
    readings = bcard.alt_readings(base, card["shown"])
    n = want["ncases"]
    show_none = card.get("none_ok", False)
    k = n + (1 if show_none else 0)
    gold_none = want["gold_none"]

    def case_draw():
        d2 = bcard.draw(card, rng)
        cv = {kk: d2["vals"][kk] for kk in keys if kk in d2["vals"]}
        cf = {kk: d2["facts"][kk] for kk in keys if kk in d2["facts"]}
        L2 = {**base, "vals": {**base["vals"], **cv}, "facts": {**base["facts"], **cf}}
        return cv, cf, L2

    pool = []
    for _ in range(50):
        cv, cf, L2 = case_draw()
        if not grid_ok(L2, card):
            continue
        try:
            pool.append(BE.compared(L2, {}))
        except (Reject, ArithmeticError):
            continue
    if len(pool) < 15:
        return None
    pool.sort()
    op = rng.choice(["gt", "ge", "lt", "le"])
    qq = rng.choice([0.6, 0.7, 0.8, 0.9])
    T = pool[int(len(pool) * (qq if op in ("gt", "ge") else 1 - qq))]
    T = quant(T, s["unit"] * (100 if s["dec2"] else 10), "half_up")
    if T <= 0:
        return None
    C = BE.CMP[op]
    # repair r1.1: cases come from one drawn pool; the gold case's rank on its first value column among the listed
    # cases is held uniform (matched case lists; v1.0 drew cases one by one, gold extreme on most rows)

    def _pv(cv):
        for kk in keys:
            v = cv.get(kk)
            if v is not None and not isinstance(v, (str, bool)):
                return D(v)
        return None
    pool_g, pool_e = [], []
    seen = set()
    need_err = n - (0 if gold_none else 1)
    for t in range(max(400, 60 * n)):
        cv, cf, L2 = case_draw()
        key = (tuple(sorted((k_, str(v_)) for k_, v_ in cv.items())), tuple(sorted(cf.items())))
        if key in seen:
            continue
        if not grid_ok(L2, card):
            continue
        try:
            g = C(BE.compared(L2, {}), T)
        except (Reject, ArithmeticError):
            continue
        try:
            tr_ = BE.evaluate(L2, {})[1]
        except (Reject, ArithmeticError):
            continue
        pay = {"vals": cv, "facts": cf, "_ops": tr_.ops, "_sel": tr_.sel}
        if g:
            if len(pool_g) < 40:
                pool_g.append(pay)
                seen.add(key)
            continue
        hits = []
        for eid, rd in readings:
            try:
                if C(BE.compared(L2, rd), T):
                    hits.append(eid)
            except (Reject, ArithmeticError, ValueError):
                continue
        if len(hits) == 1:
            pool_e.append((pay, hits[0]))
            seen.add(key)
        if len(pool_g) >= 40 and len(pool_e) >= 8 * n:
            break
    gp = O.one_group(rng, pool_g, pool_e, need_err, not gold_none,
                     lambda p_: (None if (p_["_ops"] > 2 or p_["_sel"] > 3) else ("a" if p_["_ops"] == 1 else "b")))
    if gp is None:
        return None
    pool_g, pool_e = gp
    pr = None
    if not gold_none:
        pr = O.pick_cases_ranked(rng, pool_g, pool_e, need_err, O.case_target(want, n), lambda p_: _pv(p_["vals"]))
        if pr is None and O.case_strict(want):
            return None
    if pr is not None:
        g_, picked = pr
        cases = [dict(p_, err=kd) for p_, kd in picked] + [dict(g_, err="gold")]
    else:
        picked = O.round_robin(pool_e, need_err, rng)
        if picked is None:
            return None
        cases = [dict(p_, err=kd) for p_, kd in picked] + ([] if gold_none else [dict(rng.choice(pool_g), err="gold")])
    for c_ in cases:
        c_.pop("_ops", None)
        c_.pop("_sel", None)
    rng.shuffle(cases)
    refs = card["case_refs"](n, rng)
    for c, ref in zip(cases, refs):
        c["ref"] = ref
    LP = dict(base)
    LP["vals"] = {kk: v for kk, v in base["vals"].items() if kk not in keys}
    LP["facts"] = {kk: v for kk, v in base["facts"].items() if kk not in keys}
    LP["q"] = {"kind": "cases", "cmp": op, "T": T, "cases": [{"vals": c["vals"], "facts": c["facts"]} for c in cases]}
    hits = [i for i, c in enumerate(cases) if C(BE.compared({**base, "vals": {**base["vals"], **c["vals"]},
                                                             "facts": {**base["facts"], **c["facts"]}}, {}), T)]
    if gold_none:
        if hits:
            return None
        gold_txt = card["none_text"]
    else:
        if len(hits) != 1:
            return None
        gold_txt = cases[hits[0]]["ref"]
    opts = [c["ref"] for c in cases] + ([card["none_text"]] if show_none else [])
    oerr = {c["ref"]: c["err"] for c in cases}
    if show_none:
        oerr[card["none_text"]] = "gold" if gold_none else "abst"
    groups, depths, sels = set(), [], []
    for c in cases:
        L2 = {**base, "vals": {**base["vals"], **c["vals"]}, "facts": {**base["facts"], **c["facts"]}}
        v, tr = BE.evaluate(L2, {})
        groups.add("a" if tr.ops == 1 else "b" if tr.ops == 2 else "d")
        depths.append(tr.ops)
        sels.append(tr.sel)
    if len(groups) != 1 or max(depths) > 2 or max(sels) > 3:
        return None
    tags = [f"err:{c['err']}" for c in cases if c["err"] != "gold"] + [f"cases:{n}", "cmp:" + ("incl" if op in ("ge", "le") else "excl"), "b1:" + sem["B1"]]
    if show_none:
        tags.append("abst:none")
    return {"LP": LP, "qkind": "cases", "gold": gold_txt, "options": opts, "opt_err": oerr, "tags": tags,
            "k": len(opts), "cases": cases, "op": op, "T": T, "group": groups.pop(), "depth": max(depths),
            "ops": max(depths), "sel": max(sels), "deep": False, "printed": set(), "case_keys": keys}


def _open_row(card, rng, var, want):
    """Open-world CH-V: the X10 category is 'not recorded'. Needed (NEI gold) with probability 1/k: the amount is
    above the lowest band, so X10 changes the rate; inert: the amount sits in the lowest band (nothing changes)."""
    s = card["b"]
    x = s["x10"]
    k = want["k"]
    needed = want["needed"]
    LP, d = _base(card, rng, var, want, want_band=(rng.randrange(1, s["nb"]) if needed else 0))
    if LP is None:
        return None
    outs = []
    for c in x["dom"]:
        L2 = {**LP, "facts": {**LP["facts"], x["f"]: c}}
        if not grid_ok(L2, card):
            return None
        outs.append(BE.evaluate(L2, {})[0])
    distinct = sorted(set(outs))
    idx = BE.locate(BE.amount(LP, BE.Tr()), LP["bands"], LP["sem"]["B1"])
    if needed and (idx == 0 or len(distinct) < 2):
        return None
    if not needed and (idx != 0 or len(distinct) != 1):
        return None
    LP["facts"] = {**LP["facts"], x["f"]: "not recorded"}
    LP["q"] = {"kind": "value"}
    nei = card["nei"]
    if needed:
        kk = k - 1
        if len(distinct) < kk:
            return None
        vals = sorted(rng.sample(distinct, kk))
        opts = [bcard.mstr(v, card) for v in vals] + [nei]
        oerr = {o: "E-assume" for o in opts[:-1]}
        oerr[nei] = "gold"
        return _finish(card, LP, rng, {"qkind": "value", "gold": nei, "options": opts, "opt_err": oerr,
                                       "tags": ["nei:needed", "abst:nei", "world:open"], "k": len(opts), "nei": "needed",
                                       "falling": d["falling"]})
    gold = distinct[0]
    L2 = {**LP, "facts": {**LP["facts"], x["f"]: x["dom"][0]}, "world": "closed"}
    hk = bcard.hooks(L2, card["shown"], gold)
    single = {v: e for v, e in O.single_hook_values(hk).items() if e != "E-exc"}
    k_ord = k - 1
    if k_ord > O.kmax_all_ranks(gold, single):          # repair r2
        return None
    r = O.held_rank(want, k_ord, rng)
    pr = O.pick_ranked(rng, gold, single, k_ord, r)
    if pr is None:
        return None
    vals_ord, errs = pr
    opts = [bcard.mstr(v, card) for v in vals_ord] + [nei]
    oerr = {bcard.mstr(v, card): errs[v] for v in errs}
    oerr[bcard.mstr(gold, card)] = "gold"
    oerr[nei] = "abst"
    return _finish(card, LP, rng, {"qkind": "value", "gold": bcard.mstr(gold, card), "options": opts, "opt_err": oerr,
                                   "tags": ["nei:inert", "abst:nei", "world:open"] + [f"err:{e}" for e in errs.values()],
                                   "k": len(opts), "nei": "inert", "falling": d["falling"]})
