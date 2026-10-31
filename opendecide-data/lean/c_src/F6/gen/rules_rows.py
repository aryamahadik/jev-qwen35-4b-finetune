"""Rules-kind rows (S1, S2, S5): card profiles, record + gap construction against a target, question and options
per form, display-then-gold for C-OUT, C-GAP settling sets, C-CASE decidable sets and twins.

Every label here is solver A's (P / T over the full catalog). Solver B re-solves the parsed row in the G2/G3 gate.
"""
from __future__ import annotations

import random

from . import solver_a as A
from . import rules_gen as G
from .lex import FRAMES, OPTION_TEXT
from . import render_f6 as RF

FAIL = object()


class Reject(Exception):
    pass


def card_variant(P: dict, R: dict, form: str, nei: str | None, none: str | None, nothing: str | None,
                 frames: list, world: str | None = None, ev_tag=None) -> dict:
    """The card variant (switch-sentence groups) for a rules-kind row: fixed per card profile."""
    world = world or P["world"]
    V = {"world": world, "marker": P["marker"], "entity": "entity", "ev_tag": ev_tag if ev_tag is not None else
         P["ev_tag"], "event_names": [R["events"][e]["name"] for e in R["event_order"]],
         "has_lists": bool(R["classes"]), "event_lines": P.get("mode") == "rich" and bool(R["events"] or R["classes"]), "nei": nei, "none": none, "nothing": nothing,
         "frames": frames}
    if world == "local":
        cid = P["local_cid"]
        V["local_section"] = RF.cap(R["classes"][cid]["plural"])
        V["local_thing"] = R["classes"][cid]["name"]
    return V


def catalog(R: dict) -> list:
    """Reachable outcomes: rule heads, table cells and the default (s6 reachable options)."""
    outs = [R["default"]]
    for r in A.all_rules(R):
        if r["out"] not in outs:
            outs.append(r["out"])
    return outs


# ---------------------------------------------------------------- hidden-set search

def _forced_hidden(R: dict, asg: dict, P: dict) -> dict:
    """Facts that cannot be shown: a false event or membership whose type does not close (open, local)."""
    forced = {}
    roles = G.ref_vars(R)
    for k, v in asg.items():
        if k[0] == "ev" and v is False and R["world"] != "closed":
            forced[k] = "absent"
        if k[0] == "cls" and v is False:
            closes = R["world"] == "closed" or (R["world"] == "local" and R.get("local") == k[1])
            if not closes:
                forced[k] = "absent"
    # unreferenced absences are not gaps; only count referenced ones
    return {k: h for k, h in forced.items() if k in roles}


def _ok_subclass(R: dict, asg: dict, hidden: dict) -> bool:
    for b, a in R.get("subclass", []):
        kb, ka = ("cls", b), ("cls", a)
        b_known_true = asg[kb] and kb not in hidden
        if b_known_true and ka in hidden:
            return False  # a class fact fixed by the relation is never marked, tagged or absent-as-unknown
        a_shown_false = (not asg[ka]) and ka not in hidden
        if a_shown_false and kb in hidden:
            return False  # never 'not a <class A>' while the <class B> fact is unknown
    return True


def _hide_mode(rng, R, k, v, rich=True):
    tag = R.get("ev_tag")
    can_tag = bool(tag) and not tag["counts"]
    kind = k[0]
    closes = R["world"] == "closed" or (R["world"] == "local" and kind == "cls" and R.get("local") == k[1])
    modes = ["marker"] if (rich or kind in ("num", "cat")) else []
    if kind in ("num", "cat") or not closes:
        modes.append("absent")
    if can_tag and (kind in ("num", "cat") or v is True):
        modes.append("tag")
    if R.get("plans") and kind == "ev" and not closes:
        modes.append("plan")
    if not modes:
        return None
    return rng.choice(modes)


