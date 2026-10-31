"""S5 held-out sampler (mix-tuning dev only; never a training row): correspondence threads (G0 section 5, S5; SEM-20,
SEM-27, SEM-31). 4-12 messages among 2-5 parties (the authoritative source <S> is one of them); messages state facts
(an adjective about an entity, or its negation), retract or correct an earlier message of the same sender. Base: a fact
at thread end (<S>'s latest remaining message decides; closed card: no remaining <S> message -> false) or, on closed
cards, a stance (the party's latest remaining statement). 100 bases x 4 rows (A, N, D, V), no attack twin.

M = {world, period, S, noun, ents, msgs [{mid, date, sender, kind: state|retract|correct, e, w, val, target}]}
"""
from __future__ import annotations

import datetime as dt
import random

from .forms import Core, NOT, adj_cores, conn_cores
from .plan import plan_cards
from .packs import views

SAMPLER = "S5"
N_BASES = 100


def plan_dev_cards():
    """S5 dev cards on held-out packs (the first 12 of the held-out pool; the probe uses the rest)."""
    from .packs import heldout_split
    s5_pids, _ = heldout_split()
    cards = plan_cards(12, split="heldout", samplers=["S5"], seed_tag="dv", shares={"S5": 1.0}, held_pids=s5_pids)
    per = [N_BASES // len(cards) + (1 if i < N_BASES % len(cards) else 0) for i in range(len(cards))]
    for c, n in zip(cards, per):
        c["n_bases"] = n
        c["inverted"] = False
    # partners need equal base counts (mirrored plans)
    for c in cards:
        c["n_bases"] = max(c["n_bases"], c["partner"].get("n_bases", 0))
    tot = sum(c["n_bases"] for c in cards)
    return cards


def card_setup(card):
    pv = card["pack"]
    rng = random.Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 8]
    card["ent"] = rng.choice(ents)
    card["S"] = rng.choice(pv["sources"])
    card["people"] = list(pv["people"])
    good = [a for a in pv["adjs"] if a["tag"] == "good"]
    bad = [a for a in pv["adjs"] if a["tag"] == "bad"]
    card["adjs"] = [dict(a, neg=None) for a in good[:3] + bad[:3]]
    card["ptags"] = {a["word"]: a["tag"] for a in card["adjs"]}
    card["negs"] = {}
    card["window"] = pv["window"]
    return card


def plan_slot(card, rng, s):
    kind = "fact"
    if card["world"] == "closed" and card["partner"]["world"] == "closed" and rng.random() < 0.25:
        kind = "stance"
    if s["vk"] == 0 and kind == "stance":
        s["vk"] = 1
    s["attack"] = False
    return {"kind": kind, "depth": 1}


def slot_ctx(card, slot, rng):
    pool = [a["word"] for a in card["adjs"] if a["tag"] == slot["tag"]]
    return {"w": rng.choice(pool)}


def D(s):
    return dt.date.fromisoformat(s)


def remaining(M):
    """Messages after retractions and corrections by their own senders (SEM-31)."""
    msgs = {m["mid"]: dict(m) for m in M["msgs"]}
    gone = set()
    for m in M["msgs"]:
        if m["kind"] == "retract":
            gone.add(m["target"])
    for m in M["msgs"]:
        if m["kind"] == "correct" and m["mid"] not in gone:
            msgs[m["target"]]["val"] = m["val"]
    return [msgs[k] for k in msgs if k not in gone and msgs[k]["kind"] == "state"]


def fact_value(M, e, w, rem=None):
    rem = remaining(M) if rem is None else rem
    s = [m for m in rem if m["sender"] == M["S"] and m["e"] == e and m["w"] == w]
    if not s:
        return False if M["world"] == "closed" else None
    return max(s, key=lambda m: m["date"])["val"]


def stance(M, party, e, w, which, rem=None):
    rem = remaining(M) if rem is None else rem
    s = [m for m in rem if m["sender"] == party and m["e"] == e and m["w"] == w]
    if not s:
        return False
    v = max(s, key=lambda m: m["date"])["val"]
    return (v is False) if which == "deny" else (v is True)


def eval_lf(lf, M, rem):
    op = lf[0]
    if op == "not":
        x = eval_lf(lf[1], M, rem)
        return None if x is None else not x
    if op == "and":
        xs = [eval_lf(a, M, rem) for a in lf[1:]]
        if any(x is False for x in xs):
            return False
        return None if any(x is None for x in xs) else True
    if op == "adj":
        return fact_value(M, lf[1].rsplit(" ", 1)[1], lf[2], rem)
    if op == "stance":
        _, party, which, P = lf
        return stance(M, party, P[1].rsplit(" ", 1)[1], P[2], which, rem)
    raise ValueError(op)


