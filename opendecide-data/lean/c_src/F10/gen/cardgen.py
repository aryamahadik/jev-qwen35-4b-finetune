"""F10 card generation (hidden structure only; no text): legend draw, definition ASTs under the operator-class cap,
card types (at-most-one, first-listed, partition table, decision list, description, memo with helpers), names,
polarity tags, examples; every card passes solver B's generation-time proofs before any row exists (section 4)."""
from __future__ import annotations

import itertools
import math

import lexicon as L
import model as M
import names as N
from common import contains_tokens, tokens
from solver_b import CardB

OPERATOR_WORDS = {"any", "all", "none", "not", "unless", "only", "if", "exception", "between", "before", "after",
                  "least", "most", "more", "less", "fewer", "over", "under", "above", "below", "exceeds", "within",
                  "days", "from", "including", "either", "neither", "nor", "following", "means", "yes", "no",
                  "tag", "tags", "one", "other", "except", "anything", "value", "up", "to", "record", "it",
                  "true", "false", "null", "unknown", "recorded", "listed", "stated", "missing", "blank", "pending",
                  "known", "available", "applicable", "specified", "determined", "list", "row", "code", "term",
                  "card", "example", "section", "rule", "extra", "case", "text", "with", "is", "a", "an", "the",
                  "of", "and", "or", "but", "both", "on", "same", "day", "calendar"}
MARKER_WORDS = {"unknown", "null", "false", "true", "yes", "no", "none", "not", "recorded", "unrecorded", "record",
                "records", "list", "listed", "unlisted", "stated", "missing", "blank", "pending", "known",
                "unknown", "available", "unavailable", "applicable", "inapplicable", "specified", "unspecified",
                "determined", "undetermined", "n", "a", "tbd"}


def grid(a, x: float) -> int:
    return int(round(x * (10 ** a["d"])))


def make_legend(pack, r, n_attrs, want=()):
    """Pick n_attrs attributes (one per concept group) from the pack's case entity. want: types to include first."""
    attrs = [a for a in pack["attrs"] if a["type"] in ("count", "qty", "amount", "cat", "flag", "date", "tag")]
    attrs = [a for a in attrs if not (a["type"] in ("cat", "tag") and len(a["values"] or []) < 2)]
    r.shuffle(attrs)
    chosen, groups = [], set()
    for t in want:
        for a in attrs:
            if a["type"] == t and a["group"] not in groups and a not in chosen:
                chosen.append(a)
                groups.add(a["group"])
                break
    for a in attrs:
        if len(chosen) >= n_attrs:
            break
        if a["group"] in groups or a in chosen:
            continue
        chosen.append(a)
        groups.add(a["group"])
    r.shuffle(chosen)
    legend = {}
    for i, a in enumerate(chosen):
        e = {"slot": i, "key": a["key"], "name": a["name"], "type": a["type"], "d": a["d"], "unit": a["unit"],
             "values": None, "lex": {"phrases": a["phrases"], "key_words": a["key_words"],
                                     "state_words": a["state_words"], "statements": a["statements"]},
             "currency": pack["currency"] if a["type"] == "amount" else None, "conv": None}
        if a["type"] in ("count", "qty", "amount"):
            lo, hi = grid(e, max(a["lo"] or 0, 0)), grid(e, a["hi"] if a["hi"] is not None else 100)
            if hi - lo < 4:
                hi = lo + 10 * (10 ** e["d"])
            e["range"] = [lo, hi]
        elif a["type"] == "date":
            e["range"] = [pack["date_lo"], pack["date_hi"]]
        elif a["type"] == "cat":
            e["values"] = list(a["values"])
        elif a["type"] == "tag":
            vs = list(a["values"])
            r.shuffle(vs)
            e["values"] = sorted(vs[:min(len(vs), 5)])
        legend[i] = e
    return legend


