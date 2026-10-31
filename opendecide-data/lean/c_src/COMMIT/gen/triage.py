"""TRIAGE generator (G0 section 3): which type tag did the author give the change? Choice among 4-10 of the 10 types
(named, masked IDs, swapped-name twins), per-label yes/no rows (1.11), message-only slice (3.5).
Solver A: regex parse of the EBNF + Python path classes. Solver B: a character-scanner state machine for the EBNF +
sqlite path classes (3.4). Gold is the author's own tag (a human label on real text, 3.8)."""
from __future__ import annotations

import collections
import fnmatch
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import core as K  # noqa: E402
import frame as FR  # noqa: E402
import lex2 as L  # noqa: E402
import records as RC  # noqa: E402
import texts as T  # noqa: E402

TYPES = ["feat", "fix", "docs", "refactor", "perf", "test", "build", "ci", "chore", "revert"]
HDR_A = re.compile(r"^([A-Za-z]+)(\([^():\n]+\))?(!)?: +(.*)$")
TCLS = None


def tcls() -> dict:
    global TCLS
    if TCLS is None:
        TCLS = RC.lex()["triage_classes"]
    return TCLS


# ---------------------------------------------------------------------------------------------------------------
# solver A: regex parse of the header EBNF

def parse_A(msg: str):
    first, _, rest = msg.partition("\n")
    m = HDR_A.match(first)
    if not m or m.group(1).lower() not in TYPES:
        return None
    subj = m.group(4)
    if not subj.strip():
        return None
    if parse_A(subj) is not None:
        return None
    return m.group(1).lower(), subj + ("\n" + rest if rest else "")


# solver B: character scanner (no regex)
def parse_B(msg: str):
    first = msg.split("\n", 1)[0]
    i, n = 0, len(first)
    while i < n and first[i].isascii() and first[i].isalpha():
        i += 1
    typ = first[:i].lower()
    if typ not in TYPES or i == 0:
        return None
    if i < n and first[i] == "(":
        j = i + 1
        while j < n and first[j] not in "():":
            j += 1
        if j >= n or first[j] != ")" or j == i + 1:
            return None
        i = j + 1
    if i < n and first[i] == "!":
        i += 1
    if i >= n or first[i] != ":":
        return None
    i += 1
    if i >= n or first[i] != " ":
        return None
    while i < n and first[i] == " ":
        i += 1
    subj = first[i:]
    if not subj.strip():
        return None
    if parse_B(subj) is not None:
        return None
    return typ, msg[len(first) - len(subj):] if True else None


def has_header_anywhere_B(text: str) -> bool:
    for ln in text.split("\n"):
        for start in range(len(ln)):
            if start == 0 or not (ln[start - 1].isalnum()):
                if parse_B(ln[start:]) is not None:
                    return True
    return False


# ---------------------------------------------------------------------------------------------------------------
# consistency filters (3.2), solver A form

def file_cls_A(f: dict) -> frozenset:
    return frozenset(c for c, cl in tcls().items() if K.file_in_A(f, cl))


def _pat(name: str, pats) -> bool:
    return any(fnmatch.fnmatchcase(name.lower(), p.lower()) for p in pats)


def filters_A(rec: dict, typ: str) -> str | None:
    lx = RC.lex()
    files = rec["files"]
    if not K.plain_files(rec):
        return "rename_mode_binary"
    names = [f["path"].split("/")[-1] for f in files]
    if all(_pat(n, lx["manifest_patterns"] + lx["lockfile_patterns"]) for n in names):
        return "dependency_only"
    if all(_pat(n, lx["changelog_patterns"]) for n in names):
        return "changelog_only"
    cls = [file_cls_A(f) for f in files]
    alls = [c for c in ("docs", "test", "ci") if all(c in s for s in cls)]
    if len(alls) >= 2:
        return "two_all_rules"
    if alls and typ != alls[0]:
        return "all_rule_conflict"
    if typ in ("docs", "test", "ci") and not all(typ in s for s in cls):
        return "gold_class_conflict"
    if typ == "build" and not any("build" in s for s in cls):
        return "build_without_build_file"
    return None


def eligible(rec: dict):
    p = parse_A(rec["msg"])
    if p is None:
        return None
    typ, stripped = p
    if filters_A(rec, typ):
        return None
    if has_header_anywhere_B(stripped):
        return None
    subj = stripped.split("\n", 1)[0].strip()
    lines = [t for f in rec["files"] for h in f["hunks"] for k, t in h["lines"] if k in "+-"]
    if len(subj.split()) >= 4 and any(subj in t for t in lines):
        return None
    for f in rec["files"]:
        if "docs" in file_cls_A(f):
            for h in f["hunks"]:
                for k, t in h["lines"]:
                    if k in "+-" and has_header_anywhere_B(t):
                        return None
    return typ, stripped


