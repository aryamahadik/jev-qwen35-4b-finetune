"""F7 case construction per sampler: values for a target level (label-first or by rejection), boundary placement
(S2, S3, S6), presentation features, facts list, twins (fact_flip, equiv, inv) and worked cases.
"""
from __future__ import annotations

import random
from fractions import Fraction

import f7cards as CD
import f7lex as LX
import f7model as M
import f7rows as RW


class CaseFail(Exception):
    pass


def new_name(card: dict, rng: random.Random, used: set) -> str:
    ids = card["ids"]
    for _ in range(2000):
        i = rng.choice(ids)
        if i not in used:
            used.add(i)
            return f"{card['singular'][0].upper()}{card['singular'][1:]} {i}"
    raise CaseFail("ids exhausted")


# ------------------------------------------------------------------------------------------------ values per sampler
S2_END_BOOL_P = 0.5  # r1g: share of end-level S2 rows that take the "one condition" boundary when available


def values_for(card: dict, target: int, rng: random.Random, ctx: dict) -> tuple[dict, dict]:
    """(values, info) for the target level. info carries boundary placement and override pattern facts."""
    mode = card["mode"]
    s = card["sampler"]
    info = {}
    if mode in ("count", "points"):
        at_cut = ctx.get("at_cut")
        v = RW.sample_count(card, rng, target, at_cut, need_absent=bool(ctx.get("missing_want")),
                            avoid=ctx.get("avoid_vecs"))
        if v is None:
            raise CaseFail("count")
        tot = M.count_total(card, v)
        info["boundary"] = {"kind": "boundary", "placement": RW.int_placement(card, tot), "cmp": "closed"}
        return v, info
    if mode == "cut":
        pl = ctx.get("placement", "interior")
        got = RW.place_cut(card, rng, target, pl, ctx.get("cut_idx"), avoid=ctx.get("avoid_vals"))
        if got is None and pl != "interior":
            got = RW.place_cut(card, rng, target, "interior", None, avoid=ctx.get("avoid_vals"))
            pl = "interior"
        if got is None:
            raise CaseFail("cut")
        ci, x = got
        it = card["items"][card["qty"]]
        if card["integer"]:
            placement = RW.int_placement(card, x)
            cmp = "closed"
        else:
            placement = pl if ci is not None else "interior"
            cmp = "side_high" if card["side"] == "high" else "side_low"
        info["boundary"] = {"kind": "boundary", "placement": placement, "cmp": cmp}
        info["cut_idx"] = ci
        return {card["qty"]: x}, info
    pat, binding = ctx.get("ov", ("none", False))
    check = ctx.get("check")
    fixed = None
    bool_b = False
    if s == "S2" and target < card["K"] - 1:
        # near-miss (R17): some higher-level 'and' / 'all of' criterion fails on exactly one part
        prev_nm = check

        def near_miss(v, prev=prev_nm):
            ok = False
            for k in range(target + 1, card["K"]):
                c = card["crits"][k]
                if c["t"] in ("and", "allof"):
                    if sum(1 for p in c["parts"] if not M.eval_crit(p, v)) == 1:
                        ok = True
                        break
            return ok and (prev(v) if prev else True)
        check = near_miss
    if s == "S2" and ctx.get("s2") and (pat == "none" or not binding):
        K = card["K"]
        sides = ["missed"] if target == 0 else ["met"] if target == K - 1 else ["met", "missed"]
        combos = []
        for side in sides:
            k = target if side == "met" else target + 1
            if not 1 <= k <= K - 1:
                continue
            B = card["crits"][k]
            if B["t"] == "onlyif":
                atoms = [a for a in M.atoms_of(B["main"]) if a["kind"] in ("num", "date")]
            else:
                atoms = [a for a in M.atoms_of(B) if a["kind"] in ("num", "date")]
                if B["t"] == "unless":
                    atoms = [a for a in atoms if a is not B["b"]]
            for a in atoms:
                it = card["items"][a["item"]]
                r, t, op = it["r"], a["t"], a["op"]
                x = {">=": t, ">": t + r, "<=": t, "<": t - r}[op] if side == "met" else \
                    {">=": t - r, ">": t, "<=": t + r, "<": t}[op]
                if it["lo"] <= x <= it["hi"]:
                    combos.append((side, k, a, x, RW.placement_of(x, t, r)))
        if combos and target in (0, K - 1) and rng.random() < S2_END_BOOL_P:
            # r1g (G7, 6.5): on an end level (L_0 only "just missed", L_{K-1} only "just met"; A28) a boundary
            # criterion with ONE numeric / date atom fixes the same value in every end-level row ("152 hours" on
            # L_0 20/20 of one card), and with two atoms the sampler-wide placement / comparator steering (_need)
            # can pick the same one on most rows ("booking_cost" L_2 18/21 in the r1g smoke). A28 also allows the
            # "one condition" boundary: when that criterion is an
            # "and" / "all of" with a non-numeric atom part, this share of end-level rows takes it instead (L_0: the
            # criterion fails on exactly one part, a non-numeric one, every numeric part holding; L_{K-1}: the
            # criterion holds, so flipping one Boolean part un-meets it). Such rows have a non-numeric boundary
            # criterion, so they are outside the 6.2 placement denominator (R15) and carry no boundary element.
            side0, k0 = combos[0][0], combos[0][1]
            B0 = card["crits"][k0]
            bparts = [p for p in B0.get("parts", []) if B0["t"] in ("and", "allof") and p["t"] == "atom"
                      and p["a"]["kind"] not in ("num", "date")]
            if bparts:
                combos = []
                if side0 == "missed":
                    prev_b = check

                    def bchk0(v, B=B0, prev=prev_b):
                        bad = [p for p in B["parts"] if not M.eval_crit(p, v)]
                        if len(bad) != 1 or bad[0]["t"] != "atom" or bad[0]["a"]["kind"] in ("num", "date"):
                            return False
                        return prev(v) if prev else True
                    check = bchk0
                bool_b = True
        if combos:
            cnt = ctx.get("s2_counts")
            if cnt is not None:
                # G10 r1: placement shares (6.2) and inclusive vs exclusive 50/50 among S2 boundary rows, jointly.
                # cnt is the sampler-wide counter (placements and "cmp:incl" / "cmp:excl").
                tot = sum(cnt.get(p_, 0) for p_ in ("at", "below", "above")) + 1
                tgt = {"at": 0.34, "below": 0.36, "above": 0.30}
                ctot = cnt.get("cmp:incl", 0) + cnt.get("cmp:excl", 0) + 1

                def _need(c):
                    cmp_ = "incl" if c[2]["op"] in (">=", "<=") else "excl"
                    return (tgt[c[4]] * tot - cnt.get(c[4], 0)) + 1.5 * (0.5 * ctot - cnt.get("cmp:" + cmp_, 0))
                best = max(_need(c) for c in combos)
                combos = [c for c in combos if _need(c) >= best - 1e-9]
            side, k, a, x, pl = rng.choice(combos)
            B = card["crits"][k]
            it = card["items"][a["item"]]
            r = it["r"]
            fixed = {a["item"]: x}
            want = side == "met"

            def chk(v, B=B, a=a, x=x, r=r, want=want, prev=check):
                if M.eval_crit(B, v) != want:
                    return False
                v2 = dict(v)
                step = r if ((a["op"] in (">=", ">")) != want) else -r
                v2[a["item"]] = x + step
                if M.eval_crit(B, v2) == want:
                    return False
                return prev(v) if prev else True
            check = chk
            info["boundary"] = {"kind": "boundary", "placement": pl, "cmp": "incl" if a["op"] in (">=", "<=") else "excl",
                                "side": side, "atom": a}
    nm = s == "S2" and target < card["K"] - 1
    v = RW.sample_lh(card, rng, target, pat, binding, check, fixed, near_miss=nm)
    if v is None and (fixed is not None or bool_b):
        info.pop("boundary", None)
        v = RW.sample_lh(card, rng, target, pat, binding, ctx.get("check"), None, near_miss=nm)
    if v is None:
        raise CaseFail(f"no values for level {target} pattern {pat} binding {binding}")
    return v, info


