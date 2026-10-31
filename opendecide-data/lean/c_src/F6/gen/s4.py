"""S4: bounds, dates and rounded figures (G0 s7). Events with exact, ranged (one unknown day) or month-only dates,
every event date domain on or before D; full-date deadlines with inclusive phrases only; exact, ranged, rounded or
unitless figures; totals of named figures. Questions (yes/no only): deadline met, came first, at least N days after,
total vs a threshold. Labels from solver A's interval reasoning; solver B enumerates the parse.
"""
from __future__ import annotations

import copy
import random

from . import common  # noqa: F401
from fmt1 import pool as fpool

from .common import rng_for, unit, day, ymd, month_bounds, days_in_month, MONTHS
from . import solver_a as A, rowmake as M, render_f6 as RF, styles_f6 as ST
from .lex import sw, FRAMES, FRAME_SWITCH

UNIT_PAIRS = {"minutes": ("hours", 60), "seconds": ("minutes", 60), "days": ("weeks", 7), "hours": ("days", 24),
              "months": ("years", 12), "grams": ("kilograms", 1000), "metres": ("kilometres", 1000),
              "millimetres": ("centimetres", 10), "centimetres": ("metres", 100), "kg": ("tonnes", 1000)}
DL_WORDS = ["by", "on or before", "no later than"]
CMP = {">=": ["at least", "no less than"], "<=": ["at most", "no more than"], ">": ["more than"],
       "<": ["less than"]}


class Skip(Exception):
    pass


# ---------------------------------------------------------------- cards

def make_card(card_id: str, schema: str, pack: dict) -> dict:
    rng = rng_for("card", card_id)
    case = rng.choice(pack["cases"])
    pol = pack.get("ev_pol") or {}
    good = [e for e in pack["events"] if pol.get(e) == "good"]
    bad = [e for e in pack["events"] if pol.get(e) == "bad"]
    if good and bad:                      # repair r1: one good and one bad event type, so order claims have a valence
        evs = [rng.choice(good), rng.choice(bad)]
        rest = [e for e in pack["events"] if e not in evs and pol.get(e)]
        if rest and rng.random() < 0.5:
            evs.append(rng.choice(rest))
        rng.shuffle(evs)
    else:
        evs = rng.sample(pack["events"], min(len(pack["events"]), 3))
    polar_q = [q for q in pack["qty"] if q.get("adverse")]
    other_q = [q for q in pack["qty"] if not q.get("adverse")]
    qsrc = (rng.sample(polar_q, min(len(polar_q), 2)) + rng.sample(other_q, max(0, min(len(other_q), 2 - len(polar_q)))))
    qs = []
    for q in qsrc:
        lo, hi = max(q["lo"], 2), q["hi"]
        if hi - lo > 300:
            lo = rng.randint(lo, hi - 150)
            hi = lo + rng.randint(80, 150)
        pair = UNIT_PAIRS.get(q["unit"])
        qd = {"name": q["name"], "unit": q["unit"], "lo": lo, "hi": hi,
              "R": rng.choice([10, 20]) if hi - lo >= 60 else rng.choice([2, 4]),
              "mark": "*", "adverse": q.get("adverse")}
        if pair:
            qd["V"], qd["conv"] = pair
        qs.append(qd)
    avail = ["deadline"]
    if sum(1 for e in evs if pol.get(e) == "good") and sum(1 for e in evs if pol.get(e) == "bad"):
        avail += ["before", "daycount"]
    if any(q.get("adverse") for q in qs):
        avail.append("total")
    rng.shuffle(avail)
    kinds = avail[: rng.choice([2, 3])] if len(avail) > 1 else avail
    world = rng.choice(["open", "closed", "local"])
    styles = fpool.card_style_set(ST.training_styles("S4"), 6, "F6", card_id)
    card = {"card_id": card_id, "sampler": "S4", "schema": schema, "pack": pack, "noun": case["noun"],
            "plural": case["plural"], "prefix": case["prefix"], "evs": evs, "qs": qs, "kinds": kinds,
            "world": world, "local_type": evs[0] if world == "local" else None,
            "marker": rng.choice(["not recorded", "unknown"]), "date_style": rng.choice(["iso", "name"]),
            "ambiguous": any("V" in q for q in qs) and rng.random() < 0.3, "plans": rng.random() < 0.4,
            "styles": styles, "wordings": ST.card_wordings(card_id, True), "year": rng.randint(2044, 2058),
            "defs_style": "short" if rng.random() < 0.08 else "one_line", "attack": rng.random() < 0.6,
            "frames": ["qdet", "qdet_leave", "qdet_dneg", "qest_est", "qest_det", "qplain_true"],
            "ev_pol": {e: pol.get(e) for e in evs}}
    card["triple_ok"] = any(k in kinds for k in ("deadline", "before"))
    card["attack"] = card["attack"] and any(x["container"] not in ST.NO_PARA for x in styles)
    # repair r1 (length, AG-09): one comparator family per card (row 11 or row 12 sentence) and one quantity whose
    # figures may be rounded (one row 19 sentence); card-level, never per row
    card["cmp_family"] = rng.choice(["incl", "excl"])
    card["round_q"] = 0 if qs else None
    for i, q in enumerate(qs):
        if i != card["round_q"]:
            q["R"], q["mark"] = None, None
    from . import examples_f6 as EX
    if card_id in EX.FEWSHOT_CARDS:
        card["defs_style"] = "one_line"
    n_ex, few = EX.card_flags(card_id, schema, card["defs_style"], "S4")
    exs, shots = EX.make(card, card["marker"], card["cmp_family"], n_ex, few) if n_ex else ([], [])
    card["examples"], card["fewshot"] = exs, shots
    if exs:
        card["defs_style"] = "one_line_examples"
    return card


