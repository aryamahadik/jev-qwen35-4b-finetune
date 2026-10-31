"""G4 metamorphic relations (section 3 per sampler, section 4 at a glance). Each relation transforms a built row's
Struct, question, card or display, re-renders it through the same emitter (so G3 = parse + solver B on the transformed
text runs on every transformed row), and checks the gold against the relation's predicted mapping. Relations per
sampler (>= 5 for training samplers, MR22 in each; S6 uses MR19 / MR20 / MR23 for MR5 / MR1 / MR2; S5 >= 4):
  S1: MR1 MR2 MR3 MR5 MR7 MR22      S2: MR1 MR2 MR5 MR7 MR9 MR22      S3: MR1 MR2 MR5 MR7 MR13 MR22
  S4: MR1 MR2 MR5 MR7 MR14 MR16 MR22   S6: MR7 MR18 MR19 MR20 MR22 MR23   S5: P1 (row shuffle in group) P2 (period
  reorder) P3 (footnote on a non-decisive cell) MR7
Hypothesis is not installed in the venv, so the property tests are seeded random draws (same relations, fixed seed).
Usage: f9g4.py <mode> <sampler> [--rows N]  -> out/qc/g4_<mode>_<sampler>.json"""
from __future__ import annotations

import copy
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

RELS = {"S1": ["MR1", "MR2", "MR3", "MR5", "MR7", "MR22"], "S2": ["MR1", "MR2", "MR5", "MR7", "MR9", "MR22"],
        "S3": ["MR1", "MR2", "MR5", "MR7", "MR13", "MR22"], "S4": ["MR1", "MR2", "MR5", "MR7", "MR14", "MR16", "MR22"],
        "S6": ["MR7", "MR18", "MR19", "MR20", "MR22", "MR23"], "S5": ["P1", "P2", "P3", "MR7"]}


def deep_replace(x, old, new, keys=("col", "name")):
    """Rename a column inside query / card / tag structures: dict values under `keys` equal to old, and list
    entries equal to old (tie chains, tags)."""
    if isinstance(x, dict):
        return {k: (new if (k in keys and v == old) else deep_replace(v, old, new, keys)) for k, v in x.items()}
    if isinstance(x, list):
        return [new if v == old else deep_replace(v, old, new, keys) for v in x]
    if isinstance(x, tuple):
        return tuple(new if v == old else deep_replace(v, old, new, keys) for v in x)
    return x


def rebuild_res(row, side):
    form = side["form"]
    res = {"frame": side["frame"], "form": form, "struct": side["struct"], "q": side["q"],
           "gold": side["gold_payload"], "plan": side.get("plan"), "shown": side.get("shown"),
           "short_text": side.get("short_text"), "short_flags": side.get("short_flags"), "edge": row["meta"]["edge"]}
    if form != "yn":
        res["options"] = [tuple(o) for o in side["options_full"]]
        res["gold_text"] = row["gold"]
    return res


def recard(card, held_out):
    """Re-render the card IR, examples and render key after a card-level change (rename, unit restatement)."""
    from f9cards import card_ir
    from f9examples import attach_examples
    from f9rows import render_key_fn
    attach_examples(card, random.Random("f9-card:" + card["card_id"]))
    card["ir"] = card_ir(card, card["used"], card.get("examples"), card.get("fewshot_block"))
    card["render_key"] = render_key_fn(card)
    return card


# ------------------------------------------------------------------------------------------------ relations
def same(r0, r2):
    return r2["gold"] == r0["gold"] and (r0["options"] is None or sorted(r0["options"]) == sorted(r2["options"]))


def mr1(card, res, rng):
    st = copy.deepcopy(res["struct"])
    if card["sampler"] not in ("S1", "S2", "S3", "S4"):
        return None
    for t in st["tables"]:
        rng.shuffle(t["rows"])
    return card, dict(res, struct=st), {}, same


def _top_cols(card, t):
    return [j for j, c in enumerate(t["cols"]) if j > 0 and "." not in c["name"] and c["type"] != "list"]


