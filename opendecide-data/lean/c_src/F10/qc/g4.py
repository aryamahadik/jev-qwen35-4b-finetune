"""F10 G4 metamorphic relations (G0 section 6). A separate G4 QC sample (seed tag "g4", never emitted, claims no S7
record) is drawn by the same generator; every base row and every MR variant is rendered by the generator's renderer,
parsed back by the independent parser (G3) and re-solved by solver B (G2); the MR assertion compares the variant's
gold with the base gold through the relation's expected map. 100% pass required on >= 1,000 applicable rows per
(sampler, MR); counts per (sampler, MR) are written to qc/g4_report.json.

Implemented MRs (program samplers S1-S4, S6): MR1 option / record shuffle; MR2 / MR3 consistent rename (invented ->
fresh pseudo-words, neutral -> fresh IDs, swapped -> fresh familiar words); MR4 definition swap (R3-02 rule); MR6
glossary reorder (S1, S2, S6; S3 / S4 logged); MR7 inert record sentence (S4); MR9 larger-unit restatement (U1);
MR10 boundary step; MR11 negation (single and double); MR12 exception toggle; MR13 injected instruction; MR14 reveal
an omitted attribute under a determined answer. S7: MR1, MR3 (neutral-ID rename), MR11, MR15 (code swap).
NOT YET: MR7 inert definition (S1-S3), MR8 inlining -> logged as not run.

Usage: python qc/g4.py run <workers> [rows_per_card]  -> qc/g4_report.json"""
from __future__ import annotations

import copy
import json
import re
import sys
import traceback
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen"))
import common  # noqa: E402
from common import progress, rng, uhash  # noqa: E402
from g3 import _norm_case  # noqa: E402

APPLICABLE = {"S1": ["MR1", "MR2/3", "MR4", "MR6", "MR7", "MR8", "MR9", "MR10", "MR11", "MR12", "MR13", "MR14"],
              "S2": ["MR1", "MR2/3", "MR4", "MR6", "MR7", "MR8", "MR10", "MR11", "MR12", "MR13", "MR14"],
              "S3": ["MR1", "MR3", "MR4", "MR6", "MR7", "MR10", "MR11", "MR12", "MR13", "MR14"],
              "S4": ["MR1", "MR2/3", "MR4", "MR6", "MR7", "MR8", "MR9", "MR10", "MR11", "MR12", "MR13", "MR14"],
              "S6": ["MR1", "MR2/3", "MR4", "MR8", "MR9", "MR11"],
              "S7": ["MR1", "MR3", "MR11", "MR15"]}


def rename_card(card, pack, r):
    """MR2 / MR3: a consistent bijection of every term name to a fresh name of the same mode; every card text that
    carries a name (examples, consequence lines, few-shot, look-alike note, rule text) is renamed at once."""
    import cardgen as C
    order = card["order"]
    old = [card["names"][t] for t in order]
    new = []
    for attempt in range(12):         # fresh names of the same mode, disjoint from the card's current names
        m = len(order) + (attempt % 3)
        if card["mode"] == "neutral":
            cand = C.neutral_ids(r, m)
        elif card["mode"] == "invented":
            cand = C.invented_names(r, m, card["legend"], pack)[0]
        else:
            cand = C.swapped_names(r, m, card["legend"], pack, avoid=set(old))
            cand = [w["word"] if isinstance(w, dict) else w for w in (cand or [])]
        new = [x for x in (cand or []) if x not in old][:len(order)]
        if len(new) == len(order):
            break
    if len(new) < len(order) and card["mode"] == "swapped" and len(old) >= 2:
        # the pack has too few unused familiar words: a derangement of the card's own swapped words (every term gets
        # another familiar word; one simultaneous substitution pass below)
        for _ in range(50):
            new = list(old)
            r.shuffle(new)
            if all(a != b for a, b in zip(old, new)):
                break
    if len(new) < len(order) or any(a == b for a, b in zip(old, new)):
        return None, None
    bij = dict(zip(old, new))
    rx = re.compile(r"(?<![\w-])(" + "|".join(re.escape(o) for o in sorted(old, key=len, reverse=True)) + r")(?![\w-])")
    sub = lambda s: rx.sub(lambda m: bij[m.group(1)], s) if isinstance(s, str) else s
    c2 = copy.deepcopy(card)
    c2["names"] = {t: bij[card["names"][t]] for t in order} | {k: v for k, v in card["names"].items() if k not in order}
    c2["examples"] = {t: [{**e, "text": sub(e["text"])} for e in v] for t, v in card.get("examples", {}).items()}
    if card.get("conseq"):
        c2["conseq"] = {t: sub(v) for t, v in card["conseq"].items()}
    if card.get("fewshot"):
        c2["fewshot"] = [{**f, "case_text": sub(f["case_text"]), "answer": sub(f["answer"])} for f in card["fewshot"]]
    c2["rule_text"] = [sub(x) for x in card["rule_text"]]
    if card.get("lookalike"):
        c2["lookalike"] = sub(card["lookalike"]) if isinstance(card["lookalike"], str) else card["lookalike"]
    return c2, bij


