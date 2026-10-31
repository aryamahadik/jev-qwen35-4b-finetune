"""F3 samplers (G0 spec section 4). Training: S1 forward event sequences, S2 target-first (planted decisive chains with
near misses), S3 ledger tables, S4 multi-notice correspondence, S6 effective-date amendments. Held out: S5 git-like log
syntax (mix-tuning dev only). Every sampler returns a valid closed structure; open cards then hide entries (gaps)."""
from __future__ import annotations

import copy
import hashlib
import random

import solver_a as A
from f3common import d_add
from logbuild import Builder

EVENT_BINS = ((5, 12, 0.30), (13, 24, 0.40), (25, 40, 0.30))


def draw_bin(rng, deficits=None):
    w = [b[2] for b in EVENT_BINS]
    if deficits:
        w = [max(0.02, x + deficits.get(i, 0)) for i, x in enumerate(w)]
    i = rng.choices(range(3), weights=w)[0]
    lo, hi, _ = EVENT_BINS[i]
    return i, rng.randint(lo, hi)


def mech_weights(card, closed=True):
    m = set(card["mechs"])
    w = {"CREATE": 2.0, "SET": 5.0, "TRANSFER": 6.0, "OPEN": 0.8}
    if "SETQ" in m:
        w["SETQ"] = 1.5
        w["ADJUST"] = 2.5
    if "VOID" in m:
        w["VOID"] = 3.5
    if "CORR" in m:
        w["CORR"] = 2.5
    if "SUPERSEDE" in m:
        w["SUPERSEDE"] = 4.0
    if "RENAME" in m:      # repair r2: most renames and merges are planted chain hops (decisive where present)
        w["RENAME"] = 0.25
    if "MERGE" in m:
        w["MERGE"] = 0.4
    return w


def start_date(rng):
    y = rng.randint(2031, 2049)
    m = rng.randint(1, 12)
    d = rng.randint(1, 20)
    return f"{y:04d}-{m:02d}-{d:02d}"


def _builder(card, rng, sampler, *, n_items, n_holders, n_docs=0, in_register=0.6, lookalikes=0,
             holder_lookalikes=0, timed=None):
    return Builder(card, rng, sampler=sampler, n_items=n_items, n_holders=n_holders, n_docs=n_docs,
                   in_register=in_register if card["has_register"] else 0.0, start_date=start_date(rng),
                   timed=card["timed"] if timed is None else timed, lookalikes=lookalikes,
                   holder_lookalikes=holder_lookalikes)


def _old_id_uses(b, rng, p=0.25):
    """E8: some entries after a rename use the old ID (alias: valid; retire: the entry has no effect)."""
    S = b.S
    ren = [e for e in S["entries"] if e["t"] == "RENAME"]
    if not ren:
        return
    for e in S["entries"]:
        for r in ren:
            if e["n"] <= r["n"] or rng.random() > p:
                continue
            for k in ("item", "sender", "receiver"):
                if e.get(k) == r["new"]:
                    old = e[k]
                    e[k] = r["old"]
                    if A.check_rules(S):
                        e[k] = old


# ------------------------------------------------------------------------------------------------ S1

def gen_S1(card, rng, plan):
    n_items = plan.get("n_items") or rng.randint(2, 6)
    n_holders = plan.get("n_holders") or rng.randint(3, 8)
    n_docs = rng.randint(1, 2) if card["docs_on"] else 0
    la = card.get("lookalikes_on")
    b = _builder(card, rng, card["sampler"] if card["sampler"] == "S5" else "S1", n_items=n_items,
                 n_holders=n_holders, n_docs=n_docs, lookalikes=rng.choice([0, 1, 1]) if la else 0,
                 holder_lookalikes=rng.choice([0, 1]) if la else 0)
    if card["sampler"] == "S5":
        b.S["register"]["items"] = []
        b.uncreated = list(b.items)
        b.unopened += [(d, r) for d, r in b.S["register"]["docs"]]
        b.S["register"]["docs"] = []
    if card["sampler"] != "S5" or card.get("windows"):
        b.set_windows(plan["n_entries"], chains=plan.get("chains"))
    b.run(plan["n_entries"], mech_weights(card))
    _old_id_uses(b, rng)
    return b


