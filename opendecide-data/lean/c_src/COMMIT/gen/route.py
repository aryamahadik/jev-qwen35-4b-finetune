"""ROUTE generator (G0 section 2): which area of the project a change belongs to, from code and message, no paths.
Area schema 2.1 from groups.json (top-level folders or the monorepo shift), gold = area with the most changed lines
(dominance on the full commit AND on the shown hunks: gold >= 70% of in-area lines, in-area >= 80%, in-area > 0),
options = every touched area + thirds fill (nearest to gold, nearest to another touched area, uniform), choice and
per-label (1/3) rows, masked 12%, swapped-name twins (R4-06 folder filter), attack twins (message line), message-only
slice (2.5: name hit, hittable, reader agreement, mention state, main-area check, symmetric dominance).
Solver A: path-prefix trie + dict. Solver B: sqlite GROUP BY over the shown segments mapped back to record hunks."""
from __future__ import annotations

import collections
import fnmatch
import functools
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import core as K  # noqa: E402
import frame as FR  # noqa: E402
import lex2 as L  # noqa: E402
import records as RC  # noqa: E402
import texts as T  # noqa: E402

CC = "CommitChronicle"
SAMPLERS = ["S1", "S2", "S3", "S4"]
# route choice rows (1.8): 3-4 options 30%, 5-9 40%, 10-12 30%
BUCKETS = [(3, 0.12), (4, 0.18), (5, 0.10), (6, 0.10), (7, 0.10), (9, 0.10), (10, 0.15), (12, 0.15)]
DEF_FMT = "files in the folder {folder}: {text}."
DEF_RE = re.compile(r"^files in the folder (\S+): ")


# ---------------------------------------------------------------------------------------------------------------
# area schema and solver A

def area_def(name: str) -> str:
    return L.AREA_DEFS.get(name.lower(), L.AREA_DEF_GENERIC.format(name=name))


def folder_path(card: dict, name: str) -> str:
    """2.1 (G2 fix 1, 6 Oct): the definition prints the area's folder from the project root. After a monorepo shift
    the areas are P's subfolders (P/x) plus other top-level folders (y), so no single 'inside P' sentence is true."""
    return card["areas"][name].strip("/")


class Trie:
    def __init__(self, areas: dict):
        self.root = {}
        for name, pre in areas.items():
            node = self.root
            for seg in pre.strip("/").split("/"):
                node = node.setdefault(seg, {})
            node["\0"] = name

    def area(self, path: str):
        node, hit = self.root, None
        for seg in path.split("/")[:-1]:
            if seg not in node:
                break
            node = node[seg]
            if "\0" in node:
                hit = node["\0"]
        return hit


@functools.lru_cache(maxsize=None)
def trie(group: str) -> Trie:
    return Trie(FR.groups()["groups"][group]["areas"])


def _pat(name: str, pats) -> bool:
    return any(fnmatch.fnmatchcase(name.lower(), p.lower()) for p in pats)


def file_lines(f: dict) -> int:
    return sum(1 for h in f["hunks"] for k, _ in h["lines"] if k in "+-")


def dominance(per_area: dict, outside: int):
    """(gold, share) or None by 2.2's eligibility."""
    tot_in = sum(per_area.values())
    tot = tot_in + outside
    if tot_in <= 0 or tot_in < 0.8 * tot:
        return None
    gold = max(sorted(per_area), key=lambda a: per_area[a])
    if per_area[gold] < 0.7 * tot_in:
        return None
    return gold, per_area[gold] / tot_in


def solve_A(rec: dict, group: str):
    """(gold, share, per_area, touched) or (None, reason)."""
    lx = RC.lex()
    if not K.plain_files(rec):
        return None, "rename_mode_binary"
    tr = trie(group)
    per, outside, junk, tot = collections.Counter(), 0, 0, 0
    for f in rec["files"]:
        n = file_lines(f)
        tot += n
        name = f["path"].split("/")[-1]
        segs = f["path"].split("/")[:-1]
        if _pat(name, lx["generated_patterns"] + lx["lockfile_patterns"]) or \
                any(s.lower() in lx["vendored_folders"] for s in segs):
            junk += n
        a = tr.area(f["path"])
        if a is None:
            outside += n
        elif n:
            per[a] += n
    if tot == 0:
        return None, "no_lines"
    if junk >= 0.1 * tot:
        return None, "vendored_generated_lock"
    d = dominance(per, outside)
    if d is None:
        return None, "not_dominant"
    return (d[0], d[1], dict(per), sorted(a for a in per if per[a] > 0)), None


