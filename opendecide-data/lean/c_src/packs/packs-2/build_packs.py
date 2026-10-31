#!/usr/bin/env python3
"""packs-2 builder: expand Claude-written pack sources (src/sec_*.py) into full domain packs (C_DATA_SPEC v4 2.1).

Quarter: services and professions (healthcare admin, legal practice admin, education admin, hospitality, finance ops,
insurance ops, real-estate admin, HR). One JSON object per pack in packs.jsonl, each with a stable id.

Program-derived parts (fixed seed per pack id): SEM-31 entity IDs with Damerau-Levenshtein-1 look-alike pairs,
person-name pools, organisation names, invented-jargon candidates, the F12 lexicon (actions, objects, field keys,
units), concept groups and the disjointness list, register prose. Claude-written parts: setting, roles, documents,
attributes, outcomes, level scales, label words with predicates, implicit cues, links, sources, inert facts and
declared affixed words. Persona seeds come from persona_draw.json (O*NET titles drawn by program).

v1.1 (review fixes, 3 Oct): per rubric attribute an F10 attribute lexicon (phrases, synonyms, statements, key words
in every word form, state words), a negative fact statement per flag and a "none" statement per tag attribute, an F7
concept set (term, aliases, synonyms, broader, narrower, implications); per pack an inert-context vocabulary and >= 8
F7 filler Booleans in the disjointness list. Claude-written parts come from src/lex_<sector>.py. New lints: the R4-02
marker-collision lint (word classes loaded from c_src/common/markers.json plus the R4-02 record-status words), the
R4-03 name lint on every label word (all must pass; >= 12 per pack, and >= 12 whose predicate reads only the case
entity), the R4-01 inert-vocabulary disjointness check, statement checks with a statement round trip (every statement,
rendered with probe values, parses back to exactly its own attribute, kind and value), and the F7 U01 concept-set and
disjointness checks.

Lints (any failure stops the build): counts per pack (the union of the G0 pack requirements: F1, F3, F4, F5, F7, F9,
F10, F11, F12, F13), the shared negation counter (c_src/common/negcount.py) on every name-like string, declared and
undeclared affixed words, F7 banned factor stems, F4 link and cue bans, predicate parsing, uniqueness of keys.

Usage (from this folder): ../../../../.venv/bin/python build_packs.py [--only SLOT,...]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(HERE / "src"))
from c_src.common import negcount  # noqa: E402
import common_pools as CP  # noqa: E402

GEN_VERSION = "packs-2 v1.1"
SEED = 20261003
DICT_PATH = Path("/usr/share/dict/words")
LETTERS = [c for c in "ABCDEFGHJKMNPQRSTUVWXYZ"]          # SEM-31: no I, L or O
DIGITS = list("0123456789")
CONFUSABLE = {frozenset(p) for p in [("0", "D"), ("1", "7"), ("2", "Z"), ("5", "S"), ("6", "G"), ("8", "B")]}
ID_PATTERNS = ["DDDD", "ADDD", "DDAD", "AADDD", "DDDAA", "ADADD", "DADDA", "DDDDD", "ADDDA"]
BANNED_F7_STEMS = ["risk", "plan", "possib", "request", "schedul", "expect"]
BANNED_LINK_WORDS = ["share", "co-", "linked", "match", "part of", "downstream", "within", "together", "alongside",
                     "mutual", "jointly", "each other"]
BANNED_CUES = ["question", "disput", "doubt"]
NUM_TYPES = {"int": 0, "dec1": 1, "dec2": 2, "money": 2, "money0": 0}
CAT_TYPES = {"cat", "ord", "tag"}
BOOL_TYPES = {"state", "event"}
ALL_TYPES = set(NUM_TYPES) | CAT_TYPES | BOOL_TYPES | {"date"}

ERRORS: list[str] = []
INERT_STOP = {"of", "the", "a", "an", "on", "in", "at", "to", "for", "by", "and", "or", "per", "with", "number",
              "count", "type", "date", "days", "level", "code", "name", "status", "total", "amount"}


def err(slot, msg):
    ERRORS.append(f"{slot}: {msg}")


def rng_for(*parts) -> random.Random:
    return random.Random(int(hashlib.sha256(":".join(map(str, parts)).encode()).hexdigest(), 16))


def split_semi(s):
    return [x.strip() for x in s.split(";") if x.strip()]


def load_dict():
    words = set()
    for w in DICT_PATH.read_text(errors="ignore").split():
        words.add(w.lower())
    return words


DICT = load_dict()


IRREGULAR = set("paid sent held done made kept spent built bought taught brought caught found lost left met read run "
                "set shut split spread won told sold paid laid led fed bled overdue underpaid prepaid".split())


def familiar(tok):
    """A dictionary word or a regular inflection of one (web2 lists base forms only)."""
    t = tok.lower()
    if t in DICT or t in IRREGULAR:
        return True
    cands = set()
    for suf, rep in (("ies", "y"), ("ied", "y"), ("ier", "y"), ("iest", "y"), ("ily", "y"), ("es", ""), ("s", ""),
                     ("ed", ""), ("ed", "e"), ("d", ""), ("ing", ""), ("ing", "e"), ("er", ""), ("er", "e"),
                     ("est", ""), ("ly", ""), ("y", ""), ("y", "e"), ("ness", ""), ("al", "")):
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            base = t[: len(t) - len(suf)] + rep
            cands.add(base)
            if len(base) >= 2 and base[-1] == base[-2]:
                cands.add(base[:-1])
    return any(c in DICT for c in cands)


# ---------------------------------------------------------------- string distance

def osa(a: str, b: str) -> int:
    """Damerau-Levenshtein (optimal string alignment)."""
    la, lb = len(a), len(b)
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            c = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[la][lb]


# ---------------------------------------------------------------- attribute parsing

NUM_SPEC = re.compile(r"^(-?\d+(?:\.\d+)?)\s*\.\.\s*(-?\d+(?:\.\d+)?)\s*(.*)$")


def parse_flags(parts, slot, key):
    flags = {}
    for p in parts:
        if not p:
            continue
        if "=" in p:
            k, v = p.split("=", 1)
            flags[k.strip()] = v.strip()
        else:
            flags[p.strip()] = True
    for k in flags:
        if k not in {"aka", "bad", "pre", "grp", "lbl", "inert", "signed"}:
            err(slot, f"attr {key}: unknown flag {k}")
    return flags


def parse_attr(line, slot, currency, entity, inert=False):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 2:
        err(slot, f"bad attr line: {line!r}")
        return None
    key, typ = parts[0], parts[1]
    if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
        err(slot, f"bad attr key {key!r}")
    if typ not in ALL_TYPES:
        err(slot, f"attr {key}: unknown type {typ}")
        return None
    a = {"key": key, "entity": entity, "type": typ}
    rest = parts[2:]
    if typ in NUM_TYPES:
        if not rest:
            err(slot, f"attr {key}: numeric needs a range")
            return None
        m = NUM_SPEC.match(rest[0])
        if not m:
            err(slot, f"attr {key}: bad range {rest[0]!r}")
            return None
        lo, hi, unit = m.group(1), m.group(2), m.group(3).strip()
        places = NUM_TYPES[typ]
        a["value_type"] = "integer" if places == 0 else "decimal"
        a["places"] = places
        a["grid"] = 1 if places == 0 else round(10 ** -places, places)
        a["min"] = int(lo) if places == 0 else float(lo)
        a["max"] = int(hi) if places == 0 else float(hi)
        if typ.startswith("money"):
            if unit:
                err(slot, f"attr {key}: money takes the pack currency, not {unit!r}")
            unit = currency
            a["quantity_kind"] = "money"
        if not unit:
            err(slot, f"attr {key}: numeric attribute needs a unit")
        a["unit"] = unit
        a["unit_synonyms"] = CP.UNIT_SYNONYMS.get(unit, [])
        if unit not in CP.UNIT_SYNONYMS:
            err(slot, f"attr {key}: unit {unit!r} has no synonym entry (add it to UNIT_SYNONYMS)")
        flags = parse_flags(rest[1:], slot, key)
        a["sign"] = "signed" if flags.get("signed") else "non-negative"
        if a["min"] >= a["max"]:
            err(slot, f"attr {key}: min >= max")
        if a["min"] < 0 and a["sign"] != "signed":
            err(slot, f"attr {key}: negative min needs the 'signed' flag")
        a["cutpoint_ok"] = True
    elif typ in CAT_TYPES:
        if not rest:
            err(slot, f"attr {key}: category needs values")
            return None
        vals = split_semi(rest[0])
        adverse = [v.endswith("*") for v in vals]
        vals = [v.rstrip("*").strip() for v in vals]
        if len(set(vals)) != len(vals) or len(vals) < 2:
            err(slot, f"attr {key}: values must be >= 2 and unique")
        if typ == "tag" and len(vals) > 10:
            err(slot, f"attr {key}: tag vocabulary above 10")
        a["values"] = vals
        if any(adverse):
            a["adverse_values"] = [v for v, ad in zip(vals, adverse) if ad]
        if typ == "ord":
            a["ordered"] = True
        if typ == "tag":
            a["multi_valued"] = True
        flags = parse_flags(rest[1:], slot, key)
    elif typ in BOOL_TYPES:
        a["type"] = "boolean"
        a["kind"] = typ
        flags = parse_flags(rest, slot, key)
        if not inert:
            if "bad" not in flags or flags["bad"] not in ("0", "1"):
                err(slot, f"bool {key}: needs bad=0 or bad=1 (adverse pole)")
            else:
                a["adverse_pole"] = flags["bad"] == "1"
        # F1R4-A04: every Boolean declares the Boolean it presupposes; null = declared none
        a["presupposes"] = flags["pre"] if isinstance(flags.get("pre"), str) else None
    else:  # date
        a["type"] = "date"
        flags = parse_flags(rest, slot, key)
    a["label"] = flags.get("lbl") or key.replace("_", " ")
    a["aliases"] = [x.strip() for x in flags.get("aka", "").split(",") if x.strip()] if isinstance(
        flags.get("aka"), str) else []
    a["concept_group"] = flags.get("grp") if isinstance(flags.get("grp"), str) else key
    if inert or flags.get("inert"):
        a["inert"] = True
    return a


# ---------------------------------------------------------------- predicates (label words)

PRED_TERM = re.compile(r"^(not\s+)?([a-z][a-z0-9_]*)(?:\s*(>=|<=|==|!=|>|<|in)\s*(.+))?$")


def parse_pred(expr, attrs, slot, word):
    joins = re.findall(r"\s(and|or)\s", expr)
    if "and" in joins and "or" in joins:
        err(slot, f"word {word}: mixes and/or")
    terms = re.split(r"\s(?:and|or)\s", expr)
    out = []
    for t in terms:
        t = t.strip()
        m = PRED_TERM.match(t)
        if not m:
            err(slot, f"word {word}: bad term {t!r}")
            continue
        neg, key, op, val = m.group(1), m.group(2), m.group(3), m.group(4)
        a = attrs.get(key)
        if not a or a.get("inert"):
            err(slot, f"word {word}: unknown or inert attribute {key}")
            continue
        if a["type"] == "boolean":
            if op:
                err(slot, f"word {word}: boolean {key} takes no operator")
            out.append({"attr": key, "op": "is_false" if neg else "is_true"})
            continue
        if neg or not op:
            err(slot, f"word {word}: {key} needs an operator")
            continue
        if a["type"] == "date":
            err(slot, f"word {word}: date predicates are not used")
            continue
        if a["type"] in CAT_TYPES:
            if op in ("==", "!="):
                v = val.strip()
                if v not in a["values"]:
                    err(slot, f"word {word}: {v!r} not a value of {key}")
                out.append({"attr": key, "op": op, "value": v})
            elif op == "in":
                vs = [x.strip() for x in val.strip().strip("{}").split(",")]
                for v in vs:
                    if v not in a["values"]:
                        err(slot, f"word {word}: {v!r} not a value of {key}")
                out.append({"attr": key, "op": "in", "value": vs})
            elif a["type"] == "ord" and op in (">=", "<=", ">", "<"):
                v = val.strip()
                if v not in a["values"]:
                    err(slot, f"word {word}: {v!r} not a value of {key}")
                out.append({"attr": key, "op": op, "value": v, "by": "order"})
            else:
                err(slot, f"word {word}: op {op} not allowed on {a['type']} {key}")
            continue
        # numeric
        if op not in (">=", "<=", ">", "<", "==", "!="):
            err(slot, f"word {word}: op {op} not allowed on numeric {key}")
            continue
        try:
            v = float(val)
        except ValueError:
            err(slot, f"word {word}: bad number {val!r}")
            continue
        if not (a["min"] < v < a["max"]):
            err(slot, f"word {word}: threshold {v} not inside the range of {key}")
        out.append({"attr": key, "op": op, "value": int(v) if a["places"] == 0 else v})
    return {"join": ("or" if "or" in joins else "and"), "terms": out}


# ---------------------------------------------------------------- generated pools

def gen_ids(slot, ekey, prefix, pattern, n_base=54, n_pairs=10):
    rs = rng_for("ids", slot, ekey)

    def body():
        return "".join(rs.choice(LETTERS if c == "A" else DIGITS) for c in pattern)

    bodies = []
    tries = 0
    while len(bodies) < n_base and tries < 200000:
        tries += 1
        b = body()
        if all(osa(b, x) >= 3 for x in bodies):
            bodies.append(b)
    pairs = []
    order = bodies[:]
    rs.shuffle(order)
    for b in order:
        if len(pairs) >= n_pairs:
            break
        for _ in range(60):
            if rs.random() < 0.3:
                i = rs.randrange(len(b) - 1)
                if b[i] == b[i + 1] or (pattern[i] != pattern[i + 1]):
                    continue
                v = b[:i] + b[i + 1] + b[i] + b[i + 2:]
            else:
                i = rs.randrange(len(b))
                pool = LETTERS if pattern[i] == "A" else DIGITS
                c = rs.choice(pool)
                if c == b[i] or frozenset((c, b[i])) in CONFUSABLE:
                    continue
                v = b[:i] + c + b[i + 1:]
            if osa(v, b) != 1:
                continue
            others = [x for x in bodies if x != b] + [p for pr in pairs for p in pr]
            if all(osa(v, x) >= 3 for x in others):
                pairs.append((b, v))
                break
    ids = [f"{prefix}-{b}" for b in bodies] + [f"{prefix}-{p[1]}" for p in pairs]
    if len(ids) < 60 or len(pairs) < n_pairs:
        err(slot, f"entity {ekey}: id generation short ({len(ids)} ids, {len(pairs)} pairs)")
    bad_ids = [x for x in ids if set(x) & {"I", "L", "O"}]
    if bad_ids:
        err(slot, f"entity {ekey}: {len(bad_ids)} ids contain I, L or O")
    return {"id_format": {"prefix": prefix + "-", "body_pattern": pattern, "width": len(prefix) + 1 + len(pattern),
                          "alphabet": "digits 0-9 and letters A-Z without I, L, O",
                          "pattern_legend": "D digit, A letter"},
            "ids": ids, "lookalike_pairs": [[f"{prefix}-{a}", f"{prefix}-{b}"] for a, b in pairs]}


def gen_person_names(slot, n=40):
    rs = rng_for("names", slot)
    g, s = CP.GIVEN[:], CP.SURNAME[:]
    rs.shuffle(g)
    rs.shuffle(s)
    out = []
    for gi, si in zip(g, s):
        full = f"{gi} {si}"
        if all(osa(full, x) >= 3 for x in out):
            out.append(full)
        if len(out) >= n:
            break
    return out


USED_STEMS: set[str] = set()


def gen_word(rs, syl_lo=2, syl_hi=3):
    n = rs.randint(syl_lo, syl_hi)
    w = ""
    for k in range(n):
        w += rs.choice(CP.ONSETS) + rs.choice(CP.NUCLEI) + (rs.choice(CP.CODAS) if k == n - 1 or rs.random() < .3
                                                             else "")
    return w


def ok_invented(w):
    if not (5 <= len(w) <= 10) or w in DICT or w in USED_STEMS:
        return False
    if any(re.search(p, w) for p in CP.BANNED_AFFIX_PATTERNS):
        return False
    if re.search(r"(.)\1\1", w) or re.search(r"[aeiouy]{3}", w):
        return False
    # no dictionary word of length >= 5 inside it (avoids hints)
    for i in range(len(w)):
        for j in range(i + 5, len(w) + 1):
            if w[i:j] in DICT:
                return False
    if negcount.k_all(w):
        return False
    return True


def gen_jargon(slot, n=16):
    rs = rng_for("jargon", slot)
    out = []
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        w = gen_word(rs)
        if ok_invented(w):
            out.append(w)
            USED_STEMS.add(w)
    if len(out) < n:
        err(slot, "jargon generation short")
    return out


def gen_org_names(slot, ekey, suffixes, n=24):
    rs = rng_for("orgs", slot, ekey)
    out, stems = [], []
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        w = gen_word(rs, 2, 2)
        if not ok_invented(w):
            continue
        name = f"{w.capitalize()} {rs.choice(suffixes)}"
        if all(osa(name, x) >= 3 for x in out) and all(osa(w, x) >= 3 for x in stems):
            out.append(name)
            stems.append(w)
            USED_STEMS.add(w)
    if len(out) < n:
        err(slot, f"org names short for {ekey}")
    return out


# ---------------------------------------------------------------- lints

WORD = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")


def affix_candidates(text):
    out = []
    for w in WORD.findall(text):
        lw = w.lower()
        for part in lw.split("-"):
            if part in CP.NOT_NEG_AFFIX or part in ("non",):
                continue
            m = re.match(r"^(un|non|in|im|il|ir|dis|mis)(.+)$", part)
            if m and len(m.group(2)) >= 3 and m.group(2) in DICT:
                out.append(part)
                continue
            if part.endswith("less") and part[:-4] in DICT and len(part) > 6:
                out.append(part)
        if lw.startswith("non-"):
            out.append(lw)
    return out


def lint_names(slot, kind, strings, declared_affix, allow_affix=False):
    for s in strings:
        if not isinstance(s, str) or not s.strip():
            err(slot, f"{kind}: empty string")
            continue
        nc = negcount.count(s, affixed=tuple(declared_affix))
        if nc.k_all and not (allow_affix and all(m.cls == "affixed" for m in nc.matches)):
            err(slot, f"{kind}: negation in {s!r} (k_all {nc.k_all})")
        for c in affix_candidates(s):
            if c not in declared_affix:
                err(slot, f"{kind}: undeclared affixed word {c!r} in {s!r}")
            elif not allow_affix:
                err(slot, f"{kind}: affixed word {c!r} not allowed in {s!r}")


# ---------------------------------------------------------------- F10 / F7 lexicon helpers (v1.1)

MARKERS_PATH = LEAN / "c_src" / "common" / "markers.json"
FUNC = set("""a an the of in on at to for by with from and or is are was were be been being has have had its it this
that these those as per into their his her they them he she we our your which who whom whose there here then so do does
did can s""".split())
# zero-class value words and typed words never count as key words (they are marker words, R4-02)
ZERO_WORDS = {"no", "not", "none", "0", "yes", "true", "false", "null"}
# F10 section 5 / section 9 operator and connective content words (registered pools are step 4; this list is the
# pack-side superset used for the label-word name lint, R4-03)
OPERATOR_WORDS = set("""any all none no not unless only exception exceptions either neither nor both but between before
after least most more fewer less than over under within day days except other others following including excluding
inclusive exclusive exactly means meaning meets meet met definition definitions defined condition conditions term terms
record records section sections answer answers option options equal equals same set value values rule rules case cases
first earlier later earliest latest above below until through since tag tags count counts counted listed list
determined known stated card codes code row rows""".split())
NUMBER_WORDS = set("""zero one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
hundred thousand million first second third fourth fifth half quarter dozen""".split())
CAL_WORDS = set("""monday tuesday wednesday thursday friday saturday sunday january february march april may june july
august september october november december today yesterday tomorrow weekday weekend morning afternoon evening midday
noon midnight week weeks month months year years""".split())


def load_markers():
    m = json.loads(MARKERS_PATH.read_text())
    phrases = set()
    for c in m["classes"].values():
        for w in c.get("words", []) + c.get("same_marker_forms", []):
            phrases.add(str(w).lower())
    phrases |= {"null", "false", "true", "yes"}                       # typed-value words (R4-02 a)
    for ws in m.get("families", {}).get("F10", {}).get("local", {}).values():   # F10's local "not listed" (R4-02 b)
        phrases |= {str(w).lower() for w in ws if isinstance(w, str)}
    status = {"record", "records", "recorded", "recording", "recordings", "recorder", "recorders", "unrecorded",
              "rerecorded", "recordkeeping", "recordable", "list", "lists", "listed", "listing", "listings",
              "unlisted", "relist", "relisted", "delist", "delisted", "waitlist", "waitlists", "waitlisted",
              "shortlist", "shortlisted", "checklist", "checklists", "blacklist", "blacklisted", "whitelist",
              "whitelisted", "blanks", "blanked", "availability", "unavailability", "indeterminate", "unknowns"}
    for b in ("stated", "missing", "blank", "pending", "known", "available", "applicable", "specified", "determined"):
        status |= {b, "un" + b, "in" + b}
    return phrases, status, hashlib.sha256(MARKERS_PATH.read_bytes()).hexdigest()


MARKER_PHRASES, MARKER_STATUS, MARKERS_SHA = load_markers()
# every family's local marker words (F7 present / absent, F11 not checked, ...): kept out of the inert-context
# vocabulary as a conservative extra (not part of the R4-02 lint itself)
ALL_LOCAL_MARKER_WORDS = {t for fam in json.loads(MARKERS_PATH.read_text()).get("families", {}).values()
                          for ws in fam.get("local", {}).values() for w in ws if isinstance(w, str)
                          for t in re.split(r"[^a-z0-9]+", w.lower()) if t}
_SPLIT = re.compile(r"[^a-z0-9]+")


def toks(s):
    """Whole tokens, case-insensitive; whitespace, hyphen, underscore, slash and other punctuation split tokens."""
    return [t for t in _SPLIT.split(s.lower()) if t]


def strip_ph(s):
    return re.sub(r"\{[A-Za-z]+\}", " ", s)


def marker_hits(s, allow=frozenset()):
    """R4-02 marker-collision words in s (equal to or contained as whole tokens)."""
    s = strip_ph(s)
    raw = s.strip().lower()
    chunks = raw.split()
    t = toks(s)
    out = []
    for m in MARKER_PHRASES:
        if m in allow:
            continue
        if not re.search(r"[a-z0-9]", m):                           # punctuation markers: whole chunk only
            if raw == m or m in chunks:
                out.append(m)
            continue
        mt = toks(m)
        if any(t[i:i + len(mt)] == mt for i in range(len(t) - len(mt) + 1)):
            out.append(m)
    out += [x for x in t if x in MARKER_STATUS and x not in allow]
    return sorted(set(out))


IRREG = {"pay": ["paid", "pays", "paying"], "hold": ["held"], "send": ["sent"], "make": ["made"], "keep": ["kept"],
         "spend": ["spent"], "build": ["built"], "buy": ["bought"], "teach": ["taught"], "bring": ["brought"],
         "catch": ["caught"], "find": ["found"], "lose": ["lost"], "leave": ["left"], "meet": ["met"],
         "run": ["ran"], "win": ["won"], "tell": ["told"], "sell": ["sold"], "lay": ["laid"], "lead": ["led"],
         "feed": ["fed"], "give": ["gave", "given"], "take": ["took", "taken"], "write": ["wrote", "written"],
         "go": ["went", "gone"], "see": ["saw", "seen"], "know": ["knew", "known"], "drive": ["drove", "driven"],
         "ride": ["rode", "ridden"], "break": ["broke", "broken"], "choose": ["chose", "chosen"],
         "speak": ["spoke", "spoken"], "draw": ["drew", "drawn"], "fall": ["fell", "fallen"], "get": ["got", "gotten"],
         "begin": ["began", "begun"], "come": ["came"], "stand": ["stood"], "understand": ["understood"],
         "withdraw": ["withdrew", "withdrawn"], "undergo": ["underwent", "undergone"], "overdo": ["overdone"],
         "arise": ["arose", "arisen"], "bear": ["bore", "borne"], "fly": ["flew", "flown"], "grow": ["grew", "grown"],
         "show": ["shown"], "sit": ["sat"], "think": ["thought"], "seek": ["sought"], "hear": ["heard"],
         "say": ["said"], "shut": ["shut"], "do": ["did", "done", "does"], "child": ["children"],
         "person": ["people"], "man": ["men"],
         "woman": ["women"], "foot": ["feet"], "tooth": ["teeth"]}
IRREG_REV = {f: b for b, fs in IRREG.items() for f in fs}
_STRIP = [("ies", "y"), ("ied", "y"), ("ier", "y"), ("iest", "y"), ("ily", "y"), ("ying", "ie"), ("es", ""),
          ("s", ""), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"), ("er", ""), ("er", "e"),
          ("ers", ""), ("ers", "e"), ("est", ""), ("ly", ""), ("ness", ""), ("ment", ""), ("ments", ""),
          ("ation", ""), ("ation", "e"), ("ations", ""), ("ion", ""), ("ion", "e"), ("ions", ""), ("al", "")]


def stems(t):
    """The token and its dictionary base(s): the irregular base, and the longest base that suffix stripping reaches
    (so "miles" -> "mile", never "mil"; "used" -> "use", never "us"). Used by the ban-list lints."""
    t = t.lower()
    out = {t}
    if t in IRREG_REV:
        out.add(IRREG_REV[t])
    cands = set()
    for suf, rep in _STRIP:
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            b = t[: len(t) - len(suf)] + rep
            if b in DICT or b in IRREG:
                cands.add(b)
            if len(b) >= 4 and b[-1] == b[-2] and b[:-1] in DICT:
                cands.add(b[:-1])
    if cands:
        best = max(len(c) for c in cands)
        out |= {c for c in cands if len(c) == best}
    return out


def _cvc(b):
    """One-syllable consonant-vowel-consonant words double their last letter (ship -> shipped); longer words are
    left alone because stress cannot be read from spelling (visit -> visited)."""
    return 3 <= len(b) <= 4 and b[-1] not in "aeiouwxy" and b[-2] in "aeiou" and b[-3] not in "aeiou"


def inflect(b):
    """Regular inflections of a dictionary base (plural / third person, past, -ing) plus its irregular forms; no
    derivations (derived words are caught by stems() on the other side of every comparison)."""
    out = {b}
    if re.search(r"(s|x|z|ch|sh)$", b):
        out.add(b + "es")
    elif re.search(r"[^aeiou]y$", b):
        out.add(b[:-1] + "ies")
    else:
        out.add(b + "s")
    if b not in IRREG:
        if b.endswith("e"):
            out.add(b + "d")
        elif re.search(r"[^aeiou]y$", b):
            out.add(b[:-1] + "ied")
        else:
            out.add(b + "ed")
            if _cvc(b):
                out.add(b + b[-1] + "ed")
    if b.endswith("ie"):
        out.add(b[:-2] + "ying")
    elif b.endswith("e") and not b.endswith("ee"):
        out.add(b[:-1] + "ing")
    else:
        out.add(b + "ing")
        if _cvc(b):
            out.add(b + b[-1] + "ing")
    out |= set(IRREG.get(b, []))
    return out


def forms_of(t):
    """Every word form of a key word, by rule: the word itself plus the inflections of its dictionary base (the
    stripped base when there is one, else the word itself). Over-inclusive for nouns (verb endings are added too), so
    it is used only as a ban list."""
    t = t.lower()
    st = stems(t)
    bases = (st - {t}) or ({t} if (t in DICT or t in IRREG) else set())
    out = {t}
    for b in bases:
        out |= inflect(b)
    return out


def content_tokens(s):
    return [t for t in toks(strip_ph(s)) if t not in FUNC and t not in ZERO_WORDS and len(t) >= 2]


def stem_set(words):
    out = set()
    for w in words:
        out |= stems(w)
    return out


# core state words (qualitative value words) per quantity kind; category values, tag names and declared affixed
# words are added per attribute, and each lexicon line may add its own (`st:`)
STATE_CORE = {
    "money": "high higher highest low lower lowest large larger largest small smaller smallest big bigger biggest "
             "expensive costly cheap",
    "time": "long longer longest short shorter shortest high higher low lower many few",
    "distance": "long longer longest short shorter shortest far farther near nearer distant close",
    "area": "large larger largest small smaller smallest big bigger",
    "weight": "heavy heavier light lighter",
    "rate": "high higher highest low lower lowest",
    "count": "many few high higher highest low lower lowest large small",
    "date": "early earlier earliest late later latest recent old new",
    "ord": "high higher highest low lower lowest top bottom",
}
TIME_UNITS = {"days", "business days", "hours", "minutes", "weeks", "months", "years", "nights"}
DIST_UNITS = {"miles", "kilometres"}
AREA_UNITS = {"square feet", "square metres"}
WEIGHT_UNITS = {"kilograms"}
RATE_UNITS = {"percent", "points"}


def state_kind(a):
    if a["type"] == "date":
        return "date"
    if a["type"] == "ord":
        return "ord"
    if a.get("quantity_kind") == "money":
        return "money"
    u = a.get("unit", "")
    if u in TIME_UNITS:
        return "time"
    if u in DIST_UNITS:
        return "distance"
    if u in AREA_UNITS:
        return "area"
    if u in WEIGHT_UNITS:
        return "weight"
    if u in RATE_UNITS:
        return "rate"
    if a["type"] in NUM_TYPES:
        return "count"
    return None


def split_list(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def parse_lex(slot, text):
    """Claude-written lexicon lines (src/lex_<sector>.py): `key | syn: .. | say: .. | pos: .. | neg: .. | none: .. |
    st: .. | br: .. | nr: .. | imp: ..`; `@fill: name/e; name/s; ...` (F7 filler Booleans, optional `~ syn, syn`)."""
    out, fillers, ctx = {}, [], []
    for raw in text.strip().splitlines():
        ln = raw.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("@fill:"):
            for item in split_semi(ln[6:]):
                name, _, syn = item.partition("~")
                name, _, kind = name.strip().rpartition("/")
                kind = {"e": "event", "s": "state"}.get(kind.strip())
                if not kind or not name.strip():
                    err(slot, f"filler {item!r}: needs name/e or name/s")
                    continue
                fillers.append({"label": name.strip(), "kind": kind, "syn": split_list(syn)})
            continue
        if ln.startswith("@ctx:"):
            ctx += split_list(ln[5:])
            continue
        parts = [x.strip() for x in ln.split(" | ")]
        key = parts[0]
        if key in out:
            err(slot, f"lexicon: key {key} twice")
        d = {}
        for part in parts[1:]:
            f, _, v = part.partition(":")
            f = f.strip()
            if f not in ("syn", "say", "pos", "neg", "none", "st", "br", "nr", "imp"):
                err(slot, f"lexicon {key}: unknown field {f!r}")
                continue
            d[f] = split_list(v) if f in ("syn", "st", "br", "nr", "imp") else v.strip()
        out[key] = d
    return out, fillers, ctx


def build_attr_lexicon(slot, a, lx, affix_for):
    """Attach lexicon, statements and concept set to one rubric attribute (F10 R4-01/R4-02, F7 U01)."""
    key = a["key"]
    if lx is None:
        err(slot, f"lexicon: no entry for attribute {key}")
        lx = {}
    syn = [s for s in lx.get("syn", []) if s.lower() != a["label"].lower() and s not in a["aliases"]]
    if not syn:
        err(slot, f"lexicon {key}: needs >= 1 synonym (syn:)")
    t = a["type"]
    st = {}
    if t == "boolean":
        for f in ("pos", "neg"):
            if not lx.get(f):
                err(slot, f"lexicon {key}: boolean needs {f}:")
        st = {"positive": lx.get("pos", ""), "negative": lx.get("neg", "")}
        a["pos_statement"], a["neg_statement"] = st["positive"], st["negative"]
        for f in ("say", "none"):
            if f in lx:
                err(slot, f"lexicon {key}: boolean takes no {f}:")
    elif t == "tag":
        for f in ("say", "none"):
            if not lx.get(f):
                err(slot, f"lexicon {key}: tag attribute needs {f}:")
        st = {"value": lx.get("say", ""), "none": lx.get("none", "")}
        a["none_statement"] = st["none"]
    else:
        if not lx.get("say"):
            err(slot, f"lexicon {key}: needs say:")
        st = {"value": lx.get("say", "")}
        for f in ("pos", "neg", "none"):
            if f in lx:
                err(slot, f"lexicon {key}: {t} takes no {f}:")
    for f, frame in st.items():
        if "{E}" not in frame:
            err(slot, f"lexicon {key}: {f} statement lacks {{E}}")
        if f == "value" and "{v}" not in frame:
            err(slot, f"lexicon {key}: value statement lacks {{v}}")
        if f != "value" and "{v}" in frame:
            err(slot, f"lexicon {key}: {f} statement must not carry {{v}}")
        bad = set(re.findall(r"\{([A-Za-z]+)\}", frame)) - {"E", "v"}
        if bad:
            err(slot, f"lexicon {key}: unknown placeholder {bad}")
    phrases = [a["label"]] + a["aliases"] + syn + [v for v in st.values() if v]
    key_words = set(toks(key)) - FUNC - ZERO_WORDS
    for ph in phrases:
        key_words |= set(content_tokens(ph))
    forms = set()
    for w in key_words:
        forms |= forms_of(w)
    dropped = sorted(f for f in forms if marker_hits(f))
    forms -= set(dropped)
    sk = state_kind(a)
    states = set(STATE_CORE.get(sk, "").split()) if sk else set()
    states |= {v.lower() for v in a.get("values", [])}
    states |= {w.lower() for w in lx.get("st", [])}
    states |= set(affix_for.get(key, []))
    a["lexicon"] = {
        "phrases": phrases,
        "synonyms": a["aliases"] + syn,
        "statements": st,
        "key_words": sorted(key_words),
        "key_word_forms": sorted(forms),
        "state_words": sorted(states),
        **({"forms_dropped_as_markers": dropped} if dropped else {}),
    }
    a["concept_set"] = {"term": a["label"], "aliases": a["aliases"], "synonyms": syn,
                        "broader": lx.get("br", []), "narrower": lx.get("nr", []), "implies": lx.get("imp", [])}
    a["concept_set"]["members"] = sorted({a["label"]} | set(a["aliases"]) | set(syn) | set(lx.get("br", [])) |
                                         set(lx.get("nr", [])) | set(lx.get("imp", [])), key=str.lower)


def lexicon_words(real):
    """Every lexicon word of the pack (tokens of phrases and synonyms, key-word forms, state words, legend strings)."""
    words = set()
    for a in real:
        lx = a["lexicon"]
        for ph in lx["phrases"]:
            words |= set(content_tokens(ph))
        words |= set(lx["key_word_forms"])
        for s in lx["state_words"]:
            words |= set(content_tokens(s))
        words |= set(content_tokens(a["key"]))
        for v in a.get("values", []):
            words |= set(content_tokens(v))
        for u in [a.get("unit", "")] + a.get("unit_synonyms", []):
            words |= set(content_tokens(u))
    return words


CONCEPT_STOP = INERT_STOP | {"day", "time", "first", "last"}


def concept_words(real):
    out = set()
    for a in real:
        for m in a["concept_set"]["members"]:
            out |= {w for w in content_tokens(m) if w not in CONCEPT_STOP}
        out |= {w for w in content_tokens(a["key"]) if w not in CONCEPT_STOP}
    return out


# ---------------------------------------------------------------- pack expansion

def expand(src, persona, slot):
    p = {}
    sector_code = slot.split("-")[0]
    pid = f"p2-{slot}-{src['slug']}"
    p["id"] = pid
    p["pack_agent"] = "packs-2"
    p["quarter"] = "services_and_professions"
    p["sector"] = persona["sector"]
    p["slot"] = slot
    p["gen_version"] = GEN_VERSION
    p["seed"] = SEED
    p["subdomain"] = src["sub"]
    p["org_name"] = src["org"]
    p["desk_name"] = src["desk"]
    p["setting"] = src["setting"]
    p["persona_seed"] = {"onet_code": persona["onet_code"], "onet_title": persona["onet_title"],
                         "major_group": persona["major_group"], "source": "O*NET 31.0 Occupation Data (CC BY 4.0)",
                         "draw": "persona_draw.json"}
    p["decider_role"] = src["decider"]
    roles = split_semi(src["roles"])
    p["roles"] = [src["decider"]] + [r for r in roles if r != src["decider"]]
    currency = src.get("money", "dollars")
    p["currency"] = {"unit": currency, "synonyms": CP.UNIT_SYNONYMS.get(currency, []), "places": 2,
                     "symbols": "never (unit words only)"}
    declared_affix = {}
    for item in split_semi(src.get("affix", "")):
        w, _, base = item.partition("=>")
        declared_affix[w.strip().lower()] = base.strip()
    # entities and attributes
    ents, attrs = [], {}
    pattern_rs = rng_for("patterns", slot)
    pats = ID_PATTERNS[:]
    pattern_rs.shuffle(pats)
    for i, e in enumerate(src["ents"]):
        ek = e["key"]
        ent = {"key": ek, "singular": e["singular"], "plural": e["plural"], "id_key": f"{ek}_id",
               "aliases": [x.strip() for x in e.get("aka", "").split(",") if x.strip()],
               "role": "case" if i == 0 else e.get("role", "related")}
        if set(e["id"]) & {"I", "L", "O"} or not re.fullmatch(r"[A-Z]{2,3}", e["id"]):
            err(slot, f"entity {ek}: bad id prefix {e['id']!r}")
        ent.update(gen_ids(slot, ek, e["id"], pats[i % len(pats)]))
        names = e.get("names")
        if names == "person":
            ent["name_pool"] = gen_person_names(f"{slot}:{ek}")
            ent["name_kind"] = "person"
        elif isinstance(names, str) and names.startswith("org:"):
            ent["name_pool"] = gen_org_names(slot, ek, [x.strip() for x in names[4:].split(",") if x.strip()])
            ent["name_kind"] = "organisation"
        elif isinstance(names, list):
            ent["name_pool"] = names
            ent["name_kind"] = "named item"
        ent["attributes"] = []
        for line in [ln.strip() for ln in e["attrs"].strip().splitlines() if ln.strip()]:
            a = parse_attr(line, slot, currency, ek)
            if not a:
                continue
            if a["key"] in attrs:
                err(slot, f"attr key {a['key']} not unique in the pack")
            attrs[a["key"]] = a
            ent["attributes"].append(a)
        ents.append(ent)
    case = ents[0]
    # v1.1: attribute lexicons, statements and concept sets (F10 R4-01/R4-02, F7 U01) from src/lex_<sector>.py
    lexd, fillers_src, ctx_extra = parse_lex(slot, LEX.get(slot, ""))
    affix_for = {}
    for w, b in declared_affix.items():
        affix_for.setdefault(b, []).append(w)
    for a in attrs.values():
        build_attr_lexicon(slot, a, lexd.get(a["key"]), affix_for)
    for k in sorted(set(lexd) - set(attrs)):
        err(slot, f"lexicon: entry {k} names no rubric attribute")
    cw_stems = stem_set(concept_words(list(attrs.values())))
    # inert attributes (pack-specific + generic fill to >= 12)
    inert = []
    for line in [ln.strip() for ln in src["inert"].strip().splitlines() if ln.strip()]:
        a = parse_attr(line, slot, currency, case["key"], inert=True)
        if a:
            inert.append(a)
    rs = rng_for("inert", slot)
    gen = CP.GENERIC_INERT[:]
    rs.shuffle(gen)
    for line in gen:
        if len(inert) >= 12:
            break
        a = parse_attr(line, slot, currency, case["key"], inert=True)
        if not a or a["key"] in {x["key"] for x in inert}:
            continue
        if stem_set(w for w in content_tokens(a["label"]) if w not in CONCEPT_STOP) & cw_stems:
            continue
        a["generic"] = True
        inert.append(a)
    for a in inert:
        if a["key"] in attrs:
            err(slot, f"inert key {a['key']} clashes with an attribute")
        a["concept_set"] = {"term": a["label"], "aliases": a["aliases"], "members": [a["label"]] + a["aliases"]}
    # F7 filler Booleans (Z02: named like factors, drawn only from the disjointness list, U01)
    fills = []
    for f in fillers_src:
        fk = "fill_" + "_".join(toks(f["label"]))
        if fk in attrs or fk in {x["key"] for x in inert} or fk in {x["key"] for x in fills}:
            err(slot, f"filler key {fk} not unique")
        fills.append({"key": fk, "entity": case["key"], "type": "boolean", "kind": f["kind"], "label": f["label"],
                      "filler": True,
                      "concept_set": {"term": f["label"], "synonyms": f["syn"], "members": [f["label"]] + f["syn"]}})
    # program draw from the shared filler pool to 5 event + 5 state items (authored @fill lines count first)
    rs = rng_for("fillers", slot)
    for kind, pool_s in (("event", CP.FILLER_EVENTS), ("state", CP.FILLER_STATES)):
        pool = split_semi(pool_s)
        rs.shuffle(pool)
        for name in pool:
            if sum(f["kind"] == kind for f in fills) >= 5:
                break
            fk = "fill_" + "_".join(toks(name))
            if fk in {x["key"] for x in fills}:
                continue
            if stem_set(w for w in content_tokens(name) if w not in CONCEPT_STOP) & cw_stems:
                continue
            fills.append({"key": fk, "entity": case["key"], "type": "boolean", "kind": kind, "label": name,
                          "filler": True, "drawn": True,
                          "concept_set": {"term": name, "synonyms": [], "members": [name]}})
    p["filler_items"] = fills
    p["_ctx_extra"] = ctx_extra
    for a in inert:
        attrs[a["key"]] = a
    p["entity_types"] = ents
    p["inert_attributes"] = inert
    # presuppositions
    for a in attrs.values():
        if a.get("presupposes"):
            q = attrs.get(a["presupposes"])
            if not q or q["type"] != "boolean" or q.get("inert"):
                err(slot, f"bool {a['key']}: presupposes unknown boolean {a['presupposes']}")
    # scope
    sname, svals = src["scope"]
    p["scope_dimension"] = {"name": sname, "values": split_semi(svals)}
    if sname.replace(" ", "_") in attrs:
        err(slot, "scope dimension name equals an attribute key")
    # outcomes
    p["outcome_sets"] = []
    for k, s in enumerate(src["outcomes"], 1):
        outs = []
        for o in split_semi(s):
            outs.append({"name": o.rstrip("*").strip(), "adverse": o.endswith("*")})
        p["outcome_sets"].append({"id": f"os{k}", "outcomes": outs})
    # level scales (familiar names in usual rank order, low to high)
    p["level_scales"] = []
    for k, s in enumerate(src["levels"], 1):
        lv = split_semi(s)
        p["level_scales"].append({"id": f"ls{k}", "levels": [{"name": n, "usual_rank": r} for r, n in enumerate(lv)]})
    # label words
    p["label_words"] = []
    for ln in [x.strip() for x in src["words"].strip().splitlines() if x.strip()]:
        w, _, expr = ln.partition(":")
        w, expr = w.strip(), expr.strip()
        p["label_words"].append({"word": w, "predicate_text": expr, "predicate": parse_pred(expr, attrs, slot, w)})
    # implicit cues
    p["implicit_cues"] = []
    for item in split_semi(src["cues"]):
        phrase, _, tgt = item.partition("=>")
        key, _, val = tgt.strip().partition("=")
        key = key.strip()
        if key not in attrs or attrs[key]["type"] != "boolean" or attrs[key].get("inert"):
            err(slot, f"cue {phrase.strip()!r}: target {key} is not a pack boolean")
        if val.strip() not in ("true", "false"):
            err(slot, f"cue {phrase.strip()!r}: value must be true or false")
        p["implicit_cues"].append({"cue": phrase.strip(), "attr": key, "asserts": val.strip() == "true",
                                   "polarity": "positive" if val.strip() == "true" else "negative"})
    # links
    p["links"] = []
    ekeys = {e["key"] for e in ents}
    for item in split_semi(src["links"]):
        lhs, _, phr = item.partition(":")
        fr, _, to = lhs.partition(">")
        act, _, pas = phr.partition("/")
        fr, to, act, pas = fr.strip(), to.strip(), act.strip(), pas.strip()
        if fr not in ekeys or to not in ekeys or fr == to:
            err(slot, f"link {item!r}: bad entity types")
        p["links"].append({"from": fr, "to": to, "active": act, "passive": pas})
    # sources, documents
    p["source_names"] = split_semi(src["sources"])
    p["document_types"] = split_semi(src["docs"])
    # actions (F12 closed action set)
    acts = []
    for item in split_semi(CP.BASE_ACTIONS) + split_semi(src["actions"]):
        lex, _, syn = item.partition("=")
        acts.append({"lexeme": lex.strip(), "synonyms": [x.strip() for x in syn.split(",") if x.strip()]})
    p["actions"] = acts
    p["objects"] = [{"lexeme": e["singular"], "entity": e["key"], "synonyms": e["aliases"]} for e in ents]
    # F12 field lexicon
    fields = {}
    for e in ents:
        fields[e["id_key"]] = {"entity": e["key"], "type": "id"}
        for a in e["attributes"]:
            fields[a["key"]] = {"entity": e["key"], "type": a["type"], "label": a["label"],
                                **({"unit": a["unit"]} if "unit" in a else {}),
                                **({"enum": a["values"]} if "values" in a else {})}
    p["field_lexicon"] = fields
    # concept groups and disjointness
    groups = {}
    for a in attrs.values():
        if a.get("inert"):
            continue
        groups.setdefault(a["concept_group"], []).append(a["key"])
    for a in attrs.values():
        if a.get("presupposes"):
            g1, g2 = a["concept_group"], attrs[a["presupposes"]]["concept_group"] if a["presupposes"] in attrs else None
            if g2 and g1 != g2:
                err(slot, f"bool {a['key']} presupposes {a['presupposes']} but they sit in different concept groups")
    p["concept_groups"] = groups
    p["disjointness_list"] = [a["key"] for a in inert] + [f["key"] for f in p["filler_items"]]
    # affix declarations
    p["affixed_words"] = [{"word": w, "negates": b} for w, b in declared_affix.items()]
    for w, b in declared_affix.items():
        if b not in attrs or attrs[b]["type"] != "boolean":
            err(slot, f"affixed word {w}: base {b} is not a pack boolean")
    # generated pools
    p["jargon_candidates"] = gen_jargon(slot)
    p["date_window"] = {"start": f"{2025 + rng_for('yr', slot).randint(0, 4)}-01-01", "span_days": 730}
    org, desk = src["org"], src["desk"]
    p["register"] = {
        "greetings": [g.format(desk=desk) for g in CP.GREETINGS],
        "signoffs": [s.format(desk=desk, org=org) for s in CP.SIGNOFFS],
        "headers": [h.format(org=org, desk=desk, doc=p["document_types"][i % len(p["document_types"])],
                             scope=p["scope_dimension"]["values"][0]) for i, h in enumerate(CP.HEADERS)],
        "channels": split_semi(src.get("channels", "email; memo; case note; chat log; phone note")),
    }
    p["parents"] = ["O*NET 31.0 Database, Occupation Data (gd_onet_occupation)"]
    p["licence"] = "CC0 1.0 (Claude-written pack; program-generated pools)"
    p["third_party"] = [{"name": "O*NET 31.0 Database, Occupation Data", "licence": "CC BY 4.0",
                         "use": "one main occupation title as persona_seed; credited in the notices file"}]
    p["split"] = "pool (held-out designation is the orchestrator's)"
    p["inert_context_vocab"] = build_inert_vocab(p, attrs)
    p.pop("_ctx_extra", None)
    lint_pack(p, attrs, declared_affix, slot)
    return p


def name_lint_words(p, real):
    """R4-03 ban set for term names and label words: legend strings and attribute-lexicon words (lexicon_words),
    document types, consequence outcomes and the operator / connective content words."""
    ws = lexicon_words(real) | OPERATOR_WORDS
    for d in p["document_types"]:
        ws |= set(content_tokens(d))
    for s in p["outcome_sets"]:
        for o in s["outcomes"]:
            ws |= set(content_tokens(o["name"]))
    return ws


# function, quantifier and generic value words kept out of the inert-context vocabulary (they are not about the
# setting, people or process, or they read like attribute values)
VOCAB_STOP = set("""each every against across about among also very such some many much while where when what whose
which there these those them then than with without into onto upon from over under above below other others same
both either neither only just more most less least well like their they this that number numbers total totals
amount amounts value values figure figures""".split())


def build_inert_vocab(p, attrs):
    """F10 R4-01 inert-context vocabulary: words about the setting, people and process, sharing no word (or word
    stem) with any attribute lexicon, F7 concept set, label word, operator word, number, date or marker word."""
    real = [a for a in attrs.values() if not a.get("inert")]
    lexw = lexicon_words(real) | concept_words(real)
    ban_stems = stem_set(lexw)
    lw = set()
    for w in p["label_words"]:
        lw |= set(content_tokens(w["word"]))
    ban_stems |= stem_set(lw)
    jarg = {j.lower() for j in p["jargon_candidates"]}
    src = [p["setting"], p["decider_role"], p["desk_name"], p["scope_dimension"]["name"]] + p["roles"] + \
        p["document_types"] + p["source_names"] + p["scope_dimension"]["values"] + p["register"]["channels"] + \
        [a["label"] for a in p["inert_attributes"]] + [v for a in p["inert_attributes"] for v in a.get("values", [])] + \
        [f["label"] for f in p["filler_items"]] + p.get("_ctx_extra", [])
    out = set()
    for s in src:
        for w in toks(s):
            if not w.isalpha() or len(w) < 4 or w in FUNC or w in OPERATOR_WORDS or w in NUMBER_WORDS:
                continue
            if w in CAL_WORDS or w in ZERO_WORDS or w in jarg or marker_hits(w) or w in ALL_LOCAL_MARKER_WORDS:
                continue
            if w in INERT_STOP or w in VOCAB_STOP:
                continue
            if w in lexw or w in lw or stems(w) & ban_stems:
                continue
            out.add(w)
    return sorted(out)


def lint_pack(p, attrs, aff, slot):
    real = [a for a in attrs.values() if not a.get("inert")]
    case = p["entity_types"][0]
    n = lambda pred: sum(1 for a in real if pred(a))  # noqa: E731
    checks = [
        (len(p["entity_types"]) >= 3, "entity types >= 3"),
        (len(real) >= 16, f"non-inert attributes >= 16 (have {len(real)})"),
        (len([a for a in case["attributes"]]) >= 10, "case entity attributes >= 10"),
        (n(lambda a: a["type"] == "boolean") >= 5, "booleans >= 5"),
        (n(lambda a: a["type"] == "boolean" and a["kind"] == "event") >= 2, "event booleans >= 2"),
        (n(lambda a: a["type"] == "boolean" and a["kind"] == "state") >= 2, "state booleans >= 2"),
        (n(lambda a: a["type"] in NUM_TYPES) >= 5, "numeric attributes >= 5"),
        (n(lambda a: a.get("quantity_kind") == "money") >= 1, "money attributes >= 1"),
        (n(lambda a: a["type"] in ("cat", "ord")) >= 3, "category attributes >= 3"),
        (n(lambda a: a["type"] == "ord") >= 1, "ordered category >= 1"),
        (n(lambda a: a["type"] == "tag") >= 1, "tag attribute >= 1"),
        (n(lambda a: a["type"] == "date") >= 2, "date attributes >= 2"),
        (len(p["inert_attributes"]) >= 10, "inert attributes >= 10"),
        (sum(1 for a in p["inert_attributes"] if not a.get("generic")) >= 5, "pack-specific inert >= 5"),
        (len(p["outcome_sets"]) >= 2, "outcome sets >= 2"),
        (all(3 <= len(s["outcomes"]) <= 8 for s in p["outcome_sets"]), "outcome set sizes 3-8"),
        (all(any(o["adverse"] for o in s["outcomes"]) and not all(o["adverse"] for o in s["outcomes"])
             for s in p["outcome_sets"]), "each outcome set mixes adverse and not adverse"),
        (len(p["level_scales"]) >= 2, "level scales >= 2"),
        (all(3 <= len(s["levels"]) <= 7 for s in p["level_scales"]), "level scale sizes 3-7"),
        (len(p["label_words"]) >= 12, f"label words >= 12 (have {len(p['label_words'])})"),
        (len(p["implicit_cues"]) >= 3, "implicit cues >= 3"),
        (len(p["links"]) >= 2, "links >= 2"),
        (len(p["actions"]) >= 12, "actions >= 12"),
        (len(p["source_names"]) >= 6, "source names >= 6"),
        (len(p["document_types"]) >= 5, "document types >= 5"),
        (len(p["scope_dimension"]["values"]) >= 4, "scope values >= 4"),
        (len(p["roles"]) >= 6, "roles >= 6"),
        (len(p["affixed_words"]) >= 2, "declared affixed words >= 2"),
        (sum(1 for e in p["entity_types"] if e.get("name_kind") == "person") >= 1, "a person entity type"),
        (all(len(e["ids"]) >= 60 for e in p["entity_types"]), "ids >= 60 per entity type"),
    ]
    for ok, what in checks:
        if not ok:
            err(slot, f"count check failed: {what}")
    # no two label words alike; outcomes unique
    words = [w["word"].lower() for w in p["label_words"]]
    if len(set(words)) != len(words):
        err(slot, "duplicate label words")
    for w in p["label_words"]:
        for tok in re.split(r"[\s-]+", w["word"].lower()):
            if tok and not familiar(tok):
                err(slot, f"label word {w['word']!r}: {tok!r} not a familiar dictionary word")
    allo = [o["name"].lower() for s in p["outcome_sets"] for o in s["outcomes"]]
    for s in p["outcome_sets"]:
        names = [o["name"].lower() for o in s["outcomes"]]
        if len(set(names)) != len(names):
            err(slot, f"duplicate outcome in {s['id']}")
    if len({tuple(sorted(o["name"] for o in s["outcomes"])) for s in p["outcome_sets"]}) < 2:
        err(slot, "outcome sets are not distinct")
    # F7 banned stems on boolean factor names
    for a in real:
        if a["type"] == "boolean":
            for t in [a["label"]] + a["aliases"]:
                for stem in BANNED_F7_STEMS:
                    if stem in t.lower():
                        err(slot, f"bool {a['key']}: banned factor stem {stem!r} in {t!r}")
    # F4 links
    for l in p["links"]:
        for t in (l["active"], l["passive"]):
            for b in BANNED_LINK_WORDS:
                if b in t.lower():
                    err(slot, f"link phrase {t!r}: banned word {b!r}")
    pairs = {(l["from"], l["to"]) for l in p["links"]}
    for fr, to in pairs:
        if (to, fr) in pairs:
            err(slot, f"links {fr}>{to} and {to}>{fr}: possible converse pair")
    acts = [l["active"] for l in p["links"]]
    if len(set(acts)) != len(acts):
        err(slot, "two links share an active phrase")
    for c in p["implicit_cues"]:
        for b in BANNED_CUES:
            if b in c["cue"].lower():
                err(slot, f"cue {c['cue']!r}: banned ambiguous cue")
        nc = negcount.count(c["cue"], affixed=tuple(aff))
        if c["polarity"] == "negative" and nc.k_all == 0:
            err(slot, f"cue {c['cue']!r}: negative cue but negcount finds no cue")
        if c["polarity"] == "positive" and nc.k_all != 0:
            err(slot, f"cue {c['cue']!r}: positive cue carries a negation")
    # actions: a synonym maps to one action
    seen = {}
    for a in p["actions"]:
        for t in [a["lexeme"]] + a["synonyms"]:
            if t in seen:
                err(slot, f"action word {t!r} maps to two actions")
            seen[t] = a["lexeme"]
    # names: negation and affix lints
    declared = set(aff)
    lint_names(slot, "outcome", [o["name"] for s in p["outcome_sets"] for o in s["outcomes"]], declared)
    lint_names(slot, "level", [l["name"] for s in p["level_scales"] for l in s["levels"]], declared)
    lint_names(slot, "label word", [w["word"] for w in p["label_words"]], declared)
    lint_names(slot, "entity", [x for e in p["entity_types"] for x in [e["singular"], e["plural"]] + e["aliases"]],
               declared)
    lint_names(slot, "role", p["roles"], declared)
    lint_names(slot, "document", p["document_types"], declared)
    lint_names(slot, "source", p["source_names"], declared)
    lint_names(slot, "scope", p["scope_dimension"]["values"] + [p["scope_dimension"]["name"]], declared)
    lint_names(slot, "action", [t for a in p["actions"] for t in [a["lexeme"]] + a["synonyms"]], declared)
    lint_names(slot, "attribute label", [t for a in attrs.values() for t in [a["label"]] + a["aliases"]], declared)
    lint_names(slot, "category value", [v for a in attrs.values() for v in a.get("values", [])], declared,
               allow_affix=True)
    lint_names(slot, "names", [x for e in p["entity_types"] for x in e.get("name_pool", [])] + [p["org_name"],
               p["desk_name"]], declared)
    lint_names(slot, "setting", [p["setting"], p["subdomain"]], declared, allow_affix=True)
    # inert attributes share no content word with real attribute labels or aliases
    stop = INERT_STOP
    real_words = set()
    for a in real:
        for t in [a["label"]] + a["aliases"]:
            real_words |= {w for w in re.findall(r"[a-z]+", t.lower()) if w not in stop}
    for a in p["inert_attributes"]:
        ws = {w for w in re.findall(r"[a-z]+", a["label"].lower()) if w not in stop}
        if ws & real_words:
            err(slot, f"inert {a['key']}: shares words {sorted(ws & real_words)} with rubric attributes")
    # every tag/cat value list is unique; every boolean has an adverse pole
    if p["persona_seed"]["onet_code"] is None:
        err(slot, "no persona seed")
    lint_f10_f7(p, attrs, aff, slot)


def _frame_rx(frame):
    out, pos = "", 0
    for m in re.finditer(r"\{(E|v)\}", frame):
        out += re.escape(frame[pos:m.start()]) + (f"(?P<{m.group(1)}>.+?)" if m.group(1) == "E" else "(?P<v>.+)")
        pos = m.end()
    return re.compile("^" + out + re.escape(frame[pos:]) + "$")


def _probe_values(a):
    t = a["type"]
    if t in CAT_TYPES and t != "tag":
        return list(a["values"])
    if t == "tag":
        return [", ".join(a["values"][:2]), a["values"][-1]]
    if t == "date":
        return ["2026-03-14"]
    if t == "boolean":
        return []
    lo, hi, d = a["min"], a["max"], a["places"]
    mid = round((lo + hi) / 2, d)
    return [f"{mid:.{d}f} {a['unit']}", f"{lo:.{d}f} {a['unit']}"]


def _valid_value(a, v):
    t = a["type"]
    if t in CAT_TYPES and t != "tag":
        return v in a["values"]
    if t == "tag":
        return all(x.strip() in a["values"] for x in v.split(","))
    if t == "date":
        return re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) is not None
    if t == "boolean":
        return False
    units = [a["unit"]] + a.get("unit_synonyms", [])
    return any(re.fullmatch(r"-?\d+(\.\d+)? " + re.escape(u), v) for u in units)


def statement_round_trip(p, slot):
    n, bad = 0, 0
    for e in p["entity_types"]:
        ref = f"{e['singular'].capitalize()} {e['ids'][0]}"
        frames = []
        for a in e["attributes"]:
            for kind, fr in a["lexicon"]["statements"].items():
                frames.append((a, kind, _frame_rx(fr), fr))
        for a in e["attributes"]:
            st = a["lexicon"]["statements"]
            probes = [(k, st[k], None) for k in ("positive", "negative", "none") if k in st]
            probes += [("value", st["value"], v) for v in _probe_values(a)] if "value" in st else []
            for kind, fr, v in probes:
                s = fr.replace("{E}", ref).replace("{v}", v or "") + "."
                s = s[0].upper() + s[1:]
                n += 1
                hits = []
                body = s[:-1]
                for b, k2, rx, _ in frames:
                    m = rx.match(body)
                    if not m or m.group("E") != ref:
                        continue
                    if k2 == "value" and not _valid_value(b, m.group("v")):
                        continue
                    hits.append((b["key"], k2, m.groupdict().get("v")))
                if hits != [(a["key"], kind, v)]:
                    bad += 1
                    err(slot, f"statement round trip: {a['key']} {kind} {s!r} parses as {hits}")
    return n, bad


def lint_f10_f7(p, attrs, aff, slot):
    """v1.1 lints: F10 pack requirements (R4-01, R4-02, R4-03) and F7 concept sets / disjointness (U01, Z02)."""
    real = [a for a in attrs.values() if not a.get("inert")]
    declared = set(aff)
    rep = {"marker_collision_hits": 0, "strings_checked": 0}

    def mk(kind, s, allow=frozenset()):
        rep["strings_checked"] += 1
        h = marker_hits(s, allow)
        if h:
            rep["marker_collision_hits"] += 1
            err(slot, f"marker-collision lint (R4-02): {kind} {s!r} carries {h}")

    # (b) marker-collision lint on every attribute name, category value, tag name, unit, lexicon phrase or word,
    # label word, plus every string that can sit in a rendered record (entity names, inert and filler items)
    for a in real:
        lx = a["lexicon"]
        k = f"{a['key']}"
        mk(f"{k} key", a["key"])
        for s in lx["phrases"]:
            if s in (a.get("neg_statement"), a.get("none_statement")):
                continue
            mk(f"{k} phrase", s)
        if a.get("neg_statement"):
            mk(f"{k} neg_statement", a["neg_statement"], frozenset({"no"}))
        if a.get("none_statement"):
            mk(f"{k} none_statement", a["none_statement"], frozenset({"none"}))
        for s in a.get("values", []) + [a.get("unit", "")] + a.get("unit_synonyms", []) + lx["key_word_forms"] + \
                lx["state_words"] + a["concept_set"]["members"]:
            if s:
                mk(f"{k} value/unit/word", s)
    for w in p["label_words"]:
        mk("label word", w["word"])
    for e in p["entity_types"]:
        for s in [e["singular"], e["plural"]] + e["aliases"] + e.get("name_pool", []):
            mk(f"entity {e['key']}", s)
    for a in p["inert_attributes"]:
        for s in [a["key"], a["label"]] + a.get("values", []) + [a.get("unit", "")]:
            if s:
                mk(f"inert {a['key']}", s)
    for f in p["filler_items"]:
        for s in f["concept_set"]["members"]:
            mk(f"filler {f['key']}", s)
    for w in p["inert_context_vocab"]:
        mk("inert context word", w)
    # statements: placeholders and polarity (negcount)
    for a in real:
        for f, s in a["lexicon"]["statements"].items():
            nc = negcount.count(s, affixed=tuple(declared))
            if f == "negative" and not re.search(r"\b(no|not)\b", s.lower()):
                err(slot, f"{a['key']}: neg_statement value word must be 'no' or 'not': {s!r}")
            if f == "negative" and nc.k_all == 0:
                err(slot, f"{a['key']}: neg_statement carries no counted negation: {s!r}")
            if f == "none" and not re.search(r"\bnone\b", s.lower()):
                err(slot, f"{a['key']}: none_statement must state 'none': {s!r}")
            if f in ("positive", "value") and nc.k_all:
                err(slot, f"{a['key']}: {f} statement carries a negation: {s!r}")
            if re.search(r"\b(will|would|should|may|might|could|expected|planned|likely|probably)\b", s.lower()):
                err(slot, f"{a['key']}: statement is modal or hedged (ST50): {s!r}")
        # synonyms and concept members are name-like strings: negation and affix lints
        lint_names(slot, f"{a['key']} synonym", a["concept_set"]["synonyms"], declared)
        lint_names(slot, f"{a['key']} concept member", a["concept_set"]["broader"] + a["concept_set"]["narrower"] +
                   a["concept_set"]["implies"], declared)
        if a["type"] == "boolean":
            for t in a["concept_set"]["synonyms"]:
                for stem in BANNED_F7_STEMS:
                    if stem in t.lower():
                        err(slot, f"bool {a['key']}: banned factor stem {stem!r} in synonym {t!r}")
    # (c) name lint (R4-03): label words pass against the pack's own legend, lexicon, document types, outcomes and
    # operator words; every label word must pass, and >= 12 per pack
    nl = name_lint_words(p, real)
    nl_stems = stem_set(nl)
    clean = 0
    for w in p["label_words"]:
        bad = sorted(t for t in content_tokens(w["word"]) if t in nl or stems(t) & nl_stems)
        w["name_lint"] = "pass" if not bad else "fail"
        if bad:
            err(slot, f"name lint (R4-03): label word {w['word']!r} collides with legend / lexicon word(s) {bad}")
        else:
            clean += 1
    if clean < 12:
        err(slot, f"name lint: only {clean} clean label words (need >= 12)")
    # (d) inert-context vocabulary disjoint from every attribute lexicon (R4-01)
    lexw = lexicon_words(real)
    lex_stems = stem_set(lexw)
    clash = sorted(w for w in p["inert_context_vocab"] if w in lexw or stems(w) & lex_stems)
    if clash:
        err(slot, f"inert-context vocabulary shares words with attribute lexicons: {clash}")
    if len(p["inert_context_vocab"]) < 30:
        err(slot, f"inert-context vocabulary too small ({len(p['inert_context_vocab'])} < 30)")
    # F7 U01: concept sets are more than the term; inert and filler items share no word with any rubric concept set
    thin = [a["key"] for a in real if len(a["concept_set"]["members"]) < 3]
    if thin:
        err(slot, f"F7 U01: concept sets with < 3 members: {thin}")
    nb = [a["key"] for a in real if a["type"] == "boolean" and not (a["concept_set"]["broader"] or
                                                                     a["concept_set"]["narrower"] or
                                                                     a["concept_set"]["implies"])]
    if nb:
        err(slot, f"F7 U01: boolean factors without broader / narrower / implication members: {nb}")
    cw_stems = stem_set(concept_words(real))
    for a in p["inert_attributes"] + p["filler_items"]:
        ws = set()
        for m in a["concept_set"]["members"]:
            ws |= {t for t in content_tokens(m) if t not in CONCEPT_STOP}
        ov = sorted(t for t in ws if stems(t) & cw_stems)
        if ov:
            err(slot, f"F7 U01: disjointness item {a['key']} shares {ov} with a rubric concept set")
    # F7 Z02 fillers: named like factors (affirmative, no banned stem), both kinds, enough for m + 4 on a card
    fl = p["filler_items"]
    if len(fl) < 8 or sum(f["kind"] == "event" for f in fl) < 3 or sum(f["kind"] == "state" for f in fl) < 3:
        err(slot, f"F7 fillers: need >= 8 with >= 3 event and >= 3 state (have {len(fl)})")
    lint_names(slot, "filler", [m for f in fl for m in f["concept_set"]["members"]], declared)
    for f in fl:
        for t in f["concept_set"]["members"]:
            for stem in BANNED_F7_STEMS:
                if stem in t.lower():
                    err(slot, f"filler {f['key']}: banned factor stem {stem!r} in {t!r}")
    # F10 natural predicates over the same attributes: >= 12 clean label words whose predicate reads only the case
    # entity's attributes (a program card's legend is one entity type)
    ent_of = {a["key"]: e["key"] for e in p["entity_types"] for a in e["attributes"]}
    for w in p["label_words"]:
        es = sorted({ent_of[t["attr"]] for t in w["predicate"]["terms"]})
        w["entity"] = es[0] if len(es) == 1 else es
    case_clean = sum(1 for w in p["label_words"] if w["entity"] == p["entity_types"][0]["key"] and
                     w["name_lint"] == "pass")
    if case_clean < 12:
        err(slot, f"F10: only {case_clean} clean label words over the case entity's attributes (need >= 12)")
    rep["label_words_case_entity"] = case_clean
    # statement round trip (G3 pre-check): every statement, rendered with probe values, parses back to exactly its
    # own attribute, kind and value among all statements of the same entity type
    rt_n, rt_bad = statement_round_trip(p, slot)
    rep["statement_round_trip"] = {"sentences": rt_n, "failures": rt_bad}
    rep["label_words"] = len(p["label_words"])
    rep["label_words_name_lint_pass"] = clean
    rep["inert_context_vocab"] = len(p["inert_context_vocab"])
    rep["filler_items"] = len(fl)
    rep["markers_json_sha256"] = MARKERS_SHA
    p["f10_f7_lint"] = rep


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def load_sources():
    packs = []
    for f in sorted((HERE / "src").glob("sec_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for s in mod.PACKS:
            s["_file"] = f.name
            packs.append(s)
    return packs


LEX: dict[str, str] = {}


def load_lex():
    """Claude-written lexicon sources src/lex_<sector>.py (LEX = {slot: text}); see parse_lex for the line format."""
    lex = {}
    for f in sorted((HERE / "src").glob("lex_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.LEX.items():
            if k in lex:
                ERRORS.append(f"lexicon slot {k} in two files")
            lex[k] = v
    return lex


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(HERE / "packs.jsonl"))
    ap.add_argument("--exclude", default="", help="comma list of pack ids to leave out (sealed-check drops)")
    a = ap.parse_args(argv)
    draw = json.loads((HERE / "persona_draw.json").read_text())
    by_slot = {d["slot"]: d for d in draw["drawn"]}
    # spares replace a slot when a pack source names `persona_spare` (a dropped pack's replacement)
    spares = {s["sector"]: s["spares"] for s in draw["sectors"]}
    only = set(x for x in a.only.split(",") if x)
    excl = set(x for x in a.exclude.split(",") if x)
    srcs = load_sources()
    LEX.update(load_lex())
    out, seen_slots, seen_ids = [], set(), set()
    for s in srcs:
        slot = s["slot"]
        if only and slot not in only:
            continue
        if slot in seen_slots:
            err(slot, "slot used twice")
        seen_slots.add(slot)
        persona = by_slot.get(slot)
        if s.get("persona_spare") is not None:
            sec = s["sector"]
            sp = spares[sec][s["persona_spare"]]
            persona = {"sector": sec, "slot": slot, "onet_code": sp["onet_code"], "onet_title": sp["onet_title"],
                       "major_group": sp["onet_code"][:2]}
        if not persona:
            err(slot, "no persona for slot")
            continue
        pk = expand(s, persona, slot)
        if pk["id"] in excl:
            continue
        if pk["id"] in seen_ids:
            err(slot, "duplicate pack id")
        seen_ids.add(pk["id"])
        pk["source_file"] = f"src/{s['_file']}"
        pk["sha256"] = hashlib.sha256(canonical({k: v for k, v in pk.items() if k != "sha256"}).encode()).hexdigest()
        out.append(pk)
    # cross-pack uniqueness
    orgs = [p["org_name"] for p in out]
    if len(set(orgs)) != len(orgs):
        ERRORS.append("org names not unique across packs")
    if ERRORS:
        print(f"{len(ERRORS)} lint errors:")
        for e in ERRORS:
            print("  " + e)
        return 1
    with open(a.out, "w") as fh:
        for p in out:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} packs -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
