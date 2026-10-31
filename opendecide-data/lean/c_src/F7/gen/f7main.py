"""F7 generation runs (see f7build docstring). Writes rows, relations, card definitions and a per-run report."""
from __future__ import annotations

import collections
import json
import random
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f7build as B  # noqa: E402
import f7case as CS  # noqa: E402
import f7cards as CD  # noqa: E402
import f7model as M  # noqa: E402
import f7packs as PK  # noqa: E402
import f7parse as PS  # noqa: E402
import f7render as R  # noqa: E402
import f7rows as RW  # noqa: E402
import f7solveb as SB  # noqa: E402


CUE_SET = {1, 2}  # sampler-wide absence-cue targets on ladder / highest / grid rows (6.3: level independent)

# ---- G10 / G12 repair r1: sampler-wide balance controller and per-card structure registry --------------------------
# Two-way conv directions (G0 6.2 R05; C8 and C9 pooled), S2 inclusive vs exclusive and placements (6.2), C1 decisive
# share (6.4 T02) are steered by choosing among candidate cases drawn for the SAME target level (labels and per-card
# quotas never change). One-way elements (C4, C5, C7, C1 on LADDER / HIGHEST) are not steered.
ONE_WAY = {"C4", "C5", "C7"}
BAL: dict = {}


def bal_reset() -> None:
    RW.QUOTA_TALLY.clear()
    BAL.clear()
    BAL.update({"gap": collections.defaultdict(collections.Counter), "um": collections.defaultdict(collections.Counter),
                "dir": collections.defaultdict(collections.Counter), "s2": collections.defaultdict(collections.Counter),
                "s6": collections.defaultdict(collections.Counter), "c1": collections.defaultdict(collections.Counter)})


bal_reset()


def _dir_key(card: dict, e: dict, gold: int):
    c = e["conv"]
    if c in ONE_WAY or (c == "C1" and card["mode"] in ("ladder", "highest")):
        return None
    return ("C8+C9" if c in ("C8", "C9") else c), ("above" if e["alt_level"] > gold else "below")


# G10 r1c: C16 (LADDER <-> HIGHEST reading) is two-way only across modes: LADDER gap cases give alt above, HIGHEST rows
# with a lower criterion failing give alt below (6.2). Gap-case floors: S1 >= 20% of LADDER rows (S1 checks); S2
# >= 25% of the LADDER rows whose criteria above k + 1 are drawn at random, i.e. levels k <= K - 3 (S2 shape).
C1_SHARE = 0.255  # r1i: planned unmentioned share of S1 / S2 / S4 rows (T02: 20-30%)
GAP_FLOOR = {"S1": ("all", 0.22), "S2": ("elig", 0.27)}


def c16_want(card: dict, gold: int):
    """True / False when this row's C16 element should be present / absent, None when it cannot occur."""
    if card["mode"] not in ("ladder", "highest") or card["sampler"] not in ("S1", "S2", "S4"):
        return None
    K = card["K"]
    s = card["sampler"]
    c = BAL["dir"][(s, "C16")]
    g = BAL["gap"][s]
    if card["mode"] == "ladder":
        if gold > K - 3:
            return None
        fl = GAP_FLOOR.get(s)
        if fl:
            den = g["lad_all"] if fl[0] == "all" else g["lad_elig"]
            if g["lad_gap"] < fl[1] * (den + 1):
                return True
        return c["above"] <= c["below"]
    if gold < 2:
        return None
    if s in ("S1", "S2"):
        # r1j (G10 6.2): HIGHEST "below" C16 is the scarce side (LADDER "above" is held up by the gap floor, G0 6.4),
        # and asking for it only while below <= above let early HIGHEST cards turn it off before the LADDER cards
        # ran (build 11: S1 0.606, S2 0.601 above; HIGHEST cards S1-005 / S2-029 0 C16 rows), so every eligible
        # HIGHEST row asks for one; LADDER rows keep the balance rule above
        return True
    return c["below"] <= c["above"]


def bal_score(card: dict, case: dict, gold: int) -> float:
    s = card["sampler"]
    sc = 0.0
    els = RW.conv_elements(card, case, gold, {})
    w16 = c16_want(card, gold)
    if w16 is not None:
        sc += 3.0 if any(e["conv"] == "C16" for e in els) == w16 else -3.0
    for e in els:
        kd = _dir_key(card, e, gold)
        if kd is None or (w16 is not None and kd[0] == "C16"):
            continue
        c = BAL["dir"][(s, kd[0])]
        diff = c["above"] - c["below"]
        sc += (diff if kd[1] == "below" else -diff) / (c["above"] + c["below"] + 20.0)
    if case.get("unmentioned"):
        c = BAL["c1"][s]
        n = c["dec"] + c["non"]
        want_dec = (c["dec"] / n) < 0.5 if n else True
        dec = any(e["conv"] == "C1" for e in els)
        sc += 1.0 if dec == want_dec else -1.0  # r1d: 0.5 -> 1.0 (S1 / S4 decisive share was 0.39)
    return sc


def bal_off(card: dict) -> bool:
    """r1c: draw more candidates while any two-way direction or the C1 decisive share of this sampler is off target."""
    s = card["sampler"]
    for (s_, key), c in BAL["dir"].items():
        n = c["above"] + c["below"]
        if s_ == s and n >= 30 and abs(c["above"] / n - 0.5) > 0.025:
            return True
    c = BAL["c1"][s]
    n = c["dec"] + c["non"]
    return n >= 30 and abs(c["dec"] / n - 0.5) > 0.03


def bal_update(card: dict, row: dict, gold: int) -> None:
    s = card["sampler"]
    m = row["meta"]
    if card["mode"] == "ladder":
        g = BAL["gap"][s]
        g["lad_all"] += 1
        if gold <= card["K"] - 3:
            g["lad_elig"] += 1
            g["lad_gap"] += any(e["kind"] == "conv" and e["conv"] == "C16" for e in m["edge"])
    for e in m["edge"]:
        if e["kind"] == "conv":
            kd = _dir_key(card, e, gold)
            if kd is not None:
                BAL["dir"][(s, kd[0])][kd[1]] += 1
        elif e["kind"] == "boundary":
            if s == "S2":
                BAL["s2"][s][e["placement"]] += 1
                BAL["s2"][s]["cmp:" + e["cmp"]] += 1
            elif s == "S6":
                BAL["s6"][s][e["placement"]] += 1
    if card["mode"] in ("ladder", "highest") and s in ("S1", "S2", "S4"):
        BAL["um"][s]["n"] += 1
        BAL["um"][s]["u"] += bool(m["case_features"].get("unmentioned"))
        cu = card.setdefault("_c1u", [0, 0])
        cu[1] += 1
        cu[0] += bool(m["case_features"].get("unmentioned"))
        cl = card.setdefault("_c1ul", {}).setdefault(gold, [0, 0])  # r1k: the same tally per level (ctx_for)
        cl[1] += 1
        cl[0] += bool(m["case_features"].get("unmentioned"))
    if m["case_features"].get("unmentioned"):
        BAL["c1"][s]["dec" if any(e["kind"] == "conv" and e["conv"] == "C1" for e in m["edge"]) else "non"] += 1


def c1_level_free(card: dict, rng) -> list:
    """r1e (G7 meta:n_lines / T02 "drawn independently of level"): the C1-eligible factors that can be absent at EVERY
    level of the card. A factor some level needs (e.g. every rung of the top criterion) could only be left unmentioned
    on lower-level rows, so its unmentioned rows tracked the level (S2 K=3: 36/74 level 0, 0/68 top level; in one-fact-
    per-line containers the missing line was a visible level cue). Only level-free factors are left unmentioned."""
    ok = set(card["c1_elig"])
    if not ok or card["mode"] not in ("ladder", "highest", "grid"):
        return sorted(ok)
    ov = (False if any(o["type"] == "floor" for o in card.get("overrides", [])) else None,
          False if any(o["type"] == "cap" for o in card.get("overrides", [])) else None)
    for l in range(card["K"]):
        seen = set()
        for _ in range(40):
            v = RW.construct(card, rng, l, ov)
            if v is not None and M.final_level(card, v) == l:
                seen |= {k for k in ok if not v[k]}
        for k in sorted(ok - seen):
            if CS.sample_any(card, rng, l, check=lambda v, k=k: not v[k], tries=1500) is not None:
                seen.add(k)
        ok &= seen
        if not ok:
            break
    return sorted(ok)


