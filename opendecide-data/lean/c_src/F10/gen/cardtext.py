"""Card-fixed text choices and the card IR (fmt1 blocks) for program cards. The card's sentences are identical on
every row of a card; the row layout only decides where they are printed (L1-L8)."""
from __future__ import annotations

from collections import Counter

import lexicon as L
import model as M
from common import uhash
from render import FAQ_RESTATE_IDS, atom_text, def_text, faq_def_text, pick
from values import date_text, list_text, val_text

DV_PLAIN = ["DV01", "DV02", "DV03", "DV05"]
DV_EX = ["DV12", "DV14", "DV16"]
DV_FMT = {"DV01": "{name}: {text}", "DV02": "{name} = {text}", "DV03": "{name}: {text}", "DV05": "{name} | {text}",
          "DV12": "{name}: {text}", "DV14": "{name} = {text}", "DV16": "{name}: {text}"}
FEWSHOT_TPL = ["FT01", "FT03", "FT05", "FT11", "FT12", "FT14"]
RR_COUNTER = Counter()   # balanced paraphrase choice across cards (G11 fragment caps)


CARD_ORD = [0]


def rr_pick(st_id, n):
    """Balanced, order-independent paraphrase choice: card ordinal + a fixed offset per ST row (G11 caps)."""
    off = int(uhash("rr", st_id) * 1000)
    return (CARD_ORD[0] + off) % n


def marker_text(m):
    return {"not recorded": "'not recorded'", "unknown": "'unknown'", "null": "null",
            "key_left_out": "leaving the attribute out"}[m]


def rule_ids(card):
    """The card's reading-rule rows (fixed per card; G0 section 9 triggers)."""
    s, ct = card["sampler"], card["ctype"]
    leg, defs = card["legend"], card["defs"]
    out = ["ST1"] + (["ST1_S4"] if s == "S4" else []) + ["ST2", "ST3_S3" if s == "S3" else "ST3", "ST25", "ST33"]
    if s != "S6":
        out += ["ST6", "ST48"]
        out.append("ST5" if card["world"] == "open" else "ST4")
    out += {"amo": ["ST27"], "partition": ["ST27b"], "first": ["ST28", "ST49"], "dlist": ["ST28_S3", "ST49_S3"],
            "desc": ["ST43"]}[ct]
    if s == "S3":
        out.append("ST51")
    if ct in ("amo", "first"):
        out.append("ST29")
    if ct == "dlist":
        out.append("ST29_S3")
    if card["world"] == "open" and ct in ("amo", "first", "dlist"):
        out.append("ST29b")
    if card.get("conseq"):
        out.append("ST52")
    if (ct == "amo" and s in ("S1", "S2")) or s == "S6":
        out.append("ST54")
    if card.get("lookalike"):
        out.append("ST34")
    if card["mode"] == "neutral":
        out.append("ST36")
    if card.get("examples") or card.get("fewshot"):
        out.append("ST37_S3" if s == "S3" else "ST37")
    # construct rows
    atoms = [a for d in defs.values() for a in M.walk_atoms(d)]
    forms = {d["body"]["form"] for d in defs.values()}
    has = lambda f: any(f(a) for a in atoms)
    if any(i["k"] == "item" and i.get("unless") is not None for d in defs.values() for i in d["body"]["items"]):
        out.append("ST7")
    if has(lambda a: a["t"] == "cat" and a.get("style") in ("other", "except")):
        out.append("ST8")
    if any(d.get("onlyif") is not None for d in defs.values()):
        out.append("ST9")
    if forms & {"ALL", "ANY", "NOTANY", "NOTALL"}:
        out.append("ST10")
    if "XOR" in forms:
        out.append("ST12")
    if "NEITHER" in forms:
        out.append("ST13")
    num = lambda a: leg[a["a"]]["type"] in ("count", "qty", "amount")
    if has(lambda a: a["t"] == "cmp" and num(a) and a["op"] == "ge"):
        out.append("ST14")
    if has(lambda a: a["t"] == "cmp" and num(a) and a["op"] == "le"):
        out.append("ST15")
    if has(lambda a: a["t"] == "cmp" and num(a) and a["op"] == "gt"):
        out.append("ST16")
    if has(lambda a: a["t"] == "cmp" and num(a) and a["op"] == "lt"):
        out.append("ST17")
    if has(lambda a: a["t"] == "rng" and num(a)):
        out.append("ST18")
    if has(lambda a: a["t"] == "rng" and not num(a)):
        out.append("ST20")
    if has(lambda a: a["t"] == "cmp" and leg[a["a"]]["type"] == "date"):
        out.append("ST21")
    if has(lambda a: a["t"] == "rel"):
        out.append("ST22")
    if any(not defs[r["to"]]["helper"] for d in defs.values() for r in M.walk_refs(d)):
        out.append("ST30")
    if any(d.get("exc") is not None for d in defs.values()):
        out.append("ST31")
    if card.get("scoped"):
        out.append("ST32")
    if has(lambda a: a["t"] == "tag"):
        out.append("ST39")
    if has(lambda a: a["t"] == "tag" and a["m"] in ("atl", "atlof")):
        out.append("ST40")
    if any(a["type"] == "date" for a in leg.values()):
        out.append("ST23")
    if any(a["type"] in ("amount", "qty") for a in leg.values()):
        out.append("ST24")
    if card.get("conv_slot") is not None:
        out.append("ST26")
    return out


