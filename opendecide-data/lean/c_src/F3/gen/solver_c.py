"""Solver C: possible worlds for open-card rows (G0 spec section 3).

A world fills every missing slot (each skipped number / missing notice; leading extracts: the opening state of the
queried item) with one entry from the alphabet the open card allows (T2: no rename or merge), and is kept only if it
satisfies every rule the card states: rule 6 as T17 states it (the named sender holds the item just before every
non-voided transfer), rule 7 / T28 (no quantity below 0), T36 (statuses from the listed values), T10 / T11 targets
(earlier entries only) and the numbering and date order of T3 / T5 / T41.

Alphabet per slot, reduced without loss for the queried item Y (open cards have no transfer check, lock rule,
rename or merge, so entries about other items never change Y's values): every entry about Y the card allows (SET of
each listed status, SET of each card quantity value plus one fresh value, ADJUST by +1 / -1, TRANSFER to each holder
plus one fresh holder, VOID and CORRECTION of each eligible earlier shown entry about Y in each allowed slot), plus the
original hidden entry and an inert creation of a fresh item (both stand for every filler that does not concern Y).
The verdict: every kept world gives the same answer (decided; it must equal solver A's), or two kept worlds differ
(NEI; solver A must say unknown).
"""
from __future__ import annotations

import copy
import itertools

import solver_a as A

FRESH_HOLDER = "ZZ-999"
FRESH_ITEM = "ZQ-9Z9Z"


def _world_answer(W, Q):
    """Answer on a complete world (closed replay)."""
    Wc = dict(W)
    Wc["world"] = "closed"
    Wc["gap_style"] = None
    Wc["gaps"] = []
    Qx = dict(Q)
    if Q["qt"] == "Q4" and (Q.get("neg") == "N2" or (Q.get("neg") == "D" and Q.get("dbase") == "N2")):
        states, eff, E, _ = A.replay(Wc)
        X = E.find(Q["holder"])
        at_end = states[-1].holder.get(E.find(Q["item"])) == X
        some = any(st.holder.get(E.find(Q["item"])) == X for st in states)
        guard = states[0].holder.get(E.find(Q["item"])) == X or A.guard_ok(Wc, states, eff, E, Q["item"], Q["holder"])
        if not guard or not some:
            return ("PRESUP_FAIL",)
        nl = some and not at_end
        return int(nl) if Q["neg"] == "N2" else int(not nl)
    if Q.get("still"):
        states, eff, E, _ = A.replay(Wc)
        if not A.guard_ok(Wc, states, eff, E, Q["item"], Q["holder"]) and \
                states[0].holder.get(E.find(Q["item"])) != E.find(Q["holder"]):
            return ("PRESUP_FAIL",)
    return A.answer(Wc, Qx)


def _valid(W):
    Wc = dict(W)
    Wc["world"] = "closed"
    Wc["gap_style"] = None
    Wc["gaps"] = []
    bad = A.check_rules(Wc)
    return not [b for b in bad if b not in ("item_before_create",)]


def _y_alphabet(S, Q, Y, holders, qty_vals, earlier):
    """Entries about Y for one slot (dicts without n/date)."""
    out = []
    kind = Q["kind"]
    if kind == "status":
        for v in S["statuses"]:
            out.append({"t": "SET", "item": Y, "field": "status", "value": v})
    if kind == "qty":
        for v in sorted(set(qty_vals)) + [max(qty_vals or [0]) + 37]:
            out.append({"t": "SET", "item": Y, "field": "qty", "value": v})
        out.append({"t": "ADJUST", "item": Y, "sign": 1, "amount": 1})
        out.append({"t": "ADJUST", "item": Y, "sign": -1, "amount": 1})
    if kind == "holder":
        for h in holders + [FRESH_HOLDER]:
            out.append({"t": "TRANSFER", "item": Y, "sender": None, "receiver": h})
    for e in earlier:
        about_y = e.get("item") == Y
        if e["t"] in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE") and (about_y or e["t"] == "CORR"):
            out.append({"t": "VOID", "target": e["n"]})
        if about_y and e["t"] == "SET" and e["field"] == "status" and kind == "status":
            for v in S["statuses"]:
                out.append({"t": "CORR", "target": e["n"], "slot": "value", "value": v})
        if about_y and e["t"] == "CREATE" and kind == "status":
            for v in S["statuses"]:
                out.append({"t": "CORR", "target": e["n"], "slot": "status", "value": v})
        if about_y and kind == "qty":
            if e["t"] == "SET" and e["field"] == "qty":
                for v in sorted(set(qty_vals)) + [max(qty_vals or [0]) + 37]:
                    out.append({"t": "CORR", "target": e["n"], "slot": "value", "value": v})
            if e["t"] == "ADJUST":
                for v in (max(1, e["amount"] - 1), e["amount"] + 1):
                    out.append({"t": "CORR", "target": e["n"], "slot": "amount", "value": v})
            if e["t"] == "CREATE":
                for v in sorted(set(qty_vals)) + [max(qty_vals or [0]) + 37]:
                    out.append({"t": "CORR", "target": e["n"], "slot": "qty", "value": v})
        if about_y and e["t"] == "TRANSFER" and kind == "holder":
            for h in holders + [FRESH_HOLDER]:
                if h not in (e["receiver"], e["sender"]):
                    out.append({"t": "CORR", "target": e["n"], "slot": "receiver", "value": h})
    return out


