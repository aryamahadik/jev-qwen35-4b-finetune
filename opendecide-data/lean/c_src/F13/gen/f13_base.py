"""F13 base: paths, seeded rng, dates (SEM-20), IDs (SEM-31), word lints (G0 2.1, 3.3, 7), pack adapter, wordings,
fmt1 styles, real tokenizer and the served-length measure (G0 section 1 length row). See f13_design.py."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import re
import sys
from functools import lru_cache
from pathlib import Path

F13 = Path(__file__).resolve().parents[1]
C_SRC = F13.parent
LEAN = C_SRC.parent
FMT1_DIR = C_SRC / "formats" / "formats-1"
PACKS = C_SRC / "packs"
WORDINGS = C_SRC / "formats" / "formats-2" / "wordings" / "family_pools.jsonl"
for _p in (str(LEAN), str(FMT1_DIR), str(C_SRC / "common")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SPEC_ID = "F13.G0.v7"
G0_SHA = "b4bb6319b3b7431819e99dda2759938abe2df4674be0ab21f5287269b8c42993"
GEN_VERSION = "F13-gen r1.0 (py3, sqlite3, fmt1 v1.1, Qwen3.5-4B tokenizer @851bf6e8)"
LICENCE = "CC0 1.0 (program-generated)"


def h64(*parts) -> int:
    return int.from_bytes(hashlib.sha256("\x1f".join(map(str, parts)).encode()).digest()[:8], "big")


def rng(*key) -> random.Random:
    return random.Random(h64(*key))


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ dates (SEM-20)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
DATE_FORMATS = ("iso", "dmy", "mdy")


def fmt_date(d: dt.date, form: str) -> str:
    if form == "iso":
        return d.isoformat()
    if form == "dmy":
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


_MON = "(?:" + "|".join(MONTHS) + ")"
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{1,2} " + _MON + r" \d{4}|" + _MON + r" \d{1,2}, \d{4})\b")


def parse_date(s: str) -> dt.date:
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2}) (" + _MON + r") (\d{4})", s)
    if m:
        return dt.date(int(m[3]), MONTHS.index(m[2]) + 1, int(m[1]))
    m = re.fullmatch(r"(" + _MON + r") (\d{1,2}), (\d{4})", s)
    if m:
        return dt.date(int(m[3]), MONTHS.index(m[1]) + 1, int(m[2]))
    raise ValueError(f"not a SEM-20 date: {s!r}")


def add_days(d: dt.date, n: int) -> dt.date:
    return d + dt.timedelta(days=n)


# ------------------------------------------------------------------------------------------------ IDs (SEM-31)
ID_ALPH = "0123456789ABCDEFGHJKMNPQRSTUVWXYZ"  # no I, L, O
DIGITS = "0123456789"
CONFUSABLE = {frozenset(p) for p in ("0D", "17", "2Z", "5S", "6G", "8B")}


def dl1_ok(a: str, b: str) -> bool:
    """Damerau-Levenshtein distance exactly 1 by one substitution or one adjacent transposition (same length)."""
    if len(a) != len(b) or a == b:
        return False
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    if len(diff) == 1:
        i = diff[0]
        return frozenset((a[i], b[i])) not in CONFUSABLE
    if len(diff) == 2 and diff[1] == diff[0] + 1:
        i = diff[0]
        return a[i] == b[i + 1] and a[i + 1] == b[i]
    return False


def lookalike(x: str, r: random.Random, taken=()) -> str | None:
    """One DL-1 neighbour of x in the SEM-31 alphabet (body chars after the prefix dash only)."""
    pre, _, body = x.rpartition("-")
    pre = pre + "-" if pre else ""
    for _ in range(60):
        b = list(body)
        if r.random() < 0.5 and len(b) >= 2:
            i = r.randrange(len(b) - 1)
            if b[i] == b[i + 1]:
                continue
            b[i], b[i + 1] = b[i + 1], b[i]
        else:
            i = r.randrange(len(b))
            pool = DIGITS if b[i].isdigit() else ID_ALPH
            c = r.choice(pool)
            if c == b[i] or frozenset((c, b[i])) in CONFUSABLE:
                continue
            b[i] = c
        y = pre + "".join(b)
        if y != x and y not in taken and dl1_ok(x, y):
            return y
    return None


def new_id(prefix: str, width: int, r: random.Random, taken: set, digits_only: bool = False) -> str:
    for _ in range(1000):
        body = "".join(r.choice(DIGITS if (digits_only or k == 0) else ID_ALPH) for k in range(width))
        x = f"{prefix}-{body}"
        if x not in taken and not any(dl1_ok(x, t) for t in taken):
            taken.add(x)
            return x
    raise RuntimeError("id space exhausted")


# ------------------------------------------------------------------------------------------------ word lints
L_CORE = ("not", "n't", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor")
XF10 = ("wrong", "right", "rights", "reject", "rejects", "rejected", "rejecting", "rejection", "accept", "accepts",
        "accepted", "accepting", "acceptance", "should", "would")
STATUS_WORDS = ("in force", "draft", "proposed", "void", "active", "open", "closed", "pending", "not yet received")
LEX_VERBS = ("placed", "released", "imposed", "met", "waived", "assigned", "transferred", "closed", "reopened", "made",
             "revised", "reversed", "renamed", "rolled back", "applied", "correction", "void", "carries", "fails",
             "place", "release", "impose", "waive", "assign", "transfer", "close", "reopen", "revise", "reverse",
             "rename", "apply", "correct", "carry", "fail", "failed", "carried", "voided", "amend", "amended",
             "amendment", "repeal", "repealed", "effective", "valid", "version", "rule", "rules", "status")
CUES = ("if", "unless", "only", "either", "all of", "any of", "none of", "at least", "at most", "more than",
        "less than", "fewer than", "no fewer", "no less", "no more", "not exceeding", "exceeds", "exceed", "over",
        "above", "below", "under", "up to", "between", "overrides", "override", "exception", "exceptions", "or",
        "exclusion", "criterion", "criteria", "outcome", "decision", "meets", "qualifies")
BANNED = ("until", "till", "since", "expires", "expiry", "expired", "rescinded", "overturned", "annulled", "cancelled",
          "canceled", "withdrawn", "majority", "two-thirds", "quorum", "casting vote", "change request",
          "for consultation", "overdue", "deadline", "due date", "target date", "unknown", "not recorded", "n/a",
          "tbd", "quarter", "half-year", "fiscal", "current", "currently", "now", "still", "hold", "holds", "held",
          "holding", "superseded", "null", "as of", "belong", "belongs", "holder", "responsible", "in charge",
          "owned", "allocated")
_WORD_RE = re.compile(r"[a-z0-9']+(?:-[a-z0-9']+)*")


def words(s: str) -> list[str]:
    return _WORD_RE.findall(s.lower().replace("n't", " n't"))


def has_phrase(s: str, phrases) -> str | None:
    w = " " + " ".join(words(s)) + " "
    for p in phrases:
        if " " + " ".join(words(p)) + " " in w:
            return p
    return None


def name_ok(s: str) -> bool:
    """3.3 / F13R4-04 / SEM-59: names never hold an L_core token, an XF10 word, a banned word, a status word, a
    closed-list verb or cue, a digit-only token or ': ' (option texts with definition lines)."""
    if not isinstance(s, str) or not s.strip() or len(s) > 40 or ": " in s or "\n" in s:
        return False
    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]*[A-Za-z]", s.strip()):
        return False
    w = set(words(s))
    if w & set(L_CORE) or w & set(XF10):
        return False
    return not (has_phrase(s, BANNED) or has_phrase(s, STATUS_WORDS) or has_phrase(s, LEX_VERBS) or
                has_phrase(s, CUES))


def inert_ok(s: str, forbidden=()) -> bool:
    """SEM-62 inert text lint (generator side): no cue, status word, closed verb, banned word, L_core token, digit-led
    threshold, date or label-schema name. `forbidden` = the card's names (outcomes, statuses, categories, attrs)."""
    w = set(words(s))
    if w & set(L_CORE) or w & set(XF10):
        return False
    if has_phrase(s, BANNED) or has_phrase(s, STATUS_WORDS) or has_phrase(s, LEX_VERBS) or has_phrase(s, CUES):
        return False
    if any(f and has_phrase(s, [f]) for f in forbidden):
        return False
    return True


