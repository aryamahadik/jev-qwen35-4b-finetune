"""Pack adapters: the four pack sets (packs-1..4) normalised to one F2 view, and the F2 train / held-out pack split.

F2 takes from a pack only its setting nouns: organisation, deciding role, persona seed (O*NET code; the pack declares
O*NET as a 3.H parent), the case entity (noun, plural, ID prefix), people, document types, currency, a category
dimension and priced quantity nouns. Numbers, rules and flags are F2's own (the pack range is used for generation only,
never for NEI; 3.5).

Held-out packs (S5 and the depth sweep only, never a training row): the pack agents' own proposals, unioned
(packs-1 heldout_proposal, packs-3 heldout_hint, packs-4 split_hint "heldout"; packs-2 marks none, so the packs-1 rule
sha256(pack id) mod 8 == 0 is applied to it). The orchestrator owns the final held-out ruling; this split is logged in
the manifest as an assumption.
"""
from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache

from .common import PACKS, read_jsonl, safe_path, uhash

GENERIC_QTY = [
    ("hours of service", "hour", "hours"), ("sessions held", "session", "sessions"), ("site visits", "visit", "visits"),
    ("pages processed", "page", "pages"), ("kilometres driven", "km", "km"), ("items shipped", "item", "items"),
    ("days on hire", "day", "days"), ("seats booked", "seat", "seats"), ("call-outs made", "call-out", "call-outs"),
    ("loads moved", "load", "loads"), ("samples tested", "sample", "samples"), ("tonnes handled", "tonne", "tonnes"),
]
GENERIC_CAT = [("service class", ["standard", "express", "economy", "priority"]),
               ("account type", ["basic", "plus", "trade", "partner"]),
               ("region", ["north zone", "south zone", "east zone", "west zone"])]
PRICED_UNITS = {"days", "hours", "h", "items", "people", "kg", "km", "units", "entries", "t", "points", "pages", "nights",
                "visits", "guests", "ha", "pcs", "cycles", "parts", "copies", "covers", "pieces", "parcels", "stops",
                "vehicles", "lifts", "rolls", "seats", "sessions", "claims", "square metres", "forms", "stations",
                "lines", "workers", "L", "m", "miles", "metres", "doors", "comments"}
_BAD_UNIT = re.compile(r"(%|°|/|percent|ratio|score|rank|index|grade|level|count$)", re.I)
_UNIT_OK = re.compile(r"^[A-Za-z][A-Za-z -]{0,18}$")


def _prefix(s: str | None, fallback: str) -> str:
    s = (s or "").strip()
    m = re.match(r"^([A-Z]{2,4})", s)
    if m:
        return m.group(1)
    w = re.sub(r"[^A-Za-z ]", "", fallback).split()
    p = "".join(x[0] for x in w).upper()[:3]
    return (p + "X")[:2] if len(p) < 2 else p


def _clean_unit(u):
    if not u or not isinstance(u, str):
        return None
    u = u.strip()
    if _BAD_UNIT.search(u) or not _UNIT_OK.match(u):
        return None
    return u


def _qtys_from(fields):
    out = []
    for f in fields or []:
        name = f.get("label") or f.get("name") or f.get("word")
        unit = _clean_unit(f.get("unit"))
        t = f.get("type") or f.get("value_type")
        if not name or not unit or not isinstance(name, str):
            continue
        if t not in ("int", "num", "dec1", "integer", "decimal"):
            continue
        name = name.replace("_", " ").strip()
        if len(name) > 32 or not re.match(r"^[a-z][a-z ]+$", name):
            continue
        sg = unit[:-1] if (unit.endswith("s") and len(unit) > 3 and not unit.endswith("ss")) else unit
        out.append((name, sg, unit))
    return out


def _cat_ok(name, values):
    if not name or not isinstance(name, str) or not values or len(values) < 3:
        return False
    if len(name) > 28 or not re.match(r"^[a-z][a-z ]+$", name.strip()):
        return False
    return all(isinstance(v, str) and 1 <= len(v) <= 28 and re.match(r"^[A-Za-z][A-Za-z0-9 '-]*$", v) for v in values)


