"""Pack adapter for F4: one uniform F4 view per domain pack (packs-1..4 have four schemas).

The view holds what F4 needs (G0 spec 2.1, 2.2 #6, 7.5): 2-4 specific type nouns plus an umbrella noun, invented
predicate words (the pack's own invented jargon first, then program-made nonce words checked against the system word
list), quantities with units and ranges, date attributes and the pack's date window, directional links, trusted and
untrusted source names, document names, background sentences, the deciding role and the O*NET persona seed.

Pack QC (2.2 #6), applied by program here: every value passes the 2.1 status / epistemic ban, type nouns share no
content word or 4-letter stem with each other, with links, quantities or predicates; links are directional (closed
ban list of symmetric / transitive phrases; no converse pair in one pack); predicates are invented words, so no
predicate pair, predicate-link or predicate-quantity pair carries a commonsense tie. Values that fail are dropped; a
pack that cannot serve F4 is left out (reason counted). Entity IDs are made per card by ids_for_card() (neutral prefix,
no type or property hint; unmarked IDs pairwise at Hamming distance >= 3; look-alike pairs marked).

Held-out packs (S5 only): the union of the pack agents' own hints, the same rule F3 uses: packs-1 sha256(id) mod 8 == 0,
packs-3 heldout_hint, packs-4 split_hint == "heldout". Training cards never use these packs.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
C_SRC = LEAN / "c_src"
PACKS = C_SRC / "packs"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(C_SRC / "common"))
import f4lex as L  # noqa: E402
import negcount  # noqa: E402

DICT_WORDS = HERE / "words_web2.txt"    # vendored copy of macOS /usr/share/dict/web2 (sha256 be41ad97963b), so remote (rrun) builds match local

SYMMETRIC_LINK_BAN = ("shares", "share", "co-", "linked to", "matches", "match", "is part of", "part of",
                      "downstream", "within", "together", "with each other", "partners with", "neighbours",
                      "neighbors", "is near", "adjacent", "same as", "related to", "connected to", "paired with",
                      "twinned", "alongside", "mutual")
NEG_PREFIX = ("un", "non", "dis", "mis", "in", "im", "ir", "il", "de", "anti", "pre", "re", "over", "under", "counter")
BAD_SUFFIX = ("less", "ness", "ful", "ism", "ist", "itis", "phobia", "ology", "able", "ible", "ed", "ing")
STOP = {"a", "an", "the", "of", "and", "or", "to", "in", "on", "for", "by", "at", "with", "per", "from", "is", "are",
        "was", "were", "be", "its", "it", "as"}


def uh(*parts) -> float:
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def rng_for(*parts) -> random.Random:
    return random.Random(int(hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).hexdigest()[:16], 16))


@lru_cache(maxsize=1)
def english() -> frozenset:
    try:
        return frozenset(w.strip().lower() for w in DICT_WORDS.read_text(errors="ignore").splitlines() if w.strip())
    except OSError:
        return frozenset()


def content_words(s: str) -> set:
    return {w for w in L.words(s) if w not in STOP and len(w) >= 3}


def stems(s: str) -> set:
    return {w[:4] for w in content_words(s) if len(w) >= 4}


def edit(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def clean_phrase(s) -> str | None:
    """A pack string usable in F4 text: one line, letters/digits/space/'-, no status word, no XF06 marker, no ': '."""
    if not isinstance(s, str):
        return None
    s = " ".join(s.split())
    if not s or len(s) > 48 or ": " in s or ";" in s or '"' in s or "(" in s or "|" in s:
        return None
    if L.status_hit(s):
        return None
    if any(m.lower() == s.lower() for m in L.XF06_BANNED):
        return None
    if not (len(s) >= 2 and s[0].isalnum() and s[-1].isalnum()
            and all(ch.isascii() and (ch.isalnum() or ch in " '-") for ch in s)):
        return None
    return s


def plural_of(noun: str) -> str:
    w = noun.split()
    last = w[-1]
    if last.endswith(("s", "x", "ch", "sh", "z")):
        p = last + "es"
    elif last.endswith("y") and last[-2:-1] not in "aeiou":
        p = last[:-1] + "ies"
    else:
        p = last + "s"
    return " ".join(w[:-1] + [p])


