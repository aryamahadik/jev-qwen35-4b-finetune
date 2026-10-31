"""F9 samplers (section 3): draw a Struct and a query for one frame of a card.

  S1 forward single-table query (structure first, then a query from the data);
  S2 label-first boundary tables (target label and query first; literals placed at / one step from / farther from a
     decisive record's value; near-miss records planted);
  S3 two-table join (relational first); S4 nested JSON / YAML record arrays (document first);
  S6 log lines and event streams (stream first); S5 held-out wide pivot report (mix-tuning dev only).
Every gold comes from solver A recomputing from the Struct; the sampler only steers draws (accept / reject).
"""
from __future__ import annotations

import datetime as dt
import random
from fractions import Fraction

from f9ast import atoms
from f9fmt import epoch_of_local, local_day, month_bounds
from f9lex import CMP_T10, id_key

BINS = {"S1": [(10, 20, .40), (21, 40, .35), (41, 60, .25)], "S2": [(10, 20, .40), (21, 35, .35), (36, 50, .25)],
        "S4": [(10, 30, .50), (31, 80, .38), (81, 200, .12)], "S6": [(15, 40, .50), (41, 70, .38), (71, 120, .12)],
        "S3": [(10, 25, .45), (26, 45, .35), (46, 60, .20)]}


class Retry(Exception):
    pass


def pick_bin(sampler, rng, force=None, weights=None):
    """weights: per-form bin weights (f9build.bin_weights) that keep the sampler's planned bin shares (1.8) while a
    choice row, which prints its card twice, is drawn only in a bin where it can fit its token cap."""
    bins = BINS[sampler]
    if force is not None:
        return bins[force]
    x = rng.random()
    acc = 0
    for b, w in zip(bins, weights or [b[2] for b in bins]):
        acc += w
        if x < acc:
            return b
    return bins[-1]


def ids(prefix, n, rng, width=4, lo=1, hi=9999):
    pool = rng.sample(range(lo, hi), n)
    return [f"{prefix}-{x:0{width}d}" for x in pool]


def unlisted_id(prefix, listed, rng, width=4):
    nums = sorted(id_key(x)[1] for x in listed)
    for _ in range(200):
        if rng.random() < 0.6 and len(nums) >= 2:  # inside the listed range on >= 50% of unlisted-ID rows (1.9)
            x = rng.randint(nums[0], nums[-1])
        else:
            x = rng.randint(1, 9998)
        s = f"{prefix}-{x:0{width}d}"
        if s not in listed:
            return s
    raise Retry("no unlisted id")


def rand_num(c, rng):
    k = int((c["hi"] - c["lo"]) / c["step"])
    return c["lo"] + c["step"] * rng.randint(0, k)


def norm_num(v, c):
    return v if c["dp"] else Fraction(int(v))


# ------------------------------------------------------------------------------------------------ dates
def card_base_day(card):
    r = random.Random(card["card_id"] + ":day")
    return dt.date(r.choice([2026, 2027, 2028, 2029]), r.randint(1, 6), 1).toordinal()


def rand_date(card, rng, span=170):
    return card_base_day(card) + rng.randint(0, span)


# ------------------------------------------------------------------------------------------------ main table
def main_cols(card, compact=False):
    sc = card["schema"]
    cols = [{"name": sc["idcol"], "type": "id"}]
    cols += [dict(c) for c in sc["cats"]]
    cols += [dict(c) for c in sc["nums"]]
    cols += [dict(c) for c in sc["dates"]]
    cols += [dict(c) for c in sc.get("bools", [])]
    if sc.get("text") and not compact:
        cols.append(dict(sc["text"]))
    if card["sampler"] == "S4" and not compact:
        cols += [dict(c) for c in sc["obj"]["fields"]]
        cols.append({"name": sc["list"]["name"], "type": "list", "sub": [dict(c) for c in sc["list"]["sub"]]})
    if compact:
        keep = [cols[0]] + [c for c in cols[1:] if c["type"] in ("cat", "num")][:3]
        cols = keep
    return cols


def note_text(card, rng):
    w = card["schema"]["words"]
    a = rng.choice(w)
    b = rng.choice(w)
    s = a if a == b or rng.random() < 0.4 else f"{a} near {b}"
    return s[:60]


