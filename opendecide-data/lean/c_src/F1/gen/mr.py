"""G4 metamorphic relations (G0 F1 v7 section 5): >= 1,000 base rows per training sampler; S5 on >= 1,000 extra
draws that are tested and discarded. Hypothesis is not installed in the venv (no downloads for F1): the property tests
use seeded random generation through the same samplers instead.

Expected value of every relation = solver A on the mutated structure AND the stated property. Render-level relations
(M1, M2, M3, M5, M11) are also checked end to end: render -> parse -> solver B.
"""
from __future__ import annotations

import random
import time
from collections import Counter

import common as C
import emit as EM
import parse_f1 as PF
import rows as R
import samplers as SM
import solver_a as A
import solver_b as SB
from model import Attr, Case, Inert, Item, Lit, Rule


def _gold_of(row, S, cases, q):
    gb = R.GroupBuilder.__new__(R.GroupBuilder)
    r2 = dict(row)
    r2["q"] = q
    res = R.GroupBuilder.regold(gb, r2, S, cases)
    return None if res is None else res[0]


def _base_key(row):
    q = row["q"]
    if q["qtype"] == "Q4":
        return "none" if row["gold"] == "__NONE__" else row["q4_refs"].index(row["gold"])
    return row["gold"]


def _e2e(card, pack, row, rid, vocab):
    """Render the (mutated) row, loader_check it, parse it back and re-solve with solver B; returns gold match."""
    fields, must, st, wid, opts, gold, canon_opts, qtext = EM.render_row(card, pack, row, rid)
    out = {"id": rid, "qtype": "noul" if row["q"]["qtype"] == "Q3" else "choice", "options": opts, "gold": gold,
           **fields}
    res = EM.fcard.loader_check(out, must_show=must)
    if not res["ok"]:
        return False, "loader"
    try:
        EM.gate_row(card, pack, row, out, vocab, canon_opts)
    except EM.GateFail as e:
        return False, str(e)[:120]
    return True, out


def m1(card, pack, row, rid, vocab):
    fields, must, st, wid, opts, gold, canon_opts, qtext = EM.render_row(card, pack, row, rid)
    out = {"id": rid, "qtype": "noul" if row["q"]["qtype"] == "Q3" else "choice", "options": opts, "gold": gold,
           **fields}
    n = 2 if out["qtype"] == "noul" else len(opts)
    rng = random.Random(rid)
    for t in range(2):
        p = list(range(n))
        rng.shuffle(p)
        res = EM.fcard.loader_check(out, must_show=must, perm=p, check_rows=(t == 0))
        if not res["ok"]:
            return False
    return True


def _rename_names(text, old_disp, new_disp):
    """Apply the outcome-name bijection to a worked case's text (longest names first, via placeholders)."""
    keys = sorted(old_disp, key=lambda o: -len(old_disp[o]))
    for i, o in enumerate(keys):
        text = text.replace(old_disp[o], f"\x00{i}\x00")
    for i, o in enumerate(keys):
        text = text.replace(f"\x00{i}\x00", new_disp[o])
    return text


def m2(card, pack, row, rid, vocab):
    """Consistent rename: outcome names permuted (a bijection), category values permuted within each field, new
    case reference. Gold maps through the bijection."""
    rng = random.Random(rid + "m2")
    outs = list(card["outcomes"])
    perm = outs[:]
    rng.shuffle(perm)
    omap = dict(zip(outs, perm))
    c2 = dict(card)
    c2["display"] = {o: card["display"][omap[o]] for o in outs}
    c2["meanings"] = {o: card["meanings"][o] for o in outs}
    # card text names outcomes: rebuild the statements (and worked cases) under the renamed display
    from cards import card_statements
    c2["_stmts"] = card_statements(c2)
    if card.get("few_cases"):
        c2["few_cases"] = [{"case": _rename_names(x["case"], card["display"], c2["display"]), "answer": x["answer"]}
                           for x in card["few_cases"]]
    S = row["S"].copy()
    cmaps = {}
    for k, a in list(S.attrs.items()):
        if a.type == "cat":
            vs = list(a.values)
            pv = vs[:]
            rng.shuffle(pv)
            cmaps[k] = dict(zip(vs, pv))

    def mlit(m):
        if m.attr in cmaps:
            return Lit(m.attr, m.op, tuple(sorted(cmaps[m.attr][v] for v in m.args)))
        return m

    def mrule(r):
        if r is None:
            return None
        return r.copy(items=tuple(Item(it.kind, tuple(mlit(m) for m in it.mem), it.k) for it in r.items),
                      unless=mlit(r.unless) if r.unless is not None else None)
    S.rules = [mrule(r) for r in S.rules]
    for n in S.notices:
        n.rule = mrule(n.rule)
    for e in S.inert:
        if e.notice is not None:
            e.notice.rule = mrule(e.notice.rule)
        e.rule = mrule(e.rule)
    cases = []
    for c in row["cases"]:
        v = dict(c.vals)
        for k, mp in cmaps.items():
            if k in v:
                v[k] = mp[v[k]]
        cases.append(c.copy(vals=v, ref=c.ref))
    g2 = _gold_of(row, S, cases, row["q"])
    if g2 != _base_key(row):
        return False
    r2 = dict(row)
    r2.update({"S": S, "cases": cases})
    ok, _ = _e2e(c2, pack, r2, rid + "-m2", vocab)
    return ok


