"""MATCH generator (G0 section 6): does the message describe this diff? Yes/no in two polarity frames (describes /
other-change) with negated forms, plus inverted cards (one diff, 3-4 messages). Pairing and filters 6.1 (code names,
specific-message filter, positives touched by the shown diff, negatives with a deciding code name, same-change
exclusions). Twins: message-swap (contrast), {aff, neg, dneg} sets, attack (message line).
Solver A: provenance + the 6.1 filters. Solver B: a character scanner over the shown text only (6.4)."""
from __future__ import annotations

import collections
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import core as K  # noqa: E402
import frame as FR  # noqa: E402
import lex2 as L  # noqa: E402
import texts as T  # noqa: E402
import yn  # noqa: E402

sys.path.insert(0, str(C.CSRC / "common"))
import negcount  # noqa: E402

CC, PF = "CommitChronicle", "CommitPackFT"
MARKERS = re.compile(r"(?i)cherry[- ]picked|cherry-pick|re-?apply|fixup!|squash!|\brevert")
CLAUSES = ["SEM-01", "SEM-02", "SEM-25", "SEM-30", "SEM-31d", "SEM-32", "SEM-41", "SEM-38"]


# ---------------------------------------------------------------------------------------------------------------
# 6.1 filters (solver A side)

def specific(msg: str):
    """Code names of a message that passes the specific-message filter, else None."""
    ws = K.msg_words(msg)
    names = []
    for w, _ in ws:
        if K.code_shaped(w):
            if "[" in w and re.search(r"\[(?:hash|person|email|date|link|secret|ip)\]", w):
                return None
            if not C.m_tokens(w.strip("`")):
                return None
            names.append(w.strip("`"))
    for m in re.finditer(r"`", msg):
        i = m.start()
        # every backtick must be the first or last character of one whitespace word
        left = i == 0 or msg[i - 1].isspace() or msg[i - 1] in K.OUTER
        right = i + 1 == len(msg) or msg[i + 1].isspace() or msg[i + 1] in K.OUTER + "."
        if not (left or right):
            return None
    for w, _ in ws:
        if w.count("`") not in (0, 2) or (w.count("`") == 2 and not (w[0] == "`" and w[-1] == "`")):
            return None
    if not names or len(C.m_tokens(msg)) < 3:
        return None
    return list(dict.fromkeys(names))


def full_lines(rec: dict) -> list[str]:
    out = []
    for f in rec["files"]:
        out.extend(K.header_lines(f))
        for h in f["hunks"]:
            if h["header"]:
                out.append(h["header"])
            out.extend(k + t for k, t in h["lines"])
    return out


def changed_and_paths(rec: dict) -> list[str]:
    out = [p for f in rec["files"] for p in {f["old"], f["new"], f["path"]} if p]
    out += [t for f in rec["files"] for h in f["hunks"] for k, t in h["lines"] if k in "+-"]
    return out


@functools.lru_cache(maxsize=20000)
def _diff_tokens(rid: str) -> frozenset:
    return frozenset(t for ln in full_lines(FR.rec(rid)) for t in C.m_tokens(ln))


@functools.lru_cache(maxsize=20000)
def _full_lower(rid: str) -> str:
    return "\n".join(full_lines(FR.rec(rid))).lower()


def deciding(name: str, diff_rid: str, own_rid: str) -> bool:
    if name.lower() in _full_lower(diff_rid):
        return False
    toks = C.m_tokens(name)
    dt = _diff_tokens(diff_rid)
    for t in toks:
        if t in dt:
            return False
        for u in dt:
            if (len(t) >= 5 and len(u) >= 5 and t[:5] == u[:5]) or t in u or u in t:
                return False
    return K.touched(name, changed_and_paths(FR.rec(own_rid)))


def _shingles(rec: dict) -> set:
    toks = [w for f in rec["files"] for h in f["hunks"] for k, t in h["lines"] if k in "+-" for w in t.split()]
    return {tuple(toks[i:i + 5]) for i in range(max(0, len(toks) - 4))}


def same_change(x: dict, y: dict) -> bool:
    if MARKERS.search(x["msg"]) or MARKERS.search(y["msg"]):
        return True
    sx, sy = _shingles(x), _shingles(y)
    if sx and sy and len(sx & sy) / len(sx | sy) >= 0.8:
        return True
    subj = lambda r: r["msg"].split("\n", 1)[0].strip().lower()
    if subj(x) and subj(x) in y["msg"].lower() or subj(y) and subj(y) in x["msg"].lower():
        return True
    return False


