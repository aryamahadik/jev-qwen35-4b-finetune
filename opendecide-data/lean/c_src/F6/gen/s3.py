"""S3: table-first registers with incomplete cells (G0 s7). A table of 5-60 records x 3-6 columns (ID + numbers and
categories), 1-3 marked cells (every marked cell is a visible gap, whatever its column), entity closure always
stated (row 42), an optional member list with world closure (rows 2-3), and a tie rule on C-REC cards (row 23).
Queries: at least one / every / no member (optionally filtered), count thresholds, membership (yes/no), and
argmax / argmin (C-REC). Labels from solver A's three-valued table filter; solver B enumerates the parse.
"""
from __future__ import annotations

import copy
import random

from . import common  # noqa: F401
from fmt1 import pool as fpool
from fmt1.render import BLANK

from .common import rng_for, unit, h64, day
from . import solver_a as A, rowmake as M, render_f6 as RF, styles_f6 as ST
from .lex import sw, FRAMES, OPTION_TEXT, FRAME_SWITCH

CMP_S3 = {">=": ["at least", "no fewer than", "no less than"], "<=": ["at most", "no more than"],
          ">": ["more than"], "<": ["fewer than", "less than"]}


class Skip(Exception):
    pass


# ---------------------------------------------------------------- cards

def make_card(card_id: str, schema: str, pack: dict) -> dict:
    rng = rng_for("card", card_id)
    case = rng.choice(pack["cases"])
    crec = schema == "c_rec"
    nq = 1 if schema == "c_rec" else 2     # C-REC: ID + key + one category column (compact, G0 s7)
    polar = [q for q in pack["qty"] if q.get("adverse")]
    other = [q for q in pack["qty"] if not q.get("adverse")]
    if crec:
        qty = rng.sample(pack["qty"], min(len(pack["qty"]), nq))
    else:                                 # repair r1: polar quantities first, so every claim carries a valence
        qty = rng.sample(polar, min(len(polar), nq))
        qty += rng.sample(other, max(0, min(len(other), nq - len(qty))))
    cats = rng.sample(pack["cat"], min(len(pack["cat"]), 1 if crec else rng.choice([1, 2])))
    cls = "json" if (rng.random() < 0.25 and not crec) else "text"
    member = (not crec) and cls == "text" and rng.random() < 0.6
    world = rng.choice(["open", "closed", "local"]) if member else rng.choice(["open", "closed"])
    blank = cls == "text" and world == "open" and rng.random() < 0.4
    styles = ST.training_styles("S3")
    if cls == "json":
        styles = [s for s in styles if s["skin"] == "json.array"]
    else:
        styles = [s for s in styles if s["skin"] != "json.array"]
        if member:
            styles = [s for s in styles if s["container"] in ("markdown_table", "html_snippet")]
        if blank:
            styles = [s for s in styles if s["skin"] not in ("csv.fixed_width",)]
        if crec:
            styles = [s for s in styles if s["container"] in ("csv", "markdown_table")]
    styles = fpool.card_style_set(styles, 6, "F6", card_id)
    cols = []
    for i, q in enumerate(qty):
        lo, hi = q["lo"], q["hi"]
        if hi - lo > 300:
            lo = rng.randint(lo, hi - 150)
            hi = lo + rng.randint(60, 150)
        cols.append({"id": f"q{i}", "name": q["name"], "kind": "num", "unit": q["unit"], "lo": max(lo, 0), "hi": hi,
                     "adverse": q.get("adverse")})
    for i, c in enumerate(cats):
        cols.append({"id": f"c{i}", "name": c["name"], "kind": "cat", "vals": list(c["values"])[:5]})
    card = {"card_id": card_id, "sampler": "S3", "schema": schema, "pack": pack, "noun": case["noun"],
            "plural": case["plural"], "prefix": case["prefix"], "cols": cols, "cls": cls, "member": member,
            "world": world, "blank": blank, "marker": rng.choice(["not recorded", "unknown"]),
            "list_name": ((pack["lists"][0] if (pack.get("set") == "packs-4" and pack["lists"]) else
                           f"{pack['role']} watch list") if member else None),
            "list_pol": (("good" if (pack.get("set") == "packs-4" and pack["lists"]) else "bad") if member else None),
            "styles": styles, "wordings": ST.card_wordings(card_id, schema == "yn"),
            "nei": rng.choice(OPTION_TEXT["nei"]), "none": rng.choice(OPTION_TEXT["none"]),
            "cmp_family": rng.choice(["incl", "excl"]), "year": rng.randint(2044, 2058),
            "defs_style": "short" if rng.random() < 0.08 else "one_line",
            "attack": rng.random() < 0.6,
            "filtered_rec": crec and rng.random() < 0.4}
    card["rec_key"] = next(c["id"] for c in cols if c["kind"] == "num")
    card["attack"] = card["attack"] and any(x["container"] not in ST.NO_PARA for x in styles)
    from . import examples_f6 as EX
    if card_id in EX.FEWSHOT_CARDS:
        card["defs_style"] = "one_line"
    n_ex, few = EX.card_flags(card_id, schema, card["defs_style"], "S3")
    exs, shots = EX.make(card, card["marker"], card["cmp_family"], n_ex, few) if n_ex else ([], [])
    card["examples"], card["fewshot"] = exs, shots
    if exs:
        card["defs_style"] = "one_line_examples"
    card["frames"] = (["qdet", "qdet_leave", "qdet_dneg", "qest_est", "qest_det", "qplain_true"]
                      if schema == "yn" else [])
    card["quants"] = ["every", "one", "no", "filter"] if schema == "yn" else []
    # repair r1 (length, AG-09): each yes/no card asks 2-3 query kinds and states the row 28 sentence of exactly the
    # quantifiers it uses (and the filter sentence only on cards that filter); card-level, never per row
    card["qkinds"] = ["exists", "forall", "none", "count"] if schema == "yn" else []
    card["filters"] = schema == "yn" and rng.random() < 0.5
    card["triple_ok"] = bool(member) and world == "open"
    return card