def inline_options(card):
    """MR8 (G0 section 2 Inlining, AR03, R2-01): every (host, rewritten host def) where a positive reference to Y may be
    replaced by Y's raw definition; Y has no ONLY-IF and no Exception. Rules: (i) Y's body is one item allowed at the
    reference's position; (ii) the host body is the bare reference; (iii) Y's list flattens with the same connective."""
    defs = card["defs"]
    out = []
    for hid, h in defs.items():
        for pos in ("body", "unless", "onlyif", "exc"):
            items = h["body"]["items"]
            refs = []
            if pos == "body":
                refs = [(i, it) for i, it in enumerate(items) if it["k"] == "ref"]
            elif pos == "unless":
                refs = [(i, it["unless"]) for i, it in enumerate(items) if it["k"] == "item"
                        and (it.get("unless") or {}).get("k") == "ref"]
            elif (h.get(pos) or {}).get("k") == "ref":
                refs = [(None, h[pos])]
            for i, ref in refs:
                Y = defs.get(ref["to"])
                if Y is None or ref.get("neg") or Y.get("onlyif") is not None or Y.get("exc") is not None:
                    continue
                yb, form = Y["body"], h["body"]["form"]
                one = yb["items"][0] if len(yb["items"]) == 1 else None
                simple = one is not None and (one["k"] == "ref" or one.get("unless") is None)
                h2 = copy.deepcopy(h)
                if pos == "body":
                    if form == "single" and len(items) == 1:                       # (ii)
                        h2["body"] = copy.deepcopy(yb)
                    elif one is not None and (form not in ("XOR", "NEITHER") or simple):   # (i)
                        h2["body"]["items"][i] = copy.deepcopy(one)
                    elif (yb["form"] == "ALL" and form in ("ALL", "NOTALL")) or \
                            (yb["form"] == "ANY" and form in ("ANY", "NOTANY")):     # (iii)
                        h2["body"]["items"][i:i + 1] = copy.deepcopy(yb["items"])
                    else:
                        continue
                else:
                    if not simple:
                        continue
                    cond = copy.deepcopy(one if one["k"] == "ref" else one["atom"])
                    if pos == "unless":
                        h2["body"]["items"][i]["unless"] = cond
                    else:
                        h2[pos] = cond
                out.append((hid, ref["to"], pos, h2))
    return out


def _shape(at):
    S = at.get("S")
    return (at["t"], at.get("a"), at.get("op"), at.get("style"), bool(at.get("neg")), at.get("m"), bool(at.get("half")),
            len(S) if isinstance(S, (list, tuple, set, frozenset)) else None)


def _s6_u1_share(card):
    """Share of S6 terms whose definition (references inlined) has a cmp atom on the converted attribute whose
    constant can be restated exactly in the larger unit (MR9 S6 precondition; steering only)."""
    from values import u1_ok
    import model as M
    cv = card.get("conv_slot")
    if cv is None:
        return 0.0
    defs = card["defs"]

    def ok(did, seen=()):
        for at in M.walk_atoms(defs[did]):
            if at["t"] == "cmp" and at["a"] == cv and u1_ok(card["legend"][cv], at["c"]):
                return True
        return any(ok(i["to"], seen + (did,)) for i in defs[did]["body"]["items"]
                   if i["k"] == "ref" and i["to"] not in seen)
    return sum(ok(t) for t in card["order"]) / max(1, len(card["order"]))


