"""F12 samplers S1, S2, S4, S6 (forward rows) and the question-form builders (G0 sections 1.2, 2, 4, 8).

A forward row is built target-first: the question form and its gold slot are drawn first (display-then-gold, XF01),
then a structure is built for the slot's outcome, solver A labels it, and the row is kept only when solver A's label
equals the slot (a mismatch is a rejection, never a relabel). The catalog is chosen from the pack's fixed tools after
every pack tool has been checked against the request: gold tool, functional distractors (near-misses), other candidate
tools and inert filler (own-pack tools sharing no action or object with the intent, or borrowed tools, R1-22).
"""
from __future__ import annotations

import copy
import datetime as dt
import random

import f12lex as L
import f12solve_a as A

BINS = {"S1": [(3, 5, .25), (6, 12, .25), (13, 25, .20), (26, 60, .30)],
        "S2": [(3, 5, .45), (6, 12, .45), (13, 25, .10)],
        "S4": [(3, 5, .45), (6, 12, .45), (13, 25, .10)],
        "S6": [(6, 12, .25), (13, 25, .45), (26, 60, .30)],
        "S5": [(3, 5, .45), (6, 12, .45), (13, 25, .10)]}
REL_FORMS = ["today", "tomorrow", "yesterday", "in {n} days", "{n} days ago", "in {w} weeks"]


class Reject(Exception):
    pass


def pick_bin(sampler, rng):
    x, acc = rng.random(), 0.0
    for lo, hi, w in BINS[sampler]:
        acc += w
        if x < acc:
            return lo, hi
    return BINS[sampler][-1][:2]


def draw_now(rng):
    d = dt.date(2026, 2, 1) + dt.timedelta(days=rng.randrange(0, 290))
    return f"{d.isoformat()} {rng.randrange(7, 20):02d}:{rng.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]):02d}"


def ts_before(now, rng, minutes):
    a = dt.datetime.fromisoformat(now.replace(" ", "T")) - dt.timedelta(minutes=minutes)
    return a.strftime("%Y-%m-%d %H:%M")


# ------------------------------------------------------------------------------------------------ values
def good_value(p, rng, now, avoid_boundary=False, abs_date=False):
    """A value text the param accepts (forward-row user form)."""
    t = p["type"]
    if t == "id":
        raise AssertionError("ids come from the pool")
    if t in ("integer", "decimal"):
        lo = p["min"][0] if p.get("min") else 0
        hi = p["max"][0] if p.get("max") else (lo + 60 if t == "integer" else lo + 60)
        lo_i, hi_i = (p["min"][1] if p.get("min") else True), (p["max"][1] if p.get("max") else True)
        if t == "integer":
            lo, hi = int(lo), int(hi)
            cands = list(range(lo + (0 if lo_i else 1), hi + (1 if hi_i else 0)))
            if avoid_boundary and len(cands) > 2:
                cands = cands[1:-1]
            if not cands:
                raise Reject("no int")
            v = rng.choice(cands)
            s = str(v)
        else:
            q = L.Decimal(1).scaleb(-p["places"])
            lo, hi = L.Decimal(str(lo)), L.Decimal(str(hi))
            steps = int((hi - lo) / q)
            if steps < 3:
                raise Reject("no dec")
            v = lo + q * rng.randrange(1, steps)
            s = L.fmt_dec(v)
        return s + (" " + p["unit"] if p.get("unit") else "")
    if t == "date":
        lo = dt.date.fromisoformat(p["min"][0]) if p.get("min") else dt.date(2026, 1, 1)
        hi = dt.date.fromisoformat(p["max"][0]) if p.get("max") else dt.date(2026, 12, 31)
        n = A.now_date(now)
        for _ in range(20):
            if rng.random() < 0.4 and not abs_date:
                f = rng.choice(REL_FORMS).format(n=rng.randrange(2, 20), w=rng.randrange(1, 4))
                d = A.rel_date(f, now)
                txt = f
            else:
                d = n + dt.timedelta(days=rng.randrange(-60, 120))
                txt = d.isoformat()
            if A.accept(p, txt, now)[0] and (not avoid_boundary or (d != lo and d != hi)):
                return txt
        raise Reject("no date")
    if t == "enum":
        return rng.choice(p["members"])
    if t == "string":
        return rng.choice(L.STRING_VALUES)
    if t == "boolean":
        return rng.choice(["yes", "no"])
    raise AssertionError(t)