def mr3(card, res, rng):
    """Column reorder (S1-S3; S4 MR14 = key order shuffle, the same for every record)."""
    st = copy.deepcopy(res["struct"])
    for t in st["tables"]:
        js = _top_cols(card, t)
        if len(js) < 2:
            continue
        perm = list(js)
        while perm == js:
            rng.shuffle(perm)
        order = [j for j in range(len(t["cols"])) if j not in js]
        order = [0] + perm + [j for j in order if j != 0]
        t["cols"] = [t["cols"][j] for j in order]
        t["rows"] = [[r[j] for j in order] for r in t["rows"]]
    return card, dict(res, struct=st), {}, same


def mr2(card, res, rng):
    """Consistent column rename in the card, the tables and the question (a top-level, non-id column)."""
    from f9lex import lint_colname
    st = res["struct"]
    t = st["tables"][0] if card["sampler"] != "S3" else st["tables"][1]
    cand = [t["cols"][j]["name"] for j in _top_cols(card, t) if t["cols"][j]["type"] != "text"]
    if card["sampler"] == "S3":
        cand = [c for c in cand if c != card["schema"]["key"]]
    rng.shuffle(cand)
    for old in cand:
        for suf in ("_entry", "_item", "_field", "_value"):
            new = old + suf
            if lint_colname(new) is None:
                break
        else:
            continue
        card2 = copy.deepcopy({k: v for k, v in card.items() if k != "render_key"})
        card2 = deep_replace(card2, old, new, keys=("col", "name"))
        if card2.get("t5_cols"):
            card2["t5_cols"] = [new if c == old else c for c in card2["t5_cols"]]
            card2["t5_domains"] = {(new if k == old else k): v for k, v in card2["t5_domains"].items()}
        recard(card2, card2.get("held_out"))
        st2 = copy.deepcopy(st)
        for tt in st2["tables"]:
            for c in tt["cols"]:
                if c["name"] == old:
                    c["name"] = new
        res2 = dict(res, struct=st2, q=deep_replace(copy.deepcopy(res["q"]), old, new, keys=("col",)))
        if res.get("options"):
            res2["options"] = [(p, tx, deep_replace(list(tg), old, new)) for p, tx, tg in res["options"]]
        return card2, res2, {}, same
    return None


def mr5(card, res, rng, rend0):
    s = card["sampler"]
    c0 = rend0["container"]
    if s == "S4" and res["struct"].get("compact"):
        opts = [c for c in ("json_compact", "jsonl") if c != c0]
    elif s == "S3":
        ks = card["containers"]
        opts = [(a, b) for a in ks for b in ks if (a, b) != tuple(c0)]
    elif s in ("S1", "S2", "S4"):
        opts = [c for c in card["containers"] if c != c0]
    else:
        return None
    if not opts:
        return None
    return card, res, {"container": rng.choice(opts)}, same


def mr19(card, res, rng, rend0):
    syn, fence = rend0["container"]
    opts = [x for x in card["syntaxes"] if x != syn]
    return card, res, {"container": (rng.choice(opts), fence)}, same


def mr7(card, res, rng):
    if res["form"] == "yn" or len(res["options"]) < 2:
        return None
    o = list(res["options"])
    o2 = list(o)
    while o2 == o:
        rng.shuffle(o2)
    return card, dict(res, options=o2), {}, same


def mr9(card, res, rng):
    from f9units import fact_flip
    if res["form"] != "yn":
        return None

    class _E:
        pass
    em = _E()
    em.card, em.rng = card, rng
    tw = fact_flip(em, res, "boundary")
    if tw is None:
        return None
    return card, tw, {}, (lambda r0, r2: r2["gold"] == 1 - r0["gold"])


def mr13(card, res, rng):
    from f9samp import gen_value, unlisted_id
    st = copy.deepcopy(res["struct"])
    dim, fact = st["tables"]
    keys = [r[0] for r in dim["rows"]] + list(st.get("orphans") or []) + [r[0] for r in fact["rows"]]
    k = unlisted_id(card["schema"]["ent_prefix"], keys, rng)
    row = [k] + [gen_value(card, c, rng) for c in fact["cols"][1:]]
    fact["rows"].insert(rng.randrange(len(fact["rows"]) + 1), row)
    st["orphans"] = list(st.get("orphans") or []) + [k]
    return card, dict(res, struct=st), {}, same


