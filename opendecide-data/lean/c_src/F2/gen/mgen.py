"""Money row generation (S1 forward, S2 target-first; also the S5 statement rows through stmt.py).

gen_row(card, rng, var) -> row spec (no text). Schemas: YN-T (threshold or OP 'owed'), CH-V, CH-O, CL.
Open-world cards (choice only): one case fact 'not recorded'; NEI gold with probability 1/k (XF01, SC2).
"""
from __future__ import annotations

import random

import itertools
import math
from decimal import Decimal

from . import mcard, money, options as O
from .common import D, ONE, ZERO, on_grid, quant
from .money import Reject
from .mrows import (_final, _unit, grid_ok, invariance_ok, depth_info, adj_tags, val_fn, thr_place_far, near_family,
                    near_op, choose_printing, apply_printed, node_names)

MECHS = ["round", "capfloor", "exc", "partial", "plain"]


def var_sem(card, var):
    sem = dict(card["m"]["sem"])
    if var:
        v = card["variants"][var - 1]
        sem = merge_sem(sem, v["over"])
    return sem


def merge_sem(sem, over):
    s = dict(sem)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(s.get(k), dict):
            s[k] = {**s[k], **v}
        else:
            s[k] = v
    return s


def shown_dims(card):
    return card["shown"]


def lab_of(LP, rd):
    """Label-ish value for invariance and dec: tags (yes/no: affirmative truth; value: value; outcome: name)."""
    q = LP["q"]
    if q["kind"] in ("thr", "op"):
        return money.yn_label(LP, rd)[0]
    if q["kind"] == "outcome":
        sem = {**LP["sem"], **rd.get("sem", {})}
        v = money.compared_value(LP, rd)
        return money.outcome_of(v, q["outs"], q["b1"])
    if q["kind"] == "cases":
        return tuple(case_hits(LP, rd))
    v, _ = money.evaluate(LP, rd)
    return v


def case_hits(LP, rd):
    q = LP["q"]
    hits = []
    for i, c in enumerate(q["cases"]):
        LP2 = {**LP, "vals": {**LP["vals"], **c["vals"]}, "facts": {**LP["facts"], **c["facts"]}}
        v = money.compared_value(LP2, rd)
        if money.CMP[q["cmp"]](v, D(q["T"])):
            hits.append(i)
    return hits


def _mech_decisive(LP, mech):
    """Is the drawn mechanism decisive (the label differs without it)? 'plain': no adjustment is decisive."""
    tests = {"capfloor": [{"err": "E-cap"}, {"err": "E-floor"}],
             "exc": [{"excl": {e["no"] for e in LP.get("excs", [])}}],
             "round": [{"norround": True}],
             "partial": [{"sem": {"R5": "exact"}}] if "R5" in LP["sem"] else [{"sem": {"U3": "pro_rata"}}]}
    a0 = money.yn_label(LP, {})[0]

    def dec(rd):
        try:
            return money.yn_label(LP, rd)[0] != a0
        except (Reject, ArithmeticError, ValueError):
            return False
    if mech == "plain":
        for m in ("capfloor", "exc", "round", "partial"):
            if any(dec(rd) for rd in tests[m] if _mech_avail(LP, m)):
                return False
        return True
    return any(dec(rd) for rd in tests[mech])


def _mech_avail(LP, mech):
    ops = {s["op"] for s in LP["steps"]}
    if mech == "capfloor":
        return bool(ops & {"cap", "min"})
    if mech == "exc":
        return bool(LP.get("excs"))
    if mech == "round":
        return "R1" in LP["sem"]
    if mech == "partial":
        return "R5" in LP["sem"] or "U3" in LP["sem"]
    return True