def negative_ok(diff_rec: dict, msg_rec: dict) -> list[str] | None:
    """Deciding code names of msg_rec's message against diff_rec, or None if the pair is not a kept negative."""
    if diff_rec["rid"] == msg_rec["rid"] or diff_rec["ds"] != msg_rec["ds"]:
        return None
    names = specific(msg_rec["msg"])
    if not names:
        return None
    px = {p for f in diff_rec["files"] for p in (f["old"], f["new"]) if p}
    py = {p for f in msg_rec["files"] for p in (f["old"], f["new"]) if p}
    if not px & py:
        return None
    if diff_rec["msg"].split("\n", 1)[0] == msg_rec["msg"].split("\n", 1)[0]:
        return None
    tx, ty = set(C.m_tokens(diff_rec["msg"])), set(C.m_tokens(msg_rec["msg"]))
    if tx | ty and len(tx & ty) / len(tx | ty) >= 0.5:
        return None
    if same_change(diff_rec, msg_rec):
        return None
    dec = [n for n in names if deciding(n, diff_rec["rid"], msg_rec["rid"])]
    return dec or None


def decisive_for(rec: dict, names: list[str]) -> set:
    out = set()
    for fi, f in enumerate(rec["files"]):
        for hi, h in enumerate(f["hunks"]):
            for li, (k, t) in enumerate(h["lines"]):
                if k in "+-" and any(K.touched(n, [t]) for n in names):
                    out.add((fi, hi, li))
    return out


def positive_ok(rec: dict):
    names = specific(rec["msg"])
    if not names or MARKERS.search(rec["msg"]):
        return None
    if not all(K.touched(n, changed_and_paths(rec)) for n in names):
        return None
    return names


# ---------------------------------------------------------------------------------------------------------------
# solver B: shown text only

_CHROME_OK = {}


def style_ok(st: dict) -> bool:
    """Match rows use only styles whose chrome adds no code-shaped word (so every code-shaped word in the state's
    text part is a message word)."""
    if st["id"] not in _CHROME_OK:
        from fmt1.render import render_state, FormatError
        import render as RD
        try:
            s = render_state(RD.message_doc("alpha beta gamma\ndelta epsilon"), st)
            _CHROME_OK[st["id"]] = not any(B_code_shaped(w) for w in B_words(s)) and "&" not in s and "<" not in s
        except FormatError:
            _CHROME_OK[st["id"]] = False
    return _CHROME_OK[st["id"]]


def B_words(text: str) -> list[str]:
    out, cur = [], []
    for ch in text + " ":
        if ch.isspace():
            if cur:
                w = "".join(cur)
                while w and w[0] in K.OUTER:
                    w = w[1:]
                while w and w[-1] in K.OUTER:
                    w = w[:-1]
                if w.endswith("."):
                    w = w[:-1]
                while w and w[-1] in K.OUTER:
                    w = w[:-1]
                if w:
                    out.append(w)
                cur = []
        else:
            cur.append(ch)
    return out


def B_code_shaped(w: str) -> bool:
    if len(w) >= 2 and w[0] == "`" and w[-1] == "`":
        return True
    for i, ch in enumerate(w):
        if ch in "/_":
            return True
        if ch.isupper() and i > 0 and w[i - 1].islower() and w[i - 1].isascii() and ch.isascii():
            return True
        if ch == "." and 0 < i < len(w) - 1 and w[i - 1].isalnum() and w[i + 1].isalnum():
            return True
    return False


def B_touched(name: str, lines: list[str]) -> bool:
    n = name.lower()
    for ln in lines:
        low = ln.lower()
        i = low.find(n)
        while i >= 0:
            a = low[i - 1] if i > 0 else " "
            b = low[i + len(n)] if i + len(n) < len(low) else " "
            if not (a.isalnum() or a == "_") and not (b.isalnum() or b == "_"):
                return True
            i = low.find(n, i + 1)
    return False


def B_describes(msg_text: str, diff_body: str) -> bool:
    d = K.parse_diff_text(diff_body)
    lines = [f["old"] for f in d["files"] if f["old"]] + [f["new"] for f in d["files"] if f["new"]]
    lines += [t for f in d["files"] for k, t in f["lines"] if k in "+-"]
    names = [w.strip("`") for w in B_words(msg_text) if B_code_shaped(w)]
    return all(B_touched(n, lines) for n in names)