# ----------------------------------------------------------------------------------------------- nonce predicate words
ONSETS = ("b", "d", "f", "g", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z", "br", "dr", "fr", "gr", "kr", "pr",
          "tr", "bl", "fl", "gl", "kl", "pl", "sk", "sp", "st", "sv", "th", "ch")
VOWELS = ("a", "e", "i", "o", "u", "ai", "ea", "ou", "oa", "au")
CODAS = ("", "n", "r", "l", "m", "s", "t", "k", "nd", "rt", "sk", "lm", "rn", "ld", "nt", "rv")


@lru_cache(maxsize=1)
def english_sub() -> frozenset:
    """English words of 5+ letters (substring check: an invented word holds no real word of 5+ letters)."""
    return frozenset(w for w in english() if len(w) >= 5 and w.isalpha())


def has_english_sub(w: str) -> bool:
    E = english_sub()
    for i in range(len(w)):
        for j in range(i + 5, len(w) + 1):
            if w[i:j] in E:
                return True
    return False


def nonce_words(key: str, n: int, avoid: set) -> list[str]:
    r = rng_for("f4-nonce", key)
    eng = english()
    out: list[str] = []
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        w = r.choice(ONSETS) + r.choice(VOWELS) + r.choice(CODAS) + r.choice(ONSETS[:16]) + r.choice(VOWELS) \
            + r.choice(CODAS[1:])
        if not (6 <= len(w) <= 10) or w in eng or w in avoid or has_english_sub(w):
            continue
        if w.startswith(NEG_PREFIX) or w.endswith(BAD_SUFFIX) or re.search(r"[^aeiou]{4}", w):
            continue
        if any(edit(w, x) < 3 or w[:3] == x[:3] or w in x or x in w for x in out + sorted(avoid)):
            continue
        if negcount.count(w).k_all or L.status_hit(w):
            continue
        out.append(w)
    return out


def jargon_ok(w: str) -> bool:
    if not isinstance(w, str) or not re.fullmatch(r"[a-z]{5,11}", w):
        return False
    if w in english() or w.startswith(NEG_PREFIX) or w.endswith(BAD_SUFFIX) or has_english_sub(w):
        return False
    if negcount.count(w).k_all or L.status_hit(w):
        return False
    return True


# ----------------------------------------------------------------------------------------------- per schema extraction

def _ex_p1(p):
    types = [(e["type"], e.get("plural") or plural_of(e["type"])) for e in p["entity_types"]]
    qty = []
    for a in p["attributes"]:
        if a.get("type") in ("int", "num") and a.get("range") and a.get("unit"):
            dec = int(a.get("decimals") or 0)
            qty.append({"name": a["name"], "unit": a["unit"], "lo": a["range"][0], "hi": a["range"][1], "dec": dec,
                        "type": None})
    dates = [a["name"] for a in p["attributes"] if a.get("type") == "date"]
    src = list(p.get("source_names") or [])
    trusted = [s for s in src if uh("f4-trust", p["id"], s) < 0.5]
    untrusted = [s for s in src if s not in trusted]
    docs = [d["type"] for d in p.get("document_types", [])]
    bg = [x[:1].upper() + x[1:] + "." for x in p.get("inert_fact_types", []) if isinstance(x, str)]
    jar = [j.get("term") for j in p.get("jargon", [])]
    return dict(pack_set="packs-1", persona_seed=p["persona_seed"]["onet_code"],
                persona_title=p["persona_seed"]["onet_title"], role=p.get("deciding_role"), types=types,
                umbrella=None, qty=qty, dates=dates, window=None, links=[], trusted=trusted, untrusted=untrusted,
                docs=docs, background=bg, jargon=jar,
                heldout=int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 8 == 0)