# ---------------------------------------------------------------- structures

def _ids(rng, prefix, n):
    out = set()
    while len(out) < n:
        out.add(f"{prefix}-{rng.randint(1000, 9999)}")
    out = list(out)
    rng.shuffle(out)
    return out


def _ops(card):
    return [">=", "<="] if card["cmp_family"] == "incl" else [">", "<"]


def _cond(rng, card, col):
    if col["kind"] == "num":
        ops = _ops(card)
        return {"col": col["id"], "op": rng.choice(ops), "n": rng.randint(col["lo"] + 2, col["hi"] - 2)}
    return {"col": col["id"], "v": rng.choice(col["vals"])}


def draw_table(rng, card, n_rec: int) -> dict:
    cols = card["cols"]
    D = day(card["year"], rng.randint(3, 12), rng.randint(1, 28))
    recs = []
    for rid in _ids(rng, card["prefix"], n_rec):
        cells = {}
        for c in cols:
            cells[c["id"]] = rng.randint(c["lo"], c["hi"]) if c["kind"] == "num" else rng.choice(c["vals"])
        recs.append({"id": rid, "cells": cells})
    T = {"kind": "table", "D": D, "world": card["world"], "cols": copy.deepcopy(cols), "records": recs,
         "list": None, "marker": card["marker"]}
    return T


def _flip(v):
    return {"good": "bad", "bad": "good"}.get(v)


def _atom_pol(card, cond):
    col = next((c for c in card["cols"] if c["id"] == cond["col"]), None)
    if not col or col["kind"] != "num" or col.get("adverse") not in ("high", "low"):
        return None
    up = cond["op"] in (">=", ">")
    return "bad" if up == (col["adverse"] == "high") else "good"


def s3_valence(card, Q):
    """'Yes = bad outcome' valence of S (s6 / XF04; repair r1): a member over an adverse limit is bad; 'every'
    and 'at least one' keep the atom's valence, 'no <member>' flips it, a count 'at least / more than' keeps it and
    'at most / fewer than' flips it; membership of a watch list is bad and of a trusted list good; 'not' flips."""
    t = Q["t"]
    if t == "member":
        v = card.get("list_pol")
    elif t in ("exists", "forall"):
        v = _atom_pol(card, Q["cond"])
    elif t == "none":
        v = _flip(_atom_pol(card, Q["cond"]))
    elif t == "count":
        a = _atom_pol(card, Q["cond"])
        v = a if Q["cmp"] in (">=", ">") else _flip(a)
    else:
        return None
    return _flip(v) if Q.get("neg") else v


def draw_query(rng, card, T, form: str, force_member: bool = False, vtarget=None, qtype=None, want=None) -> dict:
    cols = card["cols"]
    if form == "c_rec":
        Q = {"t": rng.choice(["argmax", "argmin"]), "key": card["rec_key"]}
        if card["filtered_rec"]:
            cat = next((c for c in cols if c["kind"] == "cat"), None)
            if cat:
                Q["filter"] = {"col": cat["id"], "v": rng.choice(cat["vals"])}
        return Q
    kinds = list(card.get("qkinds") or ["exists", "forall", "none", "count"]) + (["member"] * 2 if card["member"] else [])
    if vtarget and card["member"] and card["world"] == "open" and card.get("list_pol") and not force_member:
        # open-world lists: 'on the list' is never settled false and 'not on the list' never settled true, so a
        # membership query is drawn only when its valence and the wanted truth value can meet (repair r1)
        need_neg = {"true": False, "false": True}.get(want)
        if need_neg is not None and ((card["list_pol"] != vtarget) != need_neg):
            kinds = [x for x in kinds if x != "member"]
    t = qtype or rng.choice(kinds)
    if force_member:
        t = "member"
    if t == "member":
        neg = False
        if vtarget and not force_member and card.get("list_pol"):
            neg = card["list_pol"] != vtarget
        return {"t": "member", "who": None, "neg": neg}
    polar = [c for c in cols if c["kind"] == "num" and c.get("adverse") in ("high", "low")]
    col = rng.choice(polar) if (polar and vtarget) else rng.choice(cols)
    cond = _cond(rng, card, col)
    Q = {"t": t, "cond": cond}
    cats = [c for c in cols if c["kind"] == "cat" and c["id"] != col["id"]]
    if cats and card.get("filters", True) and rng.random() < 0.5:
        fc = rng.choice(cats)
        Q["filter"] = {"col": fc["id"], "v": rng.choice(fc["vals"])}
    if t == "count":
        Q["cmp"] = rng.choice(_ops(card))
        Q["N"] = rng.randint(2, max(2, len(T["records"]) - 1))
    if vtarget and col["kind"] == "num" and col in polar and s3_valence(card, Q) != vtarget:
        ops = _ops(card)
        if t == "count" and rng.random() < 0.5:
            Q["cmp"] = ops[1] if Q["cmp"] == ops[0] else ops[0]
        else:
            cond["op"] = ops[1] if cond["op"] == ops[0] else ops[0]
    return Q