def predraw(card, rng, want):
    """Statuses drawn once per row, before any structure is drawn, so retries never bias them (XF01: abstain gold
    with probability 1/k; NEI needed with probability 1/k)."""
    sch = card["schema"]
    # repair r1.1: gold-rank and case-rank uniforms, drawn once per base row and held across retries
    want.setdefault("u_rank", rng.random())
    want.setdefault("u_crank", rng.random())
    want.setdefault("u_k", rng.random())
    want.setdefault("u_side", rng.random())
    want.setdefault("u_grp", rng.random())        # repair r2: held depth-group target (money rows; 1.1, section 6)
    if card.get("qtype") == "noul" and "yes_rate" in card:
        # the affirmative-proposition draw is held too, so label-dependent rejections never move the yes rate
        want.setdefault("aff", rng.random() < card["yes_rate"])
    if card["world"] == "open":
        k = want.setdefault("k", rng.choice(card.get("open_k", [3])))
        want.setdefault("needed", rng.random() < O.abst_p("nei", k))          # repair r2
    elif sch == "CL":
        n = want.setdefault("ncases", O.draw_ncases(rng, card["ncase_choices"]))     # repair r2: by option bucket
        k = n + (1 if card.get("none_ok") else 0)
        # abstain gold with probability 1/k from a uniform drawn here, before any structure; money case lists may
        # shrink the case count to what the drawn rules support and then compare the same uniform with the final 1/k
        u = want.setdefault("u_none", rng.random())
        want.setdefault("gold_none", bool(card.get("none_ok")) and u < O.abst_p("none", k))   # repair r2
    elif sch in ("CH-V",):
        want.setdefault("show_none", bool(card.get("none_ok")) and rng.random() < card.get("none_rate", 0.35))
        want.setdefault("k_pref", rng.choice(card.get("k_choices", [2, 3, 4])))
    return want


def gen_row(card, rng, var=0, want=None):
    """One base row. want: optional dict of targets (mech, aff, neg, k, ...)."""
    want = predraw(card, rng, dict(want or {}))
    schema = card["schema"]
    sem = var_sem(card, var)
    shown = card["shown"]
    m = card["m"]
    unit = m["unit"]
    for attempt in range(400):
        want["_attempt"] = attempt
        try:
            vals, facts = mcard.draw(card, rng)
            if schema == "CL":
                r = _cl_row(card, rng, var, sem, want, vals, facts)
                if r is None:
                    continue
                return r
            q = {"kind": "value"}
            LP = mcard.make_lp(card, vals, facts, q, sem)
            if card["world"] == "open":
                r = _open_row(card, rng, var, sem, want, LP)
                if r is None:
                    continue
                return r
            if not grid_ok(LP, card, shown):
                continue
            if not invariance_ok({**LP, "q": {"kind": "value"}}, card, shown, lambda L, rd: val_fn(L, rd)):
                continue
            if schema == "YN-T":
                r = _yn_row(card, rng, var, sem, want, LP)
            elif schema == "CH-V":
                r = _value_row(card, rng, var, sem, want, LP)
            elif schema == "CH-O":
                r = _outcome_row(card, rng, var, sem, want, LP)
            else:
                raise ValueError(schema)
            if r is None:
                continue
            return r
        except (Reject, ArithmeticError) as e:
            continue
    raise Reject(f"no row after 400 tries ({card['card_id']})")


# repair r2: money rows (S1, S2) draw a depth-group target once per base row (held across retries) and resample the
# structure until the row's group matches, for GRP_STRICT attempts, then take the group the structure gives. v1.2 left
# the group to the drawn structure: family plain d1 46.1 / d2 42.7 / stated 4.7 / deep 6.6 vs 30 / 45 / 17 / <= 10
# (section 6). S4 date rows have no stated group and S3 band rows ~1%, so money rows carry the stated share.
GRP_W = (("a", 0.20), ("b", 0.42), ("c", 0.30), ("d", 0.08))
GRP_STRICT = 150


def group_target(want):
    u = want.get("u_grp")
    if u is None or want.get("_attempt", 0) >= GRP_STRICT:
        return None
    acc = 0.0
    for g, w in GRP_W:
        acc += w
        if u < acc:
            return g
    return GRP_W[-1][0]


