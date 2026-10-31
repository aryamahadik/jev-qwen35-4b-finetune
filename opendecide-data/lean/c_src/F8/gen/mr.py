"""Metamorphic relations (G4; G0 spec 6). Test-only: MR outputs never enter a row file.

run_all(card, S, raw, fld, B) -> {MR id: True | False} for every relation that applies to the row.
  MR1 shuffle options (choice): another display order renders and its gold letter maps back to the same gold text
  MR2 rename entities (IDs re-drawn, order kept for the tie rule): label unchanged (by entity position)
  MR3 restate one stated chance in another exact form, render, parse, solver B: label unchanged
  MR4 multiply every amount-valued number by an integer factor >= 2: label unchanged
  MR5 add an inert fact (render, parse, solver B): label unchanged
  MR6 reorder entities (IDs move with them): label unchanged (as an entity ID)
  MR7 monotone push: per form (6, MR7 column)
  MR8 multiply every P(E | Hj) by the same factor (rates rows): posterior and label unchanged
  MR9 negate the YN question: opposite label; negate twice: same label
  MR11 open world: fixing an unknown keeps a determined label; an undetermined row has two fills with two labels
Hypothesis is not installed here (no package installs); the relations use seeded random draws instead.
"""
from __future__ import annotations

import copy
import random
from fractions import Fraction as Fr

import hashes as H
import parse as PZ
import render as RD
import solver_a as SA
import solver_b as SB
from numfmt import has_text


def _ans(S):
    try:
        r = SA.solve(S)
        return r["ans"], r["det"]
    except (SA.Undetermined, ValueError, ZeroDivisionError):
        return "UNDEF", False


def _key_ans(S):
    """Solver A's answer in the form solver B reports on a parsed row (repair r2): a 5-entity rank_order row whose
    true order is not among the shown orders has gold key NOTA (render.gold_key), as in check_and_render's G3 check."""
    a, d = _ans(S)
    if S["form"] == "rank_order" and isinstance(a, tuple):
        a = RD.gold_key(S, a)
    return a, d


def _ids(S):
    return [e["id"] for e in S["ents"]]


def _as_ids(S, a):
    if isinstance(a, int) and not isinstance(a, bool) and S["form"] in ("rank_top", "dec", "inv"):
        return S["ents"][a]["id"]
    if isinstance(a, tuple):
        return tuple(S["ents"][i]["id"] for i in a)
    return a


def _textual(card, S2, row_style, B, rng, inert=None):
    """Render S2 in the given style, parse it back and solve with solver B; returns the answer or None."""
    opts = None
    row = {"version": "full" if S2.get("_version") is None else S2["_version"], "wording": "Answer.", "qvar": 0,
           "qt": S2.get("_qt"), "people": ["Reviewer"], "style": row_style, "inert": inert, "inert_pos": 1}
    if S2["form"] not in ("yn_thr", "yn_act"):
        opts = [t for t, _ in RD.options_for(card, S2)]
        rng.shuffle(opts)
        row["options"] = opts
    try:
        f = RD.render_fields(card, S2, row)
    except Exception:          # noqa: BLE001 - a style that cannot show the variant is skipped
        return None
    raw = {"id": "mr", "qtype": f["qtype"], "state": f["state"], "instructions": f["instructions"],
           "card": f["card"], "options": f["options"], "meta": {"format_style": row_style}}
    try:
        S3 = PZ.assemble(PZ.parse_row(raw), raw)
        rb = SB.solve(S3)
    except Exception:          # noqa: BLE001
        return "PARSE_FAIL"
    return rb["ans"], rb["det"]


def mr1(card, S, raw, fld, B, rng):
    if raw["qtype"] != "choice":
        return None
    from fmt1 import card as fcard
    n = len(raw["options"])
    perm = list(range(n))
    rng.shuffle(perm)
    res = fcard.loader_check({**raw, "gold": raw["gold"]}, perm=perm, check_rows=False)
    return res["ok"]


