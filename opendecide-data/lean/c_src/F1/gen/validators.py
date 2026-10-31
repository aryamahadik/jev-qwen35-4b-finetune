"""Structure validators run on the PARSED structure of every emitted row (R2, R3, R4, R5; G0 F1 v7 section 2).

Written from the spec: R3 notice constraints (dates after B, targets / anchors / inserted exceptions' targets in force on
the effective date, inserted ids never reused, never two notices on one rule with the same effective date, same-date
notices never interact, unique S3 positions), R2 (acyclic exception graph, nesting <= 2, no exception to an only-if
rule), R4 (no literal tests the governing-date field), R5 (default != escalate).
"""
from __future__ import annotations

from collections import defaultdict


class Violation(Exception):
    pass


def touched(n):
    t = set()
    if n.ntype in ("replace", "repeal"):
        t.add(n.target)
    if n.pos is not None and n.pos[0] == "after":
        t.add(n.pos[1])
    if n.ntype == "insert":
        t.add(n.rule.rid)
        if n.rule.kind in ("pexc", "oexc"):
            t.add(n.rule.target)
    return t


def check_R3(S):
    B = S.policy.B
    base_ids = {r.rid for r in S.rules}
    ins_ids = [n.rule.rid for n in S.notices if n.ntype == "insert"]
    if len(set(ins_ids)) != len(ins_ids) or set(ins_ids) & base_ids:
        raise Violation("R3 inserted id reused")
    for n in S.notices:
        if not n.edate > B or n.ndate < B:
            raise Violation("R3 notice dates")
    live = {r.rid: r for r in S.rules}
    by_date = defaultdict(list)
    for n in S.notices:
        by_date[n.edate].append(n)
    for d in sorted(by_date):
        ns = by_date[d]
        # same-date notices never interact
        ts = []
        for n in ns:
            t = touched(n)
            t |= {rid for rid, r in live.items() if r.kind in ("pexc", "oexc") and r.target in t}
            ts.append(t)
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                if ts[i] & ts[j]:
                    raise Violation("R3 same-date interaction")
        pos = [n.pos for n in S.notices if n.pos is not None]
        if len(pos) != len(set(pos)):
            raise Violation("R3 two notices at one S3 position")
        cur = {rid: r for rid, r in live.items() if r.last is None or r.last >= d}
        for n in ns:
            if n.ntype in ("replace", "repeal") and n.target not in cur:
                raise Violation("R3 target not in force")
            if n.pos is not None and n.pos[0] == "after" and n.pos[1] not in cur:
                raise Violation("R3 anchor not in force")
            if n.ntype == "insert" and n.rule.kind in ("pexc", "oexc") and n.rule.target not in cur:
                raise Violation("R3 inserted exception target not in force")
        for n in ns:
            if n.ntype == "replace":
                live[n.target] = n.rule
            elif n.ntype == "repeal":
                live.pop(n.target, None)
            else:
                live[n.rule.rid] = n.rule
        # exceptions to rules no longer present drop out of the live set
        changed = True
        while changed:
            changed = False
            for rid in list(live):
                r = live[rid]
                if r.kind in ("pexc", "oexc") and r.target not in live:
                    live.pop(rid)
                    changed = True
    return True


def check_R2(S):
    rules = {r.rid: r for r in S.rules}
    for n in S.notices:
        if n.ntype == "insert":
            rules[n.rule.rid] = n.rule
    for rid, r in rules.items():
        if r.kind in ("pexc", "oexc"):
            seen = {rid}
            lvl = 0
            x = r
            while x.kind in ("pexc", "oexc"):
                lvl += 1
                t = rules.get(x.target)
                if t is None:
                    break
                if t.kind == "onlyif":
                    raise Violation("R2 exception to an only-if rule")
                if t.rid in seen:
                    raise Violation("R2 cycle")
                seen.add(t.rid)
                x = t
            if lvl > 2:
                raise Violation("R2 nesting > 2")
    return True


def check_R4(S):
    gov = S.policy.gov
    for r in list(S.rules) + [n.rule for n in S.notices if n.rule is not None]:
        for it in r.all_items():
            for m in it.mem:
                if m.attr == gov:
                    raise Violation("R4 literal on the governing-date field")
    return True


def check_all(S):
    check_R2(S)
    check_R3(S)
    check_R4(S)
    if S.policy.escalate is not None and S.policy.default == S.policy.escalate:
        raise Violation("R5 default is escalate")
    return True
