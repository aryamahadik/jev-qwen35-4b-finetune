"""Card factory: one Card per (sampler, pack). Fixes every per-card surface choice (G0 sections 1, 2, 4)."""
from __future__ import annotations

import sys

import lex
from attrs import make_attrs, value_words
from cards import Card
from common import rng, toks
from names import code_ids, code_names, group_names, name_ok, overlap_free
from tax import CardInvalid, build_box, build_group, build_list, build_key, all_cells

sys.path.insert(0, str(__import__("common").FMT1))
from fmt1 import labels as flabels  # noqa: E402

K05 = ((20, 29, 0.55), (30, 44, 0.30), (45, 60, 0.15))
DV_LINE = ("DV01", "DV02", "DV03", "DV05")
DV_LIST = ("DV31", "DV32", "DV33", "DV34")
FT_OK = ("FT01", "FT02", "FT03", "FT05", "FT06", "FT07", "FT08", "FT11", "FT12", "FT13", "FT14", "FT15")


def draw_ncodes(r, lo=20, hi=60):
    x = r.random()
    acc = 0
    for a, b, w in K05:
        acc += w
        if x <= acc:
            return r.randint(max(a, lo), min(b, hi)) if max(a, lo) <= min(b, hi) else r.randint(lo, hi)
    return r.randint(lo, hi)


def _surface(card, r, *, sampler, view):
    card.report, card.reports = r.choice(lex.REPORT_NOUNS)
    card.entity, card.entities = view["entity"], view["entities"]
    card.event = r.choice(lex.EVENT_NOUNS)
    card.mark = r.choice(lex.MARK_WORDS)
    card.people = view["people"][:8]
    card.hedges_used = r.sample(lex.HEDGE_VERBS, 2)
    card.cues_used = list(lex.ABSENCE_CUES)
    card.dv = r.choice(DV_LINE)
    card.dv_list = r.choice(DV_LIST)
    card.ft = r.choice(FT_OK)
    card.persona_seed = view.get("persona_seed")
    card.pack_id = view["pack_id"]
    card.prefix = view["prefix"]
    # frame kinds the card's reports use (SEM-06 lists exactly these)
    kinds = ["OTHER", "PRIOR", "HYPO", "HEDGED", "LATER", "GENERIC", "NEG"]
    r.shuffle(kinds)
    keep = kinds[:r.randint(4, 7)]
    if "OTHER" not in keep:
        keep.append("OTHER")
    card.frame_kinds = [k for k in ("OTHER", "PRIOR", "LATER", "HYPO", "HEDGED", "GENERIC", "NEG") if k in keep]
    card.cmp_forms = {}
    card.records = False
    card.log_lines = False
    card.name_rows = True
    card.cue_sentences = False
    card.examples, card.worked = [], []
    card.is_s7 = False
    card.inverted = False
    card.note_order = {}


def _names_for(card, r, key):
    n = len(card.tax.codes)
    vw = value_words(card.attrs)
    avoid = vw + [a.name for a in card.attrs] + [card.entity, card.entities, card.report, card.reports]
    groups = [list(g) for g in getattr(card.tax, "sibling_groups", [])]
    grouped = {x for g in groups for x in g}
    nb = card.tax.code_neighbours()
    for k in range(n):
        if k not in grouped:
            # join a neighbour's group so the name shares a word with a neighbour (near-synonyms)
            for g in groups:
                if any(x in nb[k] for x in g):
                    g.append(k)
                    grouped.add(k)
                    break
            else:
                groups.append([k])
                grouped.add(k)
    names = code_names(n, groups, *key, avoid=avoid)
    ids = code_ids(n, *key)
    sw = None
    for mode in ("mixed", "group"):
        try:
            sw = flabels.swapped_names(mode, n, "|".join(map(str, key)), exclude=avoid + names + ids)
            break
        except Exception:
            sw = None
    allnames = names + ids + (sw or [])
    if not overlap_free([x for x in names]) or not all(name_ok(x) for x in allnames):
        raise CardInvalid("name check")
    vt = {t for w in vw for t in toks(w)}
    if any(set(toks(x)) & vt for x in names + (sw or [])):
        raise CardInvalid("code name holds a value word")
    low = [x.lower() for x in names + (sw or [])]
    if len(set(low)) != len(low) or any(x in (lex.NONE_CODES.lower(), lex.NONE_REPORTS.lower()) for x in low):
        raise CardInvalid("names not distinct")
    card.names, card.ids, card.swapped = names, ids, sw