_MO_CACHE = {}
_S4_CACHE = {}


def _s4_key(rid: str, stripped: str, typ: str) -> int:
    k = (rid, typ)
    if k not in _S4_CACHE:
        toks = C.m_tokens(stripped)
        _S4_CACHE[k] = 0 if any(t in L.TYPE_STEMS[o] for o in TYPES if o != typ for t in toks) else 1
    return _S4_CACHE[k]


def _mo_ok_cached(rid: str, stripped: str):
    if rid not in _MO_CACHE:
        _MO_CACHE[rid] = bool(mo_ok(FR.rec(rid), stripped))
    return _MO_CACHE[rid]


def mo_ok(rec: dict, stripped: str):
    words = [w for w, _ in K.msg_words(stripped) if not re.fullmatch(r"\[(?:hash|person|email|date|link|secret|ip)\]",
                                                                      w)]
    if len(words) < 5:
        return None
    own = set()
    for f in rec["files"]:
        own.update(C.m_tokens(f["path"]))
        own.update(t for x in C.identifiers([t for h in f["hunks"] for k, t in h["lines"] if k in "+-"])
                   for t in C.m_tokens(x))
    hits = [(t, p) for t, p in C.m_tokens(stripped, with_pos=True) if t in own]
    if len(hits) < 1:
        return None
    return [{"entity": "own_paths_identifiers", "token": t, "position": p, "alias": False} for t, p in hits]


# ---------------------------------------------------------------------------------------------------------------
# options, definitions, card text

BUCKETS = [(4, 0.24), (6, 0.12), (7, 0.12), (8, 0.12), (10, 0.40)]


def bucket(key: str) -> int:
    u = C.h01("tbucket", key)
    acc = 0
    for k, w in BUCKETS:
        acc += w
        if u < acc:
            return k
    return 10


def subset(gold: str, k: int, key: str) -> list[str]:
    shown = [gold] + [p for p in L.PARTNERS[gold]]
    rest = sorted((t for t in TYPES if t not in shown), key=lambda t: C.h01("decoy", key, t))
    for d in rest:
        if len(shown) >= k:
            break
        if d in shown:
            continue
        shown.append(d)
        for p in L.PARTNERS[d]:
            if len(shown) < k and p not in shown:
                shown.append(p)
    shown = shown[:k]
    if gold not in shown:
        shown[0] = gold
    return sorted(shown, key=lambda t: C.h01("topt", key, t))


def card_defs(card_id: str) -> dict:
    return {t: L.TYPE_DEFS[t][int(C.h01("tdef", card_id, t) * 3)] for t in TYPES}


def clause_ids(view: str, form: str) -> list[str]:
    if view == "message_only":
        ids = ["SEM-04t", "SEM-27mo" if form == "masked" else "SEM-27o", "SEM-28"]
    else:
        ids = ["SEM-01", "SEM-02", "SEM-27m" if form in ("masked", "swapped") else "SEM-27", "SEM-28", "SEM-08"]
    ids += ["SEM-30", "SEM-31d" if view != "message_only" else "SEM-31m", "SEM-32", "SEM-41"]
    if form == "swapped":
        ids.append("SEM-47")
    if form == "per_label":
        ids.append("SEM-49t")
    return ids


def card_ir(card: dict, view: str, form: str, opts: list[str], defs_for: dict, persona=None) -> dict:
    blocks = []
    if persona:
        blocks.append({"type": "para", "text": T.PERSONA.format(title=persona[1])})
    items = [T.SEM[i] for i in clause_ids(view, form)] + (["SEM-45: " + T.SEM["SEM-45"]] if False else [])
    if persona:
        items.append(T.SEM["SEM-45"])
    blocks.append({"type": "section", "heading": "How to read the task", "blocks": [{"type": "items", "items": items}]})
    if view != "message_only":
        blocks.append({"type": "section", "heading": "File classes", "blocks": [
            {"type": "para", "text": T.class_line(c if c != "ci" else "CI", cl)} for c, cl in tcls().items()]})
    blocks.append({"type": "defs", "variant": "DV01", "heading": "Types",
                   "entries": [{"name": o, "text": defs_for[o]} for o in opts]})
    return {"title": "Change types", "blocks": blocks}


# ---------------------------------------------------------------------------------------------------------------
# cards and rows

CC = "CommitChronicle"
SAMPLERS = ["S1", "S2", "S3", "S4"]


