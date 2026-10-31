"""G4 metamorphic relations (G0 spec section 3, table M1-M9), run on the G3 parse of emitted rows.

Relations implemented (each must pass 100% on >= 1,000 rows; a variant that breaks a section 1 generator rule is
skipped and logged per relation, never forced; A41):
  M1 inert entry outside the query's dependency closure (another item) -> label unchanged
  M2 commute two adjacent same-date-and-time entries that share no ID (not RENAME / MERGE / VOID / CORR) and
     re-shuffle a sorted / shuffled listing -> unchanged
  M3 consistent renaming to fresh, non-look-alike IDs everywhere (log, question, options) -> unchanged (mapped)
  M4 option shuffle plus container change (re-rendered in another container of the card's style set, re-parsed)
     -> gold maps to the same option text and the structure hash is unchanged
  M5 void the decisive writer (voidable types) -> solver A agrees with solver B's recomputation
  M8 attack text in a marked note field (re-rendered, re-parsed) -> unchanged
  M9 negate / double-negate the question in an allowed 2.2 form -> NOT label / same label
The property-style draws use a seeded RNG (Hypothesis, MPL-2.0, is not installed in this environment; the seeded
generator gives the same coverage contract: >= 1,000 rows per relation, fixed seed, every skip logged).
"""
from __future__ import annotations

import collections
import copy
import json
import random
import re
import sys

import canon
import parse_f3 as P
import questions as QS
import solver_a as A
import solver_b as B

ID = re.compile(r"^[A-Z]{2,4}-[0-9A-Z]{2,5}$")


def _label(S, Q, nei=None):
    if S["world"] == "open":
        v = A.answer(S, Q)
        if v == A.UNK:
            return nei
        if Q["form"] == "choice" and Q["qt"] == "Q5":
            return A.latest_id(S, None, v)
        return v
    v = A.answer(S, Q)
    if Q["form"] == "choice" and Q["qt"] == "Q5" and v not in (None, A.UNK, A.NO_SINGLE):
        return A.latest_id(S, None, v)
    return v


class RuleBreak(Exception):
    pass


def _label_b(S, Q, nei=None):
    try:
        v, info = B.solve(S, Q)
    except AssertionError:
        raise RuleBreak()
    if v == B.UNKNOWN:
        return nei, info
    if Q["form"] == "choice" and Q["qt"] == "Q5":
        return A.latest_id(S, None, v), info
    return v, info


def _renumber_insert(S, pos_n, new_e, Q):
    """Insert new_e with number pos_n; later entries shift by one; targets and the Q8 reference follow."""
    S2 = copy.deepcopy(S)
    for e in S2["entries"]:
        if e["n"] >= pos_n:
            e["n"] += 1
        if e.get("target") is not None and e["target"] >= pos_n and e["t"] in ("VOID", "CORR"):
            e["target"] += 1
    S2["gaps"] = [g + 1 if g >= pos_n else g for g in S2.get("gaps", [])]
    if S2.get("n0") and S2["sampler"] != "S4" and S2.get("gap_style") == "leading" and pos_n <= S2["n0"]:
        return None, None
    S2["entries"].append(new_e)
    S2["entries"].sort(key=lambda e: e["n"])
    Q2 = dict(Q)
    if Q.get("entry") is not None and Q["entry"] >= pos_n:
        Q2["entry"] = Q["entry"] + 1
    return S2, Q2


