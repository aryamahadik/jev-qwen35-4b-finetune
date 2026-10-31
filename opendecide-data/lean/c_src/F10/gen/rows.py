"""F10 row assembly: record Doc IR (state), question and options, layout L1-L8 through fmt1, loader_check.
`state` holds only the row's input (record, description, inverted records, S7 coded text)."""
from __future__ import annotations

from decimal import Decimal

import lexicon as L
from cardtext import card_ir
from common import uhash
from fmt1 import card as fcard
from fmt1 import pool
from fmt1.render import OMIT, FormatError
from values import val_text

TABLE_CT = ("csv", "markdown_table", "html_snippet")
TYPED_CT = ("json", "yaml")
PROSE_CT = ("prose", "memo", "bullet_sop")


def marker_value(marker, typed):
    if marker == "key_left_out":
        return OMIT
    if marker == "null":
        return None
    return marker


def statement(card, s, v, eref):
    a = card["legend"][s]
    st = a["lex"]["statements"]
    if a["type"] == "flag":
        tpl = st.get("positive") if v else st.get("negative")
    elif a["type"] == "tag" and not v:
        tpl = st.get("none")
    else:
        tpl = st.get("value")
    if not tpl:
        return None
    return tpl.replace("{E}", eref).replace("{v}", val_text(a, v, card)) + "."


def record_doc(card, case, omitted, style, u1_slot=None, extra=None, title=None):
    """The case as a Doc in the style's container. extra: attack / inert sentences (para) inside the record."""
    ct = style["container"]
    leg = card["legend"]
    marker = card["rc"]["marker"]
    slots = sorted(leg)
    title = title or card["entity"].capitalize()

    def txt(s):
        if s in omitted:
            return marker_value(marker, ct in TYPED_CT)
        a = leg[s]
        v = case[s]
        if a["type"] == "flag" and ct in TYPED_CT:
            return bool(v)
        return val_text(a, v, card, conv_u1=(s == u1_slot))
    if ct in TABLE_CT:
        blocks = [{"type": "table", "caption": None, "columns": [leg[s]["name"] for s in slots],
                   "rows": [[txt(s) for s in slots]]}]
    elif card.get("prose_record") and ct in PROSE_CT:
        sents = []
        eref = L.ENTITY_REF[int(uhash(card["card_id"], "eref") * 2) % 2].format(E=card["entity"])
        for s in slots:
            if s in omitted:
                if marker == "key_left_out":
                    continue
                sents.append(L.OMIT_STMT[int(uhash(card["card_id"], "om") * 2) % 2].format(a=leg[s]["name"], E=card["entity"], M=marker))
            else:
                x = statement(card, s, case[s], eref)
                if x is None:
                    raise FormatError("no statement template")
                if s == u1_slot:
                    raise FormatError("no U1 values in templated prose")
                sents.append(x)
        blocks = [{"type": "para", "text": " ".join(sents)}]
    else:
        blocks = [{"type": "fields", "label": None, "pairs": [[leg[s]["name"], txt(s)] for s in slots]}]
    if extra:
        blocks.append({"type": "para", "text": " ".join(extra)})
    return {"title": title, "blocks": blocks}


def style_ok_for(card, style, need_para=False):
    ct = style["container"]
    if need_para and ct not in ("prose", "memo", "bullet_sop", "json", "yaml", "markdown_table", "html_snippet"):
        return False
    if card.get("prose_record") and ct not in PROSE_CT:
        return False
    if card["sampler"] == "S6" and ct not in ("prose", "memo"):
        return False
    return True


def yn_question(kind, tpl_i, X, E, neg, neg_form=0):
    q, pos, negc = L.Q_YN[kind][tpl_i % len(L.Q_YN[kind])]
    f = lambda s: s.format(X=X, E=E)
    if neg == 0:
        return f(q)
    if neg == 1:
        return L.TRUTH_POS[0].format(C=f(negc)) if neg_form == 0 else L.TRUTH_NEG[0].format(C=f(pos))
    return L.TRUTH_NEG[0].format(C=f(negc))


def choice_question(card, tpl_i):
    key = {"S3": "s3", "S6": "s6", "S7": "s7"}.get(card["sampler"], "prog")
    pool_ = L.Q_CHOICE[key]
    return pool_[tpl_i % len(pool_)].format(E=card["entity"])


def gloss_mode(card):
    return "defs" if (card["ctype"] == "amo" and card["sampler"] in ("S1", "S2")) or card["sampler"] == "S6" else "items"


def layout_id(card, qtype, inverted, short):
    if short:
        return "L8"
    if qtype == "noul":
        return "L1"
    if inverted:
        return "L7"
    s = card["sampler"]
    if s == "S3":
        return "L4"
    if s == "S4":
        return "L5"
    if s == "S7":
        return "L6"
    if s == "S6" or card["ctype"] == "amo":
        return "L2"
    return "L3"


def place(card, style, doc, question, qtype, options, wording, short, ir=None):
    """fmt1 placement by layout; returns (fields, ir, layout)."""
    st = pool.style(style) if isinstance(style, str) else style
    ir = ir or card_ir(card, gloss_mode(card))
    an = card.get("rc", {}).get("marker") == "null"
    if short:
        from fmt1.render import render_state
        text = card["rc"]["defs_heading"] + "\n" + fcard.render_card(ir, st)
        fields = {"state": render_state(doc, st, allow_null=an),
                  "instructions": fcard.render_instructions(st, question=question, wording=wording, card_text=text),
                  "card": None}
    else:
        fields = fcard.render_row_text(st, doc=doc, question=question, qtype=qtype, card=ir,
                                       options=options if qtype == "choice" else None, wording=wording,
                                       allow_null=an)
    return fields, ir


def check(row, ir, question, wording):
    """G15 per-row: fmt1 loader_check (must_show, gold letter under a random permutation, train_decoder.check_rows on
    the pinned A16 trainer; the trainer is restored to git HEAD c2c2d1d6, TRAINER_INCIDENT)."""
    return fcard.loader_check(row, must_show=fcard.must_show(ir, question=question, wording=wording))