def sample_any(card, rng, target, check=None, fixed=None, tries=4000):
    for _ in range(tries):
        v = CD.random_values(card, rng, near=0.55)
        if fixed:
            v.update(fixed)
        if M.final_level(card, v) == target and (check is None or check(v)):
            return v
    return None


# ------------------------------------------------------------------------------------------------ presentation
def _c1_dec_cands(card: dict, target: int, elig: list) -> list:
    """r1h (G10 T02): the C1-eligible factors that can move this level when read as present: LADDER, a factor of the
    level-(target+1) criterion; HIGHEST, a factor of any higher level's criterion; either mode, a factor of a floor
    override above the target. A random key from all eligible factors hit these on few mid-level rows (S1 mid-level
    unmentioned rows decisive 15/141), so the decisive share stayed at 0.24-0.34 (rule 40-60%)."""
    K = card["K"]
    lv = ([target + 1] if target + 1 < K else []) if card["mode"] == "ladder" else \
        list(range(target + 1, K)) if card["mode"] == "highest" else []
    items = set()
    for k in lv:
        items |= {a["item"] for a in M.atoms_of(card["crits"][k])}
    for o in card.get("overrides", []):
        if o.get("type") == "floor" and o.get("m", o.get("level", K)) > target:  # r1i: overrides store "m"
            items |= {a["item"] for a in M.atoms_of(o["cond"])}
    return [k for k in elig if k in items]


