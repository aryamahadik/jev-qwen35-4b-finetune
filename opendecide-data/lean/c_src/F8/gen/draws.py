"""Exact number draws on representation grids, threshold placement (G0 spec 8: grid, placements, draw order).

Every value is an int or Fraction. A chance is drawn on its representation's grid so it always has an exact text:
pct0 k/100; pct1 k/1000 (one non-zero decimal); dec k/100 (or k/10); frac a/b, b from the card's set; ain / aoutof
a/b, b from lexicon.AIN_DENOMS.
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr

import lexicon as L
from common import log_uniform_int
from numfmt import has_text

STEP = {"chance": Fr(1, 1000), "score": Fr(1), "money": Fr(1), "num": Fr(1, 10)}


def chance_grid_step(rep: str, denom: int | None) -> Fr:
    return {"pct0": Fr(1, 100), "pct1": Fr(1, 1000), "dec": Fr(1, 100)}.get(rep, Fr(1, denom or 100))


def draw_chance(rng, rep: str, lo: Fr = Fr(1, 100), hi: Fr = Fr(99, 100), *, denom: int | None = None,
                card=None) -> tuple:
    """(value, denom) on rep's grid within [lo, hi]."""
    for _ in range(200):
        if rep == "pct0":
            k = rng.randint(math.ceil(lo * 100), math.floor(hi * 100))
            v, d = Fr(k, 100), None
        elif rep == "pct1":
            k = rng.randint(math.ceil(lo * 1000), math.floor(hi * 1000))
            if k % 10 == 0:
                continue
            v, d = Fr(k, 1000), None
        elif rep == "dec":
            if rng.random() < 0.3:
                k = rng.randint(max(1, math.ceil(lo * 10)), min(9, math.floor(hi * 10)))
                v = Fr(k, 10)
            else:
                k = rng.randint(math.ceil(lo * 100), math.floor(hi * 100))
                v = Fr(k, 100)
            d = None
        elif rep in ("frac",):
            b = denom or rng.choice((card or {}).get("frac_denoms") or list(L.FRAC_DENOMS))
            a_lo, a_hi = math.ceil(lo * b), math.floor(hi * b)
            if a_lo > a_hi:
                continue
            v, d = Fr(rng.randint(a_lo, a_hi), b), b
        elif rep in ("ain", "aoutof"):
            b = denom or rng.choice(L.AIN_DENOMS)
            a_lo, a_hi = math.ceil(lo * b), math.floor(hi * b)
            if a_lo > a_hi:
                continue
            v, d = Fr(rng.randint(a_lo, a_hi), b), b
        else:
            raise ValueError(rep)
        if lo <= v <= hi and has_text(v, rep, d):
            return v, d
    raise ValueError(f"no {rep} value in [{lo}, {hi}]")


def draw_base_rates(rng, k: int, rep: str, card=None, min_share: Fr = Fr(3, 100)) -> tuple:
    """k base rates summing to exactly 1, all on one grid (rep, denom)."""
    for _ in range(500):
        if rep in ("frac", "ain", "aoutof"):
            pool_b = [b for b in ((card or {}).get("frac_denoms") or L.FRAC_DENOMS)] if rep == "frac" \
                else list(L.AIN_DENOMS)
            pool_b = [b for b in pool_b if b >= 2 * k]
            if not pool_b:
                pool_b = [20, 40, 50] if rep == "frac" else [20, 40, 50, 100]
            b = rng.choice(pool_b)
            unit = Fr(1, b)
        elif rep == "pct1":
            b, unit = None, Fr(1, 1000)
        else:
            b, unit = None, Fr(1, 100)
        n_units = int(1 / unit)
        mins = max(1, int(min_share / unit))
        if n_units < k * mins:
            continue
        cuts = sorted(rng.sample(range(mins, n_units - mins + 1), k - 1)) if k > 1 else []
        parts = [c2 - c1 for c1, c2 in zip([0] + cuts, cuts + [n_units])]
        if min(parts) < mins:
            continue
        vals = [p * unit for p in parts]
        if all(has_text(v, rep, b) for v in vals):
            return vals, b
    raise ValueError("base rates")