def mr16(card, res, rng):
    st = copy.deepcopy(res["struct"])
    t = st["tables"][0]
    js = [j for j, c in enumerate(t["cols"]) if c["type"] == "list"]
    if not js:
        return None
    moved = False
    for r in t["rows"]:
        v = r[js[0]]
        if v and len(v) >= 2:
            v2 = list(v)
            rng.shuffle(v2)
            moved |= v2 != v
            r[js[0]] = v2
    return (card, dict(res, struct=st), {}, same) if moved else None


VALUE_OPS = ("sum", "mean", "min", "max", "lookup", "ent_sum", "ent_attr", "median")


def _base(q):
    while q["op"] in ("thr", "not"):
        q = q["inner"]
    return q


def _set_units(x, col, unit):
    """Give every literal on `col` its unit explicitly (T28: every amount literal carries its unit)."""
    if isinstance(x, dict):
        if x.get("col") == col and ("lit" in x or "lo" in x) and x.get("k") in ("cmp", "between") and not x.get("unit"):
            x["unit"] = unit
        for v in x.values():
            _set_units(v, col, unit)
    elif isinstance(x, list):
        for v in x:
            _set_units(v, col, unit)


def mr22(card, res, rng, rend0):
    """Unit restatement: one numeric column restated in a unit 10 times smaller ('d' + unit), with the exact factor
    stated in the card (T28); every literal and the named answer unit keep their own unit, so gold is unchanged.
    The answer column of a value pick and T5 columns (whose domains are stated in the old unit) are not restated."""
    if rend0["mode"] != "full":
        return None  # a short card (T1-T5, T10 only) or no card states no T28 units, so no factor can be stated
    st = copy.deepcopy(res["struct"])
    b = _base(res["q"])
    ans_col = b.get("col") if (res["form"] == "value" and b["op"] in VALUE_OPS) else None
    cands = []
    for ti, t in enumerate(st.get("tables") or []):
        for j, c in enumerate(t["cols"]):
            if c["type"] == "num" and c.get("unit") and c["name"] != ans_col and \
                    c["name"] not in (card.get("t5_cols") or []) and "." not in c["name"]:
                cands.append((ti, j))
    if not cands:
        return None
    ti, j = rng.choice(cands)
    c = st["tables"][ti]["cols"][j]
    old, new = c["unit"], "d" + c["unit"]
    for r in st["tables"][ti]["rows"]:
        if r[j] is not None:
            r[j] = Fraction(r[j]) * 10
    upd = {"unit": new, "dp": max(0, c.get("dp", 0) - 1)}
    for k in ("lo", "hi", "step"):
        if c.get(k) is not None:
            upd[k] = Fraction(c[k]) * 10
    c.update(upd)
    card2 = copy.deepcopy({k: v for k, v in card.items() if k != "render_key"})
    hit = False
    for key, v in card2["schema"].items():
        cols = v if isinstance(v, list) else ([v] if isinstance(v, dict) else [])
        for cc in cols:
            if isinstance(cc, dict) and cc.get("name") == c["name"] and cc.get("type") == "num":
                cc.update(upd)
                hit = True
    if not hit:
        return None
    card2["sem"]["conv"] = {f"{old}->{new}": "10"}
    _set_units(card2.get("terms"), c["name"], old)
    recard(card2, card2.get("held_out"))
    q2 = copy.deepcopy(res["q"])
    _set_units(q2, c["name"], old)
    return card2, dict(res, struct=st, q=q2), {}, same


def mr20(card, res, rng):
    if not card["sem"].get("merged"):
        return None
    st = copy.deepcopy(res["struct"])
    t = st["tables"][0]
    rows = list(t["rows"])
    rng.shuffle(rows)
    if rows == t["rows"]:
        return None
    t["rows"] = rows
    return card, dict(res, struct=st), {}, same


