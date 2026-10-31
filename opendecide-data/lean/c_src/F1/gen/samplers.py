"""F1 samplers (G0 F1 v7 section 3): draw the section 2 structure for one row of a card.

S1 forward (rules, then case uniform), S2 label-first (target winner + decisive chain + near-miss), S3 decision table
(conjunction cells, ORDER / SPEC / LATER / PRIORITY / pairs, positioned revision notices), S4 narrative memo (rules as
paragraphs, inert sentences on 30% of non-short rows), S6 amendment chain version-first (g placed around effective
dates). S5 (flowchart, held out) uses the S1 draw and a different render. Every draw is then solved by solver A and
accepted or rejected by the row builder (rows.py); nothing here sets a label.
"""
from __future__ import annotations

import random
from decimal import Decimal

import lexicon as L
from common import dec
from model import Attr, Case, Inert, Item, Lit, Notice, Policy, Rule, Struct
from packs_f1 import load_all

MAX_FIELDS = 10


class DrawFail(Exception):
    pass


# ---------------------------------------------------------------- attributes

def _stems(s):
    return {w[:5] for w in s.lower().replace("-", " ").split() if len(w) >= 4}


def row_attrs(card, pack, rng, n_target=None, include=()):
    """Choose 4-10 row fields: core attributes always; others drawn per row; day-count anchors kept off the row."""
    pa = {a["key"]: a for a in pack["attrs"]}
    reserved = set(card["illus_keys"])
    core = [card["gov_key"]] + list(card["listed_keys"])
    pool = [a for a in pack["attrs"] if a["key"] not in reserved and a["key"] not in core]
    cs = card["constructs"]
    if not any(c.startswith("date_") for c in cs):
        pool = [a for a in pool if a["type"] != "date"]
    if "within" not in cs:
        pool = [a for a in pool if not a.get("daycount")]
    if not ({"bool_true", "bool_false"} & cs):
        pool = [a for a in pool if a["type"] != "bool"]
    if not any(c.startswith("cat_") for c in cs):
        pool = [a for a in pool if a["type"] != "cat"]
    if card["world"] == "open":
        pool = [a for a in pool if a["type"] != "bool" or a.get("false")]
    rng.shuffle(pool)
    n = n_target or rng.randint(4, 8)
    n = max(4, min(MAX_FIELDS, n))
    chosen = [pa[k] for k in core]
    # make sure a numeric field exists
    nums = [a for a in pool if a["type"] == "num"]
    for a in list(include):
        if a in pool and a not in chosen:
            chosen.append(a)
    if nums and not any(a["type"] == "num" for a in chosen):
        chosen.append(nums[0])
    for a in pool:
        if len(chosen) >= n:
            break
        if a in chosen:
            continue
        chosen.append(a)
    # day-count anchors (F1R5-A07): no date field of the row may be the anchor event of a day-count field
    anchors = set()
    for a in chosen:
        if a.get("daycount") and a.get("anchor"):
            anchors |= _stems(a["anchor"])
    if anchors:
        bad = [a for a in chosen if a["type"] == "date" and (_stems(a["name"]) & anchors)]
        if any(a["key"] == card["gov_key"] for a in bad):
            chosen = [a for a in chosen if not a.get("daycount")]
        else:
            chosen = [a for a in chosen if a not in bad]
    # presupposed Boolean fields come along (R8 needs the field Q on the row to keep P true)
    for a in list(chosen):
        if a["type"] == "bool" and a.get("presup") and a["presup"] in pa and pa[a["presup"]] not in chosen:
            if pa[a["presup"]]["key"] not in reserved:
                chosen.append(pa[a["presup"]])
    if card["world"] == "open":
        # open-world case files state every known-false Boolean with a row-4 cue: drop fields that have none
        chosen = [a for a in chosen if a["type"] != "bool" or a.get("false")]
        keys = {a["key"] for a in chosen}
        chosen = [a for a in chosen if not (a["type"] == "bool" and a.get("presup") in pa and a["presup"] not in keys)]
    rng.shuffle(chosen)
    attrs = {}
    lo, hi = card["window"]
    for i, a in enumerate(chosen):
        key = f"f{i + 1}"
        attrs[key] = _mk_attr(key, a, card, (lo, hi))
    # presup keys -> row keys
    k2r = {a["key"]: f"f{i + 1}" for i, a in enumerate(chosen)}
    for key, at in list(attrs.items()):
        if at.type == "bool" and at.presup:
            attrs[key] = Attr(**{**at.__dict__, "presup": k2r.get(at.presup)})
    return attrs, k2r