def draw_money(rng, lo: int, hi: int, mult: int | None = None) -> Fr:
    m = mult or rng.choice([10, 50, 100])
    a, b = max(1, -(-lo // m)), hi // m
    if a > b:
        return Fr(lo)
    return Fr(rng.randint(a, b) * m)


# ------------------------------------------------------------------------------------------------ thresholds
def t_grid(qt: str, trep: dict):
    """(is_on_grid(x), step, neighbours(x, side) -> grid point strictly on side nearest x)."""
    if qt == "chance":
        r = trep["rep"]
        if r == "pct0":
            g = Fr(1, 100)
        elif r == "pct1":
            g = Fr(1, 1000)
        else:
            g = Fr(1, trep["denom"])

        def on(x):
            ok = (x / g).denominator == 1
            if r == "pct1":
                ok = ok and (x * 100).denominator != 1
            return ok
        return on, g
    if qt == "money":
        g = Fr(10 ** trep.get("zeros", 0))
        return (lambda x: (x / g).denominator == 1), g
    if qt == "score":
        return (lambda x: x.denominator == 1), Fr(1)
    if qt == "num":
        g = Fr(1) if trep.get("dec", 0) == 0 else Fr(1, 10)
        return (lambda x: (x / g).denominator == 1), g
    raise ValueError(qt)


def _grid_floor(x: Fr, g: Fr) -> Fr:
    return Fr(math.floor(x / g)) * g


def place_threshold(v: Fr, qt: str, trep: dict, cls: str, side: str, rng, *, valid, forbidden=(), cap=None,
                    pct1_skip=True):
    """Place T relative to the value v (forward samplers, draw-order step 4). side 'above': T > v; 'below': T < v.
    Returns (T, d_steps) or None when this value cannot realise the drawn class (caller redraws the numbers)."""
    on, g = t_grid(qt, trep)
    step = STEP[qt]
    lo_ok, hi_ok = valid

    def ok(T):
        if not on(T):
            return False
        if lo_ok is not None and not T > lo_ok:
            return False
        if hi_ok is not None and not T < hi_ok:
            return False
        if T in forbidden:
            return False
        return True
    if cls == "exact":
        return (v, 0) if ok(v) else None
    if cls == "near":
        if side == "above":
            T = _grid_floor(v, g) + g
        else:
            T = _grid_floor(v, g)
            if T == v:
                T = v - g
        while not on(T):            # pct1 grid skips whole percents
            T = T + (g if side == "above" else -g)
        d = (v - T) / step
        if not (0 < abs(d) <= 1):
            return None
        if not ok(T):
            return None
        return T, d
    # far: |d| in [2, L], log-uniform target distance, rounded away from v
    room = None
    if side == "above" and hi_ok is not None:
        room = (hi_ok - v) / step - 1
    elif side == "below" and lo_ok is not None:
        room = (v - lo_ok) / step - 1
    Lc = cap if cap is not None else 500
    Lmax = min(room, Lc) if room is not None else Lc
    if Lmax < 2:
        return None
    D = Fr(log_uniform_int(rng, 2, int(Lmax)))
    t = v + D * step if side == "above" else v - D * step
    if side == "above":
        T = _grid_floor(t, g)
        if T < t:
            T += g
    else:
        T = _grid_floor(t, g)
    for _ in range(20):
        if on(T):
            break
        T = T + (g if side == "above" else -g)
    d = (v - T) / step
    if abs(d) < 2:
        return None
    if not ok(T):
        return None
    return T, d


def draw_trep(rng, qt: str, card: dict) -> dict:
    """Representation and digit pattern of <T>, drawn before the value is placed (draw-order step 2)."""
    if qt == "chance":
        r = rng.choice(card.get("t_reps") or ["pct0", "pct1", "frac"])
        d = rng.choice(card.get("frac_denoms") or [20]) if r == "frac" else None
        return {"rep": r, "denom": d}
    if qt == "money":
        return {"zeros": rng.choice([0, 1, 1, 2])}
    if qt == "num":
        return {"dec": rng.choice([0, 1])}
    return {}
