"""Money rows end to end: spec -> text (doc, card, question) -> row (fmt1) -> G3 check."""
from __future__ import annotations

from . import mcard, mdoc, mgen, money, render as R, rowkit
from .common import D
from .mgen import var_sem
from .parse import parse_row


def decisive_dims(card, spec, var):
    """sem:<ID> for each shown dimension whose listed alternative changes the label (2.1 'Decisive')."""
    LP = spec["LP"]
    if spec.get("qkind") == "cases" or LP.get("world") == "open":
        return []
    out = set()
    try:
        base = mgen.lab_of(LP, {})
    except Exception:
        return []
    for eid, rd in mcard.alt_readings(LP, card["shown"] | set(LP["sem"])):
        try:
            if mgen.lab_of(LP, rd) != base:
                d = eid.split(":")[1]
                out.add(d)
        except Exception:
            continue
    return sorted(out)


def card_blocks(card, var):
    """Extra card blocks: the CH-O outcome table, the CL frame sentence."""
    sem = var_sem(card, var)
    blocks = []
    if card["schema"] == "CH-O":
        from . import lex
        b1 = sem.get("B1o", card["b1"])
        blocks.append({"type": "para", "text": lex.fill(lex.OUT_INTRO, res=card["m"]["res"], kind=card["okind"])})
        blocks.append({"type": "items", "items": mcard.outcome_items(card, card["out_disp"], b1)})
    if card["schema"] == "CL" and card.get("frame"):
        from .render import fcard
        blocks.append({"type": "para", "text": fcard.inverted_frame(card["frame"])})
    return blocks


def card_ir_for(card, var):
    sem = var_sem(card, var)
    cl = mcard.clauses(card, sem, card["shown"], card["world"])
    ex = mdoc.fragment_examples(card, sem) if card["defs_style"] == "one_line_examples" else None
    return R.card_ir(card, cl, examples=ex, extra_blocks=card_blocks(card, var), fewshot=card.get("fewshot_block"))


def to_row(card, spec, rng, *, row_id, var=0, eid=None, inert=None, attack=None, role="clean", style_key=None):
    if spec.get("qkind") != "cases" and eid is None:
        raise ValueError("eid")
    q, qinfo = mdoc.question(card, spec, eid, rng)
    spec["decisive"] = decisive_dims(card, spec, var)
    doc_fn = lambda single: mdoc.doc_ir(card, spec, eid, single=single, inert=inert, attack=attack)  # noqa: E731
    cir = card_ir_for(card, var)
    row, res, P = rowkit.assemble(card, spec, row_id=row_id, var=var, doc_fn=doc_fn, question=q, qinfo=qinfo,
                                  card_ir_=cir, role=role, style_key=style_key)
    return row, res, P, q


def build_fewshot(card, rng, n=2):
    """Few-shot card block (R1-29): 1-2 complete short solved rows in the card's own schema, answers as option text
    or Yes / No, generated from fresh structures under the base variant."""
    from .render import fpool
    from . import canon
    exs, hashes = [], []
    tries = 0
    while len(exs) < n and tries < 60:
        tries += 1
        try:
            spec = mgen.gen_row(card, rng, 0, {"neg": 0})
        except Exception:
            continue
        if spec.get("qkind") == "cases":
            return None, []
        eid = f"{card['prefix']}-{rng.randint(1000, 9999)}"
        if spec.get("qkind") in ("thr", "op"):
            spec["tf"] = False
        q, qinfo = mdoc.question(card, spec, eid, rng)
        LP = spec["LP"]
        pairs = mdoc.record_pairs(card, LP, eid) + mdoc.schedule_pairs(card, LP)
        case = "\n".join(f"{k}: {v}" for k, v in pairs) + "\n" + q
        if len(case.split()) > 120:
            continue
        if card["qtype"] == "noul":
            ans = "Yes" if spec["gold"] else "No"
        else:
            ans = spec["gold"]
        exs.append({"case": case, "answer": ans})
        hashes.append(canon.structure_hash(canon.canonize(LP)))
    if not exs:
        return None, []
    tid = rng.choice(["FT01", "FT02", "FT05", "FT11", "FT12", "FT14"])
    return {"type": "fewshot", "template": tid, "examples": exs}, hashes