def fill(card, s):
    rc = card["rc"]
    rep = {"{E}": card["entity"], "{doc}": rc.get("doc", "document"), "{M}": marker_text(rc["marker"]),
           "{CBD}": rc["cbd"], "{NONE}": rc["none"], "{T}": "given term", "{F}": rc["date_fmt_text"],
           "{S}": "A", "{W}": (card["helper_words"][0] if card["helper_words"] else "")}
    leg = card["legend"]
    cur = next((a["currency"] for a in leg.values() if a["type"] == "amount"), None)
    rep["{CUR}"] = L.ST["ST25_CUR"][rc["cur_i"]].replace("{cur}", cur) if cur else ""
    if card.get("lookalike"):
        rep["{A}"], rep["{B}"] = card["lookalike"]
    if card.get("conv_slot") is not None:
        a = leg[card["conv_slot"]]
        rep["{u1}"], rep["{u2}"], rep["{k}"] = a["conv"]["u1"], a["unit"], str(a["conv"]["k"])
        rep["{u1s}"] = L.SINGULAR.get(a["conv"]["u1"], a["conv"]["u1"])
    if card.get("scoped"):
        rep["{W}"] = card["names"][card["scoped"]]
    for k, v in rep.items():
        s = s.replace(k, v)
    return s


def legend_lines(card):
    rc = card["rc"]
    fr = L.ST19[rc["legend_set"]]
    out = []
    for s in sorted(card["legend"]):
        a = card["legend"][s]
        t = a["type"]
        u = a.get("unit") or "units"
        out.append(fr[t].format(a=a["name"], u=u, d=a["d"], cur=a.get("currency") or "", V=list_text(a.get("values") or [])))
    return out