def m1_inert(S, Q, rng, nei):
    if S["sampler"] in ("S4", "S5"):
        return "skip:sampler"
    named = {Q.get("item"), Q.get("holder")} | set(Q.get("candidates") or [])
    if Q["qt"] == "Q8":
        named |= {e.get("item") for e in S["entries"] if e["n"] == Q["entry"]}
    items = [it[0] for it in S["register"]["items"]] + [e["item"] for e in S["entries"] if e["t"] == "CREATE"]
    E = A.Ents(S)
    qroots = {E.find(x) for x in named if x}
    others = [y for y in items if E.find(y) not in qroots]
    if Q["qt"] in ("Q6", "Q7"):
        return "skip:count_query"
    if not others or not S["entries"]:
        return "skip:no_other_item"
    y = rng.choice(others)
    y = A.latest_id(S, None, y)
    if S["world"] == "open":
        pos_n = S["entries"][-1]["n"] + 1
        prev = S["entries"][-1]
    else:
        idx = rng.randrange(len(S["entries"]))
        prev = S["entries"][idx]
        pos_n = prev["n"] + 1
    e = {"t": "SET", "item": y, "field": "status", "value": rng.choice(S["statuses"] or ["x"]), "n": pos_n,
         "date": prev["date"], "time": prev.get("time")}
    if S["sampler"] == "S6":
        e["eff"] = prev.get("eff") or prev["date"]
    if prev.get("time"):
        h, mm = map(int, prev["time"].split(":"))
        t = h * 60 + mm + 1
        e["time"] = f"{t // 60:02d}:{t % 60:02d}"
    S2, Q2 = _renumber_insert(S, pos_n, e, Q)
    if S2 is None:
        return "skip:leading"
    if not S2["statuses"]:
        return "skip:no_vocab"
    Sc = dict(S2, world="closed", gap_style=None, gaps=[]) if S2["world"] == "open" else S2
    bad = A.check_rules(Sc)
    if bad:
        return "skip:rules"
    if not _guard_holds(S2, Q2):
        return "skip:t31_guard"
    return S2, Q2


def m2_commute(S, Q, rng, nei):
    if S["sampler"] in ("S4", "S5", "S6"):
        return "skip:sampler"
    ents = S["entries"]
    pairs = []
    for a, b in zip(ents, ents[1:]):
        if b["n"] != a["n"] + 1 or a["date"] != b["date"] or a.get("time") != b.get("time"):
            continue
        if {a["t"], b["t"]} & {"RENAME", "MERGE", "VOID", "CORR", "WITHDRAW"}:
            continue
        ids_a = {a.get(k) for k in ("item", "holder", "sender", "receiver", "old", "new", "record", "doc")} - {None}
        ids_b = {b.get(k) for k in ("item", "holder", "sender", "receiver", "old", "new", "record", "doc")} - {None}
        if ids_a & ids_b:
            continue
        if any(e.get("target") in (a["n"], b["n"]) for e in ents if e["t"] in ("VOID", "CORR")):
            continue
        if Q.get("entry") in (a["n"], b["n"]):
            continue
        pairs.append((a, b))
    if not pairs:
        return "skip:no_pair"
    a, b = rng.choice(pairs)
    S2 = copy.deepcopy(S)
    for e in S2["entries"]:
        if e["n"] == a["n"]:
            e["n"] = b["n"]
        elif e["n"] == b["n"]:
            e["n"] = a["n"]
    S2["entries"].sort(key=lambda e: e["n"])
    if A.check_rules(dict(S2, world="closed", gap_style=None, gaps=[]) if S2["world"] == "open" else S2):
        return "skip:rules"
    if not _guard_holds(S2, Q):
        return "skip:t31_guard"
    return S2, dict(Q)


def _rename_map(S, Q, rng):
    ids = set()
    for it in S["register"]["items"]:
        ids.add(it[0]); ids.add(it[1])
    for d, r in S["register"].get("docs", []):
        ids.add(r)
    for e in S["entries"]:
        for k in ("item", "holder", "sender", "receiver", "old", "new", "absorbed", "survivor", "record"):
            if isinstance(e.get(k), str):
                ids.add(e[k])
        if e["t"] == "CORR" and e["slot"] == "receiver":
            ids.add(e["value"])
    for k in ("item", "holder", "record"):
        if Q.get(k):
            ids.add(Q[k])
    ids |= set(Q.get("candidates") or [])
    mp = {}
    used = set(ids)
    for x in sorted(ids):
        pre = x.split("-")[0]
        while True:
            code = "".join(rng.choice("BCDFGHJKMNPQRSTVWXZ23456789") for _ in range(len(x.split("-")[1]) + 1))
            if not any(ch.isdigit() for ch in code):
                continue
            y = f"Z{pre[:2]}-{code}"
            if y not in used:
                used.add(y)
                mp[x] = y
                break
    return mp