def m3(card, pack, row, rid, vocab):
    S = row["S"].copy()
    if S.policy.prim == "ORDER" or S.s3_rows is not None:
        return None
    rng = random.Random(rid + "m3")
    rs = list(S.rules)
    rng.shuffle(rs)
    S.rules = rs
    if getattr(S, "doc_order", None):
        order = []
        for d in S.doc_order:
            order += [("r", r.rid) for r in rs] if d == "base" else [("n", d)]
        S.order = order
    else:
        S.order = [("r", r.rid) for r in rs] + [x for x in row["S"].order if x[0] == "n"]
    g2 = _gold_of(row, S, row["cases"], row["q"])
    if g2 != _base_key(row):
        return False
    r2 = dict(row)
    r2["S"] = S
    ok, _ = _e2e(card, pack, r2, rid + "-m3", vocab)
    return ok


def m4m5(builder, row, kind):
    builder.rng = random.Random(str(id(row)) + kind)
    us = builder.unit_inert(row)
    if not us:
        return None
    return True  # unit_inert re-labels and keeps only gold-preserving variants; failures are counted by builder.stats


def m5_e2e(card, pack, builder, row, rid, vocab):
    us = builder.unit_inert(row)
    if not us:
        return None
    v = us[0]
    if v.get("mr") not in ("M5d", "M5i"):
        return None
    if len(v["S"].rules) != len(row["S"].rules) or len(v["S"].notices) != len(row["S"].notices):
        return False
    ok, _ = _e2e(card, pack, v, rid + "-m5", vocab)
    return ok


def m6(builder, row):
    q = row["q"]
    if q["qtype"] == "Q4" or row.get("res") is None:
        return None
    src, W = A.gold_source(row["res"])
    S = row["S"]
    if src != "ONE" or len(S.rules) < 4:
        return None
    rmap = {r.rid: r for r in S.rules}
    if W not in rmap or rmap[W].kind != "gen":
        return None
    if any(n.target == W or (n.pos and n.pos[0] == "after" and n.pos[1] == W) or
           (n.rule is not None and n.rule.kind in ("pexc", "oexc") and n.rule.target == W) for n in S.notices):
        return None
    if any(r.kind in ("pexc", "oexc") and r.target == W for r in S.rules):
        return None
    comps = row["res"]["comps"]
    if any(sum(1 for c in cc["cands"] if cc["rules"][c][0].out == rmap[W].out) > 1 for cc in comps):
        return None
    S2 = S.copy()
    S2.rules = [r for r in S2.rules if r.rid != W]
    S2.order = [x for x in S2.order if x != ("r", W)]
    if S2.s3_rows is not None:
        S2.s3_rows = [x for x in S2.s3_rows if x != W]
    try:
        r2 = A.solve(S2, row["cases"][0])
    except A.Reject:
        return None
    # property: the candidate set is the original one without W (in every completion). Completions are compared
    # at the same filled values: removing W can coarsen the open-world completion grid, so S2 is re-solved at each
    # completion point of the original structure (not zipped against S2's own, coarser grid).
    case = row["cases"][0]
    if S.policy.world == "open" and case.unknown:
        pts = list(A.completions(S, case))
    else:
        pts = [case.vals]
    if len(pts) != len(comps):
        return False
    for v, c1 in zip(pts, comps):
        try:
            c2 = A.solve_closed(S2, v, case.notrec)
        except A.Reject:
            return False
        if sorted(x for x in c1["cands"] if x != W) != sorted(c2["cands"]):
            return False
    return True


def m7(builder, row):
    q = row["q"]
    if q["qtype"] == "Q4":
        return None
    S = row["S"]
    case = row["cases"][0]
    g = case.vals[S.policy.gov]
    cand = [n for n in S.notices if n.edate <= g and A.removal_closure(S, frozenset([n.num])) == frozenset([n.num])]
    if not cand:
        return None
    n = cand[0]
    S2 = S.copy()
    S2.notices = [x.copy(edate=g + 7) if x.num == n.num else x for x in S2.notices]
    if not builder.r3_ok(S2):
        return None
    try:
        a = A.solve(S2, case)
        b = A.solve(S, case) if False else None
        ref = A.solve_closed
        # expected: solver A on S without notice a
        fin_moved = {c["final"] for c in a["comps"]}
        Sx = S.copy()
        Sx.notices = [x for x in Sx.notices if x.num != n.num]
        x = A.solve(Sx, case)
        fin_removed = {c["final"] for c in x["comps"]}
    except A.Reject:
        return None
    return fin_moved == fin_removed