def prepare_card(card, r, pack, styles_by_marker, wordings):
    """Card-fixed text choices (rc), polarity tags, consequence lines; examples and few-shot come after."""
    s = card["sampler"]
    CARD_ORD[0] = card.get("ordinal", 0)
    rc = {}
    rc["date_fmt"], rc["date_fmt_text"] = r.choice(L.DATE_FORMATS)
    rc["legend_set"] = rr_pick("ST19", len(L.ST19))
    rc["legend_head"] = r.choice(L.LEGEND_HEAD)
    rc["persona"] = r.choice(L.PERSONA)
    ttl = (pack.get("persona_title") or "reviewer").split(",")[0].strip().lower()
    ttl = ttl[:-1] if ttl.endswith("s") and not ttl.endswith("ss") else ttl
    rc["persona_text"] = rc["persona"].replace("a {title}", ("an " if ttl[:1] in "aeiou" else "a ") + "{title}").format(title=ttl,
                                              plural=card["entity_plural"], org=pack.get("org") or "the office")
    rc["ft"] = r.choice(FEWSHOT_TPL)
    rc["fs_head"] = r.choice(L.FEWSHOT_HEAD)
    rc["sec_head"] = r.choice(L.S4_SECTION_HEADING)
    rc["rec_head"] = r.choice(L.S4_RECORD_HEADING)
    rc["defs_heading"] = r.choice(L.DEFS_HEADING)
    rc["none"] = r.choice(L.NONE_TEXT_S3 if s == "S3" else L.NONE_TEXT)
    rc["cbd"] = r.choice(L.CBD_TEXT)
    rc["cur_i"] = r.randrange(len(L.ST["ST25_CUR"]))
    rc["doc"] = r.choice(pack["doc_types"]) if pack["doc_types"] else "policy note"
    rc["line_form"] = False
    if s == "S3":
        rc["dv"] = None
    else:
        rc["dv"] = r.choice(DV_EX if card.get("examples_on") else DV_PLAIN)
    # one omission marker per card (ST5 names it; every row style of the card uses it)
    markers = [m for m in styles_by_marker if styles_by_marker[m]]
    if s in ("S4", "S6") or card.get("prose_record"):
        okc = ("prose", "memo") if s == "S6" else ("prose", "memo", "bullet_sop")
        markers = [m for m in markers if any(x["container"] in okc for x in styles_by_marker[m])]
    if card["world"] == "open":
        rc["marker"] = r.choice(markers)
    else:
        rc["marker"] = r.choice([m for m in ("not recorded", "unknown") if m in markers] or markers)
    pool = styles_by_marker[rc["marker"]] if card["world"] == "open" else [x for m in markers for x in styles_by_marker[m]]
    if s == "S4" or card.get("prose_record"):
        pool = [x for x in pool if x["container"] in ("prose", "memo", "bullet_sop")]
    if s == "S6":
        pool = [x for x in pool if x["container"] in ("prose", "memo")]
    r.shuffle(pool)
    rc["styles"] = [x["id"] for x in pool[:12]]
    anyw = [w for w in wordings if w["forms"] == ["any"]]
    rc["wordings"] = r.sample(anyw, r.choice([4, 5])) + r.sample([w for w in wordings if w["forms"] == ["yn"]], 1) + \
        r.sample([w for w in wordings if w["forms"] == ["choice"]], 1)
    card["rc"] = rc
    # polarity tags split evenly per card (SC3)
    order = card["order"]
    tags = ["bad", "not bad"] * (len(order) // 2 + 1)
    r.shuffle(tags)
    card["polarity"] = {t: tags[i] for i, t in enumerate(order)}
    if card.get("conseq_on"):
        bad = [o["name"] for o in pack["outcomes"] if o["bad"]] or ["sent back"]
        good = [o["name"] for o in pack["outcomes"] if not o["bad"]] or ["accepted"]
        fr = r.choice(L.CONSEQ)
        card["conseq"] = {t: fr.format(T=card["names"][t], O=r.choice(bad if card["polarity"][t] == "bad" else good))
                          for t in order}
    else:
        card["conseq"] = None
    rids = rule_ids(card)
    card["rules"] = [(i, rr_pick(i, len(L.ST[i]))) for i in rids]
    card["rule_text"] = [fill(card, L.ST[i][j]) for i, j in card["rules"]]
    return card


def add_examples(card, r):
    """In-definition examples on cards with examples_on (1-2 per term; AR02)."""
    from examples import example_for, one_line
    from solver_b import CardB
    from cardgen import draw_ranges
    card["examples"] = {}
    if not card.get("examples_on"):
        return
    cb = CardB(card["legend"], card["defs"], card["order"], card["ctype"])
    draw = draw_ranges(card["legend"])
    tpl = L.EXAMPLE_S3 if card["sampler"] == "S3" else L.EXAMPLE
    for t in card["order"]:
        exs = []
        for _ in range(1):          # R2-25 trim lever 2: one in-definition example per illustrated term
            res = example_for(card, cb, t, r, draw)
            if res is None:
                continue
            stated, case = res
            txt = tpl.format(R=one_line(card, stated, case), T=card["names"][t])
            if txt not in [e["text"] for e in exs]:
                exs.append({"text": txt, "stated": stated, "case": {str(k): v for k, v in case.items()}})
        card["examples"][t] = exs


def gloss_entries(card, line_form=False):
    out = []
    restate = [txt for (i, _), txt in zip(card["rules"], card["rule_text"]) if i in FAQ_RESTATE_IDS]
    for t in card["order"]:
        if card.get("faq"):
            e = {"name": card["names"][t], "text": faq_def_text(card, t, restate)}
        else:
            e = {"name": card["names"][t], "text": def_text(card, t, line_form=line_form)}
        exs = [x["text"] for x in card.get("examples", {}).get(t, [])]
        if exs:
            e["examples"] = exs
        out.append(e)
    return out


def _items_from_entries(card, entries):
    dv = card["rc"]["dv"]
    fmt = DV_FMT.get(dv, "{name}: {text}")
    items = []
    for e in entries:
        line = fmt.format(name=e["name"], text=e["text"])
        exs = e.get("examples") or []
        if exs and dv == "DV12":
            line += " (e.g. " + "; ".join(exs) + ")"
            items.append(line)
        else:
            items.append(line)
            items += [L.EXAMPLE_FRAME.format(X=x) for x in exs]
    return items


def table_block(card):
    """S3 code table (ALL-only rows; ST51): code, one column per conditioned attribute, rule column."""
    from render import atom_text
    leg, defs = card["legend"], card["defs"]
    cols = sorted({i["atom"]["a"] for d in defs.values() for i in d["body"]["items"]})
    rows = []
    for t in card["order"]:
        d = defs[t]
        cell = {}
        for i in d["body"]["items"]:
            sl = i["atom"]["a"]
            txt = atom_text(card, i["atom"], (t, "c", sl))
            nm = leg[sl]["name"] + " "
            cell[sl] = txt[len(nm):] if txt.startswith(nm) else txt
        rule = []
        if d.get("onlyif") is not None:
            rule.append(L.RULE_ONLYIF.format(C=atom_text(card, d["onlyif"], (t, "o"))))
        if d.get("exc") is not None:
            rule.append(L.RULE_EXC.format(B=atom_text(card, d["exc"], (t, "e"))))
        rows.append([card["names"][t]] + [cell.get(s, L.TABLE_ANY) for s in cols] + ["; ".join(rule) or L.RULE_NONE])
    return {"type": "table", "caption": None, "columns": ["code"] + [leg[s]["name"] for s in cols] + ["rule"],
            "rows": rows}, cols


def fewshot_block(card):
    fs = card.get("fewshot")
    if not fs:
        return None
    return {"type": "fewshot", "template": card["rc"]["ft"], "heading": card["rc"]["fs_head"],
            "examples": [{"case": x["case_text"], "answer": x["answer"]} for x in fs]}


def memo_blocks(card):
    """S4: the definitions document is the card: helper overrides, term definitions, optional sections (ST32)."""
    rc = card["rc"]
    defs = card["defs"]
    doc = rc["doc"]
    lf = rc.get("line_form", False)
    fmt = DV_FMT.get(rc["dv"], "{name}: {text}")

    def helper_line(h):
        d = defs[h]
        body = def_text(card, h, line_form=False)
        if d.get("section"):
            return L.HELPER_SCOPED.format(S=d["section"], W=card["names"][h], B=body[:-1])
        if card.get("scoped") == h:
            return L.HELPER_ELSE.format(doc=doc, W=card["names"][h], B=body[:-1])
        return L.HELPER.format(doc=doc, W=card["names"][h], B=body[:-1])

    def term_lines(t):
        e = {"name": card["names"][t], "text": def_text(card, t, line_form=lf)}
        exs = [x["text"] for x in card.get("examples", {}).get(t, [])]
        if exs:
            e["examples"] = exs
        return _items_from_entries(card, [e])
    helpers = [h for h in defs if defs[h]["helper"]]
    outside_h = [helper_line(h) for h in helpers if not defs[h].get("section")]
    sec_h = [helper_line(h) for h in helpers if defs[h].get("section") == "A"]
    out_terms = [x for t in card["order"] if not defs[t].get("section") for x in term_lines(t)]
    sec_terms = [x for t in card["order"] if defs[t].get("section") == "A" for x in term_lines(t)]
    if card.get("scoped") or sec_terms:
        hd = rc.get("sec_head", "Section {S}")
        blocks = [{"type": "para", "text": x} for x in outside_h]
        if out_terms:
            blocks.append({"type": "items", "items": out_terms})
        blocks.append({"type": "section", "heading": hd.format(S="A"),
                       "blocks": [{"type": "para", "text": x} for x in sec_h] + ([{"type": "items", "items": sec_terms}] if sec_terms else [])})
        return blocks
    return [{"type": "para", "text": x} for x in outside_h] + [{"type": "items", "items": out_terms}]


def card_ir(card, gloss_mode="defs"):
    """fmt1 card IR. gloss_mode 'defs' = a definition-style block (option-routed on L2 rows); 'items' = the same
    sentences as plain items (L3 / L5 / L7: nothing may become an option line)."""
    rc = card["rc"]
    blocks = [{"type": "para", "text": rc["persona_text"]},
              {"type": "para", "text": rc["legend_head"].format(E=card["entity"])},
              {"type": "items", "items": legend_lines(card)}]
    s = card["sampler"]
    if s == "S3":
        tb, _ = table_block(card)
        blocks.append(tb)
        exs = [L.EXAMPLE_FRAME.format(X=x["text"]) for t in card["order"] for x in card.get("examples", {}).get(t, [])]
        if exs:
            blocks.append({"type": "items", "items": exs})
    elif s == "S4":
        blocks += memo_blocks(card)
    else:
        ents = gloss_entries(card)
        if gloss_mode == "defs":
            blocks.append({"type": "defs", "variant": rc["dv"], "heading": None, "entries": ents})
        else:
            blocks.append({"type": "items", "items": _items_from_entries(card, ents)})
    fb = fewshot_block(card)
    if fb:
        blocks.append(fb)
    if card.get("conseq"):
        blocks.append({"type": "items", "items": [card["conseq"][t] for t in card["order"]]})
    blocks.append({"type": "items", "items": list(card["rule_text"])})
    title = rc["doc"].capitalize() if s == "S4" else None
    out = {"blocks": blocks}
    if title:
        out["title"] = title
    return out