def mr2(card, S, raw, fld, B, rng):
    T = copy.deepcopy(S)
    nums = sorted(rng.sample(range(1000, 9999), len(T["ents"])))
    order = sorted(range(len(T["ents"])), key=lambda i: int(T["ents"][i]["id"].rsplit("-", 1)[1]))
    for rank, i in enumerate(order):
        T["ents"][i]["id"] = f"ZQ-{nums[rank]}"
    return _ans(T) == _ans(S)


def _chances(S):
    out = []
    for i, e in enumerate(S["ents"]):
        for k, o in enumerate(e.get("outs") or []):
            if o["p"] is not None:
                out.append(("out", i, k))
        if e.get("ch") is not None and e["ch"]["p"] is not None:
            out.append(("ch", i, None))
        if e.get("en") is not None:
            out.append(("en", i, None))
        if e.get("mat") is not None:
            out.append(("mat", i, None))
    return out


def mr3(card, S, raw, fld, B, rng):
    cs = _chances(S)
    if not cs:
        return None
    kind, i, k = rng.choice(cs)
    T = copy.deepcopy(S)
    e = T["ents"][i]
    slot = {"out": lambda: (e["outs"][k], "p", "prep", "pden"), "ch": lambda: (e["ch"], "p", "rep", "den"),
            "en": lambda: (e["en"], "p", "rep", "den"), "mat": lambda: (e["mat"], "lik", "rep", "den")}[kind]()
    obj, vk, rk, dk = slot
    v = obj[vk]
    for rep in rng.sample(["pct0", "pct1", "dec", "frac", "ain"], 5):
        den = None
        if rep in ("frac", "ain"):
            den = v.denominator if v.denominator <= 1000 else None
            if den is None:
                continue
        if rep != obj[rk] and has_text(v, rep, den):
            obj[rk], obj[dk] = rep, den
            break
    else:
        return None
    a = _textual(card, T, raw["meta"]["format_style"], B, rng)
    if a is None:
        return None
    return a == _key_ans(S)


def mr4(card, S, raw, fld, B, rng):
    if not any(e.get("outs") or e.get("cost") is not None or (e.get("pts") or {}).get("a") or e.get("mat")
               for e in S["ents"]):
        return None
    k = rng.choice([2, 3, 5, 10])
    T = copy.deepcopy(S)
    R = T["rules"]
    for e in T["ents"]:
        for o in e.get("outs") or []:
            for key in ("a",):
                if o[key] is not None:
                    o[key] *= k
            if o.get("arng"):
                o["arng"] = (o["arng"][0] * k, o["arng"][1] * k)
        if e.get("cost") is not None:
            e["cost"] *= k
        if e.get("pts"):
            e["pts"]["a"] = {n: (v * k if v is not None else None) for n, v in e["pts"]["a"].items()}
        if e.get("mat"):
            e["mat"]["amt"] *= k
        if e.get("ch") is not None and e["ch"].get("amt") is not None:
            e["ch"]["amt"] *= k

    def scale_cond(c):
        for p in c["parts"]:
            if p["t"] == "amt" or (p["t"] == "q" and p["q"]["k"] in ("el", "tec", "ev")):
                p["v"] = p["v"] * k
    for ln in (R.get("scorecard") or {}).get("lines", []):
        scale_cond(ln["cond"])
        if ln.get("unless"):
            scale_cond(ln["unless"])
    for c in list((R.get("only_if") or {}).values()) + [o["cond"] for o in R.get("overrides") or []] + \
            list((R.get("arules") or {}).values()):
        scale_cond(c)
    if R.get("mat"):
        R["mat"]["imp_edges"] = [x * k for x in R["mat"]["imp_edges"]]
    if R.get("inv") and R["inv"]["kind"] == "q" and R["inv"]["q"]["k"] in ("el", "tec", "ev"):
        R["inv"]["v"] = R["inv"]["v"] * k
    if T["form"] == "yn_thr":
        qk = T["q"]["k"] if T["q"]["k"] != "risk" else T["q"]["def"]
        if qk in ("el", "tec", "ev"):
            T["thr"]["T"] = T["thr"]["T"] * k
    return _ans(T) == _ans(S)