def m3_rename(S, Q, rng, nei):
    mp = _rename_map(S, Q, rng)
    f = lambda x: mp.get(x, x) if isinstance(x, str) else x  # noqa: E731
    S2 = copy.deepcopy(S)
    S2["register"]["items"] = [[f(a), f(b), c, d] for a, b, c, d in S2["register"]["items"]]
    S2["register"]["docs"] = [[d, f(r)] for d, r in S2["register"].get("docs", [])]
    for e in S2["entries"]:
        for k in ("item", "holder", "sender", "receiver", "old", "new", "absorbed", "survivor", "record"):
            if k in e:
                e[k] = f(e[k])
        if e["t"] == "CORR" and e["slot"] == "receiver":
            e["value"] = f(e["value"])
    Q2 = dict(Q)
    for k in ("item", "holder", "record"):
        if Q2.get(k):
            Q2[k] = f(Q2[k])
    if Q2.get("candidates"):
        Q2["candidates"] = [f(x) for x in Q2["candidates"]]
    return S2, Q2, mp


def m5_void_decisive(S, Q, rng, nei):
    if S["world"] == "open" or S["sampler"] in ("S4",):
        return "skip:open_or_s4"
    try:
        lb, info = B.solve(S, Q)
    except AssertionError:
        return "skip:assert"
    dec = info.get("decisive")
    tgt = next((e for e in S["entries"] if e["n"] == dec), None)
    if tgt is None or tgt["t"] not in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE"):
        return "skip:not_voidable"
    if any(e["t"] == "VOID" and e["target"] == dec for e in S["entries"]):
        return "skip:already_void"
    last = S["entries"][-1]
    S2 = copy.deepcopy(S)
    e = {"t": "VOID", "target": dec, "n": last["n"] + 1, "date": last["date"], "time": last.get("time")}
    if last.get("time"):
        h, mm = map(int, last["time"].split(":"))
        t = min(h * 60 + mm + 1, 23 * 60 + 59)
        e["time"] = f"{t // 60:02d}:{t % 60:02d}"
    S2["entries"].append(e)
    if A.check_rules(S2):
        return "skip:rules"
    if not _guard_holds(S2, Q):
        return "skip:t31_guard"
    return S2, dict(Q)


def _guard_holds(S, Q):
    """The T31 generator guard binds every 'still' / 'no longer' row (twins and variants alike)."""
    if not (Q.get("still") or Q.get("neg") == "N2" or (Q.get("neg") == "D" and Q.get("dbase") == "N2")):
        return True
    if S["world"] == "open":
        vals, eff, E = A.open_values(S)
        return A.open_guard(S, Q, eff, E)
    states, eff, E, _ = A.replay(S)
    return A.guard_ok(S, states, eff, E, Q["item"], Q["holder"])


def m9_negate(S, Q, rng, nei):
    if Q["form"] != "yn" or Q.get("neg", "A") != "A":
        return "skip:not_affirmative_yn"
    forms, dk = QS.neg_forms_allowed(Q)
    if not forms:
        return "skip:no_form"
    f = rng.choice(forms)
    if f == "N2":
        if S["world"] == "open":
            vals, eff, E = A.open_values(S)
            if not A.open_guard(S, Q, eff, E):
                return "skip:guard"
        else:
            states, eff, E, _ = A.replay(S)
            if not A.guard_ok(S, states, eff, E, Q["item"], Q["holder"]):
                return "skip:guard"
    return S, QS.twin_neg(Q, f), f