def _ex_p2(p):
    types, qty, dates = [], [], []
    key2idx = {}
    for i, e in enumerate(p["entity_types"]):
        types.append((e["singular"], e["plural"]))
        key2idx[e["key"]] = i
        for a in e.get("attributes", []):
            t = a.get("type")
            if t in ("int", "dec1", "dec2", "money") and a.get("unit") and a.get("min") is not None:
                dec = int(a.get("places") or (2 if t == "money" else (1 if t == "dec1" else 0)))
                if t == "money":
                    dec = 0
                qty.append({"name": a.get("label"), "unit": a["unit"], "lo": a["min"], "hi": a["max"], "dec": dec,
                            "type": i})
            if t == "date" and a.get("label"):
                dates.append(a["label"])
    links = []
    for lk in p.get("links", []):
        if lk.get("from") in key2idx and lk.get("to") in key2idx:
            links.append({"active": lk["active"], "passive": lk["passive"], "from": key2idx[lk["from"]],
                          "to": key2idx[lk["to"]]})
    src = list(p.get("source_names") or [])
    trusted = [s for s in src if uh("f4-trust", p["id"], s) < 0.5]
    untrusted = [s for s in src if s not in trusted]
    dw = p.get("date_window") or {}
    window = (dw.get("start"), dw.get("span_days")) if dw.get("start") else None
    return dict(pack_set="packs-2", persona_seed=p["persona_seed"]["onet_code"],
                persona_title=p["persona_seed"]["onet_title"], role=p.get("decider_role"), types=types,
                umbrella=None, qty=qty, dates=dates, window=window, links=links, trusted=trusted,
                untrusted=untrusted, docs=list(p.get("document_types") or []), background=[],
                jargon=list(p.get("jargon_candidates") or []), heldout=False)


def _ex_p3(p):
    types, qty, dates = [], [], []
    for i, e in enumerate(p["entity_types"]):
        types.append((e["name"], e["plural"]))
        for f in e.get("fields", []):
            t = f.get("type")
            nm = f["name"].replace("_", " ")
            if t in ("int", "amt", "dec") and f.get("unit") and f.get("range"):
                qty.append({"name": nm, "unit": f["unit"], "lo": f["range"][0], "hi": f["range"][1],
                            "dec": int(f.get("places") or 0) if t != "amt" else 0, "type": i})
            if t == "date":
                dates.append(nm)
    links = []
    for j, lk in enumerate(p.get("links", [])):
        n = len(types)
        a = int(uh("f4-linkfrom", p["id"], j) * n)
        b = int(uh("f4-linkto", p["id"], j) * n)
        links.append({"active": lk["active"], "passive": lk["passive"], "from": a, "to": b})
    sn = p.get("source_names") or {}
    return dict(pack_set="packs-3", persona_seed=p["persona_seed"], persona_title=(p.get("persona") or {}).get("title"),
                role=p.get("decider_role"), types=types, umbrella=None, qty=qty, dates=dates, window=None,
                links=links, trusted=list(sn.get("trusted", [])), untrusted=list(sn.get("untrusted", [])),
                docs=[d["name"] for d in p.get("document_types", [])], background=[],
                jargon=list(p.get("jargon_candidates") or []), heldout=bool(p.get("heldout_hint")))


def _ex_p4(p):
    tid2idx = {}
    types = []
    for i, e in enumerate(p["entity_types"]):
        types.append((e["noun"], e["plural"]))
        tid2idx[e["id"]] = i
    qty = []
    for q in p.get("quantities", []):
        unit = q["unit"]
        un = {u["name"]: u for u in p.get("units", [])}
        if unit in un:
            unit = un[unit]["plural"]
        elif unit == "brasslet" or unit == (p.get("currency") or {}).get("name"):
            unit = (p.get("currency") or {}).get("plural") or unit
        tix = None
        for e in p["entity_types"]:
            if any(f.get("word") == q["name"] for f in e.get("fields", [])):
                tix = tid2idx[e["id"]]
        qty.append({"name": q["name"], "unit": unit, "lo": q["min"], "hi": q["max"], "dec": int(q.get("decimals") or 0),
                    "type": tix})
    dates = []
    for e in p["entity_types"]:
        for f in e.get("fields", []):
            if "date" in f.get("word", ""):
                dates.append(f["word"])
    links = []
    for lk in p.get("links", []):
        if lk.get("from") in tid2idx and lk.get("to") in tid2idx:
            links.append({"active": lk["active"], "passive": lk["passive"], "from": tid2idx[lk["from"]],
                          "to": tid2idx[lk["to"]]})
    dw = p.get("date_window") or {}
    window = (dw.get("start"), dw.get("end")) if dw.get("start") else None
    um = p.get("umbrella") or {}
    return dict(pack_set="packs-4", persona_seed=p["persona_seed"], persona_title=p["persona"].get("onet_title"),
                role=p["persona"].get("deciding_role"), types=types,
                umbrella=(um.get("noun"), um.get("plural")) if um.get("noun") else None, qty=qty, dates=dates,
                window=window, links=links, trusted=[s["name"] for s in p["sources"]["trusted"]],
                untrusted=[s["name"] for s in p["sources"]["untrusted"]], docs=[d["name"] for d in p["documents"]],
                background=[x["text"].rstrip(".") + "." for x in p.get("inert_facts", [])],
                jargon=[j["term"] for j in p.get("jargon", [])], heldout=p.get("split_hint") == "heldout")