QF = re.compile(r"([^\n?]*\b(?:describe|describes|written for)\b[^\n?]*\?)")


def B_solve(row: dict) -> int:
    st = row["state"]
    m = re.search(r"```diff\n(.*?)\n```", st, re.S)
    msg_text = st[:m.start()]
    desc = B_describes(msg_text, m.group(1))
    qs = QF.findall(row["instructions"])
    q = qs[-1]
    if re.search(r"(?i)\b(is it not true|isn't it|is it not the case|is it false that)\b", q):
        raise ValueError("negated frame")
    other = "different change" in q or "some other change" in q
    v = (not desc) if other else desc
    return int(v) ^ (negcount.k_syn(q) % 2)


def B_solve_inverted(row: dict) -> str:
    st = row["state"]
    m = re.search(r"```diff\n(.*?)\n```", st, re.S)
    rest = st[m.end():]
    low = rest.lower()
    pos = sorted((low.find(ref.lower()), ref) for ref in row["options"])
    if any(p < 0 for p, _ in pos):
        raise ValueError("case ref missing")
    good = []
    for j, (p, ref) in enumerate(pos):
        end = pos[j + 1][0] if j + 1 < len(pos) else len(rest)
        seg = rest[p + len(ref):end]
        if B_describes(seg, m.group(1)):
            good.append(ref)
    if len(good) != 1:
        raise ValueError(f"{len(good)} cases describe the diff")
    return good[0]


# ---------------------------------------------------------------------------------------------------------------
# cards and rows (6.2, 6.3; 1.6 units via yn.plan with pos_frame "describes")

SAMPLERS = ["S1", "S2", "S3", "S4"]
ATTACKS = [a for a in L.ATTACK_LINES if not any(B_code_shaped(w) for w in B_words(a)) and "`" not in a]


def clause_ids(inverted: bool) -> list[str]:
    ids = [c for c in CLAUSES if c != "SEM-38"]
    return ids + (["SEM-26"] if inverted else ["SEM-38"])


def card_ir(inverted: bool = False, persona=None) -> dict:
    blocks = []
    if persona:
        blocks.append({"type": "para", "text": T.PERSONA.format(title=persona[1])})
    if inverted:
        blocks.append({"type": "para", "text": T.INV_FRAME_MATCH})
    items = [T.SEM[i] for i in clause_ids(inverted)]
    if persona:
        items.append(T.SEM["SEM-45"])
    blocks.append({"type": "section", "heading": "How to read the task", "blocks": [{"type": "items", "items": items}]})
    return {"title": "Message check", "blocks": blocks}


def build_cards(split_kind: str = "train", n_yn: int = 24, n_inv: int = 16) -> list[dict]:
    cards = []
    if split_kind == "train":
        ids = [f"CMM{i + 1:03d}" for i in range(n_yn)]
        inv = [f"CMMI{i + 1:02d}" for i in range(n_inv)]
        smp = lambda i: SAMPLERS[i % 4]
    else:
        ids = [f"CMMD{i + 1:02d}" for i in range(n_yn)]
        inv = [f"CMMDI{i + 1:02d}" for i in range(n_inv)]
        smp = lambda i: "S5"
    rates = FR.antithetic_rates(ids, 55 if split_kind == "train" else 20, "match-" + split_kind)
    for i, cid in enumerate(ids):
        cards.append({"card_id": cid, "type": "match", "sampler": smp(i), "ds": CC, "r": rates[cid],
                      "inverted": False, "defs_style": "one_line", "fewshot": False,
                      "persona": FR.draw_persona(cid) if C.h01("persona", cid) < 0.4 else None})
    for j, cid in enumerate(inv):
        cards.append({"card_id": cid, "type": "match", "sampler": smp(j), "ds": CC, "r": None, "inverted": True,
                      "defs_style": "one_line", "fewshot": False,
                      "persona": FR.draw_persona(cid) if C.h01("persona", cid) < 0.4 else None})
    return cards


@functools.lru_cache(maxsize=None)
def _spec_names(rid: str):
    return specific(FR.rec(rid)["msg"])


@functools.lru_cache(maxsize=None)
def _pos_names(rid: str):
    r = FR.rec(rid)
    if not K.plain_files(r):
        return None
    return positive_ok(r)


def _paths(rec: dict) -> set:
    return {p for f in rec["files"] for p in (f["old"], f["new"]) if p}


