"""F8 view of the shared domain packs (packs-3 and packs-4; C_DATA_SPEC 2.1, XF09 one pack per card).

Each pack is mapped to the slots F8 needs: the case noun and ID prefix, Boolean factors (affirmative names only,
F8-R5-01), class groups for base rates and PRED outcomes, adverse / favourable events, actions, tier names, amount
fields, a categorical dimension, inert sentences and the currency. Every label passes the F8 pack lints: no digit, no
record-status word (F8-R4-06), no negation or absence word (F8-R5-01), no quote, colon, comma, semicolon or connective
word, and not a marker word. Packs whose own hint marks them held out (packs-3 heldout_hint, packs-4 split_hint) are S5
packs: never used by S1-S4 (8.5 lint).
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from common import PACKS
from lexicon import ABSENCE_RE, MARKER_WORDS, RECORD_STATUS_RE

_BAD_CHARS = re.compile(r"[\d'\"`:;,()\[\]{}<>|/\\#*_=+&%$@!?~^]")
_CONNECT = re.compile(r"\b(and|or|unless|only|if|exactly|either|neither|nor|of all|classed|shows?|show|than|"
                      r"above|below|over|under|least|most|chance|score|tier|rating|risk|expected|loss|cost|value|"
                      r"none|marked|required|requires|require|is|are|wrong|right|reject|rejected|accept|accepted|"
                      r"should|would|true|false|yes|no)\b", re.I)


def label_ok(s: str, *, maxlen: int = 36, allow_connect: bool = False) -> bool:
    if not isinstance(s, str):
        return False
    t = s.strip()
    if not t or t != s or len(t) > maxlen or len(t) < 3:
        return False
    if t.lower() in MARKER_WORDS:
        return False
    if _BAD_CHARS.search(t) or "  " in t:
        return False
    if RECORD_STATUS_RE.search(t) or ABSENCE_RE.search(t):
        return False
    if not allow_connect and _CONNECT.search(t):
        return False
    if t[0] in "-.":
        return False
    return True


def _dedup(xs, key=lambda x: x):
    seen, out = set(), []
    for x in xs:
        k = key(x).lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(x)
    return out


def _prefix(fmt: str, fallback: str) -> str:
    m = re.match(r"([A-Z]{2,4})", fmt or "")
    return m.group(1) if m else fallback


def _inert_ok(s: str) -> bool:
    from lexicon import banned_hits
    return (isinstance(s, str) and 8 <= len(s) <= 120 and not RECORD_STATUS_RE.search(s) and not banned_hits(s)
            and not re.search(r"\d\s*[-–—]\s*\d|\bunless\b|\bonly if\b|\b(wrong|right|reject|accept|should|"
                              r"would)\b", s, re.I)
            and not re.search(r"\b(classed|shows?|chance|score|risk|tier|rating|loss|not recorded|unless|only if)\b",
                              s, re.I)
            and not re.search(r"['\"]", s) and "\n" not in s)


def _p3(p: dict) -> dict:
    et = p["entity_types"][0]
    case = {"noun": et["name"], "plural": et["plural"], "prefix": _prefix(et.get("id_prefix", ""), "CS")}
    factors = []
    for b in p.get("boolean_facts", []):
        if b.get("presupposes"):
            continue
        for lab in b.get("concept_set", [])[:1]:
            if label_ok(lab):
                factors.append({"label": lab, "pole": None})
    cats = []
    sd = p.get("scope_dimension") or {}
    vals = [v for v in sd.get("values", []) if label_ok(v)]
    if label_ok(sd.get("name", "")) and len(vals) >= 2:
        cats.append({"name": sd["name"], "values": vals})
    amounts = []
    for f in et.get("fields", []):
        if f.get("type") == "amt":
            nm = f["name"].replace("_", " ")
            if label_ok(nm):
                amounts.append({"name": nm})
    groups = []
    for st in et.get("fields", []):
        if st.get("type") == "status" and isinstance(st.get("polarity"), dict):
            labs = [v for v in st.get("values", []) if label_ok(v)]
            pol = {v: {"bad": "adverse", "not bad": "favourable", "neutral": "neutral"}.get(st["polarity"].get(v),
                                                                                           "neutral") for v in labs}
            if len(labs) >= 3:
                groups.append({"name": st["name"].replace("_", " "), "labels": labs, "pol": pol})
    for os_ in p.get("outcome_sets", []):
        labs = [v for v in os_ if label_ok(v)]
        if len(labs) >= 3:
            groups.append({"name": "outcome", "labels": labs, "pol": {v: "neutral" for v in labs}})
    hyps = [h for h in p.get("hypotheses", []) if label_ok(h["phrase"], maxlen=40, allow_connect=True)
            and not re.search(r"\b(not|no|never)\b", h["phrase"])]
    events = []
    for e in p.get("events", []):
        if label_ok(e["phrase"]) and e["polarity"] in ("adverse", "favourable"):
            events.append({"label": e["phrase"], "pol": e["polarity"]})
    for c in p.get("consequences", []):
        if label_ok(c["phrase"]):
            events.append({"label": c["phrase"], "pol": "adverse" if c["tag"] == "bad" else "favourable"})
    actions = []
    for a in p.get("actions", []):
        if label_ok(a["phrase"]):
            actions.append({"label": a["phrase"], "pol": "protective" if a.get("protective") else "favourable",
                            "defn": None})
    tiers = []
    if p.get("level_names") and all(label_ok(x) for x in p["level_names"]):
        tiers.append(list(p["level_names"]))
    money = p.get("money") or {}
    cur = money.get("currency", "USD")
    currency = {"unit": cur, "plural": cur, "places": 2 if money.get("places", 2) == 2 else 0}
    inert = [f"The {x} were updated this month." for x in p.get("inert_fact_types", []) if _inert_ok(x)]
    inert += [f"Also noted: {x}." for x in p.get("disjoint_fillers", []) if _inert_ok(x)]
    people = list((p.get("names") or {}).get("persons", []))
    return {"pid": p["id"], "set": "packs-3", "split": "heldout" if p.get("heldout_hint") else "train",
            "persona_seed": p.get("persona_seed"), "org": p.get("org"), "role": p.get("decider_role"),
            "case": case, "factors": _dedup(factors, key=lambda x: x["label"]), "cats": cats, "amounts": amounts,
            "currency": currency, "groups": groups, "hyps": hyps, "events": _dedup(events, key=lambda x: x["label"]),
            "actions": _dedup(actions, key=lambda x: x["label"]), "tiers": tiers, "inert": inert,
            "people": people, "title": p.get("title"), "sha": None}


def _p4(p: dict) -> dict:
    et = p["entity_types"][0]
    case = {"noun": et["noun"], "plural": et["plural"], "prefix": _prefix(et.get("id_format", ""), "CS")}
    factors = []
    for b in p.get("bool_fields", []):
        if b.get("presupposes"):
            continue
        for lab in (b.get("aliases") or [])[:1]:
            if label_ok(lab):
                factors.append({"label": lab, "pole": {"true": "adverse_if_present", "false": "adverse_if_absent"}
                                .get(b.get("adverse_pole"))})
    cats, groups, tiers = [], [], []
    for c in p.get("cat_fields", []):
        labs = [v["name"] for v in c["values"] if label_ok(v["name"])]
        if len(labs) != len(c["values"]):
            continue
        pol = {v["name"]: v.get("tag", "neutral") for v in c["values"]}
        if c.get("ordered") and 3 <= len(labs) <= 6:
            ordered = sorted(c["values"], key=lambda v: v.get("rank") or 0)
            tiers.append([v["name"] for v in ordered])
        if not c.get("ordered") and label_ok(c["name"]) and len(labs) >= 2:
            cats.append({"name": c["name"], "values": labs})
        if len(labs) >= 3 and label_ok(c["name"]):
            groups.append({"name": c["name"], "labels": labs, "pol": pol})
    sts = [s for s in p.get("statuses", []) if label_ok(s["name"])]
    if len(sts) >= 3:
        groups.append({"name": "status", "labels": [s["name"] for s in sts],
                       "pol": {s["name"]: s.get("tag", "neutral") for s in sts}})
    outs = [o for o in p.get("outcomes", []) if label_ok(o["name"])]
    if len(outs) >= 3:
        groups.append({"name": "outcome", "labels": [o["name"] for o in outs],
                       "pol": {o["name"]: o.get("tag", "neutral") for o in outs}})
    amounts = []
    cur = p.get("currency") or {}
    cname = cur.get("name", "")
    for q in p.get("quantities", []):
        if q.get("unit") == cname and label_ok(q["name"]):
            amounts.append({"name": q["name"]})
    events = [{"label": r["name"], "pol": "adverse"} for r in p.get("risk_events", []) if label_ok(r["name"])]
    events += [{"label": s["name"], "pol": s["tag"]} for s in sts if s.get("tag") in ("adverse", "favourable")]
    actions = []
    for a in p.get("actions", []):
        if a.get("effect") in ("protective", "favourable") and label_ok(a["verb"]):
            syn = [x for x in a.get("synonyms", []) if label_ok(x)]
            actions.append({"label": a["verb"], "pol": a["effect"],
                            "defn": ("the same step as " + " or ".join(syn[:2])) if syn else None})
    currency = {"unit": cur.get("plural", "units"), "plural": cur.get("plural", "units"),
                "singular": cur.get("name"), "places": 0}
    inert = [x["text"].rstrip(".") + "." for x in p.get("inert_facts", []) if _inert_ok(x["text"])]
    people = [x["name"] for x in (p.get("names") or {}).get("people", [])]
    return {"pid": p["id"], "set": "packs-4", "split": "heldout" if p.get("split_hint") == "heldout" else "train",
            "persona_seed": p.get("persona_seed"), "org": p.get("title"),
            "role": (p.get("persona") or {}).get("deciding_role"), "case": case,
            "factors": _dedup(factors, key=lambda x: x["label"]), "cats": cats, "amounts": amounts,
            "currency": currency, "groups": groups, "hyps": [], "events": _dedup(events, key=lambda x: x["label"]),
            "actions": _dedup(actions, key=lambda x: x["label"]), "tiers": tiers, "inert": inert, "people": people,
            "title": p.get("title"), "sha": None}


def _distinct(v: dict) -> None:
    """Factor labels, categorical names and amount names never share a normalised name (one key per fact)."""
    def nk(x):
        return re.sub(r"[^a-z0-9]+", " ", x.lower()).strip()
    taken = set()
    for c in v["cats"]:
        taken.add(nk(c["name"]))
    v["factors"] = [f for f in v["factors"] if nk(f["label"]) not in taken]
    taken |= {nk(f["label"]) for f in v["factors"]}
    v["amounts"] = [a for a in v["amounts"] if nk(a["name"]) not in taken and nk(a["name"]) not in
                    ("reference", "event", "chance", "loss", "own cost")]
    v["factors"] = [f for f in v["factors"] if nk(f["label"]) not in ("reference", "event", "chance", "loss",
                                                                       "own cost", "case details")]


def _usable(v: dict) -> dict:
    """Which F8 sub-skills a pack can host (minimum slot counts)."""
    nf = len(v["factors"])
    ng = max([len(g["labels"]) for g in v["groups"]] or [0])
    ne = len(v["events"])
    na = len(v["actions"])
    names_ok = bool(re.fullmatch(r"[a-z][a-z ]+[a-z]", v["case"]["noun"])) and \
        bool(re.fullmatch(r"[a-z][a-z ]+[a-z]", v["case"]["plural"])) and \
        not RECORD_STATUS_RE.search(v["case"]["noun"] + " " + v["case"]["plural"]) and \
        not RECORD_STATUS_RE.search(" ".join(v.get("people") or []))
    return {"points": nf >= 5 and names_ok, "bayes": nf >= 1 and ng >= 3 and names_ok,
            "expected": ne >= 2 and names_ok, "dec": ne >= 1 and na >= 2 and names_ok,
            "rank": ne >= 1 and names_ok, "pred": ng >= 3 and nf >= 1 and names_ok}


@lru_cache(maxsize=None)
def load() -> tuple:
    out = []
    for path, fn in ((PACKS / "packs-3" / "packs-3.jsonl", _p3), (PACKS / "packs-4" / "packs.jsonl", _p4)):
        with open(path, encoding="utf-8") as f:
            for line in f:
                p = json.loads(line)
                v = fn(p)
                v["sha"] = p.get("pack_sha256") or p.get("sha256")
                _distinct(v)
                v["usable"] = _usable(v)
                out.append(v)
    return tuple(out)


def by_id() -> dict:
    return {v["pid"]: v for v in load()}


if __name__ == "__main__":
    import collections
    P = load()
    c = collections.Counter((v["set"], v["split"]) for v in P)
    print(c)
    u = collections.Counter(k for v in P if v["split"] == "train" for k, ok in v["usable"].items() if ok)
    print("train usable:", u)
    u = collections.Counter(k for v in P if v["split"] == "heldout" for k, ok in v["usable"].items() if ok)
    print("heldout usable:", u)
    allu = sum(1 for v in P if v["split"] == "train" and all(v["usable"].values()))
    print("train packs usable for every sub-skill:", allu)
    for v in P[:2] + P[80:82]:
        print(json.dumps({k: v[k] for k in ("pid", "case", "factors", "cats", "amounts", "currency", "groups",
                                            "events", "actions", "tiers")})[:1800])
