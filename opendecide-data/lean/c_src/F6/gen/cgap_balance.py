"""C-GAP decisive-gap balance (repair r1 v3d; G10 'longest option is gold' [c_gap], G7 C-GAP option features).

Why: S1 builds an open C-GAP record greedily (rules_rows.build_rules_record): the decisive gap first, then trap gaps
that keep exactly one decisive gap. A hidden on-path event almost always settles the question, so events (long option
texts: 'whether X had a "<event>" event') are the decisive gap far more often than they are a trap, and trap gaps are
mostly attributes (short texts). Result on the v3c pool: the gold gap was the longest option on 39% of C-GAP rows
(1/k = 30%), and 'interview attendance' on F6-S1-c_gap-01 was gold on 29 of 46 rows (expected 13).

Fix: an acceptance weight on the open record, by (card, k, decisive variable name). Weights come from a smoke of the
real record builder (no twins), fitted so that every variable that shows as a visible gap is the decisive gap on
1/(k-1) of the open rows that show it (iterative proportional fitting; the open-row share of 1/k 'nothing' rows then
gives P(gold | shown) = 1/k). The weight depends only on which variable is decisive, never on a row's text, and it
removes (does not add) a dependence between option identity and gold. Rejected draws are redrawn (s_rules, 8 attempts
per unit; build, 10 rounds), never relabelled.

  python -m gen.cgap_balance <n_records>        -> gen/cgap_balance.json (+ report on stdout)
"""
from __future__ import annotations

import json
import multiprocessing as mp
import random
import sys
import time
from collections import Counter, defaultdict

from .common import GEN

W_MIN = 0.15


def kind(g):
    return {"num": "val", "cat": "val"}.get(g[0], g[0])


def vname(R, g):
    t, i = g[0], g[1]
    if t in ("num", "cat"):
        return f"val:{R['attrs'][i]['name']}"
    if t == "ev":
        return f"ev:{R['events'][i]['name']}"
    if t == "cls":
        return f"cls:{R['classes'][i]['name']}"
    if t == "nd":
        return f"nd:{R['notices'][i]['name']}"
    return f"{t}:{i}"


def key(card_id, k, name):
    return f"{card_id}|{k}|{name}"


_W = None


def weight(card_id, k, R, g) -> float:
    """Acceptance weight of an open C-GAP record whose decisive gap is g (1.0 when not in the table)."""
    global _W
    if _W is None:
        p = GEN / "cgap_balance.json"
        _W = json.load(open(p))["w"] if p.exists() else {}
    return _W.get(key(card_id, k, vname(R, tuple(g))), 1.0)


_BY = {}


def _one(a):
    from . import build, s_rules, rules_card as RC
    cid, sp, i = a
    card = build._card(_BY[cid])
    sp = dict(sp, twin=None, role="open", n_gaps=sp["k"] - 1, sid=f"cgb{i}", cgap_balance_off=True)
    try:
        recs = s_rules.build_rules_unit(card, sp, f"cgb-{i}")
    except Exception:  # noqa: BLE001
        return None
    r = recs[0]
    R = r["R"]
    gl = [tuple(g) for g, _ in r["gaps"]]
    d = tuple(r["settle"][0])
    rng = random.Random(i)
    lens = {vname(R, g): len(RC.gap_text(R, g, "AAA-0000", alt=rng.random() < 0.5)) for g in gl}
    return cid, sp["k"], vname(R, d), [vname(R, g) for g in gl], lens


def fit(recs, iters=60):
    """w[(card, k, name)] so that, reweighting each record by w of its decisive variable, every shown variable is
    decisive on 1/(k-1) of the open rows that show it."""
    w = defaultdict(lambda: 1.0)
    groups = defaultdict(list)
    for r in recs:
        groups[(r[0], r[1])].append(r)
    for (cid, k), rs in groups.items():
        m = k - 1
        names = {n for r in rs for n in r[3]}
        for _ in range(iters):
            D = Counter()
            V = Counter()
            for r in rs:
                x = w[(cid, k, r[2])]
                D[r[2]] += x
                for n in r[3]:
                    V[n] += x
            for n in names:
                if D[n] > 0:
                    w[(cid, k, n)] *= ((V[n] / m) / D[n]) ** 0.5
            mx = max(w[(cid, k, n)] for n in names if D[n] > 0)
            for n in names:
                if D[n] > 0:
                    w[(cid, k, n)] = max(W_MIN, min(1.0, w[(cid, k, n)] / mx))
    return w


def report(recs, w):
    tot = Counter()
    for tag, wf in (("before", lambda r: 1.0), ("after", lambda r: w[(r[0], r[1], r[2])])):
        W = hit = 0.0
        worst = []
        D = Counter()
        V = Counter()
        for r in recs:
            x = wf(r)
            W += x
            mx = max(r[4].values())
            top = [n for n in r[4] if r[4][n] == mx]
            hit += x * (r[2] in top) / len(top)
            D[(r[0], r[1], r[2])] += x
            for n in r[3]:
                V[(r[0], r[1], n)] += x
        for kk in V:
            if V[kk] >= 15:
                worst.append((round(D[kk] / V[kk] * (kk[1] - 1), 2), kk))
        worst.sort()
        tot[tag] = W
        print(f"{tag}: yield {W / len(recs):.2f}  longest-gold on open rows {hit / W:.3f}  "
              f"(uniform {sum(1 / (r[1] - 1) for r in recs) / len(recs):.3f}); "
              f"(dec share x (k-1)) min {worst[0][0]} max {worst[-1][0]} {worst[-1][1]}")


def main():
    from . import plan, build
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    build._init()
    cards = plan.plan_cards()
    _BY.update({c["card_id"]: c for c in cards})
    specs = [s for s in plan.plan_specs(cards, 1.5, "cand") if s["form"] == "c_gap" and s["gold"] == "gap"]
    jobs = [(specs[j % len(specs)]["card"], specs[j % len(specs)], j) for j in range(n)]
    t = time.time()
    with mp.get_context("fork").Pool(2) as pool:
        recs = [r for r in pool.imap_unordered(_one, jobs, chunksize=8) if r]
    w = fit(recs)
    report(recs, w)
    out = {"_doc": "gen/cgap_balance.py (repair r1 v3d): acceptance weight of an open C-GAP record by "
                   "card|k|decisive variable; missing keys = 1.0",
           "n_records": len(recs), "seconds": round(time.time() - t),
           "w": {key(c, k, nm): round(v, 4) for (c, k, nm), v in sorted(w.items()) if v < 0.999}}
    json.dump(out, open(GEN / "cgap_balance.json", "w"), indent=1)
    print(f"records {len(recs)} / {n}; weights < 1: {len(out['w'])}; {time.time() - t:.0f}s")


if __name__ == "__main__":
    main()