def c1_cue_sets(card: dict, rng) -> dict:
    """r1f (T02 "drawn independently of level", G7 meta:n_lines, 6.3). An unmentioned factor is not stated, so it is
    no absence cue, and on some levels the stated factors cannot reach the row's cue target T without it (S2-028 csv
    K=5: build_case dropped C1 there; unmentioned 20/20 rows on levels 0-1, 0/26 on levels 2-4). For each level-free
    C1 key (and pair of keys) collect the stated absence-cue counts reachable on EVERY level with it unmentioned;
    C1 rows then take their stated target from that set (f7case.cue_target_for). -> {key or 'k1+k2': [counts]}"""
    elig = list(card["c1_elig"])
    sets = [[k] for k in elig] + [[a, b] for i, a in enumerate(elig) for b in elig[i + 1:]]
    out = {}
    for ks in sets:
        c = dict(card, c1_elig=list(ks), c1_D=None)
        common = None
        for l in range(card["K"]):
            reach = set()
            for i in range(8):
                try:
                    cs = CS._build_case_once(c, l, rng, {"ov": ("none", False), "c1": True, "c1_decisive": i % 2 == 0,
                                                         "s2": card["sampler"] == "S2",
                                                         "s2_counts": collections.Counter()}, set())
                except CS.CaseFail:
                    continue
                if sorted(cs["unmentioned"]) != sorted(ks):
                    continue
                for t in range(6):
                    if t not in reach and CS.case_cues(CS.adjust_cues(card, cs, t, rng)) == t:
                        reach.add(t)
            common = reach if common is None else (common & reach)
            if not common:
                break
        if common:
            out["+".join(sorted(ks))] = sorted(common)
    return out


PCONC_P = 1e-5  # r1f: card-level forced-phrase bound (G7 alpha is 0.01 / ~68k tests = 1.5e-7; 70x margin)
PCONC_NMIN = 16  # G7 tests features on >= 20 rows; 16 expected rows leaves room for sampling noise
PCONC_ROWS = {"S1": 64, "S2": 64, "S4": 56}  # rows per card incl. twins (candidates 59 / qc 63; S4 55)
# r2 (G6, G0 4.6: a separate QC sample of >= 5,000 rows): S1-S4 use all 80 packs-2 training packs and S6 all 69
# packs-3 packs (one pack per card), and S3 / S6 rows are fixed by (mode, K) capacity (build 17: S3 779, S6 884), so
# the S1 / S2 / S4 ladder / highest cards carry the rest: 1,170 rows per sampler (build 17 had 5,040 / 5 = 1,008 and
# 4,624 rows, card F7-qc-S2-029 dropped). Expected 3 x 1,170 + 1,663 = 5,173.
QC_SAMPLER_ROWS = 1170
PCONC_QC_HEAD = 6  # r2: qc phrase screen bound = planned rows + room for a dropped card's share


def _binom_sf(x: int, n: int, p: float) -> float:
    """P(X >= x), X ~ Bin(n, p)."""
    import math
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(max(0, x), n + 1))


def _pconc_rows(plan: dict) -> int | None:
    """r2: the phrase screen's rows per card. Candidates keep PCONC_ROWS (None); qc cards carry QC_SAMPLER_ROWS
    shares (about 70-78 rows), so their screen uses the planned rows plus PCONC_QC_HEAD."""
    if "-qc-" not in plan.get("card_id", "") or not plan.get("n"):
        return None
    return max(PCONC_ROWS.get(plan["sampler"], 64), plan["n"] + PCONC_QC_HEAD)


def phrase_conc(card: dict, rng, rows: int | None = None) -> str | None:
    """r1f (G7, 6.5: no single feature predicts the level). A stated factor value (Boolean polarity or exact number)
    whose level is forced by the rubric (e.g. the lone factor of the lowest criterion of a K=3 ladder, or a value the
    cue target T forces on the free level) can sit on one level in ~20 rows of one card,
    a level cue in its own wording ("offer: yes" level 0 20/23, "has sale contingency" level 1 19/21). The card's case
    sampler is simulated per level (cue targets, C1, C15, S2 boundary placements as in card_rows); a card whose
    expected rows of any stated value concentrate on one level with binomial p < PCONC_P (p0 = 1/K, the G7 test) is
    redrawn. -> None or a short reason."""
    K = card["K"]
    R_l = (rows or PCONC_ROWS.get(card["sampler"], 64)) / K  # r2: qc cards pass their planned rows (_pconc_rows)
    if 2 * R_l < PCONC_NMIN:
        return None
    D = card.get("cue_D") or [None]
    N = 12
    cnt = collections.defaultdict(lambda: [0] * K)
    got = [0] * K
    s2c = collections.Counter()
    for l in range(K):
        for i in range(N):
            ctx = {"ov": ("none", False), "T_lh": D[i % len(D)], "c1": bool(card["c1_elig"]) and rng.random() < 0.4,
                   "c1_decisive": i % 2 == 0, "missing_want": rng.random() < 0.15}
            if card["sampler"] == "S2":
                ctx.update({"s2": True, "s2_counts": s2c})
            try:
                cs = CS.build_case(card, l, rng, ctx, set())
            except CS.CaseFail:
                continue
            got[l] += 1
            b = (cs.get("info") or {}).get("boundary") or {}
            if card["sampler"] == "S2" and b.get("placement"):
                s2c[b["placement"]] += 1
                s2c["cmp:" + str(b.get("cmp"))] += 1
            seen = set()
            for f in cs["facts"]:
                if f["kind"] == "bool":
                    seen.add(("b", f["item"], f["polarity"]))
                elif f["kind"] == "value":
                    # r1g: S2 numbers included again (end-level boundary values now take the "one condition"
                    # boundary on S2_END_BOOL_P of rows, f7case.values_for); safety net for single-atom criteria
                    seen.add(("v", f["item"], f["value"]))
            for key in seen:
                cnt[key][l] += 1
    if min(got) == 0:
        return None
    for key, c in cnt.items():
        e = [c[l] / got[l] * R_l for l in range(K)]
        n = sum(e)
        if n < PCONC_NMIN:
            continue
        x = max(e)
        p = _binom_sf(int(round(x)), int(round(n)), 1.0 / K)
        if p < PCONC_P:
            return f"{key[0]}:{key[1]} L{e.index(x)} {x:.0f}/{n:.0f}"
    return None


def cue_feasible(card: dict, rng) -> list:
    """Cue counts reachable at every level (cheap: sampled value vectors; free Booleans can then be flipped)."""
    bools = [k for k in card["item_order"] if card["items"][k]["kind"] == "bool"]
    elig = set(card["c1_elig"])
    sets = []
    for l in range(card["K"]):
        got = set()
        for _ in range(40):
            v = RW.construct(card, rng, l, (False if any(o["type"] == "floor" for o in card.get("overrides", [])) else None,
                                            False if any(o["type"] == "cap" for o in card.get("overrides", [])) else None))
            if v is None or M.final_level(card, v) != l:
                continue
            got.add(sum(1 for k in bools if not v[k]))  # values only: C1 / plan levers are optional per row
        sets.append(got)
    if not all(sets):
        return []
    return sorted(set.intersection(*sets))  # r1c: every count reachable at every level (CUE_SET picked by caller)


def c16_short(card: dict, plan: dict, attempt: int = 0):
    """r1k (G10 6.2, C16 S2): an S2 HIGHEST card must be able to carry the C16 'below' side under its own cue targets.
    S2 is 75% LADDER, and its LADDER gap floor fixes about 108 'above' elements, so the S2 HIGHEST rows at levels >= 2
    (about 127) must carry C16 on most rows. Build 14: S2-027 (K 3) and S2-029 (K 4) had 0 C16 rows, because every
    C16 case there has a different absence-cue count from the card's level-free cue set (S2-027: level 2 with h_1
    failing needs both Booleans absent, cue set {1}; S2-029: level 3 forces h_1 to fail on its Boolean, cue set {2}),
    so C16 there could only come from off-target rows (build 13, G10 D fail). For every level >= 2, every cue target
    and C1 off / on (if the card has C1 keys), at least 2 of 4 sampler draws asking for C16 must end with C16, the
    target met and the C1 request kept. Returns the first short (level, T, c1), else None; a short card is redrawn."""
    if card["sampler"] not in ("S1", "S2") or card["mode"] != "highest" or not card.get("cue_D"):  # r1l: + S1
        return None
    rng = CD.rng_for("c16cap", plan["card_id"], attempt)
    c1s = [False, True] if (card["c1_elig"] and card.get("c15") != "key") else [False]
    for l in range(2, card["K"]):
        for T in card["cue_D"]:
            for c1 in c1s:
                ok = 0
                for t in range(4):
                    ctx = {"ov": ("none", False), "T_lh": T, "c16_req": True, "c1": c1, "c1_decisive": t % 2 == 0,
                           "s2": card["sampler"] == "S2", "s2_counts": collections.Counter()}
                    try:
                        c = CS.build_case(card, l, rng, ctx, set())
                    except CS.CaseFail:
                        continue
                    ok += bool(c.get("cue_target_met")) and M.final_level(card, c["values"], {"mode_swap": True}) != l \
                        and (not c1 or bool(c.get("unmentioned")))
                    if ok >= 2:
                        break
                if ok < 2:
                    return (l, T, c1)
    return None