def _finish(card, LP, rng, want, extra):
    """Row group, depth, tags common to every money row."""
    v, tr = _final(LP)
    if want.get("sweep"):
        if tr.ops != want["sweep"]:
            raise Reject("sweep depth")
        out = {"LP": LP, "group": "a" if tr.ops == 1 else "b" if tr.ops == 2 else "d", "depth": tr.ops, "ops": tr.ops,
               "sel": tr.sel, "deep": tr.ops >= 3, "printed": set()}
        out.update(extra)
        return out
    tg = group_target(want)
    want_c = (tg == "c") if tg in ("c", "d") else want.get("want_c", rng.random() < 0.9)
    printed, grp = choose_printing(card, LP, rng, want_c)
    if tg is not None and grp != tg:
        raise Reject("group target")
    names = node_names(card, LP)
    if printed:
        apply_printed(LP, tr.nodes, printed, names)
    depth = tr.ops - len(printed)
    if depth < 1:
        raise Reject("no unstated operation")
    if tr.sel > 3 and grp != "d":
        raise Reject("more than 3 selection steps")
    out = {"LP": LP, "group": grp, "depth": depth, "ops": tr.ops, "sel": tr.sel, "deep": grp == "d",
           "printed": printed}
    out.update(extra)
    return out


# ----------------------------------------------------------------------------------------------------------------- YN-T

def _yn_row(card, rng, var, sem, want, LP):
    m = card["m"]
    unit = m["unit"]
    neg = want.get("neg", 0)
    p = card["yes_rate"]
    aff = want["aff"] if "aff" in want else (rng.random() < p)
    # repair r1.1: label-side draws (question kind, near / far, delta, comparator family) come from a stream seeded
    # by the held uniform u_side, so structure retries never correlate them with the held label
    rs = random.Random(want["u_side"]) if "u_side" in want else rng
    if card.get("op_item") and (want.get("qkind") == "op" or (want.get("qkind") is None and rs.random() < 0.5)):
        LP["q"] = {"kind": "op", "neg": neg}
        v, tr = _final(LP)
        if (v > 0) != aff:
            return None
        # R3-14: the amount with no rounding step is > 0 exactly when the reported amount is
        if "R1" in LP["sem"]:
            vu, _ = money.evaluate(LP, {"norround": True})
            if (vu > 0) != (v > 0):
                return None
        tags = adj_tags(LP, "YN-T", lambda L, rd: money.yn_label(L, rd)[0], val_fn)
        return _finish(card, LP, rng, want, {"qkind": "op", "aff": aff, "neg": neg, "gold": aff ^ (neg % 2 == 1),
                                            "tags": tags + ["cmp:op"], "placement": None})
    R, tr = _final(LP)
    sampler = card["sampler"]
    near = sampler == "S2" or (sampler in ("S3", "S5") and rs.random() < 0.5) or want.get("near")
    if want.get("far"):
        near = False
    mech = None
    if near:
        mechs = [x for x in m.get("mechs", MECHS) if _mech_avail(LP, x)]
        mech = want.get("mech") or rng.choice(mechs)
        if not _mech_avail(LP, mech):
            return None
        res_unit = card.get("res_unit", unit)
        delta = want.get("delta")
        if delta is None:
            r = rs.random()
            delta = 0 if r < 0.30 else (-1 if r < 0.65 else 1)
        fam = near_family(rs, delta, aff)
        op = near_op(rs, delta, aff, fam)
        # comparisons read the rounded value (R3) unless the variant's R3 is the T form
        Rc = money.compared_value(LP, {})
        if op in ("ge", "gt"):
            T = Rc - delta * res_unit
        else:
            T = Rc - delta * res_unit
        if T <= 0:
            return None
        LP["q"] = {"kind": "thr", "cmp": op, "T": T, "neg": neg}
        a, lab = money.yn_label(LP, {})
        if a != aff:
            return None
        if not _mech_decisive(LP, mech):
            return None
        place = {"near": True, "delta": delta, "mech": mech}
    else:
        op, T = thr_place_far(rs, R, unit, aff)
        LP["q"] = {"kind": "thr", "cmp": op, "T": T, "neg": neg}
        a, lab = money.yn_label(LP, {})
        if a != aff:
            return None
        place = {"near": False, "delta": None, "mech": None}
    if not on_grid(T, card.get("res_unit", unit)):
        return None
    tags = adj_tags(LP, "YN-T", lambda L, rd: money.yn_label(L, rd)[0], val_fn)
    d = abs(money.compared_value(LP, {}) - T)
    if d == 0:
        tags.append("boundary:at")
    elif d <= card.get("res_unit", unit):
        tags.append("boundary:above1" if money.compared_value(LP, {}) > T else "boundary:below1")
    else:
        tags.append("boundary:far")
    tags.append("cmp:" + ("incl" if op in ("ge", "le") else "excl"))
    if place["mech"]:
        tags.append("mech:" + {"capfloor": "capfloor", "exc": "exc", "round": "round", "partial": "partial",
                               "plain": "plain"}[place["mech"]])
    return _finish(card, LP, rng, want, {"qkind": "thr", "aff": aff, "neg": neg, "gold": aff ^ (neg % 2 == 1),
                                        "tags": tags, "placement": place, "op": op, "T": T})