# ------------------------------------------------------------------------------------------------ S2 (target-first)

def gen_S2(card, rng, plan):
    """Plant a decisive chain for target item Y at a planned decile, with >= 2 near misses (one E4 look-alike)."""
    n_items = plan.get("n_items") or rng.randint(3, 9)
    n_holders = plan.get("n_holders") or rng.randint(3, 10)
    n_docs = rng.randint(1, 2) if card["docs_on"] else 0
    b = _builder(card, rng, "S2", n_items=n_items, n_holders=n_holders, n_docs=n_docs, in_register=0.8,
                 lookalikes=1, holder_lookalikes=1)
    N = plan["n_entries"]
    decile = plan.get("decile", rng.randrange(10))
    p_dec = max(2, min(N, int((decile + rng.random()) * N / 10) + 1))
    mech = plan.get("mech") or "plain"
    W = mech_weights(card)
    # background up to just before the planted chain
    look = dict(b.look_items)
    targets = [y for y in look.values()] or b.items[:1]
    Y = targets[0]
    Yl = next((k for k, v in look.items() if v == Y), None)
    pre = max(1, p_dec - 3)
    ch = list(plan.get("chains") or [])[1:2] if rng.random() < 0.67 else []
    b.set_windows(N, chains=ch, exclude={Y, Yl})
    b.run(pre, W)
    st, E = b.state()
    if E.find(Y) not in st.exists:
        e = b.cand_entry("CREATE", st, E, item=Y) if Y in b.uncreated else None
        if e and b.try_add(e):
            b.uncreated.remove(Y)
    if Yl and Yl in b.uncreated:
        st, E = b.state()
        e = b.cand_entry("CREATE", st, E, item=Yl)
        if e and b.try_add(e):
            b.uncreated.remove(Yl)
    if mech in ("SUPERSEDE", "CHECK"):
        _plant(b, rng, mech, Y, card)
    else:
        # repair r2: the planted chain has the planned depth (several hops), led by the planned mechanism
        f0, want = (list(plan.get("chains") or []) + [("status", 2)])[0]
        field = "holder" if mech == "MERGE" else f0
        b.plant_now(Y, field, want, first=None if mech == "plain" else mech)
    # near misses: E4 on the look-alike, before or after the decisive entry (50/50, B10)
    after = rng.random() < 0.5
    if not after:
        _near_miss(b, rng, Yl, Y, card)
    # repair r2: the planted chain stays decisive (no later background entry touches Y; near misses are explicit)
    b.win[Y] = (pre, b.n)
    b.run(min(N, b.n + max(0, N - b.n - 2)), W)
    if after:
        _near_miss(b, rng, Yl, Y, card)
    b.run(N, W)
    _old_id_uses(b, rng)
    b.target_item = Y
    b.planned_mech = mech
    return b


