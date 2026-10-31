"""S4 row generation: YN-D (on time / late), CH-D (last allowed day), CH-C (day counts), CH-O (date windows), CL (which
case missed its deadline), open-world CH-D / CH-O (an extension fact 'not recorded')."""
from __future__ import annotations

import random

import copy
import datetime as dt

from . import dateeval as DE, dcard, options as O
from .money import Reject, gate_true

DAY = dt.timedelta(days=1)


def var_sem(card, var):
    sem = dict(card["d"]["sem"])
    if var:
        sem.update(card["variants"][var - 1]["over"])
    return sem


def _ops(LP):
    tr = DE.trace(LP)
    return tr


def adj_tags(LP, lab):
    tests = []
    r = LP["rule"]
    if r.get("ext"):
        tests.append(("ext", {"err": "E-ext"}))
    if LP.get("holidays"):
        tests.append(("hol", {"err": "E-hol"}))
    if "D7" in LP["sem"]:
        tests.append(("roll", {"sem": {"D7": "none"}}))
    if r["kind"] == "month":
        tests.append(("clamp", {"err": "E-eom:overflow"}))
    tags = []
    try:
        l0 = lab(LP, {})
        v0 = DE.count(LP)[0] if LP["q"]["kind"] == "count" else DE.last_day(LP)[0]
    except Reject:
        return tags
    for x, rd in tests:
        tags.append(f"has:{x}")
        try:
            if lab(LP, rd) != l0:
                tags.append(f"dec:{x}")
            v1 = DE.count(LP, rd)[0] if LP["q"]["kind"] == "count" else DE.last_day(LP, rd)[0]
            if v1 != v0:
                tags.append(f"bind:{x}")
        except Reject:
            pass
    return tags


_SWEEP = None


def _finish(card, LP, extra):
    tr = _ops(LP)
    ops = tr.ops
    if _SWEEP and ops != _SWEEP:
        raise Reject("sweep depth")
    grp = "a" if ops == 1 else "b" if ops == 2 else "d" if ops <= (5 if _SWEEP else 4) else None
    if grp is None:
        raise Reject("too deep")
    out = {"LP": LP, "group": grp, "depth": ops, "ops": ops, "sel": tr.sel, "deep": grp == "d", "printed": set()}
    out.update(extra)
    return out


def gen_row(card, rng, var=0, want=None):
    from .mgen import predraw
    want = predraw(card, rng, dict(want or {}))
    sch = card["schema"]
    global _SWEEP
    _SWEEP = want.get("sweep")
    for attempt in range(300):
        want["_attempt"] = attempt
        try:
            if sch == "YN-D":
                r = _yn(card, rng, var, want)
            elif sch == "CL":
                r = _cl(card, rng, var, want)
            elif card["world"] == "open":
                r = _open(card, rng, var, want)
            elif sch == "CH-C":
                r = _count(card, rng, var, want)
            elif sch == "CH-O":
                r = _window(card, rng, var, want)
            else:
                r = _lastday(card, rng, var, want)
            if r is not None:
                return r
        except Reject:
            continue
    raise Reject(f"no date row ({card['card_id']})")


def _base(card, rng, var, q):
    sem = var_sem(card, var)
    d = dcard.draw(card, rng)
    dates = {card["d"]["evt"]: d["ev"], card["d"]["act"]: d["ev"]}
    LP = dcard.make_lp(card, d, dates, q, sem)
    return LP, d


def _hol_ok(LP, deep_ok=None):
    """Non-deep rows: N <= 10 and at most one listed holiday inside a business-day addition window (R1-13)."""
    r = LP["rule"]
    if deep_ok is None:
        deep_ok = bool(_SWEEP and _SWEEP >= 2)
    if r["kind"] != "bday" or deep_ok:
        return True
    ev = LP["dates"][LP["evt"]]
    L = DE.add_bdays(ev, r["N"], set(LP["holidays"]))
    return sum(1 for h in LP["holidays"] if ev < h <= L) <= 1


def _yn(card, rng, var, want):
    neg = want.get("neg", 0)
    rs = random.Random(want["u_side"]) if "u_side" in want else rng     # repair r1.1: held label-side draws
    kind = want.get("ykind") or rs.choice(["ontime", "late"])
    aff = want["aff"] if "aff" in want else (rng.random() < card["yes_rate"])
    on = aff if kind == "ontime" else (not aff)
    LP, d = _base(card, rng, var, {"kind": kind, "neg": neg})
    if not _hol_ok(LP):
        return None
    L, tr = DE.last_day(LP)
    ev = d["ev"]
    if on:
        act = L if rng.random() < 0.6 else L - DAY * rng.randint(1, 3)
    else:
        act = L + DAY if rng.random() < 0.6 else L + DAY * rng.randint(2, 4)
    if act <= ev:
        return None
    LP["dates"][LP["act"]] = act
    if DE.answer(LP) != aff:
        return None
    tags = adj_tags(LP, lambda L_, rd: DE.answer(L_, rd))
    dd = (act - L).days
    tags += ["cmp:date", "boundary:at" if dd == 0 else ("boundary:above1" if dd == 1 else
                                                         "boundary:below1" if dd == -1 else "boundary:far")]
    return _finish(card, LP, {"qkind": kind, "aff": aff, "neg": neg, "gold": aff ^ (neg % 2 == 1), "tags": tags,
                              "placement": {"near": abs(dd) <= 1, "delta": dd}})