# ---------------------------------------------------------------- structures

def _id(rng, prefix, used):
    while True:
        x = f"{prefix}-{rng.randint(1000, 9999)}"
        if x not in used:
            used.add(x)
            return x


def _date_repr(rng, S, d, kind):
    """Event date d rendered exact / ranged / month-only, with every domain on or before D (row 18)."""
    D = S["D"]
    if kind == "exact":
        return {"k": "exact", "d": d}
    if kind == "range":
        a = d - rng.randint(0, 12)
        b = min(D, d + rng.randint(1, 12))
        return {"k": "range", "a": a, "b": b}
    dd = ymd(d)
    lo, hi = month_bounds(dd.year, dd.month)
    if hi > D:
        return None
    return {"k": "month", "y": dd.year, "m": dd.month, "a": lo, "b": hi}


def _flip(v):
    return {"good": "bad", "bad": "good"}.get(v)


def s4_valence(card, S, Q):
    """'Yes = bad outcome' valence of S (s6 / XF04; repair r1): deadline met = good; a total above a limit whose
    high values are adverse = bad; a good step before a bad event = good; a good step at least N days after a bad
    event = bad (late); 'not' flips."""
    t = Q["t"]
    if t == "deadline":
        v = "good"
    elif t == "total":
        adv = S["quantities"][Q["q"]].get("adverse")
        if adv not in ("high", "low"):
            return None
        up = Q["op"] in (">", ">=")
        v = "bad" if up == (adv == "high") else "good"
    else:
        p1 = card.get("ev_pol", {}).get(Q["e1"].split("|")[0])
        p2 = card.get("ev_pol", {}).get(Q["e2"].split("|")[0])
        if not p1 or not p2 or p1 == p2:
            return None
        v = ("good" if p1 == "good" else "bad") if t == "before" else ("bad" if p1 == "bad" else "good")
    return _flip(v) if Q.get("neg") else v