def bad_value(p, rng, now):
    """A value of the right form family that the param does not accept (named; NG-34), or None."""
    t = p["type"]
    if t in ("integer", "decimal"):
        u = (" " + p["unit"]) if p.get("unit") else ""
        opts = []
        if p.get("max"):
            hv = L.Decimal(str(p["max"][0]))
            opts.append(L.fmt_dec(hv) if not p["max"][1] else L.fmt_dec(hv + (1 if t == "integer" else
                                                                            L.Decimal(1).scaleb(-p["places"]))))
            opts.append(L.fmt_dec(hv + (5 if t == "integer" else 3)))
        if p.get("min") and L.Decimal(str(p["min"][0])) > 0:
            lv = L.Decimal(str(p["min"][0]))
            if not p["min"][1]:
                opts.append(L.fmt_dec(lv))
        if t == "integer":
            base = int(L.Decimal(str(p["min"][0])) if p.get("min") else 1) + 1
            opts.append(f"{base}.5")
        else:
            lo = L.Decimal(str(p["min"][0])) if p.get("min") else L.Decimal(1)
            opts.append(L.fmt_dec(lo + L.Decimal(1).scaleb(-p["places"] - 1) * 3 + 1))
        opts = [o for o in opts if not A.accept(p, o + u, now)[0]]
        return (rng.choice(opts) + u) if opts else None
    if t == "date":
        opts = []
        if p.get("max"):
            hi = dt.date.fromisoformat(p["max"][0])
            opts.append((hi if not p["max"][1] else hi + dt.timedelta(days=rng.randrange(1, 9))).isoformat())
        if p.get("min"):
            lo = dt.date.fromisoformat(p["min"][0])
            opts.append((lo if not p["min"][1] else lo - dt.timedelta(days=rng.randrange(1, 9))).isoformat())
        opts = [o for o in opts if not A.accept(p, o, now)[0]]
        return rng.choice(opts) if opts else None
    if t == "enum":
        w = rng.choice(["provisional", "mixed", "other kind", "special", "pending review"])
        return None if w.lower() in [m.lower() for m in p["members"]] else w
    if t == "string":
        return "this text runs well past the forty character limit set here"
    if t == "id":
        return p["prefix"] + "".join(rng.choice("0123456789") for _ in range(p["n"] + 1))
    return None


# ------------------------------------------------------------------------------------------------ context
class Ctx:
    def __init__(self, pk, tools, card, rng, borrow):
        self.pk, self.tools, self.card, self.rng, self.borrow = pk, tools, card, rng, borrow
        self.sampler = card["sampler"]
        self.pol = card["pol"]


def inert_ok(t, a, o_word_set, cand_actions):
    return t["a"] != a and t["a"] not in cand_actions


def classify(S, res, intent_a, intent_o, cand_names):
    return A.near_misses(S, res)


def tool_copy(t):
    return copy.deepcopy(t)