SOURCES = (("packs-1/packs.jsonl", _ex_p1), ("packs-2/packs.jsonl", _ex_p2), ("packs-3/packs-3.jsonl", _ex_p3),
           ("packs-4/packs.jsonl", _ex_p4))

UMBRELLA_POOL = (("file entry", "file entries"), ("listed item", "listed items"), ("case item", "case items"),
                 ("register entry", "register entries"), ("tracked item", "tracked items"))


def _finish(pid: str, v: dict):
    """Apply F4 pack QC. Returns (view, None) or (None, reason)."""
    # persona / role
    role = clean_phrase(v.get("role") or "")
    if role and L.wording_hit(role):
        role = None
    if not role:
        t = clean_phrase(v.get("persona_title") or "")
        role = t if t and not L.wording_hit(t) else None
    if not role:
        return None, "role_lint"
    v["role"] = role.lower() if role.isupper() else role
    # types
    types = []
    for sg, pl in v["types"]:
        sg, pl = clean_phrase(sg), clean_phrase(pl)
        if not sg or not pl or L.wording_hit(sg) or sg.lower() in ("item", "entry", "record", "case"):
            continue
        if sg[:1].isupper() and not sg.isupper():
            sg, pl = sg[:1].lower() + sg[1:], pl[:1].lower() + pl[1:]
        if any((content_words(sg) & content_words(t)) or (stems(sg) & stems(t)) for t, _ in types):
            continue  # word-meaning tie between type nouns (overlap / hypernym by shared word)
        types.append((sg, pl))
    if len(types) < 2:
        return None, "types_lt2"
    types = types[:4]
    tw = set().union(*(content_words(t) | stems(t) for t, _ in types))
    # umbrella
    um = v.get("umbrella")
    if um and clean_phrase(um[0]) and clean_phrase(um[1]) and not (content_words(um[0]) & tw):
        umbrella = (um[0][:1].lower() + um[0][1:], um[1][:1].lower() + um[1][1:])
    else:
        umbrella = UMBRELLA_POOL[int(uh("f4-umbrella", pid) * len(UMBRELLA_POOL))]
    # links
    links = []
    for lk in v["links"]:
        a, ps = clean_phrase(lk.get("active")), clean_phrase(lk.get("passive"))
        if not a or not ps or lk["from"] >= len(types) or lk["to"] >= len(types):
            continue
        low = " " + a.lower() + " "
        if any((" " + b + " ") in low or low.strip().startswith(b) for b in SYMMETRIC_LINK_BAN):
            continue
        if content_words(a) & tw or stems(a) & tw or negcount.count(a).k_all:
            continue
        if a.lower().startswith(("is ", "are ", "was ", "has ", "have ")):
            continue  # an active phrase must be a plain verb phrase ("<X> <active> <Y>")
        if any(content_words(a) & content_words(o["passive"]) or content_words(a) & content_words(o["active"])
               for o in links):
            continue  # converse or overlapping pair in one pack
        links.append({"active": a, "passive": ps, "from": lk["from"], "to": lk["to"]})
    # quantities
    qty = []
    for q in v["qty"]:
        nm, un = clean_phrase(q.get("name") or ""), clean_phrase(str(q.get("unit") or ""))
        if not nm or not un and q.get("unit") != "%":
            continue
        if q.get("unit") == "%":
            un = "%"
        if content_words(nm) & tw or stems(nm) & tw or L.wording_hit(nm) or negcount.count(nm).k_all:
            continue
        lw = L.words(nm)
        if not 1 <= len(lw) <= 3 or set(lw) & STOP or (lw[-1].endswith("s") and not lw[-1].endswith("ss")) \
                or lw[-1].endswith(("ed", "cast", "made", "done", "paid", "owed")):
            continue
        if str(q.get("unit")).lower() in ("count", "units", "unit", "items", "number", "times"):
            continue
        if any(content_words(nm) & content_words(o["name"]) for o in qty):
            continue
        try:
            lo, hi = float(q["lo"]), float(q["hi"])
        except (TypeError, ValueError):
            continue
        if not hi > lo or lo < 0:
            continue
        dec = min(int(q.get("dec") or 0), 2)
        if hi - lo < 8 * 10 ** (-dec):
            continue
        t = q.get("type")
        qty.append({"name": nm.lower(), "unit": un, "lo": lo, "hi": hi, "dec": dec,
                    "type": t if isinstance(t, int) and t < len(types) else None})
    # dates
    dates = []
    for d in v["dates"]:
        d = clean_phrase(d)
        if not d or "date" not in d.lower() or content_words(d) & tw or len(d.split()) > 3:
            continue
        if d.lower() not in dates:
            dates.append(d.lower())
    if not dates:
        dates = ["filing date", "entry date"]
    # sources
    def src_ok(s):
        s = clean_phrase(s)
        if not s or re.search(r"\d", s) or L.wording_hit(s.replace("report", "")) in ("true", "false", "claim"):
            return None
        return s
    tr = [s for s in (src_ok(x) for x in v["trusted"]) if s]
    un_ = [s for s in (src_ok(x) for x in v["untrusted"]) if s]
    allsrc = []
    for s in tr + un_:
        if any(edit(s.lower(), o.lower()) < 4 or (content_words(s) & content_words(o)) for o in allsrc):
            continue
        allsrc.append(s)
    tr = [s for s in tr if s in allsrc]
    un_ = [s for s in un_ if s in allsrc]
    # documents and background
    docs = []
    banned_doc_words = {"report", "statement"} | set().union(*(content_words(s) for s in tr + un_)) \
        | set().union(*(content_words(q["name"]) for q in qty)) | set().union(*(content_words(l["active"]) for l in links))
    for d in v["docs"]:
        d = clean_phrase(d)
        if d and not (content_words(d) & banned_doc_words) and len(d) <= 32 and not L.wording_hit(d):
            docs.append(d[:1].lower() + d[1:] if not d[:2].isupper() else d)
    bg = []
    for s in v["background"]:
        if not isinstance(s, str) or re.search(r"\d", s) or L.status_hit(s) or ": " in s or len(s) > 110:
            continue
        if any(w in content_words(s) for w in tw) or any(L.has_phrase(s, x) for x in tr + un_):
            continue
        if negcount.count(s).k_all:
            continue
        bg.append(" ".join(s.split()))
    # predicates: pack jargon first, then nonce words
    avoid = set()
    for t, pl in types:
        avoid |= set(L.words(t)) | set(L.words(pl))
    jar = []
    for w in v["jargon"]:
        if jargon_ok(w) and not any(edit(w, x) < 3 or w[:3] == x[:3] or w in x or x in w for x in jar):
            jar.append(w)
    preds = jar + nonce_words(pid, 40 - len(jar), set(jar) | avoid)
    return dict(pack_id=pid, pack_set=v["pack_set"], heldout=bool(v["heldout"]), persona_seed=v["persona_seed"],
                persona_title=v.get("persona_title"), role=v["role"], types=types, umbrella=umbrella, qty=qty,
                dates=dates, window=v.get("window"), links=links, trusted=tr, untrusted=un_, docs=docs,
                background=bg, preds=preds, n_jargon=len(jar)), None


