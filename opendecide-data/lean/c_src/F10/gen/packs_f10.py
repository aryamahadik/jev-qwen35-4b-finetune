"""F10 view of the shared domain packs. Training cards (S1-S4, S6) use packs-2 (built for F10: attribute lexicons with
statements, key words and state words, inert-context vocabulary, label words with structured natural predicates,
jargon candidates; pack lints done by the pack agent). S5 (held-out, dev only) uses the pack agents' held-out
proposals (packs-4 split_hint == heldout), adapted with generic key-value containers only. One pack per card (XF09)."""
from __future__ import annotations

import datetime as dt
import json
from functools import lru_cache

from common import PACKS_DIR, sha256_text

TYPE_MAP = {"int": "count", "dec1": "qty", "dec2": "qty", "money": "amount", "cat": "cat", "ord": "cat",
            "boolean": "flag", "date": "date", "tag": "tag"}
OPS = {">=": "ge", ">": "gt", "<=": "le", "<": "lt", "==": "eq", "=": "eq", "!=": "ne", "is_true": "true",
       "is_false": "false", "in": "in"}


def _attr_p2(a):
    t = TYPE_MAP[a["type"]]
    lx = a.get("lexicon") or {}
    out = {"key": a["key"], "name": a["label"], "type": t, "group": a.get("concept_group") or a["key"],
           "phrases": list(lx.get("phrases") or []), "key_words": list(lx.get("key_word_forms") or lx.get("key_words") or []),
           "state_words": list(lx.get("state_words") or []), "statements": dict(lx.get("statements") or {}),
           "aliases": list(a.get("aliases") or []), "unit": None, "unit_syn": [], "d": 0, "values": None,
           "lo": None, "hi": None}
    if t in ("count", "qty", "amount"):
        out["d"] = int(a.get("places") or 0) if t != "count" else 0
        if t == "amount":
            out["d"] = 2
        out["unit"] = a.get("unit")
        out["unit_syn"] = list(a.get("unit_synonyms") or [])
        out["lo"], out["hi"] = float(a.get("min", 0)), float(a.get("max", 100))
    elif t in ("cat", "tag"):
        out["values"] = list(a["values"])
    if t == "flag":
        out["statements"] = {"positive": a.get("pos_statement") or out["statements"].get("positive"),
                             "negative": a.get("neg_statement") or out["statements"].get("negative")}
    if t == "tag":
        out["statements"].setdefault("none", a.get("none_statement"))
    return out


def adapt_p2(r):
    case = [e for e in r["entity_types"] if e.get("role") == "case"][0]
    attrs = [_attr_p2(a) for a in case["attributes"]]
    lw = []
    for w in r.get("label_words") or []:
        if w.get("name_lint") != "pass" or w.get("entity") not in (None, case["key"]):
            continue
        p = w.get("predicate") or {}
        terms = []
        okp = True
        for t in p.get("terms") or []:
            if t.get("op") not in OPS:
                okp = False
            terms.append({"attr": t.get("attr"), "op": OPS.get(t.get("op")), "value": t.get("value")})
        if okp and terms:
            lw.append({"word": w["word"], "join": p.get("join", "and"), "terms": terms})
    outcomes = [{"name": o["name"], "bad": bool(o.get("adverse"))} for s in r.get("outcome_sets") or []
                for o in s["outcomes"]]
    dw = r.get("date_window") or {"start": "2029-01-01", "span_days": 730}
    return {"pack_id": r["id"], "agent": "packs-2", "persona_seed": (r.get("persona_seed") or {}).get("onet_code"),
            "persona_title": (r.get("persona_seed") or {}).get("onet_title"), "role": r.get("decider_role"),
            "org": r.get("org_name"), "entity": case["singular"], "entity_plural": case["plural"],
            "attrs": attrs, "label_words": lw, "inert_vocab": list(r.get("inert_context_vocab") or []),
            "jargon": list(r.get("jargon_candidates") or []), "outcomes": outcomes,
            "doc_types": list(r.get("document_types") or []),
            "currency": (r.get("currency") or {}).get("unit", "dollars"),
            "date_lo": dt.date.fromisoformat(dw["start"]).toordinal(),
            "date_hi": dt.date.fromisoformat(dw["start"]).toordinal() + int(dw.get("span_days", 730)),
            "heldout": False, "parents": list(r.get("parents") or [])}