# ------------------------------------------------------------------------------------------------ pack adapter
def _clean_list(vals, n=None):
    out, seen = [], set()
    for v in vals or []:
        if isinstance(v, dict):
            v = v.get("name") or v.get("text") or v.get("term")
        if isinstance(v, str) and name_ok(v) and v.lower() not in seen:
            seen.add(v.lower())
            out.append(v.strip())
    return out[:n] if n else out


def _num(name, unit, dp, lo, hi):
    if not name_ok(name) or dp not in (0, None):
        return None
    try:
        lo, hi = int(lo), int(hi)
    except (TypeError, ValueError):
        return None
    if hi - lo < 20 or lo < 0:
        return None
    if unit is not None and (not isinstance(unit, str) or not re.fullmatch(r"[A-Za-z%°/²³$€£]{1,8}", unit)
                             or unit.lower() in ("no", "not", "or", "if")):
        unit = None
    return {"name": name.strip().lower(), "unit": unit, "lo": lo, "hi": hi}


def _cat(name, values):
    vals = _clean_list(values, 6)
    if not name_ok(name.replace("_", " ")) or len(vals) < 3:
        return None
    return {"name": name.replace("_", " ").strip().lower(), "values": [v.lower() for v in vals]}


def _outsets(sets):
    out = []
    for s in sets or []:
        names = s.get("outcomes") if isinstance(s, dict) else s
        if isinstance(names, list):
            names = [x.get("name") if isinstance(x, dict) else x for x in names]
            ok = _clean_list(names, 6)
            if len(ok) >= 3:
                out.append([o.lower() for o in ok])
    return out