# ----------------------------------------------------------------------------------------------------------------- CH-V

def _value_row(card, rng, var, sem, want, LP):
    m = card["m"]
    gold, tr = _final(LP)
    shown = card["shown"]
    hk = mcard.hooks(LP, shown | set(LP["sem"]), gold)
    single = O.single_hook_values(hk)
    show_none = want.get("show_none", False)
    kmax = min(1 + len(single), O.kmax_all_ranks(gold, single)) + (1 if show_none else 0)   # repair r2
    choices = [x for x in card["k_choices"] if x <= kmax and (not show_none or x >= 3)]
    if not choices:
        return None
    kp = want.get("k_pref")
    if kp and want.get("_attempt", 0) < 200:
        if kp > kmax or (show_none and kp < 3):
            return None
        k = kp
    else:
        # repair r1.1: the fallback count comes from the held uniform too (independent of the held rank)
        k = want.get("k") or choices[min(int(want.get("u_k", rng.random()) * len(choices)), len(choices) - 1)]
    if k > kmax:
        return None
    k_ord = k - (1 if show_none else 0)
    r = want.get("rank")
    if r is None:
        r = O.held_rank(want, k_ord, rng)
    if O.pick_ranked(rng, gold, single, k_ord, r) is None or (show_none and len(single) < k_ord):
        return None                      # infeasible for this structure: resample before drawing the abstain gold
    gold_none = show_none and rng.random() < O.abst_p("none", k)          # repair r2
    if gold_none:
        # "None of the listed" gold: no shown option equals the value; every shown value is a single-hook value
        cands = dict(single)
        if len(cands) < k_ord:
            return None
        pick = rng.sample(sorted(cands), k_ord)
        vals_ord = sorted(pick)
        errs = {v: cands[v] for v in pick}
        opts = [mcard.mstr(v, card) for v in vals_ord] + [card["none_text"]]
        gold_txt = card["none_text"]
        oerr = {mcard.mstr(v, card): errs[v] for v in vals_ord}
        oerr[gold_txt] = "gold"
        extra_tags = ["abst:none"]
    else:
        pr = O.pick_ranked(rng, gold, single, k_ord, r)
        if pr is None:
            return None
        vals_ord, errs = pr
        opts = [mcard.mstr(v, card) for v in vals_ord]
        gold_txt = mcard.mstr(gold, card)
        oerr = {mcard.mstr(v, card): errs[v] for v in errs}
        oerr[gold_txt] = "gold"
        extra_tags = []
        if show_none:
            opts.append(card["none_text"])
            oerr[card["none_text"]] = "abst"
            extra_tags = ["abst:none"]
    if len(set(opts)) != len(opts):
        return None
    LP["q"] = {"kind": "value"}
    tags = adj_tags(LP, "CH-V", val_fn, val_fn) + extra_tags + [f"err:{e}" for t, e in oerr.items() if e not in ("gold", "abst")]
    return _finish(card, LP, rng, want, {"qkind": "value", "gold": gold_txt, "options": opts, "opt_err": oerr,
                                        "tags": tags, "k": len(opts), "rank": r, "gold_val": gold})


# ----------------------------------------------------------------------------------------------------------------- CH-O