def gen_value(card, c, rng):
    t = c["type"]
    if t == "cat":
        return rng.choice(c["values"])
    if t == "num":
        return norm_num(rand_num(c, rng), c)
    if t == "date":
        return rand_date(card, rng)
    if t == "bool":
        return rng.random() < 0.5
    if t == "text":
        return note_text(card, rng)
    if t == "list":
        n = rng.choice([0, 1, 2, 2, 3, 3, 4, 5])
        return [[gen_value(card, sc, rng) for sc in c["sub"]] for _ in range(n)]
    raise KeyError(t)


def keep_cols(card, lean=False):
    """Columns a row's table always keeps: the id, the tie-chain date column, T5 columns, the masked column, term
    columns, the S4 nested object and list."""
    from f9ast import term_cols
    sc = card["schema"]
    keep = {sc["idcol"]} | set(card.get("t5_cols") or [])
    for c, _ in (card["sem"].get("tie_chain") or []) if not lean else []:
        keep.add(c)
    if card.get("masked"):
        keep.add(card["masked"]["col"])
    for t in (card.get("terms") or {}).values():
        keep |= set(term_cols(t))
    if lean:  # S4 1.8 ladder step after 4 columns: id + one scalar + the nested object + the list (3.4: >= 3 fields)
        if sc.get("nums"):
            keep.add(sc["nums"][0]["name"])
        return keep
    if sc.get("cats"):
        keep.add(sc["cats"][0]["name"])
    if sc.get("nums"):
        keep.add(sc["nums"][0]["name"])
    return keep


def main_table(card, rng, n, compact=False, unk=True, max_cols=None, lean=False, keep_note=False):
    cols = main_cols(card, compact)
    if compact and max_cols:
        # 1.8 ladder in the compact bin: fewer columns, down to the id plus 2 scalar fields (3 fields in all), keeping
        # the columns a card rule reads (term, masked, T5)
        keep = keep_cols(card)
        scal = cols[1:]
        pref = [c for c in scal if c["name"] in keep]
        cols = [cols[0]] + (pref + [c for c in scal if c["name"] not in keep])[:max(2, len(pref))]
    if lean and not compact:
        max_cols = 2
    if max_cols and not compact:
        keep = keep_cols(card, lean=lean)
        if keep_note and card["schema"].get("text"):  # an attack unit's free-text cell (F9 attack twins)
            keep.add(card["schema"]["text"]["name"])
            max_cols += 1
        top = [c for c in cols if "." not in c["name"] and c["type"] != "list"]
        drop = [c["name"] for c in top if c["name"] not in keep]
        rng.shuffle(drop)
        extra = len(top) - max_cols
        gone = set(drop[:max(0, extra)])
        cols = [c for c in cols if c["name"] not in gone]
    sc = card["schema"]
    idl = ids(sc["prefix"], n, rng)
    rows = []
    for i in range(n):
        r = [idl[i]] + [gen_value(card, c, rng) if not (lean and c["type"] == "list") else
                        [[gen_value(card, sc_, rng) for sc_ in c["sub"]] for _ in range(rng.choice([0, 1, 1, 2]))]
                        for c in cols[1:]]
        rows.append(r)
    t = {"role": "main", "cols": cols, "rows": rows}
    if unk and card["sem"].get("missing") and rng.random() < 0.6:
        add_unknowns(card, t, rng)
    return t


def unk_eligible(card, t):
    miss = card["sem"].get("missing")
    out = []
    for j, c in enumerate(t["cols"]):
        if c["type"] in ("id", "list", "text") or c["name"] == card.get("fkcol"):
            continue
        if miss == "T5":
            if c["name"] not in (card.get("t5_cols") or []):
                continue
        elif c["type"] not in ("cat", "num", "date", "bool"):
            continue
        out.append(j)
    return out


def add_unknowns(card, t, rng, k=None):
    el = unk_eligible(card, t)
    if not el or not t["rows"]:
        return
    k = k if k is not None else (rng.choice([1, 1, 2]) if card["sem"].get("missing") == "T5" else
                                 rng.choice([1, 1, 2, 3]))
    for _ in range(k):
        i = rng.randrange(len(t["rows"]))
        j = rng.choice(el)
        t["rows"][i][j] = None


def col_index(t, name):
    for j, c in enumerate(t["cols"]):
        if c["name"] == name:
            return j
    raise KeyError(name)


