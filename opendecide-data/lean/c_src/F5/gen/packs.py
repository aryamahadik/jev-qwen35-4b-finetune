"""F5 pack view: packs-3 and packs-4 (both with tagged predicates, affixed pairs, ID pools, sources) normalised to the
nouns F5 needs. F5 takes only nouns, names, units, value sets and polarity tags from a pack; every sentence frame is
F5's own (3.4 lexicon lint on every pack string that enters program-written text).

Held-out packs (S5 and the hard-negation probe only, never a training row): the pack agents' own hints (packs-3
heldout_hint, packs-4 split_hint == "heldout"). The orchestrator owns the final held-out ruling; this split is logged in
the manifest as an assumption (the same reading F2, F3 and F8 use).

One pack per card (XF09): a pack view is used by at most one F5 card.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from functools import lru_cache

from .common import PACKS, id_ok, pack_phrase_ok, read_jsonl

GOOD_BASES = {"certified", "insured", "registered", "licensed", "eligible", "compliant", "approved", "authorized",
              "authorised", "verified", "accredited", "sealed", "cleared", "qualified", "bonded", "permitted",
              "vetted", "inspected", "audited", "signed", "stamped", "endorsed", "accepted", "recorded", "listed",
              "tested", "calibrated", "documented", "secured", "assigned", "funded", "paid", "settled", "attested",
              "confirmed", "screened", "registered", "warranted", "sanctioned", "credentialed", "notarized", "indexed"}
FALLBACK_GOOD = [("approved", "unapproved"), ("verified", "unverified"), ("cleared", None), ("documented", "undocumented")]
FALLBACK_BAD = [("flagged", None), ("disputed", "undisputed"), ("overdue", None), ("suspended", None)]
FALLBACK_DOCS = ["signed intake form", "inspection sheet", "fee receipt", "transfer slip"]
FALLBACK_RISKS = ["damage report", "safety complaint", "billing dispute"]
CURRENCY_WORDS = {"USD": "dollars", "EUR": "euros", "GBP": "pounds", "CAD": "dollars", "AUD": "dollars"}
STATUS_BAN = {"valid", "invalid", "lapsed", "expired", "active", "inactive", "current"}
_ONE = re.compile(r"^[a-z][a-z-]{2,20}$")


def _adj_ok(w: str) -> bool:
    return bool(_ONE.match(w or "")) and pack_phrase_ok(w) and not w.startswith(("un", "in", "non", "dis", "im", "ir"))


def _neg_ok(base: str, neg: str) -> bool:
    if not neg or not _ONE.match(neg):
        return False
    return any(neg == p + base or neg == p + "-" + base for p in ("un", "in", "non", "dis", "im", "ir", "il"))


def _norm_ids(pool):
    ids = [x for x in pool if id_ok(x)]
    return sorted(set(ids), key=ids.index)


def _uniq(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def _qty_name(s):
    return s.replace("_", " ").strip()


def _qty_ok(name):
    """Singular quantity names only ('The weight of X is ...'); plural or ID-like names read badly with 'is'."""
    last = name.split()[-1]
    return not (last.endswith("s") and not last.endswith("ss")) and not any(
        w in name.split() for w in ("number", "id", "code", "count"))


def _view4(p):
    v = {"pid": p["id"], "set": "packs-4", "split": "heldout" if p.get("split_hint") == "heldout" else "train",
         "persona_seed": p.get("persona_seed"), "title": p.get("title"), "org": p["title"]}
    ents = []
    for e in p["entity_types"]:
        if not (pack_phrase_ok(e["noun"]) and pack_phrase_ok(e["plural"])):
            continue
        fmt = e.get("id_format") or ""
        pre = re.match(r"^([A-Z]{1,4})-", fmt)
        if not pre:
            continue
        ents.append({"noun": e["noun"], "plural": e["plural"], "prefix": pre.group(1), "ids": []})
    v["ents"] = ents
    v["people"] = [x["name"] for x in p["names"]["people"] if pack_phrase_ok(x["name"]) and len(x["name"].split()) == 2]
    v["sources"] = [x["name"] for x in p["sources"]["trusted"] if pack_phrase_ok(x["name"])]
    q = []
    for x in p["quantities"]:
        unit = x.get("unit") or ""
        plural = unit
        for u in p.get("units", []):
            if u.get("name") == unit:
                plural = u.get("plural") or unit
        if x.get("decimals", 0) != 0 or not pack_phrase_ok(x["name"]) or not pack_phrase_ok(plural) or \
                not _qty_ok(x["name"]):
            continue
        tag = {"high": "high_bad", "low": "low_bad"}.get(x.get("adverse"))
        lo, hi, step = int(x["min"]), int(x["max"]), int(x.get("step") or 1)
        if hi - lo < 20 * step or lo < 0:
            continue
        q.append({"name": x["name"], "unit": plural, "lo": lo, "hi": hi, "step": step, "tag": tag})
    v["qtys"] = q
    cats = []
    for c in p["cat_fields"]:
        vals = [x["name"] for x in c["values"] if pack_phrase_ok(x["name"])]
        if pack_phrase_ok(c["name"]) and len(vals) >= 3:
            cats.append({"name": c["name"], "values": vals})
    v["cats"] = cats
    v["statuses"] = [{"name": s["name"], "tag": {"favourable": "good", "adverse": "bad"}.get(s["tag"])}
                     for s in p["statuses"] if pack_phrase_ok(s["name"]) and s["name"] not in STATUS_BAN]
    adjs = {}
    for pr in p["predicates"]:
        m = re.fullmatch(r"is ([a-z-]+)", pr["phrase"])
        if m and _adj_ok(m.group(1)) and pr["adverse_pole"] in ("true", "false"):
            adjs[m.group(1)] = {"word": m.group(1), "tag": "bad" if pr["adverse_pole"] == "true" else "good",
                                "neg": None}
    for a in p.get("neg_affix_pairs", []):
        b, n = a["positive"], a["negative"]
        if _adj_ok(b) and _neg_ok(b, n):
            if b in adjs:
                adjs[b]["neg"] = n
            elif b in GOOD_BASES:
                adjs[b] = {"word": b, "tag": "good", "neg": n}
    v["adjs"] = list(adjs.values())
    v["docs"] = [d["name"] for d in p["documents"] if pack_phrase_ok(d["name"])]
    v["doc_tags"] = {d: "good" for d in v["docs"]}
    v["risks"] = [r["name"] for r in p.get("risk_events", []) if pack_phrase_ok(r["name"])]
    v["roles"] = [r["name"] for r in p["roles"] if pack_phrase_ok(r["name"]) and not r.get("decider")]
    v["actions"] = [{"verb": a["verb"], "effect": a["effect"]} for a in p["actions"]
                    if a.get("kind") == "write" and re.fullmatch(r"[a-z]+", a["verb"]) and pack_phrase_ok(a["verb"])]
    v["inert"] = [x["text"].rstrip(".") + "." for x in p.get("inert_facts", []) if pack_phrase_ok(x["text"])]
    dw = p.get("date_window") or {}
    v["window"] = (dw.get("start"), dw.get("end"))
    return v


def _view3(p):
    v = {"pid": p["id"], "set": "packs-3", "split": "heldout" if p.get("heldout_hint") else "train",
         "persona_seed": p.get("persona_seed"), "title": p.get("title"), "org": p.get("org")}
    ents, qtys, cats, sts = [], [], [], []
    for e in p["entity_types"]:
        if not (pack_phrase_ok(e["name"]) and pack_phrase_ok(e["plural"])):
            continue
        ents.append({"noun": e["name"], "plural": e["plural"], "prefix": e["id_prefix"], "ids": [],
                     "id_key": e.get("id_key")})
        for f in e["fields"]:
            nm = _qty_name(f["name"])
            if f["type"] in ("int", "amt") and pack_phrase_ok(nm) and _qty_ok(nm):
                unit = f.get("unit") or ""
                unit = CURRENCY_WORDS.get(unit, unit)
                if not pack_phrase_ok(unit):
                    continue
                lo, hi = f.get("range", [0, 0])
                lo, hi = int(lo), int(hi)
                if hi - lo < 20 or lo < 0:
                    continue
                tag = {"high is bad": "high_bad", "low is bad": "low_bad"}.get(f.get("direction"))
                qtys.append({"name": nm, "unit": unit, "lo": lo, "hi": hi, "step": 1, "tag": tag})
            elif f["type"] == "enum":
                vals = [x for x in f.get("values", []) if pack_phrase_ok(x)]
                if pack_phrase_ok(nm) and len(vals) >= 3:
                    cats.append({"name": nm, "values": vals})
            elif f["type"] == "status":
                pol = f.get("polarity") or {}
                for s in f.get("values", []):
                    if pack_phrase_ok(s) and s not in STATUS_BAN:
                        sts.append({"name": s, "tag": {"good": "good", "bad": "bad"}.get(pol.get(s))})
    for e in ents:
        sch = (p.get("id_schemes") or {}).get(e.get("id_key")) or {}
        e["ids"] = _norm_ids(sch.get("pool", []))
    v["ents"] = [e for e in ents]
    v["people"] = [x for x in p["names"]["persons"] if pack_phrase_ok(x) and len(x.split()) == 2]
    v["sources"] = [cap_words(x) for x in p["source_names"]["trusted"] if pack_phrase_ok(x)]
    v["qtys"] = qtys
    sd = p.get("scope_dimension") or {}
    vals = [x for x in sd.get("values", []) if pack_phrase_ok(x)]
    if sd and pack_phrase_ok(sd.get("name", "")) and len(vals) >= 3:
        cats.append({"name": sd["name"], "values": vals})
    v["cats"] = cats
    seen = set()
    v["statuses"] = [s for s in sts if not (s["name"] in seen or seen.add(s["name"]))]
    adjs = {}
    for pr in p["predicates"]:
        w = pr["predicate"]
        if _adj_ok(w) and pr["adverse_pole"] in ("true", "false"):
            adjs[w] = {"word": w, "tag": "bad" if pr["adverse_pole"] == "true" else "good", "neg": None}
    for a in p.get("affixed_words", []):
        b, n = a["base"], a["negated"]
        if _adj_ok(b) and _neg_ok(b, n):
            if b in adjs:
                adjs[b]["neg"] = n
            elif b in GOOD_BASES:
                adjs[b] = {"word": b, "tag": "good", "neg": n}
    v["adjs"] = list(adjs.values())
    v["docs"] = [d["name"] for d in p["document_types"] if pack_phrase_ok(d["name"])]
    v["doc_tags"] = {d["name"]: ("bad" if d.get("current_is") == "bad" else "good") for d in p["document_types"]
                     if pack_phrase_ok(d["name"])}
    v["risks"] = []
    v["roles"] = [r for r in p["roles"] if pack_phrase_ok(r)]
    v["actions"] = []
    v["inert"] = []
    v["window"] = (None, None)
    return v


def cap_words(s: str) -> str:
    return " ".join(w[:1].upper() + w[1:] for w in s.split())


def _fill(v):
    """Fallbacks so every view has what every sampler needs; the view records which parts are F5 fallbacks."""
    fb = []
    good = [a for a in v["adjs"] if a["tag"] == "good"]
    bad = [a for a in v["adjs"] if a["tag"] == "bad"]
    used = {a["word"] for a in v["adjs"]}
    for w, n in FALLBACK_GOOD:
        if len(good) >= 3:
            break
        if w not in used:
            a = {"word": w, "tag": "good", "neg": n, "fallback": True}
            v["adjs"].append(a)
            good.append(a)
            used.add(w)
            fb.append(f"adj:{w}")
    for w, n in FALLBACK_BAD:
        if len(bad) >= 3:
            break
        if w not in used:
            a = {"word": w, "tag": "bad", "neg": n, "fallback": True}
            v["adjs"].append(a)
            bad.append(a)
            used.add(w)
            fb.append(f"adj:{w}")
    if not any(a.get("neg") for a in v["adjs"]):
        for w, n in FALLBACK_GOOD:
            if n and w not in used:
                v["adjs"].append({"word": w, "tag": "good", "neg": n, "fallback": True})
                fb.append(f"adj:{w}")
                break
    if len(v["docs"]) < 3:
        for d in FALLBACK_DOCS:
            if d not in v["docs"]:
                v["docs"].append(d)
                v["doc_tags"][d] = "good"
                fb.append(f"doc:{d}")
    if len(v["risks"]) < 2:
        v["risks"] += [r for r in FALLBACK_RISKS if r not in v["risks"]]
    v["fallbacks"] = fb
    return v


def _ids_for(v, e, n=40):
    """Program ID pool for an entity type: the pack's own pool when it has one, else IDs on the pack's prefix (the
    pack declares the prefix; digits are drawn by F5, seeded by pack and type)."""
    if len(e["ids"]) >= 24:
        return e["ids"]
    from .common import rng_for
    r = rng_for("f5-ids", v["pid"], e["noun"])
    out = set(e["ids"])
    while len(out) < n:
        out.add(f"{e['prefix']}-{r.randint(1000, 9899)}")
    return sorted(out, key=lambda x: (x not in e["ids"], x))


@lru_cache(maxsize=None)
def all_views():
    vs = []
    for p in read_jsonl(PACKS / "packs-4" / "packs.jsonl"):
        vs.append(_view4(p))
    for p in read_jsonl(PACKS / "packs-3" / "packs-3.jsonl"):
        vs.append(_view3(p))
    out = []
    for v in vs:
        v = _fill(v)
        v["ents"] = [e for e in v["ents"] if re.fullmatch(r"[A-Z]{1,4}", e["prefix"] or "")]
        for e in v["ents"]:
            e["ids"] = _ids_for(v, e)
        v["usable"] = bool(v["ents"]) and len(v["people"]) >= 8 and bool(v["sources"]) and len(v["qtys"]) >= 1
        if not v["window"][0]:
            from .common import rng_for
            r = rng_for("f5-window", v["pid"])
            y = r.choice([2041, 2043, 2045, 2047, 2049])
            v["window"] = (f"{y}-01-01", f"{y + 1}-12-31")
        out.append(v)
    return tuple(out)


def views(split: str):
    return [v for v in all_views() if v["usable"] and v["split"] == split]


def window(v):
    return dt.date.fromisoformat(v["window"][0]), dt.date.fromisoformat(v["window"][1])


if __name__ == "__main__":
    import collections
    tr, ho = views("train"), views("heldout")
    print(json.dumps({"train": len(tr), "heldout": len(ho), "unusable": sum(1 for v in all_views() if not v["usable"]),
                      "fallback_packs": sum(1 for v in tr + ho if v["fallbacks"])}, indent=1))
    c = collections.Counter()
    for v in tr:
        c["adjs_good"] += sum(a["tag"] == "good" for a in v["adjs"])
        c["adjs_bad"] += sum(a["tag"] == "bad" for a in v["adjs"])
        c["neg"] += sum(bool(a["neg"]) for a in v["adjs"])
        c["qty_tag"] += sum(bool(q["tag"]) for q in v["qtys"])
        c["cats"] += len(v["cats"])
        c["stat_tag"] += sum(bool(s["tag"]) for s in v["statuses"])
        c["actions"] += len(v["actions"])
    print(dict(c))


PROBE_PACKS_PACKS4 = ("p4-026", "p4-053")   # held-out packs with tagged actions (probe C12 items need a deontic layer)


def heldout_split():
    """(S5 dev packs, probe packs): disjoint; the probe takes the two packs-4 packs with favourable and protective
    actions plus the last five held-out packs, S5 the other twelve."""
    ho = sorted(v["pid"] for v in views("heldout"))
    probe = [p for p in ho if p in PROBE_PACKS_PACKS4] + [p for p in ho if p not in PROBE_PACKS_PACKS4][-5:]
    s5 = [p for p in ho if p not in probe][:12]
    return s5, probe