def _outcome_row(card, rng, var, sem, want, LP):
    m = card["m"]
    outs = card["outs"]
    b1 = sem.get("B1o", card["b1"])
    LP["q"] = {"kind": "outcome", "outs": [{"name": o["name"], "lo": o.get("lo"), "hi": o.get("hi")} for o in outs],
               "b1": b1}
    v = money.compared_value(LP, {})
    gname = money.outcome_of(v, LP["q"]["outs"], b1)
    gi = [o["name"] for o in outs].index(gname)
    tgt = want.get("outcome")
    if tgt is not None and gi != tgt:
        return None
    on_edge = any(v == D(o[k]) for o in outs for k in ("lo", "hi") if o.get(k) is not None)
    # options: gold + outcomes reached by exactly one hook (3.4); rank uniform over edge rank
    shown = card["shown"]
    hk = mcard.hooks(LP, shown | set(LP["sem"]), None)
    reach = {}
    for hv, ids in hk.items():
        try:
            LP2 = dict(LP)
            on = money.outcome_of(hv, LP["q"]["outs"], b1)
        except Reject:
            continue
        if on == gname:
            continue
        reach.setdefault(on, set()).update(ids)
    elig = {n: sorted(ids)[0] for n, ids in reach.items() if len(ids) == 1}
    names = [o["name"] for o in outs]
    _b = [n for n in elig if names.index(n) < gi]
    _a = [n for n in elig if names.index(n) > gi]
    k = want.get("k") or O.held_k(want, [2, 3, 3, 4, 5, 5, 6], O.kmax_all_ranks_list(_b, _a), rng)   # repair r2
    if k is None or k > O.kmax_all_ranks_list(_b, _a):
        return None
    if k < 2:
        return None
    r = want.get("rank")
    if r is None:
        r = O.held_rank(want, k, rng)
    below = [n for n in elig if names.index(n) < gi]
    above = [n for n in elig if names.index(n) > gi]
    if r > len(below) or k - 1 - r > len(above):
        return None
    pick = rng.sample(below, r) + rng.sample(above, k - 1 - r)
    chosen = sorted(pick + [gname], key=names.index)
    disp = card["out_disp"]
    opts = [disp[names.index(n)] for n in chosen]
    oerr = {disp[names.index(n)]: elig[n] for n in pick}
    gold_txt = disp[gi]
    oerr[gold_txt] = "gold"
    tags = adj_tags(LP, "CH-O", lab_of, val_fn) + [f"err:{e}" for t, e in oerr.items() if e != "gold"]
    tags += [f"b1:{b1}", "named:" + card["named"]]
    if on_edge:
        tags.append("boundary:at")
    return _finish(card, LP, rng, want, {"qkind": "outcome", "gold": gold_txt, "options": opts, "opt_err": oerr,
                                        "tags": tags, "k": len(opts), "rank": r, "outcome_idx": gi,
                                        "on_edge": on_edge})


# ----------------------------------------------------------------------------------------------------------------- CL

CASE_KEYS = ("qty", "amt", "fact")


def _case_fields(card):
    """Labels that vary per case: the line quantity (or stated amount) and the exception condition facts."""
    m = card["m"]
    keys = []
    for ln in m["lines"]:
        keys.append(ln["q"] if ln["p"] in ("mul", "perk") else ln["a"])
    for e in m["excs"]:
        for c in e["conds"]:
            if c["f"] not in keys:
                keys.append(c["f"])
    return keys


def _prim_val(cv, keys):
    """The case's first value column (the visible primary scalar of a case line)."""
    for k_ in keys:
        v = cv.get(k_)
        if v is not None and not isinstance(v, (str, bool)):
            try:
                return D(v)
            except Exception:
                continue
    return None