def col_vals(t, name):
    j = col_index(t, name)
    return [r[j] for r in t["rows"] if r[j] is not None]


# ------------------------------------------------------------------------------------------------ predicates
def num_atom(card, c, vals, rng, phrases, placement=None, target=None):
    ph = rng.choice([p for p in phrases])
    op = CMP_T10[ph]
    if target is not None:
        base = target
    else:
        base = rng.choice(vals) if vals else rand_num(c, rng)
    x = Fraction(base)
    step = c["step"]
    pl = placement or rng.choice(["at", "step", "far"])
    if pl == "step":
        x += step * rng.choice([-1, 1])
    elif pl == "far":
        span = max(2 * step, (c["hi"] - c["lo"]) / 5)
        d = step * rng.randint(2, max(2, int(span / step)))
        x += d * rng.choice([-1, 1])
    x = min(max(x, c["lo"] + step), c["hi"])
    if x <= 0:
        x = step
    from f9fmt import dec_str
    lit = dec_str(x) if c["dp"] else str(int(x))
    return {"k": "cmp", "col": c["name"], "op": op, "lit": lit, "unit": c["unit"], "_ph": ph, "_pl": pl}


def between_atom(card, c, vals, rng):
    a = rng.choice(vals) if vals else rand_num(c, rng)
    w = c["step"] * rng.randint(2, max(2, int((c["hi"] - c["lo"]) / c["step"] / 4)))
    lo = max(c["lo"] + c["step"], Fraction(a) - w / 2)
    lo = c["lo"] + c["step"] * int((lo - c["lo"]) / c["step"])
    hi = lo + w
    if lo <= 0:
        lo = c["step"]
    from f9fmt import dec_str
    f = (lambda v: dec_str(v) if c["dp"] else str(int(v)))
    return {"k": "between", "col": c["name"], "lo": f(lo), "hi": f(hi), "unit": c["unit"]}


def cat_atom(card, c, vals, rng, kind):
    present = list(dict.fromkeys(vals)) or c["values"]
    if kind == "eq":
        v = rng.choice(present if rng.random() < 0.85 else c["values"])
        return {"k": "cmp", "col": c["name"], "op": "=", "lit": v}
    if kind == "in2":
        a, b = rng.sample(c["values"], 2)
        return {"k": "in", "col": c["name"], "vals": [a, b]}
    if kind == "not":
        return {"k": "not", "arg": {"k": "cmp", "col": c["name"], "op": "=", "lit": rng.choice(present)}}
    if kind == "neither":
        a, b = rng.sample(c["values"], 2)
        return {"k": "not", "arg": {"k": "in", "col": c["name"], "vals": [a, b]}}
    raise KeyError(kind)


def date_atom(card, c, vals, rng, forms):
    f = rng.choice(forms)
    D = rng.choice(vals) if vals and rng.random() < 0.8 else rand_date(card, rng)
    a = {"k": "win", "col": c["name"], "_form": f, "unit": "day", "step": 1}
    if f == "from_to":
        d2 = D + rng.randint(3, 40)
        a.update(lo=D if rng.random() < 0.5 else D - rng.randint(0, 3), hi=d2, li=True, hi_i=True)
    elif f == "before":
        a.update(lo=None, hi=D, li=True, hi_i=False)
    elif f == "after":
        a.update(lo=D, hi=None, li=False, hi_i=True)
    elif f == "on_or_before":
        a.update(lo=None, hi=D, li=True, hi_i=True)
    elif f == "on_or_after":
        a.update(lo=D, hi=None, li=True, hi_i=True)
    elif f == "on":
        a.update(lo=D, hi=D, li=True, hi_i=True)
    elif f == "in_month":
        d = dt.date.fromordinal(D)
        lo, hi = month_bounds(d.year, d.month)
        a.update(lo=lo, hi=hi, li=True, hi_i=True)
    elif f == "rolling":
        N = rng.choice([7, 10, 14, 30])
        a.update(lo=D - N + 1, hi=D, li=True, hi_i=True, _N=N)
    return a


