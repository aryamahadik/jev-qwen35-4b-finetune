"""Pack adapter for F9: reads packs-1..4 (four schemas) and builds one uniform F9 view per pack.

The view holds only what F9's samplers need: record nouns with ID prefixes, attribute pools (category columns with
3-8 values, numeric columns with unit / decimals / range, boolean and date column names), list-item nouns (S4),
short note words (text cells, S6 messages), the org name and the O*NET persona seed. Every pack word F9 uses passes
the 1.6 pack-word rules (f9lex.lint_word: comparator phrases, connectives, time lead words, negation cues, number
tokens, marker words). Values that fail are dropped; a pack that cannot supply the minimum is not used.

Held-out packs (S5 / mix-tuning dev only): the orchestrator has not ruled a held-out pack set, so F9 uses the union of
the pack agents' own hints, as F3 and F8 do (packs-1 sha256(id) mod 8 == 0 proposal, packs-3 heldout_hint, packs-4
split_hint == heldout). Training cards never use these packs; S5 items use only these packs.
"""
from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

from f9lex import C_SRC, lint_colname, lint_word, snake, uh

PACKS = C_SRC / "packs"
GENERIC_DATES = ["entry_date", "report_date", "check_date", "start_date", "review_date", "close_date"]
GENERIC_ITEMS = [("check", "checks"), ("entry", "entries"), ("part", "parts"), ("task", "tasks"),
                 ("sample", "samples"), ("visit", "visits")]
GENERIC_OBJ = ["site", "origin", "batch", "route", "station", "desk"]


def _unit_ok(u):
    if not isinstance(u, str) or not u or len(u) > 10 or " " in u:
        return False
    if u in ("%", "percent", "count", "units", "items"):
        return False
    if not re.fullmatch(r"[A-Za-z°/$€£²³]+", u):
        return False
    return lint_word(re.sub(r"[^A-Za-z]", " ", u).strip() or "x") in (None, "charset") and u.lower() not in (
        "no", "yes", "per")


def _cat(name, values):
    nm = snake(name)
    if lint_colname(nm):
        return None
    vals, seen = [], set()
    for v in values:
        if not isinstance(v, str):
            continue
        v2 = v.strip()
        if len(v2) > 22 or lint_word(v2):
            continue
        if v2.lower() in seen or v2.lower() == nm.replace("_", " "):
            continue
        seen.add(v2.lower())
        vals.append(v2)
    if len(vals) < 3:
        return None
    return {"name": nm, "values": vals[:8]}


def _num(name, unit, dp, lo, hi):
    nm = snake(name)
    if lint_colname(nm) or not _unit_ok(unit):
        return None
    try:
        dp = int(dp or 0)
        lo = float(lo)
        hi = float(hi)
    except (TypeError, ValueError):
        return None
    dp = max(0, min(dp, 2))
    lo = max(0.0, lo)
    if hi > 99999:
        hi = 99999
    if hi - lo < 10:
        hi = lo + 50
    return {"name": nm, "unit": unit, "dp": dp, "lo": round(lo, dp), "hi": round(hi, dp)}


def _bool(name):
    nm = snake(name)
    if len(nm) > 28 or lint_colname(nm):
        return None
    return nm


def _date(name):
    nm = snake(name)
    if lint_colname(nm):
        return None
    if not nm.endswith(("date", "_on", "day")):
        return None
    return nm


def _noun(sg, pl, prefix):
    if not sg or not pl or lint_word(sg) or lint_word(pl) or sg.lower() == pl.lower():
        return None
    if len(sg) > 24 or len(pl) > 26:
        return None
    pre = re.sub(r"[^A-Z]", "", (prefix or "").upper())[:3]
    if len(pre) < 2:
        pre = "".join(w[0] for w in sg.split()).upper()
        if len(pre) < 2:
            pre = sg[:2].upper()
    pre = pre[:3]
    if pre in ("NO", "OK", "ID", "NA", "TBD"):
        pre = pre[0] + "X"
    return {"sg": sg, "pl": pl, "prefix": pre}


def _words(vals):
    out = []
    for v in vals:
        if isinstance(v, dict):
            v = v.get("name") or v.get("text") or v.get("label")
        if isinstance(v, str) and 3 <= len(v) <= 24 and lint_word(v) is None:
            out.append(v)
    return out


def _plural(w):
    if w.endswith(("s", "x", "ch", "sh")):
        return w + "es"
    if w.endswith("y") and w[-2:-1] not in "aeiou":
        return w[:-1] + "ies"
    return w + "s"


def _singular(pl):
    if pl.endswith("ies"):
        return pl[:-3] + "y"
    if pl.endswith(("sses", "xes", "ches", "shes")):
        return pl[:-2]
    if pl.endswith("s") and not pl.endswith("ss"):
        return pl[:-1]
    return pl


