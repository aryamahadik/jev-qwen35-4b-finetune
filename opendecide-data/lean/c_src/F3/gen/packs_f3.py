"""Pack adapter for F3: reads the four pack sets (packs-1..4; four schemas) and builds one uniform F3 view per pack.

The view holds only what F3 needs (G0 spec section 6 interfaces): one item kind, a status vocabulary (3-8 unordered
values), an optional whole-number quantity, holder roles (hidden; polarity only), document types, people names for S4
parties, inert note texts, ID prefixes and the O*NET persona seed. Every pack value F3 uses passes the rule-5 lint
(mechanism stems, holder-change words, XF06 markers, negcount lexicon), the 2.2 banned-word lint (R1-16) and, for
status lists, the unordered-vocabulary lint (R2-04). Values that fail are dropped; a pack that cannot supply a status
list of >= 3 values is not used by F3. Polarity tags come from the pack when it has them, else from a hash of
(pack id, value): they feed only the QC sidecar (yes = bad outcome), never a label.

Held-out packs (S5 / mix-tuning dev only): the orchestrator has not ruled the held-out pack set yet, so F3 uses the
union of the pack agents' own hints (packs-1 sha256(id) mod 8 == 0 proposal, packs-3 heldout_hint, packs-4
split_hint == heldout). Training cards never use these packs; S5 items use only these packs.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from functools import lru_cache

from f3common import (BANNED_STEM_WORDS, C_SRC, GRADED, HOLDER_CHANGE_WORDS, IMPLICIT_CUE_STEMS, L_CORE,
                      MECH_STEMS, NEI_WORDINGS, NONE_WORDINGS, GAP_MARKERS, PACKS_DIR, unit_hash, words_lower)

sys.path.insert(0, str(C_SRC / "common"))
import negcount  # noqa: E402  (orchestrator-owned counter, referenced not edited)

# words that would collide with F3's own grammar words in entries, stems and cards
GRAMMAR_WORDS = ("status", "entry", "entries", "record", "records", "current", "holder", "holders", "hold", "holds",
                 "held", "log", "notice", "change", "quantity", "transfer", "true", "yes", "still", "longer",
                 "between", "today", "now", "currently", "end", "start", "illustration", "example", "result",
                 "note", "code", "means", "here", "case", "this", "that", "is", "it")
MECH_RE = re.compile(r"\b(" + "|".join({
    "void": r"void\w*", "cancel": r"cancel\w*", "withdraw": r"withdr\w*", "amend": r"amend\w*",
    "correct": r"correct\w*", "fix": r"fix\w*", "supersede": r"supersed\w*|supersession\w*",
    "replace": r"replac\w*", "rename": r"renam\w*", "renumber": r"renumber\w*", "move": r"mov\w*",
    "retire": r"retir\w*", "merge": r"merg\w*", "consolidate": r"consolidat\w*", "absorb": r"absor\w*",
    "transfer": r"transfer\w*", "revert": r"rever\w*", "create": r"creat\w*", "adjust": r"adjust\w*",
    "missing": r"miss\w*"}.values()) + r")\b", re.I)
CUE_RE = re.compile(r"\b(lack\w*|fail\w*|den(?:y|ies|ied|ying)|refus\w*|declin\w*|omit\w*|neglect\w*|prevent\w*|"
                    r"rul(?:e|es|ed|ing) out)\b", re.I)


def _forbidden_markers():
    out = set(m.lower() for m in ("unknown", "not recorded", "none", "no", "0", "null", "false", "n/a", "tbd"))
    for w in NEI_WORDINGS + NONE_WORDINGS + GAP_MARKERS:
        out.add(w.lower())
    return out


FORBIDDEN_MARKERS = _forbidden_markers()


def lint_value(s: str, *, kind: str = "value") -> str | None:
    """None if the value passes every F3 pack lint, else a short reason code (never the value)."""
    if not isinstance(s, str) or not s.strip() or s != s.strip():
        return "empty"
    if ": " in s or "\n" in s or "'" in s or '"' in s or "|" in s or ";" in s or "," in s or "(" in s:
        return "punct"
    if len(s) > 32:
        return "long"
    low = s.lower()
    ws = words_lower(s)
    if MECH_RE.search(low):
        return "mechanism"
    for w in HOLDER_CHANGE_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            return "holder_change"
    for m in FORBIDDEN_MARKERS:
        if m in ("-", "?"):
            continue
        if re.search(r"(?<![a-z0-9])" + re.escape(m) + r"(?![a-z0-9])", low):
            return "marker"
    if any(w in L_CORE for w in ws) or CUE_RE.search(low):
        return "negcount"
    nc = negcount.count(s)
    if nc.k_all or nc.k_syn:
        return "negcount"
    if any(w in BANNED_STEM_WORDS for w in ws):
        return "banned_word"
    if any(w in GRAMMAR_WORDS for w in ws):
        return "grammar_word"
    if kind == "status":
        if any(ch.isdigit() for ch in s):
            return "digit"
        if any(w in GRADED for w in ws):
            return "graded"
    if not re.fullmatch(r"[A-Za-z][A-Za-z -]*[A-Za-z]", s):
        return "charset"
    return None


def _clean_list(vals, kind="value"):
    out, seen = [], set()
    for v in vals:
        if lint_value(v, kind=kind) is None and v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)
    return out


def _initials(s: str, n_min=2, n_max=3) -> str:
    ws = [w for w in re.findall(r"[A-Za-z]+", s)]
    ini = "".join(w[0] for w in ws).upper()
    if len(ini) < n_min:
        w = re.sub(r"[^A-Za-z]", "", s).upper()
        ini = (ini + w[1:])[:n_min]
    return ini[:n_max]


def _tag(pack_id: str, what: str, val: str) -> str:
    return "bad" if unit_hash("f3-polarity", pack_id, what, val) < 0.5 else "not bad"


HOLDER_NOUNS = (("account", "accounts"), ("unit", "units"), ("desk", "desks"), ("team", "teams"),
                ("station", "stations"), ("crew", "crews"), ("office", "offices"), ("bay", "bays"),
                ("depot", "depots"), ("section", "sections"), ("post", "posts"), ("cell", "cells"))


def _holder_noun(pack_id):
    return HOLDER_NOUNS[int(unit_hash("f3-holder-noun", pack_id) * len(HOLDER_NOUNS))]


def _plural(word: str) -> str:
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def _singular(pl: str) -> str:
    if pl.endswith("ies"):
        return pl[:-3] + "y"
    if pl.endswith(("sses", "xes", "ches", "shes")):
        return pl[:-2]
    if pl.endswith("s") and not pl.endswith("ss"):
        return pl[:-1]
    return pl


# ------------------------------------------------------------------------------------------------ per schema

def _view_p1(p):
    kind = p["item_kind"]
    statuses = [(v, _tag(p["id"], "status", v)) for v in p["status_values"]]
    qty = None
    for a in p["attributes"]:
        if a.get("type") == "int" and a.get("nonneg") and a.get("unit") not in ("%", "°C", "°F") \
                and lint_value(a["name"]) is None and lint_value(a["unit"]) is None:
            qty = {"name": a["name"], "unit": a["unit"], "high_bad": unit_hash("f3-qty", p["id"]) < 0.5}
            break
    roles = [(r, _tag(p["id"], "holding", r)) for r in p["roles"]]
    docs = [(d["type"], _tag(p["id"], "current", d["type"])) for d in p["document_types"]]
    return dict(pack_id=p["id"], pack_set="packs-1", persona_seed=p["persona_seed"]["onet_code"],
                org=p["org"]["name"], item_sg=kind["singular"], item_pl=kind["plural"], field="status",
                statuses=statuses, qty=qty, roles=roles, docs=docs, people=list(p["people"]),
                inert=list(p.get("inert_fact_types", [])),
                heldout=int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 8 == 0)


def _view_p2(p):
    et = p["entity_types"][0]
    field, statuses = None, []
    for e in p["entity_types"]:
        for a in e["attributes"]:
            if a.get("type") == "cat" and a.get("values") and 3 <= len(_clean_list(a["values"], "status")) <= 8 \
                    and lint_value(a.get("label", "")) is None:
                field = a["label"]
                statuses = [(v, _tag(p["id"], "status", v)) for v in a["values"]]
                break
        if field:
            break
    if not field:
        return None
    qty = None
    for e in p["entity_types"]:
        for a in e["attributes"]:
            if a.get("type") == "int" and a.get("unit") not in (None, "%", "percent") and lint_value(a["label"]) is None \
                    and lint_value(a["unit"]) is None and (a.get("min", 0) or 0) >= 0:
                qty = {"name": a["label"], "unit": a["unit"], "high_bad": unit_hash("f3-qty", p["id"]) < 0.5}
                break
        if qty:
            break
    people = []
    roles = [(r, _tag(p["id"], "holding", r)) for r in p["roles"]]
    docs = [(d, _tag(p["id"], "current", d)) for d in p["document_types"]]
    inert = [f["label"] for f in p.get("filler_items", [])]
    return dict(pack_id=p["id"], pack_set="packs-2", persona_seed=p["persona_seed"]["onet_code"],
                org=p["org_name"], item_sg=et["singular"], item_pl=et["plural"], field=field, statuses=statuses,
                qty=qty, roles=roles, docs=docs, people=people, inert=inert, heldout=False)


def _view_p3(p):
    kind_pl = p["item_kind"]["plural"]
    field, statuses = None, []
    for e in p["entity_types"]:
        for f in e["fields"]:
            if f.get("type") == "enum" and f.get("values") and 3 <= len(_clean_list(f["values"], "status")) <= 8:
                nm = f["name"].replace("_", " ")
                if lint_value(nm) is None:
                    field = nm
                    statuses = [(v, _tag(p["id"], "status", v)) for v in f["values"]]
                    break
        if field:
            break
    if not field:
        return None
    qty = None
    for e in p["entity_types"]:
        for f in e["fields"]:
            if f.get("type") == "int" and f.get("unit") and (f.get("range") or [0])[0] >= 0:
                nm = f["name"].replace("_", " ")
                if lint_value(nm) is None and lint_value(f["unit"]) is None:
                    hb = f.get("direction") == "high is bad" or (f.get("direction") not in ("low is bad",)
                                                                  and unit_hash("f3-qty", p["id"]) < 0.5)
                    qty = {"name": nm, "unit": f["unit"], "high_bad": hb}
                    break
        if qty:
            break
    roles = [(r["role"], "bad" if r["holding_is"] == "bad" else "not bad") for r in p["item_kind"]["holder_roles"]]
    roles += [(r, _tag(p["id"], "holding", r)) for r in p["roles"] if r not in [x for x, _ in roles]]
    docs = [(d["name"], "bad" if d["current_is"] == "bad" else "not bad") for d in p["document_types"]]
    inert = list(p.get("disjoint_fillers", [])) + list(p.get("inert_fact_types", []))
    return dict(pack_id=p["id"], pack_set="packs-3", persona_seed=p["persona_seed"], org=p["org"],
                item_sg=_singular(kind_pl), item_pl=kind_pl, field=field, statuses=statuses, qty=qty, roles=roles,
                docs=docs, people=list(p["names"]["persons"]), inert=inert, heldout=bool(p.get("heldout_hint")))


def _view_p4(p):
    it = p["items"][0]
    statuses = []
    for s in p["statuses"]:
        tag = {"adverse": "bad", "favourable": "not bad"}.get(s["tag"]) or _tag(p["id"], "status", s["name"])
        statuses.append((s["name"], tag))
    qty = None
    for q in p["quantities"]:
        if q.get("decimals") == 0 and (q.get("min") or 0) >= 0 and q["unit"] not in ("percent", "%") \
                and lint_value(q["name"]) is None and lint_value(q["unit"]) is None:
            hb = {"high": True, "low": False}.get(q.get("adverse")) if q.get("adverse") in ("high", "low") \
                else unit_hash("f3-qty", p["id"]) < 0.5
            unit = q["unit"]
            qty = {"name": q["name"], "unit": unit if unit != "count" else "items", "high_bad": hb}
            break
    roles = [(r["name"], _tag(p["id"], "holding", r["name"])) for r in p["roles"]]
    docs = [(d["name"], _tag(p["id"], "current", d["name"])) for d in p["documents"]]
    people = [x["name"] for x in p["names"]["people"]]
    inert = [x["text"] for x in p.get("inert_facts", [])]
    return dict(pack_id=p["id"], pack_set="packs-4", persona_seed=p["persona_seed"], org=p["title"],
                item_sg=it["noun"], item_pl=it["plural"], field="status", statuses=statuses, qty=qty, roles=roles,
                docs=docs, people=people, inert=inert, heldout=p.get("split_hint") == "heldout")


SOURCES = (("packs-1/packs.jsonl", _view_p1), ("packs-2/packs.jsonl", _view_p2), ("packs-3/packs-3.jsonl", _view_p3),
           ("packs-4/packs.jsonl", _view_p4))


def _finish(v):
    """Apply the lints; None if the pack cannot serve F3."""
    if v is None:
        return None, "no_status_field"
    if lint_value(v["item_sg"]) or lint_value(v["item_pl"]):
        return None, "item_kind_lint"
    if v["field"] != "status" and lint_value(v["field"]):
        return None, "field_lint"
    st = [(s, t) for s, t in v["statuses"] if lint_value(s, kind="status") is None]
    seen, st2 = set(), []
    for s, t in st:
        if s.lower() not in seen and s.lower() not in (v["item_sg"].lower(), v["item_pl"].lower()):
            seen.add(s.lower())
            st2.append((s, t))
    if len(st2) < 3:
        return None, "status_lint"
    v["statuses"] = st2[:8]
    roles = [(r, t) for r, t in v["roles"] if lint_value(r) is None]
    if not roles:
        roles = [("member", "not bad"), ("lead", "bad")]
    v["roles"] = roles
    v["docs"] = [(d, t) for d, t in v["docs"] if lint_value(d) is None]
    if v["qty"] and (lint_value(v["qty"]["name"]) or lint_value(v["qty"]["unit"])):
        v["qty"] = None
    v["people"] = [x for x in v["people"] if re.fullmatch(r"[A-Z][a-z]+(?: [A-Z][a-z'-]+)+", x)
                   and lint_value(x) is None]
    v["inert"] = [x for x in v["inert"] if _inert_ok(x)]
    hn = _holder_noun(v["pack_id"])
    v["holder_sg"], v["holder_pl"] = hn
    # ID prefixes: item, holder, record, document code; all distinct
    ip = _initials(v["item_sg"], 2, 2)
    hp = _initials(hn[0], 2, 2) if len(hn[0].split()) > 1 else (hn[0][:2].upper())
    if hp == ip:
        hp = (hn[0][0] + hn[0][-1]).upper()
    if hp == ip:
        hp = "HX"
    for bad in ("NO", "OK", "ID"):
        if ip == bad:
            ip = ip[0] + "Q"
        if hp == bad:
            hp = hp[0] + "Z"
    v["item_prefix"], v["holder_prefix"] = ip, hp
    v["quarter_key"] = v["pack_set"]
    return v, None


def _inert_ok(x: str) -> bool:
    if not isinstance(x, str) or not (3 <= len(x) <= 90) or "\n" in x or ":" in x or "'" in x or '"' in x:
        return False
    if re.search(r"\d", x) or MECH_RE.search(x) or CUE_RE.search(x):
        return False
    low = x.lower()
    if any(w in words_lower(x) for w in L_CORE + BANNED_STEM_WORDS + ("entry", "entries", "record", "status",
                                                                        "holds", "held", "notice", "change")):
        return False
    if negcount.count(x).k_all:
        return False
    return not any(m in low for m in ("unknown", "null", "false"))


@lru_cache(maxsize=None)
def load_views():
    """{pack_id: view} for every pack F3 can use, plus a drop report {reason: count}."""
    views, drops = {}, {}
    for rel, fn in SOURCES:
        with open(PACKS_DIR / rel, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                p = json.loads(line)
                try:
                    v = fn(p)
                except (KeyError, IndexError, TypeError):
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
                      "with_qty": sum(1 for v in views.values() if v["qty"]),
                      "with_docs": sum(1 for v in views.values() if len(v["docs"]) >= 1),
                      "with_people": sum(1 for v in views.values() if len(v["people"]) >= 4),
                      "with_inert": sum(1 for v in views.values() if len(v["inert"]) >= 3),
                      "by_set": {s: sum(1 for v in views.values() if v["pack_set"] == s)
                                 for s in ("packs-1", "packs-2", "packs-3", "packs-4")}}, indent=1))