def inert_variant(ctx, spec, r):
    """MR7 (G0 section 6): add an inert definition: false on the case on every completion, referenced by no term,
    disjoint from every term on at-most-one cards, listed after gold on first-listed / decision-list cards, equivalent
    to no definition, not an option. Built as a copy of a term's definition with one atom redrawn to the same shape
    (same attribute, operator, style, polarity, set size), so it uses only constructs whose ST rows the card prints and no
    new operator class (card_classes checked). The parent card's proofs (solver B) must still hold."""
    import cardgen as C
    import model as M
    from solver_b import CardB
    card = ctx.card
    defs, order, leg = card["defs"], card["order"], card["legend"]
    terms = [t for t in order if not defs[t].get("helper")]
    om = spec.get("omitted", [])
    cc = {k: v for k, v in spec["case"].items() if k not in om}
    nid = "TI"
    while nid in defs:
        nid += "I"
    cls = list(card["classes"]) + [1, 2, 3, 4]
    for _ in range(60):
        Z = r.choice(terms)
        d = copy.deepcopy(defs[Z])
        d["id"] = nid
        items = [it for it in d["body"]["items"] if it["k"] == "item" and it["atom"]["t"] != "rel"]
        if not items:
            continue
        it = r.choice(items)
        old = it["atom"]
        new = None
        for _ in range(30):
            x = C.draw_atom(leg, old["a"], r, cls)
            if x is not None and _shape(x) == _shape(old) and x != old:
                new = x
                break
        if new is None:
            continue
        it["atom"] = new
        defs2 = dict(defs)
        defs2[nid] = d
        if card_cls_changed(card, defs2):
            continue
        if card["ctype"] in ("first", "dlist"):
            g = spec.get("gold")
            gi = order.index(g) if g in order else -1
            lo, hi = gi + 1, len(order)
            # sectioned first-listed memo: section A is a contiguous suffix of the card order (printed last), so a
            # section-A copy goes inside that suffix and any other copy before it (printed order == card order)
            fa = [i for i, t in enumerate(order) if defs[t].get("section") == "A"]
            if fa:
                if d.get("section") == "A":
                    lo = max(lo, fa[0])
                else:
                    hi = min(hi, fa[0])
            if lo > hi:
                continue
            pos = r.randint(lo, hi)
        else:
            pos = r.randint(0, len(order))
        order2 = order[:pos] + [nid] + order[pos:]
        mc = M.Card(defs2, order2)
        # an attribute the case does not state is unknown (open world): it is completed like an omitted one
        om_eff = list(om) + [k for k in leg if k not in spec["case"] and k not in om]
        if True in M.possible_meets(mc, leg, cc, om_eff, nid, False, "meets"):
            continue
        # the card's in-definition examples and few-shot cases keep their labels: the inert term is false on them too
        cases = [f.get("case") for f in (card.get("fewshot") or [])]
        if any(c and mc.meets(nid, {k: c.get(str(k), c.get(k)) for k in leg}) for c in cases):
            continue
        cb = CardB(leg, defs2, order2, card["ctype"])
        Rn = cb.region(nid)
        # in-definition examples state only some attributes: the inert term may not meet ANY completion (G3 check)
        ex_bad = False
        for v in (card.get("examples") or {}).values():
            for e in v:
                om_x = [k for k in leg if str(k) not in {str(x) for x in e["stated"]}]
                cs = {k: e["case"].get(str(k), e["case"].get(k)) for k in leg if k not in om_x}
                box = cb.sp.point_box(_norm_case({**{k: 0 for k in om_x}, **cs}), om_x)
                if cb.sp.box_meets(box, Rn):
                    ex_bad = True
        if ex_bad:
            continue
        if cb.sp.empty(Rn) or any(cb.sp.equal(Rn, cb.region(t)) for t in defs):
            continue
        if card["ctype"] in ("amo", "partition") and any(not cb.sp.empty(cb.sp.inter(Rn, cb.region(t))) for t in terms):
            continue
        if cb.proofs(C.draw_ranges(leg), need_uncovered=card["ctype"] in ("amo", "first", "dlist")):
            continue
        c2 = copy.deepcopy(card)
        c2["defs"], c2["order"] = defs2, order2
        used = set(card["names"].values())
        nm = None
        for _ in range(12):
            if card["mode"] == "neutral":
                cand = C.neutral_ids(r, len(used) + 1)
            elif card["mode"] == "invented":
                cand = C.invented_names(r, len(used) + 1, leg, ctx.pack)[0]
            else:
                cand = [w["word"] if isinstance(w, dict) else w for w in
                        (C.swapped_names(r, 1, leg, ctx.pack, avoid=used) or [])]
            cand = [x for x in (cand or []) if x not in used]
            if cand:
                nm = cand[0]
                break
        if nm is None:
            return None
        c2["names"][nid] = nm
        if card.get("natural") is not None:
            c2["natural"] = dict(card["natural"])
        if card.get("polarity"):
            c2["polarity"][nid] = card["polarity"][Z]
        if card.get("conseq"):
            fr = next(iter(card["conseq"].values()))
            c2["conseq"][nid] = fr.replace(card["names"][next(iter(card["conseq"]))], nm, 1)
        return c2
    return None


def card_cls_changed(card, defs2):
    import cardgen as C
    return set(C.card_classes(defs2, card["legend"], card.get("conv_slot") is not None)) != set(card["classes"])


class Ctx:
    def __init__(self, card, pack, r, plan, stats):
        self.card, self.pack, self.r, self.plan, self.stats = card, pack, r, plan, stats


def render_checked(ctx, card, spec, rid):
    """Render with the generator, then G15 loader check, G3 parse + structure hash and G2 solver B (problems list)."""
    import emit as EM
    import g3 as G3
    row, side, c_shown = EM.render_spec(card, spec, rid, ctx.pack, ctx.r, ctx.plan)
    if not side["loader_ok"]:
        return row, None, ["G15 " + "|".join(side["loader_problems"])[:80]]
    st = EM.pool.style(side["style"])
    pa = {a["name"]: a["lex"] for a in c_shown["legend"].values()}
    probs, h = G3.g3_row(row, spec, c_shown, st["container"], pa)
    return row, h, probs


def base_flags(spec, rid, card):
    spec["short"] = uhash(rid, "short") < 0.15
    spec["u1_try"] = False
    spec["inert"] = False