def _value(T, Q):
    if Q["t"] in ("argmax", "argmin"):
        return A.table_argset(T, Q)
    return A.table_claim(T, Q)


def _settled(T, Q):
    v = _value(T, Q)
    return len(v) == 1 if isinstance(v, set) else v is not A.U


def _filter_ok(T, Q):
    """Filtered quantifiers: >= 2 records known to pass; filtered argmax: >= 1 (rows 28, 42)."""
    f = Q.get("filter")
    if not f:
        return True
    known = sum(1 for r in T["records"] if r["cells"][f["col"]] is not None and r["cells"][f["col"]] == f["v"])
    return known >= (1 if Q["t"] in ("argmax", "argmin") else 2)


def cell_elem(T, Q, cid):
    if Q["t"] in ("exists", "forall", "none") and Q["cond"]["col"] == cid:
        return "gap:quant@table"
    if Q["t"] == "count" and Q["cond"]["col"] == cid:
        return "gap:count@table"
    return "gap:value@table"


def norm_elem(e: str) -> str:
    """Query-column gaps (quant / count, by query type) match as one element class in the signature."""
    return "gap:query@table" if e in ("gap:quant@table", "gap:count@table") else e


def s3_elems_n(T, Q) -> list:
    return sorted(norm_elem(e) for e in s3_elems(T, Q))


def s3_elems(T, Q) -> list:
    out = [cell_elem(T, Q, cid) for rid, cid in A.table_marked(T)]
    if Q["t"] == "member" and T.get("list") and Q["who"] not in T["list"]["members"] and not T["list"]["closed"]:
        out.append("gap:closure@list")
    return sorted(out)


def tune_threshold(rng, card, T, Q, target, want) -> bool:
    """Repair r1 (efficiency of the planned query types): choose the condition threshold (and the count N) from the
    drawn table so that the full table already has the wanted truth value (settled targets), or hinges on exactly
    one record (open targets: marking that record's cell then leaves the claim open with one decisive gap). The
    record builder still checks every row with solver A; this only stops blind redraws. Returns False if no
    threshold works."""
    t = Q["t"]
    if t not in ("exists", "forall", "none", "count") or "n" not in Q["cond"]:
        return True
    col = next(c for c in T["cols"] if c["id"] == Q["cond"]["col"])
    lo, hi = col["lo"] + 2, col["hi"] - 2
    vals = sorted({r["cells"][col["id"]] for r in T["records"] if r["cells"][col["id"]] is not None})
    cands = sorted({x for v in vals for x in (v - 1, v, v + 1) if lo <= x <= hi})
    rng.shuffle(cands)
    want_v = {"true": True, "false": False}.get(want)

    def n_qual(Q2):
        n = 0
        for r in T["records"]:
            f = A._cell_cond(T, r, Q2["filter"]) if Q2.get("filter") else True
            c = A._cell_cond(T, r, Q2["cond"])
            n += (f is True and c is True)
        return n

    def n_fail(Q2):
        n = 0
        for r in T["records"]:
            f = A._cell_cond(T, r, Q2["filter"]) if Q2.get("filter") else True
            c = A._cell_cond(T, r, Q2["cond"])
            n += (f is True and c is False)
        return n
    for x in cands[:40]:
        Q2 = {**Q, "cond": {**Q["cond"], "n": x}}
        if t == "count":
            nq = n_qual(Q2)
            Ns = list(range(2, max(3, len(T["records"]))))
            rng.shuffle(Ns)
            for N in Ns[:12]:
                Q3 = {**Q2, "N": N}
                if target == "open":
                    ok = (Q3["cmp"] in (">=", ">") and nq == (N if Q3["cmp"] == ">=" else N + 1)) or \
                         (Q3["cmp"] in ("<=", "<") and nq == (N + 1 if Q3["cmp"] == "<=" else N))
                else:
                    ok = A.table_claim(T, Q3) is want_v if want_v is not None else A.table_claim(T, Q3) is not A.U
                if ok:
                    Q["cond"]["n"], Q["N"] = x, N
                    return True
            continue
        if target == "open":
            ok = (t == "exists" and n_qual(Q2) == 1) or (t == "forall" and n_fail(Q2) == 1) or \
                 (t == "none" and n_qual(Q2) == 1)
        else:
            v = A.table_claim(T, Q2)
            ok = (v is want_v) if want_v is not None else (v is not A.U)
        if ok:
            Q["cond"]["n"] = x
            return True
    return False