def _plant(b, rng, mech, Y, card):
    st, E = b.state()
    name = lambda: b.name_of(Y, E, st)  # noqa: E731
    if E.find(Y) not in st.exists:
        return
    if mech == "VOID":
        e1 = b.try_add(b.cand_entry("SET", st, E, item=Y))
        if e1:
            st, E = b.state()
            e2 = b.try_add(b.cand_entry("SET", st, E, item=Y))
            if e2:
                b.try_add({"t": "VOID", "target": e2["n"]})
        if rng.random() < 0.5:
            st, E = b.state()
            t1 = b.cand_entry("TRANSFER", st, E, item=Y)
            if t1:
                t1 = b.try_add(t1)
                if t1:
                    b.try_add({"t": "VOID", "target": t1["n"]})
    elif mech == "CORR":
        if rng.random() < 0.5:
            e1 = b.try_add(b.cand_entry("SET", st, E, item=Y))
            if e1:
                vals = [v for v in b.S["statuses"] if v != e1["value"]]
                b.try_add({"t": "CORR", "target": e1["n"], "slot": "value", "value": rng.choice(vals)})
        else:
            t1 = b.cand_entry("TRANSFER", st, E, item=Y)
            if t1:
                t1 = b.try_add(t1)
                if t1:
                    st, E = b.state()
                    live = [x for x in b.live_holders(st, E) if x not in (t1["receiver"], t1["sender"])]
                    if live:
                        b.try_add({"t": "CORR", "target": t1["n"], "slot": "receiver", "value": rng.choice(live)})
        if rng.random() < 0.4:   # E3: a correction that a later SET overrides
            st, E = b.state()
            b.try_add(b.cand_entry("SET", st, E, item=Y))
    elif mech == "SUPERSEDE":
        for _ in range(rng.randint(2, 3)):
            st, E = b.state()
            e = b.cand_entry("SUPERSEDE", st, E)
            if e:
                b.try_add(e)
        sup = [e for e in b.S["entries"] if e["t"] == "SUPERSEDE"]
        if sup and rng.random() < 0.6:
            b.try_add({"t": "VOID", "target": sup[-1]["n"]})
    elif mech == "RENAME" and card["rename_mode"]:
        b.try_add({"t": "RENAME", "kind": "item", "old": name(), "new": b.fresh_item_id()})
        st, E = b.state()
        b.try_add(b.cand_entry("TRANSFER", st, E, item=Y) or {"t": "X"})
    elif mech == "MERGE" and "MERGE" in card["mechs"]:
        h = st.holder.get(E.find(Y))
        live = [x for x in b.live_holders(st, E) if E.find(x) != h]
        if h is not None and live:
            b.try_add({"t": "MERGE", "absorbed": b.holder_name(h, E, st), "survivor": rng.choice(live)})
    elif mech == "CHECK" and (card["check"] or card["lock"]):
        saved = card.get("wrong_sender_p")
        card["wrong_sender_p"] = 0.9
        e = b.cand_entry("TRANSFER", st, E, item=Y)
        card["wrong_sender_p"] = saved if saved is not None else 0.3
        if e:
            b.try_add(e)
        if card["lock"] and rng.random() < 0.5:
            st, E = b.state()
            b.try_add({"t": "SET", "item": name(), "field": "status", "value": card["lock_status"]})
            st, E = b.state()
            e = b.cand_entry("TRANSFER", st, E, item=Y)
            if e:
                b.try_add(e)
    else:
        k = rng.choice(["SET", "TRANSFER"])
        b.try_add(b.cand_entry(k, st, E, item=Y) or {"t": "X"})


def _near_miss(b, rng, Yl, Y, card):
    st, E = b.state()
    if Yl and E.find(Yl) in st.exists:
        k = rng.choice(["SET", "TRANSFER"])
        e = b.cand_entry(k, st, E, item=Yl)
        if e:
            b.try_add(e)
    # a second named error: E1 (voided tempting value) or E2 (original value of a corrected entry)
    st, E = b.state()
    if E.find(Y) in st.exists and "VOID" in card["mechs"] and rng.random() < 0.6:
        e = b.cand_entry("SET", st, E, item=Y)
        if e:
            e = b.try_add(e)
            if e:
                b.try_add({"t": "VOID", "target": e["n"]})


# ------------------------------------------------------------------------------------------------ S3 (ledger tables)

