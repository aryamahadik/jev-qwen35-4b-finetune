"""crowd_select_c2.py: c_build/crowd_select.select, copied VERBATIM, with exactly two optional inputs injected (PREREG Ruling A69
(b5), program fix for A42-D 6): `bins_in` (the bin of every row id; default: the p_g bins) and `order_in` (the seeded unit order
of the filling pass; default: sorted by h64(seed, key, "order", first row id)). Called with neither, it is byte-identical to
crowd_select.select (tests/test_c2_select_a69.py compares this file's source with crowd_select.select line by line, apart from
those three edits, and runs both on random pools). c_build/crowd_select.py is never edited; everything else comes from it.
"""
from __future__ import annotations

import math  # noqa: F401  (used by the copied body)
import sys
from collections import Counter, defaultdict  # noqa: F401
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crowd_select as _cs  # noqa: E402  (c_build)
from crowd_select import (CAP, REFLOW_ORDER, REFLOW_ROUNDS, SEED, _budgets, bin_of, easy_thinned,  # noqa: E402,F401
                          label_class, n_classes, selection_report, stratum)
from mixio import h64  # noqa: E402,F401


def select(rows, units, pg: dict | None, target: int, key: str = "", seed: int = SEED, bins_in: dict | None = None,
           order_in: list | None = None) -> dict:
    """Stratified, label-balanced, representative selection of whole units to `target` rows. pg None = provisional
    (no crowd yet: one bin 'na'; used by the mixer's --dry-run only). Returns sel (unit indices), bins, report."""
    crowd = pg is not None
    bins = {r["id"]: (bin_of(pg.get(r["id"])) if crowd else "na") for r in rows} if bins_in is None else dict(bins_in)   # A69: injected
    uid = [rows[u[0]]["id"] for u in units]
    order = sorted(range(len(units)), key=lambda u: h64(seed, key, "order", uid[u])) if order_in is None else list(order_in)   # A69: injected
    easy_drop = easy_thinned(rows, units, bins, key, seed) if crowd else set()
    elig = [u for u in order if u not in easy_drop]
    info = {}
    for u in elig:
        for i in units[u]:
            r = rows[i]
            b = bins[r["id"]]
            info[i] = (b, stratum(r, b), label_class(r))
    avail = Counter(v[0] for v in info.values())
    budget = _budgets(avail, target, crowd)
    n = defaultdict(Counter)
    for b, s, c in info.values():
        n[s][c] += 1
    quota = {}
    for b, B in budget.items():
        ss = [s for s in n if s[2] == b]
        bal = {s: min(n[s][c] for c in range(n_classes(s))) for s in ss}
        tot = sum(bal[s] * n_classes(s) for s in ss)
        f = min(1.0, B / tot) if tot else 0.0
        for s in ss:
            quota[s] = math.floor(bal[s] * f)      # floor: the quotas never sum above the bin budget
    cnt, used, pool = defaultdict(Counter), Counter(), defaultdict(Counter)
    sel, taken, out = [], set(), set()
    cache = {}

    def add_of(u):
        if u not in cache:
            a, ab = defaultdict(Counter), Counter()
            for i in units[u]:
                b, s, c = info[i]
                a[s][c] += 1
                ab[b] += 1
            cache[u] = (a, ab)
        return cache[u]

    def pkey(s):
        return (s[0], s[1] if s[0] != "yn" else "", s[2])

    def imbalance(c: Counter, k: int) -> int:
        return max(c[j] for j in range(k)) - min(c[j] for j in range(k))

    def tol(s, c) -> float:
        return 1 if s[0] == "ord" else max(2, 0.02 * sum(c.values()))

    def move(u, sign):
        a, ab = add_of(u)
        for s, c in a.items():
            for cl, k in c.items():
                cnt[s][cl] += sign * k
                pool[pkey(s)][cl] += sign * k
        for b, k in ab.items():
            used[b] += sign * k
        if sign > 0:
            sel.append(u)
            taken.add(u)
        else:
            sel.remove(u)
            out.add(u)

    def fill(strict, slack=0):   # strict: per-stratum quotas (+ slack, and only units that feed a class below its
        for u in elig:           # quota when slack > 0); else fill without worsening pooled or ordinal balance
            if u in taken or u in out:
                continue
            a, ab = add_of(u)
            if any(used[b] + k > budget.get(b, 0) for b, k in ab.items()):
                continue
            if strict and any(cnt[s][c] + k > quota.get(s, 0) + slack for s, cc in a.items() for c, k in cc.items()):
                continue
            if strict and slack and not any(cnt[s][c] < quota.get(s, 0) for s, cc in a.items() for c in cc):
                continue
            if not strict:
                ok = True
                for s, cc in a.items():
                    for key, cur in ((pkey(s), pool[pkey(s)]), (s, cnt[s])) if s[0] == "ord" else ((pkey(s), pool[pkey(s)]),):
                        k = n_classes(s)
                        old, new = imbalance(cur, k), imbalance(cur + cc, k)
                        if new > old and new > tol(s, cur + cc):
                            ok = False
                if not ok:
                    continue
            move(u, +1)

    def rebalance():     # drop units that only feed over-filled classes of an unbalanced stratum
        n = 0
        for s in list(cnt):
            k = n_classes(s)
            if k < 2:
                continue
            for _ in range(10 ** 4):
                c = cnt[s]
                if imbalance(c, k) <= tol(s, c):
                    break
                lo = min(c[j] for j in range(k))
                hi = {j for j in range(k) if c[j] > lo + tol(s, c) - 1}
                u = next((u for u in reversed(sel) if s in add_of(u)[0] and set(add_of(u)[0][s]) <= hi), None)
                if u is None:
                    break
                move(u, -1)
                n += 1
        return n

    def run():
        fill(True)
        fill(True, slack=1)
        for _ in range(3):
            fill(False)
            if not rebalance():
                break
        fill(False)
        if crowd:                           # caps hold on the rows actually selected (a short total raises shares)
            for b in ("hard", "easy"):
                for u in reversed(list(sel)):
                    tot = sum(used.values())
                    if used[b] <= CAP[b] * tot + 1e-9:
                        break
                    bs = Counter(info[i][0] for i in units[u])
                    if bs[b] and not bs["medium"]:
                        move(u, -1)

    run()
    budget0, reflow = dict(budget), []
    if crowd and sum(used.values()) < target:
        # Reflow (PREREG A27 c): the bin budgets were fixed before the cell-balanced downsampling, so a bin whose
        # balanced pool is short left the total short. Freeze every bin at what it holds and grant the shortfall to
        # one receiver at a time (medium = "the rest" first, then hard and easy up to their caps), raise that bin's
        # per-stratum quotas with the same proportional floor rule (never lowered), and re-run the same seeded fill,
        # rebalance and cap passes. A round that gains no rows is undone (never fewer rows than before it) and its
        # receiver is exhausted. Runs only when short, so a selection that already meets its target is unchanged.
        def snapshot():
            return (list(sel), set(taken), set(out), {s: Counter(c) for s, c in cnt.items()}, Counter(used),
                    {s: Counter(c) for s, c in pool.items()}, dict(budget), dict(quota))

        def restore(st):
            for obj, val in zip((sel, taken, out, cnt, used, pool, budget, quota), st):
                obj.clear()
                obj.extend(val) if isinstance(obj, list) else obj.update(val)

        live = [b for b in REFLOW_ORDER if b in budget]
        for _ in range(REFLOW_ROUNDS):
            tot0 = sum(used.values())
            short = target - tot0
            if short <= 0 or not live:
                break
            b = live[0]
            room = (avail[b] if b == "medium" else min(avail[b], int(CAP[b] * target))) - used[b]
            if room <= 0:
                live.pop(0)
                continue
            grant = min(short, room)
            st = snapshot()
            for x in budget:
                budget[x] = used[x]
            budget[b] = used[b] + grant
            ss = [s for s in n if s[2] == b]
            bal = {s: min(n[s][c] for c in range(n_classes(s))) for s in ss}
            tot = sum(bal[s] * n_classes(s) for s in ss)
            f = min(1.0, budget[b] / tot) if tot else 0.0
            for s in ss:
                quota[s] = max(quota.get(s, 0), math.floor(bal[s] * f))
            run()
            gained = sum(used.values()) - tot0
            reflow.append({"bin": b, "grant": grant, "gained": gained, "kept": gained > 0})
            if gained <= 0:
                restore(st)
                live.pop(0)
    rep = selection_report(rows, units, sorted(sel), bins, target, crowd, pg)
    if crowd:
        rep["reflow"] = {"rounds": reflow, "budget_after": dict(budget)}
    return {"sel": sorted(sel), "bins": bins, "easy_dropped_units": len(easy_drop), "budget": budget0,
            "reflow": reflow, "report": rep}