def build_table_record(rng, card, form, target, n_gaps, n_rec, want=None, force_member=False, sig=None,
                       vtarget=None, qtype=None):
    """A table + query with target 'settled' / 'open' and exactly n_gaps marked cells (plus the open membership on
    membership rows), with one decisive gap on open rows; with `sig` (repair r1) the marked cells realise exactly
    that kind@position signature (query-column cells are quant / count gaps, every other cell a value gap)."""
    from collections import Counter
    need = Counter(norm_elem(e) for e in sig) if sig else None
    if need is not None:
        n_gaps = sum(need.values())
        if need.get("gap:closure@list"):
            if target == "settled":
                raise Skip("closure signature on a settled row")
        if need.get("gap:query@table") and qtype == "member":
            raise Skip("membership query with query-column gaps")
    for _ in range(80):
        T = draw_table(rng, card, n_rec)
        Q = draw_query(rng, card, T, form, force_member, vtarget=vtarget, qtype=qtype, want=want)
        if need is not None and form != "c_rec" and Q["t"] == "member" and need.get("gap:query@table"):
            continue
        if Q["t"] == "member":
            if force_member:
                Q["neg"] = False
            ids = [r["id"] for r in T["records"]]
            who = f"{card['prefix']}-{rng.randint(1000, 9999)}"
            if who in ids:
                continue
            members = _ids(rng, card["prefix"], rng.randint(2, 4))
            listed = rng.random() < 0.5 if target == "settled" else False
            if listed:
                members[0] = who
            closed = card["world"] in ("closed", "local")
            if target == "open" and closed:
                continue
            if target == "settled" and not listed and not closed:
                continue
            Q["who"] = who
            if not force_member and not vtarget:
                Q["neg"] = rng.random() < 0.3
            T["list"] = {"name": card["list_name"], "members": members, "closed": closed}
        if not _filter_ok(T, Q):
            continue
        if form != "c_rec" and Q["t"] != "member" and not tune_threshold(rng, card, T, Q, target, want):
            continue
        cells = [(r["id"], c["id"]) for r in T["records"] for c in card["cols"]]
        rng.shuffle(cells)
        cells = cells[:60]
        marked = []
        dec = None
        if target == "open" and Q["t"] != "member":
            for rid, cid in cells:
                if need is not None and not need.get(norm_elem(cell_elem(T, Q, cid))):
                    continue
                T2 = A._fill_table(T, rid, cid, None)
                if not _filter_ok(T2, Q):
                    continue
                if not _settled(T2, Q):
                    d = A.table_decisive(T2, Q)
                    if d == [(rid, cid)]:
                        T, dec = T2, (rid, cid)
                        marked.append((rid, cid))
                        break
            if dec is None:
                continue
        elif target == "settled" and not _settled(T, Q):
            continue
        if target == "open" and Q["t"] == "member":
            dec = ("list", Q["who"])
        for rid, cid in cells:
            if len(marked) + (1 if Q["t"] == "member" and target == "open" else 0) >= n_gaps:
                break
            if (rid, cid) in marked:
                continue
            if need is not None:
                left = need - Counter(s3_elems_n(T, Q))
                if not left.get(norm_elem(cell_elem(T, Q, cid))):
                    continue
            T2 = A._fill_table(T, rid, cid, None)
            if not _filter_ok(T2, Q):
                continue
            if target == "settled":
                if not _settled(T2, Q):
                    continue
            else:
                if _settled(T2, Q) or A.table_decisive(T2, Q) != [dec]:
                    continue
            T = T2
            marked.append((rid, cid))
        ng = len(marked) + (1 if Q["t"] == "member" and target == "open" else 0)
        if ng != n_gaps:
            continue
        if need is not None and Counter(s3_elems_n(T, Q)) != need:
            continue
        return T, Q, dec
    raise Skip(f"no table for {target}")


# ---------------------------------------------------------------- units

def _claim_T(T, Q):
    v = A.table_claim(T, Q)
    return {True, False} if v is A.U else {v}


def build_unit(card: dict, spec: dict, uid: str) -> list[dict]:
    rng = rng_for("s3unit", uid)
    form = spec["form"]
    last = None
    for attempt in range(25):
        try:
            if form == "c_rec":
                return _crec(rng, card, spec, uid)
            return _yn(rng, card, spec, uid)
        except (Skip, ValueError) as e:
            last = e
    raise Skip(f"S3 unit {uid}: {last}")


# Repair r1 (G7 'does at' / quantifier words; F6-QC-2): with an unknown cell in the queried column, 'at least one' can
# only be settled true, and 'every' / 'no' only settled false. The query type is therefore drawn from this table by
# (form, wanted truth value), so that each type's share is the same among Yes and No rows of every form (Q-DET: the
# settled and the open rows show one type mix; Q-EST: Yes = true, No = half refuted and half open; Q-PLAIN: count
# queries, which take either value). Membership queries keep their own feasibility rule (draw_query).
TYPE_TABLE = {
    ("qdet", "true"): (("exists", 0.5), ("count", 0.5)),
    ("qdet", "false"): (("forall", 0.25), ("none", 0.25), ("count", 0.5)),
    ("qdet", "open"): (("exists", 0.25), ("forall", 0.125), ("none", 0.125), ("count", 0.5)),
    ("qest", "true"): (("exists", 0.5), ("count", 0.5)),
    ("qest", "false"): (("count", 1.0),),
    ("qest", "open"): (("exists", 1.0),),
    ("qplain", "true"): (("count", 1.0),),
    ("qplain", "false"): (("count", 1.0),),
}