# ------------------------------------------------------------------------------------------------ per schema
def _v1(p):
    nouns = [_noun(p["item_kind"]["singular"], p["item_kind"]["plural"], None)]
    for e in p["entity_types"]:
        nouns.append(_noun(e["type"], e["plural"], e.get("id_prefix")))
    cats, nums, bools, dates = [], [], [], []
    for a in p["attributes"]:
        t = a.get("type")
        if t in ("cat",):
            cats.append(_cat(a["name"], a.get("values", [])))
        elif t in ("int", "num"):
            nums.append(_num(a["name"], a.get("unit"), a.get("decimals", 0), *(a.get("range") or [0, 100])))
        elif t == "bool":
            bools.append(_bool(a["name"]))
    if p.get("status_values"):
        cats.append(_cat("status", p["status_values"]))
    words = _words(p.get("sites", [])) + _words(p.get("objects", [])) + _words(p.get("partner_orgs", []))
    return dict(pack_id=p["id"], pack_set="packs-1", org=p["org"]["name"], persona_seed=p["persona_seed"]["onet_code"],
                nouns=nouns, cats=cats, nums=nums, bools=bools, dates=dates, words=words,
                heldout=int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 8 == 0)


def _v2(p):
    nouns = []
    for e in p["entity_types"]:
        pre = (e.get("id_format") or {}).get("prefix")
        nouns.append(_noun(e["singular"], e["plural"], pre))
    cats, nums, bools, dates = [], [], [], []
    rng = {"int": (0, 200, 0), "dec1": (0, 100, 1), "money": (10, 5000, 2), "dec2": (0, 100, 2)}
    for k, f in p["field_lexicon"].items():
        t = f.get("type")
        lab = f.get("label") or k
        if t == "cat":
            cats.append(_cat(lab, f.get("enum", [])))
        elif t in rng:
            lo, hi, dp = rng[t]
            nums.append(_num(lab, f.get("unit"), dp, lo, hi))
        elif t == "boolean":
            bools.append(_bool(lab))
        elif t == "date":
            dates.append(_date(lab))
    words = _words(p.get("source_names", [])) + _words(p.get("document_types", [])) + _words(p.get("objects", []))
    return dict(pack_id=p["id"], pack_set="packs-2", org=p["org_name"], persona_seed=p["persona_seed"]["onet_code"],
                nouns=nouns, cats=cats, nums=nums, bools=bools, dates=dates, words=words, heldout=False)


def _v3(p):
    nouns = []
    cats, nums, bools, dates = [], [], [], []
    for e in p["entity_types"]:
        nouns.append(_noun(e["name"], e["plural"], e.get("id_prefix")))
        for f in e["fields"]:
            t = f.get("type")
            if t in ("enum", "status"):
                cats.append(_cat(f["name"], f.get("values", [])))
            elif t in ("int", "amt", "num"):
                r = f.get("range") or [0, 100]
                nums.append(_num(f["name"], f.get("unit"), f.get("places", 0), r[0], r[1]))
            elif t == "date":
                dates.append(_date(f["name"]))
            elif t == "bool":
                bools.append(_bool(f["name"]))
    for b in p.get("boolean_facts", []):
        nm = b.get("name") if isinstance(b, dict) else b
        if isinstance(nm, str):
            bools.append(_bool(nm))
    words = _words(p.get("disjoint_fillers", [])) + _words(p.get("document_types", []))
    return dict(pack_id=p["id"], pack_set="packs-3", org=p["org"], persona_seed=p["persona_seed"],
                nouns=nouns, cats=cats, nums=nums, bools=bools, dates=dates, words=words,
                heldout=bool(p.get("heldout_hint")))


def _v4(p):
    nouns = []
    for e in p["entity_types"]:
        pre = re.sub(r"[^A-Z]", "", e.get("id_format", "").split("-")[0])
        nouns.append(_noun(e["noun"], e["plural"], pre))
    cats, nums, bools, dates = [], [], [], []
    for c in p["cat_fields"]:
        cats.append(_cat(c["name"], [v["name"] for v in c["values"]]))
    if p.get("statuses"):
        cats.append(_cat("status", [s["name"] for s in p["statuses"]]))
    for q in p["quantities"]:
        nums.append(_num(q["name"], q.get("unit"), q.get("decimals", 0), q.get("min", 0), q.get("max", 100)))
    for b in p["bool_fields"]:
        bools.append(_bool(b.get("aliases", [b["name"]])[0] if b.get("aliases") else b["name"]))
    for e in p["entity_types"]:
        for f in e.get("fields", []):
            if f.get("key", "").endswith("date"):
                dates.append(_date(f["key"]))
    items = [(it["noun"], it["plural"]) for it in p.get("items", [])]
    words = _words([d.get("name") for d in p.get("documents", []) if isinstance(d, dict)]) + \
        _words(p.get("actions", []))
    return dict(pack_id=p["id"], pack_set="packs-4", org=p["title"], persona_seed=p["persona_seed"],
                nouns=nouns, cats=cats, nums=nums, bools=bools, dates=dates, words=words, items=items,
                heldout=p.get("split_hint") == "heldout")


