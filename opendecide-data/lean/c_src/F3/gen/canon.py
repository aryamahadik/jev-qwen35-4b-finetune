"""structure_hash and leak_key (G3 check 1; spec 7.2 canonical problem; R1-18, R2-03).

structure_hash = sha256 of (facts, stated toggles, query): facts are the opening register, the entries and the gaps;
entity names are replaced by canonical names assigned in a canonical traversal (query entities first, then entries in
effect order, then register-only entities by their field tuple), so the hash does not change with listing order,
container or consistent renaming. The query part holds the question type, decision form, entity references, asked
values, comparator and N, date points, the negated stem form and, for Q7, the candidate items. Options of Q1-Q5,
notes, illustrations and worked examples are not part of it. leak_key keeps the facts and toggles and cuts the query
to (question type, entity references, date points).
"""
from __future__ import annotations

import hashlib
import json

ITEM_SLOTS = ("item",)
HOLDER_SLOTS = ("holder", "sender", "receiver", "absorbed", "survivor")


def _key(S, e):
    sp = S["sampler"]
    if sp == "S6":
        return (e.get("eff") or e["date"], e["n"])
    if sp == "S4":
        return (e["date"], e.get("ref", 0), e.get("k", 0))
    if sp == "S5":
        return (e["n"],)
    return (e["date"], e.get("time") or "", e["n"])


class Namer:
    def __init__(self):
        self.m = {}
        self.cnt = {}

    def name(self, ident, kind):
        if ident is None:
            return None
        if ident not in self.m:
            self.cnt[kind] = self.cnt.get(kind, 0) + 1
            self.m[ident] = f"{kind}{self.cnt[kind]}"
        return self.m[ident]


def canonical(S, toggles, Q, *, coarse=False):
    nm = Namer()
    s4 = S["sampler"] == "S4"
    eid = {}
    for e in S["entries"]:
        eid[e["n"]] = f"{e['ref']}.{e['k']}" if s4 else e["n"]
    if Q:
        for k in ("item",):
            if Q.get(k):
                nm.name(Q[k], "I")
        for k in ("holder",):
            if Q.get(k):
                nm.name(Q[k], "H")
        if Q.get("doc"):
            nm.name(Q["doc"], "D")
        if Q.get("record"):
            nm.name(Q["record"], "R")
        if not coarse:
            for c in sorted(Q.get("candidates") or []):
                nm.name(c, "I")
    ents = sorted(S["entries"], key=lambda e: _key(S, e))
    rows = []
    blank_create = False
    for e in ents:
        r = {"t": e["t"], "n": eid[e["n"]], "date": e["date"], "time": e.get("time"), "eff": e.get("eff")}
        t = e["t"]
        if t == "CREATE":
            r.update(item=nm.name(e["item"], "I"), holder=nm.name(e["holder"], "H"), status=e.get("status"),
                     qty=e.get("qty"))
            if e.get("status") is None:
                blank_create = True
        elif t == "SET":
            r.update(item=nm.name(e["item"], "I"), field=e["field"], value=e["value"])
        elif t == "ADJUST":
            r.update(item=nm.name(e["item"], "I"), sign=e["sign"], amount=e["amount"])
        elif t == "TRANSFER":
            r.update(item=nm.name(e["item"], "I"), sender=nm.name(e["sender"], "H"),
                     receiver=nm.name(e["receiver"], "H"))
        elif t == "VOID":
            r.update(target=eid.get(e["target"], e["target"]))
        elif t == "WITHDRAW":
            r.update(target_ref=e["target_ref"])
        elif t == "CORR":
            v = e["value"]
            if e["slot"] == "receiver":
                v = nm.name(v, "H")
            r.update(target=eid.get(e["target"], e["target"]), slot=e["slot"], value=v)
        elif t == "SUPERSEDE":
            r.update(old=nm.name(e["old"], "R"), new=nm.name(e["new"], "R"))
        elif t == "OPEN":
            r.update(record=nm.name(e["record"], "R"), doc=nm.name(e["doc"], "D"))
        elif t == "RENAME":
            kind = "I" if e["kind"] == "item" else "H"
            r.update(kind=e["kind"], old=nm.name(e["old"], kind), new=nm.name(e["new"], kind))
        elif t == "MERGE":
            r.update(absorbed=nm.name(e["absorbed"], "H"), survivor=nm.name(e["survivor"], "H"))
        rows.append(r)
    reg_items = []
    pending = []
    for item, holder, status, qty in S["register"]["items"]:
        if item in nm.m:
            reg_items.append([nm.name(item, "I"), nm.name(holder, "H"), status, qty])
        else:
            pending.append((item, holder, status, qty))
    pending.sort(key=lambda x: (nm.m.get(x[1], "~"), x[2], -1 if x[3] is None else x[3]))
    for item, holder, status, qty in pending:
        reg_items.append([nm.name(item, "I"), nm.name(holder, "H"), status, qty])
    reg_items.sort()
    docs = sorted([nm.name(d, "D"), nm.name(r, "R")] for d, r in S["register"].get("docs", []))
    gaps = sorted(S.get("gap_refs") or []) if s4 else S.get("gaps", [])
    facts = {"sampler_axis": "eff" if S["sampler"] == "S6" else ("seq" if S["sampler"] == "S5" else
                                                                 ("notice" if s4 else "date")),
             "world": S["world"], "gap_style": S.get("gap_style"), "n0": S.get("n0"), "gaps": gaps,
             "d0": S.get("d0"), "register": reg_items, "docs": docs, "entries": rows,
             "default_status": S.get("default_status") if blank_create else None}
    tg = {k: (toggles or {}).get(k) for k in sorted(toggles or {})}
    q = {}
    if Q:
        pt = None if Q["qt"] in ("Q3", "Q6", "Q7", "Q8") else (Q.get("point") or {"kind": "end"})
        q = {"qt": Q["qt"], "item": nm.m.get(Q.get("item")), "holder": nm.m.get(Q.get("holder")),
             "doc": nm.m.get(Q.get("doc")), "record": nm.m.get(Q.get("record")), "point": pt,
             "entry": eid.get(Q.get("entry")) if Q.get("entry") is not None else None}
        if not coarse:
            q.update(form=Q["form"], value=Q.get("value") if Q["form"] == "yn" else None, cmp=Q.get("cmp"),
                     n=Q.get("n"), neg=Q.get("neg", "A") if Q["form"] == "yn" else None,
                     dbase=Q.get("dbase") if Q.get("neg") == "D" else None, still=bool(Q.get("still")),
                     candidates=sorted(nm.m.get(c) for c in (Q.get("candidates") or [])))
    return {"facts": facts, "toggles": tg, "query": q}