def plan_qtype(card, spec):
    r = rng_for("s3qtype", spec["sid"])
    form, want = spec["form"], spec["want"]
    qgap = any(e in ("gap:quant@table", "gap:count@table") for e in (spec.get("sig") or []))
    vt = "bad" if unit("valence", spec["sid"]) < 0.5 else "good"
    member_ok = card["world"] != "open" or want == "open" or (want == "true" and card.get("list_pol") == vt)
    if card["member"] and form == "qdet" and want in ("true", "open") and member_ok and spec.get("twin") != "premise" \
            and not qgap and r.random() < 0.2:
        return "member"
    if card["member"] and card["world"] != "open" and form == "qplain" and not qgap and r.random() < 0.3:
        return "member"
    opts = TYPE_TABLE[(form, want)]
    return r.choices([t for t, _ in opts], weights=[w for _, w in opts])[0]


def _yn(rng, card, spec, uid):
    form, want = spec["form"], spec["want"]
    target = "open" if want == "open" else "settled"
    vt = None if spec.get("twin") == "triple" else ("bad" if unit("valence", spec["sid"]) < 0.5 else "good")
    qt = None if spec.get("twin") == "triple" else plan_qtype(card, spec)
    T, Q, dec = build_table_record(rng, card, form, target, spec["n_gaps"], rng.randint(5, 12), want=want,
                                   force_member=spec.get("twin") == "triple", sig=spec.get("sig"), vtarget=vt,
                                   qtype=qt)
    Tset = _claim_T(T, Q)
    if want in ("true", "false") and not (form == "qdet" and spec.get("twin") == "triple" and len(Tset) == 1):
        if Tset != {want == "true"}:
            raise Skip("claim value")
    if form == "qplain" and len(Tset) != 1:
        raise Skip("qplain open")
    from .s_rules import gold_for
    rec = {"T": T, "Q": Q, "form": form, "frame": spec["frame"], "spec": spec, "uid": uid, "Tset": Tset,
           "dec": dec, "depth": 2 if Q.get("filter") else 1}
    rec["gold"] = gold_for(form, spec["frame"], Tset, set(), None)
    if rec["gold"] != spec["label"]:
        raise Skip("label")
    rows = [rec]
    if spec.get("twin") == "premise" and len(Tset) == 2:
        rows = premise_set(_premise, rng, card, rec)
    elif spec.get("twin") == "triple":
        rows = _triple(rec)
    elif spec.get("twin") == "attack":
        from .lex import ATTACK_LINES
        rows = [rec, {**rec, "attack": rng.choice(ATTACK_LINES), "twin_kind": "attack", "rel": "inv"}]
    return rows


from .common import premise_set  # noqa: E402  (repair r1 v3c)


def _premise(rng, card, rec):
    """T1 twin (repair r1): the decisive cell filled and one more cell of the same kind (same column role) marked,
    so both arms carry one gap signature (s2 trap arm, s6 'Gaps'); C-REC twins keep the displayed options."""
    from collections import Counter
    T, Q, dec = rec["T"], rec["Q"], rec["dec"]
    sp = rec["spec"]
    if dec is None or dec[0] == "list":
        raise Skip("premise twin on a membership row")
    rid, cid = dec
    sig0 = Counter(s3_elems(T, Q))
    from .s_rules import gold_for
    want_lab = sp.get("twin_label", 1 - rec["gold"]) if rec["form"] != "c_rec" else None
    tw_want = sp.get("twin_want")
    vals = A.table_regions(T, cid, Q)
    rng.shuffle(vals)
    el = cell_elem(T, Q, cid)
    for v in vals:
        T2 = A._fill_table(T, rid, cid, v)
        cells = [(r["id"], c["id"]) for r in T2["records"] for c in T2["cols"]
                 if r["cells"][c["id"]] is not None and (r["id"], c["id"]) != (rid, cid) and cell_elem(T2, Q, c["id"]) == el]
        rng.shuffle(cells)
        for r2, c2 in cells[:40]:
            T3 = A._fill_table(T2, r2, c2, None)
            if Counter(s3_elems(T3, Q)) != sig0 or not _filter_ok(T3, Q):
                continue
            if rec["form"] == "c_rec":
                P3 = A.table_argset(T3, Q)
                if len(P3) == 1 and next(iter(P3)) in rec["L"]:
                    return [{**rec, "T": T3, "P": P3}, rec]
                continue
            T3set = _claim_T(T3, Q)
            if len(T3set) != 1:
                continue
            if tw_want in ("true", "false") and T3set != {tw_want == "true"}:
                continue
            g3 = gold_for(rec["form"], rec["frame"], T3set, set(), None)
            if g3 == want_lab:
                return [{**rec, "T": T3, "Tset": T3set, "gold": g3}, rec]
    raise Skip("premise twin")