def _people(p):
    for key in ("people",):
        if isinstance(p.get(key), list):
            return _clean_list(p[key])
    nm = p.get("names")
    if isinstance(nm, dict):
        for key in ("persons", "people"):
            if isinstance(nm.get(key), list):
                return _clean_list([x.get("name") if isinstance(x, dict) else x for x in nm[key]])
    return []


def _v_common(p, pack_set, org, persona, decider, roles, ents, nums, cats, outsets, statuses, jargon, inert,
              doc_types, objects, heldout):
    sd = p.get("scope_dimension") or {}
    units = _clean_list(sd.get("values"), 6)
    kind = (sd.get("name") or "").strip().lower()
    people = _people(p)
    return {"pack_id": p["id"], "pack_set": pack_set, "org": org, "persona_seed": persona, "decider": decider,
            "scope_kind": kind if name_ok(kind) else None, "units": units, "people": people,
            "roles": _clean_list(roles), "ents": ents, "nums": [x for x in nums if x],
            "cats": [x for x in cats if x], "outsets": outsets, "statuses": _clean_list(statuses),
            "jargon": _clean_list(jargon, 12), "inert": [s for s in inert if isinstance(s, str)],
            "doc_types": _clean_list(doc_types), "objects": _clean_list(objects), "heldout": heldout,
            "pack_sha": sha(json.dumps(p, sort_keys=True))}


def _ent(noun, plural, prefix):
    if not (isinstance(noun, str) and name_ok(noun)):
        return None
    pre = re.sub(r"[^A-Z]", "", (prefix or "").upper().replace("I", "").replace("L", "").replace("O", ""))[:3]
    if len(pre) < 2:
        pre = re.sub(r"[^A-Z]", "", noun.upper().replace("I", "").replace("L", "").replace("O", ""))[:2]
    if len(pre) < 2:
        return None
    return {"noun": noun.lower(), "plural": (plural or noun + "s").lower(), "prefix": pre}


def _v1(p):
    ents = [_ent(e["type"], e.get("plural"), e.get("id_prefix")) for e in p.get("entity_types", [])]
    nums, cats = [], []
    for a in p.get("attributes", []):
        t = a.get("type")
        if t == "int":
            nums.append(_num(a["name"], a.get("unit"), a.get("decimals", 0), *(a.get("range") or [0, 100])))
        elif t == "cat":
            cats.append(_cat(a["name"], a.get("values", [])))
    jar = [j.get("term") for j in p.get("jargon", []) if isinstance(j, dict)]
    return _v_common(p, "packs-1", p["org"]["name"], p["persona_seed"]["onet_code"], p.get("deciding_role"),
                     p.get("roles"), [e for e in ents if e], nums, cats, _outsets(p.get("outcome_sets")),
                     p.get("status_values"), jar, p.get("inert_fact_types", []),
                     [d.get("type") for d in p.get("document_types", [])], (p.get("objects") or []) +
                     (p.get("sites") or []), int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 8 == 0)