def mr_variants(ctx, spec, row, h):
    """Yield (mr, card, spec2, expect) where expect(row2, h2) -> None (pass) or a problem string."""
    import model as M
    import twins as TW
    card, r = ctx.card, ctx.r
    s = card["sampler"]
    form = spec["form"]
    # MR1
    if form == "choice":
        sp = copy.deepcopy(spec)
        r.shuffle(sp["options"])
        yield "MR1", card, sp, lambda r2, h2: None if r2["gold"] == row["gold"] else "MR1 gold moved"
    elif form == "inv":
        sp = copy.deepcopy(spec)
        perm = list(range(len(sp["records"])))
        r.shuffle(perm)
        sp["records"] = [spec["records"][i] for i in perm]
        sp["gold_idx"] = perm.index(spec["gold_idx"])
        yield "MR1", card, sp, lambda r2, h2: None if TW.row_answer(card, sp) == sp["gold_idx"] else "MR1 record moved"
    # MR2 / MR3
    c2, bij = rename_card(card, ctx.pack, r)
    if c2 is not None:
        mr = "MR3" if card["mode"] == "neutral" else "MR2/3"
        exp_gold = bij.get(row["gold"], row["gold"]) if form == "choice" else row["gold"]
        yield mr, c2, copy.deepcopy(spec), lambda r2, h2, g=exp_gold: None if r2["gold"] == g else "rename map"
    # MR4 on S6 (description rows: the described term follows its definition through the swap)
    if s == "S6":
        G = spec["gold"] if form == "choice" else spec["described"]
        A = None if form == "choice" else spec["ask"]
        pool_ = [t for t in (spec["options"] if form == "choice" else card["order"]) if t != G]
        ys = [Y for Y in pool_ if TW.swap_eligible(card, G, Y)]
        if ys:
            Y = r.choice(ys)
            sig = {G: Y, Y: G}
            sp = copy.deepcopy(spec)
            if form == "choice":
                g = sig[G]
            else:
                g = 1 if sig[G] == A else 0
                if sp.get("neg") == 1:
                    g = 1 - g
                sp["described"] = sig[G]
            sp.update({"swap": [G, Y], "gold": g})
            if form == "choice":      # emitted gold is the option text (the term's name; names stay with ids)
                ok = lambda r2, g=g: r2["gold"] == card["names"][g]
            else:                     # emitted yes / no: same as the base exactly when the solver-A gold is unchanged
                ok = lambda r2, g=g: (r2["gold"] == row["gold"]) == (g == spec["gold"])
            yield "MR4", card, sp, lambda r2, h2, ok=ok: None if ok(r2) else "MR4 S6 map"
    # MR4
    X = TW.target_of(spec) if s != "S6" else None
    if X is not None:
        ys = [Y for Y in card["order"] if Y != X and TW.swap_eligible(card, X, Y)]
        if form == "choice":
            ys = [Y for Y in ys if Y in spec["options"]]
        if ys:
            Y = r.choice(ys)
            defs = TW.swapped_defs(card, X, Y)
            g = TW.row_answer(card, spec, defs)
            if g is not None:
                sp = copy.deepcopy(spec)
                sp.update({"swap": [X, Y], "gold": g})
                if form == "inv":
                    sp["gold_idx"] = g
                mc = M.Card(card["defs"], card["order"])
                one = True
                if form == "choice":   # asserted only where the case meets at most one term on every completion
                    om = spec.get("omitted", [])
                    cc = {k: v for k, v in spec["case"].items() if k not in om}
                    one = sum(1 for t in card["order"] if not card["defs"][t].get("helper")
                              and True in M.possible_meets(mc, card["legend"], cc, om, t, False, "meets")) <= 1
                mapped = {X: Y, Y: X}.get(spec.get("gold"), spec.get("gold")) if form == "choice" else g
                why = f"MR4 map gold {spec.get('gold')} exp {mapped} got {g} ctype {card['ctype']} w {card['world']}"
                yield "MR4", card, sp, lambda r2, h2, ok=(not one or mapped == g), why=why: None if ok else why
    # MR11
    if form == "yn" and not spec.get("neg"):
        for lvl, g in ((1, 1 - spec["gold"]), (2, spec["gold"])):
            sp = copy.deepcopy(spec)
            sp.update({"neg": lvl, "neg_form": int(uhash(lvl, row["id"]) * 2), "gold": g})
            yield "MR11", card, sp, lambda r2, h2, g=g: None if r2["gold"] == g else "MR11 polarity"
    # MR13
    if s in ("S1", "S2", "S3", "S4") and form != "inv":      # the generator never attacks inverted rows
        sp = copy.deepcopy(spec)
        sp["attack"] = True
        yield "MR13", card, sp, lambda r2, h2: None if (r2["gold"] == row["gold"] and h2 == h) else "MR13 changed"
    # MR10 / MR12
    # MR8 (S1, S2, S4, S6; where the inlining rule allows, otherwise skipped and counted)
    if s in ("S1", "S2", "S4", "S6"):
        opts = inline_options(card)
        if opts:
            hid, yid, pos, h2 = r.choice(opts)
            c8 = copy.deepcopy(card)
            c8["defs"][hid] = h2
            yield "MR8", c8, copy.deepcopy(spec), lambda r2, h2_: None if r2["gold"] == row["gold"] else "MR8 changed"
        else:
            ctx.stats["MR8_no_inlinable_ref"] += 1
    cs = ctx.cs
    if s == "S6":       # MR10 / MR12 / MR14 / MR7 / MR13 do not apply to S6 description rows (G0 section 6 table)
        # MR9 (S6): restate (or un-restate) one description constant on the converted attribute in the larger unit
        cv = card.get("conv_slot")
        if cv is not None and spec.get("desc") is not None and spec.get("desc_frame") is not None:
            from values import u1_ok
            import s6 as S6
            sp = copy.deepcopy(spec)
            its = [i for i in sp["desc"]["items"] if i["k"] == "item" and i["atom"]["t"] == "cmp"
                   and i["atom"]["a"] == cv and u1_ok(card["legend"][cv], i["atom"]["c"])]
            if its:
                at = r.choice(its)["atom"]
                if at.get("u1"):
                    at.pop("u1")
                else:
                    at["u1"] = True
                sp["desc_text"] = S6.desc_text(card, sp["desc"], sp["desc_alt"], sp["desc_frame"])
                yield "MR9", card, sp, lambda r2, h2: None if (r2["gold"] == row["gold"] and h2 == h) else "MR9 changed"
            else:
                ctx.stats["MR9_S6_no_u1_atom"] += 1
        if form != "inv":
            c6 = copy.deepcopy(card)
            r.shuffle(c6["order"])
            yield "MR6", c6, copy.deepcopy(spec), lambda r2, h2: None if r2["gold"] == row["gold"] else "MR6 changed"
        return
    tw = TW.twin_boundary(card, copy.deepcopy(spec), r, cs)
    if tw is not None:
        yield "MR10", card, tw, lambda r2, h2, g=tw["gold"]: None if r2["gold"] == (g if form != "choice" else r2["gold"]) else "MR10"
    tw = TW.twin_exception(card, copy.deepcopy(spec), r, cs)
    if tw is not None:
        yield "MR12", card, tw, lambda r2, h2: None if r2["gold"] != row["gold"] else "MR12 gold stayed"
    # MR14
    if card["world"] == "open" and spec.get("omitted") and (form != "choice" or spec["gold"] != "cbd"):
        sp = copy.deepcopy(spec)
        sp["omitted"] = sp["omitted"][1:]
        yield "MR14", card, sp, lambda r2, h2: None if r2["gold"] == row["gold"] else "MR14 changed"
    # MR9
    if card.get("conv_slot") is not None and form != "inv":
        sp = copy.deepcopy(spec)
        sp["u1_try"] = True
        yield "MR9", card, sp, lambda r2, h2: None if (r2["gold"] == row["gold"] and h2 == h) else "MR9 changed"
    # MR7 inert definition (S1, S2, S4; S3 decision lists only)
    if form != "inv" and (s in ("S1", "S2", "S4") or (s == "S3" and card["ctype"] == "dlist")):
        c7 = inert_variant(ctx, spec, r)
        if c7 is not None:
            yield "MR7", c7, copy.deepcopy(spec), lambda r2, h2: None if r2["gold"] == row["gold"] else "MR7 changed"
        else:
            ctx.stats["MR7_no_inert"] += 1
    # MR7b (S4 record inert sentence, reported separately)
    if s == "S4" and form != "inv":
        sp = copy.deepcopy(spec)
        sp["inert"] = True
        yield "MR7b", card, sp, lambda r2, h2: None if (r2["gold"] == row["gold"] and h2 == h) else "MR7b changed"
    # MR6 (S1, S2 prose glossaries; S3 code-table rows; S4 memo lines). Helpers keep their positions; on sectioned
    # first-listed memos the terms are shuffled within their section (section A stays the printed suffix)
    if s in ("S1", "S2", "S3", "S4", "S6") and form != "inv":
        c6 = copy.deepcopy(card)
        dd = card["defs"]
        o = c6["order"]
        slots = [i for i, t in enumerate(o) if not dd[t].get("helper")]
        tt = [o[i] for i in slots]
        if card["ctype"] not in ("amo", "partition", "desc") and any(dd[t].get("section") == "A" for t in tt):
            nA = [t for t in tt if dd[t].get("section") != "A"]
            yA = [t for t in tt if dd[t].get("section") == "A"]
            r.shuffle(nA)
            r.shuffle(yA)
            tt = nA + yA
        else:
            r.shuffle(tt)
        for i, t in zip(slots, tt):
            o[i] = t
        if card["ctype"] in ("amo", "partition", "desc"):
            yield "MR6", c6, copy.deepcopy(spec), lambda r2, h2: None if r2["gold"] == row["gold"] else "MR6 changed"
        else:
            g = TW.row_answer(c6, spec)
            if g is not None:
                sp = copy.deepcopy(spec)
                sp["gold"] = g
                yield "MR6", c6, sp, lambda r2, h2, g=g: None if r2["gold"] is not None else "MR6"