def _order_gap(rng, R):
    """Make one non-base notice's date a range or a month that straddles another notice's day (gap:order)."""
    nids = [n for n in R["notice_order"] if n != R["notice_order"][0]]
    if not nids:
        return None
    nid = rng.choice(nids)
    others = sorted(R["notices"][x]["date"]["d"] for x in R["notice_order"] if x != nid)
    d0 = R["notices"][nid]["date"]["d"]
    if rng.random() < 0.5:
        a, b = d0 - rng.randint(5, 40), d0 + rng.randint(5, 40)
        b = min(b, R["D"] - 1)
        new = {"k": "range", "a": a, "b": b}
    else:
        from .common import ymd, month_bounds
        dd = ymd(d0)
        lo, hi = month_bounds(dd.year, dd.month)
        if hi >= R["D"]:
            return None
        new = {"k": "month", "y": dd.year, "m": dd.month, "a": lo, "b": hi}
    if new["a"] >= new["b"]:
        return None
    if any(new["a"] <= o <= new["b"] for o in others if o != d0) and rng.random() < 0.3:
        return None
    R["notices"][nid] = {**R["notices"][nid], "date": new}
    return ("nd", nid)


def _evaluate(rng, R, case, asg, hidden, dis):
    Rf = G.realise(rng, R, case, asg, hidden, dis)
    gaps = G.visible_gaps(Rf, case)
    return Rf, gaps, A.solve_rules(Rf, case)


def _n_decisive(Rf, case, gaps):
    dec = A.decisive_gaps(Rf, case)
    gk = [g for g, _ in gaps]
    return [d for d in dec if d in gk]


def elems(R: dict, case: str, gaps: list) -> list:
    """kind@position of each visible gap (the gap signature, s6 'Gaps')."""
    return sorted(f"{k}@{G.gap_position(R, case, g)}" for g, k in gaps)


def _sub(a: list, need) -> bool:
    from collections import Counter
    if need is None:
        return True
    ca, cn = Counter(a), need
    return all(ca[x] <= cn.get(x, 0) for x in ca)


def _pred_elem(R, k, mode, roles):
    pos = {"num": "fields", "cat": "fields", "ev": "events", "cls": "lists", "nd": "notices"}[k[0]]
    if mode == "tag":
        return f"gap:evidence@{pos}"
    if mode == "plan":
        return f"gap:plan@{pos}"
    role = roles.get(k)
    if role == "unless":
        return f"gap:unless@{pos}"
    if role == "onlyif":
        return f"gap:onlyif@{pos}"
    return f"gap:value@{pos}"


def _modes(R, k, v, rich):
    tag = R.get("ev_tag")
    can_tag = bool(tag) and not tag["counts"]
    kind = k[0]
    closes = R["world"] == "closed" or (R["world"] == "local" and kind == "cls" and R.get("local") == k[1])
    modes = ["marker"] if (rich or kind in ("num", "cat")) else []
    if kind in ("num", "cat") or not closes:
        modes.append("absent")
    if can_tag and (kind in ("num", "cat") or v is True):
        modes.append("tag")
    if R.get("plans") and kind == "ev" and not closes:
        modes.append("plan")
    return modes


