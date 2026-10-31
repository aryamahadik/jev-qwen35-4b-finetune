"""Question sentences (Q1, N1, TF, OP) and their counters: inverting count "neg", negcount k_syn / k_all, tf, negcmp, pol.

Questions carry at most one comparator (CMP1-CMP3 question forms, whole and contiguous) or one OP predicate; every
N1 cue sits inside the complement P of a truth frame; choice questions carry no cue (R3-01 to R3-03).
"""
from __future__ import annotations

import sys

from . import lex
from .common import CSRC

sys.path.insert(0, str(CSRC.parent))
from c_src.common.negcount import count as negcount  # noqa: E402

UP = {"ge", "gt"}


def cmp_family(op):
    return "incl" if op in ("ge", "le") else "excl"


def pol_tag(prop, side, neg):
    """3.8 polarity table: prop in up | down | owed | ontime | late; side pays | paid | must_act | waits."""
    if prop in ("up", "owed"):
        t = "bad_yes" if side == "pays" else "good_yes"
    elif prop == "down":
        t = "good_yes" if side == "pays" else "bad_yes"
    elif prop == "ontime":
        t = "good_yes"
    elif prop == "late":
        t = "bad_yes"
    else:
        raise ValueError(prop)
    if neg % 2:
        t = "good_yes" if t == "bad_yes" else "bad_yes"
    return t


def cmp_phrase(op, T, idx, verb=False):
    """(phrase with the threshold filled, negcmp flag, negatable flag)."""
    if verb:
        ph, negcmp = lex.Q_CMP_VERB[op][idx % len(lex.Q_CMP_VERB[op])]
        return f"{ph} {T}", negcmp, False
    ph, pos, negcmp = lex.Q_CMP[op][idx % len(lex.Q_CMP[op])]
    neg_ok = ph in lex.NEGATABLE
    if pos == "post":
        return ph.replace("{T}", T), negcmp, neg_ok
    return f"{ph} {T}", negcmp, neg_ok


def thr_question(res, eid, op, T, neg, tf, rng):
    """Yes/no threshold question. neg in 0..2. Returns (text, info)."""
    info = {"neg": neg, "tf": int(tf or neg > 0)}
    if neg == 0 and not tf:
        idx = rng.randrange(len(lex.Q_CMP[op]))
        ph, negcmp, _ = cmp_phrase(op, T, idx)
        q = lex.fill(rng.choice(lex.Q_DIRECT), res=res, id=eid, cmpT=ph)
        info.update(frame="direct", negcmp=negcmp)
        return q, info
    frame = rng.choice(lex.TF_FRAMES)
    info["frame"] = frame
    if neg == 0:
        if rng.random() < 0.3:
            idx = rng.randrange(len(lex.Q_CMP_VERB[op]))
            ph, negcmp, _ = cmp_phrase(op, T, idx, verb=True)
            P = lex.fill(lex.P_THR_VERB, res=res, id=eid, verbT=ph)
        else:
            idx = rng.randrange(len(lex.Q_CMP[op]))
            ph, negcmp, _ = cmp_phrase(op, T, idx)
            P = lex.fill(lex.P_THR, res=res, id=eid, cmpT=ph)
    elif neg == 1:
        if rng.random() < 0.5:
            cands = [i for i, x in enumerate(lex.Q_CMP[op]) if x[0] in lex.NEGATABLE]
            ph, negcmp, _ = cmp_phrase(op, T, rng.choice(cands))
            P = lex.fill(lex.P_THR_NEG, res=res, id=eid, cmpT=ph)
        else:
            idx = rng.randrange(len(lex.Q_CMP[op]))
            ph, negcmp, _ = cmp_phrase(op, T, idx)
            P = lex.OPN + lex.fill(lex.P_THR, res=res, id=eid, cmpT=ph)
    else:
        cands = [i for i, x in enumerate(lex.Q_CMP[op]) if x[0] in lex.NEGATABLE]
        ph, negcmp, _ = cmp_phrase(op, T, rng.choice(cands))
        P = lex.OPN + lex.fill(lex.P_THR_NEG, res=res, id=eid, cmpT=ph)
    info["negcmp"] = negcmp
    return frame.replace("{P}", P), info


def owed_question(item, eid, neg, tf, rng):
    info = {"neg": neg, "tf": int(tf or neg > 0), "negcmp": False}
    if neg == 0 and not tf:
        return lex.fill(rng.choice(lex.Q_OWED_DIRECT), item=item, id=eid), {**info, "frame": "direct"}
    frame = rng.choice(lex.TF_FRAMES)
    info["frame"] = frame
    if neg == 0:
        P = lex.fill(lex.P_OWED, item=item, id=eid)
    elif neg == 1:
        r = rng.random()
        if r < 0.4:
            P = lex.fill(lex.P_OWED_NEG[0], item=item, id=eid)
        elif r < 0.7:
            P = lex.fill(lex.P_OWED_NEG[1], item=item, id=eid)
        else:
            P = lex.OPN + lex.fill(lex.P_OWED, item=item, id=eid)
    else:
        P = lex.OPN + lex.fill(rng.choice(lex.P_OWED_NEG), item=item, id=eid)
    return frame.replace("{P}", P), info


def counts(q):
    nc = negcount(q)
    return nc.k_syn, nc.k_all