def cap_short(card: dict, plan: dict, attempt: int = 0):
    """G12 / G10 r1c capacity screen (LADDER / HIGHEST): for every level and every absence-cue target T in the card's
    cue set, the sampler's own construction (S2 label-first boundary rows included) must reach ceil(q / |T|) + 2
    distinct case structures that meet T (q = ceil(n / K)), so each row keeps its drawn T (level-independent cue
    counts, 6.3) and its own structure (one surface form per structure). Returns the first short (level, T), else
    None; a short card is redrawn (CardFail), never filled with repeats."""
    rng = CD.rng_for("cap", plan["card_id"], attempt)
    K = card["K"]
    q = -(-int(plan.get("n") or 2 * K) // K)
    Ts = card.get("cue_D") or [None]
    need = -(-q // len(Ts)) + 2
    for l in range(K):
        for T in Ts:
            hs = set()
            for t in range(3 * need + 6):
                ctx = {"ov": ("none", False)}
                if T is not None:
                    ctx["T_lh"] = T
                if card["sampler"] == "S2":
                    ctx.update({"s2": True, "s2_counts": collections.Counter()})
                try:
                    c = CS.build_case(card, l, rng, ctx, set())
                except CS.CaseFail:
                    continue
                if T is not None and not c.get("cue_target_met"):
                    continue
                hs.add(RW.structure_hash(card, c["values"]))
                if len(hs) >= need:
                    break
            if len(hs) < need:
                return (l, T)
    return None


def ov_short(card: dict, plan: dict, attempt: int = 0):
    """r1c: on override cards, every firing pattern must be constructible (3 distinct structures in <= 24 draws) at
    every level of its reachable set, non-binding, and binding at its binding level (6.4 R02 quotas), so no planned
    unit fails and every card keeps its exact level quota. Returns the first short (pattern, level, binding)."""
    ovs = card.get("overrides", [])
    if not ovs:
        return None
    rng = CD.rng_for("ovcap", plan["card_id"], attempt)
    K = card["K"]
    fl = next((o for o in ovs if o["type"] == "floor"), None)
    cp = next((o for o in ovs if o["type"] == "cap"), None)
    combos = []
    if fl:
        combos += [("floor", l, False) for l in range(fl["m"], K)] + [("floor", fl["m"], True)]
    if cp:
        combos += [("cap", l, False) for l in range(0, cp["m"] + 1)] + [("cap", cp["m"], True)]
    if fl and cp:
        mw = cp["m"] if card["winner"] == "cap" else fl["m"]
        combos += [("both", mw, False), ("both", mw, True)]
    for pat, l, bind in combos:
        hs = set()
        for t in range(24):
            ctx = {"ov": (pat, bind)}
            if card["sampler"] == "S2":
                ctx.update({"s2": True, "s2_counts": collections.Counter()})
            try:
                c = CS.build_case(card, l, rng, ctx, set())
            except CS.CaseFail:
                continue
            hs.add(RW.structure_hash(card, c["values"]))
            if len(hs) >= 3:
                break
        if len(hs) < 3:
            return (pat, l, bind)
    return None


def setup_card(plan: dict, held_out: bool, report: dict, start: int = 0) -> tuple[dict, list, set]:
    pack = plan["pack"]
    last = None
    # r1k: S2 HIGHEST cards must also pass the C16 capacity screen (c16_short), which few of their first 90 draws do
    # (build 14: S2-027 / S2-029 ended on fallback draws with no C16 row), so they get 270 draws; the strict cue set
    # still holds for the first 45 and the capacity screens up to the last 2 draws, as for every card. Draws past 90
    # use their own attempt numbers (no overlap with rubric re-draws, start = 100 x n).
    # r1l (G10 A/B S2 K3 + C.direction_C16_S1, build 15): S2-027 (K 3) passed no C16 screen in 268 draws and so ended on
    # the last-draw fallback, where every capacity screen is off: its level 1 had 3 distinct structures (13 units
    # failed, 38 of 60 rows; A level share, B quota, B HIGHEST K3). S1 HIGHEST cards also carry the scarce C16 'below'
    # side (S1 above 0.5515 with S1-009 L2 0/20, S1-003 L2-L3 0/23, S1-005 L3 0/12), so S1 HIGHEST gets the same
    # screen. Now S1 / S2 HIGHEST cards get 360 draws: the C16 screen holds for the first 180 only (a card that cannot
    # carry C16 at all, as K 3 often cannot under its cue set, is then taken without it), and the structure,
    # override and phrase screens still hold up to the last 2 draws.
    hi16 = plan["sampler"] in ("S1", "S2") and plan["mode"] == "highest" and not held_out
    n_att = 360 if hi16 else 90
    last_ = n_att - 2
    for k_ in range(n_att):
        attempt = start + k_ if k_ < 90 else 10000 * (1 + start // 100) + k_
        try:
            card = CD.build_card(plan, attempt)
            B.finalize(card, plan, pack, held_out)
            card["c1_elig_all"] = list(card["c1_elig"])
            card["c1_elig"] = c1_level_free(card, CD.rng_for("c1lf", plan["card_id"], attempt))
            rng = CD.rng_for("rows", plan["card_id"], attempt)
            card["cue_D_fallback"] = False
            if card["mode"] in ("ladder", "highest", "grid"):
                D_all = cue_feasible(card, rng)
                D = sorted(set(D_all) & CUE_SET)
                if set(D) != CUE_SET:
                    if k_ < 45:
                        raise CD.CardFail("cue balance: no sampler-wide cue count reachable at every level")
                    card["cue_D_fallback"] = True
                    # r1c: a fallback card still holds one absence-cue count reachable at every level, so its cue
                    # counts stay independent of level (6.3); a card with none is redrawn
                    D = D or sorted(D_all)[:1]
                    if not D:
                        if k_ < last_:
                            raise CD.CardFail("cue balance: no cue count reachable at every level")
                        D = [1]
                card["cue_D"] = sorted(D)
                if not held_out and card["mode"] in ("ladder", "highest"):
                    short = cap_short(card, plan, attempt) if k_ < last_ else None
                    if short is not None:
                        raise CD.CardFail(f"capacity: level {short[0]} cue {short[1]}: too few distinct case structures")
                    osh = ov_short(card, plan, attempt) if k_ < last_ else None
                    if osh is not None:
                        raise CD.CardFail(f"override pattern {osh[0]} level {osh[1]} binding {osh[2]}: not constructible")
                elif not card["cue_D_fallback"]:
                    ok = tot = 0
                    weak = 0
                    for l in range(card["K"]):
                        for T in sorted(CUE_SET):
                            cell = 0
                            for _ in range(4):
                                tot += 1
                                try:
                                    cc = CS.build_case(card, l, rng, {"ov": ("none", False), "T_lh": T,
                                                                     "c1": rng.random() < 0.3,
                                                                     "missing_want": rng.random() < 0.15,
                                                                     "s2": card["sampler"] == "S2"}, set())
                                    cell += bool(cc.get("cue_target_met"))
                                except CS.CaseFail:
                                    pass
                            ok += cell
                            weak += cell < 4
                    if (ok < 0.95 * tot or weak > 1) and k_ < 45:
                        raise CD.CardFail("cue balance: target counts missed too often")
            if card["sampler"] in ("S1", "S2", "S4") and card["mode"] in ("ladder", "highest", "grid"):
                # r1f: C1 keys must stay unmentioned at every level under the cue targets (T02), and no stated
                # factor value may concentrate on one level (G7 / 6.5); own rngs, so passing cards are unchanged
                if card.get("cue_D") and card["c1_elig"] and card.get("c15") != "key":
                    c1d = c1_cue_sets(card, CD.rng_for("c1cue", plan["card_id"], attempt))
                    card["c1_elig"] = [k for k in card["c1_elig"] if k in c1d]
                    card["c1_D"] = c1d
                if hi16 and k_ < 180:  # r1k: S2 HIGHEST C16 capacity (6.2), before the phrase screen; r1l: + S1, 180
                    c16s = c16_short(card, plan, attempt)
                    if c16s is not None:
                        raise CD.CardFail(f"C16 capacity: level {c16s[0]} cue {c16s[1]} c1 {c16s[2]}")
                if k_ < last_:  # r1g: same fallback point as the capacity checks (was 80)
                    pc = phrase_conc(card, CD.rng_for("pconc", plan["card_id"], attempt), _pconc_rows(plan))
                    if pc is not None:
                        raise CD.CardFail(f"phrase concentration {pc}")
            # r1i (G10 T02): C1 decisive capacity = share of levels where some C1 key can move the level when read as
            # present (LADDER c_{g+1}, HIGHEST any h_k above g, a floor above g); the C1 allocation weight (run_group)
            el_ = card["c1_elig"]
            card["c1_cap"] = (sum(bool(CS._c1_dec_cands(card, l, el_)) for l in range(card["K"])) / card["K"]) \
                if el_ and card["mode"] in ("ladder", "highest") else 0.0
            used = set()
            fewshot = []
            n_ex = 3 if plan.get("fewshot") else (rng.choice([1, 2]) if plan["defs_style"] == "one_line_examples" else 0)
            if n_ex:
                lv = rng.sample(range(card["K"]), min(n_ex, card["K"]))
                for l in lv:
                    wc = CS.worked_case(card, l, rng, used)
                    fewshot.append({"case": R.case_doc(card, wc, card["container"], for_example=True),
                                    "answer": card["levels"]["options"][l], "_gold": l, "_case": wc})
            card["fewshot"] = fewshot
            # probe row: render, parse and prove the card on the PARSED rubric (solver B side, 4.3)
            probe = CS.build_case(card, 0, rng, {"ov": ("none", False)}, set(used))
            row = B.build_row(card, probe, 0, "probe", {"group_id": "probe", "call_id": "probe"}, None,
                              [{"case": f["case"], "answer": f["answer"]} for f in fewshot] or None)
            PC = B.g3_check(row, card, pack, 0)
            SB.prove_card(PC, pack, cut_spacing=4 if card["mode"] == "cut" else 2)
            card["proof"] = "pass"
            report["card_attempts"][plan["card_id"]] = k_ + 1
            return card, fewshot, used
        except (CD.CardFail, CS.CaseFail, PS.ParseFail, SB.SolveFail, ValueError, KeyError) as e:
            last = f"{type(e).__name__}: {e}"
            report["card_fail_reasons"][f"{type(e).__name__}: {str(e)[:70]}"] += 1
            continue
    raise CD.CardFail(f"card {plan['card_id']} failed {n_att} attempts; last {last}")


def card_rows(card: dict, plan: dict, fewshot: list, used: set, n: int, inv_rows: int, report: dict,
              role: str) -> tuple[list, list]:
    pack = plan["pack"]
    rng = CD.rng_for("units", plan["card_id"])
    if role == "dev":  # mix-tuning dev items: singletons with exact per-card level quotas, no twins
        q = RW.level_quota(n, card["K"], rng)
        units = [{"type": "single", "levels": [l]} for l in range(card["K"]) for _ in range(q[l])]
        rng.shuffle(units)
    else:
        units = RW.plan_units(card, plan, n, rng, inv_rows if plan.get("attack") else 0)
    RW.override_targets(card, units, rng)
    fs = [{"case": f["case"], "answer": f["answer"]} for f in fewshot] or None
    rows, rels = [], []
    s = card["sampler"]
    s6_rr = collections.defaultdict(int)
    s6_counts = BAL["s6"][s]  # sampler-wide actual placements (updated in emit)
    s2_counts = BAL["s2"][s]  # sampler-wide placements and comparators (updated in emit)
    # G12 r1: one unit per structure on a card (worked cases included); planned twins share their base's hash
    used_sh = {RW.structure_hash(card, f["_case"]["values"]) for f in fewshot if f.get("_case")}
    used_vals = set()
    vec = lambda vals: frozenset(k for k in card.get("listed", []) if vals.get(k))
    used_vecs = {vec(f["_case"]["values"]) for f in fewshot if f.get("_case")} if card["mode"] in ("count", "points") \
        else set()
    if card["mode"] == "cut":
        used_vals = {f["_case"]["values"].get(card["qty"]) for f in fewshot if f.get("_case")}
    c11_dir = []  # this card's C11 direction once an at-row shows it (continuous CUT cards)
    cue_cnt = collections.Counter()  # r1c: base rows emitted per (cue kind, level)
    cue_off = [rng.randrange(2) for _ in range(card["K"])]
    rid = 0
    for ui, u in enumerate(units):
        gid = f"{card['card_id']}-g{ui:03d}"

        def ctx_for(level, ri, T_count=None):
            ctx = {"ov": u["ov"][ri] if "ov" in u else ("none", False)}
            if card["mode"] in ("ladder", "highest", "grid"):
                if s in ("S1", "S2", "S4"):
                    # r1c: unmentioned-factor rows steered to 25% of the sampler's rows (T02: 20-30%), carried by
                    # the LADDER / HIGHEST rows (the only C1 rows); the decision never looks at the level
                    # r1k (G10 D / T02): the card's one rate c1_r is applied per level ([unmentioned rows, rows] at this
                    # level). r1i's single per-card tally let levels where a row lost C1 (S2-029 levels 2-3: C16
                    # requests, cue target) be made up by other levels (levels 0-1: 30/30 unmentioned, 2-3: 0/29), so
                    # C1 and with it the stated absence-cue count tracked the level (G10 D S1 / S2 failed, build 14)
                    cu = card.setdefault("_c1ul", {}).setdefault(level, [0, 0])
                    # r1l (G10 E.unmentioned_S2 0.304, S4 0.298, S1 0.279 vs 0.255 planned): "cu[0] < r (n + 1)" made the
                    # first row of every level unmentioned whatever the rate (rounds up once per card x level, about
                    # +40 rows on S2 / S4); the row now asks for C1 when that keeps the level's count nearest r (n + 1)
                    ctx["c1"] = bool(card["c1_elig"]) and card.get("c1_r", 0) > 0 and \
                        cu[0] + 0.5 <= card["c1_r"] * (cu[1] + 1)
                    c1c = BAL["c1"][s]
                    n1 = c1c["dec"] + c1c["non"]
                    ctx["c1_decisive"] = (c1c["dec"] / n1) < 0.5 if n1 else (rng.random() < 0.5)
                if s in ("S1", "S2", "S4") and card["mode"] in ("ladder", "highest"):
                    # r1h (G10 6.2): S2 C16 above share 0.587 (LADDER gap floor gives above; HIGHEST rows rarely
                    # had a failing lower criterion), so a HIGHEST row the balance wants C16 on asks for one (soft).
                    # r1j: build 10 C16 above S1 0.674 / S2 0.670 (LADDER always "above", HIGHEST always "below";
                    # "or" carrier rungs made higher LADDER criteria true more often): every S1 / S2 / S4 LADDER or
                    # HIGHEST row asks for C16 present / absent as c16_want says (soft, f7case)
                    w16 = c16_want(card, level)
                    if w16 is not None:
                        ctx["c16_req"] = w16
                if card.get("cue_D"):  # r1c: cue targets cycle per level (exactly level-independent, 6.3)
                    D_ = card["cue_D"]
                    ctx["T_lh"] = D_[(cue_off[level] + cue_cnt[("lh", level)]) % len(D_)]
                ctx["missing_want"] = rng.random() < 0.15
            if s == "S2":
                ctx["s2"] = True
                ctx["s2_counts"] = s2_counts
            if s == "S6":
                feas = [pl for pl in ("at", "below", "above", "interior")
                        if RW.place_cut(card, random.Random(0), level, pl, None, avoid=used_vals) is not None]
                if not feas:
                    feas = ["interior"]
                if c11_dir and "at" in feas:
                    # G10 r1c (6.2 T16): C11 occurs on at-cut rows of continuous cards and its direction is fixed per
                    # card (side x rising), so at-rows go to the cards whose C11 direction the sampler lacks
                    c11 = BAL["dir"][(s, "C11")]
                    gap = c11[c11_dir[0]] - c11["below" if c11_dir[0] == "above" else "above"]
                    if gap >= 2 and len(feas) > 1:
                        feas = [p_ for p_ in feas if p_ != "at"]
                    elif gap <= -2:
                        feas = ["at"]
                tot = sum(s6_counts.values()) + 1
                tgt = {"at": 0.33, "below": 0.235, "above": 0.235, "interior": 0.20}
                best = max(tgt[p] * tot - s6_counts[p] for p in feas)
                pl = rng.choice([p for p in feas if tgt[p] * tot - s6_counts[p] >= best - 1e-9])
                ctx["avoid_vals"] = used_vals
                ctx["placement"] = pl
                ctx["cut_idx"] = s6_rr[(level, pl)] % max(1, card["K"] - 1)
                s6_rr[(level, pl)] += 1
            if card["mode"] in ("count", "points"):
                ctx["at_cut"] = rng.random() < 0.45
                ctx["T"] = T_count if T_count is not None else card["cue_T"][(cue_off[level] + cue_cnt[("ct", level)]) % 2]
                ctx["missing_want"] = rng.random() < (0.25 if s == "S3" else 0.15)
                ctx["repeat_want"] = rng.random() < 0.15
                ctx["avoid_vecs"] = used_vecs
            if card.get("c15"):  # r1d: C15 two-way direction steering (which absent key is the missing entry)
                c15 = BAL["dir"][(s, "C15")]
                ctx["c15_dir"] = ("below" if c15["above"] > c15["below"] else
                                  "above" if c15["below"] > c15["above"] else None)
            return ctx

        def make(level, ri, tries=8, T_count=None):
            # G10/G12 r1: up to ncand valid candidates for this level whose structure is new on the card; keep the
            # one that best moves the sampler-wide balances (conv directions, C1 decisive share) toward target.
            # r1c: the row's design draws (cue target, C1, missing / repeat wants, placement) are made once per row
            # and kept across the candidate draws, so a level's structure capacity never reshapes their mix; only
            # the last third of the draws (logged) redraws them.
            last = None
            best = None
            ncand = 1 if card["mode"] == "cut" else (4 if bal_off(card) else 2)
            got = 0
            ctx0 = ctx_for(level, ri, T_count)
            for t in range(3 * tries):
                trial = set(used)  # names are committed only for the chosen candidate (no id-pool drain)
                if t == 2 * tries:
                    report["design_redraw"] = report.get("design_redraw", 0) + 1
                ctx_t = dict(ctx0) if t < 2 * tries else ctx_for(level, ri, T_count)
                try:
                    c = CS.build_case(card, level, rng, ctx_t, trial)
                except CS.CaseFail as e:
                    last = e
                    continue
                if RW.structure_hash(card, c["values"]) in used_sh:
                    last = CS.CaseFail("structure already used on card")
                    report["struct_redraw"] += 1
                    continue
                sc = bal_score(card, c, level)
                # r1k (T02): a candidate whose C1 status matches the row's request goes first, so the C1 decisive
                # steering (bal_score) never swaps an unmentioned row for a stated one on the levels where its C1 is
                # the unwanted kind (S1-009: unmentioned 4/9/13 of 20 by level, build 14)
                if card["c1_elig"] and bool(c.get("unmentioned")) == bool(ctx_t.get("c1")):
                    sc += 10.0
                if best is None or sc > best[0]:
                    best = (sc, c, trial)
                got += 1
                if got >= ncand:
                    break
            if best is None:
                # r1l (G10 B.per_card_quota, build 16: S4-073 level 1 lost 2 units to 'structure already used on
                # card', 11 rows vs 13-14): a row whose 3 x tries draws found no new structure was dropped, so the card
                # missed its exact level quota. Such a row now gets more draws, easing its soft design wants step by
                # step: C16 request and missing-entry want off, then the C1 request off, then the card's other cue
                # targets. Rows that found a structure before are drawn exactly as before.
                T0 = ctx0.get("T_lh")
                alts = [T_ for T_ in (card.get("cue_D") or []) if T_ != T0]
                for ph in range(3):
                    if ph == 2 and not alts:
                        break
                    for t in range(2 * tries):
                        trial = set(used)
                        ctx_t = dict(ctx0)
                        ctx_t.pop("c16_req", None)
                        ctx_t["missing_want"] = False
                        if ph >= 1:
                            ctx_t["c1"] = False
                        if ph == 2:
                            ctx_t["T_lh"] = alts[t % len(alts)]
                        try:
                            c = CS.build_case(card, level, rng, ctx_t, trial)
                        except CS.CaseFail as e:
                            last = e
                            continue
                        if RW.structure_hash(card, c["values"]) in used_sh:
                            report["struct_redraw"] += 1
                            continue
                        best = (0.0, c, trial)
                        break
                    if best is not None:
                        report["struct_relaxed"] = report.get("struct_relaxed", 0) + 1
                        report.setdefault("struct_relaxed_phase", collections.Counter())[ph] += 1
                        break
            if best is None:
                report["struct_exhausted"][f"{card['sampler']}|{card['mode']}"] += 1
                raise CS.CaseFail(f"case for level {level}: {last}")
            used.update(best[2])
            return best[1]

        def emit(case, gold, twin, call_id, **kw):
            nonlocal rid
            row_id = f"{card['card_id']}-{rid:03d}"
            rid += 1
            last = None
            for t in range(4):
                try:
                    row = B.build_row(card, case, gold, row_id, {"group_id": gid, "call_id": call_id}, twin, fs,
                                      role=role, **kw)
                    B.g3_check(row, card, pack, gold)
                    row["_emit"] = {"case": case, "gold": gold, "twin": twin, "kw": dict(kw)}
                    rows.append(row)
                    bal_update(card, row, gold)
                    if twin is None:
                        cue_cnt[("lh", gold)] += 1
                        cue_cnt[("ct", gold)] += 1
                    if not c11_dir:
                        c11_dir.extend(("above" if e["alt_level"] > gold else "below") for e in row["meta"]["edge"]
                                       if e["kind"] == "conv" and e["conv"] == "C11")
                    used_sh.add(row["meta"]["structure_hash"])
                    if card["mode"] == "cut":
                        used_vals.add(case["values"].get(card["qty"]))
                    if card["mode"] in ("count", "points"):
                        used_vecs.add(vec(case["values"]))
                    return row
                except (CS.CaseFail, PS.ParseFail, SB.SolveFail, KeyError, ValueError) as e:
                    last = e
                    report["row_fail_reasons"][f"{type(e).__name__}: {str(e)[:80]}"] += 1
                    if kw.get("style_id"):
                        kw = dict(kw, style_id=None)
            raise CS.CaseFail(f"row {row_id}: {last}")

        try:
            if u["type"] == "flip":
                l1, l2 = u["levels"]
                twin = None
                Tc = None
                if card["mode"] in ("count", "points"):
                    delta = -1 if ((l2 > l1) == card["rising"]) else 1  # twin's absence-cue change
                    Tc = card["cue_T"][1] if delta == -1 else card["cue_T"][0]
                for t in range(12):
                    base = make(l1, 0, T_count=Tc)
                    twin = CS.flip_twin(card, base, l2, rng, used,
                                        {"struct_used": lambda v2: RW.structure_hash(card, v2) in used_sh})
                    if twin is not None and RW.structure_hash(card, twin["values"]) in used_sh and t < 11:
                        twin = None  # G12 r1: the twin's structure must be new on the card too
                    if twin is not None and card.get("cue_D") and t < 10:
                        # keep the twin's absence-cue count inside the card's cue set (6.3)
                        tw_facts = CS.case_cues(twin)
                        tw_ok = (card.get("c1_D") or {}).get(CS.c1_key(twin)) if twin.get("unmentioned") else None
                        if tw_facts not in (tw_ok or card["cue_D"]):  # r1f: C1 twins use the C1 stated set
                            twin = None
                    if twin is not None:
                        break
                if twin is None:
                    report["flip_fallback"] += 1
                    b = emit(make(l1, 0), l1, None, f"{gid}-a")
                    emit(make(l2, 1), l2, None, f"{gid}-b")
                    continue
                b = emit(base, l1, None, f"{gid}-a")
                emit(twin, M.final_level(card, twin["values"]), {"of": b["id"], "kind": "fact_flip",
                                                                  "variant": "fact_flip"}, f"{gid}-b",
                     style_id=b["meta"]["format_style"])
            elif u["type"] == "equiv":
                l = u["levels"][0]
                base = make(l, 0)
                b = emit(base, l, None, gid)
                st = b["meta"]["format_style"]
                wd = next(w for w in card["wordings"] if b["meta"]["wording_id"].endswith("." + w["id"]))
                choices = ["rename", "reorder"] + (["listing"] if plan["defs_style"] in ("rubric_table", "short") or
                                                   card["mode"] == "grid" else [])
                kind = rng.choice(choices)
                if kind == "reorder" and len([f for f in base["facts"] if f["kind"] != "repeat"]) < 2:
                    kind = "rename"
                qi = __import__("f7lex").QUESTIONS.index(next(q for q in __import__("f7lex").QUESTIONS
                                                               if _q_match(q, b, base["subject"])))
                if kind == "rename":
                    tw = CS.rename_case(card, base, rng, used)
                    t = emit(tw, l, {"of": b["id"], "kind": "equiv", "variant": "rename"}, gid, style_id=st,
                             wording=wd, qi=qi)
                elif kind == "reorder":
                    # G12 r1d: a reorder twin must change the rendered case (some containers print fields in a
                    # fixed order); otherwise it would be an exact duplicate of its base, so a rename twin is used
                    tw = None
                    for _ in range(6):
                        cand_ = CS.reorder_case(base, rng)
                        try:
                            f_ = B.row_fields(card, cand_, b["id"], b["id"], fewshot=fs, style_id=st, wording=wd,
                                              qi=qi)[0]
                        except CS.CaseFail:
                            continue
                        if f_["state"] != b["state"]:
                            tw = cand_
                            break
                    if tw is None:
                        report["reorder_to_rename"] = report.get("reorder_to_rename", 0) + 1
                        tw = CS.rename_case(card, base, rng, used)
                        t = emit(tw, l, {"of": b["id"], "kind": "equiv", "variant": "rename"}, gid, style_id=st,
                                 wording=wd, qi=qi)
                    else:
                        t = emit(tw, l, {"of": b["id"], "kind": "equiv", "variant": "reorder"}, gid, style_id=st,
                                 wording=wd, qi=qi)
                else:
                    t = emit(base, l, {"of": b["id"], "kind": "equiv", "variant": "listing_reversal"}, gid,
                             style_id=st, wording=wd, qi=qi, descending=True)
                rels.append({"type": "equiv", "a": b["id"], "b": t["id"]})
            elif u["type"] == "inv":
                l = u["levels"][0]
                base = make(l, 0)
                b = emit(base, l, None, gid)
                st = b["meta"]["format_style"]
                wd = next(w for w in card["wordings"] if b["meta"]["wording_id"].endswith("." + w["id"]))
                qi = __import__("f7lex").QUESTIONS.index(next(q for q in __import__("f7lex").QUESTIONS
                                                               if _q_match(q, b, base["subject"])))
                tw = CS.add_injection(card, base, rng, l)
                t = emit(tw, l, {"of": b["id"], "kind": "inv", "variant": "inv"}, gid, style_id=st, wording=wd, qi=qi)
                rels.append({"type": "inv", "a": b["id"], "b": t["id"]})
            else:
                l = u["levels"][0]
                emit(make(l, 0), l, None, gid)
        except CS.CaseFail as e:
            report["unit_fail"][f"{u['type']}: {str(e)[:80]}"] += 1
    nd_repair(card, plan, rows, fs, role, report)
    wording_cover(card, plan, rows, fs, role, report)
    return rows, rels


def wording_cover(card: dict, plan: dict, rows: list, fs, role: str, report: dict) -> None:
    """G11 r1d: every card's rows use >= 5 of its instruction wordings (G0 / data spec G11 count). Small cards (S6, 8-15
    rows) can miss that with per-row hashed picks, so units (one call_id: a base and its twins, which share the
    wording) of an over-used wording are re-rendered with an unused one. Cases, labels, styles and questions stay."""
    need = min(5, len(card["wordings"]))
    wid = lambda r: next((w["id"] for w in card["wordings"] if r["meta"]["wording_id"].endswith("." + w["id"])), None)
    for _ in range(12):
        units = collections.defaultdict(list)
        for i, r in enumerate(rows):
            units[r["call_id"]].append(i)
        uw = {u: wid(rows[ix[0]]) for u, ix in units.items()}
        cnt = collections.Counter(uw.values())
        if len(cnt) >= need:
            return
        unused = [w for w in card["wordings"] if w["id"] not in cnt]
        movable = [u for u, w in uw.items() if cnt[w] >= 2 and all(wid(rows[i]) == w for i in units[u])]
        if not unused or not movable:
            break
        movable.sort(key=lambda u: (-cnt[uw[u]], u))
        done = False
        for u in movable:
            new = {}
            try:
                for i in units[u]:
                    r = rows[i]
                    e = r["_emit"]
                    kw = dict(e["kw"], wording=unused[0], style_id=r["meta"]["format_style"])
                    nr = B.build_row(card, e["case"], e["gold"], r["id"], {"group_id": r["group_id"],
                                     "call_id": r["call_id"]}, e["twin"], fs, role=role, **kw)
                    B.g3_check(nr, card, plan["pack"], e["gold"])
                    if nr["meta"]["format_style"] != r["meta"]["format_style"]:
                        raise CS.CaseFail("style fallback")
                    nr["_emit"] = dict(e, kw=kw)
                    new[i] = nr
            except (CS.CaseFail, PS.ParseFail, SB.SolveFail, KeyError, ValueError):
                continue
            old = {i: rows[i] for i in new}
            n0 = len(nd_pairs(rows, 0.8))
            for i, nr in new.items():
                rows[i] = nr
            if len(nd_pairs(rows, 0.8)) > n0:  # never trade a wording for a near-duplicate pair
                for i, r in old.items():
                    rows[i] = r
                continue
            report["wording_cover"] = report.get("wording_cover", 0) + 1
            done = True
            break
        if not done:
            break
    report["wording_cover_short"] = report.get("wording_cover_short", 0) + 1


# ---- G12 repair r1c: near-duplicate surface forms on a card ---------------------------------------------------------
# Rows of different units on one card must not share most of their row-level text (G12 MinHash near-dups: word 5-gram
# Jaccard over the instruction paragraphs that are not card content, i.e. present on < 50% of the card's rows, plus
# `state`). Cases and labels never change here: a unit whose rows collide with an earlier unit is re-rendered with a
# fresh draw of format style, wording and question (its twins follow the base as at emit time).
ND_THR = 0.72
_TOK = __import__("re").compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
_PARA = __import__("re").compile(r"\n\s*\n")


def _paras(ins: str) -> list:
    return [p for p in _PARA.split(ins.strip()) if p.strip()]


def _shingles(text: str, k: int = 5) -> set:
    t = _TOK.findall(text.lower())
    return {" ".join(t[i:i + k]) for i in range(max(1, len(t) - k + 1))}


def nd_units(rows: list) -> dict:
    ids = {r["id"] for r in rows}
    unit = {r["id"]: r["call_id"] for r in rows}
    for r in rows:
        if r["meta"].get("twin_kind") == "fact_flip" and r["meta"].get("twin_of") in ids:
            unit[r["id"]] = unit[r["meta"]["twin_of"]] = "ff:" + r["meta"]["twin_of"]
    return unit


def nd_pairs(rows: list, thr: float = ND_THR) -> list:
    """(i, j) row-index pairs of different units with row-level 5-gram Jaccard >= thr (j > i)."""
    cnt = collections.Counter()
    for r in rows:
        cnt.update(set(_paras(r["instructions"])))
    keep = {p for p, k in cnt.items() if k >= 0.5 * len(rows)}
    sh = [_shingles("\n\n".join(p for p in _paras(r["instructions"]) if p not in keep) + "\n" + r["state"])
          for r in rows]
    unit = nd_units(rows)
    out = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if unit[rows[i]["id"]] == unit[rows[j]["id"]]:
                continue
            a, b = sh[i], sh[j]
            if len(a & b) >= thr * len(a | b):
                out.append((i, j))
    return out


def _nd_sim(rows: list, new: dict) -> float:
    """r1l: highest row-level 5-gram Jaccard (nd_pairs text) between the re-rendered rows `new` {index: row} and the
    rows of every other unit of the card."""
    cnt = collections.Counter()
    for r in rows:
        cnt.update(set(_paras(r["instructions"])))
    keep = {p for p, k in cnt.items() if k >= 0.5 * len(rows)}
    shf = lambda r: _shingles("\n\n".join(p for p in _paras(r["instructions"]) if p not in keep) + "\n" + r["state"])
    unit = nd_units(rows)
    us = {unit[rows[i]["id"]] for i in new}
    others = [shf(r) for r in rows if unit[r["id"]] not in us]
    best = 0.0
    for nr in new.values():
        a = shf(nr)
        for b in others:
            best = max(best, len(a & b) / max(1, len(a | b)))
    return best


def _rerender_unit(card: dict, plan: dict, rows: list, idxs: list, fs, role: str, rng) -> bool:
    """r1l (G12 build 15: S2-021-008 / -010 at 0.82 left after 12 rounds): a re-render was applied as soon as it
    built, whatever its similarity, so a card with few wordings could keep drawing near-duplicate renders. Now up to
    12 renders are built and the one with the lowest similarity to the card's other units is kept (the first one
    under ND_THR ends the search)."""
    import f7lex as LX
    base_i = next((i for i in idxs if rows[i]["meta"].get("twin_kind") in (None, "")), idxs[0])
    pick = None
    for t in range(12):
        # r1c: only S6 (no absence cues) may change style here; elsewhere the row keeps its style, so a re-render
        # never moves state rendering (absence markers) between levels
        sid = rng.choice(sorted(card["style_set"])) if card["sampler"] == "S6" else rows[base_i]["meta"]["format_style"]
        wd = rng.choice(card["wordings"])
        qi = rng.randrange(len(LX.QUESTIONS))
        new = {}
        try:
            for i in [base_i] + [i for i in idxs if i != base_i]:
                r = rows[i]
                e = r["_emit"]
                kw = dict(e["kw"])
                if r["meta"].get("twin_kind") == "fact_flip":  # own wording and question, the base's style (emit)
                    kw.update(style_id=sid, wording=rng.choice(card["wordings"]), qi=rng.randrange(len(LX.QUESTIONS)))
                else:
                    kw.update(style_id=sid, wording=wd, qi=qi)
                nr = B.build_row(card, e["case"], e["gold"], r["id"], {"group_id": r["group_id"], "call_id": r["call_id"]},
                                 e["twin"], fs, role=role, **kw)
                B.g3_check(nr, card, plan["pack"], e["gold"])
                if nr["meta"]["format_style"] != sid:
                    raise CS.CaseFail("style fallback")
                nr["_emit"] = dict(e, kw=kw)
                new[i] = nr
        except (CS.CaseFail, PS.ParseFail, SB.SolveFail, KeyError, ValueError):
            continue
        sim = _nd_sim(rows, new)
        if pick is None or sim < pick[0]:
            pick = (sim, new)
        if sim < ND_THR:
            break
    if pick is None:
        return False
    for i, nr in pick[1].items():
        rows[i] = nr
    return True


def nd_repair(card: dict, plan: dict, rows: list, fs, role: str, report: dict) -> None:
    if len(rows) < 2:
        return
    rng = CD.rng_for("nd", plan["card_id"])
    for it in range(12):
        pairs = nd_pairs(rows)
        if not pairs:
            return
        unit = nd_units(rows)
        members = collections.defaultdict(list)
        for i, r in enumerate(rows):
            members[unit[r["id"]]].append(i)
        redo = []
        for i, j in pairs:
            u = unit[rows[j if it % 2 == 0 else i]["id"]]  # r1l: odd rounds re-render the other unit of the pair
            if u not in redo:
                redo.append(u)
        for u in redo:
            report["nd_rerender"] = report.get("nd_rerender", 0) + 1
            _rerender_unit(card, plan, rows, members[u], fs, role, rng)
    left = nd_pairs(rows, 0.8)
    if left:
        report["nd_left_pairs"] = report.get("nd_left_pairs", 0) + len(left)


def _q_match(q, row, S):
    return q.format(S=S) in row["instructions"]


def run(kind: str, cards_per_sampler: int = 16, rows_per_card: int | None = None, tag: str | None = None):
    t0 = time.time()
    report = {"card_attempts": {}, "card_fail_reasons": collections.Counter(), "row_fail_reasons": collections.Counter(),
              "unit_fail": collections.Counter(), "flip_fallback": 0, "struct_redraw": 0,
              "struct_exhausted": collections.Counter()}
    bal_reset()
    if kind == "mixdev":
        packs = list(PK.heldout_packs())
        plans = CD.s5_plan(packs, B.SEED, n_cards=10)
        held = True
        role = "dev"
        per_card = {p["card_id"]: 40 for p in plans}
    else:
        packs, plans = train_plans(kind, cards_per_sampler, tag)
        held = False
        role = "train" if kind == "candidates" else "qc"
        per_card = {p["card_id"]: (rows_per_card or p["n"]) for p in plans}  # r1b: planned rows (CD.plan_rows)
    groups = []
    for plan in plans:  # r1c: S3 and S4 (both with COUNT cards) share one group, so rubrics are unique across both
        gk = "S3+S4" if plan["sampler"] in ("S3", "S4") else plan["sampler"]
        if not groups or groups[-1][0] != gk:
            groups.append((gk, []))
        groups[-1][1].append(plan)
    workers = int(__import__("os").environ.get("F7_WORKERS", "1"))
    if workers > 1:
        # card set-up is per card (seeded by card_id) and samplers are independent (BAL, quotas per sampler), so both
        # stages run in parallel with the same rows as a serial run
        import multiprocessing as mp
        with mp.get_context("fork").Pool(workers) as pool_:
            setups = pool_.starmap(_setup_one, [(pl, held) for pl in plans], chunksize=1)
            sres = _setup_results(kind, plans, setups, per_card, report)
            args = [(kind, g, held, role, {p["card_id"]: per_card[p["card_id"]] for p in g},
                     {p["card_id"]: sres[p["card_id"]] for p in g}) for _, g in groups]
            parts = pool_.starmap(run_group, args, chunksize=1)
    elif kind == "qc":  # r2: set-ups first, as in the parallel run, so dropped cards' rows are re-planned the same way
        sres = _setup_results(kind, plans, [_setup_one(pl, held) for pl in plans], per_card, report)
        parts = [run_group(kind, g, held, role, {p["card_id"]: per_card[p["card_id"]] for p in g},
                           {p["card_id"]: sres[p["card_id"]] for p in g}) for _, g in groups]
    else:
        parts = [run_group(kind, g, held, role, {p["card_id"]: per_card[p["card_id"]] for p in g}) for _, g in groups]
    out_rows, out_rels, cards_out = [], [], []
    for rows_, rels_, cards_, rep_ in parts:
        out_rows += rows_
        out_rels += rels_
        cards_out += cards_
        _merge_report(report, rep_)
    B.log(f"{kind}: all groups done, {len(out_rows)} rows, {time.time() - t0:.0f}s")
    return out_rows, out_rels, cards_out, report


def _merge_report(report: dict, rep_: dict) -> None:
    for k, v in rep_.items():
        if isinstance(v, (collections.Counter, dict)):
            report.setdefault(k, collections.Counter() if isinstance(v, collections.Counter) else {}).update(v)
        else:
            report[k] = report.get(k, 0) + v


def _new_report() -> dict:
    return {"card_attempts": {}, "card_fail_reasons": collections.Counter(), "row_fail_reasons": collections.Counter(),
            "unit_fail": collections.Counter(), "flip_fallback": 0, "struct_redraw": 0,
            "struct_exhausted": collections.Counter(), "nd_rerender": 0, "nd_left_pairs": 0}


def train_plans(kind: str, cards_per_sampler: int = 16, tag: str | None = None) -> tuple[list, list]:
    """Training-pack card plans for candidates / qc (also used by f7finalize to rebuild a card). r2: the qc sample plans
    QC_SAMPLER_ROWS rows per sampler (G6 >= 5,000 rows); candidates keep CD.plan_rows' default (family_plan)."""
    packs = list(PK.training_packs())
    tg = tag or ("r1" if kind == "candidates" else "qc")
    seed = B.SEED if kind == "candidates" else B.SEED + 7
    plans = CD.family_plan(packs, cards_per_sampler, seed, tag=tg, packs_s6=list(PK.training_packs3()),
                           counts=dict(CD.R1B_CARDS))
    if kind == "qc":  # ladder / highest cards absorb the difference (CD.plan_rows)
        CD.plan_rows(plans, QC_SAMPLER_ROWS)
    return packs, plans


def _setup_results(kind: str, plans: list, setups: list, per_card: dict, report: dict) -> dict:
    """Merge card set-up results. r2 (G6 size, qc only): a card whose set-up fails (build 17: F7-qc-S2-029) leaves its
    planned rows to the surviving ladder / highest cards of its sampler (CD.plan_rows over the survivors)."""
    sres = {}
    for pl, (res_, rep_) in zip(plans, setups):
        sres[pl["card_id"]] = res_
        _merge_report(report, rep_)
    if kind == "qc":
        alive = [p for p in plans if sres[p["card_id"]][0] == "ok"]
        if len(alive) < len(plans):
            CD.plan_rows(alive, QC_SAMPLER_ROWS)
            for p in alive:
                per_card[p["card_id"]] = p["n"]
            B.log(f"qc: {len(plans) - len(alive)} card(s) dropped at set-up; rows re-planned over {len(alive)} cards")
    return sres


def _setup_one(plan: dict, held: bool):
    rep = _new_report()
    try:
        return ("ok",) + tuple(setup_card(plan, held, rep)), rep
    except CD.CardFail as e:
        return ("fail", str(e)), rep


def run_group(kind: str, plans: list, held: bool, role: str, per_card: dict, setups: dict | None = None):
    """Set up and fill the cards of one sampler (sampler-wide balances in BAL are per sampler)."""
    t0 = time.time()
    report = _new_report()
    bal_reset()
    out_rows, out_rels, cards_out = [], [], []
    ready = []
    for plan in plans:
        res_ = setups[plan["card_id"]] if setups else None
        if res_ is None:
            rep_ = _new_report()
            res_, rep_ = _setup_one(plan, held)
            _merge_report(report, rep_)
        if res_[0] == "ok":
            ready.append((plan,) + tuple(res_[1:]))
        else:
            report["unit_fail"][f"card dropped: {res_[1][:80]}"] += 1
            B.log(f"{kind}: card {plan['card_id']} dropped: {res_[1][:100]}")
    # G12 r1c: no two cards of a group share a canonical rubric (structure hashes abstract names and pack nouns, so
    # two cards with the same rubric would give different surface forms of one structure); a repeat is set up again
    seen_rub = set()
    seen_keys = set()  # r1d: COUNT band layouts in use (K, m, rising, bands); a re-draw avoids them by construction
    for idx, (plan, card, fewshot, used) in enumerate(ready):
        rh = RW.structure_hash(card, {})
        tries = 0
        while rh in seen_rub and tries < 12:  # r1d: 12 re-draws (was 4)
            tries += 1
            report["rubric_redraw"] = report.get("rubric_redraw", 0) + 1
            plan["_avoid_rub"] = set(seen_keys)
            try:
                card, fewshot, used = setup_card(plan, held, report, start=100 * tries)
            except CD.CardFail:
                continue
            finally:
                plan.pop("_avoid_rub", None)
            rh = RW.structure_hash(card, {})
        if card.get("rub_key"):
            seen_keys.add(card["rub_key"])
        ready[idx] = (plan, card, fewshot, used)
        if rh in seen_rub:
            report["rubric_dup_left"] = report.get("rubric_dup_left", 0) + 1
        seen_rub.add(rh)
    B.log(f"{kind}: {len(ready)} cards set up and proved, {time.time() - t0:.0f}s")
    # C1 unmentioned factors on 20-30% of each of S1, S2, S4 (T02): rate per eligible card
    for s_ in ("S1", "S2", "S4"):
        cs = [c for p, c, _, _ in ready if p["sampler"] == s_ and c["mode"] in ("ladder", "highest")]
        el = [c for c in cs if c["c1_elig"]]
        for c in el:
            c["c1_rate"] = min(0.9, 0.33 * len(cs) / max(1, len(el)) / 0.8)
        n_all = sum(per_card[p["card_id"]] for p, c, _, _ in ready if p["sampler"] == s_)
        n_lh = sum(per_card[p["card_id"]] for p, c, _, _ in ready if p["sampler"] == s_ and c["mode"] in ("ladder", "highest"))
        for c in cs:
            c["c1_target"] = min(0.9, 0.25 * n_all / max(1, n_lh))
        # r1i (G10 T02): unmentioned rows go to the cards whose C1 keys can be decisive on most levels. Each card's
        # rate is fixed before its rows and never looks at a row's level (T02 "drawn independently of level"): rate
        # = lam * capacity (<= 0.85), lam set so the sampler's unmentioned rows come to C1_SHARE of its rows
        ws = [(c, per_card[p["card_id"]], c.get("c1_cap", 0.0)) for p, c, _, _ in ready
              if p["sampler"] == s_ and c["mode"] in ("ladder", "highest") and c["c1_elig"] and c.get("c1_cap", 0) > 0
              and c.get("c15") != "key"]  # r1j: a key card's left-out factor is a C15 missing entry, never C1 (T02)
        need = C1_SHARE * n_all
        lo, hi = 0.0, 50.0
        for _ in range(60):
            lam = (lo + hi) / 2
            got = sum(n * min(0.85, lam * cap * cap) for c, n, cap in ws)
            lo, hi = (lam, hi) if got < need else (lo, lam)
        for c, n, cap in ws:
            c["c1_r"] = min(0.85, hi * cap * cap)
        B.log(f"{kind}: {s_} C1 carriers {len(ws)}, caps {sorted(round(cap, 2) for _, _, cap in ws)}, "
              f"rows {sum(n for _, n, _ in ws)}, planned unmentioned {sum(n * c['c1_r'] for c, n, _ in ws):.0f}/{n_all}")
    for i, (plan, card, fewshot, used) in enumerate(ready):
        n = per_card[plan["card_id"]]
        n_attack = sum(1 for p in plans if p["sampler"] == plan["sampler"] and p.get("attack"))
        n_samp = sum(per_card[p["card_id"]] for p in plans if p["sampler"] == plan["sampler"])
        inv_rows = max(1, round(0.05 * n_samp / max(1, n_attack))) if plan.get("attack") else 0
        rows, rels = card_rows(card, plan, fewshot, used, n, inv_rows, report, role)
        for r in rows:
            r.pop("_emit", None)
        out_rows += rows
        out_rels += rels
        cards_out.append(card_def(card, plan))
        if (i + 1) % 8 == 0:
            B.log(f"{kind}: {i + 1}/{len(ready)} cards, {len(out_rows)} rows, {time.time() - t0:.0f}s")
    return out_rows, out_rels, cards_out, report


def card_def(card: dict, plan: dict) -> dict:
    items = {}
    for k, it in card["items"].items():
        d = {x: (str(y) if hasattr(y, "denominator") else y) for x, y in it.items() if x not in ("concept",)}
        d["concept_set"] = it.get("concept")
        items[k] = d
    return {"card_id": card["card_id"], "sampler": card["sampler"], "pack": card["pack_id"], "mode": card["mode"],
            "K": card["K"], "depth": card["depth"], "deep": card["deep"], "defs_style": plan["defs_style"],
            "fewshot": plan.get("fewshot"), "n_worked": len(card.get("fewshot") or []), "dv": card["dv"],
            "ft": card["ft"] if card.get("fewshot") else None, "container": card["container"],
            "style_set": card["style_set"], "wording_family": plan["wording_family"],
            "wordings": [w["id"] for w in card["wordings"]], "level_word": plan["level_word"],
            "options": card["levels"]["options"], "name_form": plan["name_form"], "reversed": plan["reversed"],
            "override": plan.get("ov_set"), "attack": plan.get("attack"), "c15": card.get("c15"),
            "c21": card.get("c21"), "c1_form": card["c1_form"], "items": items, "proof": card.get("proof"),
            "fillers": [f["term"] for f in card.get("filler_pool", [])][:0], "persona_seed": PK.load_persona(card["pack_id"]),
            "second_unit": None}


def strip_private(row: dict) -> dict:
    return {k: v for k, v in row.items() if not k.startswith("_")}


def write_jsonl(path: Path, rows: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "smoke":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        rows, rels, cards, rep = run("candidates", cards_per_sampler=16, rows_per_card=n, tag="smoke")
        print(len(rows), json.dumps({k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in rep.items()
                                     if k != "card_attempts"}, indent=1)[:4000])
        write_jsonl(B.TMP / "smoke_rows.jsonl", [strip_private(r) for r in rows])
        sys.exit(0)
    rows, rels, cards, rep = run(kind)
    name = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5"}[kind]
    write_jsonl(B.OUT / f"{name}.jsonl", [strip_private(r) for r in rows])
    write_jsonl(B.OUT / f"{name}.relations.jsonl", rels)
    write_jsonl(B.OUT / f"{name}.cards.jsonl", cards)
    rep2 = {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in rep.items()}
    rep2["rows"] = len(rows)
    rep2["relations"] = len(rels)
    rep2["cards"] = len(cards)
    json.dump(rep2, open(B.TMP / f"report_{name}.json", "w"), indent=1, default=str)
    B.log(f"{kind}: done {len(rows)} rows, {len(cards)} cards, {len(rels)} relations")