def build_cards(split_kind: str = "train", n: int = 24) -> list[dict]:
    g = FR.groups()["groups"]
    elig = {gid for gid, x in g.items() if x["triage_eligible"]}
    cards = []
    ids = [f"CMT{i + 1:03d}" if split_kind == "train" else f"CMTD{i + 1:02d}" for i in range(n)]
    rates = FR.antithetic_rates(ids, 25, "triage-pl-" + split_kind)
    for i, cid in enumerate(ids):
        gsplit = "train" if split_kind == "train" else "heldout"
        pk, gs = FR.pack(cid, gsplit, CC, frac=0.4 if gsplit == "train" else 1.0, eligible=elig)
        cards.append({"card_id": cid, "type": "triage", "sampler": SAMPLERS[i % 4] if split_kind == "train" else "S5",
                      "ds": CC, "pack_id": pk, "groups": gs, "r": rates[cid], "fewshot": False, "inverted": False,
                      "defs_style": "one_line", "defs": card_defs(cid),
                      "persona": FR.draw_persona(cid) if C.h01("persona", cid) < 0.45 else None})
    return cards


_CANDS = {}


def _cands(card, gsplit):
    k = (card["card_id"], gsplit)
    if k not in _CANDS:
        _CANDS[k] = _cands0(card, gsplit)
    return _CANDS[k]


def _cands0(card, gsplit):
    gset = set(card["groups"])
    ix = FR.index()
    out = collections.defaultdict(list)
    for rid in sorted((r for r, x in ix.items() if x["group"] in gset and x["split"] == gsplit and x["n_files"] <= 20
                       and not x["bot"]), key=lambda r: C.h01("tcand", card["card_id"], r)):
        e = eligible(FR.rec(rid))
        if e:
            out[e[0]].append((rid, e[1]))
    return out


def build_rows(card: dict, em: FR.Emitter, reg: FR.Registry, split: str, n_rows: int, mo_share: float = 0.3,
               pl_share: float = 1 / 3, twin_share: float = 0.17):
    gsplit = "heldout" if split == "dev" else "train"
    by = _cands(card, gsplit)
    stats = collections.Counter({f"pool_{t}": len(v) for t, v in by.items()})
    n_pl = round(pl_share * n_rows) if split != "dev" else 0
    n_mo = round(mo_share * n_rows)
    n_ch = n_rows - n_pl - n_mo
    wch = FR.card_wordings("triage", "choice", card["card_id"])
    wyn = FR.card_wordings("triage", "yn", card["card_id"])
    n_tw = int(twin_share * n_rows) if split != "dev" else 0
    yes_pl = round(card["r"] * n_pl)
    plan = [("message_only", "choice")] * n_mo + [("message_diff", "choice")] * n_ch + \
        [("message_diff", "per_label")] * n_pl
    pos = card.get('_pos_' + split, 0)
    pl_i = 0
    for i, (view, form) in enumerate(plan):
        typ = TYPES[(i + int(C.h01("toff", card["card_id"], split) * 10)) % 10]
        pool_ = [(r, s) for r, s in by.get(typ, []) if reg.can_base(r, "triage", split)]
        if card["sampler"] == "S4":
            pool_.sort(key=lambda x: (_s4_key(x[0], x[1], typ), C.h01("tp", x[0])))
        if view == "message_only":
            # first passing candidate in the (stable) sampler order: same pick as filter-then-sort, lazily
            first = next(((r, s) for r, s in pool_ if _mo_ok_cached(r, s)), None)
            pool_ = [first] if first else []
        if not pool_:
            stats["short_" + typ] += 1
            continue
        rid, stripped = pool_[0]
        rec = FR.rec(rid)
        reg.take_base(rid, "triage", split)
        pos += 1
        bid = f"COMMIT-{split}-{card['card_id']}-{pos:03d}"
        k = bucket(bid)
        opts = subset(typ, k, bid)
        if form == "per_label":
            ask_yes = pl_i < yes_pl
            pl_i += 1
            if ask_yes:
                asked = typ
            else:
                others = [o for o in opts if o != typ]
                part = [o for o in others if o in L.PARTNERS[typ]]
                asked = (part if part and C.h01("plp", bid) < 0.5 else others)[int(C.h01("pla", bid) * len(part if part and C.h01("plp", bid) < 0.5 else others))]
            _emit(card, em, split, rec, stripped, typ, opts, "per_label", view, wyn, bid, "-b", asked=asked)
            stats["units"] += 1
            continue
        masked = view == "message_diff" and C.h01("tmask", bid) < 0.12 or (view == "message_only" and
                                                                           C.h01("tmask", bid) < 0.12)
        swap = view == "message_diff" and not masked and n_tw > 0 and C.h01("tswap", bid) < 0.25
        attack = view == "message_diff" and not masked and not swap and n_tw > 0 and C.h01("tatk", bid) < 0.35
        call = bid + "-u"
        a = _emit(card, em, split, rec, stripped, typ, opts, "masked" if masked else "named", view, wch, bid, "-b",
                  call=call)
        if a and swap:
            partners = [o for o in opts if o in L.PARTNERS[typ]] or [o for o in opts if o != typ]
            other = partners[int(C.h01("swp", bid) * len(partners))]
            t = _emit(card, em, split, rec, stripped, typ, opts, "swapped", view, wch, bid, "-s1", swap_with=other,
                      twin_of=a["id"])
            if t:
                n_tw -= 1
        elif a and attack:
            line = L.ATTACK_LINES[int(C.h01("atk", rid) * len(L.ATTACK_LINES))]
            t = _emit(card, em, split, rec, stripped + "\n" + line, typ, opts, "named", view, wch, bid, "-a1",
                      call=call, twin_of=a["id"], twin_kind="attack")
            if t:
                em.relate(a["id"], t["id"], "inv")
                n_tw -= 1
        stats["units"] += 1
    card['_pos_' + split] = pos
    return stats


