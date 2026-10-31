"""F1 view of the shared domain packs (packs-1..4): one adapter per pack schema, the F1 pack lint, and the pack split.

F1 rules applied here (G0 F1 v7): Boolean field names and true phrasings carry no counted negation and no declared
negative affix (F1R5-A01); category values likewise, never an XF06 marker word, no comma or bracket (F1R5-A01/A02);
outcome names carry no negation (F1R3-A08), no ': ', never Yes/No; presupposition declared per Boolean (F1R4-A04);
day-count fields carry their anchor event words (F1R5-A07). A field that fails is dropped; a pack left with too few
fields or outcomes is not used by F1. Held-out packs: the union of the pack builders' held-out proposals is never used for
an F1 training card; F1's S5 items and depth-sweep items draw from it (the orchestrator has not ruled a held-out set).
"""
from __future__ import annotations

import json
import re
from decimal import Decimal
from functools import lru_cache

from common import PACKS_DIR, d2o, dec, sha
import datetime as dt
import negcount

MARKER_WORDS = {"not recorded", "unknown", "null", "none", "no", "yes", "false", "true", "0", "-", "n/a", "na", "tbd", "?",
                "not applicable", "not available", "blank", "empty", "absent", "missing", "pending"}
GENERIC_AFFIX = re.compile(r"^(un|non|in|im|il|ir|dis)[a-z]{3,}$")
GENERIC_AFFIX_WORDS = {"incomplete", "invalid", "ineligible", "illegal", "improper", "insufficient", "inactive", "unpaid",
                       "unsafe", "unfit", "uncertified", "unregistered", "unlicensed", "unapproved", "unverified",
                       "unsigned", "unknown", "inadequate", "inaccurate", "incorrect", "irregular", "dishonest",
                       "disqualified", "noncompliant", "non-compliant", "nonpayment", "unresolved", "unsettled",
                       "unauthorised", "unauthorized", "unendorsed", "uninsured", "unlisted", "unreported", "unused"}
BAD_WORDS = {"reject", "refuse", "return", "hold", "defer", "delay", "suspend", "void", "cancel", "withdraw", "refer",
             "escalate", "block", "stop", "revoke", "fine", "penalty", "impound", "quarantine", "close", "decline",
             "recall", "scrap", "pause", "freeze", "remove", "reduce", "restrict", "warn", "charge", "investigate",
             "audit", "review", "send", "flag", "bar", "ban", "evict", "terminate", "retest", "redo", "rework",
             "downgrade", "detain", "seize", "lock", "deny", "dismiss", "drop", "skip", "postpone", "wait", "queue"}
GOOD_WORDS = {"approve", "grant", "accept", "post", "list", "renew", "issue", "release", "allow", "pay", "admit",
              "award", "clear", "proceed", "go", "confirm", "ship", "book", "enrol", "enroll", "register", "certify",
              "keep", "fund", "open", "sign", "publish", "credit", "count", "permit", "pass", "spray", "launch",
              "fast", "full", "settle", "refund", "upgrade", "extend", "waive", "reinstate", "restore", "start"}

_WORD = re.compile(r"[a-z0-9]+")


