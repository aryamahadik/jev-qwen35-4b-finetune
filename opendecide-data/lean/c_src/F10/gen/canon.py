"""Canonical structure and structure_hash (G0 section 5, AR12, R2-16). Shared by the generator and the parser:
both build the same JSON-able structure from their own reading, and G3 compares the hashes."""
from __future__ import annotations

import hashlib
import json

import model as M


def legend_canon(legend):
    out = []
    for s in sorted(legend):
        a = legend[s]
        e = {"type": a["type"], "d": a.get("d", 0) if a["type"] in ("count", "qty", "amount") else None,
             "conv": (a.get("conv") or {}).get("k")}
        if a["type"] in ("cat", "tag"):
            e["values"] = sorted(a["values"])
        out.append(e)
    return out


def term_ids(defs, order, ctype):
    """Abstract ids: unordered card types -> rank of the canonical definition string; ordered -> card position."""
    if ctype in ("first", "dlist", "codebook"):
        return {t: i for i, t in enumerate(order)}
    canon = {t: M.canon_def(defs, t) for t in order}
    ranked = sorted(order, key=lambda t: canon[t])
    return {t: i for i, t in enumerate(ranked)}


def helper_ids(defs):
    hs = [d for d in defs if defs[d]["helper"]]
    canon = {h: M.canon_def(defs, h) for h in hs}
    return {h: i for i, h in enumerate(sorted(hs, key=lambda h: canon[h]))}


def structure(card_like, query):
    """card_like: {ctype, legend, defs, order, world}; query: {form, wkind, target, neg, shown (option keys), abstain
    flags, case, omitted}. Returns the canonical structure (names abstracted)."""
    defs, order, ct = card_like["defs"], card_like["order"], card_like["ctype"]
    tid = term_ids(defs, order, ct)
    hid = helper_ids(defs)
    dstr = [M.canon_def(defs, t) for t in order]
    if ct not in ("first", "dlist", "codebook"):
        dstr = sorted(dstr)
    hstr = sorted(M.canon_def(defs, h) for h in hid)
    q = dict(query)

    def oid(o):
        if o in ("none", "cbd", "residual"):
            return o
        if isinstance(o, int):
            return o
        return tid.get(o, o)
    q["target"] = oid(q.get("target")) if q.get("target") is not None else None
    q["shown"] = sorted([oid(o) for o in q.get("shown", [])], key=str)
    q["gold"] = None
    return {"ctype": ct, "world": card_like.get("world"), "legend": legend_canon(card_like["legend"]),
            "defs": dstr, "helpers": hstr, "query": q}


def shash(st) -> str:
    return hashlib.sha256(json.dumps(st, sort_keys=True, default=str).encode()).hexdigest()