def solve(M, lfs):
    rem = remaining(M)
    check(M)
    out = [eval_lf(lf, M, rem) for lf in lfs]
    if any(o is None for o in out):
        raise ValueError("undetermined")
    return out


def check(M):
    by = {}
    for m in M["msgs"]:
        if m["kind"] == "state":
            k = (m["sender"], m["e"], m["w"], m["date"])
            if k in by:
                raise ValueError("two messages by one party about one fact on one date")
            by[k] = m
    idx = {m["mid"]: m for m in M["msgs"]}
    for m in M["msgs"]:
        if m["kind"] in ("retract", "correct"):
            t = idx[m["target"]]
            if t["sender"] != m["sender"] or m["date"] <= t["date"]:
                raise ValueError("retraction / correction must name an earlier message of its own sender")
            if any(x["sender"] == m["sender"] and x["kind"] == "state" and x["e"] == t["e"] and x["w"] == t["w"]
                   and x["date"] == m["date"] for x in M["msgs"]):
                raise ValueError("retraction shares a date with a message about the fact")


def build_structure(card, slot, rng):
    w0 = D(card["window"][0])
    start = w0 + dt.timedelta(days=rng.randint(0, 200))
    end = start + dt.timedelta(days=rng.randint(30, 90))
    ent = card["ent"]
    ids = list(ent["ids"])
    rng.shuffle(ids)
    ents = ids[:2]
    people = list(card["people"])
    rng.shuffle(people)
    parties = [card["S"]] + people[:rng.randint(1, 3)]
    words = [card["w"]] + rng.sample([a["word"] for a in card["adjs"] if a["word"] != card["w"]], 1)
    msgs = []
    n = rng.randint(4, 10)
    used_days = set()
    for i in range(n):
        d = (start + dt.timedelta(days=rng.randint(0, (end - start).days))).isoformat()
        snd = rng.choice(parties)
        e = rng.choice(ents)
        w = rng.choice(words)
        if (snd, e, w, d) in used_days:
            continue
        used_days.add((snd, e, w, d))
        msgs.append({"mid": None, "date": d, "sender": snd, "kind": "state", "e": e, "w": w,
                     "val": rng.random() < 0.55, "target": None})
    msgs.sort(key=lambda m: m["date"])
    for i, m in enumerate(msgs):
        m["mid"] = f"M{i + 1}"
    if rng.random() < 0.6 and msgs:
        t = rng.choice(msgs)
        later = [x for x in msgs if x["date"] > t["date"]]
        d = (D(t["date"]) + dt.timedelta(days=rng.randint(1, 6))).isoformat()
        if d <= end.isoformat():
            if rng.random() < 0.5:
                msgs.append({"mid": None, "date": d, "sender": t["sender"], "kind": "retract", "e": None, "w": None,
                             "val": None, "target": t["mid"]})
            else:
                msgs.append({"mid": None, "date": d, "sender": t["sender"], "kind": "correct", "e": t["e"],
                             "w": t["w"], "val": not t["val"], "target": t["mid"]})
    msgs.sort(key=lambda m: (m["date"], m["mid"] or "Z"))
    ren = {}
    for i, m in enumerate(msgs):
        if m["mid"]:
            ren[m["mid"]] = f"M{i + 1}"
    for i, m in enumerate(msgs):
        m["mid"] = f"M{i + 1}"
        if m["target"]:
            m["target"] = ren[m["target"]]
    M = {"world": card["world"], "period": [start.isoformat(), end.isoformat()], "S": card["S"], "noun": ent["noun"],
         "ents": ents, "msgs": msgs}
    try:
        check(M)
    except ValueError:
        return None
    e = ents[0]
    subj = f"{ent['noun']} {e}"
    P = ["adj", subj, card["w"]]
    if slot["kind"] == "stance":
        party = [p for p in parties if p != card["S"]]
        if not party:
            return None
        party = party[0]
        if any(m["sender"] == party and m["kind"] in ("retract", "correct") and m.get("e") in (None, e) for m in msgs):
            return None
        which = "confirm"          # an A row has k = 0 and j_q = 0, so the stance base is "confirmed"
        P = ["stance", party, which, ["adj", subj, card["w"]]]
        M["stance"] = {"party": party, "which": which}
    # a correction by S about the asked fact names S's latest message about it (F5-R3-05)
    rem_all = [m for m in msgs if m["kind"] == "state" and m["sender"] == card["S"] and m["e"] == e and
               m["w"] == card["w"]]
    for m in msgs:
        if m["kind"] == "correct" and m["sender"] == card["S"]:
            t = next(x for x in msgs if x["mid"] == m["target"])
            if t["e"] == e and t["w"] == card["w"] and rem_all and t["mid"] != max(rem_all, key=lambda x: x["date"])[
                    "mid"]:
                return None
    try:
        solve(M, [P])
    except ValueError:
        return None
    M["base"] = {"e": e, "subj": subj, "w": card["w"], "words": words}
    return M, P, {"depth": 1 + sum(1 for m in msgs if m["kind"] != "state" and next(
        x for x in msgs if x["mid"] == m["target"])["e"] == e)}