def gen_S3(card, rng, plan):
    big = plan.get("roster", 0)
    n_items = plan.get("n_items") or (rng.randint(10, 18) if not big else big)
    n_holders = plan.get("n_holders") or rng.randint(4, 12)
    la = card.get("lookalikes_on")
    b = _builder(card, rng, "S3", n_items=n_items, n_holders=n_holders, n_docs=0, in_register=0.85,
                 lookalikes=rng.choice([0, 1, 1]) if la else 0, holder_lookalikes=rng.choice([0, 1]) if la else 0)
    N = min(plan["n_entries"], 24 if plan.get("big_roster") else 27)
    b.set_windows(N, chains=plan.get("chains"))
    b.run(N, mech_weights(card))
    _old_id_uses(b, rng)
    return b


# ------------------------------------------------------------------------------------------------ S4 (notices)

def gen_S4(card, rng, plan):
    n_items = plan.get("n_items") or rng.randint(2, 8)
    n_holders = plan.get("n_holders") or rng.randint(3, 9)
    n_docs = rng.randint(1, 2) if card["docs_on"] else 0
    la = card.get("lookalikes_on")
    b = _builder(card, rng, "S4", n_items=n_items, n_holders=n_holders, n_docs=n_docs, timed=False,
                 lookalikes=rng.choice([0, 1]) if la else 0)
    W = mech_weights(card)
    W.pop("VOID", None)
    S = b.S
    S["notices"] = []
    target = plan["n_entries"]
    b.set_windows(target, chains=plan.get("chains"))
    people = card["people"] or ["the registry desk", "the field office"]
    ref = 0
    withdrawn = set()
    has_withdraw = set()
    fails = 0
    while b.n < target and fails < 60:
        ref += 1
        size = rng.choices([1, 2, 3, 4], [0.3, 0.35, 0.2, 0.15])[0]
        b.date = d_add(b.date, rng.randint(0, 4)) if ref > 1 else b.date
        frm, to = rng.sample(people, 2) if len(people) >= 2 else (people[0], people[0])
        S["notices"].append({"ref": ref, "date": b.date, "from": frm, "to": to})
        k = 0
        for _ in range(size):
            if b.n >= target:
                break
            st, E = b.state()
            added = None
            ce, ci = b.chain_next(st, E)
            if ce is not None and ce["t"] == "WITHDRAW" and ce["target_ref"] == ref:
                ce = None    # a notice never withdraws itself: the withdrawal waits for a later notice
            if ce is not None:
                ce["ref"], ce["k"] = ref, k + 1
                got = b.try_add(ce, stamp=False)
                b.chain_done(ci, got)
                if got is not None:
                    if got["t"] == "WITHDRAW":
                        withdrawn.add(got["target_ref"])
                        has_withdraw.add(ref)
                    k += 1
                    continue
            for _try in range(10):
                r = rng.random()
                if r < 0.14 and "VOID" in card["mechs"] and ref > 1:
                    elig = [nt["ref"] for nt in S["notices"][:-1] if nt["ref"] not in withdrawn
                            and nt["ref"] not in has_withdraw
                            and all(e["t"] in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE")
                                    for e in S["entries"] if e.get("ref") == nt["ref"])
                            and any(e.get("ref") == nt["ref"] for e in S["entries"])]
                    if b.win or b.dwin:
                        elig = [x for x in elig if not any(b.touches_frozen(e) for e in S["entries"]
                                                           if e.get("ref") == x)]
                    if not elig:
                        continue
                    m = rng.choice(elig)
                    e = {"t": "WITHDRAW", "target_ref": m}
                else:
                    kind = rng.choices(list(W), weights=list(W.values()))[0]
                    if kind == "CREATE" and not b.uncreated:
                        continue
                    e = b.cand_entry(kind, st, E)
                    if e is None:
                        continue
                e["ref"], e["k"] = ref, k + 1
                got = b.try_add(e, stamp=False)
                if got is not None:
                    if e["t"] == "CREATE":
                        b.uncreated.remove(e["item"])
                    if e["t"] == "OPEN":
                        b.unopened.pop(0)
                    if e["t"] == "WITHDRAW":
                        withdrawn.add(e["target_ref"])
                        has_withdraw.add(ref)
                    added = got
                    break
            if added is None:
                fails += 1
                continue
            k += 1
        if k == 0:
            S["notices"].pop()
            ref -= 1
    # a withdrawn notice may hold only voidable changes and never withdraws anything (re-checked)
    _old_id_uses(b, rng)
    return b


