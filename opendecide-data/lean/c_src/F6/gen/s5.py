"""S5 (held out; mix-tuning dev only, never a training row): a decision interview of questions and answers under a
rule card, with the F6-local dialogue markers ('don't know', 'declined to answer', 'can't recall'; the XF06 marker
table's S5 entries, listed on the card) and planned vs done statements (row 27). Held-out packs and held-out styles
only. The structures, solvers and gates are the rules kind's (S1 shape)."""
from __future__ import annotations

import datetime as dt
import random

from . import common  # noqa: F401
from fmt1 import pool as fpool

from .common import rng_for, unit, h64, ymd
from . import rowmake as M, render_f6 as RF, rules_card as RC, rules_rows as RR, styles_f6 as ST, rules_gen as G
from . import s_rules
from .lex import sw

DIALOGUE = ["don't know", "declined to answer", "can't recall"]


def make_card(card_id: str, schema: str, pack: dict) -> dict:
    card = s_rules.make_card(card_id, "S5", schema, pack, table=False)
    P = card["P"]
    P["adjs"], P["sub"] = [], False
    if P["world"] == "local":
        P["world"] = "open"
    P["plans"] = True
    rng = rng_for("s5card", card_id)
    card["styles"] = fpool.card_style_set(ST.dev_styles(), 4, "F6", card_id)
    card["respondent"] = rng.choice([r for r in pack["roles"] if not any(c in r for c in ":<>|[]()")] or ["Clerk"])
    card["respondent"] = card["respondent"][0].upper() + card["respondent"][1:]
    return card


def _cap(s):
    return s[:1].upper() + s[1:]


def transcript(R: dict, case: str, style: dict, rng: random.Random, card: dict) -> dict:
    F = R["facts"][case]
    ds = card["P"]["date_style"]
    tag = (R.get("ev_tag") or {}).get("tag")
    msgs = []
    for aid in R["attr_order"]:
        a = R["attrs"][aid]
        f = F["num" if a["kind"] == "num" else "cat"].get(aid)
        if f is None:
            continue
        q = f"What is the {a['name']} of {case}?"
        if f.get("m"):
            ans = _cap(f["mtext"]) + "."
        else:
            v = f"{f['v']} {a['unit']}" if a["kind"] == "num" else str(f["v"])
            ans = v + (f" ({tag})" if f.get("tag") else "") + "."
        msgs.append(q)
        msgs.append(ans)
    for eid in R["event_order"]:
        f = F["ev"].get(eid)
        if f is None:
            continue
        e = R["events"][eid]["name"]
        q = f'Did {case} have {RF.a_or_an(chr(34) + e + chr(34))} event?'
        if "plan" in f:
            ans = f"It is planned for {RF.fmt_date(f['plan'], ds)}."
        elif f.get("m"):
            ans = _cap(f["mtext"]) + "."
        else:
            ans = f"Yes, on {RF.fmt_date(f['date'], ds)}" + (f" ({tag})" if f.get("tag") else "") + "."
        msgs.append(q)
        msgs.append(ans)
    t0 = dt.datetime(ymd(R["D"]).year, ymd(R["D"]).month, ymd(R["D"]).day, 9, 0)
    chat = style["container"] == "chat_log"
    out = []
    for i, m in enumerate(msgs):
        spk = "Interviewer" if i % 2 == 0 else card["respondent"]
        msg = {"speaker": spk, "text": m}
        if chat or style["skin"] == "email.digest":
            msg["ts"] = t0 + dt.timedelta(minutes=i)
        if style["skin"] == "email.list_archive":
            msg["subject"] = f"Interview on {case}"
        out.append(msg)
    doc = {"blocks": [{"type": "messages", "messages": out}]}
    if not chat:
        doc["title"] = f"Interview record for {case}"
    return doc


def emit(card: dict, rec: dict, ids: dict) -> tuple[dict, dict]:
    """Like emit.emit_rules, with the record as an interview transcript and the S5 marker sentences."""
    from . import emit as E
    R, case = rec["R"], rec["case"]
    rng = rng_for("s5m", rec["uid"], rec.get("ridx", 0))
    for f in list(R["facts"][case]["num"].values()) + list(R["facts"][case]["cat"].values()) + \
            list(R["facts"][case]["ev"].values()):
        if f.get("m") and "mtext" not in f:
            f["mtext"] = rng.choice(DIALOGUE)
    R["plans"] = True
    R["marker"] = None
    F = R["facts"][case]
    if not (F["num"] or F["cat"] or F["ev"]):
        raise ValueError("an interview needs at least one question")
    rec["_doc_fn"] = lambda st, rr=R, cs=case, cd=card: transcript(rr, cs, st, rng_for("s5d", rec["uid"]), cd)
    rec["_s5"] = True
    return E.emit_rules(card, rec, ids)