def draw_atom(card, t, rng, col, kinds, role="main", placement=None, target=None, phrases=None):
    c = t["cols"][col_index(t, col)] if t else None
    vals = col_vals(t, col) if t else []
    typ = c["type"]
    if typ == "num":
        if card.get("use_between") and "between" in kinds and rng.random() < 0.25:
            return between_atom(card, c, vals, rng)
        return num_atom(card, c, vals, rng, phrases or card["cmp_amount"], placement, target)
    if typ == "cat":
        opts = ["eq"]
        if card.get("use_in2") and "in2" in kinds:
            opts.append("in2")
        if card.get("use_not") and "not" in kinds:
            opts += ["not", "neither"] if card.get("use_in2") else ["not"]
        return cat_atom(card, c, vals, rng, rng.choice(opts))
    if typ == "date":
        return date_atom(card, c, vals, rng, card["time_forms"])
    if typ == "text":
        v = rng.choice(vals) if vals else "yard"
        ws = v.split()
        s = rng.choice(ws)
        return {"k": "contains", "col": c["name"], "s": s}
    raise Retry(f"no atom for {typ}")


def filter_cols(card, t, s4_nested=True):
    out = []
    for c in t["cols"]:
        if c["type"] == "date" and not card.get("time_forms"):
            continue
        if c["type"] in ("cat", "num", "date"):
            if "." in c["name"] and not s4_nested:
                continue
            out.append(c["name"])
        if c["type"] == "text" and card["sampler"] == "S4":
            out.append(c["name"])
    return out


def draw_pred(card, t, rng, n_atoms=None, allow_neg=True, placement=None, exclude=()):
    cols = [c for c in filter_cols(card, t) if c not in exclude]
    n = n_atoms or (1 if rng.random() < 0.55 else 2)
    if len(cols) < n:
        n = len(cols)
    chosen = rng.sample(cols, n)
    aa = []
    for i, cn in enumerate(chosen):
        kinds = ["eq", "in2", "between"] + (["not"] if allow_neg and i == n - 1 else [])
        aa.append(draw_atom(card, t, rng, cn, kinds, placement=placement))
    # negated parts come after non-negated AND operands (1.2)
    aa.sort(key=lambda a: a["k"] == "not")
    if sum(1 for a in aa if a["k"] == "not") > 1:
        raise Retry("two negated parts")
    return aa[0] if len(aa) == 1 else {"k": "and", "args": aa}


# ------------------------------------------------------------------------------------------------ S3 tables
def s3_tables(card, rng, n_ev):
    sc = card["schema"]
    n_ent = rng.randint(5, 25)
    keys = ids(sc["ent_prefix"], n_ent, rng)
    dcols = [{"name": sc["key"], "type": "id"}] + [dict(c) for c in sc["dim_cats"]] + [dict(c) for c in sc["dim_nums"]]
    drows = [[k] + [gen_value(card, c, rng) for c in dcols[1:]] for k in keys]
    fcols = [{"name": sc["key"], "type": "fk"}] + [dict(c) for c in sc["fact_cats"]] + \
        [dict(c) for c in sc["fact_nums"]] + [dict(c) for c in sc["fact_dates"]]
    if sc.get("text"):
        fcols.append(dict(sc["text"]))
    zero = set(rng.sample(keys, min(len(keys) - 1, rng.choice([0, 0, 1, 2, 3]))))
    live = [k for k in keys if k not in zero]
    orphans = [unlisted_id(sc["ent_prefix"], keys, rng) for _ in range(rng.choice([0, 0, 1, 2, 3]))]
    frows, seen = [], set()
    for _ in range(n_ev):
        k = rng.choice(orphans) if orphans and rng.random() < 0.06 else rng.choice(live)
        r = [k] + [gen_value(card, c, rng) for c in fcols[1:]]
        key = repr(r)
        if key in seen:
            continue
        seen.add(key)
        frows.append(r)
    dim = {"role": "dim", "cols": dcols, "rows": drows}
    fact = {"role": "fact", "cols": fcols, "rows": frows}
    if card["sem"].get("missing") and rng.random() < 0.6:
        add_unknowns(card, fact if rng.random() < 0.6 else dim, rng, k=rng.choice([1, 2]))
    return dim, fact, orphans