def build_forward(ctx: Ctx, outcome: str, want: dict):
    """One forward structure aiming at `outcome` (CALL / ASK / UNABLE / ANSWER) with the form's extra needs.
    Returns (S, res, nm) or raises Reject."""
    pk, rng, pol, smp = ctx.pk, ctx.rng, ctx.pol, ctx.sampler
    ets = pk["etypes"]
    now = draw_now(rng)
    role = rng.choice(pk["roles"]) if pol["role"] else None
    # ---- request kind and capability
    kind = want.get("kind")
    if kind is None:
        if outcome == "ANSWER":
            kind = "catalog" if (rng.random() < 0.2 and want.get("catalog_ok", True)) else "info"
        else:
            kind = "info" if (rng.random() < 0.22 and want.get("info_ok", True)) else "action"
    o = rng.randrange(2)
    e = ets[o]
    if kind == "info":
        a = "look up"
    else:
        acts = [x for x in pk["actions"] if any(t["a"] == x and t["o"] == o for t in ctx.tools)]
        if want.get("cluster"):
            vc = {}
            for t in ctx.tools:
                if t["vid"] != "base" and t["vid"] != "provider" and t["o"] == o:
                    vc[t["a"]] = vc.get(t["a"], 0) + 1
            acts = [x for x in acts if vc.get(x, 0) >= 3] or acts
        if want.get("chain"):
            acts = [x for x in acts if x in L.OTHER_ID_ACTIONS]
        if not acts:
            raise Reject("no action")
        a = rng.choice(acts)
    cand_all = [t for t in ctx.tools if t["a"] == a and t["o"] == o and t["vid"] != "provider"]
    if kind != "catalog" and not cand_all and outcome != "UNABLE":
        raise Reject("no candidates")
    # ---- target entity and reference
    pairs = e["lookalikes"]
    use_look = rng.random() < want.get("p_look", 0.25)
    if use_look and pairs:
        pr = rng.choice(pairs)
        eid, look_id = (pr[0], pr[1]) if rng.random() < 0.5 else (pr[1], pr[0])
    else:
        flat = {x for p in pairs for x in p}
        eid = rng.choice([x for x in e["ids"] if x not in flat] or e["ids"])
        look_id = None
    names = list(e["names"])
    rng.shuffle(names)
    ename, look_name = names[0], names[1]
    by_name = kind != "catalog" and rng.random() < want.get("p_name", 0.25) and smp != "S5x"
    if want.get("chain"):
        by_name = False
    ref = None if kind == "catalog" else (["name", ename] if by_name else ["id", eid])
    if kind == "catalog":
        cue = "catalog"
    elif kind == "info":
        cue = rng.choice(["info", "polite"])
    else:
        cue = rng.choice(["plain", "polite", "catalog"]) if want.get("cue_ok", True) else rng.choice(["plain",
                                                                                                    "polite"])
    field = None
    if kind == "info":
        fpool = [k for k, s in pk["params"].items() if s["et"] == o and s["kind"] == "set"
                 and s["type"] in ("integer", "decimal", "date", "enum", "string", "boolean")]
        field = rng.choice(fpool)
    req = {"t": "req", "kind": kind, "cue": cue, "a": a, "o": o, "ref": ref, "field": field}
    st = [req]
    records, stored, conv_pre = [], [], []
    # ---- the main tool and value plan
    vals_plan = {}
    T0 = rng.choice(cand_all) if cand_all else None
    if want.get("chain"):
        bases = [t for t in cand_all if t["vid"] == "base"]
        if not bases:
            raise Reject("no chain base")
        T0 = bases[0]
    if T0 is not None and want.get("main_base"):
        b = [t for t in cand_all if t["vid"] == "base"]
        T0 = b[0] if b else T0
    params = {}
    for t in cand_all:
        for p in t["params"]:
            params.setdefault(p["name"], []).append(p)
    problem = None
    if kind == "action" and T0 is not None:
        need = [p for p in T0["params"] if p["required"]]
        opt = [p for p in T0["params"] if not p["required"]]
        if outcome == "ASK" or (outcome == "UNABLE" and want.get("unable_reason") == "value"):
            pool = [p for p in need if p["name"] != e["idkey"]] if (not by_name or want.get("no_id_problem")) \
                else need
            if want.get("ask_param"):
                pool = [p for p in need if p["name"] == want["ask_param"]]
            if not pool:
                raise Reject("no problem param")
            pp = rng.choice(pool)
            if outcome == "UNABLE":
                kindp = "bad"
            elif want.get("ask_kind"):
                kindp = want["ask_kind"]
            else:
                kindp = rng.choice(["absent", "absent", "unclear", "bad"] if pol["invalid"] == "A"
                                   else ["absent", "absent", "unclear"])
            if pp["type"] in ("string", "boolean") and kindp == "unclear":
                kindp = "absent"
            if pp["name"] == e["idkey"]:
                kindp = "absent" if kindp != "unclear" else "unclear"
            problem = (pp["name"], kindp)
        for p in need:
            if p["name"] == e["idkey"]:
                continue
            if problem and p["name"] == problem[0]:
                continue
            vals_plan[p["name"]] = ("good", p)
        for p in opt:
            if want.get("min_vals") or rng.random() < 0.35:  # gen:F12 after build 22: min_vals (yes/no pair bases)
                vals_plan[p["name"]] = ("good", p)
        if want.get("chain") and problem is None:
            other = ets[1 - o]["idkey"]
            vals_plan.pop(other, None)
            problem = (other, "chainabsent")
    # ---- user value statements
    for n, (how, p) in list(vals_plan.items()):
        if how == "good":
            if p["type"] == "id":
                v = rng.choice(ets[pk["params"][n]["et"]]["ids"])
            else:
                # card-free intent (G0 8 card_free_ok, repair r3): never a boundary value or a relative date
                v = good_value(p, rng, now, avoid_boundary=(rng.random() < 0.5) or bool(want.get("cf")),
                               abs_date=bool(want.get("cf")))
            # accepted by every candidate tool having it (else it is a decisive value problem)
            if not all(A.accept(q, v, now)[0] for q in params.get(n, [])):
                if want.get("strict_accept", True):
                    raise Reject("value not accepted everywhere")
            st.append({"t": "val", "p": n, "v": v, "alts": None})
    if problem:
        n, kp = problem
        p = next(q for q in T0["params"] if q["name"] == n)
        if kp == "unclear" and n != e["idkey"]:
            v1 = good_value(p, rng, now)
            v2 = good_value(p, rng, now)
            if v1 == v2 or not all(A.accept(q, v, now)[0] for q in params[n] for v in (v1, v2)):
                raise Reject("open choice")
            st.append({"t": "val", "p": n, "v": None, "alts": [v1, v2]})
        elif kp == "bad":
            v = bad_value(p, rng, now)
            if v is None or any(A.accept(q, v, now)[0] for q in params[n]):
                raise Reject("bad value")
            st.append({"t": "val", "p": n, "v": v, "alts": None})
    # gen:F12 after build 22 (f12build.YS): a yes/no pair base whose label-flip twin removes a value states >= 2 values
    if want.get("min_vals") and sum(1 for x in st if x["t"] == "val") < want["min_vals"]:
        raise Reject("min vals")
    # unnamed values where NG-19 allows (only accepted, non-string values)
    for s in st:
        if s["t"] == "val" and s["v"] and not s.get("alts") and rng.random() < want.get("p_unnamed", 0.5):
            p0 = s["p"]
            pt = params.get(p0, [{}])[0].get("type")
            if pt in ("string", "boolean", None):
                continue
            ok = all(A.accept(q, s["v"], now)[0] for q in params[p0])
            names = {nm for nm, ds in params.items() if any(A.form_ok(d, s["v"], now) for d in ds)}
            if ok and names == {p0} and all(A.form_ok(d, s["v"], now) for d in params[p0]):
                s["p"] = None
    # ---- qualifier, records (target and look-alike), status
    scoped = any(t["scope"] is not None for t in ctx.tools if t["o"] == o)
    dv = pk["dim"]["values"]
    qual = None
    if kind != "catalog" and not want.get("cf") and (scoped or rng.random() < 0.3):
        qual = rng.choice(dv)
        if want.get("qual_in"):
            qual = want["qual_in"]
    has_pre = any(t["pre"] is not None for t in ctx.tools if t["o"] == o)
    rec_needed = kind != "catalog" and (has_pre or by_name and rng.random() < 0.8 or kind == "info"
                                        and outcome == "ANSWER" and rng.random() < 0.6 or rng.random() < 0.3)
    if want.get("no_records"):
        rec_needed = False
    status = rng.choice(pk["status"]) if rec_needed else None
    qual_in_record = qual is not None and rec_needed and rng.random() < 0.4
    if qual is not None and kind == "info" and not qual_in_record:
        # NG-55 / R5-14 (fixA pass 1): an info question's request states no qualifier; a restricted dimension's value
        # comes from a record about e (NG-11), and an unrestricted one is simply not stated
        if not scoped:
            qual = None
        elif want.get("no_records"):
            raise Reject("NG-55")
        else:
            if not rec_needed:
                rec_needed = True
                status = rng.choice(pk["status"])
            qual_in_record = True
    if qual is not None and not qual_in_record:
        st.append({"t": "qual", "v": qual})
    answer_src = None
    if kind == "info" and outcome == "ANSWER":
        answer_src = want.get("answer_src") or rng.choice(["record", "record", "stored", "user"] if smp in (
            "S2", "S4", "S6") else ["record", "record", "user"])
        if answer_src == "record" and not rec_needed:
            rec_needed = True
            status = rng.choice(pk["status"])
        if answer_src == "stored" and smp not in ("S2", "S4", "S6"):
            answer_src = "record"
    fval = None
    if kind == "info":
        fp = L._param(pk, field, L.rng_for("f", pk["id"], field), True)
        fval = good_value(fp, rng, now) if fp["type"] != "date" else (
            A.now_date(now) - dt.timedelta(days=rng.randrange(1, 90))).isoformat()
        if fp["type"] == "date":
            pass
    if rec_needed:
        f = [[e["idkey"], eid], [e["namekey"], ename], ["status", status]]
        if qual_in_record:
            f.append([pk["dim"]["key"], qual])
        if kind == "info":
            if answer_src == "record":
                f.append([field, fval])
            elif rng.random() < 0.3:
                f.append([field, rng.choice(A.MARK_UNKNOWN)])
        rng.shuffle(f)
        records.append({"fields": f})
    if look_id and kind != "catalog" and (want.get("look_rec") or rng.random() < 0.8):
        lf = [[e["idkey"], look_id], [e["namekey"], look_name], ["status", rng.choice(pk["status"])]]
        if kind == "info":
            lf.append([field, good_value(L._param(pk, field, L.rng_for("f", pk["id"], field), True), rng, now)
                       if pk["params"][field]["type"] != "date" else
                       (A.now_date(now) - dt.timedelta(days=rng.randrange(1, 90))).isoformat()])
        if qual_in_record:
            lf.append([pk["dim"]["key"], rng.choice(dv)])
        records.append({"fields": lf})
    if want.get("two_sources") and by_name:
        # two records carrying the same name with different IDs: the target ID is unclear (SEM-43, NG-28)
        other = rng.choice([x for x in e["ids"] if x != eid])
        rf = [[e["idkey"], other], [e["namekey"], ename]]
        if has_pre:
            rf.append(["status", status])
        if qual_in_record:
            rf.append([pk["dim"]["key"], qual])
        records.append({"fields": rf})
    rng.shuffle(records)
    # ---- stored results (S2, S4, S6: 40-60%, flat over outcomes)
    if smp in ("S2", "S4", "S6") and kind != "catalog" and not want.get("no_stored") and (
            rng.random() < want.get("p_stored", 0.5) or answer_src == "stored"):
        ts_age = rng.randrange(5, 600)
        fresh = pol["fresh"]
        if answer_src == "stored" and fresh is not None:
            ts_age = rng.randrange(1, fresh + 1) if rng.random() < 0.85 else fresh
        if kind == "info" and answer_src != "stored" and outcome != "ANSWER" and fresh is not None \
                and rng.random() < 0.6:
            ts_age = fresh + rng.randrange(1, 300)
        ts = ts_before(now, rng, ts_age)
        if ts[:10] != now[:10] and ts_age < 24 * 60:
            ts = ts_before(now, rng, 24 * 60 + rng.randrange(30, 900))  # NG-05: no stamp within 24 h on another date
        sid = eid if (answer_src == "stored" or rng.random() < 0.7) else (look_id or eid)
        sf = [[e["idkey"], sid]]
        if by_name and sid == eid:
            sf.append([e["namekey"], ename])
        if kind == "info" and (answer_src == "stored" or (outcome != "ANSWER" and (fresh is not None and
                                                                                    A.stamp_age(now, ts) > fresh))):
            sf.append([field, fval])
        stored.append({"tool": L.tname(pk, f"look_up_{e['key']}"), "ts": ts, "fields": sf})
    if kind == "info" and answer_src == "user":
        st.append({"t": "val", "p": field, "v": fval, "alts": None})
    conv = [{"who": "user", "ts": now[11:], "st": st}]
    S = {"pol": dict(pol), "now": now, "role": role, "tools": [], "records": records, "conv": conv,
         "stored": stored, "call": None}
    # ---- S4 shapes: earlier fact statement, continuation, correction, tool-result turns
    if smp == "S4":
        S = _s4_shape(ctx, S, kind, e, eid, ename, by_name, outcome, problem, want, rng)
    # ---- check every pack tool against this request
    allt = [tool_copy(t) for t in ctx.tools]
    S["tools"] = allt
    res = A.solve(S, pk, checks_only=True)
    return S, res, {"T0": T0["name"] if T0 else None, "problem": problem, "kind": kind, "a": a, "o": o,
                    "eid": eid, "by_name": by_name}