def _c1_draw(card: dict, target: int, elig: list, dw: bool, rng: random.Random) -> list:
    """r1h: the row's unmentioned keys (1 or 2, drawn 1:1:2 as before). A decisive row takes its first key from the
    factors that can move the level (_c1_dec_cands); the second key and non-decisive rows draw from all eligible."""
    n = min(len(elig), rng.choice([1, 1, 2]))
    cands = _c1_dec_cands(card, target, elig) if dw else []
    if cands:
        k1 = rng.choice(cands)
        rest = [k for k in elig if k != k1]
        keys = [k1] + (rng.sample(rest, 1) if n == 2 and rest else [])
    else:
        keys = rng.sample(elig, n)
    if card.get("c1_D") is not None and "+".join(sorted(keys)) not in card["c1_D"]:
        keys = keys[:1]  # r1f: a pair is used only when its stated cue target is level-free (setup)
    return keys


def _build_case_once(card: dict, target: int, rng: random.Random, ctx: dict, used_names: set) -> dict:
    """r1h (G10 6.2, C16 S2): ctx['c16_below'] asks a HIGHEST row (target >= 2) for a lower criterion that fails,
    so the LADDER reading (C16) gives a level below; soft, the row is drawn without it when no such case exists."""
    want16 = ctx.get("c16_req")
    if want16 is not None and card["mode"] in ("ladder", "highest"):
        # r1j: present (LADDER read as HIGHEST gives a higher level, HIGHEST read as LADDER a lower one) or absent
        prev = ctx.get("check")

        def c16b(v, prev=prev, want16=want16):
            if (M.final_level(card, v, {"mode_swap": True}) != target) != want16:
                return False
            return prev(v) if prev else True
        # r1k (T02 over 6.2): the C16 request never costs the row its C1 request. A C16 case that lost its
        # unmentioned factor is used only when the plain draw loses it too (build 14: S2-029 levels 2-3 asked for
        # C16, came back without C1 and the per-card C1 tally moved every C1 row to levels 0-1)
        need_c1 = bool(ctx.get("c1")) and bool(card["c1_elig"])
        tmp16 = set(used_names)
        c16c = None
        try:
            c16c = _build_case_once0(card, target, rng, dict(ctx, check=c16b), tmp16)
        except CaseFail:
            pass
        if c16c is not None and (not need_c1 or c16c.get("unmentioned")):
            used_names |= tmp16
            return c16c
        try:
            c = _build_case_once0(card, target, rng, ctx, used_names)
        except CaseFail:
            if c16c is None:
                raise
            used_names |= tmp16
            return c16c
        if c16c is not None and not c.get("unmentioned"):
            used_names |= tmp16
            return c16c
        return c
    return _build_case_once0(card, target, rng, ctx, used_names)