def _mk_attr(key, a, card, window):
    role = "gov" if a["key"] == card["gov_key"] else ("listed" if a["key"] in card["listed_keys"] else "normal")
    if a["type"] == "num":
        return Attr(key=key, name=a["name"], type="num", unit=a["unit"], places=a["places"], step=dec(a["step"]),
                    lo=dec(a["lo"]), hi=dec(a["hi"]), daycount=bool(a.get("daycount")), anchor=a.get("anchor"),
                    role=role, money=a.get("money", False), pack_key=a["key"])
    if a["type"] == "date":
        return Attr(key=key, name=a["name"], type="date", lo=window[0], hi=window[1], role=role, pack_key=a["key"])
    if a["type"] == "cat":
        return Attr(key=key, name=a["name"], type="cat", values=tuple(a["values"]), role=role, pack_key=a["key"])
    return Attr(key=key, name=a["name"], type="bool", true=a["true"], false=a.get("false"), presup=a.get("presup"),
                role=role, pack_key=a["key"])


def add_distractors(attrs, card, rng, n=None):
    labels = list(L.DISTRACTOR_LABELS)
    anchors = set()
    for a in attrs.values():
        if a.daycount and a.anchor:
            anchors |= _stems(a.anchor)
    labels = [x for x in labels if not (_stems(x) & anchors) and all(x != a.name for a in attrs.values())]
    rng.shuffle(labels)
    n = n if n is not None else rng.randint(1, 3)
    lo, hi = card["window"]
    out = dict(attrs)
    for i, lab in enumerate(labels[:n]):
        key = f"d{i + 1}"
        out[key] = Attr(key=key, name=lab, type="date", lo=lo, hi=hi, role="distractor")
    return out


# ---------------------------------------------------------------- literals

def _grid_pick(a: Attr, rng, lo_frac=0.15, hi_frac=0.85):
    n = int((a.hi - a.lo) / a.step)
    i = rng.randint(int(n * lo_frac), max(int(n * lo_frac), int(n * hi_frac)))
    return a.lo + a.step * i


class LitMaker:
    def __init__(self, S_attrs, card, rng):
        self.A = S_attrs
        self.card = card
        self.rng = rng
        self.cs = card["constructs"]
        self.cat_pol = {}
        self.g_lo = card["B"]

    def usable(self):
        out = []
        for k, a in self.A.items():
            if a.role in ("gov", "distractor"):
                continue
            if a.type == "num" and any(c.startswith("num_") for c in self.cs):
                out.append(k)
            elif a.type == "num" and a.daycount and "within" in self.cs:
                out.append(k)
            elif a.type == "date" and any(c.startswith("date_") for c in self.cs):
                out.append(k)
            elif a.type == "cat" and any(c.startswith("cat_") for c in self.cs):
                out.append(k)
            elif a.type == "bool" and ("bool_true" in self.cs or "bool_false" in self.cs):
                out.append(k)
        return out

    def lit(self, k=None, avoid=()):
        rng = self.rng
        keys = [x for x in self.usable() if x not in avoid]
        if not keys:
            raise DrawFail("no usable fields")
        k = k or rng.choice(keys)
        a = self.A[k]
        if a.type == "num":
            ops = [c[4:] for c in self.cs if c.startswith("num_")]
            if a.daycount and "within" in self.cs:
                ops = ops + ["within", "within"]
            if not ops:
                ops = ["within"]
            op = rng.choice(ops)
            if op == "between":
                t1, t2 = _grid_pick(a, rng, 0.1, 0.6), _grid_pick(a, rng, 0.4, 0.9)
                if t2 <= t1:
                    t2 = t1 + a.step * rng.randint(2, 6)
                    if t2 > a.hi:
                        raise DrawFail("between")
                return Lit(k, "between", (t1, t2))
            return Lit(k, op, (_grid_pick(a, rng),))
        if a.type == "date":
            ops = [c[5:] for c in self.cs if c.startswith("date_")]
            op = rng.choice(ops)
            span = (a.hi - a.lo)
            if op == "fromto":
                d1 = a.lo + rng.randint(int(span * 0.1), int(span * 0.5))
                d2 = d1 + rng.randint(20, max(21, int(span * 0.4)))
                return Lit(k, "fromto", (d1, min(d2, a.hi - 1)))
            return Lit(k, op, (a.lo + rng.randint(int(span * 0.15), int(span * 0.85)),))
        if a.type == "cat":
            pol = self.cat_pol.get(k)
            forms = [c[4:] for c in self.cs if c.startswith("cat_")]
            if pol is not None:
                forms = [f for f in forms if (f.startswith("notin") == (pol == "notin"))] or forms
            f = rng.choice(forms)
            vals = list(a.values)
            if f in ("in1", "notin1"):
                vs = (rng.choice(vals),)
            else:
                m = rng.randint(2, max(2, len(vals) - 1))
                vs = tuple(sorted(rng.sample(vals, m)))
            op = "notin" if f.startswith("notin") else "in"
            if pol is not None and op != pol:
                op = pol
            self.cat_pol[k] = op
            return Lit(k, op, vs)
        if a.type == "bool":
            can_false = "bool_false" in self.cs and a.false
            val = False if (can_false and rng.random() < 0.35) else True
            if "bool_true" not in self.cs and can_false:
                val = False
            return Lit(k, "is", (val,))
        raise DrawFail("lit")


