"""Render one row spec into an F10 row (spec 2.4 format) + its side-manifest entry; fmt1 placement + loader_check."""
from __future__ import annotations

import random

import copy

import cardtext as CT
import lexicon as L
import model as M
import rows as RW
from common import FAMILY, GEN_VERSION, GIT_SHA, LIC_PROGRAM, SEED, SPEC_ID, contains_tokens, tokens, uhash
from fmt1 import pool
from values import u1_ok


def variant_card(card, spec, pack):
    """The card a twin row shows: definitions swapped (defswap) or one name replaced (name invariance)."""
    if not spec.get("swap") and not spec.get("nameinv"):
        return card
    c2 = copy.copy(card)
    if spec.get("swap"):
        import twins as TW
        X, Y = spec["swap"]
        c2["defs"] = TW.swapped_defs(card, X, Y)
        ex = dict(card.get("examples", {}))
        tpl = L.EXAMPLE_S3 if card["sampler"] == "S3" else L.EXAMPLE

        def ren(lst, new):
            out = []
            for e in lst:
                head = e["text"].rsplit(" meets the ", 1)[0]
                out.append({**e, "text": tpl.format(R=head, T=card["names"][new])})
            return out
        ex[X], ex[Y] = ren(card.get("examples", {}).get(Y, []), X), ren(card.get("examples", {}).get(X, []), Y)
        c2["examples"] = ex
    if spec.get("nameinv"):
        X = spec["ask"]
        word = spec["nameinv_word"]
        c2["names"] = dict(card["names"])
        old = card["names"][X]
        c2["names"][X] = word
        c2["examples"] = {t: [{**e, "text": e["text"].replace(old, word)} for e in v]
                          for t, v in card.get("examples", {}).items()}
        if card.get("conseq"):
            c2["conseq"] = {t: v.replace(old, word) for t, v in card["conseq"].items()}
        c2["lookalike"] = None if card.get("lookalike") and old in card["lookalike"] else card.get("lookalike")
    return c2


def opt_text(card, o):
    if o == "none":
        return card["rc"]["none"]
    if o == "cbd":
        return card["rc"]["cbd"]
    return card["names"][o]


def pick_style(card, spec, rid, need_para=False, need_section=False):
    ids = list(card["rc"]["styles"])
    k0 = int(uhash(rid, "style") * len(ids))
    for j in range(len(ids)):
        st = pool.style(ids[(k0 + j) % len(ids)])
        if need_section and "section" not in st["accepts"]:
            continue
        if not RW.style_ok_for(card, st, need_para):
            continue
        if spec.get("u1") is not None and card.get("prose_record"):
            continue
        return st
    return None


def attack_text(card, spec, r, pack):
    """One registered attack frame (instruction / in-record label / redefinition); label agreement 50% (AR16)."""
    order = card["order"]
    if spec["form"] == "choice":
        terms = [o for o in spec["options"] if o not in ("none", "cbd")]
        agree = r.random() < 0.5 and spec["gold"] not in ("none", "cbd")
        X = spec["gold"] if agree else r.choice([t for t in terms if t != spec["gold"]] or terms)
        agree = X == spec["gold"]
    else:
        want_yes_label = r.random() < 0.5
        X = spec["ask"] if want_yes_label else r.choice([t for t in order if t != spec["ask"]] or order)
        implied = 1 if X == spec["ask"] else 0
        if spec.get("neg") == 1:
            implied = 1 - implied
        agree = implied == spec["gold"]
    kind = r.choice(["instr", "label", "redef"])
    name = card["names"][X]
    if kind == "instr":
        return r.choice(L.ATTACK_INSTR).format(X=name), kind, X, agree
    if kind == "label":
        return r.choice(L.ATTACK_LABEL).format(X=name), kind, X, agree
    from cardgen import draw_atom
    from render import atom_text
    om = set(spec.get("omitted", []))
    slots = [s for s in card["legend"] if s not in om]
    for _ in range(20):
        at = draw_atom(card["legend"], r.choice(slots), r, [1, 2, 3, 4, 7])
        if at is None or (at["t"] == "cat" and (len(at["S"]) == 1 and not at["neg"])) or at["t"] == "rel":
            continue
        cond = atom_text(card, at, ("attack", spec.get("gid"), r.random()))
        return r.choice(L.ATTACK_REDEF).format(X=name, COND=cond), kind, X, agree
    return r.choice(L.ATTACK_LABEL).format(X=name), "label", X, agree


def inert_sentence(card, pack, r):
    from cardgen import legend_strings
    leg_s = legend_strings(card["legend"], pack)
    names = list(card["names"].values())
    vocab = [w for w in pack.get("inert_vocab", []) if w.isalpha() and len(w) > 3
             and not any(contains_tokens(s, w) for s in leg_s) and not any(contains_tokens(n, w) for n in names)
             and w.lower() not in ("record", "list", "none", "unknown", "known", "missing", "blank", "pending")]
    if len(vocab) < 2:
        return None
    w1, w2 = r.sample(vocab, 2)
    return r.choice(L.INERT).format(w1=w1, w2=w2)


