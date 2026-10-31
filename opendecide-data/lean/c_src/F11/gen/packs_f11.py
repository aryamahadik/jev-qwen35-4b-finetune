"""F11 view of the shared domain packs (spec 2.1; XF09 one pack per card; persona seed from O*NET, 2.1 F4).

Program cards (S1-S4, S6) use packs-4 train packs; S7 card wrappers use packs-3 non-held-out packs; S5 uses only
held-out packs (packs-4 split_hint 'heldout' for the program arm, packs-3 heldout_hint True for the codebook arm), so no
S5 pack is ever a training pack. Every string the generator takes from a pack passes the reserved-word check.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from common import PACKS, sha256_file, toks
from names import name_ok

P4 = PACKS / "packs-4" / "packs.jsonl"
P3 = PACKS / "packs-3" / "packs-3.jsonl"
_WORD = re.compile(r"^[a-z][a-z ]*[a-z]$")


def _ok_phrase(s: str, max_words: int = 3) -> bool:
    return isinstance(s, str) and bool(_WORD.match(s)) and len(s.split()) <= max_words and name_ok(s) \
        and "  " not in s


@lru_cache(maxsize=1)
def packs4() -> list[dict]:
    return [json.loads(l) for l in open(P4)]


@lru_cache(maxsize=1)
def packs3() -> list[dict]:
    return [json.loads(l) for l in open(P3)]


def pack_files() -> dict:
    return {"packs-4/packs.jsonl": sha256_file(P4), "packs-3/packs-3.jsonl": sha256_file(P3)}


def _unit_forms(q: dict, units: list[dict]):
    u = q["unit"]
    for x in units:
        if x["name"] == u or x["plural"] == u:
            if len(x["name"].split()) == 1 and len(x["plural"].split()) == 1:
                return x["name"], x["plural"]
            return None
    if len(u.split()) != 1 or not u.isalpha():
        return None
    if u.endswith("s"):
        return u[:-1], u
    return u, u + "s"


def view4(p: dict) -> dict:
    """The slots F11 needs from one packs-4 pack."""
    et = p["entity_types"][0]
    m = re.match(r"^([A-Z]{2,3})-", et["id_format"])
    prefix = m.group(1) if m else "XQ"
    noms = []
    for d in p["taxonomy_dims"]:
        vals = [v["name"] for v in d["values"] if _ok_phrase(v["name"])]
        if _ok_phrase(d["name"]) and len(vals) >= 3:
            noms.append({"name": d["name"], "values": vals})
    for c in p["cat_fields"]:
        if c.get("ordered"):
            continue
        vals = [v["name"].lower() for v in c["values"] if _ok_phrase(v["name"].lower())]
        if _ok_phrase(c["name"]) and len(vals) >= 3:
            noms.append({"name": c["name"], "values": vals})
    nums = []
    for q in p["quantities"]:
        uf = _unit_forms(q, p.get("units", []))
        if not uf or not _ok_phrase(q["name"]) or not all(name_ok(x) for x in uf):
            continue
        lo, hi, step = int(q["min"]), int(q["max"]), int(q.get("step") or 1)
        if (hi - lo) // max(step, 1) < 12:
            continue
        nums.append({"name": q["name"], "unit": uf, "lo": lo, "hi": hi, "step": max(step, 1)})
    pres = []
    for b in p["bool_fields"]:
        al = [a for a in b.get("aliases", []) if _ok_phrase(a)]
        nm = b["name"]
        if not al or not name_ok(nm) or len(nm.split()) > 6:
            continue
        if any(t in toks(nm) for t in ("present", "absent")):
            continue
        pres.append({"name": nm, "terms": al})
    dates = []
    for f in et["fields"]:
        if "date" in f["word"] and _ok_phrase(f["word"]):
            dates.append({"name": f["word"]})
    people = [x["name"] for x in p["names"]["people"] if name_ok(x["name"])]
    roles = [x["name"] for x in p["roles"] if name_ok(x["name"]) and len(x["name"].split()) <= 3]
    docs = [x["name"] for x in p["documents"] if _ok_phrase(x["name"].lower().replace("'", ""))]
    inert = [x["text"].rstrip(".") + "." for x in p.get("inert_facts", []) if "\n" not in x["text"]]
    return {"pack_id": p["id"], "title": p.get("title"), "persona_seed": p.get("persona_seed"),
            "entity": et["noun"], "entities": et["plural"], "prefix": prefix,
            "nominal": noms, "numeric": nums, "presence": pres, "dates": dates,
            "date_window": (p["date_window"]["start"], p["date_window"]["end"]),
            "people": people, "roles": roles, "docs": docs, "inert": inert,
            "jargon": [j["term"] for j in p.get("jargon", [])], "setting": p.get("setting")}


def program_packs(held_out: bool = False) -> list[dict]:
    out = []
    for p in packs4():
        if (p.get("split_hint") == "heldout") != held_out:
            continue
        v = view4(p)
        if len(v["nominal"]) >= 3 and v["numeric"] and len(v["people"]) >= 4 and v["entity"] and \
                _ok_phrase(v["entity"]) and _ok_phrase(v["entities"]):
            out.append(v)
    return out


def view3(p: dict) -> dict:
    ps = p.get("persona") or {}
    return {"pack_id": p["id"], "title": p.get("title"), "persona_seed": p.get("persona_seed") or ps.get("onet_code"),
            "org": p.get("org"), "setting": p.get("setting"), "decider": p.get("decider_role")}


def wrapper_packs(held_out: bool = False) -> list[dict]:
    return [view3(p) for p in packs3() if (str(p.get("heldout_hint")) == "True") == held_out]
