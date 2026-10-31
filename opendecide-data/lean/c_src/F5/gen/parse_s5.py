"""S5 G3 parser (thread message grammar), solver B (a constraint check per fact: a value v is the fact's value iff
some remaining message by S states v and no remaining message by S about the fact is dated later; remaining =
not retracted by its sender, with the sender's own correction applied) and the S5 question forms (stance verbs)."""
from __future__ import annotations

import json
import re

from . import parse as PZ

ID = r"[A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?"
DATE = r"\d{4}-\d{2}-\d{2}"


def parse(rs, consts):
    r = rs[0]
    sents, rows = PZ.sentences(r["state"])
    msgs = []
    text = " ".join(sents)
    for m in re.finditer(rf"(M\d+)\. ({DATE}), (.+?) wrote: (.+?\.)(?= M\d+\. |$)", text):
        mid, d, snd, body = m.groups()
        mm = re.fullmatch(r"I retract (M\d+)\.", body)
        if mm:
            msgs.append({"mid": mid, "date": d, "sender": snd, "kind": "retract", "e": None, "w": None, "val": None,
                         "target": mm.group(1)})
            continue
        mm = re.fullmatch(rf"Correction to (M\d+): .+? ({ID}) is (not )?([a-z-]+)\.", body)
        if mm:
            msgs.append({"mid": mid, "date": d, "sender": snd, "kind": "correct", "e": mm.group(2), "w": mm.group(4),
                         "val": not mm.group(3), "target": mm.group(1)})
            continue
        mm = re.fullmatch(rf"(.+? ({ID})) is (not )?([a-z-]+)\.", body)
        if mm:
            msgs.append({"mid": mid, "date": d, "sender": snd, "kind": "state", "e": mm.group(2), "w": mm.group(4),
                         "val": not mm.group(3), "target": None})
            continue
        raise ValueError(f"S5 message {body!r}")
    return {"msgs": msgs, "S": consts.get("S"), "world": consts["world"]}


def canon_gen(M):
    return sorted(json.dumps(m, sort_keys=True) for m in M["msgs"])


def canon_parsed(S):
    return sorted(json.dumps(m, sort_keys=True) for m in S["msgs"])


def _effective(S, sender, e, w):
    """[(date, value)] of the sender's remaining statements about (e, w), corrections applied."""
    retracted = {m["target"] for m in S["msgs"] if m["kind"] == "retract"}
    corr = {m["target"]: m["val"] for m in S["msgs"] if m["kind"] == "correct" and m["mid"] not in retracted}
    return [(m["date"], corr.get(m["mid"], m["val"])) for m in S["msgs"]
            if m["kind"] == "state" and m["sender"] == sender and m["e"] == e and m["w"] == w
            and m["mid"] not in retracted]


def _fact(S, e, w):
    eff = _effective(S, S["S"], e, w)
    sols = [v for v in (True, False) if any(val == v and all(d2 <= d for d2, _ in eff) for d, val in eff)]
    if not eff:
        if S["world"] == "closed":
            return False
        raise ValueError("open: undetermined")
    if len(sols) != 1:
        raise ValueError("fact value not unique")
    return sols[0]


def _eval(lf, S):
    op = lf[0]
    if op == "not":
        return not _eval(lf[1], S)
    if op == "and":
        return all(_eval(x, S) for x in lf[1:])
    if op == "adj":
        return _fact(S, lf[1].rsplit(" ", 1)[1], lf[2])
    if op == "stance":
        _, party, which, P = lf
        eff = _effective(S, party, P[1].rsplit(" ", 1)[1], P[2])
        if not eff:
            return False
        v = max(eff)[1]
        return (not v) if which == "deny" else v
    raise ValueError(op)


def solve_b(S, lfs):
    return [_eval(lf, S) for lf in lfs]


def triggers(S):
    return {"SEM-01", "SEM-02" if S["world"] == "closed" else "SEM-03", "SEM-20", "SEM-27", "SEM-31", "SEM-11"}


def decl(c, st, ctx):
    m = re.fullmatch(rf"([A-Z](?:[^\W\d_]|[' -])+?) (denied|confirmed|did not confirm) that (.+? {ID}) is ([a-z-]+)", c)
    if not m:
        return None
    party, v, subj, w = m.groups()
    A = ["adj", subj, w]
    if v == "denied":
        st.add("C7")
        return ["stance", party, "deny", A]
    if v == "confirmed":
        return ["stance", party, "confirm", A]
    st.add("C1")
    return ["not", ["stance", party, "confirm", A]]


def matrix(body, st, ctx):
    m = re.fullmatch(rf"Did ([A-Z](?:[^\W\d_]|[' -])+?) (deny|confirm) that (.+? {ID}) is ([a-z-]+)", body)
    if not m:
        return None
    party, v, subj, w = m.groups()
    if v == "deny":
        st.add("C7")
    return ["stance", party, "deny" if v == "deny" else "confirm", ["adj", subj, w]]


def decl_parsers():
    return [decl], [matrix]
