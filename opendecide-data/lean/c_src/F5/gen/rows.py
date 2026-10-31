"""Card IR (SEM lines by trigger, full or short form), state Doc IR, fmt1 rendering + loader_check, row meta (2.4),
polarity sidecar records (section 9)."""
from __future__ import annotations

import hashlib
import json

from fmt1 import card as fcard
from fmt1 import pool as fpool
from fmt1.render import FormatError, can_render

from . import sem
from .common import (FAMILY, GEN_VERSION, LICENCE, SEED, SOURCE, SPEC_ID, negc, rng_for, sha, text_lint, uhash)
from .texts import ATTACKS, CARD_TITLES

GIT_SHA = "repo HEAD 18c024c (F5 builder uncommitted; gen code sha256 in MANIFEST)"


def sem_entries(keys, params, variant, *, examples=None):
    """Defs entries for the printed keys, in registry order. Multi-line keys (SEM-17 per value set, SEM-18 per pair)."""
    out = []
    for k in sem.ORDER:
        if k not in keys:
            continue
        if k == "SEM-17":
            for attr, vals, form in params.get("value_sets_full", []):
                key = "SEM-17L" if form == "log" else "SEM-17"
                txt = sem.rendering(key, variant, etype=params.get("etype", ""), item=params.get("item", ""),
                                    attr=attr, values=", ".join(vals))
                out.append((k, f"{sem.TOPIC[k]} ({attr})", txt))
            continue
        if k == "SEM-18":
            for pos, neg in params.get("affixed", []):
                out.append((k, f"{sem.TOPIC[k]} ({pos})", sem.rendering(k, variant, pos=pos, neg=neg)))
            continue
        txt = sem.rendering(k, variant, etype=params.get("etype", ""), S=params.get("S", ""),
                            D_start=params.get("D_start", ""), D_end=params.get("D_end", ""), q=params.get("q", ""),
                            m=params.get("m", ""))
        out.append((k, sem.TOPIC[k], txt))
    return out


def card_ir(card, keys, params, *, short, fewshot_examples=None, inverted_block=None, rng=None):
    """The card for one base. defs style: the card's (one_line / one_line_examples / rubric_table / decision_list);
    short cards use a one_line variant (meta defs_style "short")."""
    variant = card["sem_variant"]
    ents = sem_entries(keys, params, variant)
    if short:
        dv = "DV01" if card["defs_variant"] not in fpool_ids("one_line") else card["defs_variant"]
        style = "one_line"
    else:
        dv, style = card["defs_variant"], card["defs_style"]
    entries = []
    for k, name, txt in ents:
        e = {"name": name, "text": txt}
        if style == "one_line_examples" and params.get("examples", {}).get(k):
            e["examples"] = params["examples"][k][:1]
        if style == "decision_list" and dv in ("DV31", "DV33"):
            e = {"name": None, "text": f"{name}: {txt}"}
        if style == "rubric_table":
            e = {"name": name, "text": txt, "cells": []}
        entries.append(e)
    if style == "decision_list" and dv in ("DV31", "DV33"):
        entries = [{"text": e["text"]} for e in entries]
    blk = {"type": "defs", "variant": dv, "heading": params.get("defs_heading"), "entries": entries}
    if style == "rubric_table":
        blk["columns"] = ["Topic", "Meaning"]
    blocks = []
    if inverted_block:
        blocks += inverted_block
    blocks.append(blk)
    if fewshot_examples:
        blocks.append({"type": "fewshot", "template": card["fewshot_template"], "heading": None,
                       "examples": fewshot_examples})
    title = CARD_TITLES[int(uhash("title", card["card_id"]) * len(CARD_TITLES))]
    return {"title": title, "blocks": blocks}, ("short" if short else card["defs_style"]), dv


def fpool_ids(style):
    return [o["id"] for o in fpool.defs_variants(style)]


def card_styles(card, docs_probe, *, held_out=False):
    """A fixed subset of format styles for the card (label-independent hash pick), each able to render the probe doc."""
    sts = fpool.styles(held_out=held_out)
    ok = [s for s in sts if all(can_render(d, s, allow_null=False) for d in docs_probe)]
    ok = [s for s in ok if s["card_style"] not in card.get("ban_card_styles", ())]
    ranked = sorted(ok, key=lambda s: uhash(card["card_id"], s["id"]))
    return ranked[:8]


def render_row(style, doc, question, wording, gold, card_ir_, row_id):
    fields, res = fcard.render_and_check(style, doc=doc, question=question, qtype="noul", gold=gold, card=card_ir_,
                                         wording=wording, row_id=row_id, seed="f5-loader")
    return fields, res


def attack_text(base_id):
    t = ATTACKS[int(uhash("attack", base_id) * len(ATTACKS))]
    push = "Yes" if uhash("attack-push", base_id) < 0.5 else "No"
    return t.format(X=push), push