def adapt_p4(r):
    """Held-out packs-4 pack -> F10 pack (S5 dev only): quantities, Boolean fields, category fields, one date pair."""
    ent = r["entity_types"][0]
    attrs = []
    for q in r.get("quantities") or []:
        d = int(q.get("decimals") or 0)
        unit = None if q.get("unit") in (None, "count") else q["unit"]
        attrs.append({"key": q["id"], "name": q["name"], "type": "count" if d == 0 else "qty", "group": q["id"],
                      "phrases": [q["name"]], "key_words": q["name"].split(), "state_words": [], "statements": {},
                      "aliases": [], "unit": unit, "unit_syn": [], "d": d, "values": None,
                      "lo": float(q.get("min", 0)), "hi": float(q.get("max", 100))})
    for b in r.get("bool_fields") or []:
        attrs.append({"key": b["id"], "name": b["name"], "type": "flag", "group": b["id"], "phrases": [b["name"]],
                      "key_words": b["name"].split(), "state_words": [], "statements": {}, "aliases": [],
                      "unit": None, "unit_syn": [], "d": 0, "values": None, "lo": None, "hi": None})
    for c in r.get("cat_fields") or []:
        vals = [v["name"] for v in c["values"]]
        attrs.append({"key": c["id"], "name": c["name"], "type": "cat", "group": c["id"], "phrases": [c["name"]],
                      "key_words": c["name"].split(), "state_words": vals, "statements": {}, "aliases": [],
                      "unit": None, "unit_syn": [], "d": 0, "values": vals, "lo": None, "hi": None})
    dw = r.get("date_window") or {}
    lo = dt.date.fromisoformat(dw.get("start", "2038-01-01")).toordinal()
    hi = dt.date.fromisoformat(dw.get("end", "2038-12-31")).toordinal()
    cur = r.get("currency") or {}
    return {"pack_id": r["id"], "agent": "packs-4", "persona_seed": r.get("persona_seed"),
            "persona_title": (r.get("persona") or {}).get("onet_title"),
            "role": (r.get("persona") or {}).get("deciding_role"), "org": r.get("title"),
            "entity": ent["noun"], "entity_plural": ent["plural"], "attrs": attrs, "label_words": [],
            "inert_vocab": [], "jargon": [j["term"] for j in r.get("jargon") or []],
            "outcomes": [{"name": o["name"], "bad": o.get("tag") == "unfavourable"} for o in r.get("outcomes") or []],
            "doc_types": [d["name"] for d in r.get("documents") or []], "currency": cur.get("plural", "credits"),
            "date_lo": lo, "date_hi": hi, "heldout": True, "parents": list(r.get("parents") or [])}


@lru_cache(maxsize=1)
def load():
    """(training packs, held-out packs): dicts pack_id -> F10 pack, in sorted id order."""
    train, held = {}, {}
    with open(PACKS_DIR / "packs-2" / "packs.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                p = adapt_p2(json.loads(line))
                p["pack_sha256"] = sha256_text(line.strip())
                train[p["pack_id"]] = p
    with open(PACKS_DIR / "packs-4" / "packs.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                if r.get("split_hint") == "heldout":
                    p = adapt_p4(r)
                    p["pack_sha256"] = sha256_text(line.strip())
                    held[p["pack_id"]] = p
    return dict(sorted(train.items())), dict(sorted(held.items()))


if __name__ == "__main__":
    tr, ho = load()
    from collections import Counter
    print(len(tr), len(ho))
    print(Counter(a["type"] for p in tr.values() for a in p["attrs"]))
    print(Counter(len(p["label_words"]) for p in tr.values()))
    print(Counter(a["type"] for p in ho.values() for a in p["attrs"]))