@functools.lru_cache(maxsize=None)
def _group_paths(group: str, gsplit: str, ds: str):
    """path -> rids of a group's eligible commits (<= 20 files, no bot, plain files)."""
    out = collections.defaultdict(list)
    for rid in FR.by_group(gsplit, ds).get(group, []):
        x = FR.index()[rid]
        if x["n_files"] > 20 or x["bot"]:
            continue
        r = FR.rec(rid)
        if not K.plain_files(r):
            continue
        for p in _paths(r):
            out[p].append(rid)
    return out


def _partners(rid: str, gsplit: str, ds: str) -> list[str]:
    x = FR.index()[rid]
    gp = _group_paths(x["group"], gsplit, ds)
    r = FR.rec(rid)
    s = set()
    for p in _paths(r):
        s.update(gp.get(p, []))
    s.discard(rid)
    return sorted(m for m in s if _spec_names(m))


def _neg_key(card, d: dict, m: str, dec: list[str]):
    smp = card["sampler"]
    mr = FR.rec(m)
    if smp == "S3":
        a, b = _paths(d), _paths(mr)
        jac = len(a & b) / max(1, len(a | b))
        return (0 if jac >= 0.8 else 1, -jac, C.h01("nk", card["card_id"], d["rid"], m))
    if smp == "S4":
        names = _spec_names(m)
        lines = changed_and_paths(d)
        others_touched = all(K.touched(n, lines) for n in names if n not in dec)
        return (0 if (len(dec) == 1 and len(names) >= 2 and others_touched) else 1,
                C.h01("nk", card["card_id"], d["rid"], m))
    return (C.h01("nk", card["card_id"], d["rid"], m),)


_NO_NEG = set()


def _neg_for(card, d_rid: str, reg, split: str, gsplit: str, exclude=()):
    d = FR.rec(d_rid)
    best = None
    for m in _partners(d_rid, gsplit, card["ds"]):
        if m in exclude or not reg.can_extra(m, "match", split):
            continue
        dec = negative_ok(d, FR.rec(m))
        if not dec:
            continue
        k = _neg_key(card, d, m, dec)
        if best is None or k < best[0]:
            best = (k, m, dec)
    return None if best is None else (best[1], best[2])


def _diff_extra(rec: dict, keep_names: list[str] | None, budget: int, check_names: list[str] | None = None):
    dec = decisive_for(rec, keep_names) if keep_names else set()
    sh = K.shorten(rec, budget, dec)
    if sh is None:
        return None
    body = K.render_shown(sh)
    if check_names is not None:
        d = K.parse_diff_text(body)
        lines = [f["old"] for f in d["files"] if f["old"]] + [f["new"] for f in d["files"] if f["new"]]
        lines += [t for f in d["files"] for k, t in f["lines"] if k in "+-"]
        if not all(B_touched(n, lines) for n in check_names):
            return None
    return K.fence(body, "diff"), {}


def _cands(card: dict, gsplit: str):
    pk, gs = FR.pack(card["card_id"], gsplit, card["ds"], frac=0.4 if gsplit == "train" else 1.0)
    card["pack_id"] = pk
    gset = set(gs)
    ix = FR.index()
    rids = sorted((rid for rid, x in ix.items() if x["group"] in gset and x["split"] == gsplit and x["ds"] == card["ds"]
                   and x["n_files"] <= 20 and not x["bot"]), key=lambda r: C.h01("mcand", card["card_id"], r))
    return rids


def _qpick(frame: str, k: int, card_id: str, key: str):
    qs = T.questions("match_desc" if frame == "describes" else "match_other", k)
    return qs[int(C.h01("q", card_id, key, k) * len(qs))]


def _wording(wds, card_id, rid, salt=""):
    return wds[int(C.h01("wd", card_id, rid, salt) * len(wds))]


