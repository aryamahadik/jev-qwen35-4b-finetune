#!/usr/bin/env python3
"""packs-4 builder: domain packs for invented and fictional settings (C_DATA_SPEC v4 2.1, step 3 of section 11).

Quarter: fictional organisations, invented technologies, games and leagues with invented rules, space colonies and
fantasy guilds. Every pack forces definition-following over world knowledge: its jargon, units, currency, statuses
and rules exist only inside the pack.

Authoring. Claude writes each pack in a compact text form (`src/batch_*.py`, a list `PACKS` of dicts of strings). This
program parses, lints and expands them into `packs.jsonl` (schema `c_pack.v1`, one JSON object per line, every object
and every sub-object carries a stable `id`). Persona seeds come from `persona_draw.json` (O*NET 31.0 main titles drawn
by program, `draw_personas.py`); a pack's `id` fixes its seed and its theme, so no seed or theme is hand-picked.

Schema c_pack.v1 (keys of one pack; sub-object ids are `<pack id>.<section>.<slug>`):
  id, schema, pack_set, theme, title, setting                    pack name and a 2-4 sentence setting
  persona {id, persona_seed, onet_title, major_group, deciding_role}  the O*NET title seeds the deciding role (F4)
  persona_seed                                                    O*NET-SOC code (copied to rows as meta.persona_seed)
  roles [{id, name, decider}]                                     the decider first
  names {people, organisations, places} [{id, name}]              invented names only
  entity_types [{id, noun, plural, id_key, id_format, fields[{id, key, word}]}]
                                                                  id_format: '#' digit, '@' capital letter; one ID key
                                                                  per type (F12 R2-01); field words map to keys
  umbrella {id, noun, plural}                                       umbrella noun for all entity types (F4)
  items [{id, noun, plural}]                                      holdable or transferable items (F3)
  sources {trusted, untrusted} [{id, name}]                       attribution sources (F4 source map)
  documents [{id, name, register}]                                document types and their register
  currency {id, name, plural, sub, sub_plural, sub_per_main}      invented money (F2 resolution unit = sub or main)
  units [{id, name, plural, abbr, definition}]                    invented units, defined in the pack
  quantities [{id, name, unit, min, max, step, decimals, adverse}] number ranges; adverse in high|low|none
  date_window {id, start, end}                                      Gregorian ISO dates (families need real calendars)
  bool_fields [{id, name, kind, adverse_pole, presupposes, aliases}]
                                                                  affirmative names (negcount k_all = 0); kind
                                                                  event|state (F7 U02); adverse_pole true|false|none;
                                                                  presupposes = id of the Boolean field a phrasing of
                                                                  this one presupposes (F1 R8), or null; aliases = the
                                                                  declared alias part of the concept set (F7 U01)
  cat_fields [{id, name, ordered, values[{id, name, tag, rank}]}] tag adverse|favourable|neutral; rank on ordered fields
  statuses, outcomes [{id, name, tag}]                            record statuses and decision outcomes with polarity
  predicates [{id, entity_type, phrase, adverse_pole}]            unary predicates (F4); adverse pole true|false|none
  links [{id, from, to, active, passive}]                         directional binary links (F4: one active, one passive)
  actions [{id, verb, synonyms, effect, kind}]                    closed action lexicon (F12); effect protective|
                                                                  favourable|neutral (F8 action rules); kind read|write
  risk_events [{id, name}]                                        adverse events for risk and probability cards (F8)
  taxonomy_dims [{id, name, values[{id, name}]}]                  attribute dimensions for fine-grained codes (F11)
  jargon [{id, term, definition}]                                 invented terms with in-pack definitions (F10 seeds;
                                                                  F10 still runs its own >= 300K 3-language check)
  neg_affix_pairs [{id, positive, negative}]                      SEM-18 affixed negation words the pack declares (F1,
                                                                  F5); declared words never appear in any name
  inert_facts [{id, text}]                                        background facts that state no condition, threshold,
                                                                  status or outcome (F4 inert, F7 disjointness seeds)
  parents, licence, split_hint                                    split_hint: 'heldout' when sha256("packsplit:" + id)
                                                                  mod 10 == 0, else 'train' (a hint; the orchestrator
                                                                  and family generators own the held-out choice)

Lint (all must pass; a failing pack is not written):
  - section minimum counts; unique names inside each section; ids unique;
  - every name-like string (roles, names, nouns, fields, statuses, outcomes, values, predicates, verbs, items, units,
    risk events, jargon terms) has negcount k_all = 0 (shared c_src/common/negcount.py) and holds no negating-affix
    word unless that word is declared in neg_affix_pairs (and declared words never occur in names);
  - no value equals a XF06 marker (markers.json banned + word markers, plus yes/no/on/off/true/false/null);
  - jargon terms: not in the local word list (/usr/share/dict/web2, public domain; a pre-filter only) and no banned
    morphology affix; terms unique across the whole pack set;
  - quantities: min < max, step > 0, min and max on the step grid; date window valid;
  - presupposes, link and predicate types refer to declared entries;
  - (fix round 1, review of 3 Oct) inert facts name none of their own pack's decision words: whole-word match, with
    simple inflections (-s, -es, -ies, and the singular of a plural), against statuses, outcomes, risk events,
    Boolean field names and aliases, category field names and all their values, taxonomy dimension names and values,
    quantity names, jargon terms and predicate phrases (every entry of >= 3 characters);
  - ROUGE-L (LCS F-measure on lower-case words) < 0.7 between any two packs' setting texts (G11), and (fix round 1)
    between any two inert facts, any two unit definitions and any two jargon definitions of the whole pack set, under
    both word splits used in review ([a-z]+ with hyphens kept, and [a-z0-9']+).

Usage (from this folder):  ../../../../.venv/bin/python build_packs.py [--check-only]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(LEAN))
from c_src.common.negcount import count as negcount  # noqa: E402

SCHEMA = "c_pack.v1"
PACK_SET = "packs-4"
THEMES = {"fictional_org", "invented_tech", "game_league", "space_colony", "fantasy_guild"}
TAGS = {"b": "adverse", "g": "favourable", "n": "neutral"}
POLES = {"T": "true", "F": "false", "N": "none"}
EFFECTS = {"p": "protective", "f": "favourable", "n": "neutral"}
REGISTERS = {"memo", "log", "ticket", "notice", "report", "form", "ledger", "chat", "minutes", "letter", "manual",
             "schedule", "bulletin", "register", "certificate", "roster", "manifest", "transcript", "logbook"}
MINS = {"people": 12, "orgs": 5, "places": 5, "types": 3, "items": 3, "src_t": 3, "src_u": 3, "docs": 5, "units": 2,
        "qty": 5, "bools": 8, "cats": 2, "statuses": 5, "outcomes": 4, "preds": 5, "links": 3, "actions": 6,
        "risks": 3, "tax": 3, "jargon": 6, "inert": 6, "roles": 4}
PARENTS = ["O*NET 31.0 Database, occupation_data.csv (main occupation titles; gd_onet_occupation)"]
LICENCE = ("CC0 1.0 (Claude-written pack text). The persona seed is an O*NET 31.0 occupation title (CC BY 4.0, "
           "USDOL/ETA), recorded by code; credit O*NET in the third-party notices file")
BANNED_MORPH = ("phobia", "itis", "mal", "ology", "ism", "cide", "mania", "pseudo", "anti", "osis", "ectomy",
                "philia")
NEG_PREFIX = re.compile(r"^(un|non|dis|in|im|il|ir|mis)(-)?([a-z]{3,})$")
NEG_SUFFIX = re.compile(r"^([a-z]{3,})less(ness)?$")
# Real words that start like a negating affix but do not negate a stem (reviewed by hand; the lint prints new ones).
AFFIX_OK = {"impound", "insure", "intake", "missing", "discard", "injury", "dismiss", "infraction", "ingrid",
            "dispatch", "illustration", "mismatch", "misreading", "union", "until", "investment", "intact", "ilsley",
            "disqualify", "disqualified", "misrating", "distinct", "ilona", "imrie", "increase", "irwin", "miscount", "disallow",
            "inside", "ilian", "disease", "imbert", "informed", "units", "imani", "instead", "under", "until",
            "unit", "uniform", "unique", "universal", "discovery", "dispatched", "dispute", "disputed", "distance",
            "distant", "district", "disturbance", "imagery", "imbral", "imbrals", "impounded", "incident", "included",
            "includes", "injured", "inspect", "inspected", "inspector", "instrument", "insured", "involved",
            "miscounted", "mislabelled", "underage", "underreporting", "underweight", "dispatcher", "install",
            "installed", "installer", "misfire", "mismatched", "mismatches", "ingram", "institute", "distinction", "impression", "discarded",
            "distribute", "misdeal", "dismissed", "disputes", "impose"}


def load_words():
    p = Path("/usr/share/dict/web2")
    return {w.strip().lower() for w in p.read_text(errors="ignore").splitlines() if w.strip()} if p.exists() else set()


WORDS = load_words()


def load_markers():
    """XF06 marker words (classes, dash/case forms, family-local markers) plus words some families ban as values
    (pending, maybe, partial, not stated, not available, ~) and F8's record-status words. Exact whole-value match."""
    m = json.loads((LEAN / "c_src" / "common" / "markers.json").read_text())
    out = {"yes", "no", "on", "off", "true", "false", "null", "~", "pending", "maybe", "partial", "not stated",
           "not available", "not yet received", "on file", "documented", "registered", "reported", "record", "log"}
    for c in m["classes"].values():
        out |= {w.lower() for w in c.get("words", []) + c.get("same_marker_forms", []) if isinstance(w, str)}
    for f in m["families"].values():
        for ws in (f.get("local") or {}).values():
            out |= {w.lower() for w in ws if isinstance(w, str)}
    return out