def _emit(card, em, split, rec, stripped, typ, opts, form, view, wds, bid, suf, asked=None, swap_with=None,
          twin_of=None, twin_kind=None, call=None):
    defs = card["defs"]
    from fmt1 import labels as flab
    if form == "masked":
        ids = flab.masked_ids("MS10", len(opts), bid)
        shown = ids
        defs_for = {ids[j]: defs[o] for j, o in enumerate(opts)}
        gold = ids[opts.index(typ)]
        omap = {ids[j]: o for j, o in enumerate(opts)}
    else:
        shown = list(opts)
        defs_for = {o: defs[o] for o in opts}
        gold = typ
        omap = {o: o for o in opts}
        if form == "swapped":
            defs_for[typ], defs_for[swap_with] = defs[swap_with], defs[typ]
            gold = swap_with
            omap = {o: o for o in opts}
            omap[typ], omap[swap_with] = swap_with, typ
    persona = card.get("persona")
    if form == "per_label":
        qid, qt, _ = T.questions("triage_label")[int(C.h01("tlq", bid) * 2)]
        q = qt.format(x=asked)
        cir = card_ir(card, view, "per_label", shown, defs_for, persona)
        qtype, options, g = "noul", None, int(asked == typ)
    else:
        qid, q, _ = T.questions("triage_choice")[int(C.h01("tq", bid) * 3)]
        cir = card_ir(card, view, form, shown, defs_for, persona)
        qtype, options, g = "choice", shown, gold

    def extra(b):
        if view == "message_only":
            return "", {}
        sh = K.shorten(rec, b)
        if sh is None:
            return None
        return K.fence(K.render_shown(sh), "diff"), {}
    sp = {"id": bid + suf, "type": "triage", "card": card, "rec": rec, "view": view, "form": form, "qtype": qtype,
          "question": q, "qid": qid, "k": 0, "wording": wds[int(C.h01("wd", bid) * len(wds))], "card_ir": cir,
          "options": options, "gold": g, "msg": stripped, "build_extra": extra if view != "message_only" else None,
          "twin_of": twin_of, "twin_kind": twin_kind or ("swapped_name" if form == "swapped" else None),
          "call_id": call or (bid + suf + "-u"), "variant": f"{card['card_id']}-SW{typ}-{swap_with}" if swap_with
          else None, "card_form": "per_label" if form == "per_label" else "normal", "asked_option": asked,
          "trigger_entities": mo_ok(rec, stripped) if view == "message_only" else None,
          "polarity": ("bad_yes" if asked in L.ADVERSE_TYPES else "good_yes") if form == "per_label" else None,
          "edge": [f"form:{form}", f"k:{len(opts)}"], "defs_style": card["defs_style"],
          "sidecar": {"gold_type": typ, "option_types": omap}}
    return em.emit(sp)


def B_solve(row: dict, rec: dict, option_types: dict) -> object:
    """G3: no header anywhere in the shown message; the tag parsed by the scanner from the record; options mapped to
    types through the card's printed definitions (option_types, from the card table)."""
    st = row["state"]
    pre = st.split("```diff")[0]
    if has_header_anywhere_B(pre):
        raise ValueError("header leak")
    p = parse_B(rec["msg"])
    if p is None:
        raise ValueError("no tag")
    typ = p[0]
    if row["qtype"] == "noul":
        m = re.search(r"(?:tag this change as|tagged) (\w+)", row["instructions"])
        return int(m.group(1) == typ)
    hit = [o for o in row["options"] if option_types[o] == typ]
    if len(hit) != 1:
        raise ValueError("gold option not unique")
    return hit[0]