def _triple(rec):
    Q = rec["Q"]
    if rec["form"] != "qdet" or rec["frame"] != "qdet" or Q["t"] != "member" or Q.get("neg"):
        raise Skip("triple base")
    c = {**rec, "frame": "qdet_leave", "gold": 1 - rec["gold"], "rel": "complement"}
    Qn = {**Q, "neg": True}
    Tn = _claim_T(rec["T"], Qn)
    e = {**rec, "frame": "qdet_dneg", "Q": Qn, "Tset": Tn, "gold": 1 if len(Tn) == 1 else 0, "rel": "equiv"}
    if e["gold"] != rec["gold"]:
        raise Skip("dneg label")
    return [rec, c, e]


def _crec(rng, card, spec, uid):
    k = spec["k"]
    n_conc = k - spec["nei"] - spec["none"]
    gcls = spec["gold"]
    target = "settled" if gcls == "concrete" else ("open" if gcls == "nei" else spec.get("role", "settled"))
    n_rec = max(10, n_conc + (rng.randint(0, 3) if k < 30 else 0))
    T, Q, dec = build_table_record(rng, card, "c_rec", target, spec["n_gaps"], n_rec, sig=spec.get("sig"))
    P = A.table_argset(T, Q)
    ids = [r["id"] for r in T["records"]]
    if gcls == "concrete":
        o = next(iter(P))
        L = [o] + rng.sample([i for i in ids if i != o], n_conc - 1)
    elif gcls == "nei":
        if len(P) < 2:
            raise Skip("nei")
        p = rng.choice(sorted(P))
        L = [p] + rng.sample([i for i in ids if i != p], n_conc - 1)
    else:
        rest = [i for i in ids if i not in P]
        if len(rest) < n_conc:
            raise Skip("none")
        L = rng.sample(rest, n_conc)
    rec = {"T": T, "Q": Q, "form": "c_rec", "spec": spec, "uid": uid, "P": P, "L": L, "dec": dec,
           "depth": 2 if Q.get("filter") else 1}
    rows = [rec]
    if spec.get("twin") == "premise" and len(P) >= 2:
        rows = premise_set(_premise, rng, card, rec)
    elif spec.get("twin") == "attack":
        from .lex import ATTACK_LINES
        rows = [rec, {**rec, "attack": rng.choice(ATTACK_LINES), "twin_kind": "attack", "rel": "inv"}]
    return rows


# ---------------------------------------------------------------- rendering

def col_header(c: dict) -> str:
    return f"{RF.cap(c['name'])} ({c['unit']})" if c["kind"] == "num" else RF.cap(c["name"])


def cond_text(T, cond, cmpw) -> str:
    c = next(x for x in T["cols"] if x["id"] == cond["col"])
    if c["kind"] == "num":
        return f"a {c['name']} of {cmpw[cond['op']]} {cond['n']} {c['unit']}"
    return f"a {c['name']} of {cond['v']}"


def claim_text(card, T, Q, cmpw, inversion: bool) -> tuple[str, str | None]:
    """(S, inversion question or None)."""
    noun, plural = card["noun"], card["plural"]
    t = Q["t"]
    if t == "member":
        L = T["list"]["name"]
        if Q.get("neg"):
            return f"{Q['who']} is not on the {L}", None
        return f"{Q['who']} is on the {L}", f"Is {Q['who']} on the {L}?"
    f = Q.get("filter")
    fc = next(x for x in T["cols"] if x["id"] == f["col"]) if f else None
    whose = f" whose {fc['name']} is {f['v']}" if f else ""
    cond = cond_text(T, Q["cond"], cmpw)
    if t == "exists":
        return (f"at least one {noun} in the register{whose} has {cond}",
                f"Does at least one {noun} in the register{whose} have {cond}?")
    if t == "forall":
        return (f"every {noun} in the register{whose} has {cond}",
                f"Does every {noun} in the register{whose} have {cond}?")
    if t == "none":
        return f"no {noun} in the register{whose} has {cond}", None
    w = cmpw[Q["cmp"]]
    return (f"{w} {Q['N']} {plural} in the register{whose} have {cond}",
            f"Do {w} {Q['N']} {plural} in the register{whose} have {cond}?")


def reading_lines(card, T, Q, form, ds="name") -> list[str]:
    D = RF.fmt_date(T["D"], ds)
    L = []
    w = card["world"]
    V = {"world": w, "event_names": [], "has_lists": bool(card["member"])}
    if w == "local":
        V["local_section"] = RF.cap(card["list_name"])
        V["local_thing"] = card["noun"]
    if card["member"] or w != "open":
        L += M.world_lines(V, T["D"], ds)
    else:
        L.append(sw("r1"))
    if card["cls"] == "json":
        L.append(sw("r42_json", table="register", entity=card["noun"]))
    else:
        if card["blank"]:
            L.append(sw("r4_blank", m1=card["marker"]))
        else:
            clause = ", even where this record is complete" if w != "open" else ""
            L.append(sw("r4_1", m1=card["marker"], clause=clause))
        L.append(sw("r42", table="register", entity=card["noun"], m1=card["marker"],
                    blank=" or left blank" if card["blank"] else ""))
    L.append(sw("r30"))
    L.append(sw("r32"))
    L.append(sw("r18", D=D))
    for c in card["cols"]:
        if c["kind"] == "num":
            L.append(sw("r20_qdom", q=c["name"], unit=c["unit"], lo=c["lo"], hi=c["hi"]))
        else:
            L.append(sw("r43", attr=c["name"], vals=RF.join_or_vals(c["vals"])))
    L.append(sw("r11") if card["cmp_family"] == "incl" else sw("r12"))
    if form == "yn":
        qk = card.get("qkinds") or ["exists", "forall", "none"]
        L += [sw(k) for t, k in (("forall", "r28_every"), ("exists", "r28_one"), ("none", "r28_no")) if t in qk]
        if card.get("filters", True):
            L.append(sw("r28_filter"))
        L += [sw(FRAME_SWITCH[f]) for f in card["frames"]]
    else:
        L.append(sw("r23", key=f"{next(c for c in card['cols'] if c['id'] == card['rec_key'])['name']}"))
        if card["filtered_rec"]:
            L.append(sw("r42_filter"))
        V2 = {"nei": card["nei"], "none": card["none"]}
        L += M.abstain_lines(V2)
    return L