# ------------------------------------------------------------------------------------------------ S6 (effective dates)

def gen_S6(card, rng, plan):
    n_items = plan.get("n_items") or rng.randint(2, 8)
    n_holders = plan.get("n_holders") or rng.randint(3, 9)
    la = card.get("lookalikes_on")
    b = _builder(card, rng, "S6", n_items=n_items, n_holders=n_holders, n_docs=0, in_register=1.0, timed=False,
                 lookalikes=rng.choice([0, 1]) if la else 0)
    S = b.S
    d0 = b.date
    S["d0"] = d0
    b.date = d_add(d0, rng.randint(1, 3))
    W = mech_weights(card)
    W.pop("CREATE", None)
    W.pop("OPEN", None)
    target = plan["n_entries"]
    b.set_windows(target, docs=False, chains=plan.get("chains"))
    fails = 0
    while b.n < target and fails < target * 20:
        st, E = b.state()
        e, ci = b.chain_next(st, E)
        if e is None:
            kind = rng.choices(list(W), weights=list(W.values()))[0]
            e = b.cand_entry(kind, st, E)
        if e is None:
            fails += 1
            continue
        if b.n > 0 and rng.random() > 0.35:
            b.date = d_add(b.date, rng.randint(1, 3))
        e["date"] = b.date
        if e["t"] not in ("VOID", "CORR"):
            lo = d_add(d0, 1)
            span = max(0, (A_days(lo, b.date)))
            back = rng.randint(0, min(span, 12))
            e["eff"] = d_add(b.date, -back) if rng.random() < 0.7 else b.date
        got = b.try_add(e, stamp=False)
        if ci is not None:
            b.chain_done(ci, got)
        if got is None:
            fails += 1
    # every effective date on or before the last recorded date (T6)
    return b


def A_days(a, b):
    from f3common import d_parse
    return (d_parse(b) - d_parse(a)).days


# ------------------------------------------------------------------------------------------------ S5 (git-like, dev)

def gen_S5(card, rng, plan):
    b = gen_S5_deep(card, rng, plan) if card.get("deep_card") else gen_S1(card, rng, plan)
    S = b.S
    hashes, seen = {}, set()
    for e in S["entries"]:
        while True:
            h = hashlib.sha256(f"{card['card_id']}:{rng.random()}".encode()).hexdigest()[:12]
            if h[:7] not in seen:
                break
        seen.add(h[:7])
        hashes[e["n"]] = h
    # look-alike line hashes: some lines share a 7-character prefix with another line (B20)
    ns = [e["n"] for e in S["entries"]]
    for i in range(0, len(ns) - 1, 4):
        a, c = ns[i], ns[i + 1]
        hashes[c] = hashes[a][:7] + hashes[c][7:]
    S["hashes"] = {str(k): v for k, v in hashes.items()}
    return b


