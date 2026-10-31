"""Twins (G0 spec 9): label-flip twins (9.1) and open-world twins (9.3). Negation units reuse the anchor structure with a
negated question (9.2) and are built by the pipeline.

A flip twin edits only the row's state or question, never the card text: one stated number crosses an edge, cut point
or threshold; a case fact flips; or the YN comparator switches between inclusive and strict at an exact boundary.
"""
from __future__ import annotations

import copy
import math
from fractions import Fraction as Fr

import draws as D
from numfmt import has_text
from solver_a import CV, Undetermined, solve, unknown_slots, assign, _domains

SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}


def _edits(S: dict, rng):
    """Candidate single edits (callables mutating a copy)."""
    out = []
    for i, e in enumerate(S["ents"]):
        p = e.get("pts")
        if p:
            for f, v in p["b"].items():
                if v is not None:
                    out.append(("bool", i, f))
            for a, v in p["a"].items():
                if v is not None:
                    out.append(("amt", i, a))
        b = e.get("bay")
        if b:
            if b["form"] == "counts":
                for j in range(len(b["hyps"])):
                    out.append(("cnt", i, j))
            elif b["form"] == "nE":
                for j in range(len(b["hyps"])):
                    out.append(("ne", i, j))
            elif b["form"] == "joint":
                for j in range(len(b["hyps"])):
                    out.append(("joint", i, j))
            else:
                for j in range(len(b["hyps"])):
                    out.append(("lik", i, j))
        for k, o in enumerate(e.get("outs") or []):
            if o["p"] is not None:
                out.append(("outp", i, k))
            if o["a"] is not None:
                out.append(("outa", i, k))
        if e.get("cost") is not None:
            out.append(("cost", i, None))
        if e.get("ch") is not None and e["ch"]["p"] is not None:
            out.append(("ch", i, None))
        if e.get("en") is not None:
            out.append(("en", i, None))
        if e.get("mat") is not None:
            out.append(("matp", i, None))
            out.append(("mata", i, None))
    rng.shuffle(out)
    return out