def _build_case_once0(card: dict, target: int, rng: random.Random, ctx: dict, used_names: set) -> dict:
    s = card["sampler"]
    want_c1 = ctx.get("c1", False)
    elig = card["c1_elig"]
    c1_keys = []
    if want_c1 and elig:
        decisive_wanted = ctx.get("c1_decisive", rng.random() < 0.5)  # G10 r1: set per row by the sampler controller
        if decisive_wanted and not _c1_dec_cands(card, target, elig):
            decisive_wanted = False  # r1h: no factor can move this level (e.g. LADDER top level): skip the search
        c1_keys = _c1_draw(card, target, elig, decisive_wanted, rng)
        prev = ctx.get("check")

        # r1d: on C15 "key" cards the unmentioned factors become missing entries (C15, two-way, 6.2): a decisive
        # one also takes the direction the sampler is short of
        kdir = ctx.get("c15_dir") if card.get("c15") == "key" else None

        def chk(v, keys=c1_keys, dw=decisive_wanted, prev=prev):
            if any(v[k] for k in keys):
                return False
            if prev and not prev(v):
                return False
            v1 = dict(v)
            for k in keys:
                v1[k] = True
            l0, l1 = M.final_level(card, v), M.final_level(card, v1)
            if dw and kdir and l1 != l0:
                return (l1 > l0) == (kdir == "above")
            return (l1 != l0) == dw
        ctx = dict(ctx, check=chk)
    try:
        try:
            v, info = values_for(card, target, rng, ctx)
        except CaseFail:
            if not c1_keys or not decisive_wanted:
                raise
            # G10 r1d (T02 C1 decisive share): a decisive unmentioned factor may exist with other keys; try two
            # more key draws before dropping decisiveness (the unmentioned-row decision itself is unchanged)
            got = None
            tried = {tuple(sorted(c1_keys))}
            for _ in range(4):  # r1h: 2 -> 4 draws, each from the level-moving factors (_c1_draw), new key sets only
                keys2 = _c1_draw(card, target, elig, True, rng)
                if tuple(sorted(keys2)) in tried:
                    continue
                tried.add(tuple(sorted(keys2)))
                ctx2 = dict(ctx, check=lambda v, keys=keys2: chk(v, keys))
                try:
                    got = values_for(card, target, rng, ctx2)
                    c1_keys = keys2
                    break
                except CaseFail:
                    continue
            if got is None:
                raise
            v, info = got
    except CaseFail:
        if c1_keys:
            # r1k: the non-decisive fallbacks keep the row's own check (the C16 request, f7case._build_case_once)
            ctx = dict(ctx, check=lambda v, keys=c1_keys, prev=prev: not any(v[k] for k in keys) and (prev is None or prev(v)))
            try:
                v, info = values_for(card, target, rng, ctx)
            except CaseFail:
                # r1e (T02 level independence): two factors absent together may not fit this level; keep the
                # row unmentioned with one of them before dropping C1 for the row
                got = None
                for k1 in (list(c1_keys) if len(c1_keys) > 1 else []):
                    try:
                        got = values_for(card, target, rng, dict(ctx, check=lambda v, k1=k1, prev=prev: not v[k1] and (prev is None or prev(v))))
                        c1_keys = [k1]
                        break
                    except CaseFail:
                        continue
                if got is not None:
                    v, info = got
                else:
                    c1_keys = []
                    ctx = dict(ctx, check=None)
                    v, info = values_for(card, target, rng, ctx)
        else:
            raise
    if M.final_level(card, v) != target:
        raise CaseFail("target mismatch")
    subject = new_name(card, rng, used_names)
    case = {"subject": subject, "values": v, "info": info, "unmentioned": [], "missing": [], "plans": [],
            "partials": [], "repeats": [], "fillers": [], "distractor": None, "inject": None, "other": None,
            "layout": card["layout"]}
    bool_keys = [k for k in card["item_order"] if card["items"][k]["kind"] == "bool"]
    if c1_keys:
        if card.get("c15") == "key":
            case["missing"] = list(c1_keys)
        else:
            case["unmentioned"] = list(c1_keys)
    # C15 missing entries (structured containers), decided per row before the values (level independent)
    if card.get("c15") and not case["missing"] and ctx.get("missing_want"):
        off = [k for k in bool_keys if not v[k] and k not in case["unmentioned"]]
        if off:
            # G10 r1d: C15 is two-way (6.2); among the absent keys prefer one whose "read as present" alternative
            # moves the level in the direction the sampler is short of (whether a row has a missing entry is
            # decided above, independently of the level)
            want = ctx.get("c15_dir")
            if want:
                def _dir(k):
                    l1 = M.final_level(card, {**v, k: True})
                    return "above" if l1 > target else ("below" if l1 < target else None)
                pref = [k for k in off if _dir(k) == want]
                off = pref or off
            case["missing"] = [rng.choice(off)]
    taken = set(case["unmentioned"]) | set(case["missing"])
    # S4 plans (20%) and partial facts (10%): an absent factor stated only by a plan / partial sentence
    if s == "S4":
        off = [k for k in bool_keys if not v[k] and k not in taken]
        if off and rng.random() < 0.24:
            k = rng.choice(off)
            case["plans"].append(k)
            taken.add(k)
            off.remove(k)
        if off and rng.random() < 0.14:
            k = rng.choice(off)
            case["partials"].append(k)
            taken.add(k)
    # fillers (count / points, S3 and S4 count): total absence cues uniform over m..f, independent of level (Z02)
    if card["mode"] in ("count", "points"):
        m = len(card["listed"])
        f = card["n_fillers"]
        pool = card["filler_pool"]
        # repeats (C14): 15% of rows; the restated factor's polarity is a coin flip, so it cannot track the level
        rep_abs = 0
        if ctx.get("repeat_want"):
            pol = rng.random() < 0.5
            cand = [k for k in card["listed"] if k not in taken and bool(v[k]) == pol]
            if cand:
                k = rng.choice(cand)
                case["repeats"] = [k]
                rep_abs = 0 if pol else 1
        listed_absent = sum(1 for k in card["listed"] if not v[k])
        T = ctx.get("T") if ctx.get("T") is not None else rng.randint(m, f)
        f_abs = T - listed_absent - rep_abs
        f_abs = max(0, min(f, f_abs))
        fs = rng.sample(pool, f)
        absent_idx = set(rng.sample(range(f), f_abs))
        case["fillers"] = [{"term": x["term"], "det": x["det"], "fkind": x["kind"], "present": i not in absent_idx}
                           for i, x in enumerate(fs)]
    # other entity: S1 / S3 inert facts, S4 distractor (20%) or inert
    if card.get("c21"):
        r = rng.random()
        if s == "S4" and r < 0.2:
            stated = [k for k in card["item_order"] if k not in taken and k in v]
            if stated:
                k = rng.choice(stated)
                it = card["items"][k]
                alts = _distractor_values(card, v, k, rng)
                if alts is not None:
                    case["distractor"] = (k, alts)
                    case["other"] = new_name(card, rng, used_names)
        elif r < (0.5 if s == "S4" else 0.4) and card["inert"]:
            case["other"] = new_name(card, rng, used_names)
    # inert sentence about the subject (S1, S3, S4: about 30%)
    case["inert_subject"] = None
    if s in ("S1", "S3", "S4") and card["inert"] and rng.random() < 0.3:
        it = rng.choice(card["inert"])
        case["inert_subject"] = (it["term"], rng.choice(it["values"]))
    case["facts"] = make_facts(card, case, rng)
    return case