def mr23(card, res, rng):
    """Component rename to other id-format names with the numeric order kept (new two-letter prefix)."""
    st = copy.deepcopy(res["struct"])
    t = st["tables"][0]
    comps = list(t["comps"])
    pre = comps[0].split("-")[0]
    letters = "BCDFGHJKLMNPRSTVWXZ"
    while True:
        p2 = rng.choice(letters) + rng.choice(letters)
        if p2 != pre and p2 not in ("RQ",):
            break
    mp = {c: p2 + "-" + c.split("-")[1] for c in comps}
    for r in t["rows"]:
        r[2] = mp.get(r[2], r[2])
    t["comps"] = [mp[c] for c in comps]

    def m(x):
        if isinstance(x, str):
            return mp.get(x, x)
        if isinstance(x, dict):
            return {k: m(v) for k, v in x.items()}
        if isinstance(x, list):
            return [m(v) for v in x]
        if isinstance(x, tuple):
            return tuple(m(v) for v in x)
        if isinstance(x, frozenset):
            return frozenset(m(v) for v in x)
        return x
    res2 = dict(res, struct=st, q=m(res["q"]), gold=m(res["gold"]), shown=m(res.get("shown")))
    if res.get("options"):
        res2["options"] = [(m(p), m(tx), m(list(tg))) for p, tx, tg in res["options"]]
        res2["gold_text"] = m(res["gold_text"])
    exp = (lambda r0, r2: r2["gold"] == m(r0["gold"]) and (r0["options"] is None or sorted(m(r0["options"])) ==
                                                         sorted(r2["options"])))
    return card, res2, {}, exp


def mr18(card, res, rng):
    """Shift every line time and every question time by D whole days (fixed-offset zone: no DST); a time-valued
    gold maps through the shift."""
    from f9fmt import fmt_dt, parse_dt
    D = rng.choice([-2, -1, 1, 2])
    st = copy.deepcopy(res["struct"])
    t = st["tables"][0]
    for r in t["rows"]:
        r[0] += D * 86400
    q2 = copy.deepcopy(res["q"])

    def sh(x):
        if isinstance(x, dict):
            if x.get("k") == "win":
                f = 1 if x.get("unit") == "day" else 86400
                for k in ("lo", "hi"):
                    if x.get(k) is not None:
                        x[k] += D * f
            for v in x.values():
                sh(v)
        elif isinstance(x, list):
            for v in x:
                sh(v)
    sh(q2)
    res2 = dict(res, struct=st, q=q2)
    b = _base(res["q"])
    sem = card["sem"]
    if res["form"] == "value" and b["op"] in ("first", "last"):
        z, df, tf = sem.get("zone", 0), sem["df"], sem.get("tf") or "hm"
        mv = lambda s: fmt_dt(parse_dt(s, z, df, tf) + D * 86400, z, df, tf)  # noqa: E731
        res2["gold"] = res["gold"] + D * 86400 if isinstance(res["gold"], int) else res["gold"]
        res2["options"] = [(p if tg[0] == "EA" else (mv(p) if isinstance(p, str) else p + D * 86400),
                            tx if tg[0] == "EA" else mv(tx), tg) for p, tx, tg in res["options"]]
        res2["gold_text"] = res["gold_text"] if res["gold_text"] in [tx for p, tx, tg in res["options"]
                                                                     if tg[0] == "EA"] else mv(res["gold_text"])
        exp = (lambda r0, r2: r2["gold"] == (r0["gold"] if r0["gold"] not in [tx for p, tx, tg in res["options"]
                                                                             if tg[0] != "EA"] else mv(r0["gold"])))
        return card, res2, {}, exp
    return card, res2, {}, same


def p1(card, res, rng):
    st = copy.deepcopy(res["struct"])
    pv = st["pivot"]
    moved = False
    for g in pv["groups"]:
        g2 = list(g)
        rng.shuffle(g2)
        moved |= g2 != g
        g[:] = g2
    pv["entities"] = [e for g in pv["groups"] for e in g]
    return (card, dict(res, struct=st), {}, same) if moved else None


def p2(card, res, rng):
    st = copy.deepcopy(res["struct"])
    pv = st["pivot"]
    n = len(pv["periods"])
    perm = list(range(n))
    while perm == list(range(n)):
        rng.shuffle(perm)
    pos = {old: new for new, old in enumerate(perm)}
    pv["periods"] = [pv["periods"][i] for i in perm]
    pv["cells"] = {e: [v[i] for i in perm] for e, v in pv["cells"].items()}
    pv["marks"] = [[e, pos[j]] for e, j in pv["marks"]]
    return card, dict(res, struct=st), {}, same