SOURCES = (("packs-1/packs.jsonl", _v1), ("packs-2/packs.jsonl", _v2), ("packs-3/packs-3.jsonl", _v3),
           ("packs-4/packs.jsonl", _v4))


def _finish(v):
    if v is None:
        return None, "schema"
    nouns, seen = [], set()
    for n in v["nouns"]:
        if n and n["sg"].lower() not in seen and n["prefix"] not in {x["prefix"] for x in nouns}:
            seen.add(n["sg"].lower())
            nouns.append(n)
    if len(nouns) < 2:
        return None, "nouns"
    names = set()

    def uniq(lst, key=lambda x: x["name"]):
        out = []
        for x in lst:
            if not x:
                continue
            k = key(x)
            if k in names:
                continue
            names.add(k)
            out.append(x)
        return out
    cats = uniq(v["cats"])
    # a category value must not equal another column's value set entry case-insensitively across columns
    allv = {}
    for c in cats:
        c["values"] = [x for x in c["values"] if x.lower() not in allv]
        for x in c["values"]:
            allv[x.lower()] = c["name"]
    cats = [c for c in cats if len(c["values"]) >= 3]
    nums = uniq(v["nums"])
    bools = uniq([{"name": b} for b in v["bools"] if b])
    dates = uniq([{"name": d} for d in v["dates"] if d])
    if len(cats) < 2:
        return None, "cats"
    if len(nums) < 2:
        return None, "nums"
    noun_words = {n["sg"].lower() for n in nouns} | {n["pl"].lower() for n in nouns}
    for c in cats:
        c["values"] = [x for x in c["values"] if x.lower() not in noun_words]
    gd = [d for d in GENERIC_DATES if d not in names]
    while len(dates) < 2:
        d = gd[int(uh("f9-date", v["pack_id"], len(dates)) * len(gd))]
        gd.remove(d)
        dates.append({"name": d})
        names.add(d)
    items = []
    for sg, pl in v.get("items", []):
        if lint_word(sg) is None and lint_word(pl) is None and sg.lower() not in noun_words:
            items.append((sg, pl))
    if not items:
        items = [GENERIC_ITEMS[int(uh("f9-item", v["pack_id"]) * len(GENERIC_ITEMS))]]
    obj = GENERIC_OBJ[int(uh("f9-obj", v["pack_id"]) * len(GENERIC_OBJ))]
    words = [w for w in dict.fromkeys(v["words"]) if w.lower() not in allv]
    if len(words) < 4:
        words += ["north yard", "south yard", "main office", "front desk", "back room", "loading bay"]
    v.update(nouns=nouns, cats=cats, nums=nums, bools=[b["name"] for b in bools], dates=[d["name"] for d in dates],
             items=items, obj=obj, words=words[:24])
    return v, None


@lru_cache(maxsize=None)
def load_views():
    """Pack views, cached on disk in F9/tmp keyed by the sha256 of the four pack files and of this module."""
    import hashlib
    import pickle
    h = hashlib.sha256(Path(__file__).read_bytes())
    for rel, _ in SOURCES:
        h.update((PACKS / rel).read_bytes())
    cache = Path(__file__).resolve().parent.parent / "tmp" / f"packviews_{h.hexdigest()[:16]}.pkl"
    if cache.exists():
        try:
            return pickle.loads(cache.read_bytes())
        except Exception:
            pass
    out = _load_views()
    tmp = cache.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(out))
    tmp.replace(cache)
    return out


def _load_views():
    views, drops = {}, {}
    for rel, fn in SOURCES:
        with open(PACKS / rel, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                p = json.loads(line)
                try:
                    v = fn(p)
                except (KeyError, IndexError, TypeError, AttributeError):
                    v = None
                v, why = _finish(v)
                if v is None:
                    drops[why] = drops.get(why, 0) + 1
                    continue
                views[v["pack_id"]] = v
    return views, drops


def training_packs():
    views, _ = load_views()
    return sorted((v for v in views.values() if not v["heldout"]), key=lambda v: v["pack_id"])


def heldout_packs():
    views, _ = load_views()
    return sorted((v for v in views.values() if v["heldout"]), key=lambda v: v["pack_id"])


if __name__ == "__main__":
    views, drops = load_views()
    tr, ho = training_packs(), heldout_packs()
    print(json.dumps({"usable": len(views), "training": len(tr), "heldout": len(ho), "drops": drops,
                      "by_set": {s: sum(1 for v in views.values() if v["pack_set"] == s)
                                 for s in ("packs-1", "packs-2", "packs-3", "packs-4")},
                      "cats>=3": sum(1 for v in views.values() if len(v["cats"]) >= 3),
                      "nums>=3": sum(1 for v in views.values() if len(v["nums"]) >= 3),
                      "bools": sum(1 for v in views.values() if v["bools"])}, indent=1))
