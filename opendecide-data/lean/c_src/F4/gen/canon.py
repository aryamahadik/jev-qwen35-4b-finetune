"""Canonical structure of a sampled row (generator side), in the same form parse_f4.parse_row outputs, plus the
structure hash (2.4 #6: rules, facts, values, links, closures, trust map, claim, form and flag vector, with names
abstracted)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from decimal import Decimal

import core as C


def _v(x):
    if isinstance(x, Decimal):
        return format(x, "f")
    if isinstance(x, dt.date):
        return x.isoformat()
    return x


def qfmt(rec, q, v):
    if v is None:
        return None
    dec = rec.qtys[q]["dec"]
    return format(Decimal(v).quantize(Decimal(1).scaleb(-dec)), "f")


def cond_c(rec, c):
    k = c[0]
    if k == "lit":
        return ["lit", c[1], c[2]]
    if k == "cmp":
        return ["cmp", c[1], c[2], qfmt(rec, c[1], c[3])]
    if k == "rng":
        return ["rng", c[1], qfmt(rec, c[1], c[2]), qfmt(rec, c[1], c[3])]
    if k == "dcmp":
        return ["dcmp", c[1], c[2], c[3].isoformat()]
    if k == "win":
        return ["win", c[1], c[2].isoformat(), c[3].isoformat()]
    raise ValueError(k)


def rule_c(rec, r):
    T = rec.types
    conds = sorted(cond_c(rec, c) for c in r.conds) if r.form != "link" else []
    return [r.form, T[r.typ][0], conds, [r.head[0], r.head[1]], r.ante, r.exc,
            rec.links[r.link]["active"] if r.link is not None else None,
            T[r.ptyp][0] if r.ptyp is not None else None,
            [r.pcond[0], r.pcond[1]] if r.pcond else None, r.k, r.where]


def flags_c(card: C.Card):
    if card.short:
        world, unless = "unspecified", "unspecified"
    else:
        world = card.world
        unless = card.unless if card.unless in ("strict", "listc", "cw") else "none"
    if card.trust and card.trust[0] == "list":
        trust = ["list"] + sorted(card.trust[1])
    elif card.trust and card.trust[0] == "all":
        trust = ["all"]
    else:
        trust = ["unspecified"]
    return {"world": world, "unless": unless, "trust": trust, "clauses": sorted(card.clauses)}


def canon_of(rec: C.Record, card: C.Card, row: dict):
    T = rec.types
    stmts = []
    for s in rec.stmts:
        prov = "attr:" + s.src if s.src is not None else s.via
        if s.kind == "lit":
            stmts.append(["lit", s.pred, s.e, s.pos, prov])
        elif s.kind == "val":
            stmts.append(["val", s.pred, s.e, qfmt(rec, s.pred, s.value), prov])
        elif s.kind == "date":
            stmts.append(["date", s.pred, s.e, s.value.isoformat() if s.value else None, prov])
        elif s.kind == "link":
            stmts.append(["link", rec.links[s.pred]["active"], s.e, s.value, prov])
    form = row["form"]
    out = {
        "flags": flags_c(card),
        "ents": sorted([e, T[t][0]] for e, t in rec.ents.items()),
        "stmts": sorted(stmts, key=lambda x: json.dumps(x, default=str)),
        "blank": sorted([p, e] for p, e, tid in rec.blank_cells),
        "rules": sorted((rule_c(rec, r) for r in rec.rules), key=lambda x: json.dumps(x, default=str)),
        "hedges": sorted([k, T[t][0], [c[0], c[1]], [h[0], h[1]]] for k, t, c, h in rec.hedges),
        "ehedges": sorted([k, e, p] for k, e, p in rec.ehedges),
        "closures": sorted([p, T[t][0], f] for p, t, f, tid in rec.closures),
        "form": form,
        "claim": None, "options": None, "none_shown": bool(row.get("none_shown")), "gold": row["gold_canon"],
    }
    if form.startswith("YN") or form in ("CH-3", "CH-2"):
        out["claim"] = list(row["claim"])
    if form in ("CH-3", "CH-2"):
        out["options"] = list(row["opt_labels"])
    if form == "CH-claim":
        out["options"] = [list(o) if o is not None else None for o in row["options"]]
    if form == "CH-entity":
        out["options"] = list(row["options"])
        out["H"] = row["H"]
        out["etype"] = T[row["etyp"]][0]
    return out


def _norm_json(x):
    return json.loads(json.dumps(x, default=str))


def canon_equal(a, b):
    a, b = _norm_json(a), _norm_json(b)
    for k in ("stmts", "rules", "hedges", "ehedges", "closures", "blank", "ents"):
        a[k] = sorted(a[k], key=lambda x: json.dumps(x))
        b[k] = sorted(b[k], key=lambda x: json.dumps(x))
    return a == b, [k for k in a if a.get(k) != b.get(k)]


def structure_hash(cn):
    """Names abstracted: entity IDs and predicate words replaced by role-ordered placeholders (c's entity and
    predicate first, then by sorted name)."""
    cn = _norm_json(cn)
    ents = [e for e, _ in cn["ents"]]
    preds = set()
    for s in cn["stmts"]:
        if s[0] == "lit":
            preds.add(s[1])
    for r in cn["rules"]:
        preds.add(r[3][0])
        for c in r[2]:
            if c[0] == "lit":
                preds.add(c[1])
        for x in (r[4], r[5]):
            if x:
                preds.add(x)
        if r[8]:
            preds.add(r[8][0])
    first_e, first_p = [], []
    if cn.get("claim"):
        first_p.append(cn["claim"][0])
        first_e.append(cn["claim"][1])
    emap = {e: f"E{i}" for i, e in enumerate(first_e + sorted(set(ents) - set(first_e)))}
    pmap = {p: f"P{i}" for i, p in enumerate(first_p + sorted(preds - set(first_p)))}
    s = json.dumps(cn, sort_keys=True)
    for e in sorted(emap, key=len, reverse=True):
        s = s.replace(json.dumps(e), json.dumps(emap[e]))
    for p in sorted(pmap, key=len, reverse=True):
        s = s.replace(json.dumps(p), json.dumps(pmap[p]))
    return hashlib.sha256(s.encode()).hexdigest()