def strip_headers(rec: dict) -> dict:
    return {**rec, "files": [{**f, "hunks": [{**h, "header": None} for h in f["hunks"]]} for f in rec["files"]]}


def shown_per_area(rec: dict, shown: dict, group: str):
    tr = trie(group)
    per, outside = collections.Counter(), 0
    for sf in shown["files"]:
        n = sum(1 for h in sf["hunks"] for k, _ in h["items"] if k in ("+", "-"))
        a = tr.area(sf["path"])
        if a is None:
            outside += n
        elif n:
            per[a] += n
    return per, outside


# ---------------------------------------------------------------------------------------------------------------
# area token sets (nearest areas; full token sets for the symmetric dominance filter)

@functools.lru_cache(maxsize=None)
def area_tokens(group: str, gsplit: str) -> dict:
    areas = FR.groups()["groups"][group]["areas"]
    tr = trie(group)
    out = {a: set(C.m_tokens(a)) for a in areas}
    for rid in FR.by_group(gsplit, CC).get(group, []):
        for f in FR.rec(rid)["files"]:
            a = tr.area(f["path"])
            if a is not None:
                rel = f["path"][len(areas[a]):]
                out[a].update(C.m_tokens(rel))
    return {a: frozenset(v) for a, v in out.items()}


def nearest(target: str, cands: list[str], toks: dict, key: str) -> list[str]:
    return sorted(cands, key=lambda a: (-len(toks[a] & toks[target]), a, C.h01("near", key, a)))


def options_for(card: dict, touched: list[str], gold: str, k: int, key: str, allowed=None) -> list[str] | None:
    areas = [a for a in card["areas"] if allowed is None or a in allowed]
    if len(touched) > k:
        k = len(touched)
    k = min(k, len(areas))
    if k < max(3, len(touched)) or any(t not in areas for t in touched):
        return None
    toks = card["_toks"]
    opts = list(touched)
    rest = [a for a in areas if a not in opts]
    others = [a for a in touched if a != gold]
    anchor = others[int(C.h01("anc", key) * len(others))] if others else None
    turn = 0
    while len(opts) < k and rest:
        if turn % 3 == 0:
            pick = nearest(gold, rest, toks, key)[0]
        elif turn % 3 == 1:
            pick = nearest(anchor, rest, toks, key)[0] if anchor else rest[int(C.h01("rnd", key, turn) * len(rest))]
        else:
            pick = rest[int(C.h01("uni", key, turn) * len(rest))]
        opts.append(pick)
        rest.remove(pick)
        turn += 1
    return sorted(opts, key=lambda a: C.h01("ropt", key, a))


def bucket(key: str) -> int:
    u = C.h01("rbucket", key)
    acc = 0
    for k, w in BUCKETS:
        acc += w
        if u < acc:
            return k
    return 12


# ---------------------------------------------------------------------------------------------------------------
# message-only slice (2.5)

