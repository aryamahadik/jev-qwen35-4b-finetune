"""F11 S7 solver B and round-trip check (independent of s7.py): a separate loader re-reads each record by record_id
from the pinned formats-2 records file, rebuilds the annotation combination from the raw labels, and matches it
against the label sets parsed from the rendered card (parse.py). Gold is recomputed from that and compared with the
row's gold and with solver A (the generator's codebook table)."""
from __future__ import annotations

import json
import re
from functools import lru_cache

import common  # noqa: F401
import lex
import negcount
import parse as PZ
from common import FMT2, sha256_file, cstr

FILES = {"xed": "xed.jsonl", "mams_acsa": "mams_acsa.jsonl", "mams_atsa": "mams_atsa.jsonl"}


class S7Fail(ValueError):
    pass


@lru_cache(maxsize=4)
def loader(scheme):
    p = FMT2 / "records" / FILES[scheme]
    idx = {}
    for l in open(p):
        r = json.loads(l)
        idx[str(r["record_id"])] = r
    return idx, sha256_file(p)


def annotation(scheme, record_id, target):
    """(combination, text) from the raw record; target = the named aspect / term for MAMS."""
    rec = loader(scheme)[0][str(record_id)]
    a = rec["ann"]
    if scheme == "xed":
        return frozenset(a["emotions"]), rec["text"]
    if scheme == "mams_acsa":
        hit = [i for i, x in enumerate(a["aspects"]) if x[0] == target]
        if len(hit) != 1:
            raise S7Fail("named aspect not unique in the record")
        i = hit[0]
        return (a["aspects"][i][1], frozenset(x[1] for j, x in enumerate(a["aspects"]) if j != i)), rec["text"]
    hit = [i for i, x in enumerate(a["terms"]) if x["term"] == target]
    if len(hit) != 1:
        raise S7Fail("named term not unique in the record")
    n = len(re.findall(r"(?<!\w)" + re.escape(target.lower()) + r"(?!\w)", rec["text"].lower()))
    if n != 1:
        raise S7Fail("named term not exactly once in the text (F11-R3-05)")
    i = hit[0]
    return (a["terms"][i]["polarity"], frozenset(x["polarity"] for j, x in enumerate(a["terms"]) if j != i)), rec["text"]


def walk_s7key(pc, comb):
    """S5 codebook arm: walk the parsed key from couplet 1 over the record's annotation combination."""
    n, seen = 1, set()
    while True:
        if n in seen or n not in pc.couplets or "a" not in pc.couplets[n] or "b" not in pc.couplets[n]:
            raise S7Fail("solver B: key walk broken")
        seen.add(n)
        cp = pc.couplets[n]
        kind, L = cp["a"][0]
        if isinstance(comb, frozenset):
            S = comb
        elif kind == "is":
            S = None
        else:
            S = comb[1]
        if S is None:
            hit = comb[0] in L
        else:
            hit = any(x in S for x in L) if kind == "any" else all(x in S for x in L)
        t = cp["a"][1] if hit else cp["b"]
        if t.isdigit():
            n = int(t)
            continue
        return t


def solve_b(pc, comb):
    """Code whose parsed label sets hold the combination: exactly one, else an error."""
    if pc.s7key:
        return walk_s7key(pc, comb)
    hits = []
    if pc.s7_short:
        for nm, _ in pc.s7_short:
            if PZ.parse_s7_name(pc, nm) == comb:
                hits.append(nm)
    else:
        for cid, d in pc.codes.items():
            if any(s == comb for s in d["sets"]):
                hits.append(cid)
    if len(hits) != 1:
        raise S7Fail(f"solver B: {len(hits)} codes hold the combination")
    return hits[0]


