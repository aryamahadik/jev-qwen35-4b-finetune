"""Pack adapter for F7: domain packs (packs-2 for training cards, packs-3 held-out packs for S5) -> F7 pack IR.

F7 pack IR (one dict per pack): entity naming, Boolean factors (f7factors, linted), numeric / date / ordered-category
attributes from the pack, inert attributes (pack disjointness list), filler items (shared pool filtered by stem
disjointness, U01), concept sets (term, alias, pack synonyms) and "about" keys (H02). Lints follow spec 2.2 and 3.1.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from f7factors import FACTORS, HELDOUT_FACTORS
from f7lex import (BANNED_STEMS, FILLER_EVENTS, FILLER_STATES, LEVEL_NAMES, MULTI_BANNED, NEG_IN_NAME,
                   OPERATOR_WORDS, PARTIAL_BANNED)

LEAN = Path(__file__).resolve().parents[3]
PACKS2 = LEAN / "c_src/packs/packs-2/packs.jsonl"
PACKS3 = LEAN / "c_src/packs/packs-3/packs-3.jsonl"

EXTRA_OPS = {"on", "of", "in", "to", "be", "been", "was", "were", "are", "it", "they", "this", "that", "the"}
STOP = {"a", "an", "the", "of", "to", "for", "by", "with", "on", "in", "at", "from", "per", "and", "or", "its"}
LEVEL_NAME_WORDS = {w.lower() for g in LEVEL_NAMES.values() for seq in g for w in seq}


def _tokens(s: str) -> list[str]:
    return re.findall(r"[a-z]+(?:[-'][a-z]+)*", s.lower())


def stem(w: str) -> str:
    w = w.lower()
    for suf in ("ations", "ation", "ings", "ing", "ments", "ment", "ions", "ion", "ers", "er", "ies", "es", "ed", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def stems(s: str) -> set[str]:
    out = set()
    for t in _tokens(s):
        for part in t.split("-"):
            if part and part not in STOP and len(part) > 2:
                out.add(stem(part))
    return out


def lint_name(s: str, *, allow_ops: bool = False) -> list[str]:
    """Spec 2.2 / 3.1 name lints for factor, alias, filler and attribute names. Returns the problems found."""
    p = []
    low = s.lower()
    toks = _tokens(s)
    if re.search(r"\d", s):
        p.append("digit")
    parts = [x for t in toks for x in t.split("-")]
    if any(t in NEG_IN_NAME for t in toks + parts) or any(t.startswith(("un", "non")) and len(t) > 5 and t not in
                                                  ("union", "unit", "units", "unique", "uniform", "university")
                                                  for t in toks):
        p.append("negation cue")
    if any(t in BANNED_STEMS for t in toks):
        p.append("banned stem")
    if re.search(r"\b(will|intends|scheduled|due|aims|should|could|likely|probably|proposed|pending|upcoming|"
                 r"forecast|projected|estimated|anticipated)\b", low):
        p.append("future or modal word")
    for w in PARTIAL_BANNED + MULTI_BANNED:
        if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            p.append(f"banned word {w!r}")
    if not allow_ops and any(t in OPERATOR_WORDS or t in EXTRA_OPS for t in toks):
        p.append("operator word")
    if any(t in LEVEL_NAME_WORDS for t in toks):
        p.append("level-name word")
    if re.search(r"[;:()\[\]|=,\"]", s):
        p.append("punctuation")
    if s != s.strip() or "  " in s:
        p.append("spacing")
    return p


def article(term: str) -> str:
    return "an" if term[0].lower() in "aeiou" and not term.lower().startswith(("uni", "use", "eu")) else "a"


def _parse_entry(e: str) -> tuple:
    e = e.strip()
    kind, pol = e[0], e[1]
    rest = e[2:].strip()
    term, alias = [x.strip() for x in rest.split("|")]
    return kind, pol, term, alias


def _np(s: str) -> tuple[str, str]:
    """('~x' -> ('x', '')), ('a x' -> ('x', 'a')), ('x' -> ('x', 'a'/'an'))."""
    if s.startswith("~"):
        return s[1:], ""
    for d in ("a ", "an "):
        if s.startswith(d):
            return s[len(d):], d.strip()
    return s, article(s)


def build_factors(spec: str, pack_id: str) -> tuple[list, list]:
    out, dropped = [], []
    seen = set()
    for i, e in enumerate(spec.split(";")):
        kind, pol, term, alias = _parse_entry(e)
        t, dt = _np(term)
        a, da = _np(alias)
        if lint_name(t):
            if not lint_name(a) and a.lower() not in seen:
                dropped.append({"pack": pack_id, "term": t, "why": lint_name(t), "replaced_by_alias": a})
                t, dt, a, da = a, da, None, None
            else:
                dropped.append({"pack": pack_id, "term": t, "why": lint_name(t)})
                continue
        if t.lower() in seen:
            continue
        if a is not None and (lint_name(a) or a.lower() == t.lower()):
            a, da = None, None
        seen.add(t.lower())
        concept = {t.lower()} | ({a.lower()} if a else set())
        out.append({"key": f"f{i:02d}", "term": t, "det": dt, "alias": a, "alias_det": da,
                    "kind": "event" if kind == "E" else "state", "pol": "adverse" if pol == "+" else "favourable",
                    "about": f"{pack_id}:f{i:02d}", "concept": sorted(concept),
                    "stems": sorted(stems(t) | (stems(a) if a else set()))})
    return out, dropped


def _grid(typ: str, lo: float, hi: float) -> Fraction:
    span = hi - lo
    if typ in ("int",):
        return Fraction(1)
    if typ == "dec1":
        return Fraction(1, 10) if span <= 100 else Fraction(1)
    if typ == "dec2":
        return Fraction(1, 100) if span <= 10 else Fraction(1, 10)
    if typ in ("money", "amt"):
        return Fraction(1) if span <= 5000 else (Fraction(10) if span <= 100000 else Fraction(100))
    if typ in ("dec", "num"):
        return Fraction(1, 10) if span <= 100 else Fraction(1)
    if typ == "pct":
        return Fraction(1)
    return Fraction(1)


def _date_term(a: dict) -> str | None:
    syn = list((a.get("concept_set") or {}).get("synonyms") or [])
    for s in syn:
        if s.endswith(" date") and not lint_name(s):
            return s
    return None


def _id_gen(prefix: str, pattern: str | None, rng: random.Random, n: int, taken: set) -> list[str]:
    L = "ABCDEFGHJKMNPQRSTUVWXYZ"
    D = "0123456789"
    out = []
    while len(out) < n:
        if pattern:
            body = "".join(rng.choice(L) if ch == "A" else rng.choice(D) for ch in pattern)
        else:
            body = rng.choice(L) + "".join(rng.choice(D) for _ in range(3))
        s = prefix + body
        if s not in taken:
            taken.add(s)
            out.append(s)
    return out


@lru_cache(maxsize=None)
def load_packs2() -> tuple:
    rows = [json.loads(l) for l in open(PACKS2, encoding="utf-8")]
    return tuple(rows)


@lru_cache(maxsize=None)
def load_packs3() -> tuple:
    rows = [json.loads(l) for l in open(PACKS3, encoding="utf-8")]
    return tuple(rows)


def _fillers(all_rubric_stems: set) -> list[dict]:
    out = []
    for kind, pool in (("event", FILLER_EVENTS), ("state", FILLER_STATES)):
        for s in pool:
            t, d = _np(s)
            if lint_name(t):
                continue
            st = stems(t)
            if st & all_rubric_stems:
                continue
            out.append({"term": t, "det": d, "kind": kind, "stems": sorted(st)})
    # pairwise disjoint (H02 for fillers): drop later items sharing a stem with an earlier one
    keep, used = [], set()
    for f in out:
        if set(f["stems"]) & used:
            continue
        used |= set(f["stems"])
        keep.append(f)
    return keep


def pack2_ir(p: dict) -> dict:
    pid = p["id"]
    et = [e for e in p["entity_types"] if e.get("role") == "case"][0]
    factors, dropped = build_factors(FACTORS[pid], pid)
    nums, dates, ords = [], [], []
    for a in et["attributes"]:
        t = a.get("label") or ""
        if a["type"] in ("int", "money", "dec1", "dec2"):
            unit = a.get("unit") or ""
            if lint_name(t) or not unit or re.search(r"\d", unit) or lint_name(unit, allow_ops=True):
                continue
            lo, hi = float(a["min"]), float(a["max"])
            r = _grid(a["type"], lo, hi)
            lo_f = Fraction(lo).limit_denominator(1000)
            hi_f = Fraction(hi).limit_denominator(1000)
            lo_g = (lo_f / r).__ceil__() * r
            hi_g = (hi_f / r).__floor__() * r
            if (hi_g - lo_g) / r < 40:
                continue
            nums.append({"key": a["key"], "term": t, "unit": unit, "int": a["type"] == "int", "r": r,
                         "lo": lo_g, "hi": hi_g, "about": f"{pid}:{a.get('concept_group') or a['key']}",
                         "concept": sorted({m.lower() for m in (a.get("concept_set") or {}).get("members", [t])}),
                         "stems": sorted(stems(" ".join((a.get("concept_set") or {}).get("members", [t]))))})
        elif a["type"] == "date":
            dt = _date_term(a)
            if not dt:
                continue
            dates.append({"key": a["key"], "term": dt, "about": f"{pid}:{a.get('concept_group') or a['key']}",
                          "concept": sorted({m.lower() for m in (a.get("concept_set") or {}).get("members", [dt])}),
                          "stems": sorted(stems(" ".join((a.get("concept_set") or {}).get("members", [dt]))))})
        elif a["type"] == "ord":
            vals = list(a.get("values") or [])
            if lint_name(t) or len(vals) < 3:
                continue
            bad = False
            for v in vals:
                if lint_name(v) or re.search(r"\b(first|second|third|fourth|final|one|two|three|four|five)\b", v.lower()):
                    bad = True
                if len(v.strip()) <= 2:
                    bad = True
            if bad:
                continue
            ords.append({"key": a["key"], "term": t, "ranks": vals, "about": f"{pid}:{a.get('concept_group') or a['key']}",
                         "concept": sorted({m.lower() for m in (a.get("concept_set") or {}).get("members", [t])}),
                         "stems": sorted(stems(" ".join((a.get("concept_set") or {}).get("members", [t]) + vals)))})
    rubric_stems = set()
    for x in factors + nums + dates + ords:
        rubric_stems |= set(x["stems"])
    inert = []
    for a in p.get("inert_attributes", []):
        t = a.get("label") or ""
        vals = [v for v in (a.get("values") or []) if isinstance(v, str) and not lint_name(v, allow_ops=True)
                and not re.search(r"\d", v) and not (set(_tokens(v)) & LEVEL_NAME_WORDS)]
        if lint_name(t) or len(vals) < 2 or stems(t) & rubric_stems:
            continue
        if any(stems(v) & rubric_stems for v in vals):
            continue
        inert.append({"key": a["key"], "term": t, "values": vals})
    rng = random.Random(int(hashlib.sha256(("ids:" + pid).encode()).hexdigest()[:12], 16))
    fmt = et.get("id_format") or {}
    ids = [i for i in et.get("ids", []) if isinstance(i, str)]
    taken = set(ids)
    ids += _id_gen(fmt.get("prefix", "ID-"), fmt.get("body_pattern"), rng, 400, taken)
    singular = et["singular"]
    if lint_name(singular, allow_ops=True):
        singular = "case"
    roles = [r for r in p.get("roles", []) if not lint_name(r, allow_ops=True)][:6] or ["intake desk", "review desk"]
    return {"id": pid, "source": "packs-2", "persona_seed": (p.get("persona_seed") or {}).get("onet_code"),
            "org": p.get("org_name"), "singular": singular, "plural": et.get("plural") or singular + "s",
            "ids": ids, "roles": roles, "factors": factors, "dropped": dropped, "nums": nums, "dates": dates,
            "ords": ords, "inert": inert, "fillers": _fillers(rubric_stems | {stem(w) for w in _tokens(singular)}),
            "date_start": (p.get("date_window") or {}).get("start", "2029-01-01"),
            "date_span": int((p.get("date_window") or {}).get("span_days", 730)),
            "currency": (p.get("currency") or {}).get("unit")}


def pack3_ir(p: dict) -> dict:
    pid = p["id"]
    et = p["entity_types"][0]
    # r1b: packs-3 training packs (not held out) carry no factor list: S6 CUT cards read one quantity only
    factors, dropped = build_factors(HELDOUT_FACTORS[pid], pid) if pid in HELDOUT_FACTORS else ([], [])
    nums = []
    for f in et["fields"]:
        if f["type"] not in ("int", "amt", "dec", "pct"):
            continue
        t = f["name"].replace("_", " ")
        unit = f.get("unit") or ""
        if t.endswith(" year") or "grade" in t or lint_name(t) or not unit or lint_name(unit, allow_ops=True):
            continue
        lo, hi = [float(x) for x in f["range"]]
        typ = {"amt": "amt", "dec": "dec1", "pct": "int", "int": "int"}[f["type"]]
        r = _grid(typ, lo, hi)
        lo_g = (Fraction(lo).limit_denominator(1000) / r).__ceil__() * r
        hi_g = (Fraction(hi).limit_denominator(1000) / r).__floor__() * r
        if (hi_g - lo_g) / r < 10:
            continue
        nums.append({"key": f["name"], "term": t, "unit": unit, "int": typ == "int", "r": r, "lo": lo_g, "hi": hi_g,
                     "about": f"{pid}:{f['name']}", "concept": [t], "stems": sorted(stems(t))})
    rubric_stems = set()
    for x in factors + nums:
        rubric_stems |= set(x["stems"])
    rng = random.Random(int(hashlib.sha256(("ids:" + pid).encode()).hexdigest()[:12], 16))
    ids = _id_gen(et.get("id_prefix", "ID") + "-", "DDDD", rng, 400, set())
    inert = []
    for i, x in enumerate(p.get("inert_fact_types", [])):
        pass  # packs-3 inert types are phrases, not attribute/value pairs; S5 uses no inert sentences beyond M4 tests
    return {"id": pid, "source": "packs-3", "persona_seed": p.get("persona_seed"), "org": p.get("org"),
            "singular": et["name"], "plural": et.get("plural") or et["name"] + "s", "ids": ids,
            "roles": ["intake desk", "review desk"], "factors": factors, "dropped": dropped, "nums": nums,
            "dates": [], "ords": [], "inert": inert,
            "fillers": _fillers(rubric_stems), "date_start": "2029-01-01", "date_span": 730,
            "level_names": p.get("level_names")}


@lru_cache(maxsize=None)
def training_packs() -> tuple:
    return tuple(pack2_ir(p) for p in load_packs2())


@lru_cache(maxsize=None)
def training_packs3() -> tuple:
    """r1b: packs-3 packs that are not held out (heldout_hint false and not one of F7's S5 dev packs) and state at
    least one quantity with room for 7 ranges; used for S6 CUT cards only (one pack per card, X03)."""
    out = []
    for p in load_packs3():
        if p["id"] in HELDOUT_FACTORS or p.get("heldout_hint"):
            continue
        ir = pack3_ir(p)
        if any((a["hi"] - a["lo"]) / a["r"] >= 38 for a in ir["nums"]):
            out.append(ir)
    return tuple(out)


@lru_cache(maxsize=None)
def heldout_packs() -> tuple:
    return tuple(pack3_ir(p) for p in load_packs3() if p["id"] in HELDOUT_FACTORS)


def pack_summary() -> dict:
    tp, hp = training_packs(), heldout_packs()
    return {"training_packs": len(tp), "heldout_packs": len(hp),
            "factors_kept": sum(len(p["factors"]) for p in tp + hp),
            "factors_dropped_by_lint": sum(len(p["dropped"]) for p in tp + hp),
            "nums": sum(len(p["nums"]) for p in tp), "dates": sum(len(p["dates"]) for p in tp),
            "ords": sum(len(p["ords"]) for p in tp), "inert": sum(len(p["inert"]) for p in tp),
            "fillers_min": min(len(p["fillers"]) for p in tp + hp)}


if __name__ == "__main__":
    print(json.dumps(pack_summary(), indent=1))
    for p in training_packs() + heldout_packs():
        if len(p["factors"]) < 8 or len(p["nums"]) < 2:
            print(p["id"], len(p["factors"]), len(p["nums"]), len(p["dates"]), len(p["ords"]), len(p["fillers"]),
                  [d["term"] for d in p["dropped"]])


@lru_cache(maxsize=None)
def _persona_map() -> dict:
    return {p["id"]: p["persona_seed"] for p in training_packs() + heldout_packs()}


def load_persona(pack_id: str):
    return _persona_map().get(pack_id)


@lru_cache(maxsize=None)
def _packs_index() -> dict:
    # r1g: packs-3 training packs (S6 CUT cards, r1b) were missing here, so the finalize gates (f7gates G3 re-parse)
    # raised KeyError on 'pk3-...' rows; lookup only, generation unchanged
    out = {}
    for p in training_packs() + heldout_packs() + training_packs3():
        out.setdefault(p["id"], p)
    return out


def pack_by_id(pack_id: str) -> dict:
    p = _packs_index().get(pack_id)
    if p is None:
        raise KeyError(pack_id)
    return p
