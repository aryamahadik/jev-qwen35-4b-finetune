"""F6 view of the shared domain packs (packs-3 and packs-4; C_DATA_SPEC v4 2.1, XF09 one pack per card).

Each pack is mapped to the slots F6 needs: case nouns with fixed-width ID prefixes, whole-number quantities with
units and ranges, category attributes with value lists, event types (noun phrases), class adjectives, an outcome pool,
people and places, and the persona seed (O*NET code). Every string passes the F6 record scan (scan.py: 3.1 banned
phrases, completeness words, markers, plan / evidence words). Packs whose own hint marks them held out (packs-3
heldout_hint, packs-4 split_hint) are S5 packs: never used by S1-S4.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from .common import PACKS, sha256_text
from . import scan

_WORD = re.compile(r"^[A-Za-z][A-Za-z' ]*[A-Za-z]$")


def _ok(s: str, max_words: int = 4) -> bool:
    if not isinstance(s, str) or not _WORD.match(s) or "  " in s:
        return False
    if len(s.split()) > max_words or "'" in s:
        return False
    return not scan.record_hits(s) and not scan.question_hits(s)


def _prefix(p: str) -> str | None:
    m = re.match(r"^([A-Z]{2,4})", p or "")
    return m.group(1) if m else None


def _dedup(xs):
    out, seen = [], set()
    for x in xs:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def _p3(p: dict) -> dict:
    cases = []
    for e in p["entity_types"]:
        pre = _prefix(e.get("id_prefix", ""))
        if pre and _ok(e["name"], 3) and _ok(e["plural"], 3) and len(e["name"].split()) == len(e["plural"].split()) \
                and e["name"].lower() != e["plural"].lower():
            cases.append({"noun": e["name"], "plural": e["plural"], "prefix": pre})
    qty, cat = [], []
    for e in p["entity_types"]:
        for f in e["fields"]:
            nm = f["name"].replace("_", " ")
            if f["type"] == "int" and _ok(nm, 3) and _ok(f.get("unit", ""), 2):
                lo, hi = f["range"]
                if hi - lo >= 20 and lo >= 0:
                    dr = f.get("direction")
                    adv = "high" if dr == "high is bad" else ("low" if dr == "low is bad" else None)
                    qty.append({"name": nm, "unit": f["unit"], "lo": int(lo), "hi": int(hi), "adverse": adv})
            elif f["type"] == "enum" and _ok(nm, 3):
                vals = [v for v in f["values"] if _ok(v, 3)]
                if len(vals) >= 3:
                    cat.append({"name": nm, "values": vals})
    events = []
    for b in p.get("boolean_facts", []):
        if b.get("kind") == "event":
            for c in b.get("concept_set", [])[:1]:
                if _ok(c, 3):
                    events.append(c)
    ev_pol = {}
    for e in p.get("events", []):
        if _ok(e.get("phrase", ""), 3) and e.get("polarity") in ("adverse", "favourable"):
            events.append(e["phrase"])
            ev_pol[e["phrase"]] = "bad" if e["polarity"] == "adverse" else "good"
    adjs = [x["predicate"] for x in p.get("predicates", []) if _ok(x["predicate"], 1)]
    outs = []
    for s in p.get("outcome_sets", []):
        outs += [o for o in s if _ok(o, 4)]
    outs += [c["phrase"] for c in p.get("consequences", []) if _ok(c["phrase"], 4)]
    valence = {}
    for c in p.get("consequences", []):
        valence[c["phrase"]] = "bad" if c.get("tag") == "bad" else "good"
    people = [x for x in p["names"].get("persons", []) if _ok(x, 3)]
    places = [x for x in p["names"].get("places", []) if _ok(x, 3)]
    docs = [d["name"] for d in p.get("document_types", []) if _ok(d["name"], 3)]
    lists = [f"{x} register" for x in docs[:3]]
    return {"pid": p["id"], "set": "packs-3", "split": "heldout" if p.get("heldout_hint") else "train",
            "persona_seed": p.get("persona_seed", {}).get("onet_code") if isinstance(p.get("persona_seed"), dict)
            else p.get("persona_seed"),
            "role": p.get("decider_role", "case officer"), "cases": cases, "qty": qty, "cat": cat,
            "events": _dedup(events), "adjs": _dedup(adjs), "outcomes": _dedup(outs), "valence": valence,
            "ev_pol": ev_pol,
            "people": people, "places": places, "roles": [r for r in p.get("roles", []) if _ok(r, 3)],
            "docs": docs, "lists": lists, "sha": p.get("sha256") or sha256_text(json.dumps(p, sort_keys=True))}


def _p4(p: dict) -> dict:
    cases = []
    for e in p["entity_types"]:
        pre = _prefix(e.get("id_format", ""))
        if pre and _ok(e["noun"], 3) and _ok(e["plural"], 3) and len(e["noun"].split()) == len(e["plural"].split()) \
                and e["noun"].lower() != e["plural"].lower():
            cases.append({"noun": e["noun"], "plural": e["plural"], "prefix": pre})
    units = {u["name"]: u for u in p.get("units", [])}
    qty = []
    for q in p.get("quantities", []):
        u = q["unit"]
        up = units[u]["plural"] if u in units else u
        if q.get("decimals", 0) == 0 and q.get("step", 1) == 1 and _ok(q["name"], 3) and _ok(up, 2):
            if q["max"] - q["min"] >= 20 and q["min"] >= 0 and u not in ("brasslet",) and \
                    u != (p.get("currency") or {}).get("name"):
                adv = q.get("adverse") if q.get("adverse") in ("high", "low") else None
                qty.append({"name": q["name"], "unit": up, "lo": int(q["min"]), "hi": int(q["max"]), "adverse": adv})
    cat = []
    for c in p.get("cat_fields", []) + p.get("taxonomy_dims", []):
        vals = [v["name"] for v in c["values"] if _ok(v["name"], 3)]
        if _ok(c["name"], 3) and len(vals) >= 3:
            cat.append({"name": c["name"], "values": vals})
    events = []
    ev_pol = {}
    for b in p.get("bool_fields", []):
        if b.get("kind") == "event":
            for a in b.get("aliases", [])[:1]:
                if _ok(a, 3):
                    events.append(a)
                    if b.get("adverse_pole") in ("true", "false"):
                        ev_pol[a] = "bad" if b["adverse_pole"] == "true" else "good"
    for r in p.get("risk_events", []):
        if _ok(r["name"], 3):
            events.append(r["name"])
            ev_pol[r["name"]] = "bad"
    adjs = []
    for x in p.get("predicates", []):
        m = re.match(r"^is ([a-z]+)$", x["phrase"])
        if m and _ok(m.group(1), 1):
            adjs.append(m.group(1))
    outs = [o["name"] for o in p.get("outcomes", []) if _ok(o["name"], 4)]
    valence = {o["name"]: {"adverse": "bad", "favourable": "good"}.get(o.get("tag"))
               for o in p.get("outcomes", []) if o.get("tag") in ("adverse", "favourable")}
    people = [x["name"] for x in p["names"].get("people", []) if _ok(x["name"], 3)]
    places = [x["name"] for x in p["names"].get("places", []) if _ok(x["name"], 3)]
    docs = [d["name"] for d in p.get("documents", []) if _ok(d["name"], 3)]
    lists = [s["name"] for s in (p.get("sources") or {}).get("trusted", []) if _ok(s["name"], 3)]
    return {"pid": p["id"], "set": "packs-4", "split": "heldout" if p.get("split_hint") == "heldout" else "train",
            "persona_seed": p.get("persona_seed"),
            "role": (p.get("persona") or {}).get("deciding_role", "case officer"),
            "cases": cases, "qty": qty, "cat": cat, "events": _dedup(events), "adjs": _dedup(adjs),
            "outcomes": _dedup(outs), "valence": valence, "ev_pol": ev_pol, "people": people, "places": places,
            "roles": [r["name"] for r in p.get("roles", []) if _ok(r["name"], 3)], "docs": docs, "lists": lists,
            "sha": p.get("sha256") or sha256_text(json.dumps(p, sort_keys=True))}


def _dedup_named(xs):
    out, seen = [], set()
    for x in xs:
        k = x["name"].lower()
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def usable(v: dict) -> bool:
    return (len(v["cases"]) >= 1 and len(v["qty"]) >= 2 and len(v["cat"]) >= 1 and len(v["events"]) >= 2
            and len(v["adjs"]) >= 2 and len(v["outcomes"]) >= 4 and len(v["people"]) >= 4
            and len(v["places"]) >= 3)


@lru_cache(maxsize=None)
def all_packs() -> tuple:
    out = []
    for path, fn in ((PACKS / "packs-3" / "packs-3.jsonl", _p3), (PACKS / "packs-4" / "packs.jsonl", _p4)):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    v = fn(json.loads(line))
                    v["cat"] = _dedup_named(v["cat"])          # repair r1: one attribute per name
                    v["qty"] = _dedup_named(v["qty"])
                    v["usable"] = usable(v)
                    out.append(v)
    return tuple(out)


def packs(split: str = "train") -> list[dict]:
    return [v for v in all_packs() if v["split"] == split and v["usable"]]


def pack(pid: str) -> dict:
    for v in all_packs():
        if v["pid"] == pid:
            return v
    raise KeyError(pid)


if __name__ == "__main__":
    import collections
    P = all_packs()
    print(collections.Counter((v["set"], v["split"], v["usable"]) for v in P))
    bad = collections.Counter()
    for v in P:
        for k in ("cases", "qty", "cat", "events", "adjs", "outcomes", "people", "places"):
            if not v[k] or (k in ("qty", "events", "adjs") and len(v[k]) < 2) or (k == "outcomes" and len(v[k]) < 4):
                bad[k] += 1
    print("short slots:", dict(bad))