def check_s7_row(card, row):
    spec = row["_spec"]
    scheme = card.scheme
    qtype = row["qtype"]
    from check import strip_question_block
    if qtype == "noul":
        card_text, instr_rest = row["card"], None
        _, question = strip_question_block(row["instructions"])
    else:
        instr_rest, question = strip_question_block(row["instructions"])
        card_text = row["card"]
    if question is None:
        raise S7Fail("question not found")
    try:
        pc = PZ.parse_card(card_text, instr_rest, row.get("options"), qtype=qtype)
    except PZ.ParseError as e:
        raise S7Fail(f"card parse: {e}")
    if pc.shape != "s7":
        raise S7Fail("not parsed as an S7 card")
    # card check: parsed label sets equal the card's (G3 card side)
    if card.form == "key":
        if not pc.s7key:
            raise S7Fail("key card not parsed as a key")
        for cp in pc.couplets.values():
            for t in ((cp.get("a") or (None, "1"))[1], cp.get("b") or "1"):
                if not t.isdigit():
                    pc.codes.setdefault(t, {"parts": [], "rule": None})
        if set(pc.codes) != set(card.ids):
            raise S7Fail("key code set differs")
        if set(pc.couplets) != set(card.couplets):
            raise S7Fail("key couplet numbers differ")
        for n, cp in card.couplets.items():
            p = pc.couplets[n]
            ref = lambda x: str(x[1]) if x[0] == "n" else card.ids[x[1]]  # noqa: E731
            if "a" not in p or "b" not in p or p["a"][0] != tuple(cp["cond"]) or p["a"][1] != ref(cp["a"]) or \
                    p["b"] != ref(cp["b"]):
                raise S7Fail(f"key couplet {n} differs")
        for k, cid in enumerate(card.ids):
            nm = pc.codes[cid].get("name")
            if nm is not None and nm != card.names[k]:
                raise S7Fail("key legend name differs")
    elif card.form == "short":
        got = sorted(map(cstr, (PZ.parse_s7_name(pc, nm) for nm, _ in pc.s7_short)))
        want = sorted(map(cstr, (_key(s[0], scheme) for s in card.sets)))
        if got != want:
            raise S7Fail("short S7 names differ")
    else:
        if set(pc.codes) != set(card.ids):
            raise S7Fail("S7 code set differs")
        for k, cid in enumerate(card.ids):
            if sorted(map(cstr, pc.codes[cid]["sets"])) != sorted(map(cstr, (_key(s, scheme) for s in card.sets[k]))):
                raise S7Fail(f"S7 definition of {cid} differs")
    # question: target and asked code
    T = None
    mams = scheme in ("mams_acsa", "mams_atsa")
    qkeys = [k for k in lex.Q if k.startswith("s7_") and k.endswith("_mams") == mams]
    m = None
    for qk in qkeys:
        pat = re.escape(lex.Q[qk])
        for ph, rx in (("{K}", r"(?P<K>.+?)"), ("{T}", r"(?P<T>.+?)"), ("{target}", r"(?P<tg>\w+)")):
            pat = pat.replace(re.escape(ph), rx)
        mm = re.fullmatch(pat, question)
        if mm:
            m = (qk, mm)
            break
    if m is None:
        raise S7Fail("S7 question frame")
    qk, mm = m
    if mams:
        T = mm.group("T")
        if pc.s7_target is None or mm.group("tg") != pc.s7_target[0]:
            raise S7Fail("question target word")
    # state: quoted text == the record's text (G3), attack notes
    try:
        text, attacks = PZ.parse_s7_state(row["state"])
    except PZ.ParseError as e:
        raise S7Fail(str(e))
    if bool(attacks) != bool(spec.get("attack")):
        raise S7Fail("attack note")
    rid = row["meta"]["text_source"]["record_id"]
    comb, rtext = annotation(scheme, rid, T)
    if text != rtext:
        raise S7Fail("quoted text differs from the pinned record")
    kB = solve_b(pc, comb)
    kA = card.ids[card.table[_key_from_comb(comb)]] if card.form != "short" else card.names[card.table[_key_from_comb(comb)]]
    if kA != kB:
        raise S7Fail(f"G2: solver B {kB} != solver A {kA}")
    if qtype == "noul":
        nc = negcount.count(question)
        nf = lex.N_FRAME[qk.replace("_mams", "")]
        if not (nc.k_syn == nc.k_all == nf):
            raise S7Fail("negcount on the question != n_frame")
        Kt = mm.group("K")
        if card.form != "short" and Kt not in pc.codes:
            ids = [cid for cid, c in pc.codes.items() if c.get("name") == Kt]
            if len(ids) != 1:
                raise S7Fail("asked name")
            Kt = ids[0]
        gold = 1 if ((kB == Kt) != (nf == 1)) else 0
        if gold != row["gold"]:
            raise S7Fail("S7 yes/no gold")
    else:
        opts = row["options"]
        offered = {}
        for o in opts:
            if o == lex.NONE_CODES:
                continue
            if card.form == "short":
                offered[o] = o
            elif o in pc.codes:
                offered[o] = o
            else:
                hits = [cid for cid, c in pc.codes.items() if c.get("option") == o or c.get("name") == o]
                if len(hits) != 1:
                    raise S7Fail(f"option {o!r} maps to no code")
                offered[o] = hits[0]
        inv = {v: k for k, v in offered.items()}
        want = inv.get(kB, lex.NONE_CODES)
        if want == lex.NONE_CODES and lex.NONE_CODES not in opts:
            raise S7Fail("gold not offered and no none option")
        if want != row["gold"]:
            raise S7Fail(f"S7 choice gold {row['gold']!r} != parsed {want!r}")
    return {"ok": True}


def _key(fs, scheme):
    if scheme == "xed":
        return frozenset(fs)
    return (fs[0], frozenset(fs[1]))


def _key_from_comb(comb):
    return comb
