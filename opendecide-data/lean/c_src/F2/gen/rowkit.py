"""Row assembly shared by every engine: style / wording pick, fmt1 render + loader_check, meta (2.4), edge tags (3.8),
and the G3 round-trip check (parse -> canonical problem -> hash and re-solve)."""
from __future__ import annotations

import hashlib
import subprocess
from decimal import Decimal

from . import canon, lex, qtext, solve_b
from .cards import wording_text
from .common import GEN_VERSION, LICENCE, SEED, SPEC_ID, D, LEAN, uhash
from .render import render, can_render, fpool, FormatError

_GIT = None


def git_sha():
    global _GIT
    if _GIT is None:
        try:
            _GIT = subprocess.run(["git", "-C", str(LEAN), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        except Exception:
            _GIT = "unknown"
    return _GIT


SINGLE_BLOCK = {"csv"}


def pick_style(card, row_key, doc_fn):
    """A style from the card's fixed set that can render this row's document (label-independent pick)."""
    order = sorted(card["styles"], key=lambda s: uhash("F2-style", card["card_id"], row_key, s))
    for sid in order:
        st = fpool.style(sid)
        single = st["container"] in SINGLE_BLOCK
        doc = doc_fn(single)
        if can_render(doc, sid):
            return sid, doc
    raise FormatError("no style in the card's set can render this document")


def pick_wording(card, row_key):
    wid = card["wordings"][int(uhash("F2-wording", card["card_id"], row_key) * len(card["wordings"]))]
    return wid, wording_text(wid, gb=card.get("gb", False))


def pick_note(card, row_key, qtype):
    pool = lex.NOTE_YN if qtype == "noul" else lex.NOTE_CH
    return pool[int(uhash("F2-note", card["card_id"], row_key) * len(pool))]


def assemble(card, spec, *, row_id, var, doc_fn, question, qinfo, card_ir_, extra_meta=None, role="clean",
             style_key=None):
    qtype = card["qtype"]
    key = style_key or row_id
    sid, doc = pick_style(card, key, doc_fn)
    wid, wording = pick_wording(card, key)
    note = pick_note(card, key, qtype)
    if qtype == "noul":
        gold = 1 if spec["gold"] else 0
        opts = None
    else:
        gold = spec["gold"]
        opts = spec["options"]
    f, res = render(sid, doc=doc, question=question, qtype=qtype, card_ir_=card_ir_, options=opts or [],
                    wording=wording, note=note, gold=gold if qtype == "choice" else None, row_id=row_id)
    if qtype == "noul":
        # the loader check above ran with gold None; re-run with the real yes/no gold
        from .render import fcard
        row0 = {"id": row_id, "qtype": "noul", "options": None, "gold": gold, **f}
        res = fcard.loader_check(row0, must_show=fcard.must_show(card_ir_, question=question, wording=wording,
                                                                 note=note), check_rows=True)
    k_syn, k_all = qtext.counts(question)
    tags = list(spec.get("tags", []))
    tags += [f"neg:{qinfo.get('neg', 0)}", f"syn:{k_syn}", f"cue:{k_all}", f"tf:{qinfo.get('tf', 0)}",
             f"world:{card['world']}", f"var:{var}", f"sel:{spec.get('sel', 0)}", f"ops:{spec.get('ops', 0)}"]
    if qinfo.get("negcmp"):
        tags.append("negcmp")
    if qinfo.get("pol"):
        tags.append(f"pol:{qinfo['pol']}")
    for k_ in ("m", "b", "s"):
        if card.get(k_):
            tags.append("money:" + ("dec2" if card[k_]["dec2"] else "whole"))
            break
    if "calendar" in f["state"] and card.get("engine") in ("date", "stmt"):
        tags.append("aid:strip")
    if spec.get("group") == "c":
        tags.append("stated_intermediate")
    if card.get("short"):
        tags.append("short_card")
    tags += [f"sem:{d}" for d in spec.get("decisive", [])]
    P = canon.canonize(spec["LP"])
    meta = {"family": "F2", "spec_id": SPEC_ID, "card_id": card["card_id"], "domain_pack": card["pack"],
            "sampler": card["sampler"], "gen_version": GEN_VERSION, "git_sha": git_sha(), "seed": SEED,
            "structure_hash": canon.structure_hash(P), "difficulty_bin": None, "crowd_pg": None,
            "depth": spec.get("depth"), "deep": bool(spec.get("deep")), "format_style": sid, "wording_id": wid,
            "defs_style": card["defs_style"], "twin_of": None, "twin_kind": None, "text_source": None,
            "licence": LICENCE, "edge": sorted(set(tags), key=str)}
    if card.get("persona_seed"):
        meta["persona_seed"] = card["persona_seed"]
    if extra_meta:
        meta.update(extra_meta)
    row = {"id": row_id, "group_id": None, "call_id": None, "source": f"own_F2_{card['sampler']}", "state": f["state"],
           "qtype": qtype, "instructions": f["instructions"], "options": opts if qtype == "choice" else None,
           "gold": gold, "role": role, "card": f.get("card"), "meta": meta}
    return row, res, P


def g3_check(row, P_A, parse_fn):
    """G3: (a) parsed structure hash == A's, (b) re-solve on the parsed problem == the row's gold."""
    probs = []
    try:
        LPp = parse_fn(row)
    except Exception as e:
        return {"ok": False, "problems": [f"parse: {type(e).__name__}: {str(e)[:160]}"]}
    try:
        Pp = canon.canonize(LPp)
    except Exception as e:
        return {"ok": False, "problems": [f"canonize: {type(e).__name__}: {str(e)[:120]}"]}
    if canon.structure_hash(Pp) != canon.structure_hash(P_A):
        diff = [k for k in set(Pp) | set(P_A) if Pp.get(k) != P_A.get(k)]
        probs.append(f"hash: keys differ {sorted(diff)}")
    names = [o["name"] for o in LPp["q"]["outs"]] if LPp.get("q", {}).get("kind") == "outcome" else LPp.get("_names")
    try:
        r = solve_b.solve(Pp, options=row.get("options"), names=names)
    except Exception as e:
        probs.append(f"solve_b: {type(e).__name__}: {str(e)[:120]}")
        return {"ok": False, "problems": probs}
    kind, val = r
    gold = row["gold"]
    if row["qtype"] == "noul":
        if kind != "yn" or (1 if val else 0) != gold:
            probs.append("re-solve label differs")
    else:
        exp = answer_text(row, LPp, kind, val)
        if exp != gold:
            probs.append(f"re-solve answer differs: {exp!r} vs gold")
    return {"ok": not probs, "problems": probs}


def answer_text(row, LPp, kind, val):
    opts = row["options"]
    if kind == "nei":
        cand = [o for o in opts if o in lex.NEI_TEXTS]
        return cand[0] if cand else None
    if kind == "value":
        n, d = val
        v = D(n) / D(d)
        cur = LPp.get("_cur")
        for o in opts:
            parts = o.split(" ")
            if len(parts) == 2 and parts[1] == cur:
                try:
                    if D(parts[0]) == v:
                        return o
                except Exception:
                    pass
        none = [o for o in opts if o.startswith("None of the listed")]
        return none[0] if none else None
    if kind == "outcome":
        return val if val in opts else None
    if kind == "date":
        from .parse_date import parse_date
        for o in opts:
            try:
                if parse_date(o)[0].isoformat() == val:
                    return o
            except Exception:
                continue
        return None
    if kind == "count":
        for o in opts:
            m = o.split(" ")
            if m and m[0].isdigit() and int(m[0]) == val:
                return o
        return None
    if kind == "cases":
        refs = LPp["q"].get("_refs")
        if not val:
            none = [o for o in opts if o.startswith("None of the listed")]
            return none[0] if none else None
        if len(val) != 1:
            return None
        return refs[val[0]]
    return None