def _uses(it: Item):
    return {m.attr for m in it.mem}


def draw_condition(lm: LitMaker, rng, n_items=None, allow_unless=True, plain=False, kind="gen", used_sets=None):
    cs = lm.cs
    n = n_items or rng.choice([1, 1, 2, 2, 2, 3, 3, 4])
    n = max(1, min(n, len(lm.usable()) - 1))
    # bare or / xor: only item, no unless
    if not plain or "or" in cs:
        if ("xor" in cs and rng.random() < 0.25) or ("or" in cs and rng.random() < 0.18):
            k1 = lm.lit()
            k2 = lm.lit(avoid=(k1.attr,))
            kind_i = "xor" if ("xor" in cs and (rng.random() < 0.6 or "or" not in cs)) else "or"
            return (Item(kind_i, (k1, k2)),), None
    items = []
    usedf = set()
    for i in range(n):
        lists = [x for x in ("all", "any", "kofn") if x in cs]
        free = len([k for k in lm.usable() if k not in usedf])
        try:
            if lists and rng.random() < 0.25 and free >= 3:
                lk = rng.choice(lists)
                m = rng.randint(3 if lk == "kofn" else 2, min(4, free - 1))
                if lk == "kofn" and m < 3:
                    lk = "all"
                mem = []
                for _ in range(m):
                    l = lm.lit(avoid=tuple(usedf | {x.attr for x in mem}))
                    mem.append(l)
                kk = rng.randint(2, m - 1) if lk == "kofn" else 0
                it = Item(lk, tuple(mem), kk)
            else:
                l = lm.lit(avoid=tuple(usedf))
                it = Item("lit", (l,))
        except DrawFail:
            if items:
                break
            raise
        usedf |= _uses(it)
        items.append(it)
    unless = None
    if allow_unless and "unless" in cs and kind != "onlyif" and len(items) >= 1 and rng.random() < 0.3:
        unless = lm.lit(avoid=tuple(usedf))
    return tuple(items), unless


# ---------------------------------------------------------------- rules and notices

def _ids(rng, n, avoid=()):
    pool = [x for x in range(10, 100) if x not in avoid]
    return sorted(rng.sample(pool, n))