def case_cues(case: dict) -> int:
    """Absence cues in the rendered case (6.3): negate frames, absent markers and missing markers, any entity."""
    n = 0
    for f in case["facts"]:
        if f["kind"] in ("bool", "filler") and not f["polarity"]:
            n += 1
        elif f["kind"] == "missing":
            n += 1
        elif f["kind"] == "repeat" and f["of"]["kind"] in ("bool", "filler") and not f["of"]["polarity"]:
            n += 1
    return n


def c1_key(case: dict) -> str | None:
    """Key of a case's unmentioned-factor set in card['c1_D'] (r1f)."""
    return "+".join(sorted(case["unmentioned"])) if case.get("unmentioned") else None


def cue_target_for(card: dict, case: dict, T):
    """r1f (6.3 / T02): the stated absence-cue count a case must carry. Rows without unmentioned factors: the row's
    target T. Rows with unmentioned factors (C1): an unmentioned factor is not stated, so it carries no cue, and the
    stated counts the other factors can reach with it left out differ by level (S2-028: unmentioned 20/20 on levels
    0-1, 0/26 on levels 2-4, because build_case then dropped C1). Setup stores per unmentioned set the stated counts
    reachable at EVERY level (card['c1_D']); the C1 row's target is taken from that set by the index of T in the
    card's cue set, so it depends on T only (cycled per level) and both C1 and the stated count stay level-free."""
    if T is None:
        return None
    k = c1_key(case)
    Ds = (card.get("c1_D") or {}).get(k) if k else None
    if not Ds:
        return T
    D = sorted(card.get("cue_D") or [T])
    i = D.index(T) if T in D else 0
    return Ds[i % len(Ds)]


def _near_miss(card: dict, target: int, v: dict) -> bool:
    for k in range(target + 1, card["K"]):
        c = card["crits"][k]
        if c["t"] in ("and", "allof") and sum(1 for p in c["parts"] if not M.eval_crit(p, v)) == 1:
            return True
    return False


def adjust_cues(card: dict, case: dict, T: int, rng: random.Random, want16=None) -> dict:
    """Move the case's absence-cue count toward T by flipping stated subject Booleans whose flip keeps the final level,
    the mode level, the firing pattern, the unmentioned-factor decisiveness and the S2 boundary criterion.
    r1j: with want16 (the row's C16 request, f7main.c16_want) a flip may not undo a C16 status that meets the request
    (build 12: S2 HIGHEST rows drawn with a failing lower criterion lost it to a cue flip; C16 S2 above share 0.60)."""
    v = case["values"]
    n = case_cues(case)
    if n == T:
        return case
    gold = M.final_level(card, v)
    ml = M.mode_level(card, v)
    fire = M.firing(card, v)
    ov_items = {a["item"] for o in card.get("overrides", []) for a in M.atoms_of(o["cond"])}
    b = case["info"].get("boundary") or {}
    bchk = None
    if b.get("atom") is not None:
        k_b = None
        for k, c in card.get("crits", {}).items():
            if any(a is b["atom"] for a in M.atoms_of(c)):
                k_b = k
        if k_b is not None:
            B = card["crits"][k_b]
            a_b = b["atom"]
            r_b = card["items"][a_b["item"]]["r"]
            want_b = b.get("side") == "met"

            def bchk(vv, B=B, a=a_b, r=r_b, want=want_b):
                if M.eval_crit(B, vv) != want:
                    return False
                v3 = dict(vv)
                step = r if ((a["op"] in (">=", ">")) != want) else -r
                v3[a["item"]] = vv[a["item"]] + step
                return M.eval_crit(B, v3) != want
    blocked = set(case["unmentioned"]) | set(case["missing"]) | set(case["plans"]) | set(case["partials"]) | \
        set(case["repeats"]) | ov_items
    if case.get("distractor"):
        blocked.add(case["distractor"][0])

    def c1_dec(vv):
        if not case["unmentioned"]:
            return None
        v1 = dict(vv)
        for k in case["unmentioned"]:
            v1[k] = True
        return M.final_level(card, v1) != M.final_level(card, vv)
    dec0 = c1_dec(v)
    s16 = (lambda vv: M.final_level(card, vv, {"mode_swap": True}) != gold) \
        if want16 is not None and card["mode"] in ("ladder", "highest") else None
    v = dict(v)
    for _ in range(6):
        if n == T:
            break
        want_false = n < T
        cands = [k for k in card["item_order"] if card["items"][k]["kind"] == "bool" and k not in blocked
                 and bool(v[k]) == want_false]
        rng.shuffle(cands)
        moved = False
        for k in cands:
            v2 = dict(v)
            v2[k] = not v2[k]
            if M.final_level(card, v2) != gold or M.mode_level(card, v2) != ml or M.firing(card, v2) != fire:
                continue
            if c1_dec(v2) != dec0:
                continue
            if s16 is not None and s16(v) == want16 and s16(v2) != want16:
                continue
            if bchk is not None and not bchk(v2):
                continue
            if card["sampler"] == "S2" and gold < card["K"] - 1 and not _near_miss(card, gold, v2):
                continue
            v = v2
            n += 1 if want_false else -1
            moved = True
            break
        if not moved:
            break
    if v == case["values"]:
        return case
    facts = []
    for f in case["facts"]:
        g = dict(f)
        if g.get("who") == case["subject"] and g.get("kind") == "bool":
            g["polarity"] = bool(v[g["item"]])
        facts.append(g)
    return dict(case, values=v, facts=facts)