def _v2(p):
    ents = []
    for e in p.get("entity_types", []):
        ents.append(_ent(e.get("singular"), e.get("plural"), (e.get("id_format") or {}).get("prefix")))
    nums, cats = [], []
    rngs = {"int": (0, 200, 0)}
    for k, f in (p.get("field_lexicon") or {}).items():
        t, lab = f.get("type"), f.get("label") or k
        if t == "cat":
            cats.append(_cat(lab, f.get("enum", [])))
        elif t in rngs:
            nums.append(_num(lab, f.get("unit"), 0, *rngs[t][:2]))
    persona = p["persona_seed"]["onet_code"] if isinstance(p.get("persona_seed"), dict) else p.get("persona_seed")
    return _v_common(p, "packs-2", p.get("org_name"), persona, p.get("decider_role"), p.get("roles"),
                     [e for e in ents if e], nums, cats, _outsets(p.get("outcome_sets")), [], p.get(
                         "jargon_candidates"), [], p.get("document_types"), p.get("objects"), False)


def _v3(p):
    ents, nums, cats = [], [], []
    for e in p.get("entity_types", []):
        ents.append(_ent(e.get("name"), e.get("plural"), e.get("id_prefix")))
        for f in e.get("fields", []):
            t = f.get("type")
            if t in ("enum", "status"):
                cats.append(_cat(f["name"], f.get("values", [])))
            elif t == "int":
                r = f.get("range") or [0, 100]
                nums.append(_num(f["name"].replace("_", " "), f.get("unit"), f.get("places", 0), r[0], r[1]))
    persona = p.get("persona_seed") if isinstance(p.get("persona_seed"), str) else None
    return _v_common(p, "packs-3", p.get("org"), persona, p.get("decider_role"), p.get("roles"),
                     [e for e in ents if e], nums, cats, _outsets(p.get("outcome_sets")), [],
                     p.get("jargon_candidates"), p.get("inert_fact_types", []),
                     [d.get("name") if isinstance(d, dict) else d for d in p.get("document_types", [])],
                     p.get("disjoint_fillers", []), bool(p.get("heldout_hint")))


SOURCES = (("packs-3/packs-3.jsonl", _v3), ("packs-1/packs.jsonl", _v1), ("packs-2/packs.jsonl", _v2))


def f13_ready(v) -> str | None:
    """X7 minimums for an F13 pack view (None = ready; else the reason)."""
    if not v["scope_kind"] or len(v["units"]) < 3:
        return "scope"
    if len(v["people"]) + len(v["roles"]) < 8:
        return "holders"
    if not v["ents"]:
        return "registers"
    if len(v["nums"]) < 2:
        return "numeric attributes"
    if not v["outsets"]:
        return "outcome sets"
    if not v["persona_seed"]:
        return "persona"
    bad = set(map(str.lower, v["units"])) & set(map(str.lower, v["people"] + v["roles"]))
    if bad:
        return "holder pool meets scope units"
    return None


@lru_cache(maxsize=1)
def pack_views() -> dict:
    views, drops = {}, {}
    for rel, fn in SOURCES:
        for line in open(PACKS / rel):
            p = json.loads(line)
            try:
                v = fn(p)
            except Exception as e:  # noqa: BLE001
                drops[p.get("id")] = f"adapter: {type(e).__name__}"
                continue
            why = f13_ready(v)
            if why:
                drops[v["pack_id"]] = why
                continue
            views[v["pack_id"]] = v
    pack_views.drops = drops
    return views


def training_packs() -> list:
    return sorted((v for v in pack_views().values() if not v["heldout"]), key=lambda v: (v["pack_set"], v["pack_id"]))


def heldout_packs() -> list:
    return sorted((v for v in pack_views().values() if v["heldout"]), key=lambda v: (v["pack_set"], v["pack_id"]))