def draw_rules(S_attrs, card, rng, n_rules=None, plain=False):
    cs = card["constructs"]
    lm = LitMaker(S_attrs, card, rng)
    P_outs = [o for o in card["outcomes"] if o != card["M"]]
    n = n_rules or rng.choice([3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12])
    n_onlyif = 0
    if "onlyif" in cs:
        n_onlyif = rng.choice([0, 1, 1, 2])
    n_exc = 0
    if "exc" in cs or "pexc_short" in cs:
        n_exc = rng.choice([0, 1, 1, 2, 2, 3])
    n_gen = max(2, n - n_onlyif - n_exc)
    ids = _ids(rng, n_gen + n_exc + n_onlyif)
    rng.shuffle(ids)
    rules = []
    pri = "PRIORITY" in (card["prim"], card["sec"])
    later = "LATER" in (card["prim"], card["sec"])
    B = card["B"]
    for i in range(n_gen):
        items, unless = draw_condition(lm, rng, plain=plain)
        o = rng.choice(P_outs)
        r = Rule(ids[i], "gen", items, unless, o)
        rules.append(r)
    gens = list(rules)
    for j in range(n_exc):
        rid = ids[n_gen + j]
        targets = list(gens)
        if "exc2" in cs:
            targets += [r for r in rules if r.kind in ("pexc", "oexc") and _level(r, rules) == 1]
        t = rng.choice(targets)
        if plain or "pexc_short" in cs:
            kind = "pexc"
        else:
            kind = rng.choice(["pexc", "oexc"])
        items, unless = draw_condition(lm, rng, n_items=rng.choice([1, 1, 2]), plain=plain)
        o = rng.choice([x for x in P_outs if x != t.out] or P_outs) if kind == "oexc" else None
        rules.append(Rule(rid, kind, items, unless, o, target=t.rid))
    for j in range(n_onlyif):
        rid = ids[n_gen + n_exc + j]
        ys = [x for x in P_outs if x not in (card["fallback"],)]
        items, _ = draw_condition(lm, rng, n_items=rng.choice([1, 1, 2]), allow_unless=False, kind="onlyif")
        rules.append(Rule(rid, "onlyif", items, None, rng.choice(ys)))
    for r in rules:
        if pri and r.kind in ("gen", "oexc"):
            r.tier = rng.randrange(len(card["tiers"]))
        if later:
            r.date = B - rng.choice([0, 0, 30, 60, 90, 120, 200, 365])
        if "last" in cs and rng.random() < 0.18:
            r.last = B + rng.randint(30, 420)
    return rules, lm


def _level(r, rules):
    by = {x.rid: x for x in rules}
    lv = 0
    while r.kind in ("pexc", "oexc"):
        lv += 1
        r = by.get(r.target)
        if r is None:
            break
    return lv


def new_rule_text(old: Rule, lm: LitMaker, card, rng, plain=False):
    P_outs = [o for o in card["outcomes"] if o != card["M"]]
    if old.kind == "onlyif":
        items, _ = draw_condition(lm, rng, n_items=rng.choice([1, 2]), allow_unless=False, kind="onlyif")
        return Rule(old.rid, "onlyif", items, None, old.out)
    items, unless = draw_condition(lm, rng, n_items=rng.choice([1, 2, 2, 3]), plain=plain)
    out = rng.choice(P_outs) if old.kind in ("gen", "oexc") else None
    r = Rule(old.rid, old.kind, items, unless, out, target=old.target)
    if "PRIORITY" in (card["prim"], card["sec"]) and r.kind in ("gen", "oexc"):
        r.tier = rng.randrange(len(card["tiers"]))
    if "last" in card["constructs"] and rng.random() < 0.25:
        r.last = card["B"] + rng.randint(60, 480)
    return r