def verify(S, Q, gold, *, nei, full=None, max_worlds=20000):
    """{"ok", "why", "worlds", "verdict"}: ok when the possible-worlds verdict agrees with solver A's label."""
    full = full or S.get("_full")
    vals, eff, E = A.open_values(S)
    Y = Q["item"]
    holders = sorted({x[1] for x in S["register"]["items"]} |
                     {e[k] for e in S["entries"] for k in ("holder", "sender", "receiver") if e.get(k)} |
                     {e["value"] for e in S["entries"] if e["t"] == "CORR" and e["slot"] == "receiver"})
    qty_vals = sorted({x[3] for x in S["register"]["items"] if x[3] is not None} |
                      {e["value"] for e in S["entries"] if e["t"] == "SET" and e["field"] == "qty"} |
                      {e["qty"] for e in S["entries"] if e["t"] == "CREATE" and e.get("qty") is not None}) or [1]
    worlds = list(_worlds(S, Q, Y, holders, qty_vals, full))
    if not worlds:
        return {"ok": False, "why": "no_world", "worlds": 0, "verdict": None}
    answers = set()
    n = 0
    for W in worlds:
        n += 1
        if n > max_worlds:
            return {"ok": False, "why": "too_many_worlds", "worlds": n, "verdict": None}
        if not _valid(W):
            continue
        a = _world_answer(W, Q)
        if isinstance(a, tuple):
            return {"ok": False, "why": "presupposition_fails_in_a_world", "worlds": n, "verdict": None}
        answers.add(str(a))
        if len(answers) > 1 and gold != nei:
            return {"ok": False, "why": "worlds_differ_but_A_known", "worlds": n, "verdict": "NEI"}
    if not answers:
        return {"ok": False, "why": "no_valid_world", "worlds": n, "verdict": None}
    if len(answers) > 1:
        return {"ok": gold == nei, "why": "ok" if gold == nei else "worlds_differ_but_A_known", "worlds": n,
                "verdict": "NEI"}
    only = answers.pop()
    if gold == nei:
        return {"ok": False, "why": "A_unknown_but_worlds_agree", "worlds": n, "verdict": only}
    return {"ok": only == str(gold), "why": "ok" if only == str(gold) else "decided_value_differs", "worlds": n,
            "verdict": only}