def _date_options(card, LP, rng, gold, readings_fn, k=None, want=None):
    hk = {}
    for eid, rd in readings_fn(LP):
        try:
            v = DE.answer(LP, rd)
        except (Reject, ValueError):
            continue
        if v != gold:
            hk.setdefault(v, []).append(eid)
    single = O.single_hook_values(hk)
    _km = min(1 + len(single), O.kmax_all_ranks(gold, single))   # repair r2
    if k is not None:
        if k > _km:
            return None
    else:
        k = O.held_k(want, [2, 3, 4, 4, 5, 5, 6, 6, 7], _km, rng)
        if k is None:
            return None
    if k < 2:
        return None
    r = O.held_rank(want, k, rng)
    pr = O.pick_ranked(rng, gold, single, k, r)
    if pr is None:
        return None
    return pr, r


def _lastday(card, rng, var, want):
    LP, d = _base(card, rng, var, {"kind": "lastday"})
    if not _hol_ok(LP):
        return None
    L, tr = DE.last_day(LP)
    LP["dates"].pop(LP["act"], None)
    res = _date_options(card, LP, rng, L, lambda L_: dcard.alt_readings(L_, card["shown"]), k=want.get("k"), want=want)
    if res is None:
        return None
    (vals, errs), r = res
    opts = [dcard.dstr(card, v, wd=False) for v in vals]
    oerr = {dcard.dstr(card, v, wd=False): e for v, e in errs.items()}
    gold = dcard.dstr(card, L, wd=False)
    oerr[gold] = "gold"
    tags = adj_tags(LP, lambda L_, rd: DE.answer(L_, rd)) + [f"err:{e}" for e in errs.values()]
    out = _finish(card, LP, {"qkind": "lastday", "gold": gold, "options": opts, "opt_err": oerr, "tags": tags,
                             "k": len(opts), "rank": r, "opt_dates": vals})
    return out


def _count(card, rng, var, want):
    s = card["d"]
    LP, d = _base(card, rng, var, {"kind": "count"})
    ev = d["ev"]
    d2 = ev + DAY * rng.randint(2, 31)
    LP["dates"][LP["act"]] = d2
    n, tr = DE.count(LP)
    hk = {}
    for eid, rd in dcard.alt_readings(LP, card["shown"]):
        try:
            v = DE.count(LP, rd)[0]
        except Reject:
            continue
        if v != n:
            hk.setdefault(v, []).append(eid)
    single = O.single_hook_values(hk)
    k = O.held_k(want, [2, 3, 4, 5], min(1 + len(single), O.kmax_all_ranks(n, single)), rng)   # repair r2
    if k is None:
        return None
    if k < 2:
        return None
    r = O.held_rank(want, k, rng)
    pr = O.pick_ranked(rng, n, single, k, r)
    if pr is None:
        return None
    vals, errs = pr
    unit = "calendar days" if s["ckind"] == "cal" else "business days"
    fmt = lambda x: f"{x} {unit}"   # noqa: E731
    opts = [fmt(v) for v in vals]
    oerr = {fmt(v): e for v, e in errs.items()}
    oerr[fmt(n)] = "gold"
    tags = adj_tags(LP, lambda L_, rd: DE.count(L_, rd)[0]) + [f"err:{e}" for e in errs.values()]
    return _finish(card, LP, {"qkind": "count", "gold": fmt(n), "options": opts, "opt_err": oerr, "tags": tags,
                              "k": len(opts), "rank": r})