MARKERS = load_markers()


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s[:48] or "x"


def split(s: str, sep: str = ";") -> list[str]:
    return [x.strip() for x in s.split(sep) if x.strip()]


class Lint:
    def __init__(self, pid):
        self.pid, self.errors, self.affix_flags = pid, [], set()

    def err(self, msg):
        self.errors.append(f"{self.pid}: {msg}")


def words_of(s):
    return re.findall(r"[a-z]+(?:-[a-z]+)*", s.lower())


def check_name(L: Lint, s: str, where: str, declared_neg: set[str]):
    if not s:
        L.err(f"empty name in {where}")
        return
    if s.strip().lower() in MARKERS:
        L.err(f"marker value '{s}' in {where}")
    nc = negcount(s, affixed=tuple(declared_neg))
    if nc.k_all:
        L.err(f"negation cue in {where}: '{s}' (k_all {nc.k_all})")
    for w in words_of(s):
        for part in w.split("-") if "-" in w and not w.startswith("non-") else [w]:
            if part in declared_neg:
                L.err(f"declared negative word '{part}' used in name ({where})")
            m = NEG_PREFIX.match(part)
            if m and part not in AFFIX_OK and (m.group(1) in ("un", "non") or stem_known(m.group(3))):
                L.affix_flags.add(part)
            m = NEG_SUFFIX.match(part)
            if m and m.group(1) in WORDS and part not in AFFIX_OK:
                L.affix_flags.add(part)
        if w.startswith("non-") or w.startswith("non"):
            if w not in AFFIX_OK and w.replace("non-", "").replace("non", "", 1) in WORDS:
                L.affix_flags.add(w)


