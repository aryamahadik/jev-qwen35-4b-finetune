"""G4 relations that need a re-render (M4 option shuffle + container change, M8 attack note): the parsed structure of
an emitted row is rendered again by the generator's renderer in another style of the same card, parsed again, and
compared (structure hash, option set, gold option text). Test harness only (the parser never imports this)."""
from __future__ import annotations

import copy
import random

import cards as CARDS
import cardfit
import parse_f3 as P
import registry as R
import render_f3 as RF
import canon
from fmt1 import pool as fmt1_pool

_CACHE = {}


def cards_for(part):
    if part in _CACHE:
        return _CACHE[part]
    from build import tokenizer
    cs = CARDS.make_dev_cards() if part == "dev" else CARDS.make_training_cards()
    cardfit.fit(cs, tokenizer())
    _CACHE[part] = {c["card_id"]: c for c in cs}
    return _CACHE[part]


def _prep(row, Pp, cards):
    c = copy.deepcopy(cards[row["meta"]["card_id"]])
    S = copy.deepcopy(Pp["S"])
    if S["sampler"] == "S5":
        return None, None
    dt = dict(Pp["state"].get("doctype") or {})
    sl = P.parse_question(row["instructions"])[1]["slots"]
    if sl.get("DOC") and sl.get("doctype"):
        dt.setdefault(sl["DOC"], sl["doctype"])
    for d, _ in S["register"].get("docs", []):
        if not dt.get(d):
            dt[d] = sl.get("doctype") or "document"
    for e in S["entries"]:
        if e["t"] == "OPEN" and not dt.get(e["doc"]):
            dt[e["doc"]] = "document"
    c["_doctype"] = dt
    if S["sampler"] == "S4":
        people = c["people"] or ["Registry desk", "Field office"]
        S["notices"] = [{"ref": r, "date": P.parse_date(d, Pp["info"]["date_fmt"]), "from": people[0],
                         "to": people[1 % len(people)]} for r, d in sorted(Pp["state"]["notices"].items())]
    S["list_order"] = None
    if c["listing"] in ("sorted", "shuffled", "eff_sorted"):
        RF.set_listing(c, S, random.Random(row["id"]))
    return c, S


def render_variant(name, row, Pp, cards, rng):
    c, S = _prep(row, Pp, cards)
    if c is None:
        return "skip:s5"
    Q = Pp["Q"]
    opts = list(row["options"]) if row["qtype"] == "choice" else None
    if name == "M4":
        if opts:
            rng.shuffle(opts)
        cont = P._STYLES[row["meta"]["format_style"]]["container"]
        others = [s for s in c["styles"] if fmt1_pool.style(s)["container"] != cont]
        if not others:
            return "skip:one_container"
        style_ids = [rng.choice(others)]
        notes = {}
    else:
        if not c.get("notes_on") or c["encoding"] == "git":
            return "skip:no_notes"
        style_ids = [row["meta"]["format_style"]]
        txt = rng.choice(R.ATTACK)
        notes = ({("notice", rng.choice(S["notices"])["ref"]): txt} if c["encoding"] == "notice"
                 else {rng.choice(S["entries"])["n"]: txt})
    spec = {"Q": dict(Q, kinds=False, end_word="at the end"), "gold": row["gold"], "options": opts}
    try:
        fields, res, st, wid, cir, q, tok = RF.render_row(c, S, spec, notes, row_key=row["id"] + name,
                                                          style_ids=style_ids)
    except Exception as ex:
        return "skip:render_" + type(ex).__name__
    v = {"id": row["id"] + "-" + name, "qtype": row["qtype"], "options": opts, "gold": row["gold"], "role": "own",
         "meta": dict(row["meta"], format_style=st["id"]), **fields}
    try:
        P2 = P.parse_row(v)
    except Exception as ex:
        return False
    h1 = canon.structure_hash(Pp["S"], Pp["toggles"], dict(Pp["Q"]))
    h2 = canon.structure_hash(P2["S"], P2["toggles"], dict(P2["Q"]))
    if h1 != h2:
        return False
    if opts and sorted(v["options"]) != sorted(row["options"]):
        return False
    lb, info = __import__("solver_b").solve(P2["S"], P2["Q"])
    if P2["S"]["world"] == "open" and lb == "<UNKNOWN>":
        lb = (P2["statements"].get("T34n") or {}).get("NEI")
    elif row["qtype"] == "choice" and P2["Q"]["qt"] == "Q5":
        lb = __import__("solver_a").latest_id(P2["S"], None, lb)
    return lb == row["gold"]