def _window(card, rng, var, want):
    s = card["d"]
    LP, d = _base(card, rng, var, {"kind": "window"})
    if not _hol_ok(LP):
        return None
    L, tr = DE.last_day(LP)
    wins = s["windows"]
    ti = want.get("win", rng.randrange(len(wins)))
    w = wins[ti]
    lo = w.get("lo")
    hi = w.get("hi")
    sem = LP["sem"]
    cands = []
    for e in [x for x in (lo, hi) if x is not None]:
        for dd in (e - 1, e, e + 1):
            cands.append(L + DAY * dd)
    a = (lo if lo is not None else -3)
    b = (hi if hi is not None else (lo or 0) + 10)
    for _ in range(4):
        cands.append(L + DAY * rng.randint(a, max(a, b)))
    rng.shuffle(cands)
    act = None
    for c in cands:
        if c <= d["ev"]:
            continue
        try:
            if DE.window_of(LP, L, c) == w["name"]:
                act = c
                break
        except Reject:
            continue
    if act is None:
        return None
    LP["dates"][LP["act"]] = act
    gname = w["name"]
    names = [x["name"] for x in wins]
    reach = {}
    for eid, rd in dcard.alt_readings(LP, card["shown"]):
        try:
            v = DE.answer(LP, rd)
        except Reject:
            continue
        if v != gname:
            reach.setdefault(v, set()).add(eid)
    elig = {n_: sorted(ids)[0] for n_, ids in reach.items() if len(ids) == 1}
    gi = names.index(gname)
    _km = O.kmax_all_ranks_list([n_ for n_ in elig if names.index(n_) < gi], [n_ for n_ in elig if names.index(n_) > gi])
    if want.get("k"):
        k = want["k"]
        if k > _km:                                      # repair r2
            return None
    else:
        k = O.held_k(want, [2, 3, 3, 4], _km, rng)
        if k is None:
            return None
    if k < 2:
        return None
    r = O.held_rank(want, k, rng)
    below = [n_ for n_ in elig if names.index(n_) < gi]
    above = [n_ for n_ in elig if names.index(n_) > gi]
    if r > len(below) or k - 1 - r > len(above):
        return None
    pick = rng.sample(below, r) + rng.sample(above, k - 1 - r)
    chosen = sorted(pick + [gname], key=names.index)
    oerr = {n_: elig[n_] for n_ in pick}
    oerr[gname] = "gold"
    edges = [L + DAY * x for ww in wins for x in (ww.get("lo"), ww.get("hi")) if x is not None]
    on_edge = act in edges
    tags = adj_tags(LP, lambda L_, rd: DE.answer(L_, rd)) + [f"err:{e}" for e in oerr.values() if e != "gold"]
    tags += ["b1:" + sem.get("B1w", "upper"), "named:plain"] + (["boundary:at"] if on_edge else [])
    return _finish(card, LP, {"qkind": "window", "gold": gname, "options": chosen, "opt_err": oerr, "tags": tags,
                              "k": len(chosen), "rank": r, "edge_dates": edges})