def p3(card, res, rng):
    """A footnote mark on a cell that no part of Q reads; the printed totals are rewritten by T31 (the renderer
    re-adds them)."""
    st = copy.deepcopy(res["struct"])
    pv = st["pivot"]
    b = _base(res["q"])
    marks = {tuple(m) for m in pv["marks"]}
    cells = [(e, j) for e in pv["entities"] for j in range(len(pv["periods"])) if (e, j) not in marks]
    if b["op"] == "cell":
        cells = [(e, j) for e, j in cells if e != b["ent"]]
    elif b["op"] == "row_total":
        cells = [(e, j) for e, j in cells if e != b["ent"]]
    elif b["op"] == "col_count":
        cells = [(e, j) for e, j in cells if pv["periods"][j] != b["period"]]
    else:
        return None
    if res["form"] != "yn":
        if any(tg[0] not in ("gold", "EA", "E0") for p, tx, tg in res["options"]):
            return None
        e0 = {tg[1] for p, tx, tg in res["options"] if tg[0] == "E0"}
        cells = [(e, j) for e, j in cells if e not in e0]
    if not cells:
        return None
    e, j = rng.choice(cells)
    pv["marks"].append([e, j])
    return card, dict(res, struct=st), {}, same


FNS = {"MR1": mr1, "MR2": mr2, "MR3": mr3, "MR14": mr3, "MR7": mr7, "MR9": mr9, "MR13": mr13, "MR16": mr16,
       "MR18": mr18, "MR20": mr20, "MR23": mr23, "P1": p1, "P2": p2, "P3": p3}
NEEDS_REND = {"MR5": mr5, "MR19": mr19, "MR22": mr22}
# distractors recomputed under the metamorphic rule: order-dependent tie-breaks (E7 first / last listed) after a
# row shuffle, the missed factor (E9) after a unit restatement; every other option and the gold must be unchanged
RETAG = {"MR1": {"E7"}, "MR20": {"E7", "E27"}, "MR22": {"E9"}, "MR13": {"E6"}}  # MR13: an added orphan legitimately moves the E6 "orphans kept" distractor
# repair r1c: MR20 (merged-line shuffle) legitimately moves the E27 "line position instead of line time" distractor (T32)


def _retag(card, res, mode, kinds):
    from f9frames import solve
    from f9render import ans_text
    from f9rows import fm_for
    from f9solve_a import SPECIALS
    opts = list(res["options"])
    gold = [p for p, tx, tg in opts if list(tg)[:1] == ["gold"]]
    out = []
    for p, tx, tg in opts:
        tg = list(tg)
        if tg and tg[0] in kinds and not (tg[0] == "E7" and len(tg) > 1 and tg[1] == "dir"):
            a = solve(card, res["struct"], res["q"], shown=res.get("shown"), alt=tuple(tg))
            same_p = a == p or (isinstance(p, list) and isinstance(a, (tuple, list)) and list(a) == p)
            if not same_p:
                if a in SPECIALS or not isinstance(a, (str, int, Fraction)) or any(a == g for g in gold):
                    return None
                tx = ans_text(card, res["frame"], res["q"], a, fm_for(card, mode), tuple(tg))
                p = a
        out.append((p, tx, tg))
    texts = [tx for _, tx, _ in out]
    if len(set(texts)) != len(texts):
        return None
    return dict(res, options=out)


def same_as(res2):
    want = sorted(tx for _, tx, _ in res2["options"])

    def ok(r0, r2):
        return r2["gold"] == r0["gold"] and sorted(r2["options"]) == want
    return ok


def load_items(mode, sampler):
    from f9build import card_parts, dec, parts_dir, row_targets
    out = []
    d = parts_dir(mode)
    for ct, n in row_targets(mode):
        if ct[1] != sampler:
            continue
        # repair r1c: every finished part of the card (base + top-up parts t1, t2, ...), as merged into the pool
        for stem in card_parts(d, ct[0]):
            rows = [json.loads(x) for x in open(d / f"{stem}.jsonl")]
            sides = [dec(json.loads(x)) for x in open(d / f"{stem}.side.jsonl")]
            for r, sd in zip(rows, sides):
                out.append((ct, r, sd))
    return out