def _apply(T: dict, ed, rng, card) -> bool:
    kind, i, key = ed
    e = T["ents"][i]
    if kind == "bool":
        e["pts"]["b"][key] = not e["pts"]["b"][key]
        e["pts"]["stated"][key] = True
        return True
    if kind == "amt":
        e["pts"]["a"][key] = D.draw_money(rng, 100, 20000, 50)
        return True
    if kind == "cnt":
        b = e["bay"]
        s = b["signs"][0]
        col = 0 if b["sig"][s] else 1
        row = b["cnt"][s][key]
        row[col] = max(1, row[col] + rng.choice([-1, 1]) * rng.randint(1, max(1, row[col])))
        return True
    if kind == "ne":
        b = e["bay"]
        s = b["signs"][0]
        b["ne"][s][key] = max(1, b["ne"][s][key] + rng.choice([-1, 1]) * rng.randint(1, max(1, b["ne"][s][key])))
        return True
    if kind == "joint":
        b = e["bay"]
        s = b["signs"][0]
        J = b["joint"][s]
        nv = J[key] + Fr(rng.choice([-1, 1]) * rng.randint(1, 15), 100)
        if not (0 < nv < 1) or sum(J) - J[key] + nv > 1:
            return False
        J[key] = nv
        return True
    if kind == "lik":
        b = e["bay"]
        s = b["signs"][0]
        rep = b["rep"]["lik"]
        den = b["rep"]["lik_den"][key] if isinstance(b["rep"]["lik_den"], list) else b["rep"]["lik_den"]
        try:
            v, d = D.draw_chance(rng, rep, Fr(2, 100), Fr(95, 100), denom=den, card=card)
        except ValueError:
            return False
        b["lik"][s][key] = v
        if isinstance(b["rep"]["lik_den"], list):
            b["rep"]["lik_den"][key] = d
        return True
    if kind == "outp":
        o = e["outs"][key]
        others = sum(x["p"] for j, x in enumerate(e["outs"]) if j != key)
        try:
            v, d = D.draw_chance(rng, o["prep"], Fr(1, 100), min(Fr(95, 100), 1 - others), denom=o["pden"],
                                 card=card)
        except ValueError:
            return False
        o["p"], o["pden"] = v, d
        return True
    if kind == "outa":
        o = e["outs"][key]
        sign = -1 if o["a"] < 0 else 1
        o["a"] = sign * D.draw_money(rng, 200, 30000, 50)
        return True
    if kind == "cost":
        e["cost"] = D.draw_money(rng, 50, 8000, 50)
        e["cost_word"] = None
        return True
    if kind == "ch":
        c = e["ch"]
        try:
            v, d = D.draw_chance(rng, c["rep"], Fr(1, 100), Fr(95, 100), denom=c["den"], card=card)
        except ValueError:
            return False
        c["p"], c["den"] = v, d
        return True
    if kind == "en":
        n = e["en"]
        n["n"] = max(2, n["n"] + rng.choice([-1, 1]) * rng.randint(1, max(1, n["n"] // 2)))
        return True
    if kind == "matp":
        m = T["ents"][i]["mat"]
        try:
            v, d = D.draw_chance(rng, m["rep"], Fr(1, 100), Fr(99, 100), denom=m.get("den"), card=card)
        except ValueError:
            return False
        m["lik"], m["p"], m["den"] = v, v, d
        return True
    if kind == "mata":
        m = T["ents"][i]["mat"]
        m["amt"] = D.draw_money(rng, 100, 40000, 10)
        return True
    return False


def flip_twin(S: dict, card: dict, rng, accept, tries: int = 120):
    """A twin of S with a different gold; accept(T) runs the row checks (CI lint, placement, lints)."""
    base = solve(S, CV())
    if not base["det"]:
        return None
    # exact boundary: switch the comparator between inclusive and strict (question edit)
    if S["form"] == "yn_thr" and S.get("_place") == "exact" and rng.randrange(100) < 50:
        import lexicon as L
        T = copy.deepcopy(S)
        T["thr"]["op"] = SWAP[T["thr"]["op"]]
        ws = [w["w"] for w in L.COMPARATORS[T["thr"]["op"]] if w["neg_ok"] or T["thr"]["neg"] == 0]
        T["cmp_word"] = rng.choice(ws)
        T["_flip"] = "comparator"
        r = solve(T, CV())
        if r["det"] and r["ans"] != base["ans"] and accept(T):
            return T
    for _ in range(tries):
        for ed in _edits(S, rng)[:6]:
            T = copy.deepcopy(S)
            if not _apply(T, ed, rng, card):
                continue
            try:
                r = solve(T, CV())
            except (Undetermined, ValueError, ZeroDivisionError):
                continue
            if not r["det"] or r["ans"] == base["ans"]:
                continue
            T["_flip"] = ed[0]
            if accept(T):
                return T
    return None


def world_twin(S: dict, card: dict, rng, accept, target=None, tries: int = 60):
    """Closed-world twin of an open anchor: every unknown replaced by a stated value inside its range (9.3)."""
    base = solve(S, CV())
    slots = unknown_slots(S)
    if not slots:
        return None
    for _ in range(tries):
        vals = []
        for path, dom in slots:
            if path[0] == "pts" and path[2] == "b":
                vals.append(rng.choice([True, False]))
            else:
                lo, hi = dom
                vals.append(_grid_value(rng, lo, hi, path))
        T = assign(S, slots, tuple(vals))
        T["world"] = "closed"
        _fix_reps(T, S)
        for e in T["ents"]:
            if e.get("pts"):
                e["pts"]["stated"] = {f: True for f in e["pts"]["b"]}
        try:
            r = solve(T, CV())
        except (Undetermined, ValueError, ZeroDivisionError):
            continue
        if not r["det"]:
            continue
        if base["det"] and r["ans"] != base["ans"]:
            continue
        if target is not None and r["ans"] != target:
            continue
        if accept(T):
            return T
    return None


def _grid_value(rng, lo: Fr, hi: Fr, path) -> Fr:
    kind = path[0]
    if kind in ("lik", "outp", "ch"):
        a, b = math.ceil(lo * 100), math.floor(hi * 100)
        if a > b:
            return lo
        return Fr(rng.randint(a, b), 100)
    a, b = math.ceil(lo / 10), math.floor(hi / 10)
    if a > b:
        return lo
    return Fr(rng.randint(a, b) * 10)


def _fix_reps(T: dict, S: dict) -> None:
    """Filled chances are whole percents: give them the pct0 representation."""
    for e in T["ents"]:
        b = e.get("bay")
        if b and b["form"] == "rates":
            dl = b["rep"]["lik_den"]
            for s, vec in b["lik"].items():
                for j, v in enumerate(vec):
                    if not has_text(v, b["rep"]["lik"], dl[j] if isinstance(dl, list) else dl):
                        b["rep"].setdefault("lik_list", [(b["rep"]["lik"], dl[jj] if isinstance(dl, list) else dl)
                                                         for jj in range(len(vec))])
                        b["rep"]["lik_list"][j] = ("pct0", None)
            b["rng"] = {}
            b.pop("rngshow", None)
        for o in e.get("outs") or []:
            if o.get("prng") is not None:
                o["prep"], o["pden"], o["prng"] = "pct0", None, None
                o.pop("prng_show", None)
            if o.get("arng") is not None:
                o["arng"] = None
                o.pop("arng_show", None)
        if e.get("ch") is not None and e["ch"].get("rng") is not None:
            e["ch"]["rep"], e["ch"]["den"], e["ch"]["rng"] = "pct0", None, None
        if e.get("pts"):
            e["pts"]["arng"] = {}