@lru_cache(maxsize=1)
def load_views():
    views, drops = {}, {}
    for rel, fn in SOURCES:
        with open(PACKS / rel, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                p = json.loads(line)
                pid = p.get("id") or p.get("pack_id")
                try:
                    v = fn(p)
                except (KeyError, IndexError, TypeError) as e:
                    drops["schema:" + type(e).__name__] = drops.get("schema:" + type(e).__name__, 0) + 1
                    continue
                v2, why = _finish(pid, v)
                if v2 is None:
                    drops[why] = drops.get(why, 0) + 1
                    continue
                views[pid] = v2
    return views, drops


def training_packs():
    views, _ = load_views()
    return sorted((v for v in views.values() if not v["heldout"]), key=lambda v: v["pack_id"])


def heldout_packs():
    views, _ = load_views()
    return sorted((v for v in views.values() if v["heldout"]), key=lambda v: v["pack_id"])


# ----------------------------------------------------------------------------------------------- per-card entity IDs
ID_LETTERS = "BCDFGHJKLMNPQRSTVWXZ"
ID_DIGITS = "23456789"


def ids_for_card(card_key: str, n: int, n_look: int = 0) -> tuple[list[str], list[tuple[str, str]]]:
    """n entity IDs with one neutral prefix per card (no type or property hint), pairwise Hamming distance >= 3 on the
    4-character body, plus n_look marked look-alike partners (one substitution or one adjacent transposition)."""
    r = rng_for("f4-ids", card_key)
    pre = r.choice(ID_LETTERS) + r.choice(ID_LETTERS)
    shape = r.choice(("LDDDD", "DDLDD", "DLDDD", "DDDLD", "DDDDD"))
    sep = r.choice(("-", "-", "/"))

    def body():
        return "".join(r.choice(ID_LETTERS if c == "L" else ID_DIGITS) for c in shape)

    def ham(a, b):
        return sum(x != y for x, y in zip(a, b))
    bodies: list[str] = []
    tries = 0
    while len(bodies) < n and tries < 50000:
        tries += 1
        b = body()
        if all(ham(b, x) >= 3 for x in bodies):
            bodies.append(b)
    if len(bodies) < n:
        raise ValueError("id pool exhausted")
    looks = []
    for b in bodies[:n_look]:
        for _ in range(200):
            c = list(b)
            if r.random() < 0.5:
                i = r.randrange(len(c))
                c[i] = r.choice(ID_LETTERS if shape[i] == "L" else ID_DIGITS)
            else:
                i = r.randrange(len(c) - 1)
                if shape[i] != shape[i + 1]:
                    continue
                c[i], c[i + 1] = c[i + 1], c[i]
            nb = "".join(c)
            if nb != b and 1 <= ham(nb, b) <= 2 and all(ham(nb, x) >= 3 for x in bodies if x != b) \
                    and all(ham(nb, y) >= 1 for _, y in looks):
                looks.append((b, nb))
                break
    ids = [pre + sep + b for b in bodies]
    pairs = [(pre + sep + a, pre + sep + b) for a, b in looks]
    return ids, pairs


if __name__ == "__main__":
    views, drops = load_views()
    tr, ho = training_packs(), heldout_packs()
    import collections
    print(json.dumps({"usable": len(views), "training": len(tr), "heldout": len(ho), "drops": drops,
                      "by_set": collections.Counter(v["pack_set"] for v in views.values()),
                      "heldout_by_set": collections.Counter(v["pack_set"] for v in ho),
                      "with_links": sum(1 for v in views.values() if v["links"]),
                      "with_qty2": sum(1 for v in views.values() if len(v["qty"]) >= 2),
                      "with_src": sum(1 for v in views.values() if len(v["trusted"]) >= 1 and len(v["untrusted"]) >= 1),
                      "with_bg": sum(1 for v in views.values() if len(v["background"]) >= 2),
                      "n_jargon_mean": round(sum(v["n_jargon"] for v in views.values()) / max(1, len(views)), 2),
                      "types_hist": collections.Counter(len(v["types"]) for v in views.values())}, indent=1,
                     default=str))