def build_rows(card: dict, em: FR.Emitter, reg: FR.Registry, split: str, n_rows: int, twin_rate: float = 0.30):
    gsplit = "heldout" if split == "dev" else "train"
    rids = _cands(card, gsplit)
    if card["inverted"]:
        return _build_inverted(card, em, reg, split, n_rows, rids, gsplit)
    kinds = []
    budget_tw = int(twin_rate * n_rows) if split != "dev" else 0
    used = 0
    for kd in ["contrast", "negset", "contrast", "attack", "contrast", "contrast", "negset", "contrast"] * 3:
        add = yn.ROWS[kd] - 1
        if used + add > budget_tw:
            continue
        kinds.append(kd)
        used += add
    n_single = max(0, n_rows - sum(yn.ROWS[k] for k in kinds))
    kinds += ["single"] * n_single
    units = yn.plan(card["card_id"], split, 0, kinds, card["r"], "other", "describes")
    wds = FR.card_wordings("match", "yn", card["card_id"])
    stats = collections.Counter()
    pos_i = card.get('_pos_' + split, 0)
    ptr_pos, ptr_neg = 0, 0
    singles_first = card["sampler"] == "S4"
    for u in units:
        truth = yn.truth_for(u["s"], u["frame"], u["k"], "describes")
        need_pos = truth or u["kind"] == "contrast"
        need_neg = (not truth) or u["kind"] == "contrast"
        got = None
        order = rids
        if singles_first and need_pos and not need_neg:
            order = sorted(rids, key=lambda r: (len(_pos_names(r) or ()) != 1, C.h01("s4p", card["card_id"], r)))
        for rid in order:
            if not reg.can_base(rid, "match", split):
                continue
            if need_pos and not _pos_names(rid):
                continue
            neg = None
            if need_neg:
                if (card["card_id"], rid) in _NO_NEG:
                    continue
                neg = _neg_for(card, rid, reg, split, gsplit)
                if neg is None:
                    _NO_NEG.add((card["card_id"], rid))   # the registry only tightens: no partner now, none later
                    continue
            got = (rid, neg)
            break
        if got is None:
            stats["unit_unfilled_" + u["kind"] + ("_pos" if truth else "_neg")] += 1
            continue
        rid, neg = got
        reg.take_base(rid, "match", split)
        if neg:
            reg.take_extra(neg[0], "match", split)
        pos_i += 1
        _emit_unit(card, em, split, u, FR.rec(rid), neg, truth, wds, pos_i)
        stats["units"] += 1
    card['_pos_' + split] = pos_i
    return stats


def _emit_unit(card, em, split, u, d: dict, neg, truth: bool, wds, pos):
    base_id = f"COMMIT-{split}-{card['card_id']}-{pos:03d}"
    cir = card_ir(False, card.get("persona"))
    own = _pos_names(d["rid"])
    mrec = FR.rec(neg[0]) if neg else None
    keep = own if own else None

    def mk(suf, k, show_pos: bool, msg_extra="", twin_of=None, twin_kind=None, call=None, edge=()):
        qid, qtext, kk = _qpick(u["frame"], k, card["card_id"], d["rid"] + suf)
        msg_rec = d if show_pos else mrec
        msg = msg_rec["msg"] + (("\n" + msg_extra) if msg_extra else "")
        gold = yn.shown(show_pos, u["frame"], kk, "describes")
        names = _pos_names(d["rid"]) if show_pos else None
        sp = {"id": base_id + suf, "type": "match", "card": card, "rec": d, "view": "message_diff",
              "form": "yesno", "qtype": "noul", "question": qtext, "qid": qid, "k": kk,
              "wording": _wording(wds, card["card_id"], d["rid"]), "card_ir": cir, "gold": gold, "msg": msg,
              "build_extra": (lambda b: _diff_extra(d, keep, b, names)), "style_ok": style_ok,
              "depth": 1, "twin_of": twin_of, "twin_kind": twin_kind,
              "call_id": call or (base_id + suf + "-u"),
              "polarity": "bad_yes" if u["frame"] == "other" else "good_yes",
              "variant": None if show_pos else f"neg-{mrec['rid']}",
              "extra_recs": [] if show_pos else [dict(mrec, _use="negative_message")],
              "edge": [f"frame:{u['frame']}", f"k:{kk}", "pos" if show_pos else "neg", *edge],
              "sidecar": {"frame": u["frame"], "describes": show_pos,
                          "msg_record": msg_rec["rid"], "code_names": own if show_pos else _spec_names(mrec["rid"]),
                          "deciding": None if show_pos else neg[1]}}
        return em.emit(sp)

    kind = u["kind"]
    if kind == "single":
        mk("-b", u["k"], truth)
    elif kind == "negset":
        call = base_id + "-u"
        a = mk("-b", 0, truth, call=call)
        if a:
            n1 = mk("-n1", 1, truth, twin_of=a["id"], twin_kind="negated", call=call)
            n2 = mk("-n2", 2, truth, twin_of=a["id"], twin_kind="double_negated", call=call)
            if n1:
                em.relate(a["id"], n1["id"], "complement")
            if n2:
                em.relate(a["id"], n2["id"], "equiv")
    elif kind == "attack":
        call = base_id + "-u"
        a = mk("-b", 0, truth, call=call)
        if a:
            line = ATTACKS[int(C.h01("atk", d["rid"]) * len(ATTACKS))]
            t = mk("-a1", 0, truth, msg_extra=line, twin_of=a["id"], twin_kind="attack", call=call, edge=("attack",))
            if t:
                em.relate(a["id"], t["id"], "inv")
    elif kind == "contrast":
        a = mk("-b", 0, truth)
        if a:
            t = mk("-s1", 0, not truth, twin_of=a["id"], twin_kind="message_swap")
            if t:
                em.relate(a["id"], t["id"], "flip")