def build_rules_record(rng: random.Random, P: dict, pack: dict, case: str, distractors: list, *, target: str,
                       n_gaps: int, n_rules: int, n_out_min: int, table_shape=None, claim_fn=None,
                       tries: int = 60, policy=None, sig=None):
    """A record for one case whose answer matches target: 'settled' (|P| = 1) or 'open' (|P| >= 2 with exactly one
    decisive gap), with exactly n_gaps visible gaps; with `sig` (a kind@position multiset taken from an open row of
    the same card, repair r1) the gaps realise exactly that signature. Greedy: the decisive gap first (open rows),
    then trap gaps that keep the answer (settled) or keep exactly one decisive gap (open)."""
    from collections import Counter
    rich = P.get("mode") == "rich"
    need = Counter(sig) if sig else None
    if need is not None:
        n_gaps = sum(need.values())
        tries = max(tries, 80)
    for _ in range(tries):
        try:
            R = policy or G.draw_policy(rng, P, pack, n_rules, n_out_min, table_shape)
        except ValueError:
            continue
        R = {**R, "notices": {k: dict(v) for k, v in R["notices"].items()}}
        if P["world"] == "local":
            R["local"] = P["local_cid"]
        asg = G.full_case(rng, R, case)
        roles = G.ref_vars(R)
        hidden = _forced_hidden(R, asg, P)
        if len(hidden) > n_gaps or not _ok_subclass(R, asg, hidden):
            continue
        if len(R["notices"]) > 1:
            if need is not None:
                if need.get("gap:order@notices"):
                    if _order_gap(rng, R) is None:
                        continue
            elif P.get("order_gaps") and rng.random() < 0.3:
                _order_gap(rng, R)
        elif need is not None and need.get("gap:order@notices"):
            continue
        try:
            Rf, gaps, Pset = _evaluate(rng, R, case, asg, hidden, distractors)
        except (ValueError, A.Drop):
            continue
        if len(gaps) > n_gaps or not _sub(elems(Rf, case, gaps), need):
            continue
        onp = [k for k in roles if k not in hidden]
        offp = [(a["kind"], aid) for aid, a in R["attrs"].items() if (a["kind"], aid) not in roles]
        rng.shuffle(onp)
        rng.shuffle(offp)
        dec = None
        if target == "open":
            if len(Pset) >= 2:
                d = _n_decisive(Rf, case, gaps)
                if len(d) != 1:
                    continue
                dec = d[0]
            else:
                for k in onp:
                    ms = _modes(R, k, asg[k], rich)
                    if need is not None:
                        ms = [m for m in ms if need.get(_pred_elem(R, k, m, roles))]
                    if not ms:
                        continue
                    hm = rng.choice(ms)
                    h2 = {**hidden, k: hm}
                    if not _ok_subclass(R, asg, h2):
                        continue
                    try:
                        Rf2, g2, P2 = _evaluate(rng, R, case, asg, h2, distractors)
                    except (ValueError, A.Drop):
                        continue
                    if len(P2) >= 2 and len(g2) <= n_gaps and _sub(elems(Rf2, case, g2), need):
                        d = _n_decisive(Rf2, case, g2)
                        if len(d) == 1:
                            hidden, Rf, gaps, Pset, dec = h2, Rf2, g2, P2, d[0]
                            break
                if dec is None:
                    continue
        elif len(Pset) != 1:
            continue
        # trap gaps: on-path vars whose hiding keeps the target, and off-path marked attributes
        pool = [k for k in onp if k not in hidden] + offp
        rng.shuffle(pool)
        for k in pool:
            if len(gaps) >= n_gaps:
                break
            if k in roles:
                ms = _modes(R, k, asg[k], rich)
            else:
                ms = ["marker"]
            if need is not None:
                left = need - Counter(elems(Rf, case, gaps))
                ms = [m for m in ms if left.get(_pred_elem(R, k, m, roles))]
            if not ms:
                continue
            hm = rng.choice(ms)
            h2 = {**hidden, k: hm}
            if not _ok_subclass(R, asg, h2):
                continue
            try:
                Rf2, g2, P2 = _evaluate(rng, R, case, asg, h2, distractors)
            except (ValueError, A.Drop):
                continue
            if len(g2) != len(gaps) + 1 or not _sub(elems(Rf2, case, g2), need):
                continue
            if target == "settled":
                if len(P2) != 1:
                    continue
            else:
                if len(P2) < 2:
                    continue
                d = _n_decisive(Rf2, case, g2)
                if d != [dec]:
                    continue
            hidden, Rf, gaps, Pset = h2, Rf2, g2, P2
        if len(gaps) != n_gaps:
            continue
        if need is not None and Counter(elems(Rf, case, gaps)) != need:
            continue
        return Rf, asg, hidden, Pset, None, gaps
    raise Reject(f"no record for target {target}")