def draw_notices(rules, lm, card, rng, n_not, s3=False, plain=False):
    """0-3 operative notices satisfying R3 (targets in force at effective date, no reuse, no same-date interaction,
    unique S3 positions)."""
    cs = card["constructs"]
    if n_not == 0 or "notices" not in cs:
        return []
    types = [t for t in ("replace", "repeal", "insert") if t in cs]
    if not types:
        return []
    B = card["B"]
    used_ids = {r.rid for r in rules}
    nums = sorted(rng.sample(range(10, 100), n_not))
    rng.shuffle(nums)
    edates = sorted(B + rng.randint(15, 400) for _ in range(n_not))
    if n_not >= 2 and rng.random() < 0.12 and not plain:
        edates[1] = edates[0]  # same-date notices (must not interact; checked below)
    notices = []
    state = {r.rid: r for r in rules}
    touched_by_date = {}
    positions = set()
    for i in range(n_not):
        ed = edates[i]
        nd = max(B, ed + rng.choice([-60, -30, -14, -7, 0, 0, 7, 21, 45]))
        t = rng.choice(types)
        # in force at ed: state after earlier notices, minus expired
        live = {rid: r for rid, r in state.items() if r.last is None or r.last >= ed}
        live = _drop_orphans(live)
        tset = touched_by_date.setdefault(ed, set())
        cand = [rid for rid in live if rid not in tset and all(rid not in _excs_of(live, x) for x in tset)
                and not any(live[x].kind in ("pexc", "oexc") and live[x].target == rid for x in tset)]
        if t in ("replace", "repeal"):
            if not cand:
                continue
            if s3:
                cand = [c for c in cand if live[c].kind == "gen"]
                if not cand:
                    continue
            tgt = rng.choice(cand)
            if t == "replace":
                nr = new_rule_text(live[tgt], lm, card, rng, plain)
                n = Notice(nums[i], "replace", tgt, nr, nd, ed)
                state[tgt] = nr
            else:
                n = Notice(nums[i], "repeal", tgt, None, nd, ed)
                state.pop(tgt)
            tset.add(tgt)
        else:
            nid = _ids(rng, 1, avoid=used_ids)[0]
            used_ids.add(nid)
            kinds = ["gen"]
            if not s3 and "exc" in cs and not plain:
                kinds += ["pexc", "oexc"]
            if not s3 and "onlyif" in cs and not plain:
                kinds.append("onlyif")
            kind = rng.choice(kinds)
            P_outs = [o for o in card["outcomes"] if o != card["M"]]
            if kind == "onlyif":
                items, _ = draw_condition(lm, rng, n_items=1, allow_unless=False, kind="onlyif")
                nr = Rule(nid, "onlyif", items, None, rng.choice([x for x in P_outs if x != card["fallback"]]))
                if sum(1 for r in state.values() if r.kind == "onlyif") >= 2:
                    continue
            elif kind in ("pexc", "oexc"):
                gens = [rid for rid in cand if live[rid].kind == "gen"]
                if not gens:
                    continue
                tg = rng.choice(gens)
                items, unless = draw_condition(lm, rng, n_items=rng.choice([1, 2]), plain=plain)
                o = rng.choice([x for x in P_outs if x != live[tg].out] or P_outs) if kind == "oexc" else None
                nr = Rule(nid, kind, items, unless, o, target=tg)
                tset.add(tg)
            else:
                items, unless = draw_condition(lm, rng, plain=plain)
                nr = Rule(nid, "gen", items, unless, rng.choice(P_outs))
            if "PRIORITY" in (card["prim"], card["sec"]) and nr.kind in ("gen", "oexc"):
                nr.tier = rng.randrange(len(card["tiers"]))
            if "last" in cs and rng.random() < 0.2 and not plain:
                nr.last = ed + rng.randint(30, 300)
            pos = None
            if s3:
                opts = [("top",), ("bottom",)] + [("after", rid) for rid in live if live[rid].kind == "gen"
                                                  and rid not in tset]   # R3: no same-date interaction
                opts = [p for p in opts if p not in positions]
                if not opts:
                    continue
                pos = rng.choice(opts)
                positions.add(pos)
                if pos[0] == "after":
                    tset.add(pos[1])
            n = Notice(nums[i], "insert", None, nr, nd, ed, pos)
            state[nid] = nr
            tset.add(nid)
        notices.append(n)
    return notices


def _excs_of(rules, rid):
    return {x for x, r in rules.items() if r.kind in ("pexc", "oexc") and r.target == rid}


def _drop_orphans(live):
    live = dict(live)
    ch = True
    while ch:
        ch = False
        for rid in list(live):
            r = live[rid]
            if r.kind in ("pexc", "oexc") and r.target not in live:
                live.pop(rid)
                ch = True
    return live


# ---------------------------------------------------------------- inert elements

def draw_inert(rules, notices, lm, card, pack, rng, n=None):
    cs = card["constructs"]
    if "inert" not in cs:
        return []
    n = n if n is not None else rng.choice([1, 1, 2])
    used_nums = {r.rid for r in rules} | {x.num for x in notices}
    out = []
    kinds = ["draft", "other_scope", "comment", "other_body"]
    for _ in range(n):
        k = rng.choice(kinds)
        if k == "comment":
            facts = [x for x in pack.get("inert_facts") or [] if isinstance(x, str) and 3 < len(x) < 90
                     and all(ch not in x for ch in ":;()[]")]
            if not facts:
                continue
            out.append(Inert("comment", text=rng.choice(facts).rstrip(".")))
        elif k == "other_scope":
            items, unless = draw_condition(lm, rng, n_items=rng.choice([1, 2]))
            o = rng.choice([x for x in card["outcomes"] if x != card["M"]])
            r = Rule(0, "gen", items, unless, o)
            sv = rng.choice(card["scope"][2])
            out.append(Inert("other_scope", rule=r, scope_value=sv))
        else:
            gens = [r for r in rules if r.kind == "gen"]
            t = rng.choice(["replace", "repeal"])
            tg = rng.choice(gens)
            ed = card["B"] + rng.randint(15, 400)
            nd = max(card["B"], ed - rng.randint(0, 40))
            if t == "replace":
                nr = new_rule_text(tg, lm, card, rng)
                nt = Notice(None, "replace", tg.rid, nr, nd, ed)
            else:
                nt = Notice(None, "repeal", tg.rid, None, nd, ed)
            if k == "other_body":
                num = rng.choice([x for x in range(100, 200) if x not in used_nums])
                used_nums.add(num)
                nt = nt.copy(num=num)
                out.append(Inert("other_body", num=num, notice=nt, body=rng.choice(card["other_bodies"])))
            else:
                out.append(Inert("draft", notice=nt, body=card["body"]))
    return out