def inv_doc(card, spec, labels, typed=False):
    leg = card["legend"]
    secs = []
    for lab, case in zip(labels, spec["records"]):
        pairs = [[leg[s]["name"], bool(case[s]) if (typed and leg[s]["type"] == "flag") else RW.val_text(leg[s], case[s], card)]
                 for s in sorted(leg)]
        secs.append({"type": "section", "heading": lab, "blocks": [{"type": "fields", "label": None, "pairs": pairs}]})
    return {"title": card["entity_plural"].capitalize(), "blocks": secs}


def render_spec(card, spec, rid, pack, r, plan):
    """Returns (row, side) or raises FormatError / ValueError (a generator bug or an unrenderable draw)."""
    c = variant_card(card, spec, pack)
    form = spec["form"]
    extra = []
    side = {"attack": None, "inert": False}
    if spec.get("attack"):
        txt, kind, X, agree = attack_text(c, spec, r, pack)
        extra.append(txt)
        side["attack"] = {"kind": kind, "label_term": X, "agrees": agree}
    if card["sampler"] == "S6":
        st_ok = None
    if card["sampler"] == "S4" and form != "inv" and not spec.get("attack") and spec.get("inert"):
        t = inert_sentence(c, pack, r)
        if t:
            extra.append(t)
            side["inert"] = True
    st = pick_style(c, spec, rid, need_para=bool(extra), need_section=(form == "inv"))
    if st is None:
        raise ValueError("no style")
    want = {"yn": ("any", "yn"), "choice": ("any", "choice") if card["sampler"] in ("S1", "S2", "S4", "S6") else ("any",),
            "inv": ("any",)}[form]
    wl = [w for w in c["rc"]["wordings"] if w["forms"][0] in want]
    # G11 (repair r1): rows of a card cycle through the card's wordings for their form (hashed start), so every card
    # uses all of its >= 5 wordings instead of a per-row hash that could miss one on a small card
    # (a row id keeps the wording it got first, so re-renders of one row, e.g. G4 variants, keep it)
    ctr = card.setdefault("_wdctr", {})
    wmap = card.setdefault("_wdmap", {})
    if (rid, want) not in wmap:
        wi = ctr.get(want, int(uhash(card["card_id"], "wd0", "|".join(want)) * len(wl)))
        ctr[want] = wi + 1
        wmap[(rid, want)] = wi
    wid = wl[wmap[(rid, want)] % len(wl)]
    wording = wid["text"]
    short = spec.get("short", False)
    E = c["entity"]
    if form == "inv":
        labels = [L.INV_REF[int(uhash(card["card_id"], "inv") * 3) % 3].format(i=i + 1) for i in range(len(spec["records"]))]
        q = L.Q_INVERTED[int(uhash(rid, "q") * 3) % 3].format(X=c["names"][spec["ask"]])
        doc = inv_doc(c, spec, labels, typed=st["container"] in ("json", "yaml"))
        options = labels
        gold = labels[spec["gold_idx"]]
        qtype = "choice"
    else:
        u1 = None
        cs_ = c.get("conv_slot")
        # record values only (S6 rows have no record: their U1 restatement is a description rewrite, s6.paraphrase)
        if cs_ is not None and card["sampler"] != "S6" and not c.get("prose_record") \
                and cs_ not in spec.get("omitted", []) and spec.get("u1_try") \
                and u1_ok(c["legend"][cs_], spec["case"][cs_]):
            u1 = cs_
        spec["u1"] = u1
        title = c["rc"]["rec_head"] if card["sampler"] == "S4" else None
        if card["sampler"] == "S6":
            doc = {"title": "Description", "blocks": [{"type": "para", "text": spec["desc_text"]}]}
        else:
            doc = RW.record_doc(c, spec["case"], spec.get("omitted", []), st, u1_slot=u1, extra=extra, title=title)
        if form == "choice":
            q = RW.choice_question(c, int(uhash(rid, "q") * 97))
            # G10 gold letter (repair r1): the stored option order is a seeded shuffle per row (it used to start with
            # the gold term); fmt1 option lines follow this order and the trainer shuffles again at train time
            perm = list(spec["options"])
            random.Random(int(uhash(rid, "optorder") * 2 ** 32)).shuffle(perm)
            spec["options"] = perm
            options = [opt_text(c, o) for o in spec["options"]]
            gold = opt_text(c, spec["gold"])
            qtype = "choice"
        else:
            kind = spec["wkind"]
            if card["sampler"] == "S3":
                kind = "s3_" + kind
            q = RW.yn_question(kind, int(uhash(card["card_id"], rid, "q") * 97), c["names"][spec["ask"]], E,
                               spec.get("neg", 0), spec.get("neg_form", 0))
            options = None
            gold = spec["gold"]
            qtype = "noul"
    fields, ir = RW.place(c, st, doc, q, qtype, options, wording, short)
    row = {"id": rid, "qtype": qtype, "options": options, "gold": gold, **fields}
    res = RW.check(row, ir, q, wording)
    layout = RW.layout_id(card, qtype, form == "inv", short)
    side.update({"style": st["id"], "wording_id": wid["id"], "question": q, "layout": layout, "loader_ok": res["ok"],
                 "loader_problems": res["problems"][:3]})
    return row, side, c
