"""T63 NEAR plan: quota cells (group types, ops, flips, queried age / downloads classes, ladder mechanism decorations).

Design (G0-lite section 4 / K5-K7 / K13; resized 500 -> 550 rows by Opus ruling Q5, 18 Oct, before any pool rows):
  * 550 rows = YES 275 / NO 275; NM-T1..NM-T7 33 YES rows each (12%), NM-T8 44 YES rows (16%): every id inside 5-25% of YES.
  * group types: pair_a 83 groups (166 rows: squat YES + legit NO = NM-R1), yes_flip 66 groups (132 rows: pub 22 / fork 22 / age 22
    flips = NM-R2 / NM-R2 / NM-R3), t8_flip 44 groups (88 rows: own_org / not_reserved / internal_first / internal_query),
    single_yes 82, single_no 82 (NM-R2 66 + NM-R4 16). 70% of the rows are in a pair (bar 50%). NM-R1..R3 = 94% of NO (bar 92%), NM-R4 6% (<= 8%).
    (At 500 rows the counts were 75 / 60 / 40 / 75 / 75; the K13 shares above are unchanged by the resize.)
  * K6 (queried-package metadata equal across labels within 5 pp per class): flip pairs keep the queried package untouched, so both
    labels share its (age, downloads); the pair-A squat (young) is mirrored by NO singles (young), the pair-A legit side (A2/A3, D2)
    by YES singles (A2, D2). Planned marginals are asserted by a CPU test; the gate measures the built rows.
Quota cells are oversampled by 15% (plan.OVERSAMPLE) at generation; the caller scales `rows` and the plan truncates after drops.
"""
from LP_COMMON import plan as plan_mod
from LP_COMMON import util

from . import config as C
from . import near_build as NB

# group counts for 550 rows (see module docstring): YES = pair_a + yes_flip + t8_flip + single_yes = 275 = NO = pair_a + yes_flip + t8_flip + single_no
GROUPS_550 = {"pair_a": 83, "yes_flip": 66, "t8_flip": 44, "single_yes": 82, "single_no": 82}
T17 = ("NM-T1", "NM-T2", "NM-T3", "NM-T4", "NM-T5", "NM-T6", "NM-T7")
SQUAT_AGE = (("A0", 0.40), ("A1", 0.60))
SQUAT_DL = (("D0", 0.3), ("D1", 0.3), ("D2", 0.4))
BASE_AGE = (("A0", 0.30), ("A1", 0.40), ("A2", 0.30))


def _pick(rng, weights):
    x, acc = rng.random(), 0.0
    for k, w in weights:
        acc += w
        if x <= acc:
            return k
    return weights[-1][0]


def _decor_for_level(rng, edit, target):
    """Choose (sib, xreg) so that ladder_level(edit, sib, xreg) == target when possible (fewest decorations first)."""
    opts = [None, "low", "high"]
    cands = []
    for sib in opts:
        for xr in opts:
            flags = [edit, sib, xr]
            lv = plan_mod.ladder_level(sum(1 for f in flags if f == "low"), sum(1 for f in flags if f == "high"))
            cands.append((lv, sib, xr, sum(1 for f in (sib, xr) if f)))
    ok = [c for c in cands if c[0] == target]
    if not ok:
        order = {lv: i for i, lv in enumerate(plan_mod.LEVELS)}
        best = min(abs(order[c[0]] - order[target]) for c in cands)
        ok = [c for c in cands if abs(order[c[0]] - order[target]) == best]
    m = min(c[3] for c in ok)
    ok = [c for c in ok if c[3] == m]
    c = rng.choice(ok)
    return c[1], c[2]


def _edit_of(op):
    return NB.EDIT_MECH.get(op)