def cores(card, M, P, rng, slot):
    out = {}
    if P[0] == "adj":
        for c in adj_cores(P[1], P[2], None):
            out[c.tid] = c
        for w2 in M["base"]["words"]:
            if w2 != P[2]:
                for c in conn_cores(P[1], P[2], w2):
                    c.tid = f"{c.tid}:{w2}"
                    out[c.tid] = c
        parties = sorted({m["sender"] for m in M["msgs"]} - {M["S"]})
        if M["world"] == "closed":
            for p in parties:
                if not any(m["sender"] == p and m["kind"] != "state" for m in M["msgs"]):
                    out[f"C7.denied:{p}"] = Core(f"C7.denied:{p}", ("C7",), f"{p} denied that {P[1]} is {P[2]}", None,
                                                 ["stance", p, "deny", P], 1, None, lneg=("deny",), rel="other")
    else:
        party, which, A = P[1], P[2], P[3]
        verb = "denied" if which == "deny" else "confirmed"
        out["ST.pos"] = Core("ST.pos", (), f"{party} {verb} that {A[1]} is {A[2]}",
                             f"Did {party} {'deny' if which == 'deny' else 'confirm'} that {A[1]} is {A[2]}", P,
                             1 if which == "deny" else 0, None, lneg=("deny",) if which == "deny" else ())
        if which == "confirm":
            out["C1.st"] = Core("C1.st", ("C1",), f"{party} did not confirm that {A[1]} is {A[2]}", None, NOT(P), 1,
                                None, nd=True, lneg=("not",))
        out["C7.alt"] = Core("C7.alt", ("C7",), f"{party} {'confirmed' if which == 'deny' else 'denied'} that {A[1]} "
                                                f"is {A[2]}", None,
                             ["stance", party, "confirm" if which == "deny" else "deny", A],
                             0 if which == "deny" else 1, None, rel="other")
    return out


def is_v_core(card, c):
    return c.rel in ("conn", "other") and (c.k >= 1 or c.fam == ("C16",))


def nd_ok(card, c):
    return True


def valid_structure(card, M, P):
    return True


def tag_of(card, P, M):
    A = P if P[0] == "adj" else P[3]
    return card["ptags"].get(A[2])


def perturb(M, rng):
    return []


def msg_text(M, m):
    s = f"{m['mid']}. {m['date']}, {m['sender']} wrote: "
    if m["kind"] == "state":
        subj = f"{M['noun']} {m['e']}"
        return s + f"{subj[:1].upper() + subj[1:]} is {'' if m['val'] else 'not '}{m['w']}."
    if m["kind"] == "retract":
        return s + f"I retract {m['target']}."
    subj = f"{M['noun']} {m['e']}"
    return s + f"Correction to {m['target']}: {subj} is {'' if m['val'] else 'not '}{m['w']}."


def doc(M, inert=None, attack=None):
    return {"title": "Correspondence", "blocks": [{"type": "items", "items": [msg_text(M, m) for m in M["msgs"]]}]}


def text_triggers(M):
    return {"SEM-01", "SEM-02" if M["world"] == "closed" else "SEM-03", "SEM-20", "SEM-27", "SEM-31", "SEM-11"}


def full_keys(card):
    return {"SEM-01", "SEM-02" if card["world"] == "closed" else "SEM-03", "SEM-20", "SEM-27", "SEM-31", "SEM-11",
            "SEM-10", "SEM-28"}


def sem_params(card, M):
    return {"etype": f"{card['ent']['noun']} and every party", "S": card["S"], "D_start": M["period"][0],
            "D_end": M["period"][1], "value_sets": [], "affixed": []}


def affixed_used(M):
    return []


def t_txt(M):
    from .common import negc
    return sum(1 for m in M["msgs"] if negc(msg_text(M, m)).k_all > 0)


def fewshot(card, b):
    return None


def inverted_block(card, b):
    return None
