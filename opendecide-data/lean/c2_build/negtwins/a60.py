"""negtwins/a60.py: Ruling A60 (17 Oct 2026, Opus), the pooled complement-twin selection. Pure: no file, no model, no heavy import.

Spec 3.18 binds on the complement twins that ENTER C2, pooled over GB + MD + RTW: implicit >= 25%, antonym >= 30%, syntactic <= 45%.
The frozen catalogue (A48-F7) has only 27 antonym complement twins, so C2 keeps all of them and sizes the pool from them:
    N_c = floor(antonym / 0.30)                       (27 -> 90)
    the non-antonym slots (N_c - antonym) are split by the pooled implicit : syntactic proportion (656 : 584 -> 33 + 30)
    within a kind the hash-earliest twins stay (key sha256("negtw-trim-v1" + base row id + pattern id), plan.trim_pooled's key)
Every other complement twin leaves C2 (the caller moves it byte-unchanged to a hold file); nothing is relabelled or refilled.
If the bars cannot hold with every antonym twin kept (too few implicit twins), antonym twins leave hash-latest first and N_c is
recomputed; if no compliant pool exists, no complement twin enters. All comparisons are exact (integers / fractions), never rounded.

Used by negtwins.pooled_audit (--select-a60, at block build) and mix_c2 (the final-mix assertion, after every trim).
"""
from __future__ import annotations

import hashlib
from fractions import Fraction

SEED = "negtw-trim-v1"                     # plan.trim_pooled's default seed
KINDS = ("syntactic", "implicit", "antonym")
MIN_IMPLICIT, MIN_ANTONYM, MAX_SYNTACTIC = Fraction(1, 4), Fraction(3, 10), Fraction(9, 20)    # spec 3.18, as plan.MIN_* / MAX_*


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def trim_key(base_id: str, pattern_id: str) -> str:
    """The hash order inside a kind: the earliest keys stay."""
    return sha(SEED + base_id + pattern_id)


def counts_of(items: dict) -> dict:
    return {k: len(items.get(k, ())) for k in KINDS}


def exact_problems(counts: dict) -> list:
    """Spec 3.18 problems on kind counts (exact fractions; no rounding can hide a miss). [] = the bars hold; zero twins = no problem
    is NOT decided here (see report(vacuous_ok))."""
    syn, imp, ant = (int(counts.get(k, 0)) for k in KINDS)
    n = syn + imp + ant
    if n == 0:
        return ["no complement twin"]
    shares = {k: round(v / n, 4) for k, v in zip(KINDS, (syn, imp, ant))}
    out = []
    if Fraction(imp, n) < MIN_IMPLICIT:
        out.append(f"implicit {shares['implicit']} < {float(MIN_IMPLICIT)}")
    if Fraction(ant, n) < MIN_ANTONYM:
        out.append(f"antonym {shares['antonym']} < {float(MIN_ANTONYM)}")
    if Fraction(syn, n) > MAX_SYNTACTIC:
        out.append(f"syntactic {shares['syntactic']} > {float(MAX_SYNTACTIC)}")
    return out


def report(counts: dict, vacuous_ok: bool = False) -> dict:
    """{"complement_twins", "shares", "by_kind", "problems"[, "vacuous"]}. vacuous_ok: with no complement twin the bars bind on
    nothing (A60: 'if nothing compliant remains, no complement twin enters'), so there is no problem."""
    by = {k: int(counts.get(k, 0)) for k in KINDS}
    n = sum(by.values())
    rep = {"complement_twins": n, "shares": {k: round(by[k] / max(1, n), 4) for k in KINDS}, "by_kind": by}
    if n == 0 and vacuous_ok:
        return rep | {"problems": [], "vacuous": True}
    return rep | {"problems": exact_problems(by)}


def ratio_of(counts: dict) -> tuple:
    """The pooled implicit : syntactic proportion (as counts) the non-antonym slots are split by."""
    return int(counts.get("implicit", 0)), int(counts.get("syntactic", 0))


def n_c(antonym: int) -> int:
    """floor(antonym / 0.30), in integers."""
    return (10 * int(antonym)) // 3


def split_slots(slots: int, ratio: tuple) -> tuple:
    """(implicit, syntactic) slots by largest remainder of slots x ratio; a tie goes to implicit (the floored share)."""
    pi, ps = ratio
    if slots <= 0 or pi + ps <= 0:
        return 0, 0
    tot = pi + ps
    ni, ns = slots * pi // tot, slots * ps // tot
    if slots - ni - ns:
        if (slots * pi) % tot >= (slots * ps) % tot:
            ni += 1
        else:
            ns += 1
    return ni, ns


def choose(ranked: dict, ratio: tuple) -> tuple:
    """ranked = {kind: [items, hash-earliest first]} -> ({kind: kept items}, info). Keeps all antonym items, N_c = floor(a / 0.30),
    non-antonym slots by `ratio`, hash-earliest per kind; short supply keeps what there is. Shares are then forced inside the bars
    by dropping syntactic items (hash-latest first), then antonym items (N_c recomputed); no compliant pool -> nothing is kept."""
    ant, imp, syn = (list(ranked.get(k, ())) for k in ("antonym", "implicit", "syntactic"))
    info = {"available": {"antonym": len(ant), "implicit": len(imp), "syntactic": len(syn)}, "ratio_implicit_syntactic": list(ratio)}
    for a in range(len(ant), 0, -1):
        nc = n_c(a)
        ni0, ns0 = split_slots(nc - a, ratio)
        ni, ns = min(ni0, len(imp)), min(ns0, len(syn))
        while ns > 0:                                        # syntactic too high or implicit too low: fewer syntactic twins fix both
            t = a + ni + ns
            if 20 * ns > 9 * t or 4 * ni < t:
                ns -= 1
            else:
                break
        if exact_problems({"antonym": a, "implicit": ni, "syntactic": ns}):
            continue                                         # e.g. too few implicit twins for this many antonym twins: fewer antonym
        info |= {"N_c": nc, "slots": {"non_antonym": nc - a, "implicit": ni0, "syntactic": ns0},
                 "antonym_dropped_to_fit_bars": len(ant) - a, "compliant": True}
        kept = {"antonym": ant[:a], "implicit": imp[:ni], "syntactic": syn[:ns]}
        info["kept"] = counts_of(kept)
        return kept, info
    info |= {"N_c": 0, "compliant": False, "kept": {k: 0 for k in KINDS},
             "note": "no compliant pool: no complement twin enters (A60)"}
    return {"antonym": [], "implicit": [], "syntactic": []}, info