def build_case(card: dict, target: int, rng: random.Random, ctx: dict, used_names: set) -> dict:
    """One case; on ladder / highest / grid cards with a target absence-cue count T (ctx['T_lh']), the case is drawn
    and then adjusted by level-preserving flips of free Booleans until it carries exactly T cues, so the cue count is
    independent of the level (6.3). The cue target wins over an unmentioned-factor request (C1) after 6 tries."""
    T = ctx.get("T_lh")
    best = None
    tries = (40 if card["sampler"] == "S2" else 24) if T is not None else 1
    D = set(card.get("cue_D") or [])
    for i in range(tries):
        # r1k: requests give way in a fixed order, the cue target (6.3) last: the C16 request after the first third
        # of the tries, the C1 request (T02) after two thirds (r1j dropped C1 at one third while it still kept C16,
        # so rows traded C1 for C16 on the levels where both did not fit the cue target)
        cx = ctx
        if T is not None and i >= tries // 3:
            cx = {k_: v_ for k_, v_ in ctx.items() if k_ != "c16_req"}
            if i >= (2 * tries) // 3:
                cx["c1"] = False
        tmp = set(used_names)
        try:
            c = _build_case_once(card, target, rng, cx, tmp)
        except CaseFail:
            if i == tries - 1 and best is None:
                raise
            continue
        Ts = cue_target_for(card, c, T)  # r1f: C1 rows take their level-free stated target
        if T is not None:
            # r1j: the C16 status is kept through cue flips only while the row still asks for it (r1k: first third
            # of the tries), so the cue target wins (6.3; keeping it on every try left 228 rows off target, build 13)
            c = adjust_cues(card, c, Ts, rng, cx.get("c16_req"))
        n = case_cues(c)
        if T is None or n == Ts:
            used_names |= tmp
            c["cue_target_met"] = True if T is not None else None
            return c
        sc = (0 if (n in D or Ts != T) else 1, abs(n - Ts))  # a miss stays inside the card's cue set when it can
        if best is None or sc < best[2]:
            best = (c, tmp, sc)
    if best is None:
        raise CaseFail("no case")
    c, tmp, _ = best
    used_names |= tmp
    c["cue_target_met"] = False
    return c


def _distractor_values(card: dict, v: dict, k: str, rng: random.Random):
    """A value for the other entity's statement of item k; on rows where the merged reading differs from gold it is
    above gold on 50% (6.4)."""
    it = card["items"][k]
    gold = M.final_level(card, v)
    cands = []
    if it["kind"] == "bool":
        cands = [True, False]
    else:
        ths = CD.collect_thresholds(card).get(k, [])
        r = it["r"]
        for t in ths:
            for d in (-1, 0, 1):
                x = t + d * r
                if it["lo"] <= x <= it["hi"]:
                    cands.append(x)
        steps = int((it["hi"] - it["lo"]) / r)
        cands.append(it["lo"] + rng.randint(0, steps) * r)
    up, down, same = [], [], []
    for x in cands:
        v1 = dict(v)
        v1[k] = x
        l1 = M.final_level(card, v1)
        (up if l1 > gold else down if l1 < gold else same).append(x)
    want = rng.choice(["up", "down", "same"])
    for w in [want, "up", "down", "same"]:
        pool = {"up": up, "down": down, "same": same}[w]
        if pool:
            return rng.choice(pool)
    return None


