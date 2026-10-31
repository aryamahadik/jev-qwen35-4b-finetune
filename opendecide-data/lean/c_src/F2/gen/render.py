"""Render a row spec to the raw row format (2.4) through the formats-1 renderers (CP1: fmt1 card.render_row_text,
then card.loader_check on every row)."""
from __future__ import annotations

import sys

from .common import FMT1, money_str

sys.path.insert(0, str(FMT1))
from fmt1 import card as fcard, pool as fpool, render as frender, labels as flabels  # noqa: E402

BLANK = frender.BLANK
FormatError = frender.FormatError
NAMED_DV = {"one_line": ["DV01", "DV02", "DV03", "DV04", "DV05", "DV06"],
            "one_line_examples": ["DV11", "DV12", "DV13", "DV14", "DV15", "DV16"],
            "decision_list": ["DV31", "DV33", "DV35"], "short": ["DV01", "DV02", "DV03", "DV05"]}


def card_ir(card, clauses, examples=None, extra_blocks=None, fewshot=None):
    """fmt1 card IR: task line, a defs block (one entry per clause), extra blocks (outcome table, CL frame), few-shot."""
    dv = card["dv"]
    v = fpool.defs_variant(dv)
    named = v["style"] != "decision_list" or v.get("named")
    entries = []
    for topic, sid, text in clauses:
        e = {"text": text}
        if named:
            e["name"] = topic
        exs = (examples or {}).get(sid)
        if exs and v["style"] == "one_line_examples":
            e["examples"] = exs[:2]
        entries.append(e)
    blocks = [{"type": "task", "text": card["task"]}]
    blocks.append({"type": "defs", "variant": dv, "heading": card.get("rules_heading"), "entries": entries})
    for b in extra_blocks or []:
        blocks.append(b)
    if fewshot:
        blocks.append(fewshot)
    ir = {"blocks": blocks}
    if card.get("title"):
        ir["title"] = card["title"]
    return ir


def render(style_id, *, doc, question, qtype, card_ir_, options, wording, note, gold, row_id):
    st = fpool.style(style_id)
    f = fcard.render_row_text(st, doc=doc, question=question, qtype=qtype, card=card_ir_, options=options,
                              wording=wording, note=note)
    row = {"id": row_id, "qtype": qtype, "options": list(options) if qtype == "choice" else None, "gold": gold, **f}
    res = fcard.loader_check(row, must_show=fcard.must_show(card_ir_, question=question, wording=wording, note=note),
                             check_rows=True)
    return f, res


def can_render(doc, style_id):
    try:
        frender.render_state(doc, fpool.style(style_id))
        return True
    except FormatError:
        return False
