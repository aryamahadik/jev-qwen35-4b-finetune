"""r1.1 repair: per-card yes rates y for Q3 cards (G0 1 / 8, v4 2.1: y uniform in 20-80% per card).

r1.0 drew y independently per card, so card-level strata with few Q3 cards (missing-field world, LATER+SPEC, the
cards with an only-if fallback, M) ended far from 50% (G10 marginals, G6 metadata). Here the y values are still
uniform draws in [0.2, 0.8], taken as antithetic pairs (u, 1 - u), and the values are then permuted over the Q3
cards (a seeded hill climb over swaps) so that the row-weighted mean y is close to 0.5 inside every card-level
stratum the gates read: world, precedence policy, tie rule, sampler, notices allowed, fallback present, M present,
short card, label form. Each card's y is still marginally uniform; only the pairing of values to cards is chosen.
"""
from __future__ import annotations

import random

SEED = 20261005


def strata(c):
    cs = c.get("constructs") or ()
    pol = c["prim"] + ("+" + c["sec"] if c.get("sec") else "")
    return {"world": c["world"], "policy": pol, "tie": str(c.get("tie")), "sampler": c["sampler"],
            "notices": "notices" in cs, "fallback": c.get("fallback") is not None, "M": c.get("M") is not None,
            "short": bool(c.get("short")), "label_form": c.get("label_form"),
            # r2: few-shot cards are a stratum of the plan (replaces the r1.1 pass-6 swaps SWAPS_P6)
            "fewshot": bool(c.get("fewshot"))}


def _row_weights():
    """Per-card Q3 row counts by X role and notice count from the r1.1 provisional build (yplan_weights_r11.json):
    the row-level marginals (yes rate per X role and per amendment count) are row-weighted means of the card y."""
    import json
    import os
    # r2: expected weights on the r2 plan (yplan_weights_r2.json: r1.1 X-role shares and the r2 amendment targets,
    # times the r2 planned rows); the r1.1 file is the fallback
    d = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(d, "yplan_weights_r2.json")
    if not os.path.exists(p):
        p = os.path.join(d, "yplan_weights_r11.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def loss(ys, cards, W, RW=None):
    tot = 0.0
    if RW:
        keys_rw = sorted({k for c in cards for k in RW.get(c["card_id"], {})})
        for k in keys_rw:
            s = n = 0.0
            for y, c in zip(ys, cards):
                x = RW.get(c["card_id"], {}).get(k, 0)
                s += x * y
                n += x
            if n:
                tot += n * (s / n - 0.5) ** 2
    keys = strata(cards[0]).keys()
    for k in keys:
        acc = {}
        for y, c, w in zip(ys, cards, W):
            v = strata(c)[k]
            a = acc.setdefault(v, [0.0, 0.0])
            a[0] += w * y
            a[1] += w
        for s, n in acc.values():
            tot += n * (s / n - 0.5) ** 2
    return tot


def plan(cards, iters=8000):
    q3 = sorted([c for c in cards if c["qtype"] == "Q3"], key=lambda c: c["card_id"])
    rng = random.Random(SEED)
    vals = []
    for _ in range(len(q3) // 2):
        u = rng.random()
        vals += [0.2 + 0.6 * u, 0.8 - 0.6 * u]
    if len(q3) % 2:
        vals.append(0.2 + 0.6 * rng.random())
    rng.shuffle(vals)
    W = [float(c.get("n_rows") or 1) for c in q3]
    RW = _row_weights()
    best = loss(vals, q3, W, RW)
    for it in range(iters):
        i, j = rng.randrange(len(vals)), rng.randrange(len(vals))
        if i == j:
            continue
        vals[i], vals[j] = vals[j], vals[i]
        l2 = loss(vals, q3, W, RW)
        if l2 <= best:
            best = l2
        else:
            vals[i], vals[j] = vals[j], vals[i]
    return {c["card_id"]: round(y, 4) for c, y in zip(q3, vals)}, best


# r1.1 pass 6: the 8 few-shot Q3 cards (worked cases in the card: a distinctive card text) had a row-weighted mean y of
# 0.59 against 0.48 on the other Q3 cards, so the card text alone predicted the yes/no label above chance under
# card-grouped CV (G6 view c 0.536 vs chance 0.503; without those 8 cards 0.512). Few-shot presence was not a yplan
# stratum. These four swaps of y values (few-shot card <-> other card; greedy best swaps on the yplan loss plus a
# few-shot stratum, starting from the plan above) bring the few-shot mean to 0.508 vs 0.495; only these 7 cards change.
SWAPS_P6 = (("F1-C030", "F1-C055"), ("F1-C075", "F1-C082"), ("F1-C077", "F1-C120"), ("F1-C082", "F1-C102"))


USE_SWAPS_P6 = False   # r2: the few-shot stratum is in the plan's loss instead


def apply(cards):
    p, _ = plan(cards)
    if USE_SWAPS_P6:
        for a, b in SWAPS_P6:
            if a in p and b in p:
                p[a], p[b] = p[b], p[a]
    for c in cards:
        if c["card_id"] in p:
            c["yes_rate"] = p[c["card_id"]]
    return p