def g4_s7(pc, tag, mult):
    """S7 G4 (G0 section 6: MR1, MR3 via MR15 rename, MR11, MR15) on a card of the S7 plan drawn on the G4 seed range.
    Records come from an in-memory pool (no claim is written: QC rows claim no S7 record). Every variant row passes the
    loader check and G3 (g3_s7) and its expectation."""
    import build_s7 as BS
    import parse_s7 as PS
    import pools
    import s7 as S
    from cardgen import neutral_ids
    from fmt1 import card as fcard
    cbs = {c["id"]: c for c in S.codebooks()}
    cb = cbs[pc["cb"]]
    r = rng("s7card", tag, cb["id"], pc["idx"])
    card = S.build_s7_card(cb, pc["idx"], pc["mode"], r, pc["ex_on"])
    card["card_id"] += f"-{tag}"
    if pc["mode"] == "swapped" and cb["scheme"] == "ghc":
        card["names"] = BS.ghc_perm(card, r)
        card["qnames"] = [card["qform"].format(n=x) for x in card["names"]]
    pool = S.Pool7(cb["scheme"], set())
    idx = pool.index(card["codes"])
    S.add_examples(card, pool, idx, r)
    sty = sorted([s_ for m, ss in pools.styles().items() for s_ in ss], key=lambda s_: s_["id"])
    card["styles"] = r.sample(sty, 6)
    wds = pools.wordings()[0]
    card["wordings"] = r.sample([w for w in wds if w["forms"] == ["any"]], r.choice([4, 5])) + \
        r.sample([w for w in wds if w["forms"] == ["yn"]], 1)
    plan = {"n_rows": int(pc["n_rows"] * mult), "choice_share": max(pc["choice_share"], 0.5),
            "yes_rate": r.uniform(0.2, 0.8), "twin_p": 0.0, "neg_p": 0.0, "dneg_p": 0.0}
    res, fails, stats = Counter(), [], Counter()

    def rend(c, spec, rid):
        short = uhash(rid, "short") < 0.15
        st = c["styles"][int(uhash(rid, "st") * len(c["styles"]))]
        want = ("any", "yn") if spec["form"] == "yn" else ("any",)
        wl = [w for w in c["wordings"] if w["forms"][0] in want]
        wd = wl[int(uhash(rid, "wd") * len(wl))]
        row, ir, q, layout = S.render_row(c, spec, rid, st, wd["text"], short)
        lc = fcard.loader_check(row, must_show=fcard.must_show(ir, question=q, wording=wd["text"]))
        if not lc["ok"]:
            return row, ["loader: " + "|".join(lc["problems"])[:80]]
        probs, _ = PS.g3_s7(row, c, spec, spec["rec"])
        return row, probs

    codes = card["codes"]
    nonres = [i for i, c_ in enumerate(codes) if not c_["residual"]]
    for group in S.s7_groups(card, pool, idx, r, plan, stats):
        spec = group[0]
        rid = f"G4-{card['card_id']}-{spec['gid']:03d}-a"
        try:
            row, probs = rend(card, spec, rid)
        except Exception as e:
            res["base_render_error"] += 1
            res[f"base_render_error:{type(e).__name__}:{str(e)[:60]}"] += 1
            continue
        if probs:
            res["base_fail"] += 1
            res["base_fail:" + probs[0][:70]] += 1
            continue
        var = []
        if spec["form"] == "choice":
            sp = copy.deepcopy(spec)
            while sp["options"] == spec["options"] and len(set(sp["options"])) > 1:
                r.shuffle(sp["options"])
            var.append(("MR1", card, sp, lambda r2, c2: None if r2["gold"] == row["gold"] else "MR1 gold moved"))
        else:
            for lvl in (1, 2):
                sp = dict(spec, neg=lvl, neg_form=r.randrange(2))
                g = 1 - spec["gold"] if lvl == 1 else spec["gold"]
                sp["gold"] = g
                var.append(("MR11", card, sp, lambda r2, c2, g=g: None if r2["gold"] == g else "MR11 gold"))
        # MR3 via MR15 rename: every code to a fresh neutral ID; gold maps through the relabel
        used = set(card["names"])
        new = None
        for _ in range(20):
            cand = neutral_ids(r, len(codes))
            if not used & set(cand) and len(set(cand)) == len(codes):
                new = cand
                break
        if new is not None:
            c3 = dict(card, names=new, qnames=[card["qform"].format(n=x) for x in new])
            var.append(("MR3", c3, copy.deepcopy(spec), lambda r2, c2: None if r2["gold"] == (
                c2["qnames"][spec["gold"]] if spec["form"] == "choice" else spec["gold"]) else "MR3 rename map"))
        # MR15 definition swap: gold follows the definition where the record fits at most one non-residual code
        X = spec["gold"] if spec["form"] == "choice" else spec["ask"]
        if not codes[X]["residual"]:
            cands = [Y for Y in nonres if Y != X and (spec["form"] == "yn" or Y in spec["options"])]
            if cands:
                Y = r.choice(cands)
                sw = S.swapped_codes(codes, X, Y)
                g = S.s7_answer(sw, spec, card["scheme"])
                nfit = sum(S.fits(codes[i], spec["rec"], spec["ti"], card["scheme"]) for i in nonres)
                if g is not None:
                    sp = dict(spec, swap=[X, Y], gold=g)
                    if nfit <= 1 and spec["form"] == "choice":
                        exp = Y
                    elif nfit <= 1:
                        exp = int(S.cond(codes[Y]["condition"], spec["rec"], spec["ti"], card["scheme"]))
                    else:
                        exp = g
                    res["S7|MR15|asserted" if nfit <= 1 else "S7|MR15|recompute"] += 1
                    var.append(("MR15", card, sp, lambda r2, c2, exp=exp: None if r2["gold"] == (
                        c2["qnames"][exp] if spec["form"] == "choice" else exp) else "MR15 gold"))
                else:
                    stats["MR15_no_single_gold"] += 1
        for mr, c2, sp, expect in var:
            key = f"S7|{mr}"
            try:
                row2, probs2 = rend(c2, sp, rid)
            except Exception as e:
                res[key + "|render_error"] += 1
                if len(fails) < 20:
                    fails.append((key, f"render {type(e).__name__}: {str(e)[:80]}"))
                continue
            p_ = probs2[0] if probs2 else expect(row2, c2)
            res[key + ("|fail" if p_ else "|pass")] += 1
            if p_ and len(fails) < 20:
                fails.append((key, p_[:100]))
    return {"card": card["card_id"], "counts": dict(res), "fails": fails,
            "stats": {k: v for k, v in stats.items() if k.startswith("MR")}}