def table_doc(card, T, style) -> dict:
    cols = T["cols"]
    head = [f"{RF.cap(card['noun'])} ID"] + [col_header(c) for c in cols]
    rows = []
    for r in T["records"]:
        row = [r["id"]]
        for c in cols:
            v = r["cells"][c["id"]]
            if v is None:
                row.append(None if card["cls"] == "json" else (BLANK if card["blank"] else card["marker"]))
            else:
                row.append(str(v) if c["kind"] == "num" else v)
        rows.append(row)
    blocks = [{"type": "table", "caption": None, "columns": head, "rows": rows}]
    if T.get("list"):
        blocks.append({"type": "fields", "pairs": [[RF.cap(T["list"]["name"]), ", ".join(T["list"]["members"])]]})
    doc = {"blocks": blocks}
    if style["container"] in ("markdown_table", "html_snippet"):
        doc["title"] = f"{RF.cap(card['plural'])} register"
    return doc


def emit(card: dict, rec: dict, ids: dict) -> tuple[dict, dict]:
    T, Q, form = rec["T"], rec["Q"], rec["form"]
    from .emit import pick_wording, switch_keys
    sts = card["styles"]
    if rec.get("attack"):
        sts = [x for x in sts if x["container"] not in ST.NO_PARA]
        if not sts:
            raise ValueError("no paragraph-capable style for the attack line")
    style = fpool.pick(sts, "F6", card["card_id"], rec["uid"], rec.get("ridx", 0))
    wd = pick_wording(card, rec)
    rng = rng_for("s3emit", rec["uid"], rec.get("ridx", 0))
    cmpw = {op: rng.choice(ws) for op, ws in CMP_S3.items()}
    H = M.headings(style)
    yn = form in ("qdet", "qest", "qplain")
    reading = reading_lines(card, T, Q, "yn" if yn else "c_rec")
    card_ir = {"blocks": [M.reading_section(H["reading"], reading)] + M.example_blocks(card, H)}
    doc = table_doc(card, T, style)
    if rec.get("attack"):
        doc["blocks"].append({"type": "para", "text": rec["attack"]})
    if yn:
        S, inv = claim_text(card, T, Q, cmpw, True)
        frame = rec["frame"]
        if form == "qplain" and inv and unit("inv3", rec["uid"]) < 0.5:
            question = inv
            frame_id = "qplain_inv"
        else:
            question = FRAMES[frame].format(S=S)
            frame_id = frame
        qtype, options, gold = "noul", None, rec["gold"]
        gcls = "yes" if gold == 1 else "no"
    else:
        key = next(c for c in T["cols"] if c["id"] == Q["key"])
        f = Q.get("filter")
        if f:
            fc = next(c for c in T["cols"] if c["id"] == f["col"])
            question = FRAMES["c_rec_fhi" if Q["t"] == "argmax" else "c_rec_flo"].format(
                col=fc["name"], val=f["v"], key=key["name"])
        else:
            question = FRAMES["c_rec_hi" if Q["t"] == "argmax" else "c_rec_lo"].format(key=key["name"])
        frame_id = "c_rec"
        options = list(rec["L"])
        sp = rec["spec"]
        if sp["nei"]:
            options.append(card["nei"])
        if sp["none"]:
            options.append(card["none"])
        rng.shuffle(options)
        P = rec["P"]
        inter = [o for o in rec["L"] if o in P]
        if len(P) == 1 and inter:
            gold, gcls = inter[0], "concrete"
        elif not inter and sp["none"]:
            gold, gcls = card["none"], "none"
        elif len(P) >= 2 and inter and sp["nei"]:
            gold, gcls = card["nei"], "nei"
        else:
            raise ValueError("C-REC gold not displayed")
        qtype = "choice"
    fields, res = M.render(style, doc, question, qtype, gold, card_ir, options, wd["text"], ids["id"],
                           allow_null=card["cls"] == "json")
    marked = A.table_marked(T)
    kinds = []
    for rid, cid in marked:
        if Q["t"] in ("exists", "forall", "none") and Q["cond"]["col"] == cid:
            kinds.append("gap:quant")
        elif Q["t"] == "count" and Q["cond"]["col"] == cid:
            kinds.append("gap:count")
        else:
            kinds.append("gap:value")
    if Q["t"] == "member" and Q["who"] not in T["list"]["members"] and not T["list"]["closed"]:
        kinds.append("gap:closure")
    world = card["world"]
    edge = sorted(set(kinds)) + [f"world:{world}"]
    sym = {"T": {k: v for k, v in T.items() if k != "cols"}, "cols": [[c["kind"], c.get("lo"), c.get("hi"),
           len(c.get("vals", []))] for c in T["cols"]], "Q": Q, "form": form, "frame": rec.get("frame"),
           "L": rec.get("L")}
    meta = M.make_meta(card_id=card["card_id"], pack=card["pack"]["pid"], sampler="S3", seed=ids["seed"],
                       structure_hash=M.structure_hash(sym), depth=ids["depth"], deep=ids["deep"],
                       format_style=style["id"], wording_id=wd["id"], defs_style=card["defs_style"],
                       twin_of=ids.get("twin_of"), twin_kind=ids.get("twin_kind"), edge=edge,
                       persona_seed=card["pack"].get("persona_seed"),
                       subtype={"qdet": "q_det", "qest": "q_est", "qplain": "q_plain"}.get(form, form),
                       git_sha=ids["git_sha"])
    row = M.make_row(rid=ids["id"], group_id=ids["group_id"], call_id=ids["call_id"], fields=fields, qtype=qtype,
                     options=options if qtype == "choice" else None, gold=gold, role=ids.get("role", "train"),
                     meta=meta)
    side = {"id": ids["id"], "kind": "table", "form": form, "gold_class": gcls,
            "p_set": sorted(rec["P"]) if rec.get("P") else None,
            "t_set": sorted(rec["Tset"]) if rec.get("Tset") else None, "n_gaps": len(kinds), "gap_kinds": kinds,
            "gap_positions": ["table"] * len(marked) + (["list"] if "gap:closure" in kinds else []),
            "frame_id": frame_id, "card_variant": world, "label_form": "plain",
            "k": len(options) if options else 2,
            "loader": {"gold_letter": res["gold_letter"], "prompt_sha256": res["prompt_sha256"]},
            "attack": bool(rec.get("attack")), "valence": s3_valence(card, Q) if yn else None,
            "struct": {"T": copy.deepcopy(T), "Q": Q, "L": rec.get("L")},
            "wording_text": wd["text"], "style": style["id"], "frames_card": card["frames"], "cmpw": cmpw,
            "switches_stated": switch_keys(reading), "decisive_gap": list(rec["dec"]) if rec.get("dec") else None}
    return row, side