def _build_inverted(card, em, reg, split, n_rows, rids, gsplit):
    stats = collections.Counter()
    wds = FR.card_wordings("match", "choice", card["card_id"])
    cir = card_ir(True, card.get("persona"))
    fcard = __import__("fmt1.card", fromlist=["case_refs"])
    i = 0
    for rid in rids:
        if i >= n_rows:
            break
        if not reg.can_base(rid, "match", split) or not reg.can_extra(rid, "match", split) or not _pos_names(rid):
            continue
        k = 3 + (C.h01("invk", card["card_id"], split, i) < 0.5)
        d = FR.rec(rid)
        ds_, used = [], set()
        for _ in range(k - 1):
            got = _neg_for(card, rid, reg, split, gsplit, exclude=used)
            if got is None:
                break
            # distractors must also differ from each other (6.1 first lines / Jaccard against the diff only; keep
            # pairwise distinct messages so exactly one case describes the diff)
            if any(FR.rec(got[0])["msg"] == FR.rec(x[0])["msg"] for x in ds_):
                used.add(got[0])
                continue
            ds_.append(got)
            used.add(got[0])
        if len(ds_) < 2:
            stats["inv_no_distractors"] += 1
            continue
        if len(ds_) < k - 1:
            k = len(ds_) + 1
        reg.take_base(rid, "match", split)
        for m, _ in ds_:
            reg.take_extra(m, "match", split)
        i += 1
        recs = [d] + [FR.rec(m) for m, _ in ds_]
        refs = fcard.case_refs("IVN01", k, f"{card['card_id']}-{split}-{i}")
        order = sorted(range(k), key=lambda j: C.h01("invpos", card["card_id"], split, i, j))
        cases = [(refs[j], recs[order[j]]) for j in range(k)]
        gold_ref = refs[order.index(0)]
        doc = {"title": None, "meta": [], "blocks": [
            {"type": "section", "heading": ref, "blocks": [{"type": "para", "text": ln}
                                                          for ln in r_["msg"].split("\n") if ln.strip()]}
            for ref, r_ in cases]}
        own = _pos_names(rid)

        def extra(b, d=d, own=own):
            got = _diff_extra(d, own, b, own)
            if got is None:
                return None
            return "", {"_state_first": got[0]}
        qid, qtext, _ = T.questions("match_inv")[int(C.h01("qi", card["card_id"], i) * 2)]
        sp = {"id": f"COMMIT-{split}-{card['card_id']}-{i:03d}-b", "type": "match", "card": card, "rec": d,
              "view": "message_diff", "form": "inverted", "qtype": "choice", "question": qtext, "qid": qid, "k": 0,
              "wording": _wording(wds, card["card_id"], rid), "card_ir": cir, "options": refs, "gold": gold_ref,
              "msg": d["msg"], "doc": doc, "build_extra": extra, "style_ok": style_ok,
              "budgets": [1200, 900, 700, 500, 350], "depth": 1,
              "call_id": f"COMMIT-{split}-{card['card_id']}-{i:03d}-u", "card_form": "inverted",
              "extra_recs": [dict(FR.rec(m), _use="inverted_case") for m, _ in ds_],
              "edge": [f"k_cases:{k}"],
              "sidecar": {"case_records": {ref: r_["rid"] for ref, r_ in cases},
                          "deciding": {m: dec for m, dec in ds_}}}
        if em.emit(sp):
            stats["units"] += 1
        else:
            stats["inv_emit_drop"] += 1
    if i < n_rows:
        stats["inv_short"] += n_rows - i
    return stats