def mr5(card, S, raw, fld, B, rng):
    pack = B.packs[card["pack"]]
    inert = None
    labs = set()
    for e in S["ents"]:
        if e.get("bay"):
            labs |= set(e["bay"]["hyps"]) | set(e["bay"]["signs"])
    cand = [x for x in pack["inert"] if not any(l.lower() in x.lower() for l in labs)]
    if not cand:
        return None
    inert = rng.choice(cand)
    a = _textual(card, S, raw["meta"]["format_style"], B, rng, inert=inert)
    if a is None:
        return None
    return a == _key_ans(S)


def mr6(card, S, raw, fld, B, rng):
    if len(S["ents"]) < 2:
        return None
    T = copy.deepcopy(S)
    idx = list(range(len(T["ents"])))
    rng.shuffle(idx)
    T["ents"] = [T["ents"][i] for i in idx]
    if T.get("case") is not None:
        T["case"] = idx.index(S["case"])
    if T.get("subset"):
        T["subset"] = dict(T["subset"], X=idx.index(S["subset"]["X"]))
    return _as_ids(T, _ans(T)[0]) == _as_ids(S, _ans(S)[0])


def mr7(card, S, raw, fld, B, rng):
    """Monotone push (closed world): the stated expected direction per form."""
    if S["world"] != "closed":
        return None
    f = S["form"]
    T = copy.deepcopy(S)
    a0 = _ans(S)[0]

    def push(e, q, up=True):
        k = q.get("k")
        if k == "risk":
            k = q["def"]
        if k in ("el", "tec", "ev"):
            o = max(e["outs"], key=lambda o: o["a"]) if up else e["outs"][0]
            o["a"] = o["a"] + (100 if up else -min(100, o["a"]))
            return o["a"] >= 0
        if k == "chance":
            c = e["ch"] if e.get("ch") is not None else None
            if c is None:
                return False
            nv = c["p"] + (Fr(1, 100) if up else -Fr(1, 100))
            if not (0 <= nv <= 1):
                return False
            c["p"], c["rep"], c["den"] = nv, "pct1" if (nv * 100).denominator != 1 else "pct0", None
            return True
        if k == "en":
            e["en"]["n"] += 1 if up else -1
            return e["en"]["n"] >= 1
        if k == "post":
            b = e["bay"]
            h = q["h"]
            if b["form"] == "rates" and len(b["signs"]) == 1:
                s = b["signs"][0]
                cur = b["lik"][s][h]
                step = Fr(1, 100) if (b["sig"][s] == up) else -Fr(1, 100)
                nv = cur + step
                if not (0 < nv < 1):
                    return False
                b["lik"][s][h] = nv
                b["rep"]["lik_list"] = [("frac", None)] * len(b["hyps"])
                return True
            if b["form"] in ("counts",):
                s = b["signs"][0]
                col = 0 if b["sig"][s] else 1
                b["cnt"][s][h][col] += 1 if up else 0
                return up
            if b["form"] == "nE":
                s = b["signs"][0]
                b["ne"][s][h] += 1 if up else 0
                return up
            return False
        if k == "score":
            f_ = [x for x, v in e["pts"]["b"].items() if v]
            if f in ("inv", "rank_top", "rank_order"):
                # repair r2: the added scorecard line applies to every entity, so on many-entity forms it is a push
                # of the target alone only when no other entity has that feature (else the relation does not apply)
                f_ = [x for x in f_ if not any(o is not e and (o.get("pts") or {}).get("b", {}).get(x)
                                               for o in T["ents"])]
            if not f_ or not up:
                return False
            R = T["rules"] = copy.deepcopy(T["rules"])
            R["scorecard"]["lines"].append({"cond": {"conn": "and", "parts": [{"t": "bool", "f": f_[0]}]}, "pts": 1})
            return True
        return False
    if f == "yn_thr":
        op = S["thr"]["op"]
        up = op in (">", ">=")
        if not push(T["ents"][T["case"]], T["q"], up=True):
            return None
        a1 = _ans(T)[0]
        aff0 = a0 if S["thr"]["neg"] % 2 == 0 else (not a0)
        aff1 = a1 if S["thr"]["neg"] % 2 == 0 else (not a1)
        return (not aff0 or aff1) if up else (aff0 or not aff1)
    if f in ("bin", "tier"):
        if not push(T["ents"][T["case"]], T["q"] if f == "bin" else {"k": "score"}, up=True):
            return None
        a1 = _ans(T)[0]
        return a1 >= a0
    if f == "mat":
        T["ents"][0]["mat"]["amt"] += 100
        return _ans(T)[0] >= a0
    if f == "rank_top":
        hi = S["hl"] == "high"
        if not push(T["ents"][a0], T["q"], up=hi):
            return None
        return _ans(T)[0] == a0
    if f == "rank_order":
        first = a0[0]
        if not push(T["ents"][first], T["q"], up=True):
            return None
        return _ans(T)[0] == a0
    if f == "dec":
        others = [i for i in range(len(S["ents"])) if i != a0]
        if not others:
            return None
        T["ents"][rng.choice(others)]["cost"] += 50
        return _ans(T)[0] == a0
    if f == "pred":
        e = T["ents"][T["case"]]
        if not push(e, {"k": "post", "h": a0}, up=True):
            return None
        return _ans(T)[0] == a0
    if f == "inv":
        r = S["rules"]["inv"]
        if r["kind"] != "q" or a0 == "NOTA":
            return None
        up = r["op"] in (">", ">=")
        if not push(T["ents"][a0], r["q"], up=up):
            return None
        return _ans(T)[0] == a0
    return None