def _cl_row(card, rng, var, sem, want, vals, facts):
    """Inverted case list: exactly one case meets the question's comparison under the card's rules, or none
    ("None of the listed" gold); every other case meets it under exactly one named error (3.4)."""
    m = card["m"]
    keys = _case_fields(card)
    n_want = want["ncases"]
    show_none = card.get("none_ok", False)
    base = mcard.make_lp(card, vals, facts, {"kind": "value"}, sem)
    shown = card["shown"]
    readings = mcard.alt_readings(base, shown | set(base["sem"])) + mcard.error_readings(base)
    if not readings:
        return None
    unit = m["unit"]

    def case_draw():
        v2, f2 = mcard.draw(card, rng)
        cv = {kk: v2[kk] for kk in keys if kk in v2}
        cf = {kk: f2[kk] for kk in keys if kk in f2}
        L2 = {**base, "vals": {**base["vals"], **cv}, "facts": {**base["facts"], **cf}}
        return cv, cf, L2

    pool = []
    seen_keys = set()
    for _ in range(min(900, max(250, 35 * n_want))):
        cv, cf, L2 = case_draw()
        key = (tuple(sorted((k_, str(v_)) for k_, v_ in cv.items())), tuple(sorted(cf.items())))
        if key in seen_keys:
            continue
        try:
            if not grid_ok(L2, card, shown):
                continue
            vg = money.compared_value(L2, {})
            hv = {}
            for eid, rd in readings:
                try:
                    hv[eid] = money.compared_value(L2, rd)
                except (Reject, ArithmeticError, ValueError, money.Unknown):
                    pass
            _, trx = _final(L2)
            if trx.ops > 2 or trx.sel > 3:
                continue
            seen_keys.add(key)
            pool.append((cv, cf, vg, hv, trx.ops))
        except (Reject, ArithmeticError):
            continue
    if pool:
        from collections import Counter as _C
        top = _C(p[4] for p in pool).most_common(1)[0][0]
        pool = [p for p in pool if p[4] == top]
    if len(pool) < 20:
        return None
    combos = [(op, qq) for op in ("gt", "ge", "lt", "le") for qq in (0.5, 0.6, 0.7, 0.8, 0.9)]
    rng.shuffle(combos)
    step = unit * 10
    for op, qq in combos[:10]:
        gv = sorted(p[2] for p in pool)
        T = gv[int(len(gv) * (qq if op in ("gt", "ge") else 1 - qq))]
        T = quant(T, step, "half_up")
        if T <= 0:
            continue
        C = money.CMP[op]

        def kind_of(p):
            if C(p[2], T):
                return "gold"
            hits = [e for e, x in p[3].items() if C(x, T)]
            return hits[0] if len(hits) == 1 else None
        kinds_ = [kind_of(p) for p in pool]
        golds = [p for p, kd in zip(pool, kinds_) if kd == "gold"]
        errs = [(p, kd) for p, kd in zip(pool, kinds_) if kd not in (None, "gold")]
        # case count: the drawn target, or fewer (never below 5) when the rules support fewer single-error cases
        n = min(n_want, len(errs))
        if n < 5:
            continue
        gold_none = show_none and want["u_none"] < O.abst_p("none", n + 1)   # repair r2
        if not gold_none and not golds:
            continue
        need_err = n - (0 if gold_none else 1)
        if len(errs) < need_err:
            continue
        # repair r1.1: the gold case's rank on the first value column is held uniform (matched case lists)
        pr = None
        if not gold_none:
            pr = O.pick_cases_ranked(rng, golds, errs, need_err, O.case_target(want, n), lambda p: _prim_val(p[0], keys))
            if pr is None and O.case_strict(want):
                continue
        # spread the distractors over the error types (round robin by type)
        by = {}
        for p, kd in errs:
            by.setdefault(kd, []).append(p)
        for lst in by.values():
            rng.shuffle(lst)
        order = sorted(by)
        rng.shuffle(order)
        cases = []
        while len(cases) < need_err:
            moved = False
            for kd in order:
                if by[kd] and len(cases) < need_err:
                    p = by[kd].pop()
                    cases.append({"vals": p[0], "facts": p[1], "err": kd})
                    moved = True
            if not moved:
                break
        if len(cases) < need_err:
            continue
        if pr is not None:
            g_, picked = pr
            cases = [{"vals": p[0], "facts": p[1], "err": kd} for p, kd in picked]
            cases.append({"vals": g_[0], "facts": g_[1], "err": "gold"})
        elif not gold_none:
            p = rng.choice(golds)
            cases.append({"vals": p[0], "facts": p[1], "err": "gold"})
        rng.shuffle(cases)
        refs = card["case_refs"](n, rng)
        for c, ref in zip(cases, refs):
            c["ref"] = ref
        LP = dict(base)
        LP["vals"] = {kk: v for kk, v in base["vals"].items() if kk not in keys}
        LP["facts"] = {kk: v for kk, v in base["facts"].items() if kk not in keys}
        LP["q"] = {"kind": "cases", "cmp": op, "T": T, "cases": [{"vals": c["vals"], "facts": c["facts"]} for c in cases]}
        hits = case_hits(LP, {})
        if gold_none:
            if hits:
                continue
            gold_txt = card["none_text"]
        else:
            if len(hits) != 1:
                continue
            gold_txt = cases[hits[0]]["ref"]
        opts = [c["ref"] for c in cases] + ([card["none_text"]] if show_none else [])
        oerr = {c["ref"]: c["err"] for c in cases}
        if show_none:
            oerr[card["none_text"]] = "gold" if gold_none else "abst"
        groups, depths, sels = set(), [], []
        for c in cases:
            L2 = {**base, "vals": {**base["vals"], **c["vals"]}, "facts": {**base["facts"], **c["facts"]}}
            v, tr = _final(L2)
            groups.add("a" if tr.ops == 1 else "b" if tr.ops == 2 else "d")
            depths.append(tr.ops)
            sels.append(tr.sel)
        if len(groups) != 1 or max(depths) > 2 or max(sels) > 3:
            return None
        tags = [f"err:{c['err']}" for c in cases if c["err"] != "gold"] + [f"cases:{n}", "cmp:" + ("incl" if op in ("ge", "le") else "excl")]
        if show_none:
            tags.append("abst:none")
        return {"LP": LP, "qkind": "cases", "gold": gold_txt, "options": opts, "opt_err": oerr, "tags": tags,
                "k": len(opts), "cases": cases, "op": op, "T": T, "group": groups.pop(), "depth": max(depths),
                "ops": max(depths), "sel": max(sels), "deep": False, "printed": set(), "case_keys": keys}
    return None