def _p1(r):
    ent = (r.get("entity_types") or [{}])[0]
    attrs = r.get("attributes") or []
    cat = r.get("scope_dimension") or {}
    return dict(
        id=r["id"], set="packs-1", org=r["org"]["name"], decider=r.get("deciding_role"),
        persona=(r.get("persona_seed") or {}).get("onet_code"), persona_title=(r.get("persona_seed") or {}).get("onet_title"),
        ent_sg=(r.get("item_kind") or {}).get("singular") or ent.get("type"),
        ent_pl=(r.get("item_kind") or {}).get("plural") or ent.get("plural"),
        prefix=_prefix(ent.get("id_prefix"), ent.get("type") or "case"),
        people=list(r.get("people") or []), docs=[d["type"] for d in r.get("document_types") or []],
        currency=None, cat=(cat.get("name"), cat.get("values")), qtys=_qtys_from(attrs), side_money=None, side_date=None)


def _p2(r):
    ent = (r.get("entity_types") or [{}])[0]
    cur = r.get("currency") or {}
    cat = r.get("scope_dimension") or {}
    idf = ent.get("id_format") or {}
    return dict(
        id=r["id"], set="packs-2", org=r.get("org_name"), decider=r.get("decider_role"),
        persona=(r.get("persona_seed") or {}).get("onet_code"), persona_title=(r.get("persona_seed") or {}).get("onet_title"),
        ent_sg=ent.get("singular"), ent_pl=ent.get("plural"), prefix=_prefix(idf.get("prefix"), ent.get("singular") or "case"),
        people=[], docs=list(r.get("document_types") or []), currency=cur.get("unit"),
        cat=(cat.get("name"), cat.get("values")), qtys=_qtys_from(ent.get("attributes")), side_money=None, side_date=None)


def _p3(r):
    ent = (r.get("entity_types") or [{}])[0]
    money = r.get("money") or {}
    cat = r.get("scope_dimension") or {}
    side_m = {"pays": "pays", "paid": "paid"}.get(money.get("decider_side"))
    side_d = {"must act": "must_act", "waits": "waits"}.get(money.get("decider_date_side"))
    return dict(
        id=r["id"], set="packs-3", org=r.get("org"), decider=r.get("decider_role"),
        persona=r.get("persona_seed") if isinstance(r.get("persona_seed"), str) else (r.get("persona") or {}).get("onet_code"),
        persona_title=(r.get("persona") or {}).get("title"),
        ent_sg=ent.get("name"), ent_pl=ent.get("plural"), prefix=_prefix(ent.get("id_prefix"), ent.get("name") or "case"),
        people=list((r.get("names") or {}).get("persons") or []),
        docs=[d.get("name") for d in r.get("document_types") or [] if isinstance(d, dict)],
        currency=money.get("currency"), cat=(cat.get("name"), cat.get("values")), qtys=_qtys_from(ent.get("fields")),
        side_money=side_m, side_date=side_d)


def _p4(r):
    ent = (r.get("entity_types") or [{}])[0]
    cur = r.get("currency") or {}
    persona = r.get("persona") or {}
    cats = [c for c in r.get("cat_fields") or [] if not c.get("ordered")]
    cat = (cats[0]["name"], [v["name"] for v in cats[0]["values"]]) if cats else (None, None)
    units = {u["name"]: u for u in r.get("units") or []}
    qtys = []
    for q in r.get("quantities") or []:
        u = units.get(q.get("unit"))
        if u and q.get("decimals", 0) == 0 and re.match(r"^[a-z][a-z ]+$", q["name"]):
            qtys.append((q["name"], u["name"], u["plural"]))
    return dict(
        id=r["id"], set="packs-4", org=r.get("title"), decider=persona.get("deciding_role"),
        persona=r.get("persona_seed"), persona_title=persona.get("onet_title"),
        ent_sg=ent.get("noun"), ent_pl=ent.get("plural"), prefix=_prefix(ent.get("id_format"), ent.get("noun") or "case"),
        people=[p["name"] for p in (r.get("names") or {}).get("people") or []],
        docs=[d["name"] for d in r.get("documents") or []], currency=cur.get("plural"), cat=cat, qtys=qtys,
        side_money=None, side_date=None)


FIRST = ["Ada", "Bram", "Cleo", "Dov", "Esme", "Faris", "Gita", "Hal", "Ines", "Jory", "Kemi", "Lars", "Mina", "Nils",
         "Oona", "Pavel", "Rhea", "Sol", "Tamsin", "Ugo", "Vida", "Wren", "Yusuf", "Zara"]
LAST = ["Ashdown", "Brackett", "Corwen", "Dunmore", "Ellery", "Fenwick", "Garrow", "Hollins", "Ivers", "Jessop",
        "Kettle", "Lowry", "Marchetti", "Norrell", "Okafor", "Pell", "Quarrie", "Rowntree", "Sefton", "Thorne"]
CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD", "NZD", "CHF", "SGD"]


def _finish(v: dict) -> dict:
    pid = v["id"]
    if not v.get("ent_sg") or not re.match(r"^[A-Za-z][A-Za-z '-]{1,30}$", v["ent_sg"] or ""):
        v["ent_sg"], v["ent_pl"] = "case", "cases"
    v["ent_sg"] = v["ent_sg"].strip()
    v["ent_pl"] = (v.get("ent_pl") or v["ent_sg"] + "s").strip()
    people = [p for p in v.get("people") or [] if isinstance(p, str) and re.match(r"^[A-Z][A-Za-z'-]+( [A-Z][A-Za-z'-]+)+$", p)]
    if len(people) < 6:
        h = int(hashlib.sha256(pid.encode()).hexdigest()[:8], 16)
        people += [f"{FIRST[(h + 7 * i) % len(FIRST)]} {LAST[(h // 7 + 3 * i) % len(LAST)]}" for i in range(8)]
    v["people"] = list(dict.fromkeys(people))
    docs = [d for d in v.get("docs") or [] if isinstance(d, str) and 3 <= len(d) <= 40 and re.match(r"^[A-Za-z][A-Za-z '-]+$", d)]
    v["docs"] = docs or ["case record", "charge sheet", "account statement"]
    cur = v.get("currency")
    if not cur or not re.match(r"^[A-Za-z]{3,12}$", str(cur)):
        cur = CURRENCIES[int(hashlib.sha256((pid + "cur").encode()).hexdigest()[:8], 16) % len(CURRENCIES)]
    v["currency"] = cur
    cname, cvals = v.get("cat") or (None, None)
    if not _cat_ok(cname, cvals):
        g = GENERIC_CAT[int(hashlib.sha256((pid + "cat").encode()).hexdigest()[:8], 16) % len(GENERIC_CAT)]
        cname, cvals = g[0], list(g[1])
    v["cat"] = (cname.strip(), [x.strip() for x in cvals][:6])
    q = [x for x in v.get("qtys") or [] if x[0] and x[2] and (v["set"] == "packs-4" or x[2] in PRICED_UNITS)]
    seen, qq = set(), []
    for x in q + GENERIC_QTY:
        if x[0] in seen:
            continue
        seen.add(x[0])
        qq.append(x)
    v["qtys"] = qq
    if v.get("side_money") is None:
        v["side_money"] = "pays" if uhash("side_money", pid) < 0.5 else "paid"
    if v.get("side_date") is None:
        v["side_date"] = "must_act" if uhash("side_date", pid) < 0.5 else "waits"
    if not v.get("decider"):
        v["decider"] = "case officer"
    if not v.get("org"):
        v["org"] = "the office"
    return v


@lru_cache(maxsize=1)
def all_packs() -> list[dict]:
    out = []
    for path, fn in ((PACKS / "packs-1" / "packs.jsonl", _p1), (PACKS / "packs-2" / "packs.jsonl", _p2),
                     (PACKS / "packs-3" / "packs-3.jsonl", _p3), (PACKS / "packs-4" / "packs.jsonl", _p4)):
        for r in read_jsonl(path):
            out.append(_finish(fn(r)))
    return out


@lru_cache(maxsize=1)
def heldout_ids() -> frozenset:
    ids = set()
    m1 = json.load(open(safe_path(PACKS / "packs-1" / "manifest.json")))
    ids |= set(m1["heldout_proposal"]["ids"])
    for r in read_jsonl(PACKS / "packs-3" / "packs-3.jsonl"):
        if r.get("heldout_hint"):
            ids.add(r["id"])
    for r in read_jsonl(PACKS / "packs-4" / "packs.jsonl"):
        if r.get("split_hint") == "heldout":
            ids.add(r["id"])
    for r in read_jsonl(PACKS / "packs-2" / "packs.jsonl"):
        if int(hashlib.sha256(r["id"].encode()).hexdigest(), 16) % 8 == 0:
            ids.add(r["id"])
    return frozenset(ids)


def split():
    """(training packs, held-out packs), each sorted by a seeded hash so the pick order is fixed."""
    ho = heldout_ids()
    allp = all_packs()
    tr = sorted([p for p in allp if p["id"] not in ho], key=lambda p: uhash("F2-pack-order", p["id"]))
    he = sorted([p for p in allp if p["id"] in ho], key=lambda p: uhash("F2-pack-order", p["id"]))
    return tr, he