# ---------------------------------------------------------------- G3 for tables

def g3(row: dict, side: dict, wordings: set) -> list[str]:
    from . import parse_f6 as PF, solver_b as B
    try:
        S = PF.parse_table_row(row, wordings)
    except PF.ParseError as e:
        return [f"parse: {e}"]
    probs = []
    st = side["struct"]
    gT = st["T"]
    want = canon_table(gT, st["Q"])
    got = canon_table(S["T"], S["Q"])
    if want != got:
        import json
        a, b = json.loads(want), json.loads(got)
        probs.append(f"structure differs: {[k for k in a if a[k] != b.get(k)]}")
    try:
        vals = B.table_values(S["T"], S["Q"])
    except B.Dropped as e:
        return probs + [f"solver B drop: {e}"]
    form = S["form"]
    if form == "c_rec":
        L = S["concrete"]
        inter = [o for o in L if o in vals]
        if len(vals) == 1 and inter:
            lb = inter[0]
        elif not inter and "none" in S["abstain"]:
            lb = S["abstain"]["none"]
        elif len(vals) >= 2 and inter and "nei" in S["abstain"]:
            lb = S["abstain"]["nei"]
        else:
            lb = None
    else:
        fr = S["frame"]
        if form == "qdet":
            settled = len(vals) == 1
            lb = (0 if settled else 1) if fr in ("qdet_leave", "qdet_imp") else (1 if settled else 0)
        elif form == "qest":
            lb = 1 if vals == {True} else 0
        else:
            lb = (1 if vals == {True} else 0) if len(vals) == 1 else None
    if lb != row["gold"]:
        probs.append(f"solver B label {lb!r} != gold {row['gold']!r}")
    want_set = side.get("p_set") if form == "c_rec" else side.get("t_set")
    if want_set is not None and sorted(vals) != sorted(want_set):
        probs.append("G2: solver A set != solver B set")
    return probs


def canon_table(T: dict, Q: dict) -> str:
    import json
    cols = sorted([c["name"].lower(), c["kind"], c.get("unit"), c.get("lo"), c.get("hi"), c.get("vals")]
                  for c in T["cols"])
    name = {c["id"]: c["name"].lower() for c in T["cols"]}
    recs = sorted([r["id"], sorted([name[k], v] for k, v in r["cells"].items())] for r in T["records"])
    q = dict(Q)
    for k in ("cond", "filter"):
        if q.get(k):
            q[k] = {**q[k], "col": name[q[k]["col"]]}
    if q.get("key"):
        q["key"] = name[q["key"]]
    lst = T.get("list")
    lst = None if not lst else [lst["name"].lower(), sorted(lst["members"]), lst["closed"]]
    return json.dumps({"cols": cols, "recs": recs, "q": q, "list": lst, "D": T["D"], "world": T["world"]},
                      sort_keys=True, default=str)