def make_facts(card: dict, case: dict, rng: random.Random) -> list[dict]:
    v = case["values"]
    S = case["subject"]
    facts = []
    alias_rate = 0.4 if card.get("aliases_on") else 0.0
    for k in card["item_order"]:
        it = card["items"][k]
        if k in case["unmentioned"]:
            continue
        if it["kind"] == "bool":
            if k in case["missing"]:
                facts.append({"kind": "missing", "who": S, "item": k})
            elif k in case["plans"]:
                facts.append({"kind": "plan", "who": S, "item": k, "frame": rng.randrange(4),
                              "alias": rng.random() < alias_rate})
            elif k in case["partials"]:
                facts.append({"kind": "partial", "who": S, "item": k, "frame": rng.randrange(2),
                              "alias": rng.random() < alias_rate})
            else:
                fr = rng.randrange(3)
                facts.append({"kind": "bool", "who": S, "item": k, "polarity": bool(v[k]), "frame": fr,
                              "alias": rng.random() < alias_rate})
        else:
            facts.append({"kind": "value", "who": S, "item": k, "value": v[k]})
    for fl in case["fillers"]:
        facts.append({"kind": "filler", "who": S, "term": fl["term"], "det": fl["det"], "fkind": fl["fkind"],
                      "polarity": fl["present"], "frame": rng.randrange(3)})
    if case.get("inert_subject"):
        t, val = case["inert_subject"]
        facts.append({"kind": "inert", "who": S, "term": t, "value": val})
    if case["other"]:
        O = case["other"]
        if case["distractor"]:
            k, val = case["distractor"]
            it = card["items"][k]
            if it["kind"] == "bool":
                facts.append({"kind": "bool", "who": O, "item": k, "polarity": bool(val), "frame": rng.randrange(3),
                              "alias": False, "distractor": True})
            else:
                facts.append({"kind": "value", "who": O, "item": k, "value": val, "distractor": True})
        else:
            it = rng.choice(card["inert"])
            facts.append({"kind": "inert", "who": O, "term": it["term"], "value": rng.choice(it["values"])})
    rng.shuffle(facts)
    for k in case["repeats"]:
        first = next((f for f in facts if f.get("item") == k and f["kind"] == "bool" and f["who"] == S), None)
        if first is not None:
            pos = rng.randint(facts.index(first) + 1, len(facts))
            facts.insert(pos, {"kind": "repeat", "who": S, "of": first, "item": k})
    return facts


def add_injection(card: dict, case: dict, rng: random.Random, gold: int) -> dict:
    K = card["K"]
    above = [l for l in range(K) if l > gold]
    below = [l for l in range(K) if l < gold]
    side = rng.choice([x for x in (above, below) if x])
    adj = [l for l in side if abs(l - gold) == 1]
    far = [l for l in side if abs(l - gold) >= 2]
    lvl = rng.choice(far) if (far and rng.random() < 0.5) else rng.choice(adj)
    # G7 r1: the imperative names the level as "<level word> <n>" only (G0 3.1 W05 form "output Level <n>"), never by
    # its name: level names never occur in any case record, so no name feature exists that only attack rows carry.
    opt = card["levels"]["options"][lvl].split(" - ")[0]
    text = rng.choice(LX.INJECT).format(OPT=opt)
    c2 = dict(case)
    c2["inject"] = lvl
    facts = list(case["facts"])
    facts.insert(rng.randint(0, len(facts)), {"kind": "inject", "who": None, "text": text, "level": lvl})
    c2["facts"] = facts
    return c2


def rename_case(card: dict, case: dict, rng: random.Random, used: set) -> dict:
    """equiv twin (M3-style rename): new subject (and other entity) names; same values and frames."""
    old_s, old_o = case["subject"], case["other"]
    S = new_name(card, rng, used)
    O = new_name(card, rng, used) if old_o else None
    m = {old_s: S}
    if old_o:
        m[old_o] = O

    def fx(f):
        g = dict(f)
        if g.get("who") in m:
            g["who"] = m[g["who"]]
        if g.get("kind") == "repeat":
            g["of"] = fx(g["of"])
        return g
    c2 = dict(case, subject=S, other=O, facts=[fx(f) for f in case["facts"]])
    return c2