def stem_known(st: str) -> bool:
    """The stem after a negating prefix is a known word, allowing simple inflections (web2 lists lemmas only)."""
    cands = {st, st[:-1], st[:-2], st[:-3], st[:-2] + "e" if st.endswith("ed") else st, st[:-3] + "e"}
    if st.endswith("ied"):
        cands.add(st[:-3] + "y")
    return any(c in WORDS for c in cands if len(c) >= 3)


def uniq(L, items, where, key=lambda x: x):
    seen = set()
    for it in items:
        k = key(it).lower()
        if k in seen:
            L.err(f"duplicate in {where}: '{key(it)}'")
        seen.add(k)


def id_ok(fmt):
    return bool(re.fullmatch(r"[A-Z@#][A-Z0-9@#\-/.]{2,15}", fmt)) and "#" in fmt


def decimals_of(step: str) -> int:
    return len(step.split(".")[1]) if "." in step else 0


def on_grid(v: float, step: float) -> bool:
    q = v / step
    return abs(q - round(q)) < 1e-9


def expand(raw: dict, draw: dict) -> tuple[dict, Lint]:
    pid = raw["id"]
    L = Lint(pid)
    P = lambda sec: f"{pid}.{sec}"  # noqa: E731
    for k in MINS:
        if k not in raw:
            L.err(f"missing section {k}")
    if L.errors:
        return {}, L
    neg_pairs = []
    for x in split(raw.get("negpairs", "")):
        pos, _, neg = x.partition("/")
        neg_pairs.append({"id": f"{P('negaffix')}.{slug(neg)}", "positive": pos.strip(), "negative": neg.strip()})
    declared = {p["negative"].lower() for p in neg_pairs}

    def named_list(sec, sep=";"):
        vals = split(raw[sec], sep)
        if len(vals) < MINS[sec]:
            L.err(f"{sec}: {len(vals)} < {MINS[sec]}")
        uniq(L, vals, sec)
        for v in vals:
            check_name(L, v, sec, declared)
        return vals

    role = raw["role"].strip()
    check_name(L, role, "role", declared)
    others = named_list("roles")
    if role.lower() in {o.lower() for o in others}:
        L.err("deciding role repeated in roles")
    roles = [{"id": f"{P('role')}.{slug(role)}", "name": role, "decider": True}] + \
            [{"id": f"{P('role')}.{slug(r)}", "name": r, "decider": False} for r in others]

    people = named_list("people", ",")
    for p_ in people:
        if len(p_.split()) < 2:
            L.err(f"person needs given and family name: '{p_}'")
    orgs, places = named_list("orgs"), named_list("places")
    names = {"people": [{"id": f"{P('person')}.{slug(x)}", "name": x} for x in people],
             "organisations": [{"id": f"{P('org')}.{slug(x)}", "name": x} for x in orgs],
             "places": [{"id": f"{P('place')}.{slug(x)}", "name": x} for x in places]}

    types = []
    for t in split(raw["types"]):
        parts = [x.strip() for x in t.split("|")]
        if len(parts) != 4:
            L.err(f"types entry needs noun|plural|ID|fields: '{t}'")
            continue
        noun, plural, fmt, flds = parts
        for s in (noun, plural):
            check_name(L, s, "types", declared)
        if not id_ok(fmt):
            L.err(f"bad id_format '{fmt}'")
        fl = [f.strip() for f in flds.split(",") if f.strip()]
        if len(fl) < 3:
            L.err(f"type '{noun}' needs >= 3 fields")
        uniq(L, fl, f"fields of {noun}")
        for f in fl:
            check_name(L, f, f"fields of {noun}", declared)
        tid = f"{P('type')}.{slug(noun)}"
        types.append({"id": tid, "noun": noun, "plural": plural, "id_key": f"{slug(noun)}_id", "id_format": fmt,
                      "fields": [{"id": f"{tid}.field.{slug(f)}", "key": slug(f), "word": f} for f in fl]})
    if len(types) < MINS["types"]:
        L.err("types < 3")
    uniq(L, types, "types", key=lambda x: x["noun"])
    uniq(L, [t["id_format"] for t in types], "id formats")
    tnouns = {t["noun"].lower(): t["id"] for t in types}

    un, _, upl = raw.get("umbrella", "").partition("|")
    if not un.strip():
        L.err("missing umbrella")
    check_name(L, un.strip(), "umbrella", declared)

    items = []
    for x in split(raw["items"]):
        noun, _, plural = x.partition("|")
        check_name(L, noun.strip(), "items", declared)
        items.append({"id": f"{P('item')}.{slug(noun)}", "noun": noun.strip(), "plural": plural.strip() or noun.strip() + "s"})
    if len(items) < MINS["items"]:
        L.err("items < 3")
    uniq(L, items, "items", key=lambda x: x["noun"])

    src_t, src_u = named_list("src_t"), named_list("src_u")
    sources = {"trusted": [{"id": f"{P('source')}.{slug(x)}", "name": x} for x in src_t],
               "untrusted": [{"id": f"{P('source')}.{slug(x)}", "name": x} for x in src_u]}
    uniq(L, src_t + src_u, "sources")

    docs = []
    for x in split(raw["docs"]):
        name, _, reg = x.rpartition(":")
        if reg.strip() not in REGISTERS:
            L.err(f"doc register '{reg}' not in list")
        check_name(L, name.strip(), "docs", declared)
        docs.append({"id": f"{P('doc')}.{slug(name)}", "name": name.strip(), "register": reg.strip()})
    if len(docs) < MINS["docs"]:
        L.err("docs < 5")
    uniq(L, docs, "docs", key=lambda x: x["name"])

    mparts = [x.strip() for x in raw["money"].split("|")]
    if len(mparts) != 5 or not mparts[4].isdigit():
        L.err("money needs name|plural|sub|subplural|per")
        mparts = (mparts + ["", "", "", "", "100"])[:5]
    for s in mparts[:4]:
        check_name(L, s, "money", declared)
    currency = {"id": f"{P('currency')}.{slug(mparts[0])}", "name": mparts[0], "plural": mparts[1],
                "sub": mparts[2], "sub_plural": mparts[3], "sub_per_main": int(mparts[4] or 100)}

    units = []
    for x in split(raw["units"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 4:
            L.err(f"unit needs name|plural|abbr|definition: '{x}'")
            continue
        check_name(L, parts[0], "units", declared)
        units.append({"id": f"{P('unit')}.{slug(parts[0])}", "name": parts[0], "plural": parts[1], "abbr": parts[2],
                      "definition": parts[3]})
    if len(units) < MINS["units"]:
        L.err("units < 2")
    uniq(L, units, "units", key=lambda x: x["name"])
    unit_names = {u["name"].lower() for u in units} | {currency["name"].lower(), currency["sub"].lower(),
                                                        "count", "percent", "days", "hours", "minutes", "years", "weeks"}

    qty = []
    for x in split(raw["qty"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 6:
            L.err(f"qty needs name|unit|min|max|step|adverse: '{x}'")
            continue
        name, unit, lo, hi, step, adv = parts
        check_name(L, name, "qty", declared)
        if unit.lower() not in unit_names:
            L.err(f"qty '{name}' unit '{unit}' not declared")
        try:
            lo_f, hi_f, st_f = float(lo), float(hi), float(step)
            if not (lo_f < hi_f and st_f > 0 and on_grid(lo_f, st_f) and on_grid(hi_f, st_f)):
                L.err(f"qty '{name}' range/step bad")
        except ValueError:
            L.err(f"qty '{name}' numbers bad")
            continue
        if adv not in ("high", "low", "none"):
            L.err(f"qty '{name}' adverse '{adv}'")
        dec = decimals_of(step)
        qty.append({"id": f"{P('qty')}.{slug(name)}", "name": name, "unit": unit, "min": lo_f if dec else int(lo_f),
                    "max": hi_f if dec else int(hi_f), "step": st_f if dec else int(st_f), "decimals": dec,
                    "adverse": adv})
    if len(qty) < MINS["qty"]:
        L.err("qty < 5")
    uniq(L, qty, "qty", key=lambda x: x["name"])

    d0, _, d1 = raw["dates"].partition("..")
    try:
        a, b = datetime.date.fromisoformat(d0.strip()), datetime.date.fromisoformat(d1.strip())
        if not (a < b and (b - a).days >= 180 and 1901 <= a.year and b.year <= 2099):
            L.err("date window bad")
    except ValueError:
        L.err("date window not ISO")
    date_window = {"id": f"{pid}.date_window", "start": d0.strip(), "end": d1.strip()}

    bools = []
    for x in split(raw["bools"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 5:
            L.err(f"bool needs name|kind|pole|presupposes|aliases: '{x}'")
            continue
        name, kind, pole, pre, al = parts
        check_name(L, name, "bools", declared)
        if kind not in ("event", "state"):
            L.err(f"bool '{name}' kind '{kind}'")
        if pole not in POLES:
            L.err(f"bool '{name}' pole '{pole}'")
        aliases = [y.strip() for y in al.split(",") if y.strip()]
        for y in aliases:
            check_name(L, y, f"aliases of {name}", declared)
        bools.append({"id": f"{P('bool')}.{slug(name)}", "name": name, "kind": kind,
                      "adverse_pole": POLES.get(pole, "none"), "presupposes": pre or None, "aliases": aliases})
    if len(bools) < MINS["bools"]:
        L.err("bools < 8")
    uniq(L, bools, "bools", key=lambda x: x["name"])
    bmap = {b_["name"].lower(): b_["id"] for b_ in bools}
    for b_ in bools:
        if b_["presupposes"]:
            tgt = bmap.get(b_["presupposes"].lower())
            if not tgt or tgt == b_["id"]:
                L.err(f"bool '{b_['name']}' presupposes unknown '{b_['presupposes']}'")
            b_["presupposes"] = tgt
    all_alias = [a_ for b_ in bools for a_ in b_["aliases"]] + [b_["name"] for b_ in bools]
    uniq(L, all_alias, "bool names and aliases")

    cats = []
    for x in split(raw["cats"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 3 or parts[2] not in ("ordered", "nominal"):
            L.err(f"cat needs name|v:tag,...|ordered|nominal: '{x}'")
            continue
        name, vals, kind = parts
        check_name(L, name, "cats", declared)
        cid = f"{P('cat')}.{slug(name)}"
        vv = []
        for i, v in enumerate([y.strip() for y in vals.split(",") if y.strip()]):
            vn, _, tg = v.rpartition(":")
            if tg not in TAGS:
                L.err(f"cat '{name}' value '{v}' tag")
            check_name(L, vn, f"values of {name}", declared)
            vv.append({"id": f"{cid}.{slug(vn)}", "name": vn, "tag": TAGS.get(tg, "neutral"),
                       "rank": i if kind == "ordered" else None})
        if len(vv) < 3:
            L.err(f"cat '{name}' < 3 values")
        uniq(L, vv, f"values of {name}", key=lambda z: z["name"])
        cats.append({"id": cid, "name": name, "ordered": kind == "ordered", "values": vv})
    if len(cats) < MINS["cats"]:
        L.err("cats < 2")

    def tagged(sec):
        out = []
        for v in split(raw[sec], ","):
            vn, _, tg = v.rpartition(":")
            if tg not in TAGS:
                L.err(f"{sec} '{v}' tag")
            check_name(L, vn, sec, declared)
            out.append({"id": f"{P(sec[:-1])}.{slug(vn)}", "name": vn, "tag": TAGS.get(tg, "neutral")})
        if len(out) < MINS[sec]:
            L.err(f"{sec} < {MINS[sec]}")
        uniq(L, out, sec, key=lambda z: z["name"])
        if not any(o["tag"] == "adverse" for o in out) or not any(o["tag"] != "adverse" for o in out):
            L.err(f"{sec} needs both adverse and non-adverse entries")
        return out

    statuses, outcomes = tagged("statuses"), tagged("outcomes")

    preds = []
    for x in split(raw["preds"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 3:
            L.err(f"pred needs type|phrase|pole: '{x}'")
            continue
        t, ph, pole = parts
        if t.lower() not in tnouns:
            L.err(f"pred type '{t}' undeclared")
        check_name(L, ph, "preds", declared)
        if pole not in POLES:
            L.err(f"pred '{ph}' pole")
        preds.append({"id": f"{P('pred')}.{slug(ph)}", "entity_type": tnouns.get(t.lower()), "phrase": ph,
                      "adverse_pole": POLES.get(pole, "none")})
    if len(preds) < MINS["preds"]:
        L.err("preds < 5")
    uniq(L, preds, "preds", key=lambda z: z["phrase"])

    links = []
    for x in split(raw["links"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 4:
            L.err(f"link needs from|active|passive|to: '{x}'")
            continue
        f, act, pas, t = parts
        for s in (act, pas):
            check_name(L, s, "links", declared)
        if f.lower() not in tnouns or t.lower() not in tnouns:
            L.err(f"link '{act}' types bad ({f} -> {t})")
        links.append({"id": f"{P('link')}.{slug(act)}", "from": tnouns.get(f.lower()), "to": tnouns.get(t.lower()),
                      "active": act, "passive": pas})
    if len(links) < MINS["links"]:
        L.err("links < 3")
    uniq(L, links, "links", key=lambda z: z["active"])

    actions = []
    for x in split(raw["actions"]):
        parts = [y.strip() for y in x.split("|")]
        if len(parts) != 4:
            L.err(f"action needs verb|synonyms|effect|kind: '{x}'")
            continue
        verb, syn, eff, kind = parts
        syns = [y.strip() for y in syn.split(",") if y.strip()]
        for s in [verb] + syns:
            check_name(L, s, "actions", declared)
        if eff not in EFFECTS or kind not in ("read", "write"):
            L.err(f"action '{verb}' effect/kind")
        actions.append({"id": f"{P('action')}.{slug(verb)}", "verb": verb, "synonyms": syns,
                        "effect": EFFECTS.get(eff, "neutral"), "kind": kind})
    if len(actions) < MINS["actions"]:
        L.err("actions < 6")
    if not any(a_["kind"] == "read" for a_ in actions):
        L.err("actions need >= 1 read action")
    uniq(L, [w for a_ in actions for w in [a_["verb"]] + a_["synonyms"]], "action verbs and synonyms")

    risks = named_list("risks")
    risk_events = [{"id": f"{P('risk')}.{slug(x)}", "name": x} for x in risks]

    tax = []
    for x in split(raw["tax"]):
        name, _, vals = x.partition("|")
        vv = [y.strip() for y in vals.split(",") if y.strip()]
        check_name(L, name.strip(), "tax", declared)
        for v in vv:
            check_name(L, v, f"tax {name}", declared)
        if len(vv) < 4:
            L.err(f"tax dim '{name}' < 4 values")
        uniq(L, vv, f"tax {name}")
        did = f"{P('taxdim')}.{slug(name)}"
        tax.append({"id": did, "name": name.strip(), "values": [{"id": f"{did}.{slug(v)}", "name": v} for v in vv]})
    if len(tax) < MINS["tax"]:
        L.err("tax < 3")

    jargon = []
    for x in split(raw["jargon"]):
        term, _, defi = x.partition("=")
        term, defi = term.strip(), defi.strip()
        check_name(L, term, "jargon", declared)
        for w in words_of(term):
            if w in WORDS or (w.endswith("s") and w[:-1] in WORDS):
                L.err(f"jargon term '{term}' has dictionary word '{w}'")
            if any(w.startswith(m) or w.endswith(m) for m in BANNED_MORPH):
                L.err(f"jargon term '{term}' carries morphology hint")
        if len(defi.split()) < 5:
            L.err(f"jargon '{term}' definition too short")
        jargon.append({"id": f"{P('jargon')}.{slug(term)}", "term": term, "definition": defi})
    if len(jargon) < MINS["jargon"]:
        L.err("jargon < 6")
    uniq(L, jargon, "jargon", key=lambda z: z["term"])

    inert = split(raw["inert"])
    if len(inert) < MINS["inert"]:
        L.err("inert < 6")
    inert_facts = [{"id": f"{P('inert')}.{i + 1:02d}", "text": x} for i, x in enumerate(inert)]
    for x in inert:
        if negcount(x).k_all:
            L.err(f"inert fact has a negation cue: '{x}'")

    # a declared negative word may not appear in any name-like string of the pack
    for p in neg_pairs:
        check_name(L, p["positive"], "negpairs positive", set())

    if raw.get("title", "").strip() == "" or len(raw.get("setting", "").split()) < 25:
        L.err("title or setting missing/short")
    if draw["theme"] not in THEMES:
        L.err("theme")
    pack = {
        "id": pid, "schema": SCHEMA, "pack_set": PACK_SET, "theme": draw["theme"], "title": raw["title"].strip(),
        "setting": raw["setting"].strip(),
        "persona": {"id": f"{pid}.persona", "persona_seed": draw["persona_seed"], "onet_title": draw["onet_title"],
                    "major_group": draw["major_group"], "deciding_role": role},
        "persona_seed": draw["persona_seed"],
        "roles": roles, "names": names, "entity_types": types,
        "umbrella": {"id": f"{pid}.umbrella", "noun": un.strip(), "plural": upl.strip() or un.strip() + "s"},
        "items": items, "sources": sources, "documents": docs, "currency": currency, "units": units,
        "quantities": qty, "date_window": date_window, "bool_fields": bools, "cat_fields": cats,
        "statuses": statuses, "outcomes": outcomes, "predicates": preds, "links": links, "actions": actions,
        "risk_events": risk_events, "taxonomy_dims": tax, "jargon": jargon, "neg_affix_pairs": neg_pairs,
        "inert_facts": inert_facts, "parents": PARENTS, "licence": LICENCE,
        "split_hint": "heldout" if int(hashlib.sha256(f"packsplit:{pid}".encode()).hexdigest(), 16) % 10 == 0
        else "train",
    }
    # inert facts are disjoint filler (F4 inert, F7 disjointness, F11): they may not name a decision word of the pack
    vocab = decision_vocab(pack)
    for f in inert_facts:
        hits = inert_vocab_hits(f["text"], vocab)
        if hits:
            L.err(f"inert fact {f['id']} names in-pack decision vocabulary: "
                  + ", ".join(sorted({f'{k}:{v}' for k, v in hits})))
    # every id unique inside the pack
    ids = []

    def walk(o):
        if isinstance(o, dict):
            if "id" in o:
                ids.append(o["id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(pack)
    if len(ids) != len(set(ids)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        L.err(f"duplicate ids: {dup[:5]}")
    return pack, L


def wtoks(s: str) -> list[str]:
    """Word split for the inert-fact vocabulary check: lower-case runs of letters and digits (hyphen and apostrophe
    split words, so 'sale-day' is 'sale day' and "judges'" is 'judges')."""
    return re.findall(r"[a-z0-9]+", s.lower())


def decision_vocab(pack: dict) -> list[tuple[str, str]]:
    """Every decision word of a pack: the strings a family uses as a condition, label, value or term."""
    v = [("status", s["name"]) for s in pack["statuses"]] + [("outcome", s["name"]) for s in pack["outcomes"]]
    v += [("risk_event", s["name"]) for s in pack["risk_events"]]
    for b_ in pack["bool_fields"]:
        v += [("bool_field", b_["name"])] + [("bool_alias", a_) for a_ in b_["aliases"]]
    for c in pack["cat_fields"]:
        v += [("cat_field", c["name"])] + [("cat_value", x["name"]) for x in c["values"]]
    for t in pack["taxonomy_dims"]:
        v += [("tax_dim", t["name"])] + [("tax_value", x["name"]) for x in t["values"]]
    v += [("quantity", q["name"]) for q in pack["quantities"]]
    v += [("jargon", j["term"]) for j in pack["jargon"]]
    v += [("predicate", p["phrase"]) for p in pack["predicates"]]
    return [(k, x) for k, x in v if len(x.strip()) >= 3]


def phrase_forms(phrase: str) -> set[str]:
    """The phrase and simple inflections of its last word (plural -s/-es/-ies, singular of a plural)."""
    ws = wtoks(phrase)
    if not ws:
        return set()
    last = ws[-1]
    forms = {last, last + "s", last + "es"}
    if last.endswith("y"):
        forms.add(last[:-1] + "ies")
    if last.endswith("ies"):
        forms.add(last[:-3] + "y")
    if last.endswith("es"):
        forms.add(last[:-2])
    if last.endswith("s"):
        forms.add(last[:-1])
    return {" ".join(ws[:-1] + [f]) for f in forms if f}


def inert_vocab_hits(text: str, vocab: list[tuple[str, str]]) -> list[tuple[str, str]]:
    t = " " + " ".join(wtoks(text)) + " "
    return [(k, x) for k, x in vocab if any(" " + f + " " in t for f in phrase_forms(x))]


def g11_pairs(items, toks_fns, thr=0.7):
    """All pairs (id_a, id_b, score) with ROUGE-L >= thr under any of the word splits; a bag-overlap bound skips most
    pairs (LCS <= multiset overlap)."""
    out = []
    for fn in toks_fns:
        T = [(i, fn(t)) for i, t in items]
        C = [__import__("collections").Counter(t) for _, t in T]
        for a in range(len(T)):
            ia, ta = T[a]
            for b in range(a + 1, len(T)):
                ib, tb = T[b]
                if not ta or not tb:
                    continue
                m = sum((C[a] & C[b]).values())
                if 2 * m / (len(ta) + len(tb)) < thr:
                    continue
                l_ = lcs(ta, tb)
                s = 2 * l_ / (len(ta) + len(tb))
                if s >= thr:
                    out.append((ia, ib, round(s, 3)))
    return sorted(set(out))


def toks_review(s: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", s.lower())


def lcs(a, b):
    if len(a) < len(b):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    ta, tb = words_of(a), words_of(b)
    if not ta or not tb:
        return 0.0
    l_ = lcs(ta, tb)
    if l_ == 0:
        return 0.0
    p, r = l_ / len(tb), l_ / len(ta)
    return 2 * p * r / (p + r)


def load_raw():
    raws = []
    for f in sorted((HERE / "src").glob("batch_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for r in mod.PACKS:
            r["_src"] = f.name
            raws.append(r)
    return raws


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--only", help="comma list of pack ids to lint")
    args = ap.parse_args()
    draws = {d["id"]: d for d in json.loads((HERE / "persona_draw.json").read_text())["draws"]}
    raws = load_raw()
    if args.only:
        keep = set(args.only.split(","))
        raws = [r for r in raws if r["id"] in keep]
    packs, errors, flags = [], [], {}
    seen = set()
    for r in raws:
        if r["id"] in seen:
            errors.append(f"{r['id']}: duplicate pack id")
            continue
        seen.add(r["id"])
        if r["id"] not in draws:
            errors.append(f"{r['id']}: no persona draw")
            continue
        pack, L = expand(r, draws[r["id"]])
        errors += L.errors
        if L.affix_flags:
            flags[r["id"]] = sorted(L.affix_flags)
        if not L.errors:
            packs.append(pack)
    # cross-pack checks
    jt = {}
    for p in packs:
        for j in p["jargon"]:
            jt.setdefault(j["term"].lower(), []).append(p["id"])
    for t, ps in jt.items():
        if len(ps) > 1:
            errors.append(f"jargon term '{t}' in several packs {ps}")
    titles = {}
    for p in packs:
        titles.setdefault(p["title"].lower(), []).append(p["id"])
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f"title '{t}' repeated {ps}")
    worst = (0.0, None)
    for i in range(len(packs)):
        for j in range(i + 1, len(packs)):
            s = rouge_l(packs[i]["setting"], packs[j]["setting"])
            if s > worst[0]:
                worst = (s, (packs[i]["id"], packs[j]["id"]))
            if s >= 0.7:
                errors.append(f"setting ROUGE-L {s:.2f} >= 0.7: {packs[i]['id']} {packs[j]['id']}")
    # G11 on the short Claude seeds of the whole pack set (fix round 1): inert facts, unit and jargon definitions
    for what, items in (("inert fact", [(f["id"], f["text"]) for p in packs for f in p["inert_facts"]]),
                        ("unit definition", [(u["id"], u["definition"]) for p in packs for u in p["units"]]),
                        ("jargon definition", [(j["id"], j["definition"]) for p in packs for j in p["jargon"]])):
        for a, b, s in g11_pairs(items, (words_of, toks_review)):
            errors.append(f"{what} ROUGE-L {s:.3f} >= 0.7: {a} {b}")
    for e in errors:
        print("ERROR", e)
    for k, v in flags.items():
        print("AFFIX?", k, v)
    print(f"packs ok {len(packs)} / {len(raws)}; errors {len(errors)}; affix flags {sum(map(len, flags.values()))}; "
          f"max setting ROUGE-L {worst[0]:.3f} {worst[1]}")
    if args.check_only or args.only:
        return 1 if errors else 0
    if errors:
        print("not written: fix errors first")
        return 1
    packs.sort(key=lambda p: p["id"])
    out = HERE / "packs.jsonl"
    with out.open("w") as fh:
        for p in packs:
            fh.write(json.dumps(p, ensure_ascii=False, sort_keys=False) + "\n")
    print("wrote", out, len(packs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