def _cl(card, rng, var, want):
    """Which case missed its deadline: exactly one case is late under the card's rules (or none, 'None of the
    listed' gold); every other case is late under exactly one named error. Cases share the holiday line."""
    s = card["d"]
    sem = var_sem(card, var)
    n = want["ncases"]
    show_none = card.get("none_ok", False)
    k = n + (1 if show_none else 0)
    gold_none = want["gold_none"]
    d0 = dcard.draw(card, rng)
    base_ev = d0["ev"]
    q = {"kind": "late", "neg": 0}
    keys = [s["evt"], s["act"]] + ([c["f"] for c in s["ext"]["conds"]] if s["ext"] else [])
    base = dcard.make_lp(card, d0, {s["evt"]: base_ev, s["act"]: base_ev}, q, sem)
    readings = dcard.alt_readings(base, card["shown"])
    # repair r1.1: cases come from one drawn pool (gold-capable cases and single-error cases); the gold case's rank
    # on its visible gap (action date minus event date, in days) among the listed cases is held uniform (matched
    # case lists; v1.0 drew cases one by one and the gold case was the extreme on 77% of case-list rows)
    pool_g, pool_e = [], []
    used = set()
    need_err = n - (0 if gold_none else 1)
    for t in range(max(400, 60 * n)):
        ev = base_ev + DAY * rng.randint(0, max(6, n + 4))
        facts = {}
        if s["ext"]:
            for c in s["ext"]["conds"]:
                facts[c["f"]] = rng.choice(c["dom"])
        L2 = {**base, "dates": {s["evt"]: ev, s["act"]: ev}, "facts": facts}
        try:
            if not _hol_ok(L2):
                continue
            L, tr = DE.last_day(L2)
        except Reject:
            continue
        act = L + DAY * rng.choice([-2, -1, 0, 0, 1, 1, 2, 3])
        if act <= ev or (ev, act) in used:
            continue
        L2["dates"][s["act"]] = act
        late = DE.answer(L2)
        try:
            ops_ = DE.trace(L2).ops
        except Reject:
            continue
        pay = {"dates": dict(L2["dates"]), "facts": facts, "_ops": ops_}
        if late:
            if len(pool_g) < 40:
                pool_g.append(pay)
                used.add((ev, act))
            continue
        hits = []
        for eid, rd in readings:
            try:
                if DE.answer(L2, rd):
                    hits.append(eid)
            except Reject:
                continue
        if len(hits) == 1:
            pool_e.append((pay, hits[0]))
            used.add((ev, act))
        if len(pool_g) >= 40 and len(pool_e) >= 8 * n:
            break
    gp = O.one_group(rng, pool_g, pool_e, need_err, not gold_none,
                     lambda p_: (None if p_["_ops"] > 2 else ("a" if p_["_ops"] == 1 else "b")))
    if gp is None:
        return None
    pool_g, pool_e = gp
    prim = lambda p_: (p_["dates"][s["act"]] - p_["dates"][s["evt"]]).days
    pr = None
    if not gold_none:
        pr = O.pick_cases_ranked(rng, pool_g, pool_e, need_err, O.case_target(want, n), prim)
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
    rng.shuffle(cases)
    refs = card["case_refs"](n, rng)
    for c, ref in zip(cases, refs):
        c["ref"] = ref
    LP = dict(base)
    LP["dates"] = {}
    LP["facts"] = {}
    LP["q"] = {"kind": "cases", "cases": [{"dates": c["dates"], "facts": c["facts"]} for c in cases]}
    hits = []
    for i, c in enumerate(cases):
        L2 = {**base, "dates": c["dates"], "facts": c["facts"], "q": {"kind": "late", "neg": 0}}
        if DE.answer(L2):
            hits.append(i)
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
    groups, depths = set(), []
    for c in cases:
        L2 = {**base, "dates": c["dates"], "facts": c["facts"], "q": {"kind": "late", "neg": 0}}
        tr = DE.trace(L2)
        groups.add("a" if tr.ops == 1 else "b" if tr.ops == 2 else "d")
        depths.append(tr.ops)
    if len(groups) != 1 or max(depths) > 2:
        return None
    tags = [f"err:{c['err']}" for c in cases if c["err"] != "gold"] + [f"cases:{n}", "cmp:date"]
    if show_none:
        tags.append("abst:none")
    return {"LP": LP, "qkind": "cases", "gold": gold_txt, "options": opts, "opt_err": oerr, "tags": tags, "k": len(opts),
            "cases": cases, "group": groups.pop(), "depth": max(depths), "ops": max(depths), "sel": 0, "deep": False,
            "printed": set(), "case_keys": keys}


def _open(card, rng, var, want):
    """Open-world CH-D / CH-O: the extension's first condition field is 'not recorded'."""
    s = card["d"]
    ext = s["ext"]
    if not ext:
        raise Reject("open card without extension")
    uf = ext["conds"][0]["f"]
    dom = ext["conds"][0]["dom"]
    k = want["k"]
    needed = want["needed"]
    sch = card["schema"]
    w2 = {**want, "k": k - 1}
    if sch == "CH-O":
        r = _window(card, rng, var, w2)
    else:
        r = _lastday(card, rng, var, w2)
    if r is None:
        return None
    LP = r["LP"]
    outs, gates = [], set()
    for x in dom:
        f2 = {**LP["facts"], uf: x}
        outs.append(DE.answer(LP, {}, facts=f2))
        gates.add(gate_true({"no": 0, "conn": ext["conn"], "join": ext["join"], "conds": LP["rule"]["ext"]["conds"]}, f2, {}, {}))
    distinct = []
    for o in outs:
        if o not in distinct:
            distinct.append(o)
    on_path = len(gates) > 1
    if on_path and len(distinct) < 2:
        return None
    if needed != (len(distinct) >= 2):
        return None
    LP["facts"] = {**LP["facts"], uf: "not recorded"}
    nei = card["nei"]
    if needed:
        kk = k - 1
        if len(distinct) < kk:
            return None
        if sch == "CH-O":
            names = [w["name"] for w in s["windows"]]
            vals = sorted(rng.sample(distinct, kk), key=names.index)
            opts = list(vals)
        else:
            vals = sorted(rng.sample(distinct, kk))
            opts = [dcard.dstr(card, v, wd=False) for v in vals]
        opts.append(nei)
        oerr = {o: "E-assume" for o in opts[:-1]}
        oerr[nei] = "gold"
        r.update({"gold": nei, "options": opts, "opt_err": oerr, "k": len(opts), "nei": "needed",
                  "tags": ["nei:needed", "abst:nei", "world:open"], "opt_dates": vals if sch != "CH-O" else []})
        return r
    if len(r["options"]) + 1 != k:
        return None
    r["options"] = r["options"] + [nei]
    r["opt_err"][nei] = "abst"
    r["k"] = len(r["options"])
    r["nei"] = "inert"
    r["tags"] = r["tags"] + ["nei:inert", "abst:nei", "world:open"]
    return r