def build_cells(rows, seed):
    """-> list of plan items {"gid","seed","size","cell"} for ~`rows` NEAR rows (before oversampling)."""
    rng = util.rng_for("T63-near-plan", seed)
    scale = rows / 550.0
    counts = {k: max(1, int(round(v * scale))) for k, v in GROUPS_550.items()}
    # land on exactly `rows` (e.g. the 275-row pilot share): only the singles (1 row each) absorb the rounding, alternately YES / NO
    diff, k_ = rows - (2 * (counts["pair_a"] + counts["yes_flip"] + counts["t8_flip"]) + counts["single_yes"] + counts["single_no"]), 0
    while diff != 0 and rows >= 20:
        key = ("single_yes", "single_no")[k_ % 2]
        step = 1 if diff > 0 else -1
        if counts[key] + step >= 1:
            counts[key] += step
            diff -= step
        k_ += 1
    items = []
    # ops for YES T1..T7: balanced cycle over the (pair_a + yes_flip + single_yes) YES slots
    n_ops = counts["pair_a"] + counts["yes_flip"] + counts["single_yes"]
    ops = [T17[i % 7] for i in range(n_ops)]
    rng.shuffle(ops)
    levels = plan_mod.level_cycle(sum(counts.values()), rng, C.NON_LIC_LEVEL_WEIGHTS)       # Opus ruling Q7b: LIC is all L3, the family composition holds with it
    li = 0

    def next_level():
        nonlocal li
        lv = levels[li % len(levels)]
        li += 1
        return lv

    def eco():
        return C.ECOSYSTEMS[rng.randrange(len(C.ECOSYSTEMS))]

    k = 0
    # pair A
    for _ in range(counts["pair_a"]):
        op = ops.pop()
        a_leg = "A2" if rng.random() < 0.95 else "A3"
        a_sq = _pick(rng, SQUAT_AGE) if a_leg == "A2" else "A1"
        sib, xr = _decor_for_level(rng, _edit_of(op), next_level())
        items.append(("pair_a", {"op": op, "a_p": a_leg, "a_sq": a_sq, "d_p": _pick(rng, SQUAT_DL), "eco": eco(),
                                 "mech": {"sib": sib, "xreg": xr}}, 2))
    # yes_flip: 1/3 each pub / fork / age
    flips = (["pub"] * (counts["yes_flip"] // 3) + ["fork"] * (counts["yes_flip"] // 3))
    flips += ["age"] * (counts["yes_flip"] - len(flips))
    rng.shuffle(flips)
    for fl in flips:
        op = ops.pop()
        if fl == "age":
            a_p, d_p = "A2", "D2"
        else:
            a_p, d_p = _pick(rng, BASE_AGE), _pick(rng, (("D0", 0.25), ("D1", 0.3), ("D2", 0.45)))
        sib, xr = _decor_for_level(rng, _edit_of(op), next_level())
        if fl == "fork":
            sib = "high" if sib is None else sib
        items.append(("yes_flip", {"op": op, "a_p": a_p, "d_p": d_p, "flip": fl, "eco": eco(), "mech": {"sib": sib, "xreg": xr}}, 2))
    # t8 flips
    t8flips = (["t8_own_org", "t8_not_reserved", "t8_internal_first", "t8_internal_query"] * (counts["t8_flip"] // 4 + 1))[:counts["t8_flip"]]
    rng.shuffle(t8flips)
    for fl in t8flips:
        lv = next_level()
        xr = "high" if lv in ("L3", "L4") and fl != "t8_internal_first" else ("low" if lv == "L2" else None)
        sib = "high" if lv == "L4" else None
        items.append(("t8_flip", {"op": "NM-T8", "a_p": _pick(rng, BASE_AGE), "d_p": _pick(rng, SQUAT_DL), "flip": fl, "eco": eco(),
                                  "explicit": rng.random() < 0.4, "mech": {"sib": sib, "xreg": xr}}, 2))
    # singles
    for _ in range(counts["single_yes"]):
        op = ops.pop()
        sib, xr = _decor_for_level(rng, _edit_of(op), next_level())
        items.append(("single_yes", {"op": op, "a_p": "A2", "d_p": "D2", "eco": eco(), "mech": {"sib": sib, "xreg": xr}}, 1))
    n2 = counts["single_no"]
    n4 = int(round(n2 * 0.2))
    for i in range(n2):
        kind = "NM-R4" if i < n4 else "NM-R2"
        op = T17[rng.randrange(7)] if kind == "NM-R2" else None
        sib, xr = _decor_for_level(rng, _edit_of(op) if op else None, next_level())
        cell = {"no_kind": kind, "op": op, "a_p": _pick(rng, SQUAT_AGE), "d_p": _pick(rng, SQUAT_DL), "eco": eco(),
                "mech": {"sib": sib if kind == "NM-R4" else None, "xreg": xr}}
        if kind == "NM-R2":
            cell["sib"] = "high" if rng.random() < 0.4 else "low"
            cell["a_p"] = _pick(rng, SQUAT_AGE)
        items.append(("single_no", cell, 1))
    rng.shuffle(items)
    out = []
    for typ, cell, size in items:
        k += 1
        cell = dict(cell, type=typ)
        out.append({"gid": "T63-NEAR-%04d" % k, "seed": "near-%d" % k, "size": size, "head": "NEAR", "cell": cell})
    return out