def nice_const(a, r, lo_q=0.15, hi_q=0.85):
    lo, hi = a["range"]
    x = lo + (hi - lo) * (lo_q + (hi_q - lo_q) * r.random())
    if a["type"] == "date":
        return int(x)
    g = int(round(x))
    step = 10 ** a["d"]
    if a["type"] == "amount":
        unit = 100 * r.choice([1, 5, 10, 25, 50]) if r.random() < 0.8 else 1
    elif a["type"] == "qty":
        unit = step if r.random() < 0.6 else 1
    else:
        unit = r.choice([1, 1, 5, 10]) if hi - lo > 50 else 1
    g = max(lo + 1, (g // unit) * unit)
    return g


NUMERIC = ("count", "qty", "amount")
from collections import Counter
LAST_WHY = Counter()


def draw_atom(legend, s, r, cls, avoid_classes=()):
    """One atom on slot s using only the card's allowed operator classes (AR13). None if the slot has no allowed
    construct. Base constructs (category in / not in, flags) need no class."""
    a = legend[s]
    t = a["type"]
    ok = [c for c in cls if c not in avoid_classes]
    if t in NUMERIC:
        opts = [c for c in (1, 2, 3) if c in ok]
        if not opts:
            return None
        c = r.choice(opts)
        if c == 3:
            x, y = sorted((nice_const(a, r, 0.1, 0.6), nice_const(a, r, 0.4, 0.9)))
            if y - x < 2:
                y = x + 2 * (10 ** a["d"]) if a["type"] != "count" else x + 2
            return M.A_rng(s, x, y, half=r.random() < 0.35)
        op = r.choice(("ge", "le")) if c == 1 else r.choice(("gt", "lt"))
        return M.A_cmp(s, op, nice_const(a, r))
    if t == "date":
        opts = [c for c in (4, 3) if c in ok]
        if not opts:
            return None
        c = r.choice(opts)
        if c == 3:
            x = nice_const(a, r, 0.05, 0.5)
            return M.A_rng(s, x, x + r.randint(20, 160))
        return M.A_cmp(s, r.choice(("ge", "gt", "le", "lt")), nice_const(a, r))
    if t == "cat":
        vals = a["values"]
        n = r.randint(1, max(1, len(vals) - 1))
        S = r.sample(vals, n)
        neg = r.random() < 0.3
        style = "is" if n == 1 else "oneof"
        if neg and 6 in ok and r.random() < 0.6:
            style = r.choice(("other", "except"))
        return M.A_cat(s, S, neg=neg, style=style)
    if t == "flag":
        return M.A_flag(s, r.random() < 0.6)
    if t == "tag":
        if 7 not in ok:
            return None
        vs = a["values"]
        m = r.choice(("has", "any", "all", "none", "atl", "atlof"))
        if m == "has":
            return M.A_tag(s, "has", [r.choice(vs)])
        if m in ("any", "all", "none"):
            return M.A_tag(s, m, r.sample(vs, r.randint(2, min(3, len(vs)))))
        if m == "atl":
            return M.A_tag(s, "atl", kk=r.randint(1, min(3, len(vs) - 1)))
        S = r.sample(vs, min(len(vs), r.randint(2, 4)))
        return M.A_tag(s, "atlof", S, kk=r.randint(1, len(S) - 1))
    return None


def disc_cells(legend, k, r, cls, slots):
    """k pairwise-disjoint discriminator conditions (each a list of 1-2 atoms) on one or two attributes."""
    cats = [s for s in slots if legend[s]["type"] == "cat" and len(legend[s]["values"]) >= k]
    nums = [s for s in slots if legend[s]["type"] in NUMERIC and (legend[s]["range"][1] - legend[s]["range"][0]) >= 3 * k]
    choices = []
    if cats:
        choices.append("cat")
    if nums and (3 in cls or (1 in cls and 2 in cls) or 1 in cls or 2 in cls):
        choices.append("num")
    if not choices:
        return None, None
    kind = r.choice(choices)
    if kind == "cat":
        s = r.choice(cats)
        vals = list(legend[s]["values"])
        r.shuffle(vals)
        spare = len(vals) - k
        groups = [[v] for v in vals[:k]]
        for v in vals[k:]:
            if r.random() < 0.5 and spare > 1:
                r.choice(groups).append(v)
                spare -= 1
        cells = [[M.A_cat(s, g, style="is" if len(g) == 1 else "oneof")] for g in groups]
        return cells, [s]
    s = r.choice(nums)
    a = legend[s]
    lo, hi = a["range"]
    cuts = sorted(r.sample(range(lo + 1, hi), k + 1)) if hi - lo > k + 2 else list(range(lo + 1, lo + k + 2))
    cells = []
    for i in range(k):
        x, y = cuts[i], cuts[i + 1]
        if 3 in cls:
            cells.append([M.A_rng(s, x, y, half=True)] if r.random() < 0.5 or y - x < 2 else [M.A_rng(s, x, y - 1)])
        else:
            op_lo = "ge" if 1 in cls else "gt"
            op_hi = "lt" if 2 in cls else "le"
            cells.append([M.A_cmp(s, op_lo, x if op_lo == "ge" else x - 1), M.A_cmp(s, op_hi, y if op_hi == "lt" else y - 1)])
    r.shuffle(cells)
    return cells, [s]


def _extra_atom(legend, r, cls, slots, rel=None, used=()):
    """An extra atom on one of `slots` (or a relative atom on the card's pair when class 5 is on)."""
    if rel and 5 in cls and r.random() < 0.35:
        x, e = rel
        return M.A_rel(x, e, r.choice([3, 5, 7, 10, 14, 21, 30, 45, 60, 90]), r.choice(("after", "before")))
    cand = [s for s in slots if s not in used] or list(slots)
    r.shuffle(cand)
    for s in cand:
        at = draw_atom(legend, s, r, cls)
        if at is not None:
            return at
    return None


def gen_def(did, legend, r, cls, base, slots, rel=None, refs=(), ref_sign=None, ctype="amo", n_extra=None, narrow=False):
    """One term definition. base: discriminator atoms that must hold (ALL item or ONLY-IF). refs: term ids this
    definition may reference (positive refs only where ref_sign allows)."""
    used = {a["a"] for a in base}
    forms = ["single", "ALL"]
    if len(base) <= 1:
        forms += ["ANY"] * 2
        if 11 in cls:
            forms += ["NOTANY", "NOTALL", "NEITHER"]
        if 12 in cls:
            forms += ["XOR", "XOR"]
    if base and len(base) == 1 and 9 not in cls:
        forms = [f for f in forms if f in ("single", "ALL")]
    form = r.choice(forms)
    onlyif = exc = None
    items = []
    if form in ("single", "ALL"):
        items = [M.It(a) for a in base]
        n = n_extra if n_extra is not None else (r.choice([0, 1, 1, 2]) if base else r.choice([1, 2, 2, 3]))
        for _ in range(n):
            at = _extra_atom(legend, r, cls, slots, rel, used)
            if at is not None:
                items.append(M.It(at))
                used.add(at["a"])
        if refs and 13 in cls and r.random() < 0.45:
            to = r.choice(list(refs))
            neg = (ref_sign == "neg") or (ref_sign is None and r.random() < 0.4)
            items.append(M.R(to, neg))
        if not items:
            at = _extra_atom(legend, r, cls, slots, rel, used)
            if at is None:
                return None
            items.append(M.It(at))
        form = "single" if len(items) == 1 else "ALL"
    else:
        if base:
            onlyif = base[0]
        n = 2 if form in ("XOR", "NEITHER") else r.choice([2, 2, 3])
        for _ in range(n):
            if refs and 13 in cls and r.random() < 0.25 and not any(i["k"] == "ref" for i in items):
                items.append(M.R(r.choice(list(refs)), (ref_sign == "neg") or (ref_sign is None and r.random() < 0.4)))
                continue
            at = _extra_atom(legend, r, cls, slots, rel, used)
            if at is None:
                return None
            items.append(M.It(at))
            used.add(at["a"])
        if len(items) < 2:
            return None
    # item-level unless (class 8): atom items only; never inside XOR / NEITHER items (R2-02)
    if 8 in cls and form in ("single", "ALL", "ANY", "NOTANY", "NOTALL") and r.random() < 0.35:
        cand = [i for i in items if i["k"] == "item" and i["atom"] not in base]
        if cand:
            it = r.choice(cand)
            b = _extra_atom(legend, r, cls, slots, None, used | {it["atom"]["a"]})
            if b is not None:
                it["unless"] = b
                used.add(b["a"])
    if form in ("ANY", "NOTANY", "NOTALL"):
        un = [i for i in items if i.get("unless") is not None]
        if un and len(un) == len(items):
            un[-1]["unless"] = None
        items.sort(key=lambda i: 0 if i.get("unless") is not None else 1)   # unless-position lint (R5-01)
    if 9 in cls and onlyif is None and r.random() < 0.25:
        onlyif = _extra_atom(legend, r, cls, slots, None, used)
        if onlyif is not None:
            used.add(onlyif["a"])
    if 10 in cls and r.random() < 0.3:
        exc = _extra_atom(legend, r, cls, slots, None, used)
    return M.Def(did, M.Body(form, items), onlyif=onlyif, exc=exc)


# ------------------------------------------------------------------------------------------------ names and lints
def legend_strings(legend, pack=None):
    out = []
    for a in legend.values():
        out.append(a["name"])
        if a.get("unit"):
            out.append(a["unit"])
        if a.get("conv"):
            out.append(a["conv"]["u1"])
        out += list(a.get("values") or [])
        lx = a.get("lex") or {}
        out += [p for p in lx.get("phrases", []) if "{" not in p]
        out += list(lx.get("key_words", [])) + list(lx.get("state_words", []))
    if pack:
        out.append(pack["currency"])
        out += [o["name"] for o in pack["outcomes"]] + list(pack["doc_types"])
    return out


def name_lint(name, legend, pack, others=()):
    """R4-02 / R4-03 / R5-03: no whole-token overlap with legend strings, lexicon, operator and marker words,
    or another defined name on the card. Also no ': ', no line break, never 'Yes' / 'No'."""
    if ": " in name or "\n" in name or name.lower() in ("yes", "no"):
        return False
    tk = tokens(name)
    if not tk or any(t in OPERATOR_WORDS or t in MARKER_WORDS for t in tk):
        return False
    for s in legend_strings(legend, pack):
        if contains_tokens(s, name) or contains_tokens(name, s):
            return False
    for o in others:
        if contains_tokens(o, name) or contains_tokens(name, o):
            return False
    return True


def neutral_ids(r, n):
    letters = [c for c in "ABCDEFGHJKMPQRSTUVWXYZ"]
    shape = r.choice(("ld", "ldd"))
    for _ in range(100):
        pool = set()
        while len(pool) < n:
            pool.add(r.choice(letters) + (str(r.randint(1, 9)) if shape == "ld" else str(r.randint(10, 99))))
        ids = list(pool)
        r.shuffle(ids)
        if n >= 3 and (ids == sorted(ids) or ids == sorted(ids, reverse=True)):
            continue
        return ids
    return ids


def invented_names(r, n, legend, pack, lookalike=False):
    L_ = r.randint(5, 9)
    cands = [w for w in pack.get("jargon", []) if len(w) == L_ and N.invented_ok(w)[0]]
    r.shuffle(cands)
    out = []
    for w in cands:
        if len(out) >= n:
            break
        if name_lint(w, legend, pack, out):
            out.append(w)
    tries = 0
    while len(out) < n and tries < 400:
        tries += 1
        w = N.syllable_word(r, L_)
        if w and w not in out and name_lint(w, legend, pack, out):
            out.append(w)
    if len(out) < n:
        return None, None
    pair = None
    if lookalike and n >= 2:
        base = out[0]
        for _ in range(60):
            i = r.randrange(1, L_)
            w = base[:i] + r.choice("aeiou" if base[i] in "aeiou" else "bdfgklmnprstvz") + base[i + 1:]
            if w != base and w not in out and N.invented_ok(w)[0] and name_lint(w, legend, pack, [x for x in out if x != base]):
                out[1] = w
                pair = (base, w)
                break
    return out, pair


def swapped_names(r, n, legend, pack, avoid=()):
    slots_by_key = {a["key"]: s for s, a in legend.items()}
    words = []
    pool = list(pack["label_words"])
    r.shuffle(pool)
    for w in pool:
        if len(words) >= n:
            break
        if any(t["attr"] not in slots_by_key for t in w["terms"]):
            continue
        if w["word"] in avoid or not name_lint(w["word"], legend, pack, [x["word"] for x in words] + list(avoid)):
            continue
        words.append(w)
    return words if len(words) >= n else None


def natural_pred(word, legend):
    """A label word's natural predicate as a Def AST over the card's legend (name prior only; never a gold)."""
    slots = {a["key"]: s for s, a in legend.items()}
    items = []
    for t in word["terms"]:
        s = slots[t["attr"]]
        a = legend[s]
        op, v = t["op"], t["value"]
        if a["type"] == "flag" or op in ("true", "false"):
            items.append(M.It(M.A_flag(s, op != "false" and v is not False)))
        elif a["type"] in ("cat", "tag"):
            vs = v if isinstance(v, list) else [v]
            if a["type"] == "cat":
                vs = [x for x in vs if x in a["values"]] or a["values"][:1]
                items.append(M.It(M.A_cat(s, vs, neg=(op == "ne"))))
            else:
                vs = [x for x in vs if x in a["values"]] or a["values"][:1]
                items.append(M.It(M.A_tag(s, "any", vs)))
        elif a["type"] == "date":
            items.append(M.It(M.A_cmp(s, "ge", a["range"][0] + (a["range"][1] - a["range"][0]) // 2)))
        else:
            g = grid(a, float(v))
            items.append(M.It(M.A_cmp(s, op if op in ("ge", "gt", "le", "lt") else "ge", g)))
    return M.Def("np", M.Body("single" if len(items) == 1 else "ALL", items))


# ------------------------------------------------------------------------------------------------ card structures
def choose_classes(r, legend, ctype, sampler):
    """The card's allowed operator classes (at most 6, AR13): numeric / date classes first, then structure."""
    types = {a["type"] for a in legend.values()}
    cls = set()
    if types & set(NUMERIC):
        cls.update(r.sample([1, 2, 3], r.choice([1, 2, 2])))
    dates = [s for s, a in legend.items() if a["type"] == "date"]
    if dates:
        if len(dates) >= 2 and ctype not in ("partition", "dlist") and r.random() < 0.45:
            cls.add(5)
        elif r.random() < 0.6:
            cls.add(4)
    if "tag" in types and r.random() < 0.5:
        cls.add(7)
    struct = [6, 8, 9, 10, 11, 12]
    if ctype in ("first", "desc") or sampler == "S4":
        struct += [13, 13]
    if ctype in ("partition", "dlist"):
        struct = [6, 9, 10]
    r.shuffle(struct)
    for c in struct:
        if len(cls) >= r.choice([4, 5, 6]):
            break
        cls.add(c)
    return sorted(cls)[:6] if len(cls) <= 6 else sorted(cls)[:6]


def card_classes(defs, legend, conv=False):
    cl = set()
    for d in defs.values():
        cl |= M.def_classes(d, legend)
    if conv:
        cl.add(14)
    return cl


def draw_ranges(legend):
    return {s: tuple(a["range"]) for s, a in legend.items() if a["type"] in NUMERIC + ("date",)}


def build_amo(legend, r, k, cls, rel):
    slots = [s for s in legend if not rel or s not in rel]
    cells, dslots = disc_cells(legend, k, r, cls, slots)
    if cells is None:
        return None
    other = [s for s in slots if s not in dslots]
    defs = {}
    for i in range(k):
        d = gen_def(f"t{i}", legend, r, cls, cells[i], other, rel)
        if d is None:
            return None
        defs[d["id"]] = d
    return defs, [f"t{i}" for i in range(k)]


def build_first(legend, r, k, cls, rel):
    res = build_first_overlap(legend, r, k, cls, rel) if r.random() < 0.75 else None
    return res or build_first_random(legend, r, k, cls, rel)


def build_first_overlap(legend, r, k, cls, rel):
    """First-listed card from disjoint cells whose earlier terms are widened over a later term's cell: card order
    then decides the overlap, and every term keeps a private region (checked by solver B)."""
    res = build_amo(legend, r, k, cls, rel)
    if res is None:
        return None
    defs, order = res
    for i in r.sample(range(k - 1), max(1, (k - 1) // 2)):
        X = order[i]
        Y = r.choice(order[i + 1:])
        dx, dy = defs[X], defs[Y]
        ax = [it["atom"] for it in dx["body"]["items"] if it["k"] == "item"] + ([dx["onlyif"]] if dx.get("onlyif") and dx["onlyif"]["k"] == "atom" else [])
        ay = [it["atom"] for it in dy["body"]["items"] if it["k"] == "item"] + ([dy["onlyif"]] if dy.get("onlyif") and dy["onlyif"]["k"] == "atom" else [])
        cx = next((a for a in ax if a["t"] == "cat" and not a["neg"]), None)
        cy = next((a for a in ay if cx is not None and a["t"] == "cat" and a["a"] == cx["a"] and not a["neg"]), None)
        if cx is None or cy is None:
            rx_ = next((a for a in ax if a["t"] == "rng"), None)
            ry_ = next((a for a in ay if rx_ is not None and a["t"] == "rng" and a["a"] == rx_["a"]), None)
            if rx_ is None or ry_ is None:
                continue
            keep = (rx_["lo"], rx_["hi"], rx_["half"])
            lo, hi = min(rx_["lo"], ry_["lo"]), max(rx_["hi"], ry_["hi"])
            rx_["lo"], rx_["hi"], rx_["half"] = lo, hi, False
            cb = CardB(legend, defs, order, "first")
            if cb.proofs():
                rx_["lo"], rx_["hi"], rx_["half"] = keep
            continue
        keep = cx["S"], cx.get("style")
        cx["S"] = sorted(set(cx["S"]) | set(cy["S"]))
        cx["style"] = "oneof"
        if len(cx["S"]) == len(legend[cx["a"]]["values"]):
            cx["S"], cx["style"] = keep
            continue
        cb = CardB(legend, defs, order, "first")
        if cb.proofs():
            cx["S"], cx["style"] = keep
    return defs, order


def build_first_random(legend, r, k, cls, rel):
    """First-listed card, drawn in card order with a local check: each new definition keeps a region that no
    earlier one covers (no shadowed term) and equals no earlier one; then references to later-listed terms are
    added where the proofs still pass (ST28 / ST30)."""
    slots = [s for s in legend if (not rel or s not in rel) and draw_atom(legend, s, r, cls) is not None]
    if len(slots) < 2:
        return None
    hot = r.sample(slots, min(len(slots), r.choice([3, 3, 4])))
    defs, order = {}, []
    why = Counter()
    for i in range(k):
        did = f"t{i}"
        ok = False
        for _ in range(40):
            d = gen_def(did, legend, r, cls, [], hot if r.random() < 0.7 else slots, rel)
            if d is None:
                why["gen"] += 1
                continue
            trial = dict(defs)
            trial[did] = d
            cb = CardB(legend, trial, order + [did], "first")
            R = cb.region(did)
            if not R or not cb.sp.comp(R) or not cb.assigned_region(did):
                why["region"] += 1
                continue
            if any(cb.sp.equal(R, cb.region(t)) for t in order):
                why["equiv"] += 1
                continue
            defs, ok = trial, True
            order.append(did)
            break
        if not ok:
            LAST_WHY.clear()
            LAST_WHY.update(why)
            return None
    if 13 in cls:
        for i in r.sample(range(k - 1), max(1, (k - 1) // 3)):
            X = order[i]
            Y = r.choice(order[i + 1:])
            d = defs[X]
            if d["body"]["form"] not in ("single", "ALL"):
                continue
            keep = d
            nd = dict(d, body={"k": "body", "form": "ALL", "items": d["body"]["items"] + [M.R(Y, r.random() < 0.35)]})
            defs[X] = nd
            cb = CardB(legend, defs, order, "first")
            if cb.proofs():
                defs[X] = keep
    return defs, order


def _leaf_atom(legend, s, c, r, cls):
    """One cell atom for a leaf constraint on slot s; None means 'any'."""
    a = legend[s]
    t = a["type"]
    if t in NUMERIC or t == "date":
        lo, hi = c
        dlo = 0 if t in NUMERIC else None
        if (lo is None or lo == dlo) and hi is None:
            return None
        if lo is None or lo == dlo:
            if t == "date":
                return M.A_cmp(s, "lt", hi + 1) if 4 in cls and r.random() < 0.5 else M.A_cmp(s, "le", hi)
            return M.A_cmp(s, "lt", hi + 1) if (2 in cls and (1 not in cls or r.random() < 0.5)) else M.A_cmp(s, "le", hi)
        if hi is None:
            if t == "date":
                return M.A_cmp(s, "ge", lo) if r.random() < 0.5 else M.A_cmp(s, "gt", lo - 1)
            return M.A_cmp(s, "gt", lo - 1) if (2 in cls and (1 not in cls or r.random() < 0.5)) else M.A_cmp(s, "ge", lo)
        if t != "date" and r.random() < 0.4:
            return M.A_rng(s, lo, hi + 1, half=True)
        return M.A_rng(s, lo, hi)
    if t == "cat":
        S = sorted(c)
        if len(S) == len(a["values"]):
            return None
        comp = sorted(set(a["values"]) - set(S))
        if len(comp) < len(S) and r.random() < 0.6:
            return M.A_cat(s, comp, neg=True, style=("other" if 6 in cls and r.random() < 0.5 else ("is" if len(comp) == 1 else "oneof")))
        return M.A_cat(s, S, style="is" if len(S) == 1 else "oneof")
    if t == "flag":
        return None if len(c) == 2 else M.A_flag(s, list(c)[0])
    if t == "tag":
        if c is None:
            return None
        m, tg = c
        return M.A_tag(s, m, [tg])
    return None


def build_partition(legend, r, k, cls):
    """Decision-tree partition of the whole legend domain into k leaves (S3 partition tables, ST27b)."""
    slots = [s for s, a in legend.items() if a["type"] != "date" or 4 in cls]
    slots = [s for s in slots if legend[s]["type"] != "tag" or 7 in cls]
    num_ok = any(c in cls for c in (1, 2, 3))
    slots = [s for s in slots if legend[s]["type"] not in NUMERIC or num_ok]

    def root():
        lf = {}
        for s in slots:
            t = legend[s]["type"]
            lf[s] = (0 if t in NUMERIC else None, None) if t in NUMERIC + ("date",) else (
                frozenset(legend[s]["values"]) if t == "cat" else (frozenset([True, False]) if t == "flag" else None))
        return lf
    leaves = [root()]
    guard = 0
    while len(leaves) < k and guard < 500:
        guard += 1
        i = r.randrange(len(leaves))
        lf = leaves[i]
        s = r.choice(slots)
        a = legend[s]
        t = a["type"]
        if t in NUMERIC + ("date",):
            lo, hi = lf[s]
            rl, rh = a["range"]
            lo2 = rl if lo is None or lo < rl else lo
            hi2 = rh if hi is None or hi > rh else hi
            if hi2 - lo2 < 3:
                continue
            c = r.randint(lo2 + 1, hi2 - 1)
            A, B = dict(lf), dict(lf)
            A[s], B[s] = (lo, c - 1), (c, hi)
        elif t == "cat":
            vs = sorted(lf[s])
            if len(vs) < 2:
                continue
            r.shuffle(vs)
            cut = r.randint(1, len(vs) - 1)
            A, B = dict(lf), dict(lf)
            A[s], B[s] = frozenset(vs[:cut]), frozenset(vs[cut:])
        elif t == "flag":
            if len(lf[s]) < 2:
                continue
            A, B = dict(lf), dict(lf)
            A[s], B[s] = frozenset([True]), frozenset([False])
        else:
            if lf[s] is not None:
                continue
            tg = r.choice(legend[s]["values"])
            A, B = dict(lf), dict(lf)
            A[s], B[s] = ("has", tg), ("none", tg)
        leaves[i:i + 1] = [A, B]
    if len(leaves) < k:
        return None
    r.shuffle(leaves)
    defs = {}
    for j, lf in enumerate(leaves):
        items = []
        for s in slots:
            at = _leaf_atom(legend, s, lf[s], r, cls)
            if at is not None:
                items.append(M.It(at))
        if not items:
            return None
        defs[f"t{j}"] = M.Def(f"t{j}", M.Body("single" if len(items) == 1 else "ALL", items))
    return defs, [f"t{j}" for j in range(len(leaves))]


def add_rule_splits(defs, order, legend, r, cls, n_split):
    """Partition tables: split n_split codes in two with one rule atom C ('only if C' / 'exception: C')."""
    order = list(order)
    for _ in range(n_split):
        if 9 not in cls or 10 not in cls:
            break
        did = r.choice(order)
        d = defs[did]
        if d["onlyif"] is not None or d["exc"] is not None:
            continue
        used = {i["atom"]["a"] for i in d["body"]["items"]}
        cand = [s for s in legend if s not in used and legend[s]["type"] != "date"]
        if not cand:
            continue
        C = draw_atom(legend, r.choice(cand), r, cls)
        if C is None or C["t"] == "tag":
            continue
        new = f"t{len(order)}"
        d2 = M.Def(new, {"k": "body", "form": d["body"]["form"], "items": [dict(i) for i in d["body"]["items"]]}, exc=C)
        d["onlyif"] = C
        defs[new] = d2
        pos = order.index(did)
        order.insert(pos + 1 if r.random() < 0.5 else pos, new)
    return defs, order


def build_dlist(legend, r, k, cls):
    """S3 decision list: disjoint leaves of a partition (1-2 leaves dropped, so 'none' can be gold), shuffled,
    then some rows relaxed (a cell set to 'any') so rows overlap and card order decides; a relaxation that
    shadows a row is undone (no shadowed term, R2-20)."""
    res = build_partition(legend, r, k + r.choice([1, 2]), cls)
    if res is None:
        return None
    defs, order = res
    drop = order[k:]
    for d in drop:
        defs.pop(d)
    order = order[:k]
    r.shuffle(order)
    defs = {f"t{i}": dict(defs[o], id=f"t{i}") for i, o in enumerate(order)}
    order = [f"t{i}" for i in range(len(order))]
    for t in r.sample(order, max(1, len(order) * 2 // 5)):
        its = defs[t]["body"]["items"]
        if len(its) < 2:
            continue
        keep = dict(defs[t])
        cut = r.randrange(len(its))
        nits = its[:cut] + its[cut + 1:]
        defs[t] = dict(defs[t], body={"k": "body", "form": "single" if len(nits) == 1 else "ALL", "items": nits})
        cb = CardB(legend, defs, order, "dlist")
        if any(b.startswith(("shadowed", "equiv", "whole")) for b in cb.proofs()):
            defs[t] = keep
    if 9 in cls or 10 in cls:
        for t in r.sample(order, max(1, len(order) // 6)):
            if defs[t]["onlyif"] is not None or defs[t]["exc"] is not None:
                continue
            used = {i["atom"]["a"] for i in defs[t]["body"]["items"]}
            cand = [s for s in legend if s not in used and legend[s]["type"] not in ("date", "tag")]
            if not cand:
                continue
            C_ = draw_atom(legend, r.choice(cand), r, cls)
            if C_ is None:
                continue
            keep = dict(defs[t])
            key = "onlyif" if (9 in cls and (10 not in cls or r.random() < 0.5)) else "exc"
            defs[t] = dict(defs[t], **{key: C_})
            cb = CardB(legend, defs, order, "dlist")
            if any(b.startswith(("shadowed", "equiv", "whole", "empty")) for b in cb.proofs()):
                defs[t] = keep
    return defs, order


def build_desc(legend, r, k, cls):
    """S6 card: k definitions on one frame that differ only in one atom slot, so every pair is a one-atom
    definition near miss (E3 boundary / constant edits); frame: ALL(f1, [f2], <slot>) or single(<slot>) with optional
    ONLY-IF / Exception. Returns defs, order and the frame info for the description rewrites."""
    nums = [s for s, a in legend.items() if a["type"] in NUMERIC and (a["range"][1] - a["range"][0]) > 3 * k]
    if not nums or not any(c in cls for c in (1, 2)):
        return None
    vs = r.choice(nums)
    others = [s for s in legend if s != vs and legend[s]["type"] in NUMERIC + ("cat", "flag")]
    frame = []
    for s in r.sample(others, min(len(others), r.choice([1, 1, 2]))):
        at = draw_atom(legend, s, r, [c for c in cls if c in (1, 2, 6)])
        if at is not None:
            frame.append(at)
    ops = [o for o, c in (("ge", 1), ("le", 1), ("gt", 2), ("lt", 2)) if c in cls]
    seen, slots_ = set(), []
    tries = 0
    while len(slots_) < k and tries < 200:
        tries += 1
        op = r.choice(ops)
        c = nice_const(legend[vs], r, 0.2, 0.8)
        key = (op, c)
        # no two variants may be equal on the grid: x >= c == x > c-1 on whole-number grids
        canon = (op if op in ("ge", "le") else ("ge" if op == "gt" else "le"), c + (1 if op == "gt" else (-1 if op == "lt" else 0)))
        if key in seen or canon in {(("ge" if o == "gt" else "le") if o in ("gt", "lt") else o, cc + (1 if o == "gt" else (-1 if o == "lt" else 0))) for o, cc in seen}:
            continue
        seen.add(key)
        slots_.append(M.A_cmp(vs, op, c))
    if len(slots_) < k:
        return None
    onlyif = draw_atom(legend, r.choice(others), r, cls) if (9 in cls and others and r.random() < 0.3) else None
    defs = {}
    # reference variant (class 13; G0 section 3 S6 rewrite "inlining a referenced term", MR8): the frame is a shown
    # base term B with no ONLY-IF / Exception, and each slot term is ALL(it is a B, <slot>), so its description inlines
    # B's atoms (AR03: B's ALL list flattens into the host ALL). B itself is one of the k terms (k - 1 slot terms).
    if 13 in cls and frame and k >= 3 and r.random() < 0.6:
        bid = f"t{k - 1}"
        defs[bid] = M.Def(bid, M.Body("single" if len(frame) == 1 else "ALL", [M.It(dict(f)) for f in frame]))
        for j, at in enumerate(slots_[:k - 1]):
            defs[f"t{j}"] = M.Def(f"t{j}", M.Body("ALL", [M.R(bid), M.It(at)]), onlyif=onlyif)
        order = [f"t{j}" for j in range(k)]
        r.shuffle(order)
        return defs, order
    for j, at in enumerate(slots_):
        items = [M.It(dict(f)) for f in frame] + [M.It(at)]
        defs[f"t{j}"] = M.Def(f"t{j}", M.Body("single" if len(items) == 1 else "ALL", items), onlyif=onlyif)
    return defs, [f"t{j}" for j in range(k)]


def build_memo(legend, r, k, cls, ctype, pack, sectioned):
    """S4: helpers (familiar-word overrides, body only) + terms that use them ('it is W' / 'it is not W')."""
    slots = list(legend)
    words = swapped_names(r, 2, legend, pack)
    if not words:
        return None
    nh = 1 if (len(words) < 2 or r.random() < 0.5) else 2
    defs = {}
    helpers = []
    for i in range(nh):
        hs = r.sample(slots, min(len(slots), r.choice([1, 2])))
        its = [M.It(a) for a in (draw_atom(legend, s, r, cls) for s in hs) if a is not None]
        if not its:
            return None
        hid = f"h{i}"
        defs[hid] = M.Def(hid, M.Body("single" if len(its) == 1 else "ALL", its), helper=True)
        helpers.append(hid)
    scoped = None
    if sectioned:
        hid = helpers[0]
        its = [M.It(a) for a in [draw_atom(legend, r.choice(slots), r, cls)] if a is not None]
        if not its:
            return None
        defs[hid + "A"] = M.Def(hid + "A", M.Body("single", its), helper=True, section="A")
        scoped = hid
    cls2 = sorted(set(cls) | {13})
    if ctype == "amo":
        res = build_amo(legend, r, k, cls2, None)
    else:
        res = build_first(legend, r, k, cls2, None)
    if res is None:
        return None
    tdefs, order = res
    # section A terms: every other term on order-free (at-most-one) cards; on first-listed cards a contiguous
    # suffix of the card order, because the memo prints the terms outside section A first and then section A, and
    # the printed order is the card order that decides priority
    n_sec = (len(order) + 1) // 2
    for j, did in enumerate(order):
        d = tdefs[did]
        if sectioned and (j % 2 == 0 if ctype == "amo" else j >= len(order) - n_sec):
            d["section"] = "A"
        hid = helpers[j % len(helpers)]
        use = hid + "A" if (scoped == hid and d.get("section") == "A") else hid
        ref = M.R(use, r.random() < 0.35)
        where = r.random()
        if where < 0.6 or d["body"]["form"] in ("XOR", "NEITHER"):
            if d["body"]["form"] in ("single", "ALL"):
                d["body"]["items"].append(ref)
                d["body"]["form"] = "ALL"
            elif d["onlyif"] is None:
                d["onlyif"] = ref
            else:
                d["body"]["items"].append(ref) if d["body"]["form"] not in ("XOR", "NEITHER") else None
        elif d["exc"] is None:
            d["exc"] = M.R(use, False)
        elif d["onlyif"] is None:
            d["onlyif"] = ref
        # drop term-to-term references on memo cards (helpers carry the nesting; scope isolation is then trivial)
        d["body"]["items"] = [i for i in d["body"]["items"] if not (i["k"] == "ref" and i["to"].startswith("t"))]
        for key in ("onlyif", "exc"):
            if d[key] is not None and d[key]["k"] == "ref" and d[key]["to"].startswith("t"):
                d[key] = None
        if not d["body"]["items"]:
            return None
        if d["body"]["form"] == "single" and len(d["body"]["items"]) > 1:
            d["body"]["form"] = "ALL"
        if d["body"]["form"] == "ALL" and len(d["body"]["items"]) == 1:
            d["body"]["form"] = "single"
        if d["body"]["form"] in ("XOR", "NEITHER") and len(d["body"]["items"]) != 2:
            return None
        if d["body"]["form"] in ("ANY", "NOTANY", "NOTALL") and len(d["body"]["items"]) < 2:
            return None
        defs[did] = d
    used = {x["to"] for d in defs.values() for x in M.walk_refs(d)}
    if not all(h in used for h in helpers):
        return None
    return defs, order, [words[i] for i in range(nh)], scoped


def set_conversion(legend, r):
    cand = [s for s, a in legend.items() if a["type"] in ("count", "qty") and a.get("unit") in L.CONVERSIONS]
    if not cand:
        return None
    s = r.choice(cand)
    u1, k = L.CONVERSIONS[legend[s]["unit"]]
    for t, a in legend.items():   # the ST26 line is unit-wide: every attribute in that unit gets the factor
        if a["type"] in ("count", "qty") and a.get("unit") == legend[s]["unit"]:
            a["conv"] = {"u1": u1, "k": k}
    return s


def build_program_card(plan, pack, r):
    """plan: sampler, ctype (amo / first / partition / dlist / desc), world, mode, k, flags. Returns the card dict
    (hidden structure + card-fixed choices) or None after too many failed draws (logged by the caller)."""
    sampler, ctype, k = plan["sampler"], plan["ctype"], plan["k"]
    redraws = {"proof": 0, "build": 0, "classes": 0, "names": 0}
    for attempt in range(240):
        if attempt and attempt % 80 == 0 and k > 3 and ctype not in ("partition", "dlist"):
            k -= 1            # logged: the card is drawn one term smaller
            redraws["k_reduced"] = redraws.get("k_reduced", 0) + 1
        # R2-25 trim lever 1 (card-wide): legend toward the low end of 4-10
        n_attrs = r.choice([4, 4, 5]) if sampler != "S3" else r.choice([4, 5])
        want = ["cat", "count", "flag"]
        if r.random() < 0.5:
            want += ["date", "date"]
        if r.random() < 0.4:
            want.append("tag")
        legend = make_legend(pack, r, n_attrs, want)
        cls = choose_classes(r, legend, ctype, sampler)
        dates = [s for s, a in legend.items() if a["type"] == "date"]
        rel = tuple(r.sample(dates, 2)) if (5 in cls and len(dates) >= 2) else None
        helpers_words, scoped = [], None
        if sampler == "S4":
            res = build_memo(legend, r, k, cls, ctype, pack, plan.get("sectioned", False))
            if res is not None:
                defs, order, helpers_words, scoped = res
        elif ctype == "amo":
            res = build_amo(legend, r, k, cls, rel)
        elif ctype == "first":
            res = build_first(legend, r, k, cls, rel)
        elif ctype == "partition":
            res = build_partition(legend, r, k - plan.get("n_split", 0), cls)
            if res is not None:
                res = add_rule_splits(res[0], res[1], legend, r, cls, plan.get("n_split", 0))
        elif ctype == "dlist":
            res = build_dlist(legend, r, k, cls)
        elif ctype == "desc":
            res = build_desc(legend, r, k, cls)
        else:
            raise ValueError(ctype)
        if res is None:
            redraws["build"] += 1
            continue
        if sampler != "S4":
            defs, order = res[0], res[1]
        conv = set_conversion(legend, r) if (plan.get("conv") and sampler in ("S1", "S2", "S4", "S6")) else None
        used_cls = card_classes(defs, legend, conv is not None)
        if len(used_cls) > 6:
            redraws["classes"] += 1
            continue
        cb = CardB(legend, defs, order, ctype)
        bad = cb.proofs(draw_ranges(legend), need_uncovered=ctype in ("amo", "first", "dlist"))
        if bad:
            redraws["proof"] += 1
            continue
        if ctype in ("first", "dlist") and attempt < 200 and not any(
                cb.sp.inter(cb.region(order[i]), cb.region(order[j])) for i in range(len(order)) for j in range(i + 1, len(order))):
            redraws["no_overlap"] = redraws.get("no_overlap", 0) + 1
            continue
        card = {"sampler": sampler, "ctype": ctype, "world": plan["world"], "mode": plan["mode"], "legend": legend,
                "defs": defs, "order": order, "pack_id": pack["pack_id"], "persona_seed": pack["persona_seed"],
                "entity": pack["entity"], "entity_plural": pack["entity_plural"], "classes": sorted(used_cls),
                "conv_slot": conv, "helper_words": [w["word"] for w in helpers_words], "scoped": scoped,
                "redraws": redraws}
        if not assign_names(card, pack, r, plan):
            redraws["names"] += 1
            continue
        return card
    return None


def assign_names(card, pack, r, plan):
    order = card["order"]
    n = len(order)
    mode = card["mode"]
    legend = card["legend"]
    avoid = list(card["helper_words"])
    card["lookalike"] = None
    if mode == "invented":
        nm, pair = invented_names(r, n, legend, pack, lookalike=plan.get("lookalike", False))
        if nm is None:
            return False
        if any(not name_lint(x, legend, pack, avoid) for x in nm):
            return False
        card["lookalike"] = pair
    elif mode == "neutral":
        nm = neutral_ids(r, n)
    else:
        words = swapped_names(r, n, legend, pack, avoid=avoid)
        if not words:
            return False
        r.shuffle(words)
        nm = [w["word"] for w in words]
        card["natural"] = {w["word"]: natural_pred(w, legend) for w in words}
    perm = list(range(n))
    r.shuffle(perm)
    card["names"] = {order[i]: nm[perm[i]] for i in range(n)}
    card["names"].update({h: w for h, w in zip([d for d in card["defs"] if card["defs"][d]["helper"] and not d.endswith("A")],
                                                card["helper_words"])})
    for d in card["defs"]:
        if d.endswith("A") and card["defs"][d]["helper"]:
            card["names"][d] = card["names"][d[:-1]]
    return True