def g4_card(args):
    if args and args[0] == "S7":
        try:
            return g4_s7(*args[1:])
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1200:], "card": args[1]}
    pc, pack_id, rows_per_card, tag = (list(args) + ["g4"])[:4]
    try:
        out = None
        for salt in [None] + [f"cd{i}" for i in range(1, 7)]:     # whole-card redraw, as in the build
            out = _g4_card(pc, pack_id, rows_per_card, tag, salt)
            if out.get("error") != "card draw failed":
                return out
        return out
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1200:], "card": pc}


def _g4_card(pc, pack_id, rows_per_card, tag="g4", salt=None):
    import build_prog as BP
    import cardgen as C
    import cardtext as T
    import packs_f10 as P
    import pools
    from plan import k_drawer
    from samplers import ProgRows
    tr, ho = P.load()
    pack = tr[pack_id]
    r = rng("card", tag, pc["sampler"], pc["idx"], pack_id, *([salt] if salt else []))
    card = C.build_program_card(pc, pack, r)
    if pc.get("_need") == "mr8":
        # steering (G0 section 6): redraw the card on this seed range until it carries an inlinable reference
        for j in range(1, 301):
            if card is not None and inline_options(card) and (pc["sampler"] != "S6" or _s6_u1_share(card) >= 0.5):
                break
            r = rng("card", tag, pc["sampler"], pc["idx"], pack_id, *([salt] if salt else []), f"mr8-{j}")
            card = C.build_program_card(pc, pack, r)
        else:
            return {"error": "card draw failed", "card": pc}
    if card is None:
        return {"error": "card draw failed", "card": pc}
    card["card_id"] = f"F10-{pc['sampler']}-{pc['idx']:02d}-{tag}"
    card["ordinal"] = pc["ordinal"]
    for k in ("examples_on", "conseq_on", "prose_record", "inverted"):
        card[k] = pc.get(k, False)
    if card["sampler"] == "S6":
        card["prose_record"] = False
    T.prepare_card(card, r, pack, pools.styles(), pools.wordings()[0])
    T.add_examples(card, r)
    if pc.get("fewshot"):
        card["fewshot"] = BP.fewshot_for(card, r)
    plan = dict(pc, yes_rate=r.uniform(0.2, 0.8), choice_share=0.5, inv_kmax=9, twin_p=0, neg_p=0, dneg_p=0,
                nameinv_p=0, attack_p=0, n_rows=rows_per_card)
    plan["draw_k"] = k_drawer(card["sampler"], r, len(card["order"]), 1 if card["world"] == "open" else 0)
    stats = Counter()
    if card["sampler"] == "S6":
        import s6
        pr = None
        gen = s6.s6_rows(card, r, plan, stats)
    else:
        pr = ProgRows(card, r, stats)
        gen = pr.groups(plan)
    ctx = Ctx(card, pack, r, plan, stats)
    ctx.cs = pr.cs if pr is not None else None
    res = Counter()
    fails = []
    for group in gen:
        spec = group[0]
        rid = f"G4-{card['card_id']}-{spec['gid']:03d}-a"
        base_flags(spec, rid, card)
        try:
            row, h, probs = render_checked(ctx, card, spec, rid)
        except Exception as e:
            res["base_render_error"] += 1
            res[f"base_render_error:{type(e).__name__}:{str(e)[:60]}"] += 1
            continue
        if probs:
            res["base_fail"] += 1
            res["base_fail:" + probs[0][:70]] += 1
            res["base_fail_card:" + card["card_id"] + ":" + str(pack_id) + ":" + str(salt)] += 1
            continue
        for mr, c2, sp, expect in mr_variants(ctx, spec, row, h):
            key = f"{card['sampler']}|{mr}"
            try:
                row2, h2, probs2 = render_checked(ctx, c2, sp, rid)
            except Exception as e:
                res[key + "|render_error"] += 1
                if len(fails) < 20:
                    fails.append((key, f"render {type(e).__name__}: {str(e)[:80]} @ "
                                  + " < ".join(f"{Path(f.filename).name}:{f.lineno}:{f.name}"
                                               for f in traceback.extract_tb(e.__traceback__)[::-1][:4])))
                continue
            p = probs2[0] if probs2 else expect(row2, h2)
            res[key + ("|fail" if p else "|pass")] += 1
            if p and len(fails) < 20:
                fails.append((key, p[:100]))
    return {"card": card["card_id"], "counts": dict(res), "fails": fails,
            "stats": {k: v for k, v in stats.items() if k.startswith("MR")}}