def gen_S5_deep(card, rng, plan):
    """Deep S5 logs for the depth sweep: a target item's holder history stacked with layers that each add hops on
    solver B's decisive path (a corrected receiver, voided later transfers, transfers blocked by the transfer check,
    transfers that name a retired holder ID), interleaved with background entries on other items."""
    b = _builder(card, rng, "S5", n_items=rng.randint(2, 4), n_holders=rng.randint(5, 8), in_register=0.0,
                 timed=card["timed"])
    W = mech_weights(card)
    W.pop("RENAME", None)
    for y in list(b.uncreated):
        st, E = b.state()
        e = b.cand_entry("CREATE", st, E, item=y)
        if e and b.try_add(e):
            b.uncreated.remove(y)
    Y = b.items[0]
    layers = plan.get("deep_layers", rng.randint(0, 7))
    st, E = b.state()
    w = b.cand_entry("TRANSFER", st, E, item=Y)
    w = b.try_add(w) if w else None
    if not w:
        return b
    kinds = []
    for _ in range(layers):
        kinds.append(rng.choice(["void", "void", "blocked", "blocked", "retired", "corr"]))
    used_corr = False
    for k in kinds:
        if rng.random() < 0.5:
            b.run(b.n + 1, W)
        st, E = b.state()
        if k == "corr" and not used_corr:
            live = [x for x in b.live_holders(st, E) if x not in (w["receiver"], w["sender"])]
            if live and b.try_add({"t": "CORR", "target": w["n"], "slot": "receiver", "value": rng.choice(live)}):
                used_corr = True
        elif k == "void":
            t = b.cand_entry("TRANSFER", st, E, item=Y)
            if t:
                card["wrong_sender_p"] = 0.0
                t = b.try_add(t)
                if t:
                    b.try_add({"t": "VOID", "target": t["n"]})
        elif k == "blocked":
            h = st.holder.get(E.find(Y))
            others = [x for x in b.live_holders(st, E) if E.find(x) != h]
            if len(others) >= 2:
                snd, rcv = rng.sample(others, 2)
                b.try_add({"t": "TRANSFER", "item": b.name_of(Y, E, st), "sender": snd, "receiver": rcv})
        elif k == "retired":
            h = st.holder.get(E.find(Y))
            if h is None:
                continue
            old = b.holder_name(h, E, st)
            new = b.fresh_holder_id()
            if b.try_add({"t": "RENAME", "kind": "holder", "old": old, "new": new}):
                st, E = b.state()
                others = [x for x in b.live_holders(st, E) if E.find(x) != E.find(new)]
                if others:
                    b.try_add({"t": "TRANSFER", "item": b.name_of(Y, E, st), "sender": old,
                               "receiver": rng.choice(others)})
    b.run(min(40, b.n + rng.randint(1, 4)), W)
    b.target_item = Y
    return b


SAMPLERS = {"S1": gen_S1, "S2": gen_S2, "S3": gen_S3, "S4": gen_S4, "S6": gen_S6, "S5": gen_S5}


# ------------------------------------------------------------------------------------------------ open world

def _removable(full, ns):
    """True if the complete log stays valid with entries `ns` left out (no later shown entry depends on them, so a
    missing slot is not forced; this keeps the solver C lemma: unknown values have two kept worlds that differ)."""
    W = copy.deepcopy(full)
    W["entries"] = [e for e in W["entries"] if e["n"] not in ns]
    if any(e["t"] in ("VOID", "CORR") and e["target"] in ns for e in W["entries"]):
        return False
    if any(e["t"] == "WITHDRAW" and any(x["n"] in ns and x.get("ref") == e["target_ref"] for x in full["entries"])
           for e in W["entries"]):
        return False
    return not A.check_rules(W)


