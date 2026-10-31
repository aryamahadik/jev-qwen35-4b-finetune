"""F7 row samplers: unit plans (fact_flip pairs, equiv and inv units, singletons), exact per-card level quotas,
override firing quotas (6.4), case construction per sampler, presentation features (C1 unmentioned, C15 missing, C3
plans, C20 partial facts, C14 repeats, C21 other entity / distractor, inert sentences, Z02 fillers), conv and boundary
edges (3.4, 6.2) and the structure hash.
"""
from __future__ import annotations

import hashlib
import json
import random
from fractions import Fraction

import f7cards as CD
import f7model as M


# ------------------------------------------------------------------------------------------------ card features
def card_atoms(card: dict) -> list[tuple[str, dict]]:
    """(context, atom): context 'up' (level criteria, floors, unless-A, only-if C) or 'down' (caps, unless-B)."""
    out = []

    def walk(c, ctx):
        t = c["t"]
        if t == "atom":
            out.append((ctx, c["a"]))
        elif t in ("and", "or", "allof", "anyof"):
            for p in c["parts"]:
                walk(p, ctx)
        elif t == "unless":
            walk(c["a"], ctx)
            out.append(("down" if ctx == "up" else "up", c["b"]))
        elif t == "onlyif":
            walk(c["main"], ctx)
            out.append((ctx, c["c"]))
    for c in card.get("crits", {}).values():
        walk(c, "up")
    for o in card.get("overrides", []):
        walk(o["cond"], "up" if o["type"] == "floor" else "down")
    for row in card.get("grid", {}).values():
        for a in row:
            out.append(("up", a))
    return out


def crit_kinds(card: dict) -> set:
    ks = set()

    def walk(c):
        ks.add(c["t"])
        if c["t"] in ("and", "or", "allof", "anyof"):
            for p in c["parts"]:
                walk(p)
        elif c["t"] == "unless":
            walk(c["a"])
        elif c["t"] == "onlyif":
            walk(c["main"])
    for c in card.get("crits", {}).values():
        walk(c)
    for o in card.get("overrides", []):
        walk(o["cond"])
    return ks


def c1_eligible(card: dict) -> list[str]:
    """Boolean factors that may be left unmentioned: they occur only as 'present' atoms in up contexts and never in
    an unless part, an only-if part or a cap condition (C1 rule)."""
    bad, good = set(), set()

    def walk(c, ctx, special=False):
        t = c["t"]
        if t == "atom":
            a = c["a"]
            if a["kind"] == "bool":
                if ctx == "up" and a["op"] == "present" and not special:
                    good.add(a["item"])
                else:
                    bad.add(a["item"])
        elif t in ("and", "or", "allof", "anyof"):
            for p in c["parts"]:
                walk(p, ctx, special)
        elif t == "unless":
            walk(c["a"], ctx, special)
            walk({"t": "atom", "a": c["b"]}, ctx, True)
        elif t == "onlyif":
            walk(c["main"], ctx, special)
            walk({"t": "atom", "a": c["c"]}, ctx, True)
    for c in card.get("crits", {}).values():
        walk(c, "up")
    for o in card.get("overrides", []):
        walk(o["cond"], "up" if o["type"] == "floor" else "down", o["type"] == "cap")
    if card["mode"] in ("count", "points"):
        return []
    return sorted(good - bad)


def card_features(card: dict, plan: dict) -> dict:
    ks = crit_kinds(card)
    atoms = [a for _, a in card_atoms(card)]
    incl_words, excl_words = [], []
    for a in atoms:
        if a["kind"] == "num":
            w = CD_word(a)
            (incl_words if a["op"] in (">=", "<=") else excl_words).append(w)
    f = {"and": bool(ks & {"and", "allof"}) or any(c["t"] == "unless" and c["a"]["t"] == "and"
                                                   for c in card.get("crits", {}).values()),
         "or": bool(ks & {"or", "anyof"}), "unless": "unless" in ks, "onlyif": "onlyif" in ks,
         "date": any(a["kind"] == "date" for a in atoms), "ord": any(a["kind"] == "ord" for a in atoms),
         "incl_words": sorted(set(incl_words)), "excl_words": sorted(set(excl_words)),
         "continuous": any(a["kind"] == "num" and not card["items"][a["item"]]["int"] for a in atoms)
         or (card["mode"] == "cut" and not card["integer"]),
         "override": bool(card.get("overrides")), "both": len(card.get("overrides", [])) == 2}
    if card["mode"] in ("count", "points"):
        f["incl_words"] = sorted(set(f["incl_words"]) | {"N or more"} | ({"N or fewer"} if _band_or_fewer(card) else set()))
    if card["mode"] == "cut":
        if card["integer"]:
            f["incl_words"] = sorted(set(f["incl_words"]) | {"N or more"} | ({"N or fewer"} if card.get("low_word") == "or fewer" else set()))
        elif card["side"] == "high":
            f["incl_words"] = ["N or more"]
            f["excl_words"] = ["below N"]
        else:
            f["incl_words"] = ["N or less", "at most N"]
            f["excl_words"] = ["above N"]
    return f