def draw_structure(rng, card, target_kind: str, vtarget=None, neg=False) -> tuple[dict, dict]:
    D = day(card["year"], rng.randint(3, 12), rng.randint(1, 28))
    used = set()
    ents = [_id(rng, card["prefix"], used) for _ in range(3)]
    S = {"kind": "timeline", "D": D, "world": card["world"], "local": card["local_type"], "marker": card["marker"],
         "events": {}, "day_dom": {}, "figures": {}, "quantities": {},
         "noshare_types": sorted(card["evs"]) if "before" in card["kinds"] else [], "ents": ents}
    for i, q in enumerate(card["qs"]):
        S["quantities"][f"q{i}"] = dict(q)
    evs = card["evs"]
    pol = card.get("ev_pol") or {}
    t = target_kind
    want_v = _flip(vtarget) if (vtarget and neg) else vtarget      # the valence of the un-negated S
    if t == "deadline":
        e = rng.choice(evs)
        key = f"{e}|{ents[0]}"
        if rng.random() < 0.25:
            by = D + rng.randint(5, 60)
        else:
            by = D - rng.randint(5, 120)
        Q = {"t": "deadline", "ev": key, "by": by, "neg": neg}
        S["_true"] = {key: by + rng.randint(-25, 25)}
    elif t in ("before", "daycount"):
        good = [e for e in evs if pol.get(e) == "good"]
        bad = [e for e in evs if pol.get(e) == "bad"]
        if good and bad and want_v:
            g, b = rng.choice(good), rng.choice(bad)
            if t == "before":
                e1, e2 = (g, b) if want_v == "good" else (b, g)
            else:
                e1, e2 = (b, g) if want_v == "bad" else (g, b)
        else:
            e1, e2 = rng.sample(evs, 2) if len(evs) >= 2 else (evs[0], evs[0])
        k1, k2 = f"{e1}|{ents[0]}", f"{e2}|{ents[0] if e1 != e2 else ents[1]}"
        d1 = D - rng.randint(20, 200)
        d2 = d1 + rng.randint(-25, 40)
        if d2 > D:
            d2 = D - 1
        if d2 == d1:
            d2 += 1
        S["_true"] = {k1: d1, k2: min(d2, D)}
        if t == "before":
            Q = {"t": "before", "e1": k1, "e2": k2, "neg": neg}
        else:
            Q = {"t": "daycount", "e1": k1, "e2": k2, "N": max(1, abs(d2 - d1) + rng.randint(-6, 6))}
    else:
        polar = [i for i, q in enumerate(card["qs"]) if q.get("adverse")]
        qi = rng.choice(polar) if polar else rng.randrange(len(card["qs"]))
        q = card["qs"][qi]
        n = rng.choice([2, 3])
        figs = [f"q{qi}|{ents[j]}" for j in range(n)]
        vals = [rng.randint(q["lo"], q["hi"]) for _ in range(n)]
        S["_figtrue"] = dict(zip(figs, vals))
        tot = sum(vals)
        up = rng.random() < 0.5
        if want_v and q.get("adverse") in ("high", "low"):
            up = (want_v == "bad") == (q["adverse"] == "high")
        fam = card.get("cmp_family", "incl")
        ops = (">=" if fam == "incl" else ">") if up else ("<=" if fam == "incl" else "<")
        spread = max(3, (q["hi"] - q["lo"]) // 4)
        Q = {"t": "total", "figs": figs, "op": ops, "T": max(1, tot + rng.randint(-spread, spread)), "q": f"q{qi}"}
    # off-path facts (trap gaps when uncertain): another event line and another figure no question uses
    if rng.random() < 0.85:
        e = rng.choice(evs)
        k = f"{e}|{ents[2]}"
        if k not in S.get("_true", {}):
            S.setdefault("_true", {})[k] = D - rng.randint(10, 200)
    if card["qs"] and rng.random() < 0.7:
        qi = rng.randrange(len(card["qs"]))
        q = card["qs"][qi]
        k = f"q{qi}|{ents[2]}"
        if k not in S.get("_figtrue", {}) and (Q["t"] != "total" or k not in Q["figs"]):
            S.setdefault("_figtrue", {})[k] = rng.randint(q["lo"], q["hi"])
    return S, Q


def _realise(rng, card, S, Q, reps: dict) -> dict:
    """Render the truth into record facts with the chosen representation per key."""
    S2 = copy.deepcopy(S)
    D = S2["D"]
    for key, d in S.get("_true", {}).items():
        r = reps.get(key, "exact")
        typ = key.split("|")[0]
        closed = S2["world"] == "closed" or (S2["world"] == "local" and S2.get("local") == typ)
        if d > D:
            r = "absent" if r not in ("marker", "plan") else r
        if r in ("exact", "range", "month"):
            dr = _date_repr(rng, S2, d, r)
            if dr is None:
                raise Skip("month reaches D")
            S2["events"][key] = dr
        elif r == "marker":
            S2["events"][key] = {"k": "marker"}
            S2["day_dom"][key] = (D - rng.randint(150, 260), D - rng.randint(1, 20))
        elif r == "plan":
            if not card["plans"]:
                raise Skip("plans off")
            S2["events"][key] = {"k": "plan", "d": D - rng.randint(1, 60) if closed else D + rng.randint(1, 40)}
            if not closed:
                S2["day_dom"][key] = (D - rng.randint(150, 260), D - rng.randint(1, 20))
        elif r == "absent":
            if not closed:
                S2["day_dom"][key] = (D - rng.randint(150, 260), D - rng.randint(1, 20))
    for key, v in S.get("_figtrue", {}).items():
        q = S2["quantities"][key.split("|")[0]]
        r = reps.get(key, "exact")
        if r == "exact":
            S2["figures"][key] = {"q": key.split("|")[0], "k": "exact", "x": v, "unit": "U"}
        elif r == "range":
            a = max(q["lo"], v - rng.randint(1, 15))
            b = min(q["hi"], v + rng.randint(1, 15))
            S2["figures"][key] = {"q": key.split("|")[0], "k": "range", "a": a, "b": b, "unit": "U"}
        elif r == "round":
            R = q["R"]
            x = ((v + R // 2) // R) * R
            if not (q["lo"] <= x - R // 2 and x + R // 2 - 1 <= q["hi"]):
                raise Skip("rounding interval outside the domain")
            S2["figures"][key] = {"q": key.split("|")[0], "k": "round", "x": x, "unit": "U"}
        elif r == "unitless":
            S2["figures"][key] = {"q": key.split("|")[0], "k": "unitless", "x": v}
        elif r == "marker":
            S2["figures"][key] = {"q": key.split("|")[0], "k": "marker"}
    S2.pop("_true", None)
    S2.pop("_figtrue", None)
    return S2


def _fills(S, key):
    """Region representatives of one visible gap (for the decisive test)."""
    kind, k = key
    if kind == "ev":
        e = S["events"].get(k)
        if e and e["k"] in ("range", "month"):
            return [("day", d) for d in range(e["a"], e["b"] + 1)]
        dom = S["day_dom"].get(k)
        out = [("none", None)]
        if dom:
            out += [("day", d) for d in range(dom[0], dom[1] + 1)]
        return out
    f = S["figures"][k]
    q = S["quantities"][f["q"]]
    if f["k"] == "range":
        return [("fig", x) for x in range(f["a"], f["b"] + 1)]
    if f["k"] == "round":
        h = q["R"] // 2
        return [("fig", x) for x in range(f["x"] - h, f["x"] + h)]
    if f["k"] == "unitless":
        return [("fig", f["x"]), ("fig", f["x"] * q["conv"])]
    return [("fig", x) for x in range(q["lo"], q["hi"] + 1)]


def _apply(S, key, fill):
    S2 = copy.deepcopy(S)
    kind, k = key
    if kind == "ev":
        if fill[0] == "none":
            S2["events"].pop(k, None)
            S2["day_dom"].pop(k, None)
            S2["_forced_none"] = S2.get("_forced_none", []) + [k]
        else:
            S2["events"][k] = {"k": "exact", "d": fill[1]}
            S2["day_dom"].pop(k, None)
    else:
        q = S2["figures"][k]["q"]
        S2["figures"][k] = {"q": q, "k": "exact", "x": fill[1], "unit": "U"}
    return S2


def claim_val(S, Q):
    S2 = S
    if S.get("_forced_none"):
        S2 = copy.deepcopy(S)
        S2["world"] = "closed_some"
    return _claim(S2, Q)


def _claim(S, Q):
    if S["world"] == "closed_some":
        # events filled as 'did not happen' close for this test only
        S = {**S, "world": S.get("_orig_world", "open")}
    return A.timeline_claim(S, Q)


def decisive(S, Q):
    out = []
    for key, kind in A.timeline_unknowns(S, Q):
        ok = True
        for fill in _fills(S, key):
            S2 = _apply(S, key, fill)
            if fill[0] == "none":
                # 'did not happen up to D': the event is closed for this check
                v = A.timeline_claim({**S2, "world": "closed", "local": None}, Q) if Q.get("ev") == key[1] or \
                    Q.get("e1") == key[1] or Q.get("e2") == key[1] else A.timeline_claim(S2, Q)
            else:
                try:
                    v = A.timeline_claim(S2, Q)
                except A.Drop:
                    continue        # an infeasible value (a shared day under row 46) is not a completion
            if v is A.U:
                ok = False
                break
        if ok:
            out.append(key)
    return out


REP_OF = {"gap:bound@ev": "range", "gap:month@ev": "month", "gap:value@ev": "marker", "gap:plan@ev": "plan",
          "gap:bound@fig": "range", "gap:round@fig": "round", "gap:unit@fig": "unitless", "gap:value@fig": "marker"}


def s4_elems(S, Q) -> list:
    return sorted(f"{k}@{g[0]}" for g, k in A.timeline_unknowns(S, Q))


def build_record(rng, card, target, n_gaps, kind, sig=None, vtarget=None, neg=False):
    """An S4 record with target 'settled' / 'open' (one decisive gap) and exactly n_gaps visible gaps; with `sig`
    (repair r1) exactly that kind@position signature (representations drawn toward the needed kinds)."""
    from collections import Counter
    need = Counter(sig) if sig else None
    if need is not None:
        n_gaps = sum(need.values())
    for _ in range(160):
        S, Q = draw_structure(rng, card, kind, vtarget, neg)
        keys = list(S.get("_true", {})) + list(S.get("_figtrue", {}))
        reps = {}
        cand_ev = ["exact", "range", "month", "marker"] + (["absent"] if card["world"] != "closed" else []) + \
            (["plan"] if card["plans"] else [])
        cand_fig = ["exact", "range", "round", "marker"] + (["unitless"] if card["ambiguous"] else [])
        rq = card.get("round_q")
        qkeys = {Q.get("ev"), Q.get("e1"), Q.get("e2")} | set(Q.get("figs", []))
        if need is not None:
            # assign each needed element to one key of its position, then the rest exact
            ev_keys = [k for k in S.get("_true", {})]
            fig_keys = [k for k in S.get("_figtrue", {})]
            rng.shuffle(ev_keys)
            rng.shuffle(fig_keys)
            ok = True
            for el, c in need.items():
                for _i in range(c):
                    pool = ev_keys if el.endswith("@ev") else fig_keys
                    rep = REP_OF.get(el)
                    cands = [k for k in pool if k not in reps]
                    if Q["t"] in ("before", "daycount"):
                        cands = [k for k in cands if k not in qkeys or rep in ("range", "month")]
                    if rep == "unitless":
                        cands = [k for k in cands if "V" in S["quantities"][k.split("|")[0]] and card["ambiguous"]]
                    if rep == "round" and el.endswith("@fig"):
                        cands = [k for k in cands if k.split("|")[0] == f"q{rq}"]
                    if rep == "plan" and not card["plans"]:
                        cands = []
                    if not cands or rep is None:
                        ok = False
                        break
                    k = rng.choice(cands)
                    if rep == "marker" and el == "gap:value@ev" and card["world"] != "closed" and rng.random() < 0.5:
                        rep = "absent"
                    reps[k] = rep
            if not ok:
                continue
            for k in keys:
                reps.setdefault(k, "exact")
        else:
            for k in keys:
                pool = cand_fig if k in S.get("_figtrue", {}) else cand_ev
                if k in S.get("_figtrue", {}) and "V" not in S["quantities"][k.split("|")[0]]:
                    pool = [p for p in pool if p != "unitless"]
                if k in S.get("_figtrue", {}) and k.split("|")[0] != f"q{rq}":
                    pool = [p for p in pool if p != "round"]
                if Q["t"] in ("before", "daycount") and k in qkeys:
                    pool = ["exact", "range", "month"]
                reps[k] = rng.choice(pool) if rng.random() < 0.6 else "exact"
        if card["ambiguous"] and sum(1 for v in reps.values() if v == "unitless") > 1:
            continue
        try:
            S2 = _realise(rng, card, S, Q, reps)
            v = A.timeline_claim(S2, Q)
        except (Skip, A.Drop):
            continue
        ns = set(S2.get("noshare_types") or [])
        days = [e["d"] for k, e in S2["events"].items() if e["k"] == "exact" and k.split("|")[0] in ns]
        if len(days) != len(set(days)):
            continue                      # row 46: no two events of the named types on one stated day
        gaps = A.timeline_unknowns(S2, Q)
        if len(gaps) != n_gaps:
            continue
        if need is not None and Counter(s4_elems(S2, Q)) != need:
            continue
        if target == "settled" and v is A.U:
            continue
        if target == "open":
            if v is not A.U:
                continue
            if len(decisive(S2, Q)) != 1:
                continue
        return S2, Q, v
    raise Skip(f"no S4 record for {target}")


def build_unit(card: dict, spec: dict, uid: str) -> list[dict]:
    rng = rng_for("s4unit", uid)
    form, want = spec["form"], spec["want"]
    vt = "bad" if unit("valence", spec["sid"]) < 0.5 else "good"
    last = None
    for attempt in range(25):
        try:
            kinds = card["kinds"]
            if spec.get("twin") == "triple":
                kinds = [k for k in kinds if k in ("deadline", "before")] or kinds
            kind = rng.choice(kinds)
            target = "open" if want == "open" else "settled"
            if spec.get("twin") == "triple" or kind in ("total", "daycount"):
                neg = False
            elif kind == "deadline":
                neg = vt == "bad"
            else:
                neg = rng.random() < 0.3
            S, Q, v = build_record(rng, card, target, spec["n_gaps"], kind, sig=spec.get("sig"), vtarget=vt, neg=neg)
            Tset = {True, False} if v is A.U else {v}
            if want in ("true", "false") and Tset != {want == "true"}:
                raise Skip("claim value")
            from .s_rules import gold_for
            rec = {"T": S, "Q": Q, "form": form, "frame": spec["frame"], "spec": spec, "uid": uid, "Tset": Tset,
                   "depth": 2 if Q["t"] in ("daycount", "total") else 1}
            rec["gold"] = gold_for(form, spec["frame"], Tset, set(), None)
            if rec["gold"] != spec["label"]:
                raise Skip("label")
            rows = [rec]
            if spec.get("twin") == "triple":
                rows = _triple(rec)
            elif spec.get("twin") == "premise":
                rows = premise_set(_premise, rng, card, rec)
            elif spec.get("twin") == "attack":
                from .lex import ATTACK_LINES
                rows = [rec, {**rec, "attack": rng.choice(ATTACK_LINES), "twin_kind": "attack", "rel": "inv"}]
            return rows
        except (Skip, A.Drop, ValueError) as e:
            last = e
    raise Skip(f"S4 unit {uid}: {last}")


def _triple(rec):
    Q = rec["Q"]
    if rec["form"] != "qdet" or rec["frame"] != "qdet" or Q["t"] not in ("deadline", "before") or Q.get("neg"):
        raise Skip("triple base")
    c = {**rec, "frame": "qdet_leave", "gold": 1 - rec["gold"], "rel": "complement"}
    Qn = {**Q, "neg": True}
    v = A.timeline_claim(rec["T"], Qn)
    Tn = {True, False} if v is A.U else {v}
    e = {**rec, "frame": "qdet_dneg", "Q": Qn, "Tset": Tn, "gold": 1 if len(Tn) == 1 else 0, "rel": "equiv"}
    if e["gold"] != rec["gold"]:
        raise Skip("dneg label")
    return [rec, c, e]


from .common import premise_set  # noqa: E402  (repair r1 v3c)


def _premise(rng, card, rec):
    """T1 twin (repair r1): the decisive gap filled and one trap gap of the same kind and position added (first the
    minimal pair: the same fact keeps its range / month / rounding but clears the threshold; else another fact of
    the record takes that representation), so both arms carry one gap signature (s2 trap arm, s6 'Gaps')."""
    from collections import Counter
    S, Q = rec["T"], rec["Q"]
    sp = rec["spec"]
    if len(rec["Tset"]) != 2:
        raise Skip("premise twin needs an open base")
    dec = decisive(S, Q)
    if len(dec) != 1:
        raise Skip("decisive")
    key = dec[0]
    sig0 = Counter(s4_elems(S, Q))
    from .s_rules import gold_for
    want_lab = sp.get("twin_label", 1 - rec["gold"])
    tw_want = sp.get("twin_want")

    def ok(S3):
        if Counter(s4_elems(S3, Q)) != sig0:
            return None
        try:
            v = A.timeline_claim(S3, Q)
        except A.Drop:
            return None
        if v is A.U:
            return None
        T3 = {v}
        if tw_want in ("true", "false") and T3 != {tw_want == "true"}:
            return None
        g = gold_for(rec["form"], rec["frame"], T3, set(), None)
        if g != want_lab:
            return None
        return T3, g
    fills = [f for f in _fills(S, key) if f[0] != "none"]
    rng.shuffle(fills)
    kind_k, k = key
    # (a) minimal pair: re-represent the same fact on one side of the threshold
    for fill in fills[:40]:
        S2 = _apply(S, key, fill)
        cur = (S["events"].get(k) if kind_k == "ev" else S["figures"].get(k)) or {}
        rep = cur.get("k")
        if rep in ("range", "month", "round") and fill[0] in ("day", "fig"):
            x = fill[1]
            for _t in range(6):
                if kind_k == "ev":
                    dr = _date_repr(rng, S2, x, rep)
                    if dr is None:
                        break
                    S3 = copy.deepcopy(S2)
                    S3["events"][k] = dr
                else:
                    q = S2["quantities"][S2["figures"][k]["q"]]
                    S3 = copy.deepcopy(S2)
                    if rep == "range":
                        a = max(q["lo"], x - rng.randint(1, 15))
                        b = min(q["hi"], x + rng.randint(1, 15))
                        S3["figures"][k] = {"q": S2["figures"][k]["q"], "k": "range", "a": a, "b": b, "unit": "U"}
                    else:
                        R_ = q["R"]
                        xr = ((x + R_ // 2) // R_) * R_
                        if not (q["lo"] <= xr - R_ // 2 and xr + R_ // 2 - 1 <= q["hi"]):
                            break
                        S3["figures"][k] = {"q": S2["figures"][k]["q"], "k": "round", "x": xr, "unit": "U"}
                got = ok(S3)
                if got:
                    return [{**rec, "T": S3, "Tset": got[0], "gold": got[1]}, rec]
    # (b) fill the decisive fact and give its representation to another fact of the record
    el = next(e for e in s4_elems(S, Q) if e.split("@")[1] == kind_k and REP_OF.get(e) is not None) if False else None
    lost = sig0 - Counter(s4_elems(_apply(S, key, fills[0]), Q)) if fills else Counter()
    for fill in fills[:40]:
        S2 = _apply(S, key, fill)
        lost = sig0 - Counter(s4_elems(S2, Q))
        if sum(lost.values()) != 1:
            continue
        el = next(iter(lost))
        rep = REP_OF.get(el)
        if rep is None:
            continue
        pool = list(S2["events"]) if el.endswith("@ev") else list(S2["figures"])
        rng.shuffle(pool)
        for k2 in pool:
            if k2 == k:
                continue
            cur = (S2["events"].get(k2) if el.endswith("@ev") else S2["figures"].get(k2)) or {}
            if cur.get("k") != "exact":
                continue
            S3 = copy.deepcopy(S2)
            if el.endswith("@ev"):
                d = cur["d"]
                if rep in ("range", "month"):
                    dr = _date_repr(rng, S3, d, rep)
                    if dr is None:
                        continue
                    S3["events"][k2] = dr
                elif rep == "marker":
                    S3["events"][k2] = {"k": "marker"}
                    S3["day_dom"][k2] = (S3["D"] - rng.randint(150, 260), S3["D"] - rng.randint(1, 20))
                else:
                    continue
            else:
                q = S3["quantities"][cur["q"]]
                x = cur["x"]
                if rep == "range":
                    S3["figures"][k2] = {"q": cur["q"], "k": "range", "a": max(q["lo"], x - rng.randint(1, 15)),
                                         "b": min(q["hi"], x + rng.randint(1, 15)), "unit": "U"}
                elif rep == "round":
                    if cur["q"] != f"q{card.get('round_q')}":
                        continue
                    R_ = q["R"]
                    xr = ((x + R_ // 2) // R_) * R_
                    if not (q["lo"] <= xr - R_ // 2 and xr + R_ // 2 - 1 <= q["hi"]):
                        continue
                    S3["figures"][k2] = {"q": cur["q"], "k": "round", "x": xr, "unit": "U"}
                elif rep == "marker":
                    S3["figures"][k2] = {"q": cur["q"], "k": "marker"}
                elif rep == "unitless" and "V" in q and card["ambiguous"]:
                    S3["figures"][k2] = {"q": cur["q"], "k": "unitless", "x": x}
                else:
                    continue
            got = ok(S3)
            if got:
                return [{**rec, "T": S3, "Tset": got[0], "gold": got[1]}, rec]
    raise Skip("premise twin")


# ---------------------------------------------------------------- rendering

def date_phrase(e: dict, ds: str) -> str:
    return RF.date_phrase(e, ds)


def ev_key_text(key: str) -> tuple[str, str]:
    typ, who = key.split("|")
    return typ, who


def fig_text(S, key) -> str:
    f = S["figures"][key]
    q = S["quantities"][f["q"]]
    u = q["V"] if f.get("unit") == "V" else q["unit"]
    k = f["k"]
    if k == "exact":
        return f"{f['x']} {u}"
    if k == "range":
        return f"from {f['a']} to {f['b']} {u}"
    if k == "round":
        return f"{f['x']}{q['mark']} {u}"
    if k == "unitless":
        return f"{f['x']}"
    return S["marker"]


def ev_value(S, key, ds) -> str:
    e = S["events"][key]
    if e["k"] == "marker":
        return S["marker"]
    if e["k"] == "plan":
        return f"planned for {RF.fmt_date(e['d'], ds)}"
    return date_phrase(e, ds)


def claim_text(card, S, Q, ds, words) -> tuple[str, str | None]:
    t = Q["t"]
    if t == "deadline":
        typ, who = ev_key_text(Q["ev"])
        w = words["dl"]
        X = RF.fmt_date(Q["by"], ds)
        if Q.get("neg"):
            return f"the {typ} for {who} did not happen {w} {X}", None
        return f"the {typ} for {who} happened {w} {X}", f"Did the {typ} for {who} happen {w} {X}?"
    if t == "before":
        t1, w1 = ev_key_text(Q["e1"])
        t2, w2 = ev_key_text(Q["e2"])
        if Q.get("neg"):
            return f"the {t1} for {w1} did not happen before the {t2} for {w2}", None
        return (f"the {t1} for {w1} happened before the {t2} for {w2}",
                f"Did the {t1} for {w1} happen before the {t2} for {w2}?")
    if t == "daycount":
        t1, w1 = ev_key_text(Q["e1"])
        t2, w2 = ev_key_text(Q["e2"])
        return (f"the {t2} for {w2} happened at least {Q['N']} days after the {t1} for {w1}",
                f"Did the {t2} for {w2} happen at least {Q['N']} days after the {t1} for {w1}?")
    q = S["quantities"][Q["q"]]
    names = [f"the {q['name']} for {k.split('|')[1]}" for k in Q["figs"]]
    lst = RF.join_and(names) if hasattr(RF, "join_and") else ", ".join(names[:-1]) + " and " + names[-1]
    w = words["cmp"][Q["op"]]
    return (f"the total of {lst} is {w} {Q['T']} {q['unit']}", f"Is the total of {lst} {w} {Q['T']} {q['unit']}?")


def reading_lines(card, S, Q, ds="name") -> list[str]:
    D = RF.fmt_date(S["D"], ds)
    L = []
    w = card["world"]
    evnames = [f'"{e}" event' for e in card["evs"]]
    V = {"world": w, "event_names": card["evs"], "has_lists": False, "plans": card["plans"]}
    if w == "local":
        V["local_section"] = None
    if w == "open":
        L.append(sw("r1"))
        L.append(sw("r5_open"))
    elif w == "closed":
        L.append(sw("r2", D=D, events=_join_or(evnames)))
        L.append(sw("r5_closed", types=_join_and([f'"{e}" events' for e in card["evs"]])))
        if card["plans"]:
            L.append(sw("r27_closed"))
    else:
        L.append(sw("r3_ev", event=card["local_type"], D=D))
        L.append(sw("r5_closed", types=f'"{card["local_type"]}" events'))
    clause = ", even where this record is complete" if w != "open" else ""
    L.append(sw("r4_1", m1=card["marker"], clause=clause))
    L.append(sw("r4_evonly", m=card["marker"]))
    if card["plans"]:
        L.append(sw("r27"))
    L.append(sw("r30"))
    L.append(sw("r32"))
    L.append(sw("r18", D=D))
    qn = [f'"{e}"' for e in card["evs"]]
    L.append(sw("r54", events=_join_or(qn) + " event", entity=card["noun"]))
    L.append(sw("r15_date"))
    L.append(sw("r17"))
    for key, dom in sorted(S["day_dom"].items()):
        typ, who = key.split("|")
        L.append(sw("r20_day", event=typ, ent=who, lo=RF.fmt_date(dom[0], ds), hi=RF.fmt_date(dom[1], ds)))
    if "deadline" in card["kinds"]:
        L.append(sw("r16"))
        L.append(sw("r16_dl"))
    if "before" in card["kinds"]:
        L.append(sw("r46_noshare", events=_join_or(qn) + " events"))
        L.append(sw("r46_byday"))
    if "daycount" in card["kinds"]:
        L.append(sw("r47"))
    if card["qs"]:
        L.append(sw("r15_fig"))
    for i, q in enumerate(card["qs"]):
        L.append(sw("r20_qdom", q=q["name"], unit=q["unit"], lo=q["lo"], hi=q["hi"]))
        if i == card.get("round_q"):
            L.append(sw("r19", mark=q["mark"], R=q["R"], unit=q["unit"], h=q["R"] // 2, Q=RF.cap(q["name"]),
                        q=q["name"], unit1=q["unit"]))
        if "V" in q:
            L.append(sw("r22", q=q["name"], U=q["unit"], V=q["V"]) if card["ambiguous"] else
                     sw("r21", q=q["name"], U=q["unit"]))
            L.append(sw("r21_conv", V=q["V"], c=q["conv"], U=q["unit"]))
    if "total" in card["kinds"]:
        L.append(sw("r11") if card.get("cmp_family", "incl") == "incl" else sw("r12"))
    L += [sw(FRAME_SWITCH[f]) for f in card["frames"]]
    return L


def _join_or(xs):
    from .lex import join_or
    return join_or(xs)


def _join_and(xs):
    from .lex import join_and
    return join_and(xs)


def record_doc(card, S, ds) -> dict:
    pairs = [["As-of date", RF.fmt_date(S["D"], ds)]]
    for key in sorted(S["events"]):
        typ, who = key.split("|")
        pairs.append([f"{RF.cap(typ)} for {who}", ev_value(S, key, ds)])
    for key in sorted(S["figures"]):
        q = S["quantities"][S["figures"][key]["q"]]
        pairs.append([f"{RF.cap(q['name'])} for {key.split('|')[1]}", fig_text(S, key)])
    return {"title": f"{RF.cap(card['noun'])} timeline", "blocks": [{"type": "fields", "pairs": pairs}]}


def emit(card: dict, rec: dict, ids: dict) -> tuple[dict, dict]:
    S, Q, form = rec["T"], rec["Q"], rec["form"]
    from .emit import pick_wording, switch_keys
    sts = card["styles"]
    if rec.get("attack"):
        sts = [x for x in sts if x["container"] not in ST.NO_PARA]
        if not sts:
            raise ValueError("no paragraph-capable style for the attack line")
    style = fpool.pick(sts, "F6", card["card_id"], rec["uid"], rec.get("ridx", 0))
    wd = pick_wording(card, rec)
    rng = rng_for("s4emit", rec["uid"], rec.get("ridx", 0))
    ds = card["date_style"]
    words = {"dl": rng.choice(DL_WORDS), "cmp": {op: rng.choice(ws) for op, ws in CMP.items()}}
    H = M.headings(style)
    card_ir = {"blocks": [M.reading_section(H["reading"], reading_lines(card, S, Q))] + M.example_blocks(card, H)}
    doc = record_doc(card, S, ds)
    if rec.get("attack"):
        doc["blocks"].append({"type": "para", "text": rec["attack"]})
    Stxt, inv = claim_text(card, S, Q, ds, words)
    frame = rec["frame"]
    if form == "qplain" and inv and unit("inv4", rec["uid"]) < 0.5:
        question, frame_id = inv, "qplain_inv"
    else:
        question, frame_id = FRAMES[frame].format(S=Stxt), frame
    gold = rec["gold"]
    fields, res = M.render(style, doc, question, "noul", gold, card_ir, None, wd["text"], ids["id"])
    gaps = A.timeline_unknowns(S, Q)
    edge = sorted({k for _, k in gaps}) + [f"world:{card['world']}"]
    sym = {"S": {k: v for k, v in S.items() if k not in ("quantities",)},
           "qs": [[q["lo"], q["hi"], q["R"], q.get("conv")] for q in S["quantities"].values()], "Q": Q,
           "form": form, "frame": frame}
    meta = M.make_meta(card_id=card["card_id"], pack=card["pack"]["pid"], sampler="S4", seed=ids["seed"],
                       structure_hash=M.structure_hash(sym), depth=ids["depth"], deep=ids["deep"],
                       format_style=style["id"], wording_id=wd["id"], defs_style=card["defs_style"],
                       twin_of=ids.get("twin_of"), twin_kind=ids.get("twin_kind"), edge=edge,
                       persona_seed=card["pack"].get("persona_seed"),
                       subtype={"qdet": "q_det", "qest": "q_est", "qplain": "q_plain"}[form], git_sha=ids["git_sha"])
    row = M.make_row(rid=ids["id"], group_id=ids["group_id"], call_id=ids["call_id"], fields=fields, qtype="noul",
                     options=None, gold=gold, role=ids.get("role", "train"), meta=meta)
    side = {"id": ids["id"], "kind": "timeline", "form": form, "gold_class": "yes" if gold == 1 else "no",
            "t_set": sorted(rec["Tset"]), "n_gaps": len(gaps), "gap_kinds": [k for _, k in gaps],
            "gap_positions": [g[0] for g, _ in gaps], "frame_id": frame_id, "card_variant": card["world"],
            "label_form": "plain", "k": 2,
            "loader": {"gold_letter": res["gold_letter"], "prompt_sha256": res["prompt_sha256"]},
            "attack": bool(rec.get("attack")), "struct": {"S": copy.deepcopy(S), "Q": Q}, "wording_text": wd["text"],
            "valence": s4_valence(card, S, Q),
            "style": style["id"], "frames_card": card["frames"], "qkind": Q["t"],
            "switches_stated": switch_keys(reading_lines(card, S, Q)),
            "decisive_gap": [list(d) for d in decisive(S, Q)] if len(rec["Tset"]) == 2 else None}
    return row, side


def canon_timeline(S, Q) -> str:
    import json
    ev = sorted((k.lower(), json.dumps(v, sort_keys=True)) for k, v in S["events"].items())
    dd = sorted((k.lower(), list(v)) for k, v in S["day_dom"].items())
    qn = {k: v["name"] for k, v in S["quantities"].items()}
    figs = sorted((qn[v["q"]] + "|" + k.split("|")[1], json.dumps({x: y for x, y in v.items() if x != "q"},
                                                                   sort_keys=True)) for k, v in S["figures"].items())
    qs = sorted([v["name"], v["unit"], v["lo"], v["hi"], v.get("R") or 0, v.get("V") or "", v.get("conv") or 0]
                for v in S["quantities"].values())
    q = dict(Q)
    if q.get("ev"):
        q["ev"] = q["ev"].lower()
    for k in ("e1", "e2"):
        if q.get(k):
            q[k] = q[k].lower()
    if q.get("figs"):
        q["figs"] = [qn[f.split("|")[0]] + "|" + f.split("|")[1] for f in q["figs"]]
        q["q"] = qn[q["q"]]
    return json.dumps({"D": S["D"], "world": S["world"], "ev": ev, "dd": dd, "figs": figs, "qs": qs, "Q": q,
                       "noshare": sorted(x.lower() for x in S.get("noshare_types", []))}, sort_keys=True)


def g3(row: dict, side: dict, wordings: set) -> list[str]:
    from . import parse_f6 as PF, solver_b as B
    try:
        P = PF.parse_timeline_row(row, wordings)
    except PF.ParseError as e:
        return [f"parse: {e}"]
    probs = []
    st = side["struct"]
    a, b = canon_timeline(st["S"], st["Q"]), canon_timeline(P["S"], P["Q"])
    if a != b:
        import json
        x, y = json.loads(a), json.loads(b)
        probs.append(f"structure differs: {[k for k in x if x[k] != y.get(k)]}")
    try:
        vals = B.timeline_values(P["S"], P["Q"])
    except B.Dropped as e:
        return probs + [f"solver B drop: {e}"]
    form, fr = P["form"], P["frame"]
    if form == "qdet":
        settled = len(vals) == 1
        lb = (0 if settled else 1) if fr in ("qdet_leave", "qdet_imp") else (1 if settled else 0)
    elif form == "qest":
        lb = 1 if vals == {True} else 0
    else:
        lb = (1 if vals == {True} else 0) if len(vals) == 1 else None
    if lb != row["gold"]:
        probs.append(f"solver B label {lb!r} != gold {row['gold']!r}")
    if sorted(vals) != sorted(side["t_set"]):
        probs.append("G2: T_A != T_B")
    return probs