# ------------------------------------------------------------------------------------------------ wordings
@lru_cache(maxsize=1)
def wordings() -> list:
    out = []
    for line in open(WORDINGS):
        d = json.loads(line)
        if d.get("family") == "F13":
            out.append({"id": d["id"], "text": d["text"], "forms": d.get("forms") or ["any"],
                        "register": d.get("register")})
    return out


# ------------------------------------------------------------------------------------------------ fmt1 styles
DOC_CONTAINERS = ("memo", "markdown_table", "html_snippet", "json", "yaml", "prose", "bullet_sop")
TABLE_CONTAINERS = ("memo", "markdown_table", "html_snippet", "json", "yaml")


def fmt1():
    from fmt1 import card, pool, render  # noqa: F401
    return card, pool, render


_PROBE = {"title": "Probe", "meta": [["Issued by", "desk"]], "blocks": [
    {"type": "section", "heading": "Part 1", "blocks": [{"type": "items", "items": ["One line.", "Two line."]}]},
    {"type": "section", "heading": "Part 2", "blocks": [{"type": "fields", "label": "Record AB-1234",
                                                          "pairs": [["size", "4 m"], ["site", "north"]]},
                                                         {"type": "items", "items": ["Three line."]}]}]}
_PROBE_T = {"type": "section", "heading": "Part 3", "blocks": [{"type": "table", "caption": "Table T-1",
                                                                "columns": ["ID", "Amount"],
                                                                "rows": [["AB-1234", "4"], ["AB-1235", "5"]]}]}


@lru_cache(maxsize=2)
def styles(held_out: bool) -> tuple:
    """fmt1 styles that render a multi-section F13 document (probe render); each gets s['tables_ok']."""
    _, pool, render = fmt1()
    out = []
    for s in pool.styles(held_out=held_out):
        if s["container"] not in DOC_CONTAINERS:
            continue
        try:
            render.render_state(_PROBE, s)
        except Exception:  # noqa: BLE001
            continue
        s = dict(s)
        try:
            render.render_state({**_PROBE, "blocks": _PROBE["blocks"] + [_PROBE_T]}, s)
            s["tables_ok"] = True
        except Exception:  # noqa: BLE001
            s["tables_ok"] = False
        out.append(s)
    return tuple(out)


# ------------------------------------------------------------------------------------------------ tokenizer
@lru_cache(maxsize=1)
def tok():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)


def n_tok(text: str) -> int:
    return len(tok()(text, add_special_tokens=False)["input_ids"])


def n_tok_many(texts: list) -> list:
    return [len(x) for x in tok()(texts, add_special_tokens=False)["input_ids"]]


def offsets(text: str) -> list:
    """Char start of every token (for decile depths)."""
    enc = tok()(text, add_special_tokens=False, return_offsets_mapping=True)
    return [a for a, _ in enc["offset_mapping"]]


@lru_cache(maxsize=1)
def dio():
    card, _, _ = fmt1()
    d = card._dio()
    d.STYLE, d.LAYOUT = "cygnet", "schema_branch_mark"
    return d


def measured_perms(row: dict, n: int) -> list:
    """F13R1-30 / F13R2-19: canonical, reversed and 16 seeded orders (all orders when n <= 3)."""
    import itertools
    if n <= 3:
        return [list(p) for p in itertools.permutations(range(n))]
    r = rng("f13-perm", row["id"])
    out = [list(range(n)), list(range(n))[::-1]]
    for _ in range(16):
        p = list(range(n))
        r.shuffle(p)
        out.append(p)
    return out


def served_tokens(row: dict) -> int:
    """Max real-token length of the served chat (system turn + user_msg, cygnet / schema_branch_mark) over the
    measured option orders; instructions and options are printed twice by the layout, as served."""
    d = dio()
    card, _, _ = fmt1()
    n = 2 if row["qtype"] == "noul" else len(row["options"])
    texts = []
    with card._serving(d, n):
        for p in measured_perms(row, n):
            texts.append(d.render_chat(tok(), d.CYGNET_SYSTEM, d.user_msg(row, p)))
    return max(n_tok_many(texts))