def mo_check(rec: dict, card: dict, gold: str, touched: list[str], share: float):
    """(ok, reason, offered-hittable areas, trigger entities)."""
    msg = rec["msg"]
    areas = card["areas"]
    name_t = {a: set(C.m_tokens(a)) for a in areas}
    hittable = [a for a in areas if name_t[a]]
    if any(t not in hittable for t in touched):
        return False, "touched_not_hittable", None, None
    hits = K.m_hits(msg, {a: name_t[a] for a in hittable})
    if gold not in hits:
        return False, "no_gold_name_hit", None, None
    if K.reader_conflict(msg, {a: [a] for a in hittable}, hits):
        return False, "reader_conflict", None, None
    ms = K.mention_classes(msg, {a: [p for _, p in hs] for a, hs in hits.items()})
    if ms is None:
        return False, "mention_mixed", None, None
    for a, st in ms.items():
        if st == "not_changed" and a in touched:
            return False, "said_not_changed_but_touched", None, None
        if st == "changed" and a not in touched:
            return False, "said_changed_untouched", None, None
    said = [a for a, st in ms.items() if st == "changed"]
    if gold not in said:
        return False, "gold_not_said_changed", None, None
    if len(said) >= 2:
        words, starts, ends = K.word_index(msg)
        mains, minors = set(), set()
        mc, nc = [c.split() for c in L.MAIN_CUES], [c.split() for c in L.MINOR_CUES]
        for a in said:
            for _, p in hits[a]:
                wi = K.hit_word(p, starts, ends)
                if wi is not None and K.cue_near(words, wi, mc):
                    mains.add(a)
                if wi is not None and K.cue_near(words, wi, nc):
                    minors.add(a)
        if mains & minors:
            return False, "main_and_minor", None, None
        marked = set(mains)
        for a in said:
            if a not in minors and all(b in minors for b in said if b != a):
                marked.add(a)
        if marked != {gold}:
            return False, "main_area_check", None, None
    full = card["_toks"]
    mt = set(C.m_tokens(msg))
    if sum(1 for a in areas if full[a] & mt) >= 2 and share < 0.85:
        return False, "symmetric_dominance", None, None
    trig = [{"entity": a, "token": t, "position": p, "alias": False} for a, hs in hits.items() for t, p in hs]
    return True, None, hittable, trig


# ---------------------------------------------------------------------------------------------------------------
# cards

def card_lint(areas: dict) -> bool:
    names = list(areas)
    if not all(re.fullmatch(r"[A-Za-z0-9._-]+", n) for n in names):
        return False
    low = [n.lower() for n in names]
    if len(set(low)) != len(low):
        return False
    ts = [frozenset(C.m_tokens(n)) for n in names]
    ne = [t for t in ts if t]
    return len(set(ne)) == len(ne)


@functools.lru_cache(maxsize=None)
def group_pool(group: str, gsplit: str) -> tuple:
    """Eligible commits of a group: (rid, gold, share, n_touched)."""
    out, why = [], collections.Counter()
    for rid in FR.by_group(gsplit, CC).get(group, []):
        x = FR.index()[rid]
        if x["n_files"] > 20 or x["bot"]:
            why["files_or_bot"] += 1
            continue
        res, reason = solve_A(FR.rec(rid), group)
        if res is None:
            why[reason] += 1
            continue
        out.append((rid, res[0], round(res[1], 4), len(res[3])))
    return tuple(out), dict(why)


def build_cards(split_kind: str = "train", n: int = 30, min_pool: int = 60) -> list[dict]:
    g = FR.groups()["groups"]
    gsplit = "train" if split_kind == "train" else "heldout"
    cand = sorted((gid for gid, x in g.items() if x["route_eligible"] and x["split"] == gsplit
                   and len(x["areas"]) >= 4 and card_lint(x["areas"])),
                  key=lambda gid: C.h01("route-group", split_kind, gid))
    sized = []
    for gid in cand:
        pool, _ = group_pool(gid, gsplit)
        if len(pool) >= min_pool:
            sized.append((gid, len(pool)))
    sized = sized[:n]
    ids = [f"CMR{i + 1:03d}" if split_kind == "train" else f"CMRD{i + 1:02d}" for i in range(len(sized))]
    rates = FR.antithetic_rates(ids, 20, "route-pl-" + split_kind)
    cards = []
    for i, ((gid, npool), cid) in enumerate(zip(sized, ids)):
        x = g[gid]
        cards.append({"card_id": cid, "type": "route", "sampler": SAMPLERS[i % 4] if split_kind == "train" else "S5",
                      "ds": CC, "group": gid, "pack_id": "pk-" + C.sha256(cid + "|" + gid)[:10],
                      "areas": dict(sorted(x["areas"].items())), "shift": x.get("shift"), "pool_n": npool,
                      "r": rates[cid], "fewshot": False, "inverted": False, "defs_style": "one_line",
                      "persona": FR.draw_persona(cid) if C.h01("persona", cid) < 0.45 else None})
    return cards