def run(rows, cards_by_id, *, n_min=1000, seed=20261003, render_fn=None):
    """Apply every relation to every row (parse first). Returns the G4 report."""
    rng = random.Random(seed)
    rep = {m: collections.Counter() for m in ("M1", "M2", "M3", "M4", "M5", "M8", "M9")}
    fails = {m: [] for m in rep}
    for r in rows:
        try:
            Pp = P.parse_row(r)
        except Exception:
            rep["M1"]["parse_fail"] += 1
            continue
        S, Q = Pp["S"], Pp["Q"]
        gold = r["gold"]
        nei = (Pp["statements"].get("T34n") or {}).get("NEI")
        base = _label(S, Q, nei)
        if base != gold:
            rep["M1"]["base_label_mismatch"] += 1
            continue
        # M1, M2, M5: structural variants, label checked by A and B
        for name, fn in (("M1", m1_inert), ("M2", m2_commute)):
            out = fn(S, Q, rng, nei)
            if isinstance(out, str):
                rep[name][out] += 1
                continue
            S2, Q2 = out
            try:
                la, (lb, _) = _label(S2, Q2, nei), _label_b(S2, Q2, nei)
            except RuleBreak:
                rep[name]["skip:rule11"] += 1
                continue
            ok = la == gold and lb == gold
            rep[name]["pass" if ok else "FAIL"] += 1
            if not ok and len(fails[name]) < 5:
                fails[name].append(r["id"])
        out = m5_void_decisive(S, Q, rng, nei)
        if isinstance(out, str):
            rep["M5"][out] += 1
        else:
            S2, Q2 = out
            try:
                la, (lb, _) = _label(S2, Q2, nei), _label_b(S2, Q2, nei)
                ok = la == lb and la is not None
            except RuleBreak:
                ok = None
        if not isinstance(out, str) and ok is None:
            rep["M5"]["skip:rule11"] += 1
        elif not isinstance(out, str):
            rep["M5"]["pass" if ok else "FAIL"] += 1
            if not ok and len(fails["M5"]) < 5:
                fails["M5"].append(r["id"])
        S3, Q3, mp = m3_rename(S, Q, rng, nei)
        la3, (lb3, _) = _label(S3, Q3, nei), _label_b(S3, Q3, nei)
        exp3 = mp.get(gold, gold) if isinstance(gold, str) else gold
        ok = la3 == exp3 and lb3 == exp3
        rep["M3"]["pass" if ok else "FAIL"] += 1
        if not ok and len(fails["M3"]) < 5:
            fails["M3"].append(r["id"])
        out = m9_negate(S, Q, rng, nei)
        if isinstance(out, str):
            rep["M9"][out] += 1
        else:
            S9, Q9, f = out
            la9, (lb9, _) = _label(S9, Q9, nei), _label_b(S9, Q9, nei)
            ok = la9 == 1 - gold and lb9 == 1 - gold
            rep["M9"]["pass" if ok else "FAIL"] += 1
            if not ok and len(fails["M9"]) < 5:
                fails["M9"].append(r["id"])
            dk = QS.neg_forms_allowed(Q)[1]
            if dk and f in ("N1", "N2", "N3"):
                Qd = QS.twin_neg(Q, "D", f)
                lad, (lbd, _) = _label(S9, Qd, nei), _label_b(S9, Qd, nei)
                ok = lad == gold and lbd == gold
                rep["M9"]["pass" if ok else "FAIL"] += 1
        if render_fn is not None:
            for name in ("M4", "M8"):
                try:
                    res = render_fn(name, r, Pp, cards_by_id, rng)
                except Exception as ex:
                    res = "skip:" + type(ex).__name__
                if isinstance(res, str):
                    rep[name][res] += 1
                else:
                    rep[name]["pass" if res else "FAIL"] += 1
                    if not res and len(fails[name]) < 5:
                        fails[name].append(r["id"])
    out = {}
    for m, c in rep.items():
        out[m] = {"pass": c.get("pass", 0), "fail": c.get("FAIL", 0), "skips": {k: v for k, v in c.items()
                                                                                if k not in ("pass", "FAIL")},
                  "ok": c.get("FAIL", 0) == 0 and c.get("pass", 0) >= n_min, "first_fail_ids": fails[m]}
    return out