def bucket_low(n):
    """The low end of n's K05 code-count bucket (G15 length lever 1: the card stays in its bucket)."""
    for a, b, _ in K05:
        if a <= n <= b:
            return a
    return n


S6_REPEAT_SHARE = (0.3, 0.3, 0.15, 0.0)     # by trim level (G0 S6: at most one third of codes in two entries)


def make_program_card(sampler, view, idx, *, form_hint=None, inverted=False, short=False, examples=0,
                      worked=0, default_missing=False, attempt=0, trim=0):
    """sampler: S1 | S2 | S3 | S4 | S6 | S5 (program arm). Raises CardInvalid when the draw fails.
    trim (G15 length levers, build.length_trim; no label, share or bucket changes): 0 none; >= 1 the code count moves
    to the low end of its K05 bucket; S6 >= 2 fewer repeated entries (<= 15% of codes), 3 none."""
    key = ("card", sampler, view["pack_id"], idx, attempt)
    r = rng(*key)
    card = Card(sampler=sampler, card_id=f"F11-{sampler}-{idx:03d}", view=view)
    _surface(card, r, sampler=sampler, view=view)
    card.inverted = inverted
    if short:
        nv = r.choice(([4, 4, 3], [4, 3, 3], [3, 3, 3], [4, 4, 4], [3, 3, 4]))
        attrs = make_attrs(view, {"nom": nv}, *key)
        prod = 1
        for a in attrs:
            prod *= a.n
        if not 20 <= prod <= 60:
            raise CardInvalid("short-card product outside 20-60")
        # one code per cell: a full split tree down to single cells
        tax = build_box(attrs, prod, r, sampler=sampler)
        card.form = "short"
        card.shape = "box"
        card.attrs, card.tax = attrs, tax
        card.ai = {a.aid: i for i, a in enumerate(attrs)}
        card.frame_kinds = [k for k in card.frame_kinds if k in ("OTHER", "PRIOR", "NEG")] or ["OTHER", "PRIOR"]
        if "OTHER" not in card.frame_kinds:
            card.frame_kinds = ["OTHER"] + card.frame_kinds
        for c in tax.codes:
            cell = next(cl for cl, k in tax.table.items() if k == c.k)
            c.short_cell = cell
        card.names = [" / ".join(attrs[i].values[cell[i]] for i in range(len(attrs)))
                      for cell in (c.short_cell for c in tax.codes)]
        card.ids = code_ids(len(tax.codes), *key)
        card.swapped = None
        card.order = list(range(len(tax.codes)))
        r.shuffle(card.order)
        card.records = False
        return card
    n_codes = draw_ncodes(r)
    if trim:
        n_codes = bucket_low(n_codes)
    if sampler in ("S1", "S2", "S4"):
        if sampler == "S4":
            plan = {"nom": [4, 3], "num": r.choice((3, 4)), "pres": r.random() < 0.5}
            if not plan["pres"]:
                plan["date"] = 2
            if inverted:
                plan = {"nom": [4, 3], "num": 3, "pres": True}
        else:
            plan = {"nom": r.choice(([4, 4], [4, 3], [4, 4, 3])), "num": r.choice((None, 3, 3, 4)),
                    "pres": r.random() < 0.5}
            if len(plan["nom"]) == 3 and plan["num"] and plan["pres"]:
                plan["pres"] = False
            if inverted and len(plan["nom"]) > 2 and plan["num"] and plan["pres"]:
                plan["nom"] = [4, 4]
        attrs = make_attrs(view, plan, *key)
        ncell = len(all_cells(attrs))
        n_codes = min(n_codes, max(20, ncell // 3))
        if ncell < 2 * n_codes:
            raise CardInvalid("cell space too small")
        default = None
        if default_missing:
            cand = [a for a in attrs if a.kind in ("nom", "pres")]
            a = r.choice(cand)
            default = (a.aid, r.randrange(a.n))
        tax = build_box(attrs, n_codes, r, n_unless=r.choice((0, 1, 1, 2)), n_onlyif=r.choice((0, 0, 1)),
                        n_notes=r.choice((0, 1, 1, 2)), default=default, sampler=sampler)
        card.shape = "box"
        card.form = "table" if n_codes >= 30 else "oneline"
        card.records = sampler == "S4"
    elif sampler == "S3":
        nv = r.choice(([5, 4, 4], [5, 4, 3], [4, 4, 4], [5, 4, 4]))
        plan = {"nom": nv}
        if r.random() < 0.4:
            plan = {"nom": nv[:2], "num": 3}
        attrs = make_attrs(view, plan, *key)
        noms = [a for a in attrs if a.kind == "nom"]
        g = max(noms, key=lambda a: a.n)
        attrs = [g] + [a for a in attrs if a is not g]
        for j, a in enumerate(attrs):
            a.aid = f"a{j}"
        n_top = r.randint(3, min(5, g.n))
        leaf_space = 1
        for a in attrs[1:]:
            leaf_space *= a.n
        per = max(3, min(10, n_codes // n_top))
        leaves_per = [max(3, min(leaf_space - 1, per + r.randint(-1, 1))) for _ in range(n_top)]
        tax = build_group(attrs, r, n_top=n_top, leaves_per=leaves_per, n_scope=r.choice((1, 1, 2)))
        if not 20 <= len(tax.codes) <= 60:
            raise CardInvalid("S3 code count")
        card.shape = "group"
        card.form = "group"
        card.gnames = group_names(len(tax.groups), *key, avoid=value_words(attrs))
        card.group_order = list(range(len(tax.groups)))
        r.shuffle(card.group_order)
        card.leaf_order = {}
        for gi, gr in enumerate(tax.groups):
            lo = list(gr["leaves"])
            r.shuffle(lo)
            card.leaf_order[gi] = lo
        tax.sibling_groups = [[k for k in gr["leaves"]] + ([gr["residual"]] if gr["residual"] is not None else [])
                              for gr in tax.groups]
    elif sampler == "S6":
        attrs = make_attrs(view, {"nom": [4, 4, 4], "num": 3}, *key)
        tax = build_list(attrs, n_codes, r, max_repeat_share=S6_REPEAT_SHARE[min(trim, 3)])
        card.shape = "list"
        card.form = "list"
        tax.sibling_groups = []
        # near-synonym groups: codes whose entries are adjacent in the list share a head word
        ks = [k for _, k in tax.entries] + [tax.catch]
        seen, grp = set(), []
        for k in ks:
            if k not in seen:
                seen.add(k)
                grp.append(k)
                if len(grp) == 3:
                    tax.sibling_groups.append(grp)
                    grp = []
        if grp:
            tax.sibling_groups.append(grp)
    elif sampler == "S5":
        attrs = make_attrs(view, {"nom": [4, 4, 3], "num": 3}, *key)
        n_codes = min(n_codes, 40)
        tax = build_key(attrs, n_codes, r)
        card.shape = "key"
        card.form = "key"
        groups_named = sorted({c["group"] for c in tax.couplets.values() if c.get("group") is not None})
        card.gnames = group_names(max(2, len(groups_named)), *key, avoid=value_words(attrs))
        tax.sibling_groups = []
        # siblings: codes under one couplet
        for n, cp in tax.couplets.items():
            ks = [x[1] for x in (cp["a"], cp["b"]) if x[0] == "k"]
            if len(ks) == 2:
                tax.sibling_groups.append(ks)
    else:
        raise ValueError(sampler)
    card.attrs, card.tax = attrs, tax
    card.ai = {a.aid: i for i, a in enumerate(attrs)}
    _names_for(card, r, key)
    card.order = list(range(len(tax.codes)))
    r.shuffle(card.order)
    for w, l in tax.notes:
        card.note_order[(w, l)] = r.randrange(2)
    for a in attrs:
        if a.kind == "num":
            card.cmp_forms[("ge", a.aid)] = r.choice(lex.CMP_GE)
            card.cmp_forms[("lt", a.aid)] = r.choice(lex.CMP_LT)
    if tax.default is not None:
        a = attrs[card.ai[tax.default[0]]]
        card.cue_sentences = a.kind == "nom" and r.random() < 0.5
    if sampler == "S4":
        import records
        records.setup_card(card, r, {t for w in value_words(attrs) for t in toks(w)})
    return card