def main(workers=16, rows_per_card=120, replicas=1, extra=""):
    """replicas: plan copies for every sampler; extra "S3=12,S4=4": more copies for the samplers whose (sampler, MR)
    cells need more applicable rows (steering, section 6). Extra copies make every non-inverted S3 decision-list card
    open-world (MR14 precondition; S3 partitions stay closed as in the plan)."""
    import build as B
    import plan as PL
    jobs = []
    more = {k: int(v) for k, v in (x.split("=") for x in extra.split(",") if x)}
    for i in range(replicas + max((v for k, v in more.items() if k.startswith("S")), default=0)):   # own seed range (tags g4, g4-1, ...), never emitted
        tag = "g4" if i == 0 else f"g4-{i}"
        cards = PL.program_plan(tag)
        pm = B.pack_map(cards, tag)
        for c in cards:
            if i >= replicas:
                if i - replicas >= more.get(c["sampler"], 0):
                    continue
                c = dict(c)
                if c["sampler"] == "S3" and c["ctype"] == "dlist" and not c.get("inverted"):
                    c["world"] = "open"
            jobs.append((c, pm[c["ordinal"]], rows_per_card, tag))
    # MR8 steering for S1 / S2: inlinable references occur only on first-listed cards (class 13, ST30); one plan
    # copy of every S1 / S2 card drawn as first-listed and redrawn until it carries an inlinable reference
    if more.get("MR8", 0):
        for i in range(more["MR8"]):
            tag = f"g4-mr8-{i}"
            cards = PL.program_plan(tag)
            pm = B.pack_map(cards, tag)
            for c in cards:
                if c["sampler"] in ("S1", "S2") and not c.get("inverted"):
                    c = dict(c, ctype="first", _need="mr8")
                    jobs.append((c, pm[c["ordinal"]], rows_per_card, tag))
                elif c["sampler"] == "S6":
                    # S6: reference variant (class 13) redrawn until inlinable, with a conversion line (MR9 S6)
                    c = dict(c, _need="mr8", conv=True)
                    jobs.append((c, pm[c["ordinal"]], rows_per_card, tag))
    # S7 (MR1, MR3, MR11, MR15): the S7 plan on the G4 seed range; extra "S7=<mult>" scales its rows (default 3)
    import build_s7 as BS
    for c in BS.s7_plan("g4"):
        jobs.append(("S7", c, "g4", float(more.get("S7", 3))))
    tot, skips = Counter(), Counter()
    fails, errors = [], []
    with Pool(workers) as p:
        for out in p.imap_unordered(g4_card, jobs):
            if "error" in out:
                c = out.get("card") or {}
                errors.append(out["error"] + " " + (f"{c.get('sampler')}-{c.get('idx')}-{c.get('ctype')}"
                                                    if isinstance(c, dict) else str(c)) + " " + out.get("trace", "")[-300:])
                continue
            tot.update(out["counts"])
            skips.update(out.get("stats", {}))
            fails += out["fails"]
    per = {}
    for k, v in tot.items():
        parts = k.split("|")
        if len(parts) == 3:
            per.setdefault(f"{parts[0]}|{parts[1]}", Counter())[parts[2]] += v
    rep = {"spec": "G0 section 6; 100% pass on >= 1,000 applicable rows per (sampler, MR)",
           "per_sampler_mr": {k: dict(v) for k, v in sorted(per.items())},
           "base": {k: v for k, v in tot.items() if k.startswith("base") and not k.startswith("base_fail_card:")},
           "base_fail_cards": {k[15:]: v for k, v in tot.items() if k.startswith("base_fail_card:")},
           "fail_examples": fails[:40],
           "card_errors": errors[:10], "skipped_no_precondition": dict(skips), "not_run": [],
           "applicable_table": APPLICABLE}
    rep["pass_all_run"] = all(v.get("fail", 0) == 0 and v.get("render_error", 0) == 0 for v in per.values())
    rep["min_rows_per_run_mr"] = min((v.get("pass", 0) + v.get("fail", 0)) for v in per.values()) if per else 0
    (HERE / "g4_report.json").write_text(json.dumps(rep, indent=1))
    progress(f"G4 program samplers: {len(per)} (sampler, MR) cells; all pass {rep['pass_all_run']}; min rows "
             f"{rep['min_rows_per_run_mr']}; card errors {len(errors)}")
    print(json.dumps({k: dict(v) for k, v in sorted(per.items())})[:3000])


if __name__ == "__main__":
    if sys.argv[1] == "run":
        main(int(sys.argv[2]) if len(sys.argv) > 2 else 2, int(sys.argv[3]) if len(sys.argv) > 3 else 120,
             int(sys.argv[4]) if len(sys.argv) > 4 else 1, sys.argv[5] if len(sys.argv) > 5 else "")