def clause_ids(view: str, form: str) -> list[str]:
    if view == "message_only":
        ids = ["SEM-04", "SEM-46", "SEM-42", "SEM-30", "SEM-31m", "SEM-32", "SEM-41"]
    else:
        ids = ["SEM-01", "SEM-02", "SEM-03", "SEM-24", "SEM-30", "SEM-31d", "SEM-32", "SEM-41"]
    if form == "swapped":
        ids.append("SEM-47r")
    if form == "per_label":
        ids.append("SEM-49r")
    return ids


def card_ir(card: dict, view: str, form: str, entries: list[dict]) -> dict:
    blocks = []
    persona = card.get("persona")
    if persona:
        blocks.append({"type": "para", "text": T.PERSONA.format(title=persona[1])})
    if card.get("shift"):
        blocks.append({"type": "para", "text": f"Most of this project's files are inside the folder {card['shift']}. "
                                               "Each folder below is given from the project root."})
    items = [T.SEM[i] for i in clause_ids(view, form)]
    if persona:
        items.append(T.SEM["SEM-45"])
    blocks.append({"type": "section", "heading": "How to read the task", "blocks": [{"type": "items", "items": items}]})
    blocks.append({"type": "defs", "variant": "DV01", "heading": "Areas", "entries": entries})
    return {"title": "Project areas", "blocks": blocks}


# ---------------------------------------------------------------------------------------------------------------
# rows

def _sampler_order(card: dict, pool: list, split: str) -> list:
    smp = card["sampler"]
    cid = card["card_id"]
    if smp == "S2":
        by = collections.defaultdict(list)
        for x in pool:
            by[x[1]].append(x)
        golds = sorted(a for a, v in by.items() if len(v) >= 5) or sorted(by)
        for v in by.values():
            v.sort(key=lambda x: C.h01("s2", cid, split, x[0]))
        out, i = [], 0
        while any(by[a] for a in golds):
            a = golds[i % len(golds)]
            if by[a]:
                out.append(by[a].pop(0))
            i += 1
        return out
    if smp == "S3":
        return sorted(pool, key=lambda x: (0 if x[3] >= 2 and x[2] <= 0.85 else 1, C.h01("s3", cid, split, x[0])))
    if smp == "S4":
        toks = card["_toks"]

        def key(x):
            mt = set(C.m_tokens(FR.rec(x[0])["msg"]))
            hit = any(toks[a] & mt for a in card["areas"] if a != x[1])
            return (0 if hit else 1, C.h01("s4", cid, split, x[0]))
        return sorted(pool, key=key)
    return sorted(pool, key=lambda x: C.h01("s1", cid, split, x[0]))


HUNK_SEP = "@@"


def render_route(shown: dict) -> str:
    """Route view: no file header, path or hunk header; a ROUTE_SEP line opens each file, a bare '@@' line (no line
    numbers, no context text) separates two hunks of one file."""
    out = []
    for sf in shown["files"]:
        out.append(K.ROUTE_SEP)
        for j, h in enumerate(sf["hunks"]):
            if j:
                out.append(HUNK_SEP)
            for k, t in h["items"]:
                out.append(K.CUT.format(n=t) if k == "cut" else k + t)
    return "\n".join(out)


def _diff_extra(rec: dict, card: dict, gold: str, budget: int):
    r2 = strip_headers(rec)
    gold_lines = {(fi, hi, li) for fi, f in enumerate(rec["files"]) if trie(card["group"]).area(f["path"]) == gold
                  for hi, h in enumerate(f["hunks"]) for li, (k, _) in enumerate(h["lines"]) if k in "+-"}
    for dec in (frozenset(), gold_lines):
        sh = K.shorten(r2, budget, dec, view="route")
        if sh is None:
            continue
        per, out = shown_per_area(rec, sh, card["group"])
        d = dominance(per, out)
        if d is not None and d[0] == gold:
            return K.fence(render_route(sh), "diff"), {}
    return None