def _band_or_fewer(card):
    return card.get("low_word") == "or fewer"


def CD_word(a: dict) -> str:
    from f7lex import CMP_WORD, EXCL_HI, EXCL_LO, INCL_HI, INCL_LO
    cls = "count" if a.get("count") else "noncount"
    table = {">=": INCL_LO, "<=": INCL_HI, ">": EXCL_LO, "<": EXCL_HI}[a["op"]][cls]
    return CMP_WORD[table[a["wv"] % len(table)]]


# ------------------------------------------------------------------------------------------------ quotas and units
QUOTA_TALLY: dict = {}  # G10 r1c: (sampler, K) -> rows per level over the cards filled so far (reset per run group)


def level_quota(n: int, K: int, rng: random.Random, key=None) -> list[int]:
    """Per-card quota: floor(n / K) or ceil(n / K) rows per level. G10 r1c: the ceil levels go to the levels with the
    fewest rows so far in the card's sampler x K (ties drawn), so small cards (S6) keep each sampler x K level share
    within 1/K +/- 2 pp."""
    base = [n // K] * K
    extra = n - sum(base)
    if key is None:
        picks = rng.sample(range(K), extra)
    else:
        tally = QUOTA_TALLY.setdefault(key, [0] * K)
        order = sorted(range(K), key=lambda i: (tally[i], rng.random()))
        picks = order[:extra]
    for i in picks:
        base[i] += 1
    if key is not None:
        for i in range(K):
            QUOTA_TALLY[key][i] += base[i]
    return base


def plan_units(card: dict, plan: dict, n: int, rng: random.Random, inv_rows: int) -> list[dict]:
    """Units with target gold levels; totals per level are exactly the per-card quota (floor / ceil of n / K)."""
    K = card["K"]
    q = level_quota(n, K, rng, key=(card["sampler"], K))
    rem = list(q)
    units = []
    n_pairs = round(0.115 * n)
    for _ in range(n_pairs):
        cands = [j for j in range(K - 1) if rem[j] > 0 and rem[j + 1] > 0]
        if not cands:
            break
        j = rng.choice(cands)
        up = rng.random() < 0.5
        base, twin = (j, j + 1) if up else (j + 1, j)
        rem[base] -= 1
        rem[twin] -= 1
        units.append({"type": "flip", "levels": [base, twin]})
    n_eq = round(0.10 * n)
    for _ in range(n_eq):
        cands = [j for j in range(K) if rem[j] >= 2]
        if not cands:
            break
        j = rng.choice(cands)
        rem[j] -= 2
        units.append({"type": "equiv", "levels": [j, j]})
    for _ in range(inv_rows):
        cands = [j for j in range(K) if rem[j] >= 2]
        if not cands:
            break
        j = rng.choice(cands)
        rem[j] -= 2
        units.append({"type": "inv", "levels": [j, j]})
    for j in range(K):
        for _ in range(rem[j]):
            units.append({"type": "single", "levels": [j]})
    rng.shuffle(units)
    return units


def override_targets(card: dict, units: list, rng: random.Random) -> None:
    """6.4 R02: per level, ceil(q/2) rows with no override firing, floor(q/2) spread over the patterns whose reachable
    set holds the level; binding 50/50 at the binding-able level of each pattern. Writes unit['ov'] = [(pattern,
    binding) per row]; fact_flip rows never fire a binding override and their changed attribute is no condition item."""
    ovs = card.get("overrides", [])
    if not ovs:
        return
    K = card["K"]
    fl = next((o for o in ovs if o["type"] == "floor"), None)
    cp = next((o for o in ovs if o["type"] == "cap"), None)
    pats = []
    if fl:
        pats.append(("floor", set(range(fl["m"], K))))
    if cp:
        pats.append(("cap", set(range(0, cp["m"] + 1))))
    if fl and cp:
        mw = cp["m"] if card["winner"] == "cap" else fl["m"]
        pats.append(("both", {mw}))
    slots = {}  # level -> list of row slots (unit idx, row idx)
    for ui, u in enumerate(units):
        u["ov"] = [("none", False)] * len(u["levels"])
        for ri, lv in enumerate(u["levels"]):
            slots.setdefault(lv, []).append((ui, ri))
    for lv, sl in slots.items():
        P = [p for p, R in pats if lv in R]
        free = [s for s in sl if units[s[0]]["type"] != "flip"]
        rng.shuffle(free)
        k_fire = len(sl) // 2
        fire = free[:k_fire]
        for i, (ui, ri) in enumerate(fire):
            if not P:
                break
            pat = P[i % len(P)]
            bind_level = {"floor": fl["m"] if fl else None, "cap": cp["m"] if cp else None,
                          "both": (cp["m"] if card.get("winner") == "cap" else fl["m"]) if (fl and cp) else None}[pat]
            binding = (lv == bind_level) and (i // len(P)) % 2 == 0
            units[ui]["ov"] = list(units[ui]["ov"])
            units[ui]["ov"][ri] = (pat, binding)
        # twins of a unit share the base's case: copy the base's pattern
    for u in units:
        if u["type"] in ("equiv", "inv"):
            u["ov"] = [u["ov"][0], u["ov"][0]]


# ------------------------------------------------------------------------------------------------ value construction
def _ov_ok(card: dict, v: dict, pat: str, binding: bool) -> bool:
    if not card.get("overrides"):
        return True
    ff, cf = M.firing(card, v)
    got = "both" if (ff and cf) else "floor" if ff else "cap" if cf else "none"
    if got != pat:
        return False
    b = M.final_level(card, v) != M.mode_level(card, v)
    return b == binding


def _truths(c: dict, want: bool, rng: random.Random, out: list) -> None:
    """Atom truth assignments that make criterion c evaluate to `want` (parts left free are not constrained)."""
    t = c["t"]
    if t == "atom":
        out.append((c["a"], want))
        return
    if t in ("and", "allof"):
        if want:
            for p in c["parts"]:
                _truths(p, True, rng, out)
        else:
            ps = list(c["parts"])
            k = rng.randint(1, len(ps)) if rng.random() < 0.3 else 1
            for p in rng.sample(ps, k):
                _truths(p, False, rng, out)
        return
    if t in ("or", "anyof"):
        if want:
            ps = list(c["parts"])
            k = 1 if rng.random() < 0.6 else rng.randint(1, len(ps))
            for p in rng.sample(ps, k):
                _truths(p, True, rng, out)
        else:
            for p in c["parts"]:
                _truths(p, False, rng, out)
        return
    if t == "unless":
        if want:
            _truths(c["a"], True, rng, out)
            out.append((c["b"], False))
        elif rng.random() < 0.5:
            _truths(c["a"], False, rng, out)
        else:
            out.append((c["b"], True))
        return
    if t == "onlyif":
        if want:
            _truths(c["main"], True, rng, out)
            out.append((c["c"], True))
        elif rng.random() < 0.5:
            _truths(c["main"], False, rng, out)
        else:
            out.append((c["c"], False))
        return
    raise ValueError(t)


def _atom_interval(a: dict, truth: bool, it: dict):
    if a["kind"] == "bool":
        return ("bool", (a["op"] == "present") == truth)
    r = it["r"]
    if a["op"] == "within":
        D, N = a["t"], a["N"]
        return ("iv", (D, D + N)) if truth else ("iv", (D + N + 1, None))
    t = a["t"]
    op = a["op"]
    if not truth:
        op = {">=": "<", ">": "<=", "<=": ">", "<": ">="}[op]
    if op == ">=":
        return ("iv", (t, None))
    if op == ">":
        return ("iv", (t + r, None))
    if op == "<=":
        return ("iv", (None, t))
    return ("iv", (None, t - r))


def construct(card: dict, rng: random.Random, M_target: int, fire: tuple = (None, None), fixed: dict | None = None,
              near_miss: bool = False):
    """Constructive draw: criterion truths for the mode target, override condition truths, then per-item intervals
    intersected and sampled near their ends (boundary bias). Returns values or None on a conflict."""
    K = card["K"]
    req = []
    mode = card["mode"]
    if mode == "ladder":
        for k in range(1, M_target + 1):
            _truths(card["crits"][k], True, rng, req)
        if M_target < K - 1:
            _truths(card["crits"][M_target + 1], False, rng, req)
    elif mode == "highest":
        if M_target >= 1:
            _truths(card["crits"][M_target], True, rng, req)
        for j in range(M_target + 1, K):
            _truths(card["crits"][j], False, rng, req)
    elif mode == "grid":
        if M_target >= 1:
            for a in card["grid"][M_target]:
                req.append((a, True))
        for j in range(M_target + 1, K):
            _truths({"t": "allof", "parts": [{"t": "atom", "a": a} for a in card["grid"][j]]}, False, rng, req)
    if near_miss and mode in ("ladder", "highest") and M_target < K - 1:
        # S2 near-miss (R17): one higher 'and' / 'all of' criterion fails on exactly one part, the others hold
        ks = [k for k in range(M_target + 1, K) if card["crits"][k]["t"] in ("and", "allof")]
        if ks:
            k = rng.choice(ks)
            if mode == "ladder" and k != M_target + 1:
                pass
            c = card["crits"][k]
            req = [(a, t) for a, t in req if not any(a is x for x in M.atoms_of(c))] if mode == "highest" or \
                k == M_target + 1 else req
            off = rng.randrange(len(c["parts"]))
            for i, p_ in enumerate(c["parts"]):
                _truths(p_, i != off, rng, req)
    ff, cf = fire
    for o in card.get("overrides", []):
        want = ff if o["type"] == "floor" else cf
        if want is not None:
            _truths(o["cond"], want, rng, req)
    bounds = {}
    for a, truth in req:
        it = card["items"][a["item"]]
        kind, x = _atom_interval(a, truth, it)
        if kind == "bool":
            if a["item"] in bounds and bounds[a["item"]] != x:
                return None
            bounds[a["item"]] = x
        else:
            lo, hi = bounds.get(a["item"], (it["lo"], it["hi"]))
            nlo = lo if x[0] is None else max(lo, x[0])
            nhi = hi if x[1] is None else min(hi, x[1])
            if nlo > nhi:
                return None
            bounds[a["item"]] = (nlo, nhi)
    v = {}
    ths = CD.collect_thresholds(card)
    for k, it in card["items"].items():
        if fixed and k in fixed:
            v[k] = fixed[k]
            b = bounds.get(k)
            if b is not None:
                if it["kind"] == "bool":
                    if b != fixed[k]:
                        return None
                elif not (b[0] <= fixed[k] <= b[1]):
                    return None
            continue
        if it["kind"] == "bool":
            v[k] = bounds[k] if k in bounds else (rng.random() < 0.5)
            continue
        lo, hi = bounds.get(k, (it["lo"], it["hi"]))
        r = it["r"]
        near = [t + d * r for t in ths.get(k, []) for d in (-1, 0, 1) if lo <= t + d * r <= hi]
        if near and rng.random() < 0.55:
            v[k] = rng.choice(near)
        else:
            steps = int((hi - lo) / r)
            v[k] = lo + rng.randint(0, steps) * r
    return v


def mode_target_for(card: dict, target: int, pat: str, binding: bool, rng: random.Random):
    K = card["K"]
    ovs = card.get("overrides", [])
    fl = next((o for o in ovs if o["type"] == "floor"), None)
    cp = next((o for o in ovs if o["type"] == "cap"), None)
    if pat == "none":
        return target, (False if fl else None, False if cp else None)
    if pat == "floor":
        if binding:
            return rng.randint(0, fl["m"] - 1) if fl["m"] >= 1 else None, (True, False if cp else None)
        return target, (True, False if cp else None)
    if pat == "cap":
        if binding:
            return rng.randint(cp["m"] + 1, K - 1) if cp["m"] < K - 1 else None, (False if fl else None, True)
        return target, (False if fl else None, True)
    mw = cp["m"] if card["winner"] == "cap" else fl["m"]
    if binding:
        cands = [m for m in range(K) if m != mw]
        return rng.choice(cands), (True, True)
    return mw, (True, True)


def sample_lh(card: dict, rng: random.Random, target: int, pat: str = "none", binding: bool = False, check=None,
              fixed: dict | None = None, tries: int = 600, near_miss: bool = False) -> dict | None:
    for i in range(tries):
        Mt, fire = mode_target_for(card, target, pat, binding, rng)
        if Mt is None:
            return None
        v = construct(card, rng, Mt, fire, fixed, near_miss=near_miss and i % 4 != 3)
        if v is None:
            continue
        if M.final_level(card, v) != target:
            continue
        if not _ov_ok(card, v, pat, binding):
            continue
        if check and not check(v):
            continue
        return v
    for i in range(300 if near_miss else 1500):
        v = CD.random_values(card, rng, near=0.55)
        if fixed:
            v.update(fixed)
        if M.final_level(card, v) != target or not _ov_ok(card, v, pat, binding):
            continue
        if check and not check(v):
            continue
        return v
    return None


def sample_count(card: dict, rng: random.Random, target: int, at_cut: bool | None = None,
                 need_absent: bool = False, avoid=None) -> dict | None:
    """G12 r1b: `avoid` = presence vectors (frozensets of present listed items) already used on the card; the draw is
    uniform over the unused subsets (COUNT: count uniform over the counts that still have one, then subset uniform)."""
    lo, hi = card["bands"][target]
    listed = card["listed"]
    m = len(listed)
    avoid = avoid or set()
    if card["mode"] == "count":
        import itertools
        hi2 = min(hi, m)
        vals = list(range(lo, hi2 + 1))
        if avoid:
            vals = [x for x in vals if any(frozenset(sub) not in avoid for sub in itertools.combinations(listed, x))] \
                or vals
        if need_absent and [x for x in vals if x < m]:
            vals = [x for x in vals if x < m]
        if at_cut is not None:
            cutvals = [x for x in vals if _is_cut_value(card, x)]
            if at_cut and cutvals:
                vals = cutvals
            elif at_cut is False and [x for x in vals if x not in cutvals]:
                vals = [x for x in vals if x not in cutvals]
        c = rng.choice(vals)
        free = [sub for sub in itertools.combinations(listed, c) if frozenset(sub) not in avoid]
        on = set(rng.choice(free)) if free else set(rng.sample(listed, c))
        return {f: f in on for f in listed}
    w = card["weights"]
    P = card["P"]
    subs = []
    import itertools
    for r in range(0, min(P, m) + 1):
        for sub in itertools.combinations(listed, r):
            t = sum(w[f] for f in sub)
            if lo <= t <= hi:
                subs.append((t, sub))
    if not subs:
        return None
    if avoid and [s_ for s_ in subs if frozenset(s_[1]) not in avoid]:
        subs = [s_ for s_ in subs if frozenset(s_[1]) not in avoid]
    if need_absent and [s_ for s_ in subs if len(s_[1]) < m]:
        subs = [s_ for s_ in subs if len(s_[1]) < m]
    if at_cut is not None:
        cs = [s for s in subs if _is_cut_value(card, s[0])]
        ns = [s for s in subs if not _is_cut_value(card, s[0])]
        if at_cut and cs:
            subs = cs
        elif at_cut is False and ns:
            subs = ns
    t, sub = rng.choice(subs)
    return {f: f in sub for f in listed}


def _is_cut_value(card: dict, x: int) -> bool:
    bv = card["band_by_value"]
    return any(x == lo for lo, hi in bv[1:])


def place_cut(card: dict, rng: random.Random, target: int, placement: str, cut_idx: int | None,
              avoid=None) -> tuple | None:
    """S6 value for the target level with numeric placement at / below / above a cut, or interior. Values in `avoid`
    (already used on the card; G12 r1: one unit per structure) are never returned."""
    avoid = avoid or ()
    it = card["items"][card["qty"]]
    r = it["r"]
    cuts = card["cuts"]
    K = card["K"]
    j = target if card["rising"] else K - 1 - target  # range index by value
    cands = []
    if placement in ("at", "below", "above"):
        for ci, c in enumerate(cuts):
            x = c + {"at": 0, "below": -r, "above": r}[placement]
            if it["lo"] <= x <= it["hi"] and M.cut_level(card, x) == target and x not in avoid:
                cands.append((ci, x))
        if cut_idx is not None:
            pref = [cx for cx in cands if cx[0] == cut_idx]
            cands = pref or cands
        if not cands:
            return None
        return rng.choice(cands)
    lo = cuts[j - 1] if j >= 1 else it["lo"]
    hi = cuts[j] if j < K - 1 else min(it["hi"], cuts[-1] + (cuts[-1] - cuts[0]) // max(1, K - 2) + 6 * r
                                         if K > 2 else it["hi"])
    xs = []
    steps = int((hi - lo) / r)
    for s in range(2, steps - 1):
        x = lo + s * r
        if all(abs(x - c) > r for c in cuts) and M.cut_level(card, x) == target and it["lo"] <= x <= it["hi"] and \
                x not in avoid:
            xs.append(x)
    if not xs:
        return None
    return (None, rng.choice(xs))


def placement_of(x, t, r) -> str:
    if x == t:
        return "at"
    if x == t - r:
        return "below"
    if x == t + r:
        return "above"
    return "interior"


def int_placement(card: dict, x: int) -> str:
    bv = card["band_by_value"] if card["mode"] in ("count", "points") else None
    if bv is None:
        cuts = card["cuts"]
    else:
        cuts = [lo for lo, hi in bv[1:]]
    if x in cuts:
        return "at"
    if x + 1 in cuts:
        return "below"
    if x - 1 in cuts:
        return "above"
    return "interior"


# ------------------------------------------------------------------------------------------------ conv elements
def conv_elements(card: dict, case: dict, gold: int, pres: dict) -> list[dict]:
    v = case["values"]
    K = card["K"]
    feats = card["features"]
    els = {}

    def add(cid, alt):
        if alt is not None and alt != gold:
            els[(cid, alt)] = 1

    def lvl(vv, rd=None):
        try:
            return M.final_level(card, vv, rd)
        except ValueError:
            return None
    if case.get("unmentioned"):
        v1 = dict(v)
        for f in case["unmentioned"]:
            v1[f] = True
        add("C1", lvl(v1))
    for key, cid in (("plans", "C3"), ("partials", "C20"), ("missing", "C15")):
        if case.get(key):
            v1 = dict(v)
            for f in case[key]:
                v1[f] = True
            add(cid, lvl(v1))
    if feats["unless"]:
        add("C4", lvl(v, {"unless_ignored": True}))
    if feats["onlyif"]:
        add("C5", lvl(v, {"onlyif_as_if": True}))
    if feats["or"]:
        add("C7", lvl(v, {"or_exclusive": True}))
    if any(a["kind"] == "num" and a["op"] in (">=", "<=") for _, a in card_atoms(card)):
        add("C8", lvl(v, {"flip_incl": "incl->excl"}))
    if any(a["kind"] == "num" and a["op"] in (">", "<") for _, a in card_atoms(card)):
        add("C9", lvl(v, {"flip_incl": "excl->incl"}))
    if feats["date"]:
        add("C10", lvl(v, {"flip_incl": "date"}))
        add("C10", lvl(v, {"within_excl": True}))
    if card["mode"] == "cut" and not card["integer"]:
        add("C11", lvl(v, {"side_swap": True}))
    if feats["override"]:
        if feats["both"]:
            add("C13", lvl(v, {"prec_swap": True}))
        add("C13", lvl(v, {"ignore_floor": True}))
        add("C13", lvl(v, {"ignore_cap": True}))
    if case.get("repeats") and card["mode"] in ("count", "points"):
        add("C14", lvl(v, {"count_twice": {f: 2 for f in case["repeats"]}}))
    if card["mode"] in ("ladder", "highest"):
        add("C16", lvl(v, {"mode_swap": True}))
    if card["mode"] == "points":
        add("C16", lvl(v, {"points_as_count": True}))
    if card["mode"] in ("count", "points") and case.get("fillers"):
        cx = dict(card, fillers_on_row=[f"_fill{i}" for i in range(len(case["fillers"]))])
        vv = dict(v)
        for i, fl in enumerate(case["fillers"]):
            vv[f"_fill{i}"] = fl["present"]
        try:
            alt = M.final_level(cx, vv, {"fillers_count": True})
        except ValueError:
            alt = None
        add("C16", alt)
    if card["plan"]["reversed"]:
        add("C17", K - 1 - gold)
    if card["plan"]["name_form"] == "swapped":
        usual = card["levels"]["usual_rank"]
        alt = next(k for k in range(K) if usual[k] == gold)
        add("C19", alt)
    if case.get("distractor"):
        v1 = dict(v)
        k, val = case["distractor"]
        v1[k] = val
        add("C21", lvl(v1))
    if case.get("inject") is not None:
        add("C24", case["inject"])
    if feats["ord"]:
        add("C25", lvl(v, {"rank_swap": True}))
    return [{"kind": "conv", "conv": c, "alt_level": a} for (c, a) in sorted(els)]


# ------------------------------------------------------------------------------------------------ structure hash
def canon_atom(a: dict, idx: dict) -> list:
    if a["op"] in ("present", "absent"):
        return [idx[a["item"]], a["op"]]
    if a["op"] == "within":
        return [idx[a["item"]], "within", str(a["t"]), str(a["N"])]
    return [idx[a["item"]], a["op"], str(a["t"])]


def canon_crit(c: dict, idx: dict):
    t = c["t"]
    if t == "atom":
        return canon_atom(c["a"], idx)
    if t in ("and", "or", "allof", "anyof"):
        return [{"allof": "and", "anyof": "or"}.get(t, t), [canon_crit(p, idx) for p in c["parts"]]]
    if t == "unless":
        return ["unless", canon_crit(c["a"], idx), canon_atom(c["b"], idx)]
    if t == "onlyif":
        return ["onlyif", canon_crit(c["main"], idx), canon_atom(c["c"], idx)]


def item_order(card: dict) -> list[str]:
    seen = []

    def add(k):
        if k not in seen:
            seen.append(k)
    if card["mode"] in ("count", "points"):
        for k in card["listed"]:
            add(k)
    elif card["mode"] == "cut":
        add(card["qty"])
    elif card["mode"] == "grid":
        for k in range(1, card["K"]):
            for a in card["grid"][k]:
                add(a["item"])
    else:
        for k in range(1, card["K"]):
            for a in M.atoms_of(card["crits"][k]):
                add(a["item"])
        for o in card.get("overrides", []):
            for a in M.atoms_of(o["cond"]):
                add(a["item"])
    return seen


def structure_hash(card: dict, values: dict) -> str:
    order = item_order(card)
    idx = {k: i for i, k in enumerate(order)}
    can = {"K": card["K"], "mode": card["mode"]}
    if card["mode"] in ("ladder", "highest"):
        can["crits"] = [canon_crit(card["crits"][k], idx) for k in range(1, card["K"])]
        can["ov"] = sorted([[o["type"], canon_crit(o["cond"], idx), o["m"]] for o in card.get("overrides", [])])
        if len(card.get("overrides", [])) == 2:
            can["winner"] = card["winner"]
    elif card["mode"] in ("count", "points"):
        can["bands"] = [[lo, hi if hi < CD.OPEN_TOP else None] for lo, hi in card["bands"]]
        if card["mode"] == "points":
            can["w"] = [card["weights"][k] for k in order]
    elif card["mode"] == "cut":
        can["ranges"] = cut_intervals(card)
    elif card["mode"] == "grid":
        can["grid"] = [[canon_atom(a, idx) for a in card["grid"][k]] for k in range(1, card["K"])]
    can["v"] = [str(values.get(k)) for k in order]
    return hashlib.sha256(json.dumps(can, sort_keys=True).encode()).hexdigest()[:32]


def cut_intervals(card: dict) -> list:
    """Canonical CUT ranges per level index: [lo, lo_incl, hi, hi_incl] (None when unbounded); on integer cards the
    smallest-value range has lo None whatever its printed form."""
    K = card["K"]
    cuts = card["cuts"]
    out = []
    for k in range(K):
        j = k if card["rising"] else K - 1 - k
        if card["integer"]:
            lo = cuts[j - 1] if j >= 1 else None
            hi = cuts[j] - 1 if j < K - 1 else None
            out.append([None if lo is None else str(Fraction(lo)), None if lo is None else True,
                        None if hi is None else str(Fraction(hi)), None if hi is None else True])
        else:
            hs = card["side"] == "high"
            lo = cuts[j - 1] if j >= 1 else None
            hi = cuts[j] if j < K - 1 else None
            out.append([None if lo is None else str(Fraction(lo)), None if lo is None else hs,
                        None if hi is None else str(Fraction(hi)), None if hi is None else (not hs)])
    return out