# ---------------------------------------------------------------- case

def _rand_val(a: Attr, rng):
    if a.type == "num":
        n = int((a.hi - a.lo) / a.step)
        return a.lo + a.step * rng.randint(0, n)
    if a.type == "date":
        return rng.randint(a.lo, a.hi)
    if a.type == "cat":
        return rng.choice(a.values)
    if a.type == "bool":
        return rng.random() < 0.5
    raise ValueError


def draw_case(S: Struct, card, rng, g=None, ref=""):
    A = S.attrs
    vals = {}
    for k, a in A.items():
        if a.role == "gov":
            continue
        vals[k] = _rand_val(a, rng)
    P = S.policy
    vals[P.gov] = g if g is not None else P.B + rng.randint(0, 420)
    unknown, notrec = set(), set()
    if P.world == "open":
        cands = [k for k, a in A.items() if a.role == "normal"]
        lit_keys = {m.attr for r in S.rules for it in r.all_items() for m in it.mem}
        pref = [k for k in cands if k in lit_keys]
        nu = rng.choice([0, 1, 1, 1, 2, 2])
        rng.shuffle(pref)
        for k in pref[:nu]:
            unknown.add(k)
    if P.world == "missing" and P.listed and rng.random() < 0.22:
        m = rng.choice([1, 1, 2])
        for k in rng.sample(list(P.listed), min(m, len(P.listed))):
            notrec.add(k)
    for k in unknown | notrec:
        vals.pop(k, None)
    case = Case(vals, frozenset(unknown), frozenset(notrec), ref)
    fix_presup(S, case)
    return case


def fix_presup(S: Struct, case: Case):
    """R8 case constraint: a Boolean P whose phrasing presupposes field Q of the row is true or unknown only when Q is
    stated true."""
    A = S.attrs
    for k, a in A.items():
        if a.type == "bool" and a.presup and a.presup in A:
            q = a.presup
            q_true = case.vals.get(q) is True and q not in case.unknown
            if (case.vals.get(k) is True or k in case.unknown) and not q_true:
                if k in case.unknown:
                    # make Q known true
                    case.vals[q] = True
                    case.unknown = frozenset(case.unknown - {q})
                else:
                    case.vals[k] = False


# ---------------------------------------------------------------- whole structure

def make_policy(card, attrs, k2r):
    return Policy(world=card["world"], prim=card["prim"], sec=card["sec"], tie=card["tie"],
                  strict=tuple(card["strict"]), outcomes=tuple(card["outcomes"]),
                  roles=dict(card["roles"]), valence=dict(card["valence"]), default=card["default"],
                  escalate=card["escalate"], fallback=card["fallback"], M=card["M"],
                  gov=k2r[card["gov_key"]], body=card["body"], B=card["B"],
                  listed=tuple(k2r[k] for k in card["listed_keys"] if k in k2r), tiers=tuple(card["tiers"]),
                  scope_name=card["scope"][0], scope_value=card["scope"][1])


def n_notices_draw(card, rng, sampler):
    if "notices" not in card["constructs"]:
        return 0
    if sampler == "S6":
        return rng.choice([1, 1, 2, 2, 3, 3])
    # cards with notices: 0 22%, 1 35%, 2 25%, 3 18% (overall 0:35 1:30 2:20 3:15 with notice-free cards)
    x = rng.random()
    return 0 if x < 0.05 else 1 if x < 0.40 else 2 if x < 0.72 else 3