def build_rows(card: dict, em: FR.Emitter, reg: FR.Registry, split: str, n_rows: int, mo_share: float = 0.3,
               pl_share: float = 1 / 3, twin_share: float = 0.25):
    gsplit = "heldout" if split == "dev" else "train"
    card["_toks"] = area_tokens(card["group"], gsplit)
    pool, _ = group_pool(card["group"], gsplit)
    order = _sampler_order(card, [x for x in pool if reg.can_base(x[0], "route", split)], split)
    stats = collections.Counter()
    n_pl = round(pl_share * n_rows) if split != "dev" else 0
    n_mo = round(mo_share * n_rows)
    yes_pl = round(card["r"] * n_pl)
    wch = FR.card_wordings("route", "choice", card["card_id"])
    wyn = FR.card_wordings("route", "yn", card["card_id"])
    # message-only first (scarce), then per-label, then choice
    mo_rows, pos = 0, card.get('_pos_' + split, 0)
    used = set()
    if n_mo:
        for rid, gold, share, nt in order:
            if mo_rows >= n_mo:
                break
            rec = FR.rec(rid)
            res, _ = solve_A(rec, card["group"])
            ok, why, hittable, trig = mo_check(rec, card, gold, res[3], share)
            stats["mo_" + (why or "ok")] += 1
            if not ok:
                continue
            bid = f"COMMIT-{split}-{card['card_id']}-{pos + 1:03d}"
            opts = options_for(card, res[3], gold, bucket(bid), bid, allowed=set(hittable))
            if opts is None:
                stats["mo_no_options"] += 1
                continue
            reg.take_base(rid, "route", split)
            used.add(rid)
            pos += 1
            masked = C.h01("rmask", bid) < 0.12
            if _emit(card, em, split, rec, gold, opts, "masked" if masked else "named", "message_only", wch, bid,
                     "-b", trig=trig):
                mo_rows += 1
                stats["units"] += 1
        stats["mo_short"] = n_mo - mo_rows
    n_ch = n_rows - n_pl - mo_rows
    n_tw = int(twin_share * n_ch) if split != "dev" else 0
    plan = ["per_label"] * n_pl + ["choice"] * n_ch
    plan.sort(key=lambda f: C.h01("rplan", card["card_id"], split, f, plan.count(f)))
    pl_i = 0
    it = iter([x for x in order if x[0] not in used])
    for form in plan:
        x = next((y for y in it if reg.can_base(y[0], "route", split)), None)
        if x is None:
            stats["short_" + form] += 1
            continue
        rid, gold, share, nt = x
        rec = FR.rec(rid)
        res, _ = solve_A(rec, card["group"])
        bid = f"COMMIT-{split}-{card['card_id']}-{pos + 1:03d}"
        opts = options_for(card, res[3], gold, bucket(bid), bid)
        if opts is None:
            stats["no_options"] += 1
            continue
        reg.take_base(rid, "route", split)
        pos += 1
        if form == "per_label":
            ask_yes = pl_i < yes_pl
            pl_i += 1
            others = [o for o in opts if o != gold]
            asked = gold if ask_yes else nearest(gold, others, card["_toks"], bid)[0] if C.h01("pln", bid) < 0.5 \
                else others[int(C.h01("pla", bid) * len(others))]
            if _emit(card, em, split, rec, gold, opts, "per_label", "message_diff", wyn, bid, "-b", asked=asked):
                stats["units"] += 1
            continue
        masked = C.h01("rmask", bid) < 0.12
        swap_ok = not masked and n_tw > 0 and C.h01("rswap", bid) < 0.45
        other = None
        if swap_ok:
            # R4-06 folder filter: neither swapped folder name's tokens appear in the message or the hunks
            cands = [o for o in opts if o != gold]
            body = rec["msg"] + "\n" + "\n".join(t for f in rec["files"] for h in f["hunks"] for _, t in h["lines"])
            bt = set(C.m_tokens(body))
            cands = [o for o in cands if not (set(C.m_tokens(o)) & bt)]
            if set(C.m_tokens(gold)) & bt or not cands:
                swap_ok = False
            else:
                other = cands[int(C.h01("rsw", bid) * len(cands))]
        attack = not masked and not swap_ok and n_tw > 0 and C.h01("ratk", bid) < 0.25
        call = bid + "-u"
        a = _emit(card, em, split, rec, gold, opts, "masked" if masked else "named", "message_diff", wch, bid, "-b",
                  call=call)
        if a:
            stats["units"] += 1
        if a and swap_ok:
            t = _emit(card, em, split, rec, gold, opts, "swapped", "message_diff", wch, bid, "-s1", swap_with=other,
                      twin_of=a["id"])
            if t:
                em.relate(a["id"], t["id"], "swap")
                n_tw -= 1
        elif a and attack:
            line = L.ATTACK_LINES[int(C.h01("atk", rid) * len(L.ATTACK_LINES))]
            t = _emit(card, em, split, rec, gold, opts, "named", "message_diff", wch, bid, "-a1", call=call,
                      twin_of=a["id"], twin_kind="attack", msg_extra=line)
            if t:
                em.relate(a["id"], t["id"], "inv")
                n_tw -= 1
    card['_pos_' + split] = pos
    return stats