def mr8(card, S, raw, fld, B, rng):
    e = S["ents"][S["case"]] if S.get("case") is not None and S["form"] in ("yn_thr", "bin", "pred") else None
    if e is None or not e.get("bay") or e["bay"]["form"] != "rates" or len(e["bay"]["signs"]) != 1:
        return None
    b = e["bay"]
    s = b["signs"][0]
    if not b["sig"][s] or any(x is None for x in b["lik"][s]):
        return None
    T = copy.deepcopy(S)
    f = rng.choice([Fr(1, 2), Fr(1, 4), Fr(3, 4)])
    T["ents"][T["case"]]["bay"]["lik"][s] = [x * f for x in b["lik"][s]]
    p0 = SA.post_vec(e, SA.CV())
    p1 = SA.post_vec(T["ents"][T["case"]], SA.CV())
    return p0 == p1 and _ans(T) == _ans(S)


def mr9(card, S, raw, fld, B, rng):
    if S["form"] not in ("yn_thr", "yn_act"):
        return None
    key = "thr" if S["form"] == "yn_thr" else "act"
    a0 = _ans(S)[0]
    T1, T2 = copy.deepcopy(S), copy.deepcopy(S)
    T1[key]["neg"] = S[key]["neg"] + 1
    T2[key]["neg"] = S[key]["neg"] + 2
    return _ans(T1)[0] == (not a0) and _ans(T2)[0] == a0


def mr11(card, S, raw, fld, B, rng):
    if S["world"] != "open":
        return None
    slots = SA.unknown_slots(S)
    a0, det0 = _ans(S)
    vals = []
    for path, dom in slots:
        vals.append(dom[0] if not (path[0] == "pts" and path[2] == "b") else rng.choice([True, False]))
    T = SA.assign(S, slots, tuple(vals))
    T["world"] = "closed"
    a1, det1 = _ans(T)
    if det0:
        return det1 and a1 == a0
    # undetermined: the corner values give at least two different determined labels
    seen = set()
    import itertools
    for combo in itertools.product(*[d for _, d in slots]):
        Tc = SA.assign(S, slots, combo)
        Tc["world"] = "closed"
        a, d = _ans(Tc)
        if d:
            seen.add(repr(a))
    return len(seen) >= 2


RELS = {"MR1": mr1, "MR2": mr2, "MR3": mr3, "MR4": mr4, "MR5": mr5, "MR6": mr6, "MR7": mr7, "MR8": mr8,
        "MR9": mr9, "MR11": mr11}


def run_all(card, S, raw, fld, B, seed) -> dict:
    rng = random.Random(seed)
    out = {}
    for k, fn in RELS.items():
        try:
            r = fn(card, S, raw, fld, B, rng)
        except Exception as e:    # noqa: BLE001 - an exception inside a relation is a failure of that relation
            r = False
            out[k + ":exc"] = f"{type(e).__name__}: {str(e)[:60]}"
        if r is not None:
            out[k] = bool(r)
    return out