def norm_name(s: str) -> str:
    """Normalized key for name matching (also what the parser uses): lower-case alnum words joined by one space;
    camelCase is split."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    return " ".join(_WORD.findall(s.lower()))


BANNED_IN_NAMES = re.compile(r"\b(provided that|as long as|notwithstanding|except|if and only if|neither|other than|"
                             r"up to|until|through|prior to|since|as of|expires|unless|only if|subject to|either|"
                             r"or|nor|not recorded|unknown|null|switched off|in force|applies|apply)\b", re.I)


def neg_free(text: str, affixed=()) -> bool:
    if BANNED_IN_NAMES.search(text):
        return False
    c = negcount.count(text, affixed=tuple(affixed))
    if c.k_syn or c.k_all:
        return False
    for w in re.findall(r"[a-z][a-z\-]+", text.lower()):
        if w in GENERIC_AFFIX_WORDS or w in affixed:
            return False
        if w.startswith(("un", "non")) and len(w) > 5 and w not in {"under", "unit", "units", "union", "unique",
                                                                     "universal", "university", "until", "uniform",
                                                                     "unified", "united", "unload", "unloading"}:
            return False
    return True


def clean_name(s: str) -> str:
    return " ".join(str(s).replace("_", " ").split())


def _valence_hint(name: str):
    ws = set(_WORD.findall(name.lower()))
    stems = {w[:5] for w in ws}
    b = any(w in ws or w[:5] in stems for w in BAD_WORDS)
    g = any(w in ws or w[:5] in stems for w in GOOD_WORDS)
    if b and not g:
        return "bad"
    if g and not b:
        return "good"
    return None


def _num_attr(key, name, unit, places, step, lo, hi, money=False):
    step = dec(step) if step is not None else Decimal(1).scaleb(-int(places or 0))
    places = int(places or 0)
    if step < Decimal(1).scaleb(-places):
        step = Decimal(1).scaleb(-places)
    lo, hi = dec(lo), dec(hi)
    # snap to grid
    lo = (lo / step).to_integral_value(rounding="ROUND_CEILING") * step
    hi = (hi / step).to_integral_value(rounding="ROUND_FLOOR") * step
    n = clean_name(name).lower()
    unit = clean_name(unit or "").strip()
    day = unit.lower() in ("days", "day") and ("day" in n)
    anchor = None
    if day:
        m = re.search(r"days? (?:since|after|from|in|of|on|at|before)\s+(.+)$", n)
        anchor = m.group(1) if m else n.replace("days", "").strip()
    return {"key": key, "name": n, "type": "num", "unit": unit, "places": places, "step": str(step),
            "lo": str(lo), "hi": str(hi), "money": bool(money), "daycount": day, "anchor": anchor}


def _date_attr(key, name):
    return {"key": key, "name": clean_name(name).lower(), "type": "date"}


def _cat_attr(key, name, values):
    vals = [clean_name(v) for v in values]
    return {"key": key, "name": clean_name(name).lower(), "type": "cat", "values": vals}


def _aux_neg(clause: str):
    """'X is/was/are/were Y' -> 'X is not Y' (non-occurrence / absence cue); None if no auxiliary."""
    m = re.match(r"^(.*?\b)(is|are|was|were|has been|have been)\b(.*)$", clause)
    if not m:
        return None
    head, aux, rest = m.groups()
    if aux in ("has been", "have been"):
        a1, a2 = aux.split()
        return f"{head}{a1} not {a2}{rest}"
    return f"{head}{aux} not{rest}"


def _bool_attr(key, name, kind, true_t, false_t, presup):
    return {"key": key, "name": clean_name(name).lower(), "type": "bool", "kind": kind or "state",
            "true": true_t, "false": false_t, "presup": presup}


def _article(np: str) -> str:
    return ("an " if np[:1].lower() in "aeiou" else "a ") + np


# ------------------------------------------------------------------ adapters

def _date_window(lo: str | None, hi: str | None, span: int | None = None):
    try:
        a = dt.date.fromisoformat(lo) if lo else dt.date(2027, 1, 1)
    except ValueError:
        a = dt.date(2027, 1, 1)
    if hi:
        b = dt.date.fromisoformat(hi)
    else:
        b = a + dt.timedelta(days=span or 730)
    if (b - a).days < 400:
        b = a + dt.timedelta(days=730)
    return d2o(a), d2o(b)


def adapt_p1(r):
    attrs = []
    for a in r.get("attributes", []):
        t = a.get("type")
        if t in ("int", "num"):
            attrs.append(_num_attr(a["aid"], a["name"], a.get("unit"), a.get("decimals", 0), a.get("grid"),
                                   a["range"][0], a["range"][1], money=False))
        elif t in ("cat", "ord"):
            attrs.append(_cat_attr(a["aid"], a["name"], a.get("values", [])))
        elif t == "date":
            attrs.append(_date_attr(a["aid"], a["name"]))
        elif t == "bool":
            nm = clean_name(a["name"]).lower()
            if a.get("kind") == "event":
                tt, ft = f"there was {_article(nm)}", f"there was no {nm}"
            else:
                tt, ft = f"there is {_article(nm)}", f"there is no {nm}"
            attrs.append(_bool_attr(a["aid"], nm, a.get("kind"), tt, ft, a.get("presupposes")))
    outs = [{"name": clean_name(o), "tag": None} for s in r.get("outcome_sets", []) for o in s.get("outcomes", [])]
    ik = r.get("item_kind") or {}
    ids = []
    for p in r.get("id_pool", []):
        ids = p.get("ids", [])
        break
    return {
        "pack_id": r["id"], "agent": "packs-1", "persona_seed": (r.get("persona_seed") or {}).get("onet_code"),
        "deciding_role": r.get("deciding_role"), "org": (r.get("org") or {}).get("name"),
        "subject": {"noun": clean_name(ik.get("singular", "case")).lower(),
                    "plural": clean_name(ik.get("plural", "cases")).lower(), "ids": ids},
        "attrs": attrs, "outcomes": outs,
        "scope": r.get("scope_dimension") or None,
        "inert_facts": list(r.get("inert_fact_types", [])), "people": list(r.get("people", [])),
        "orgs": list(r.get("partner_orgs", [])), "roles": list(r.get("roles", [])),
        "doc_types": [d.get("type") for d in r.get("document_types", [])],
        "affixed": list(r.get("affixed_negatives", [])),
        "date_window": _date_window(None, None),
        "heldout_proposal": None,
    }


def adapt_p2(r):
    ents = r.get("entity_types", [])
    case = next((e for e in ents if e.get("role") == "case"), ents[0] if ents else {})
    attrs = []
    for a in case.get("attributes", []):
        t = a.get("type")
        key = f"{r['id']}:{a['key']}"
        if t in ("int", "dec1", "dec2", "money", "decimal", "pct"):
            attrs.append(_num_attr(key, a.get("label", a["key"]), a.get("unit"), a.get("places", 0), a.get("grid"),
                                   a.get("min", 0), a.get("max", 100), money=(t == "money")))
        elif t in ("cat", "ord"):
            attrs.append(_cat_attr(key, a.get("label", a["key"]), a.get("values", [])))
        elif t == "date":
            attrs.append(_date_attr(key, a.get("label", a["key"])))
        elif t == "boolean":
            pos, neg = a.get("pos_statement"), a.get("neg_statement")
            if not pos:
                continue
            tt = pos.replace("{E}", "{S}")
            ft = neg.replace("{E}", "{S}") if neg else None
            pres = a.get("presupposes")
            attrs.append(_bool_attr(key, a.get("label", a["key"]), a.get("kind"), tt, ft,
                                    f"{r['id']}:{pres}" if pres else None))
    outs = []
    for s in r.get("outcome_sets", []):
        for o in s.get("outcomes", []):
            outs.append({"name": clean_name(o["name"]), "tag": "bad" if o.get("adverse") else "good"})
    dw = r.get("date_window") or {}
    return {
        "pack_id": r["id"], "agent": "packs-2", "persona_seed": (r.get("persona_seed") or {}).get("onet_code"),
        "deciding_role": r.get("decider_role"), "org": r.get("org_name"),
        "subject": {"noun": clean_name(case.get("singular", "case")).lower(),
                    "plural": clean_name(case.get("plural", "cases")).lower(), "ids": list(case.get("ids", []))},
        "attrs": attrs, "outcomes": outs, "scope": r.get("scope_dimension") or None,
        "inert_facts": [f.get("label") for f in r.get("filler_items", []) if f.get("label")],
        "people": [], "orgs": list(r.get("source_names", [])), "roles": list(r.get("roles", [])),
        "doc_types": [d if isinstance(d, str) else d.get("name", "") for d in r.get("document_types", [])],
        "affixed": [w.get("word") for w in r.get("affixed_words", []) if w.get("word")],
        "date_window": _date_window(dw.get("start"), None, dw.get("span_days")),
        "heldout_proposal": None,
    }


def adapt_p3(r):
    ents = r.get("entity_types", [])
    case = ents[0] if ents else {}
    attrs = []
    for f in case.get("fields", []):
        t = f.get("type")
        key = f"{r['id']}:{f['name']}"
        if t in ("int", "dec", "pct", "amt"):
            rng = f.get("range") or [0, 100]
            places = f.get("places", 0)
            attrs.append(_num_attr(key, f["name"], f.get("unit"), places, None, rng[0], rng[1], money=(t == "amt")))
        elif t in ("enum", "status"):
            attrs.append(_cat_attr(key, f["name"], f.get("values", [])))
        elif t == "date":
            attrs.append(_date_attr(key, f["name"]))
    for b in r.get("boolean_facts", []):
        ph = b.get("phrase")
        if not ph:
            continue
        pres = b.get("presupposes")
        nm = re.sub(r"^(the|a|an) ", "", ph.strip())
        if len(nm) > 48:
            continue
        attrs.append(_bool_attr(f"{r['id']}:{b['id']}", nm, b.get("kind"), ph, _aux_neg(ph),
                                f"{r['id']}:{pres}" if pres else None))
    outs = [{"name": clean_name(o), "tag": None} for s in r.get("outcome_sets", []) for o in s]
    pool = []
    for k, v in (r.get("id_schemes") or {}).items():
        if k == case.get("id_key"):
            pool = list(v.get("pool", []))
    names = r.get("names") or {}
    return {
        "pack_id": r["id"], "agent": "packs-3", "persona_seed": (r.get("persona_seed") or {}).get("onet_code")
        if isinstance(r.get("persona_seed"), dict) else r.get("persona_seed"),
        "deciding_role": r.get("decider_role"), "org": (r.get("org") or {}).get("name") if isinstance(r.get("org"), dict)
        else r.get("org"),
        "subject": {"noun": clean_name(case.get("name", "case")).lower(),
                    "plural": clean_name(case.get("plural", "cases")).lower(), "ids": pool},
        "attrs": attrs, "outcomes": outs, "scope": r.get("scope_dimension") or None,
        "inert_facts": list(r.get("inert_fact_types", [])), "people": list(names.get("persons", [])),
        "orgs": list(names.get("organisations", [])), "roles": list(r.get("roles", [])),
        "doc_types": [d.get("name", d) if isinstance(d, dict) else d for d in r.get("document_types", [])],
        "affixed": [w.get("negated") for w in r.get("affixed_words", []) if w.get("negated")],
        "date_window": _date_window(None, None),
        "heldout_proposal": bool(r.get("heldout_hint")),
    }


def adapt_p4(r):
    attrs = []
    for q in r.get("quantities", []):
        attrs.append(_num_attr(q["id"], q["name"], q.get("unit"), q.get("decimals", 0), q.get("step"),
                               q.get("min", 0), q.get("max", 100), money=False))
    for c in r.get("cat_fields", []):
        attrs.append(_cat_attr(c["id"], c["name"], [v["name"] for v in c.get("values", [])]))
    seen = set()
    for e in r.get("entity_types", []):
        for f in e.get("fields", []):
            w = f.get("word", "")
            if ("date" in w or f.get("key", "").endswith("_date")) and w not in seen:
                seen.add(w)
                attrs.append(_date_attr(f["id"], w))
    for b in r.get("bool_fields", []):
        nm = clean_name(b["name"]).lower()
        ph = "the " + nm if not nm.startswith(("a ", "an ", "the ")) else nm
        nm = re.sub(r"^(the|a|an) ", "", nm)
        attrs.append(_bool_attr(b["id"], nm, b.get("kind"), ph, _aux_neg(ph), b.get("presupposes")))
    outs = []
    for o in r.get("outcomes", []):
        tag = {"favourable": "good", "adverse": "bad"}.get(o.get("tag"))
        outs.append({"name": clean_name(o["name"]), "tag": tag})
    ents = r.get("entity_types", [])
    case = ents[0] if ents else {}
    dw = r.get("date_window") or {}
    names = r.get("names") or {}
    return {
        "pack_id": r["id"], "agent": "packs-4", "persona_seed": r.get("persona_seed"),
        "deciding_role": (r.get("persona") or {}).get("deciding_role"), "org": r.get("title"),
        "subject": {"noun": clean_name(case.get("noun", "case")).lower(),
                    "plural": clean_name(case.get("plural", "cases")).lower(), "ids": [],
                    "id_format": case.get("id_format")},
        "attrs": attrs, "outcomes": outs, "scope": None,
        "inert_facts": [x.get("text") for x in r.get("inert_facts", []) if x.get("text")],
        "people": [p["name"] for p in names.get("people", [])],
        "orgs": [o["name"] for o in names.get("organisations", [])][1:],
        "roles": [x["name"] for x in r.get("roles", [])],
        "doc_types": [d.get("name") for d in r.get("documents", [])],
        "affixed": [p.get("negative") for p in r.get("neg_affix_pairs", []) if p.get("negative")],
        "date_window": _date_window(dw.get("start"), dw.get("end")),
        "heldout_proposal": r.get("split_hint") == "heldout",
    }


@lru_cache(maxsize=1)
def _p1_heldout():
    m = json.load(open(PACKS_DIR / "packs-1" / "manifest.json"))
    return set((m.get("heldout_proposal") or {}).get("ids", []))


# ------------------------------------------------------------------ lint

def lint_pack(u: dict) -> tuple[dict, list]:
    """Return (linted pack, problems). Fields / outcomes that fail F1 rules are dropped."""
    probs = []
    aff = tuple(w.lower() for w in u.get("affixed", []) if w)
    keep = []
    seen_norm = set()
    for a in u["attrs"]:
        nm = a["name"]
        if not nm or not re.fullmatch(r"[a-z0-9][a-z0-9' \-]*", nm) or len(nm) > 48 or "--" in nm:
            probs.append(("field_name_chars", a["key"]))
            continue
        if not neg_free(nm, aff):
            probs.append(("field_name_negation", a["key"]))
            continue
        if norm_name(nm) in seen_norm or norm_name(nm) in ("case id", "case", "outcome", "row", "notice", "rule"):
            probs.append(("field_name_dup", a["key"]))
            continue
        if a["type"] == "cat":
            vals = []
            for v in a["values"]:
                vl = v.lower()
                if (vl in MARKER_WORDS or any(ch in v for ch in ",()[];:|/") or " and " in f" {vl} "
                        or " or " in f" {vl} " or not neg_free(v, aff) or not re.fullmatch(r"[A-Za-z0-9' \-]+", v)):
                    continue
                vals.append(v)
            # distinct under normalization; no value contains another
            vals2 = []
            for v in vals:
                if any(norm_name(v) == norm_name(w) for w in vals2):
                    continue
                vals2.append(v)
            vals2 = [v for v in vals2 if not any(v != w and norm_name(v) in norm_name(w).split(" ") for w in vals2)]
            if len(vals2) < 3:
                probs.append(("cat_values", a["key"]))
                continue
            a = {**a, "values": vals2[:6]}
        if a["type"] == "bool":
            tt = a.get("true")
            if not tt or not neg_free(tt.replace("{S}", "the case"), aff) or any(ch in tt for ch in ",;:()[]"):
                probs.append(("bool_true_phrase", a["key"]))
                continue
            ft = a.get("false")
            if ft:
                low = " " + ft.replace("{S}", "X").lower() + " "
                cue_ok = any(c in low for c in (" has no ", " have no ", " had no ", " lacks ", " lacked ", " did not ",
                                                 " does not ", " failed to ", " was not ", " were not ", " is no ",
                                                 " was no ", " there is no ", " there was no "))
                if not cue_ok or any(ch in ft for ch in ",;:()[]"):
                    a = {**a, "false": None}
        if a["type"] == "num":
            lo, hi, st = Decimal(a["lo"]), Decimal(a["hi"]), Decimal(a["step"])
            if hi <= lo or (hi - lo) / st < 6 or not re.fullmatch(r"[A-Za-z%°µ/ ²³\.\-]*", a["unit"] or ""):
                probs.append(("num_range", a["key"]))
                continue
            if not a["unit"]:
                a = {**a, "unit": "units"}
        seen_norm.add(norm_name(nm))
        keep.append(a)
    # field names: none contains another (parser longest match is still used, this keeps text unambiguous)
    names = [a["name"] for a in keep]
    keep2 = []
    for a in keep:
        if any(a["name"] != b and (f" {a['name']} " in f" {b} ") for b in names):
            probs.append(("field_name_contained", a["key"]))
            continue
        keep2.append(a)
    keys = {a["key"] for a in keep2}
    for a in keep2:
        if a["type"] == "bool" and a.get("presup") and a["presup"] not in keys:
            a["presup_missing"] = True  # presupposed field not in the pack's F1 view: the phrasing presupposes a
            # field the row can never have, so R8 holds trivially (no field Q on the row)
    outs = []
    for o in u["outcomes"]:
        nm = o["name"]
        if (not nm or ": " in nm or nm.lower() in ("yes", "no") or not neg_free(nm, aff) or len(nm) > 40
                or any(ch in nm for ch in ",;:()[]|/") or not re.fullmatch(r"[A-Za-z0-9' \-]+", nm)):
            continue
        if any(norm_name(nm) == norm_name(x["name"]) for x in outs):
            continue
        tag = o.get("tag") or _valence_hint(nm)
        outs.append({"name": nm, "tag": tag})
    # no outcome name contains another (row 39)
    outs = [o for o in outs if not any(o is not p and f" {norm_name(o['name'])} " in f" {norm_name(p['name'])} "
                                       for p in outs)]
    u2 = {**u, "attrs": keep2, "outcomes": outs}
    return u2, probs


def pack_usable(u: dict) -> tuple[bool, str]:
    t = {}
    for a in u["attrs"]:
        t[a["type"]] = t.get(a["type"], 0) + 1
    if t.get("date", 0) < 1:
        return False, "no date field"
    if t.get("num", 0) < 2:
        return False, "too few numeric fields"
    if t.get("num", 0) + t.get("cat", 0) + t.get("bool", 0) < 6:
        return False, "too few fields"
    if len(u["outcomes"]) < 3:
        return False, "too few outcomes"
    if not u.get("org"):
        return False, "no org"
    return True, "ok"


@lru_cache(maxsize=1)
def load_all() -> dict:
    out = {}
    srcs = [("packs-1/packs.jsonl", adapt_p1), ("packs-2/packs.jsonl", adapt_p2), ("packs-3/packs-3.jsonl", adapt_p3),
            ("packs-4/packs.jsonl", adapt_p4)]
    ho1 = _p1_heldout()
    for rel, fn in srcs:
        with open(PACKS_DIR / rel, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                u = fn(r)
                if u["agent"] == "packs-1":
                    u["heldout_proposal"] = u["pack_id"] in ho1
                u["pack_sha256"] = sha(line.strip())
                u2, probs = lint_pack(u)
                ok, why = pack_usable(u2)
                u2["lint_problems"] = probs
                u2["usable"] = ok
                u2["unusable_reason"] = None if ok else why
                out[u2["pack_id"]] = u2
    return out


def split_packs():
    """(training pack ids, held-out pack ids) in a fixed program order. Held-out = builders' held-out proposals."""
    allp = load_all()
    train, held = [], []
    for pid in sorted(allp):
        u = allp[pid]
        if not u["usable"]:
            continue
        (held if u.get("heldout_proposal") else train).append(pid)
    return train, held


if __name__ == "__main__":
    allp = load_all()
    from collections import Counter
    c = Counter((u["agent"], u["usable"], u["unusable_reason"]) for u in allp.values())
    for k, v in sorted(c.items(), key=str):
        print(k, v)
    tr, ho = split_packs()
    print("train", len(tr), "heldout", len(ho))
    pc = Counter(p[0] for u in allp.values() for p in u["lint_problems"])
    print(pc)