def _emit(card, em, split, rec, gold, opts, form, view, wds, bid, suf, asked=None, swap_with=None, twin_of=None,
          twin_kind=None, call=None, trig=None, msg_extra=None):
    from fmt1 import labels as flab
    folder_of = {o: o for o in opts}
    if form == "masked":
        ids = flab.masked_ids("MS10", len(opts), bid)
        shown = ids
        omap = {ids[j]: o for j, o in enumerate(opts)}
        g = ids[opts.index(gold)]
    else:
        shown = list(opts)
        omap = {o: o for o in opts}
        g = gold
        if form == "swapped":
            omap[gold], omap[swap_with] = swap_with, gold
            g = swap_with
    entries = [{"name": s, "text": DEF_FMT.format(folder=folder_path(card, omap[s]), text=area_def(omap[s]))}
               for s in shown]
    if form == "per_label":
        qid, qt, _ = T.questions("route_label")[int(C.h01("rlq", bid) * 2)]
        q = qt.format(x=asked)
        qtype, options, gg = "noul", None, int(asked == gold)
    else:
        qs = T.questions("route_choice")
        qid, q, _ = qs[int(C.h01("rq", bid) * len(qs))]
        qtype, options, gg = "choice", shown, g
    cir = card_ir(card, view, form, entries)
    msg = rec["msg"] + (("\n" + msg_extra) if msg_extra else "")

    def extra(b):
        return _diff_extra(rec, card, gold, b)
    sp = {"id": bid + suf, "type": "route", "card": card, "rec": rec, "view": view, "form": form, "qtype": qtype,
          "question": q, "qid": qid, "k": 0, "wording": wds[int(C.h01("wd", bid) * len(wds))], "card_ir": cir,
          "options": options, "gold": gg, "msg": msg, "build_extra": extra if view != "message_only" else None,
          "twin_of": twin_of, "twin_kind": twin_kind or ("swapped_name" if form == "swapped" else None),
          "call_id": call or (bid + suf + "-u"),
          "variant": f"{card['card_id']}-SW{gold}-{swap_with}" if swap_with else None,
          "card_form": "per_label" if form == "per_label" else form, "asked_option": asked,
          "trigger_entities": trig or [],
          "polarity": "good_yes" if form == "per_label" else None,
          "edge": [f"form:{form}", f"k:{len(opts)}"], "defs_style": card["defs_style"],
          "sidecar": {"gold_area": gold, "option_areas": omap, "group": card["group"]}}
    return em.emit(sp)


# ---------------------------------------------------------------------------------------------------------------
# solver B (sqlite over shown segments mapped to record hunks) and the round-trip parse (G3)

def B_parse_defs(row: dict, names: list[str] | None = None) -> dict:
    """Option (name or ID) -> folder, read from the rendered card text."""
    txt = row["card"] if isinstance(row.get("card"), str) else json.dumps(row.get("card"), ensure_ascii=False)
    txt = K.unescape_state(txt)
    if names is None:
        names = [m.group(1) for m in re.finditer(r"([A-Za-z0-9_.\-]+(?: [A-Z]\d)?)\W{0,8}files in the folder ", txt)]
    out = {}
    for o in names:
        m = re.search(r"(?<![A-Za-z0-9_.\-])" + re.escape(o) + r"\W{0,8}files in the folder (\S+): ", txt)
        if m:
            out[o] = m.group(1)
    return out


def _segments(body: str):
    segs, cur = [], None
    for ln in body.split("\n"):
        if ln == K.ROUTE_SEP:
            cur = [[]]
            segs.append(cur)
            continue
        if cur is None:
            continue
        if K.CUT_RE.match(ln) or ln == HUNK_SEP:
            cur.append([])
            continue
        k = ln[:1] if ln[:1] in "+-" else " "
        cur[-1].append((k, ln[1:]))
    return [[p for p in s if p] for s in segs]