def _h(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def structure_hash(S, toggles, Q):
    return _h(canonical(S, toggles, Q))


def leak_key(S, toggles, Q):
    return _h(canonical(S, toggles, Q, coarse=True))


def toggles_from(stated, slots, *, date_fmt, timed, vocab):
    """The stated toggles (the rule graph) from the statement ids a row's card text carries plus their slot values.
    The generator calls it with the ids it wrote; the parser with the ids it found (B06: only stated toggles)."""
    st = set(stated)
    world = "open" if st & {"T2", "T2c"} else ("closed" if "T1" in st else "unstated")
    gap = None
    for t, v in (("T3x", "explicit"), ("T3x4", "explicit"), ("T3s", "skipped"), ("T3s4", "skipped"),
                 ("T3l", "leading"), ("T3l4", "leading")):
        if t in st:
            gap = v
    if "T6s" in st:
        listing = "eff_sorted"
    elif "T6x" in st:
        listing = "shuffled"
    elif st & {"T42", "T42k"}:
        listing = {"subject": "sorted", "entry number": "chrono", "no particular key": "shuffled"}.get(
            slots.get("key"), "chrono")
    elif "T43" in st:
        listing = {"newest first": "newest_first", "oldest first": "oldest_first"}.get(slots.get("listing"))
    else:
        listing = "default"
    lock = bool(st & {"T19", "T40"})
    return {"rules": sorted(st), "world": world, "gap_style": gap,
            "rename_mode": "alias" if "T14a" in st else ("retire" if "T14r" in st else None),
            "check": bool(st & {"T18", "T40"}), "lock": lock, "lock_status": slots.get("S") if lock else None,
            "listing": listing, "vocab": vocab, "date_fmt": date_fmt, "timed": bool(timed)}


def row_toggles(card, S, stated):
    """Generator side: the toggles of a row from the statement ids its card text carries."""
    key = {"sorted": "subject", "chrono": "entry number", "shuffled": "no particular key"}.get(card.get("listing"))
    lst = {"newest_first": "newest first", "oldest_first": "oldest first"}.get(card.get("listing"))
    return toggles_from(stated, {"S": card.get("lock_status"), "key": key, "listing": lst},
                        date_fmt=card["date_fmt"], timed=any(e.get("time") for e in S["entries"]),
                        vocab=card["vocab"])