def draw_struct(card, pack, rng, sampler=None, plain=None, n_rules=None, n_fields=None, n_not=None):
    """n_not (r2): the planned operative-notice count (G0 8 amendment shares, steered per card by the row builder);
    None draws it as before."""
    sampler = sampler or card["sampler"]
    plain = card["short"] if plain is None else plain
    attrs, k2r = row_attrs(card, pack, rng, n_target=n_fields)
    attrs = add_distractors(attrs, card, rng)
    pol = make_policy(card, attrs, k2r)
    s3 = sampler == "S3"
    if s3:
        rules, lm = draw_table_rules(attrs, card, rng, n=n_rules)
    else:
        rules, lm = draw_rules(attrs, card, rng, n_rules=n_rules, plain=plain)
    nn = n_notices_draw(card, rng, sampler) if (n_not is None or "notices" not in card["constructs"]) else n_not
    notices = draw_notices(rules, lm, card, rng, nn, s3=s3, plain=plain)
    inert = []
    if not plain and "inert" in card["constructs"]:
        p = 0.30 if sampler == "S4" else 0.2
        if rng.random() < p:
            inert = draw_inert(rules, notices, lm, card, pack, rng)
    S = Struct(attrs=attrs, rules=rules, notices=notices, inert=inert, policy=pol)
    set_order(S, card, rng, sampler)
    if s3:
        S.s3_rows = [r.rid for r in rules]
    return S


def draw_table_rules(attrs, card, rng, n=None):
    """S3: rows are conjunctions of cells (one literal, a category value set, or 'any'); one outcome per row."""
    lm = LitMaker(attrs, card, rng)
    cols = [k for k in lm.usable()]
    rng.shuffle(cols)
    cols = cols[:rng.randint(2, min(5, len(cols)))] if len(cols) >= 2 else cols
    if len(cols) < 2:
        raise DrawFail("too few columns")
    n = n or rng.choice([3, 4, 4, 5, 5, 6, 7, 8])
    ids = _ids(rng, n)
    P_outs = [o for o in card["outcomes"] if o != card["M"]]
    rules = []
    pri = "PRIORITY" in (card["prim"], card["sec"])
    later = "LATER" in (card["prim"], card["sec"])
    for i in range(n):
        items = []
        for c in cols:
            if rng.random() < 0.55:
                items.append(Item("lit", (lm.lit(c),)))
        if not items:
            items.append(Item("lit", (lm.lit(rng.choice(cols)),)))
        r = Rule(ids[i], "gen", tuple(items), None, rng.choice(P_outs))
        if pri:
            r.tier = rng.randrange(len(card["tiers"]))
        if later:
            r.date = card["B"] - rng.choice([0, 0, 30, 60, 90, 120, 200, 365])
        rules.append(r)
    lm.table_cols = cols
    return rules, lm


def set_order(S: Struct, card, rng, sampler):
    """Reading order of the operative rule-bearing elements (decisive position, E9)."""
    rules = list(S.rules)
    if sampler == "S4":
        # exception paragraph before or after its target, by draw (C04)
        rules.sort(key=lambda r: r.rid)
        order = []
        for r in rules:
            if r.kind in ("pexc", "oexc"):
                continue
            order.append(r)
        for r in rules:
            if r.kind in ("pexc", "oexc"):
                ti = next((i for i, x in enumerate(order) if x.rid == r.target), None)
                if ti is None:
                    order.append(r)
                elif rng.random() < 0.5:
                    order.insert(ti, r)
                else:
                    order.insert(ti + 1, r)
        rules = order
    elif sampler == "S3":
        pass
    else:
        rules.sort(key=lambda r: r.rid)
    S.rules = rules
    notes = list(S.notices)
    if sampler == "S6":
        # base policy and notices as separate documents, shuffled (C04): the base document is one element group
        docs = [("base", None)] + [("n", n.num) for n in notes]
        rng.shuffle(docs)
        order = []
        for d in docs:
            if d[0] == "base":
                order += [("r", r.rid) for r in rules]
            else:
                order.append(d)
        S.order = order
        S.doc_order = [d[1] if d[0] == "n" else "base" for d in docs]
    else:
        S.order = [("r", r.rid) for r in rules] + [("n", n.num) for n in sorted(notes, key=lambda n: n.num)]
        S.doc_order = None


def recompute_order(S: Struct):
    """Reading order after a rule-list change: S6 keeps its document order; other samplers list rules, then notices."""
    if getattr(S, "doc_order", None):
        order = []
        for d in S.doc_order:
            order += [("r", r.rid) for r in S.rules] if d == "base" else [("n", d)]
        S.order = order
    else:
        S.order = [("r", r.rid) for r in S.rules] + [("n", n.num) for n in sorted(S.notices, key=lambda n: n.num)]