def _in_order_sub(part: list, lines: list) -> bool:
    n = len(part)
    for i in range(len(lines) - n + 1):
        if lines[i:i + n] == part:
            return True
    return False


def B_solve(row: dict, rec: dict, areas: dict, option_areas: dict | None = None):
    """Gold option (choice) or 0/1 (per-label). Raises on a leak or an unmapped shown hunk."""
    st = row["state"]
    if row["meta"]["input_view"] == "message_only":
        if "```diff" in st or K.ROUTE_SEP in st:
            raise ValueError("hunk text on a message-only row")
        segs = [[[tuple(x) for x in h["lines"]] for h in f["hunks"]] for f in rec["files"]]
    else:
        m = re.search(r"```diff\n(.*?)\n```", st, re.S)
        body = m.group(1)
        for ln in body.split("\n"):
            if ln.startswith(("--- ", "+++ ", "diff --git", "rename ", "Binary files", "@@ ")):
                raise ValueError("header leak")
        segs = _segments(body)
    db = sqlite3.connect(":memory:")
    db.execute("create table areas(name text, prefix text)")
    db.executemany("insert into areas values (?, ?)", list(areas.items()))
    db.execute("create table seg(path text, n int)")
    files = list(rec["files"])
    cand = [[i for i, f in enumerate(files) if all(
        any(_in_order_sub(p, [tuple(x) for x in h["lines"]]) for h in f["hunks"]) for p in parts)] for parts in segs]
    if any(not c for c in cand):
        raise ValueError("shown hunk not a record substring")
    nseg = [sum(1 for p in parts for k, _ in p if k in "+-") for parts in segs]
    # every one-to-one assignment of shown segments to record files (order-free); the (path, n) multiset must agree
    sols, cur, used = set(), [], set()

    def _walk(j):
        if len(sols) > 64:
            return
        if j == len(segs):
            sols.add(tuple(sorted((files[fi]["path"], n) for fi, n in zip(cur, nseg))))
            return
        for fi in cand[j]:
            if fi not in used:
                used.add(fi); cur.append(fi)
                _walk(j + 1)
                used.discard(fi); cur.pop()
    _walk(0)
    if not sols:
        raise ValueError("shown hunk not a record substring")
    if len(sols) > 64:
        raise ValueError("shown hunks map to files ambiguously")
    q = """select a.name, sum(s.n) from seg s join areas a on s.path glob (a.prefix || '*')
           where length(a.prefix) = (select max(length(b.prefix)) from areas b where s.path glob (b.prefix || '*'))
           group by a.name order by sum(s.n) desc, a.name"""
    golds = set()
    for sol in sorted(sols):
        db.execute("delete from seg")
        db.executemany("insert into seg values (?, ?)", list(sol))
        per = {a: n for a, n in db.execute(q).fetchall()}
        tot = db.execute("select coalesce(sum(n), 0) from seg").fetchone()[0]
        d = dominance({a: n for a, n in per.items() if n > 0}, tot - sum(per.values()))
        golds.add(None if d is None else d[0])
    if len(golds) > 1:
        raise ValueError("shown hunks map to files ambiguously")
    gold = golds.pop()
    if gold is None:
        raise ValueError("shown hunks not dominant")
    # printed folders are paths from the project root (folder_path); map them back to area names by prefix
    by_folder = {p.strip("/"): a for a, p in areas.items()}
    if row["qtype"] == "noul":
        mm = re.search(r"mainly to area (\S+?)\?", row["instructions"]) or \
            re.search(r"\bIs (\S+) the area this change mainly belongs to\?", row["instructions"])
        asked = mm.group(1)
        defs = option_areas or {o: by_folder.get(f, f) for o, f in B_parse_defs(row, [asked]).items()}
        return int(defs.get(asked, asked) == gold)
    defs = option_areas or {o: by_folder.get(f, f) for o, f in B_parse_defs(row, row["options"]).items()}
    hit = [o for o in row["options"] if defs.get(o) == gold]
    if len(hit) != 1:
        raise ValueError("gold option not unique")
    return hit[0]