def make_open(card, b, rng):
    """Hide entries of a complete closed log to make an open-card structure (T2, T3). Returns (shown S, full S) or
    None if no valid hiding exists. At most 2 missing entries in total (solver C stays exhaustive)."""
    full = copy.deepcopy(b.S)
    S = copy.deepcopy(full)
    gs = card["gap_style"]
    ents = S["entries"]
    if len(ents) < 5:
        return None
    S["world"] = "open"
    S["gap_style"] = gs
    # repair r2: the hidden entries come before the planted chains' writers (on 75% of logs), so a chain item stays
    # knowable (T2: its writer follows every missing entry) and can carry a deep yes/no row
    limit = min((ch["w_n"] for ch in getattr(b, "chains", []) if ch.get("w_n")), default=None)
    if limit is not None and rng.random() > 0.75:
        limit = None
    if gs == "leading":
        hi0 = max(2, min(len(ents) - 3, len(ents) // 2, len(ents) - card.get("_bin_lo", 5) + 1))
        if limit is not None and limit >= 2:
            hi0 = max(2, min(hi0, limit))
        n0 = rng.randint(2, hi0)
        hidden = [e for e in ents if e["n"] < n0]
        shown = [e for e in ents if e["n"] >= n0]
        if S["sampler"] == "S4":
            r0 = next(e["ref"] for e in shown)
            hidden = [e for e in ents if e["ref"] < r0]
            shown = [e for e in ents if e["ref"] >= r0]
            S["notices"] = [nt for nt in S["notices"] if nt["ref"] >= r0]
            S["n0"] = r0
        else:
            S["n0"] = n0
        S["entries"] = shown
        S["register"] = {"items": [], "docs": []}
        S["gaps"] = []
        hidden_ns = {e["n"] for e in hidden}
    else:
        n_missing = rng.choice([1, 1, 2])
        cands = [e for e in ents[1:-1]]
        if limit is not None and [e for e in cands if e["n"] < limit]:
            cands = [e for e in cands if e["n"] < limit]
        rng.shuffle(cands)
        hidden_ns = set()
        targeted = {e.get("target") for e in ents if e["t"] in ("VOID", "CORR")}
        for e in cands:
            if len(hidden_ns) >= n_missing:
                break
            if e["t"] in ("CREATE", "OPEN") or e["n"] in targeted:
                continue
            if not _removable(full, {e["n"]} | hidden_ns if S["sampler"] != "S4" else
                              {x["n"] for x in ents if x["ref"] == e["ref"]} | hidden_ns):
                continue
            if S["sampler"] == "S4":
                # whole notices only: hide a notice whose changes are all hideable
                ref = e["ref"]
                group = [x for x in ents if x["ref"] == ref]
                if ref == ents[0]["ref"] or ref == ents[-1]["ref"] or len(group) > 2:
                    continue
                if any(x["t"] in ("CREATE", "OPEN") or x["n"] in targeted for x in group):
                    continue
                if any(x["t"] == "WITHDRAW" for x in ents if x not in group and x.get("target_ref") == ref):
                    continue
                hidden_ns |= {x["n"] for x in group}
                break
            hidden_ns.add(e["n"])
        if not hidden_ns:
            return None
        S["entries"] = [e for e in ents if e["n"] not in hidden_ns]
        if S["sampler"] == "S4":
            hrefs = sorted({e["ref"] for e in ents if e["n"] in hidden_ns})
            S["notices"] = [nt for nt in S["notices"] if nt["ref"] not in hrefs]
            S["gap_refs"] = hrefs
            # a gap position = after the last shown change before the hidden notice
            S["gaps"] = sorted({max(e["n"] for e in S["entries"] if e["ref"] < r) for r in hrefs})
            # repair r2 (G5 seed 5002 flag): render_f3 draws the explicit marker after these shown notices
            S["gap_after_refs"] = sorted({max(e["ref"] for e in S["entries"] if e["ref"] < r) for r in hrefs})
        else:
            S["gaps"] = sorted({max(e["n"] for e in S["entries"] if e["n"] < h) for h in hidden_ns})
    # shown text names no item that only a missing entry creates (rule 19)
    created_hidden = {e["item"] for e in ents if e["n"] in hidden_ns and e["t"] == "CREATE"}
    if gs != "leading":
        for e in S["entries"]:
            for k in ("item",):
                if e.get(k) in created_hidden:
                    return None
    # shown VOID / CORR never points at a missing entry
    shown_ns = {e["n"] for e in S["entries"]}
    for e in S["entries"]:
        if e["t"] in ("VOID", "CORR") and e["target"] not in shown_ns:
            return None
        if e["t"] == "WITHDRAW" and e["target_ref"] not in {x["ref"] for x in S["entries"]}:
            return None
    S["hidden"] = sorted(hidden_ns)
    return S, full
