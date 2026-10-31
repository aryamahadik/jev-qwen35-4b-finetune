"""F11 twins and relation units (G0 section 5): negation units (complement / equiv), attack (inv), inert (equiv),
attr_flip / cut_cross (label flip, own call_id). One relation unit per row (A31, K17); units hold <= 3 rows."""
from __future__ import annotations

import copy

import lex
import items as I
from forms import FormGen
from rows import RowFail
from tax import neighbours_of_cell, PRES


def clone_spec(spec):
    sp = dict(spec)
    if spec.get("item") is not None:
        it = copy.copy(spec["item"])
        it.frames = [dict(f) for f in spec["item"].frames]
        it.inert = list(spec["item"].inert)
        it.exact = dict(spec["item"].exact)
        it.surf = dict(spec["item"].surf)
        it.pform = dict(spec["item"].pform)
        sp["item"] = it
    sp["edge"] = list(spec.get("edge", []))
    return sp


def neg_unit(g: FormGen, base_row, rid, gid, cid):
    """Affirmative base row -> (negated row, double-negated row) with the same state, card, style and wording."""
    out = []
    for nf, kind in ((1, "neg"), (2, "dneg")):
        sp = clone_spec(base_row["_spec"])
        sp["n_frame"] = nf
        row = g.emit(sp, rid=f"{rid}-{kind}", gid=gid, cid=cid, role="twin", twin_of=base_row["id"], twin_kind=kind,
                     style=base_row["_spec"]["style"], wording=base_row["_spec"]["wording"])
        out.append(row)
    rels = [{"a": base_row["id"], "b": out[0]["id"], "type": "complement"},
            {"a": base_row["id"], "b": out[1]["id"], "type": "equiv"}]
    return out, rels


def attack_text(g: FormGen, row):
    r = g.r
    if row["qtype"] == "noul":
        ans = r.choice(("Yes", "No"))
    else:
        opts = [o for o in row["options"] if o not in (lex.NONE_CODES, lex.NONE_REPORTS)]
        ids = [o for o in opts if o in g.card.ids] if g.card.form != "short" else []
        ans = r.choice(ids) if ids and r.random() < 0.6 else r.choice("ABCD"[:min(4, len(row["options"]))])
    t = r.choice(lex.ATTACK_TEMPLATES)
    return t.format(ans=ans)


def attack_twin(g: FormGen, base_row, rid):
    sp = clone_spec(base_row["_spec"])
    if sp.get("item") is None:
        raise RowFail("attack twins only on single-report rows")
    sp["item"].attack = attack_text(g, base_row)
    row = g.emit(sp, rid=rid, gid=base_row["group_id"], cid=base_row["call_id"], role="twin",
                 twin_of=base_row["id"], twin_kind="attack", style=base_row["_spec"]["style"],
                 wording=base_row["_spec"]["wording"])
    if row["gold"] != base_row["gold"] or row["options"] != base_row["options"]:
        raise RowFail("attack twin changed the label")
    return row, {"a": base_row["id"], "b": row["id"], "type": "inv"}


def inert_twin(g: FormGen, base_row, rid):
    sp = clone_spec(base_row["_spec"])
    if sp.get("item") is None:
        raise RowFail("inert twins only on single-report rows")
    new = g.r.choice([s for s in g.inert if s not in sp["item"].inert] or g.inert)
    sents = list(sp["sents"])
    sents.insert(g.r.randrange(len(sents) + 1), {"text": new, "frame": "INERT", "attr": None})
    sp["sents"] = sents
    sp["doc"] = None
    sp["item"].inert.append(new)
    row = g.emit(sp, rid=rid, gid=base_row["group_id"], cid=base_row["call_id"], role="twin",
                 twin_of=base_row["id"], twin_kind="inert", style=base_row["_spec"]["style"],
                 wording=base_row["_spec"]["wording"])
    if row["gold"] != base_row["gold"]:
        raise RowFail("inert twin changed the label")
    return row, {"a": base_row["id"], "b": row["id"], "type": "equiv"}


def flip_twin(g: FormGen, base_row, rid, cid):
    """attr_flip / cut_cross on a taxonomy choice row: one stated focal attribute moves one neighbour step; gold moves
    to a shown member of N(v) (options identical); frames on that attribute are dropped (no echo turns negated)."""
    c, t, r = g.card, g.card.tax, g.r
    sp = clone_spec(base_row["_spec"])
    if sp["form"] != "choice" or sp["none_gold"]:
        raise RowFail("flip twins on taxonomy choice rows with a shown gold")
    it = sp["item"]
    cell = t.resolve_cell(it.cell, it.missing)
    shown = set(sp["shown"])
    cands = []
    for i, c2 in neighbours_of_cell(c.attrs, cell, fixed=it.missing):
        k2 = t.table[c2]
        if k2 != sp["gold_code"] and k2 in shown and g.code_count[k2] < g.cap + 1:
            cands.append((i, c2))
    if not cands:
        raise RowFail("no flip")
    i, c2 = r.choice(cands)
    a = c.attrs[i]
    kind = "attr_flip"
    newcell = list(it.cell)
    newcell[i] = c2[i]
    it.cell = tuple(newcell)
    it.frames = [f for f in it.frames if f["attr"] != i]
    if a.kind in ("num", "date"):
        # cut_cross: from below the cut move to the cut; from at or above move to one grid step below
        up = c2[i] > cell[i]
        lo, hi = a.band_range(c2[i])
        vals = a.grid_values(c2[i])
        it.exact[i] = lo if up else vals[-1]
        kind = "cut_cross"
    elif a.kind == "nom":
        it.surf[i] = I.surface_for(c, i, c2[i], r)
    else:
        it.surf[i] = r.choice(a.terms["attr"])
        it.pform[i] = "has" if c2[i] == PRES else r.choice(("no", "lacks", "without", "denial"))
    sp.pop("sents", None)
    sp["doc"] = None
    sp["gold_code"] = t.table[c2]
    row = g.emit(sp, rid=rid, gid=base_row["group_id"], cid=cid, role="twin", twin_of=base_row["id"],
                 twin_kind=kind, style=base_row["_spec"]["style"], wording=base_row["_spec"]["wording"])
    if row["gold"] == base_row["gold"]:
        raise RowFail("flip did not change the label")
    g.code_count[sp["gold_code"]] += 0
    return row