# ------------------------------------------------------------------------------------------------ S6 log
def s6_table(card, rng, n):
    sc = card["schema"]
    lv = sc["levels"]
    # repair r1: a card with a component pick draws 4-8 components, so the pick can show 5-9 options (named errors
    # and E0 components; section 5 S6 bucket plan), other cards 2-6
    ncomp = rng.randint(4, 8) if "C_COMP" in (card.get("menu") or {}) else rng.randint(2, 6)
    pre = card["schema"].get("comp_prefix") or "".join(w[0] for w in card["org"].split()[:2]).upper()[:2]
    if len(pre) < 2:
        pre = "CX"
    comps = sorted({f"{pre}-{x:02d}" for x in rng.sample(range(1, 40), ncomp)}, key=id_key)
    nreq = rng.randint(5, 30)
    reqs = [f"RQ-{x:04d}" for x in rng.sample(range(1, 9999), nreq)]
    day0 = card_base_day(card) + rng.randint(0, 100)
    off = card["sem"]["zone"]
    t = epoch_of_local(day0, rng.randint(6, 10) * 3600, off)
    tf = card["sem"].get("tf") or "hm"
    unit = 60 if tf == "hm" else 1
    w = [0.25, 0.4, 0.22, 0.13]
    cols = [{"name": "time", "type": "dt"}, {"name": "level", "type": "lvl"}, {"name": "component", "type": "comp"},
            {"name": "request", "type": "req"}, {"name": sc["code"]["name"], "type": "cat",
                                                  "values": sc["code"]["values"]},
            {"name": sc["numf"]["name"], "type": "num", "unit": sc["numf"]["unit"], "dp": 0, "lo": sc["numf"]["lo"],
             "hi": sc["numf"]["hi"], "step": Fraction(1)}, {"name": "message", "type": "text"}]
    # request ids on 75% of lines on cards with request questions (T41), else 30% (shorter lines, 1.8)
    preq = 0.75 if {"Y_REQ", "C_REQ", "SET_REQ"} & set(card["menu"]) else 0.3
    rows = []
    for i in range(n):
        t += unit * rng.randint(1, 40) * (1 if unit == 60 else rng.randint(1, 60))
        level = rng.choices(lv, weights=w)[0]
        comp = rng.choice(comps)
        req = rng.choice(reqs) if rng.random() < preq else ""
        code = rng.choice(sc["code"]["values"]) if rng.random() < 0.6 else None
        num = Fraction(rng.randint(int(sc["numf"]["lo"]), int(sc["numf"]["hi"]))) if rng.random() < 0.5 else None
        msg = rng.choice(sc["words"]).lower()
        rows.append([t, level, comp, req, code, num, msg])
    if rng.random() < 0.3 and rows:  # identical repeated line (T32: each line is one event)
        j = rng.randrange(len(rows))
        rows.insert(j + 1, list(rows[j]))
    tb = {"role": "log", "cols": cols, "rows": rows, "comps": comps, "reqs": reqs}
    return tb


def s6_order(card, tb, rng):
    """Render order: time order, or merged-source order under the T32 merged variant (card-level)."""
    rows = tb["rows"]
    rows.sort(key=lambda r: r[0])
    if card["sem"].get("merged"):
        comps = tb["comps"]
        half = set(comps[: max(1, len(comps) // 2)])
        a = [r for r in rows if r[2] in half]
        b = [r for r in rows if r[2] not in half]
        out = []
        while a or b:
            take = rng.randint(1, 4)
            src = a if (rng.random() < 0.5 and a) or not b else b
            out += src[:take]
            del src[:take]
        tb["rows"] = out


# ------------------------------------------------------------------------------------------------ S5 pivot
def s5_pivot(card, rng):
    sc = card["schema"]
    ng = rng.randint(2, 3)
    ents = ids(sc["ent_prefix"], rng.randint(6, 11), rng)
    groups = []
    k = 0
    sizes = []
    rest = len(ents)
    for g in range(ng):
        s = rest if g == ng - 1 else rng.randint(2, max(2, rest - 2 * (ng - g - 1)))
        sizes.append(s)
        rest -= s
    for s in sizes:
        groups.append(ents[k:k + s])
        k += s
    periods = [f"Week {i}" for i in range(1, rng.randint(4, 6) + 1)]
    cells = {e: [rng.randint(0, 200) for _ in periods] for e in ents}
    marks = []
    for _ in range(rng.randint(2, 4)):
        marks.append([rng.choice(ents), rng.randrange(len(periods))])
    return {"entities": ents, "groups": groups, "periods": periods, "cells": cells, "marks": marks}