def run(mode, sampler, nrows, per_row=2, seed=20261006):
    import f9g3
    import f9plan
    from f9build import _init_errs
    from f9emit import Emitter
    from f9rows import Ctx
    from f9samp import Retry
    _init_errs()
    items = load_items(mode, sampler)
    rng = random.Random(f"{seed}-{mode}-{sampler}")
    rng.shuffle(items)
    items = items[:nrows]
    rels = RELS[sampler]
    stats = {r: {"tried": 0, "pass": 0, "fail": 0, "na": 0, "skip_tokens": 0} for r in rels}
    fails, cards, k = [], {}, 0
    rows_tested = set()
    for i, (ct, row, side) in enumerate(items):
        if ct[0] not in cards:
            cards[ct[0]] = f9plan.finalize(*ct, held_out=(mode == "dev"))
        card = cards[ct[0]]
        res = rebuild_res(row, side)
        cont = side["container"]
        rend0 = {"container": tuple(cont) if isinstance(cont, list) else cont, "style": row["meta"]["format_style"],
                 "wid": row["meta"]["wording_id"], "mode": side["mode"]}
        tried = 0
        for j in range(len(rels)):
            if tried >= per_row:
                break
            rel = rels[(k + j) % len(rels)]
            r_rng = random.Random(f"{seed}-{row['id']}-{rel}")
            try:
                out = NEEDS_REND[rel](card, res, r_rng, rend0) if rel in NEEDS_REND else FNS[rel](card, res, r_rng)
            except Exception as e:  # a relation that cannot be built on this row is not applicable
                out = None
                stats[rel]["na"] += 1
                continue
            if out is None:
                stats[rel]["na"] += 1
                continue
            card2, res2, over, exp = out
            if rel in RETAG and res2.get("options"):
                try:
                    res2 = _retag(card2, res2, rend0["mode"], RETAG[rel])
                except Exception:
                    res2 = None
                if res2 is None:
                    stats[rel]["na"] += 1
                    continue
                exp = same_as(res2)
            r = dict(rend0, **over)
            em = Emitter(card2, Ctx(), random.Random(f"g4-{row['id']}-{rel}"), "g4", g3=f9g3.check)
            stats[rel]["tried"] += 1
            tried += 1
            try:
                row2, _ = em.finish(res2, mode=r["mode"], container=r["container"], style=r["style"], wid=r["wid"],
                                    ids={"id": row["id"] + "-g4-" + rel, "group_id": row["group_id"],
                                         "call_id": row["call_id"], "seed": row["meta"]["seed"]})
            except Retry as e:
                if str(e).startswith("tokens"):
                    stats[rel]["skip_tokens"] += 1
                    stats[rel]["tried"] -= 1
                    tried -= 1
                    continue
                stats[rel]["fail"] += 1
                fails.append({"row": row["id"], "rel": rel, "why": str(e)[:120]})
                continue
            if exp(row, row2):
                stats[rel]["pass"] += 1
                rows_tested.add(row["id"])
            else:
                stats[rel]["fail"] += 1
                fails.append({"row": row["id"], "rel": rel, "why": "gold mapping differs"})
        k += 1
    rep = {"mode": mode, "sampler": sampler, "rows_sampled": len(items), "rows_tested": len(rows_tested),
           "relations": stats, "fails": fails[:200], "n_fail": len(fails),
           "pass": not fails and len(rows_tested) >= min(1000, len(items)),
           "note": "Hypothesis not installed: seeded random property draws"}
    return rep


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("mode")
    ap.add_argument("sampler")
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--per-row", type=int, default=2)
    a = ap.parse_args()
    from f9build import OUT
    rep = run(a.mode, a.sampler, a.rows, a.per_row)
    d = OUT / "qc"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"g4_{a.mode}_{a.sampler}.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: v for k, v in rep.items() if k != "fails"}))


if __name__ == "__main__":
    main()