def _worlds(S, Q, Y, holders, qty_vals, full):
    base = copy.deepcopy(S)
    base.pop("_full", None)
    if S.get("gap_style") == "leading":
        yield from _leading_worlds(base, Q, Y, holders, qty_vals, full)
        return
    hidden = list(S.get("hidden") or [])
    if not hidden:
        yield base
        return
    by_n_full = {e["n"]: e for e in (full["entries"] if full else [])}
    slots = []
    if S["sampler"] == "S4":
        refs = sorted(S.get("gap_refs") or [])
        for r in refs:
            ns = sorted(e["n"] for e in full["entries"] if e["ref"] == r)
            slots.append(("notice", r, ns))
    else:
        for h in hidden:
            slots.append(("entry", h, [h]))
    alph = []
    for kind, key, ns in slots:
        first = ns[0]
        earlier = [e for e in S["entries"] if e["n"] < first]
        opts = [("orig", None)]
        opts.append(("inert", {"t": "CREATE", "item": FRESH_ITEM + str(first), "holder": holders[0],
                               "status": S["statuses"][0], "qty": (1 if S["has_qty"] else None)}))
        if kind == "entry":
            for e in _y_alphabet(S, Q, Y, holders, qty_vals, earlier):
                opts.append(("y", e))
        else:
            ys = _y_alphabet(S, Q, Y, holders, qty_vals, earlier)
            for e in ys:
                if e["t"] == "VOID":
                    continue
                opts.append(("y", e))
            # withdraw notice M: an earlier shown notice of voidable changes that withdraws nothing
            prev_refs = sorted({e["ref"] for e in earlier})
            for m in prev_refs:
                ch = [e for e in S["entries"] if e["ref"] == m]
                if ch and all(e["t"] in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE") for e in ch) \
                        and any(e.get("item") == Y for e in ch):
                    opts.append(("y", {"t": "WITHDRAW", "target_ref": m}))
        alph.append(opts)
    for combo in itertools.product(*alph):
        W = copy.deepcopy(base)
        ents = list(W["entries"])
        for (kind, key, ns), (tag, f) in zip(slots, combo):
            if tag == "orig":
                ents += [copy.deepcopy(by_n_full[n]) for n in ns]
                continue
            proto = by_n_full[ns[0]]
            e = dict(f)
            e["n"] = ns[0]
            e["date"] = proto["date"]
            e["time"] = proto.get("time")
            if S["sampler"] == "S4":
                e["ref"], e["k"] = proto["ref"], 1
            if e["t"] == "TRANSFER":
                e["sender"] = "__SENDER__"
            ents.append(e)
            # remaining numbers of a multi-change missing notice are left empty (one-change notices)
        ents.sort(key=lambda e: e["n"])
        W["entries"] = ents
        if S["sampler"] == "S4" and full:
            W["notices"] = full["notices"]
        _fix_senders(W)
        if W is None:
            continue
        yield W


def _fix_senders(W):
    """A missing transfer's sender is the true holder just before it in that world (rule 6, as T17 states), read on
    the whole world with every void and correction applied (they act retroactively)."""
    for e in W["entries"]:
        if e["t"] == "TRANSFER" and e["sender"] == "__SENDER__":
            e["sender"] = "ZZ-996"
            Wc = dict(W)
            Wc["world"] = "closed"
            Wc["gap_style"] = None
            Wc["gaps"] = []
            try:
                states, eff, E, _ = A.replay(Wc)
                idx = next(i for i, x in enumerate(eff) if x["n"] == e["n"])
                h = states[idx].holder.get(E.find(e["item"]))
            except Exception:
                h = None
            e["sender"] = h if isinstance(h, str) else "ZZ-998"
            if e["sender"] == e["receiver"]:
                e["receiver"] = FRESH_HOLDER if e["sender"] != FRESH_HOLDER else "ZZ-997"


def _leading_worlds(base, Q, Y, holders, qty_vals, full):
    """Leading extracts: the state before N0 of every item comes from the true world, except Y's, which ranges over
    the card's holders plus one fresh holder, the listed statuses, and the card's quantities plus one fresh value."""
    if not full:
        return
    n0 = base["n0"]
    pre = copy.deepcopy(full)
    if base["sampler"] == "S4":
        pre["entries"] = [e for e in full["entries"] if e["ref"] < n0]
    else:
        pre["entries"] = [e for e in full["entries"] if e["n"] < n0]
    states, eff, E, _ = A.replay(pre)
    st = states[-1]
    reg = []
    named = set()
    for e in base["entries"]:
        for k in ("item",):
            if e.get(k):
                named.add(e[k])
    for i in sorted(st.exists):
        reg.append([i, st.holder.get(i), st.status.get(i), st.qty.get(i) if base["has_qty"] else None])
    yi = next((r for r in reg if E.find(r[0]) == E.find(Y)), None)
    if yi is None:
        # Y is created at or after N0: its values come from shown entries only
        W = copy.deepcopy(base)
        W["register"] = {"items": reg, "docs": []}
        W["gap_style"] = None
        yield W
        return
    hs = holders + [FRESH_HOLDER] if Q["kind"] == "holder" else [yi[1]]
    ss = list(base["statuses"]) if Q["kind"] == "status" else [yi[2]]
    qs = ((sorted(set(qty_vals)) + [max(qty_vals) + 37]) if base["has_qty"] else [None]) if Q["kind"] == "qty" \
        else [yi[3]]
    for h in hs:
        for s in ss:
            for q in qs:
                W = copy.deepcopy(base)
                r2 = [list(r) for r in reg]
                for r in r2:
                    if E.find(r[0]) == E.find(Y):
                        r[1], r[2], r[3] = h, s, q
                W["register"] = {"items": r2, "docs": []}
                W["gap_style"] = None
                yield W