def _s4_shape(ctx, S, kind, e, eid, ename, by_name, outcome, problem, want, rng):
    """Dialogue: 2-8 turns; earlier fact statement, assistant question + continuation, corrections, tool results."""
    conv = S["conv"]
    st = conv[0]["st"]
    req = st[0]
    turns = []
    now = S["now"]
    t0 = dt.datetime.fromisoformat(now.replace(" ", "T"))

    def hm(mins):
        return (t0 - dt.timedelta(minutes=mins)).strftime("%H:%M")
    # earlier fact statement about the target (gives its ID when the request names it by name)
    if by_name and rng.random() < 0.5 and not want.get("two_sources"):
        turns.append({"who": "user", "ts": hm(30), "st": [{"t": "fact", "name": ename, "p": e["idkey"], "v": eid}]})
        turns.append({"who": "assistant", "ts": hm(29), "ask": None})
        S["records"] = [r for r in S["records"] if dict(r["fields"]).get(e["namekey"]) != ename
                        or dict(r["fields"]).get(e["idkey"]) == eid]
    # a tool-result turn about the target (ID only, plus asked field on info rows when it is not the answer)
    if rng.random() < 0.35 and kind != "catalog":
        f = [[e["idkey"], eid]]
        if by_name:
            f.append([e["namekey"], ename])
        turns.append({"who": "tool", "ts": (t0 - dt.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M"),
                      "tool": L.tname(ctx.pk, f"look_up_{e['key']}"), "fields": f})
    # continuation: the request first, then the assistant asks for one value, the user answers it
    vals = [s for s in st if s["t"] == "val" and s["p"] and s["v"] and not s.get("alts")]
    if kind == "action" and vals and rng.random() < 0.3:
        s = rng.choice(vals)
        st.remove(s)
        turns.append({"who": "user", "ts": hm(6), "st": st})
        turns.append({"who": "assistant", "ts": hm(5), "ask": s["p"]})
        last = {"who": "user", "ts": hm(0), "st": [{"t": "cont", "v": s["v"]}]}
        turns.append(last)
    elif kind == "action" and vals and rng.random() < (0.9 if want.get("corr_v") else 0.35):
        # correction across turns: an earlier statement in the current request is replaced by a later one
        s = rng.choice(vals)
        p = None
        for t in ctx.tools:
            for q in t["params"]:
                if q["name"] == s["p"]:
                    p = q
        try:
            old = good_value(p, rng, now) if p and p["type"] not in ("id",) else None
        except Reject:
            old = None
        if old and old != s["v"]:
            i = st.index(s)
            st.insert(i, {"t": "val", "p": s["p"], "v": old, "alts": None})
            st.insert(i + 1, {"t": "corr"})
        turns.append({"who": "user", "ts": hm(0), "st": st})
    else:
        turns.append({"who": "user", "ts": hm(0), "st": st})
    conv[:] = turns
    return S


def choose_catalog(ctx, S, res, info, outcome, want):
    """Pick listed tools from the checked pack tools: gold / fitting tools for the outcome, near-misses, filler."""
    rng = ctx.rng
    pk = ctx.pk
    by = {t["name"]: t for t in S["tools"]}
    ck = res["checks"]
    a, o, kind = info["a"], info["o"], info["kind"]
    tools_all = S["tools"]
    if want.get("cf"):
        # card-free intent (section 8 card_free_ok): no precondition, scope or returns tool is ever listed
        tools_all = [t for t in S["tools"] if t["pre"] is None and t["scope"] is None and not t["returns"]]
    cand = [t for t in tools_all if t["a"] == a and t["o"] == o and t["vid"] != "provider"]
    fit = [t for t in cand if ck[t["name"]]["fit"]]
    comp = [t for t in fit if ck[t["name"]]["complete"]]
    # near-miss pool on the full set (component failing exactly one)
    nm_pool = []
    for t in tools_all:
        f = ck[t["name"]]["fails"]
        if t["vid"] == "provider":
            continue
        if len(f) == 1 and f[0] != "capability":
            nm_pool.append(t)
    inert = [t for t in tools_all if t["a"] != a and t["o"] != o and t["vid"] != "provider"
             and not t["returns"]]
    listed = []
    gold = None
    if kind == "catalog":
        pass
    elif outcome == "CALL" and want.get("chain"):
        ets = pk["etypes"]
        T0 = by.get(info["T0"])
        P = L.by_dname(S["tools"], f"look_up_{ets[1 - o]['key']}_for_{ets[o]['key']}")
        if T0 is None or P is None or not ck[T0["name"]]["fit"]:
            raise Reject("chain tools")
        listed += [T0, P]
        gold = P
    elif outcome == "CALL":
        # NG-29 (R1-04, fixA pass 1): the called tool and every tie member have a param for every stated value
        stated = stated_params(S, res, pk)
        comp = [t for t in comp if stated <= {p["name"] for p in t["params"]}]
        if not comp:
            raise Reject("no complete tool")
        if want.get("tie") and len(comp) >= 2:
            pair = None
            for x in comp:
                for y in comp:
                    if x is not y and (x["cost"] != y["cost"] or (x["pref"] != y["pref"])):
                        pair = (x, y)
                        break
                if pair:
                    break
            if not pair:
                raise Reject("no tie pair")
            listed += list(pair)
            gold = min(pair, key=lambda t: (t["cost"], not t["pref"]))
        else:
            gold = rng.choice(comp)
            listed.append(gold)
    elif outcome == "ASK":
        if not fit or comp:
            if not fit:
                raise Reject("ASK: no fitting tool")
        inc = [t for t in fit if not ck[t["name"]]["complete"]]
        if not inc:
            raise Reject("ASK: no incomplete fitting")
        nfit = 1 if want.get("one_fit") else rng.randint(1, min(2, len(inc)))
        listed += rng.sample(inc, nfit)
    elif outcome == "UNABLE":
        pass
    elif outcome == "ANSWER" and kind == "info":
        # a read tool may or may not be listed (on card-free rows none is)
        if not want.get("no_read") and rng.random() < 0.6:
            rt = [t for t in cand if ck[t["name"]]["fit"]]
            if rt:
                listed.append(rng.choice(rt))
    lnames = {t["name"] for t in listed}
    # near-misses: never a complete fitting tool on CALL rows (would tie); never a fitting tool on ASK rows
    nms = [t for t in nm_pool if t["name"] not in lnames]
    if outcome in ("UNABLE",):
        nms = [t for t in nms if not ck[t["name"]]["fit"]]
    nms = [t for t in nms if not ck[t["name"]]["fit"]]
    rng.shuffle(nms)
    if want.get("nm_prio"):  # repair r4 (G7 tool words): over-gold tools of the card first, shuffle breaks ties
        pr = want["nm_prio"]
        nms.sort(key=lambda t: -pr.get(t["name"], 0.0))
    need_nm = want.get("need_nm", 1)
    lo, hi = want.get("bin") or pick_bin(ctx.sampler, rng)
    n_target = rng.randint(lo, hi)
    if len(nms) < need_nm:
        raise Reject(f"near-miss supply {len(nms)} < {need_nm}")
    k_nm = max(need_nm, min(len(nms), rng.randint(1, max(1, n_target - len(listed) - 1))))
    if want.get("nm_exact") is not None:
        k_nm = want["nm_exact"]
    chosen_nm = nms[:k_nm]
    listed += chosen_nm
    # CALL rows: optionally an extra fitting-but-incomplete candidate (SEM-20)
    if outcome == "CALL" and not want.get("one_fit"):
        inc = [t for t in fit if not ck[t["name"]]["complete"] and t["name"] not in {x["name"] for x in listed}]
        if inc and rng.random() < 0.3:
            listed.append(rng.choice(inc))
    # chain providers on chain cards: listed only on rows built for them (else excluded)
    # filler: own inert tools then borrowed
    names_now = {t["name"] for t in listed}
    fill = [t for t in inert if t["name"] not in names_now]
    rng.shuffle(fill)
    while len(listed) < n_target and fill:
        listed.append(fill.pop())
    if len(listed) < n_target:
        words = {x["word"] for x in pk["etypes"]} | {x["plural"] for x in pk["etypes"]}
        acts = {t["a"] for t in listed} | {a}
        bor = [b for b in ctx.borrow if b["a"] not in acts and b["a"] != "look up"
               and not any(w in b["oword"] or b["oword"] in w for w in words)]
        rng.shuffle(bor)
        seen_src = []
        for b in bor:
            if len(listed) >= n_target:
                break
            if b["src"] not in seen_src:
                if len(seen_src) >= 3:
                    continue
                seen_src.append(b["src"])
            if b["name"] in {t["name"] for t in listed}:
                continue
            if any(b["oword"] in x.get("oword", "") or x.get("oword", "") in b["oword"] for x in listed
                   if x.get("borrowed")):
                if b["oword"] not in [x.get("oword") for x in listed if x.get("borrowed")]:
                    continue
            listed.append(b)
    if len(listed) < max(3, lo):
        raise Reject("catalog too small")
    rng.shuffle(listed)
    return listed, gold, chosen_nm


def finalize(ctx, S, listed):
    S2 = copy.deepcopy(S)
    S2["tools"] = [copy.deepcopy(t) for t in listed]
    res = A.solve(S2, ctx.pk)
    nm = A.near_misses(S2, res)
    return S2, res, nm


# ------------------------------------------------------------------ not-generated structures (G0 10.1; fixA pass 1)
def stated_params(S, res, pk):
    """Params the user stated a value for in the current request (section 3 step 0): named values, continuations,
    unnamed values as step 1 attributes them, and e's ID named next to its entity word. On an info question a
    statement of the asked field f fills no param (it is a fact about e)."""
    req, cur, et = A.target_info(S, pk)
    info = A.kind_of(req) == "info"
    conv = S["conv"]
    out = set()
    for i in cur:
        for st in conv[i]["st"]:
            if st["t"] == "val" and st.get("p") and not (info and st["p"] == req.get("field")):
                out.add(st["p"])
            elif st["t"] == "cont" and i > 0 and conv[i - 1].get("ask"):
                out.add(conv[i - 1]["ask"])
    out |= {p for p, s in (res.get("src") or {}).items() if s in ("stated", "current", "reldate", "continuation")}
    if req.get("ref") and req["ref"][0] == "id" and et is not None and et["idkey"] in (res.get("vals") or {}):
        out.add(et["idkey"])
    if info:
        out.discard(req.get("field"))
    return out


def ng29_bad(S, res, pk, names=None):
    """NG-29 (R1-04): a candidate tool that would be complete (the called tool, or a tie member) has no parameter for
    a param value the user stated for the request. `names` overrides the complete tools checked."""
    if names is None:
        if res.get("outcome") != "CALL" or res.get("chain") or not res.get("tool"):
            return False
        names = res.get("tie") or [res["tool"]]
    stated = stated_params(S, res, pk)
    by = {t["name"]: t for t in S["tools"]}
    return any(not stated <= {p["name"] for p in by[n]["params"]} for n in names if n in by)


def ng55_bad(S, pk):
    """NG-55 (R5-14): an info question whose current request states anything besides f's word, e's ID or name and,
    optionally, f's own value (a qualifier, a param value, ...)."""
    req, cur, et = A.target_info(S, pk)
    if A.kind_of(req) != "info":
        return False
    for i in cur:
        for st in S["conv"][i]["st"]:
            if st["t"] == "qual":
                return True
            if st["t"] == "val" and st.get("p") != req.get("field"):
                return True
    return False