# ----------------------------------------------------------------------------------------------------------------- open world

def _open_row(card, rng, var, sem, want, LP):
    """Open-world choice row: exactly one case fact is 'not recorded' (the card's unknown field); it is needed (on a
    decision path, NEI gold) with probability 1/k, else inert (off every path) and NEI is shown and wrong."""
    m = card["m"]
    uf = card["unknown_field"]
    dom = card["unknown_dom"]
    schema = card["schema"]
    k = want["k"]
    needed = want["needed"]
    # completions
    outs = []
    for x in dom:
        L2 = {**LP, "facts": {**LP["facts"], uf: x}}
        try:
            if not grid_ok(L2, card, card["shown"]):
                return None
            if schema == "CH-V":
                outs.append(money.evaluate(L2, {})[0])
            else:
                L2["q"] = {"kind": "outcome", "outs": card["outs_q"], "b1": sem.get("B1o", card["b1"])}
                outs.append(money.outcome_of(money.compared_value(L2, {}), card["outs_q"], L2["q"]["b1"]))
        except (Reject, ArithmeticError):
            return None
    distinct = list(dict.fromkeys(outs))
    gates = set()
    for x in dom:
        L2 = {**LP, "facts": {**LP["facts"], uf: x}}
        gates.add(tuple(money.applicable(L2, {})))
    on_path = len(gates) > 1
    if on_path and len(distinct) < 2:
        return None          # on a decision path but the label is fixed: not generated in round 1 (3.5)
    if needed and len(distinct) < 2:
        return None
    if not needed and (on_path or len(distinct) != 1):
        return None
    LP["facts"] = {**LP["facts"], uf: "not recorded"}
    LP["world"] = "open"
    nei = card["nei"]
    if needed:
        if len(distinct) < k - 1:
            return None
        vals = rng.sample(distinct, k - 1)
        if schema == "CH-V":
            vals = sorted(vals)
            opts = [mcard.mstr(v, card) for v in vals]
        else:
            names = [o["name"] for o in card["outs"]]
            vals = sorted(vals, key=names.index)
            opts = [card["out_disp"][names.index(v)] for v in vals]
        opts.append(nei)
        oerr = {o: "E-assume" for o in opts[:-1]}
        oerr[nei] = "gold"
        gold_txt = nei
        LP["q"] = {"kind": "value"} if schema == "CH-V" else {"kind": "outcome", "outs": card["outs_q"],
                                                                "b1": sem.get("B1o", card["b1"])}
        tags = ["nei:needed", "abst:nei", "world:open"] + ["err:E-assume"] * (k - 1)
        return {"LP": LP, "qkind": "value" if schema == "CH-V" else "outcome", "gold": gold_txt, "options": opts,
                "opt_err": oerr, "tags": tags, "k": len(opts), "group": "a", "depth": 1, "ops": 1, "sel": 0,
                "deep": False, "printed": set(), "nei": "needed", "_needs_depth": True}
    # inert: determined value; options = gold + single-hook values (ranked) + NEI
    LPd = {**LP, "facts": {**LP["facts"], uf: dom[0]}, "world": "closed"}
    if schema == "CH-V":
        gold = money.evaluate(LPd, {})[0]
        hk = mcard.hooks(LPd, card["shown"] | set(LPd["sem"]), gold)
        single = O.single_hook_values(hk)
        k_ord = k - 1
        if k_ord > O.kmax_all_ranks(gold, single):          # repair r2: accept on every rank, never the drawn one
            return None
        r = O.held_rank(want, k_ord, rng)
        pr = O.pick_ranked(rng, gold, single, k_ord, r)
        if pr is None:
            return None
        vals_ord, errs = pr
        opts = [mcard.mstr(v, card) for v in vals_ord] + [nei]
        oerr = {mcard.mstr(v, card): errs[v] for v in errs}
        gold_txt = mcard.mstr(gold, card)
        oerr[gold_txt] = "gold"
        oerr[nei] = "abst"
        LP["q"] = {"kind": "value"}
        qk = "value"
    else:
        names = [o["name"] for o in card["outs"]]
        gname = distinct[0]
        gi = names.index(gname)
        LPd["q"] = {"kind": "outcome", "outs": card["outs_q"], "b1": sem.get("B1o", card["b1"])}
        hk = mcard.hooks(LPd, card["shown"] | set(LPd["sem"]), None)
        reach = {}
        for hv, ids in hk.items():
            try:
                on = money.outcome_of(hv, card["outs_q"], LPd["q"]["b1"])
            except Reject:
                continue
            if on != gname:
                reach.setdefault(on, set()).update(ids)
        elig = {n_: sorted(ids)[0] for n_, ids in reach.items() if len(ids) == 1}
        k_ord = k - 1
        below = [n_ for n_ in elig if names.index(n_) < gi]
        if k_ord > O.kmax_all_ranks_list(below, [n_ for n_ in elig if names.index(n_) > gi]):   # repair r2
            return None
        r = O.held_rank(want, k_ord, rng)
        above = [n_ for n_ in elig if names.index(n_) > gi]
        if r > len(below) or k_ord - 1 - r > len(above):
            return None
        pick = rng.sample(below, r) + rng.sample(above, k_ord - 1 - r)
        chosen = sorted(pick + [gname], key=names.index)
        opts = [card["out_disp"][names.index(n_)] for n_ in chosen] + [nei]
        oerr = {card["out_disp"][names.index(n_)]: elig[n_] for n_ in pick}
        gold_txt = card["out_disp"][gi]
        oerr[gold_txt] = "gold"
        oerr[nei] = "abst"
        LP["q"] = LPd["q"]
        qk = "outcome"
    tags = ["nei:inert", "abst:nei", "world:open"] + [f"err:{e}" for e in oerr.values() if e not in ("gold", "abst")]
    return {"LP": LP, "qkind": qk, "gold": gold_txt, "options": opts, "opt_err": oerr, "tags": tags, "k": len(opts),
            "group": "a", "depth": 1, "ops": 1, "sel": 0, "deep": False, "printed": set(), "nei": "inert",
            "_needs_depth": True}