def reorder_case(case: dict, rng: random.Random) -> dict:
    """equiv twin (M5-style reorder): facts in a new order (repeats stay after their first mention)."""
    base = [f for f in case["facts"] if f["kind"] != "repeat"]
    reps = [f for f in case["facts"] if f["kind"] == "repeat"]
    for _ in range(20):
        nb = list(base)
        rng.shuffle(nb)
        if nb != base or len(nb) < 2:
            break
    for r in reps:
        first = next(i for i, f in enumerate(nb) if f.get("item") == r["item"] and f["kind"] == "bool"
                     and f["who"] == case["subject"])
        nb.insert(rng.randint(first + 1, len(nb)), r)
    return dict(case, facts=nb)


def flip_twin(card: dict, base: dict, twin_level: int, rng: random.Random, used: set, ctx: dict) -> dict | None:
    """fact_flip twin: one fact changed (one attribute value or one factor's presence); solver A gives exactly the
    drawn adjacent twin level (every mode, so per-card level quotas stay exact). On override cards the changed
    attribute is in no override condition and no override is binding on either row."""
    v = base["values"]
    ov_items = {a["item"] for o in card.get("overrides", []) for a in M.atoms_of(o["cond"])}
    keys = [k for k in v if k not in ov_items and k not in base["unmentioned"] and k not in base["missing"]
            and k not in base["plans"] and k not in base["partials"] and k not in base["repeats"]
            and not (base["distractor"] and base["distractor"][0] == k)]
    rng.shuffle(keys)
    ths = CD.collect_thresholds(card)
    cands = []
    for k in keys:
        it = card["items"][k]
        if it["kind"] == "bool":
            opts = [not v[k]]
        else:
            r = it["r"]
            opts = set()
            for t in ths.get(k, []):
                for d in (-2, -1, 0, 1, 2):
                    x = t + d * r
                    if it["lo"] <= x <= it["hi"]:
                        opts.add(x)
            opts.discard(v[k])
            opts = sorted(opts)
            rng.shuffle(opts)
        for x in opts:
            v2 = dict(v)
            v2[k] = x
            if card["mode"] == "points":
                if sum(1 for f in card["listed"] if v2[f]) > card["P"]:
                    continue
            try:
                l2 = M.final_level(card, v2)
            except ValueError:
                continue
            if card.get("overrides"):
                if M.final_level(card, v2) != M.mode_level(card, v2) or M.final_level(card, v) != M.mode_level(card, v):
                    continue
            if l2 == twin_level and not (ctx.get("struct_used") and ctx["struct_used"](v2)):
                cands.append((k, x, l2))  # G12 r1b: the twin's structure must be new on the card
        if cands:
            break
    if not cands:
        return None
    k, x, l2 = rng.choice(cands)
    v2 = dict(v)
    v2[k] = x
    twin = dict(base)
    twin["values"] = v2
    twin["flip"] = {"item": k, "from": v[k], "to": x}
    facts = []
    for f in base["facts"]:
        g = dict(f)
        if g.get("item") == k and g["who"] == base["subject"]:
            if g["kind"] == "bool":
                g["polarity"] = bool(x)
            elif g["kind"] == "value":
                g["value"] = x
            elif g["kind"] == "repeat":
                of = dict(g["of"])
                of["polarity"] = bool(x)
                g["of"] = of
        facts.append(g)
    twin["facts"] = facts
    if card["mode"] in ("count", "points"):
        tot = M.count_total(card, v2)
        twin["info"] = dict(base["info"], boundary={"kind": "boundary", "placement": RW.int_placement(card, tot),
                                                     "cmp": "closed"})
    elif card["mode"] == "cut":
        it = card["items"][card["qty"]]
        if card["integer"]:
            pl = RW.int_placement(card, x)
            cmp = "closed"
        else:
            pls = [RW.placement_of(x, c, it["r"]) for c in card["cuts"]]
            pl = next((p for p in pls if p == "at"), next((p for p in pls if p != "interior"), "interior"))
            cmp = "side_high" if card["side"] == "high" else "side_low"
        twin["info"] = dict(base["info"], boundary={"kind": "boundary", "placement": pl, "cmp": cmp})
    else:
        twin["info"] = {k2: v2_ for k2, v2_ in base["info"].items() if k2 != "boundary"}
    return twin


def worked_case(card: dict, level: int, rng: random.Random, used: set) -> dict:
    """A full sampler draw on the card's rubric for a worked example: every rubric item stated, no injected text."""
    ctx = {"ov": ("none", False)}
    if card["mode"] == "cut":
        ctx["placement"] = rng.choice(["at", "below", "above", "interior"])
    v, info = values_for(card, level, rng, ctx)
    S = new_name(card, rng, used)
    case = {"subject": S, "values": v, "info": info, "unmentioned": [], "missing": [], "plans": [], "partials": [],
            "repeats": [], "fillers": [], "distractor": None, "inject": None, "other": None, "layout": "narrative",
            "inert_subject": None}
    case["facts"] = make_facts(card, case, rng)
    return case
