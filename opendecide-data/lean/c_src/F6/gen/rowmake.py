"""Row assembly: card-variant switch sets (fixed per card variant, never per row), card IR, fmt1 render_and_check,
the 2.4 row format and the QC side record.
"""
from __future__ import annotations

from . import common  # noqa: F401  (sys.path for fmt1)

import json

from fmt1 import card as fcard, pool as fpool
from fmt1.render import FormatError

from .common import FAMILY, SPEC_ID, GEN_VERSION, LICENCE, SOURCE, sha256_text, canon, iso
from .lex import sw, SW, join_or, join_and, FRAMES, FRAME_SWITCH, OPTION_TEXT
from . import render_f6 as RF


# ---------------------------------------------------------------- switch sets (section 3 core rows)

def world_lines(V: dict, D: int, ds: str) -> list[str]:
    """World group (rows 1/2/3 + row 5 variant + row 27 closed addition)."""
    Dt = RF.fmt_date(D, ds)
    out = []
    w = V["world"]
    if w == "open":
        out.append(sw("r1"))
        out.append(sw("r5_open"))
    elif w == "closed":
        evs = [f'"{e}" event' for e in V.get("event_names", [])]
        out.append(sw("r2", D=Dt, events=join_or(evs)) if evs else sw("r2_noev", D=Dt))
        types = [f'"{e}" events' for e in V.get("event_names", [])] + (["list membership"] if V.get("has_lists")
                                                                         else [])
        out.append(sw("r5_closed", types=join_and(types)) if types else sw("r5_open"))
        if V.get("plans"):
            out.append(sw("r27_closed"))
    else:
        out.append(sw("r3", section=V["local_section"], thing=V["local_thing"], D=Dt))
        out.append(sw("r5_closed", types=f"membership of the list under {V['local_section']}"))
    return out


def marker_lines(V: dict) -> list[str]:
    if V.get("s5"):
        return [sw("s5_markers"), sw("s5_ev"), sw("r27")]
    clause = ", even where this record is complete" if V["world"] != "open" else ""
    out = []
    if V.get("blank"):
        out.append(sw("r4_blank", m1=V["marker"]))
    else:
        out.append(sw("r4_1", m1=V["marker"], clause=clause))
    if V.get("event_lines"):
        out.append(sw("r4_ev", m=V["marker"]))
    return out


def evidence_lines(V: dict) -> list[str]:
    t = V.get("ev_tag")
    if not t:
        return []
    clause = ", even where this record is complete" if V["world"] != "open" else ""
    if t["counts"]:
        return [sw("r26_count", tag=RF.cap(t["tag"]))]
    return [sw("r26_not", tag=t["tag"], clause=clause)]


def abstain_lines(V: dict) -> list[str]:
    out = []
    if V.get("nei"):
        out.append(sw("r33", NEI=V["nei"]))
    if V.get("none"):
        out.append(sw("r34", NONE=V["none"]))
    if V.get("nei") and V.get("none"):
        out.append(sw("r35", NEI=V["nei"], NONE=V["none"]))
    if V.get("nei") or V.get("none"):
        out.append(sw("r50"))
    return out


def frame_lines(V: dict) -> list[str]:
    return [sw(FRAME_SWITCH[f]) for f in V.get("frames", []) if f in FRAME_SWITCH]


# ---------------------------------------------------------------- the card IR

def example_blocks(card: dict, H: dict) -> list:
    """The card's definition examples and few-shot worked examples (repair r1), one 'Examples' section."""
    items = list(card.get("examples") or []) + list(card.get("fewshot") or [])
    if not items:
        return []
    return [{"type": "section", "heading": H.get("examples") or "Examples", "blocks": [{"type": "items", "items": items}]}]


def card_ir(sections: list) -> dict:
    return {"blocks": [s for s in sections if s]}


def reading_section(heading: str, lines: list[str]) -> dict:
    return {"type": "section", "heading": heading, "blocks": [{"type": "items", "items": lines}]}


def headings(style: dict) -> dict:
    reg = fpool.register(style["register"])
    return reg["headings"]


# ---------------------------------------------------------------- rendering and the 2.4 row

def render(style: dict, doc: dict, question: str, qtype: str, gold, card: dict, options: list | None,
           wording: str, rid: str, allow_null: bool = False):
    """fmt1 render + loader_check (check_rows on the pinned A16 trainer, fmt1._td)."""
    f = fcard.render_row_text(style, doc=doc, question=question, qtype=qtype, card=card, options=options,
                              wording=wording, note=None, allow_null=allow_null, choice_card="move")
    row = {"id": rid, "qtype": qtype, "options": list(options) if qtype == "choice" else None, "gold": gold, **f}
    res = fcard.loader_check(row, must_show=fcard.must_show(card, question=question, wording=wording, note=None),
                             seed="fmt1-loader", raise_on_fail=True)
    return f, res


def make_row(*, rid, group_id, call_id, fields, qtype, options, gold, role, meta) -> dict:
    return {"id": rid, "group_id": group_id, "call_id": call_id, "source": SOURCE, "state": fields["state"],
            "qtype": qtype, "instructions": fields["instructions"], "options": options, "gold": gold, "role": role,
            "card": fields.get("card"), "meta": meta}


META_KEYS = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
             "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
             "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge", "persona_seed", "subtype"]


def make_meta(*, card_id, pack, sampler, seed, structure_hash, depth, deep, format_style, wording_id, defs_style,
              twin_of, twin_kind, edge, persona_seed, subtype, git_sha) -> dict:
    m = {"family": FAMILY, "spec_id": SPEC_ID, "card_id": card_id, "domain_pack": pack, "sampler": sampler,
         "gen_version": GEN_VERSION, "git_sha": git_sha, "seed": seed, "structure_hash": structure_hash,
         "difficulty_bin": None, "crowd_pg": None, "depth": depth, "deep": deep, "format_style": format_style,
         "wording_id": wording_id, "defs_style": defs_style, "twin_of": twin_of, "twin_kind": twin_kind,
         "text_source": None, "licence": LICENCE, "edge": edge, "subtype": subtype}
    if persona_seed:
        m["persona_seed"] = persona_seed
    return m


def structure_hash(struct: dict) -> str:
    """Names abstracted: the symbolic structure (ids, numbers, days, world, gaps), never surface names."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k not in ("name", "plural", "case_noun", "vals_names")}
        if isinstance(o, (list, tuple)):
            return [strip(x) for x in o]
        return o
    return sha256_text(canon(strip(struct)))[:32]