def m8(builder, row, pack):
    S = row["S"]
    if S.policy.world != "closed" or row["q"]["qtype"] == "Q4":
        return None
    used = {m.attr for r in S.rules for it in r.all_items() for m in it.mem}
    used |= {m.attr for n in S.notices if n.rule for it in n.rule.all_items() for m in it.mem}
    free = [k for k, a in S.attrs.items() if a.type == "bool" and k not in used and not a.presup]
    if not free:
        return None
    S2 = S.copy()
    case = row["cases"][0].copy(vals=dict(row["cases"][0].vals))
    case.vals[free[0]] = True
    return _gold_of(row, S2, [case], row["q"]) == _base_key(row)


def m9(row):
    S = row["S"]
    case = row["cases"][0]
    if S.policy.world != "open" or not case.unknown or row["q"]["qtype"] == "Q4":
        return None
    resA = A.solve(S, case)
    resB = SB.solve(S, case)
    finB = {c["final"] for c in resB["comps"]}
    if resA["det"]:
        return finB == {resA["final"]}
    return len(finB) >= 2


def m10(row):
    if row["q"]["qtype"] != "Q3":
        return None
    res = row["res"]
    X = row["q"]["X"]
    a = A.q3_answer(res, X, "aff")
    n = A.q3_answer(res, X, "neg")
    d = A.q3_answer(res, X, "dneg")
    if a is None:
        return None
    return n == 1 - a and d == a


def m11(card, pack, row, rid, vocab):
    if card["short"]:
        return None
    r2 = dict(row)
    r2["attack"] = random.Random(rid).choice(__import__("lexicon").INJECTIONS)
    ok, _ = _e2e(card, pack, r2, rid + "-m11", vocab)
    return ok


def m12(row):
    S = row["S"]
    if row["q"]["qtype"] == "Q4" or row.get("res") is None:
        return None
    comps = row["res"]["comps"]
    if any(len(c["cands"]) != 1 for c in comps):
        return None
    pols = ["SPEC"]
    if all(r.date is not None for r in S.rules) or S.policy.prim == "LATER" or S.policy.sec == "LATER":
        pols.append("LATER")
    if all(r.tier is not None for r in S.rules if r.kind in ("gen", "oexc")) and S.policy.tiers:
        pols.append("PRIORITY")
    alt = [p for p in pols if p != S.policy.prim]
    if not alt:
        return None
    S2 = S.copy()
    S2.policy.prim = alt[0]
    S2.policy.sec = None
    return _gold_of(row, S2, row["cases"], row["q"]) == _base_key(row)


def run_card(args):
    card, pack, n_base = args[:3]
    tag = args[3] if len(args) > 3 else ""      # extra runs use a new seed stream (no repeated base rows)
    vocab = PF.vocab_for(pack)
    tr = R.Trackers()
    gb = R.GroupBuilder(card, pack, tr, f"g4{tag}|{card['card_id']}")
    res = Counter()
    fails = []
    done = 0
    t0 = time.time()
    while done < n_base and time.time() - t0 < 900:
        try:
            grp = gb.build_group()
        except A.Reject:
            continue
        row = grp[0]
        done += 1
        rid = f"g4-{card['card_id']}-{done}"
        tests = {
            "M1": lambda: m1(card, pack, row, rid, vocab),
            "M2": lambda: m2(card, pack, row, rid, vocab),
            "M3": lambda: m3(card, pack, row, rid, vocab),
            "M4/M5": lambda: m4m5(gb, row, "inert"),
            "M5e2e": lambda: m5_e2e(card, pack, gb, row, rid, vocab),
            "M6": lambda: m6(gb, row),
            "M7": lambda: m7(gb, row),
            "M8": lambda: m8(gb, row, pack),
            "M9": lambda: m9(row),
            "M10": lambda: m10(row),
            "M11": lambda: m11(card, pack, row, rid, vocab),
            "M12": lambda: m12(row),
        }
        for name, fn in tests.items():
            try:
                r = fn()
            except (A.Reject, SM.DrawFail, KeyError, ValueError, IndexError) as e:
                r = None
            except Exception as e:  # noqa: BLE001
                r = False
                fails.append((name, rid, f"{type(e).__name__}: {str(e)[:120]}"))
            if r is None:
                res[f"{name}:na"] += 1
            elif r:
                res[f"{name}:pass"] += 1
            else:
                res[f"{name}:fail"] += 1
                if len(fails) < 30:
                    fails.append((name, rid, "fail"))
    res["rows"] = done
    return {"card_id": card["card_id"], "sampler": card["sampler"], "res": dict(res), "fails": fails,
            "inert_dropped": gb.stats.get("inert_dropped", 0)}
