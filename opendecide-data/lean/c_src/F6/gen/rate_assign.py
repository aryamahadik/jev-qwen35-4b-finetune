"""Card yes-rate assignment (repair r1; G7 raw multi-card features, F6-QC-1 follow-up).

Per-card yes rates are drawn from U[20, 80] in complementary pairs (C_DATA_SPEC 2.1; plan.yes_rates). Which card
gets which drawn rate is a free design choice. This script permutes the drawn rates among the yes/no cards so that
every word or word pair shared by several cards (pack vocabulary, card sentences) sits near a 50% aggregate: it
minimises the sum of squared z-scores of the card-weighted yes rate over the shared features of a test build
(simulated annealing over rate swaps). The drawn multiset of rates is unchanged, so the per-card rates stay
U[20, 80] draws and the aggregate stays at 50%.

  python -m gen.rate_assign <build_tag>      -> gen/yesrate_assign.json
"""
from __future__ import annotations

import json
import math
import random
import re
import sys
from collections import defaultdict

from .common import TMP, GEN, rng_for
from . import plan

TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def main():
    tag = sys.argv[1]
    rows = [json.loads(l) for l in open(TMP / f"build_{tag}_rows.jsonl")]
    yn = [r for r in rows if r["qtype"] == "noul"]
    nrows = defaultdict(int)
    feat = defaultdict(lambda: defaultdict(int))
    for r in yn:
        c = r["meta"]["card_id"]
        nrows[c] += 1
        txt = "\n".join([r.get("card") or "", r["instructions"], r["state"]])
        for f in ngrams(txt):
            feat[f][c] += 1
    cards = sorted(nrows)
    # keep features shared by >= 2 cards with a non-trivial share of rows in each
    F = []
    for f, per in feat.items():
        # repair r1 v3d: G7's raw multi-card rule counts a feature in >= 2 cards with ANY row count (e.g. '11 count':
        # 74 rows of F6-S4-yn-07 + 15 rows of 5 other cards failed G7), so every card's rows count here (was >= 5)
        cs = dict(per)
        if len(cs) >= 2 and sum(cs.values()) >= 20 and len(cs) < len(cards) * 0.8:
            F.append(cs)
    allc = plan.plan_cards()
    base = plan.yes_rates(allc, "cand")
    rates = [base[c] for c in cards]
    idx = {c: i for i, c in enumerate(cards)}
    Fi = [[(idx[c], n) for c, n in cs.items()] for cs in F]
    var = [sum(n for _, n in fl) * 0.25 for fl in Fi]

    def score(rt):
        s = 0.0
        for fl, v in zip(Fi, var):
            z = sum(n * (rt[i] - 0.5) for i, n in fl) / math.sqrt(v)
            s += z * z
        return s
    by_card = defaultdict(list)
    for k, fl in enumerate(Fi):
        for i, n in fl:
            by_card[i].append((k, n))
    rng = rng_for("rate_assign", tag)
    cur = list(rates)
    S = [sum(n * (cur[i] - 0.5) for i, n in fl) for fl in Fi]
    # repair r1 v3c: tail objective. The G7 raw test fails a feature near |z| ~ 4.8 (Bonferroni); a pure z^4 sum left
    # 16-21 two-card features at expected |z| > 4. Penalise only the excess over Z0 (steeply), so the search spends
    # its swaps on the features that can fail, not on the bulk.
    Z0 = float(sys.argv[4]) if len(sys.argv) > 4 else 2.5   # v3d: optional tail threshold

    def g(x, v):
        z = abs(x) / math.sqrt(v)
        return (z - Z0) ** 4 * 100.0 + z * z if z > Z0 else z * z
    cs_ = sum(g(x, v) for x, v in zip(S, var))
    best, bs = list(cur), cs_
    T = 50.0
    for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 120000):
        i, j = rng.randrange(len(cur)), rng.randrange(len(cur))
        if i == j or cur[i] == cur[j]:
            continue
        d = {}
        for k, n in by_card[i]:
            d[k] = d.get(k, 0.0) + n * (cur[j] - cur[i])
        for k, n in by_card[j]:
            d[k] = d.get(k, 0.0) + n * (cur[i] - cur[j])
        delta = sum(g(S[k] + x, var[k]) - g(S[k], var[k]) for k, x in d.items())
        if delta < 0 or rng.random() < math.exp(-delta / T):
            for k, x in d.items():
                S[k] += x
            cur[i], cur[j] = cur[j], cur[i]
            cs_ += delta
            if cs_ < bs:
                best, bs = list(cur), cs_
        T *= 0.99993 ** (120000 / (int(sys.argv[2]) if len(sys.argv) > 2 else 120000))
    zmax = 0.0
    for fl, v in zip(Fi, var):
        z = abs(sum(n * (best[i] - 0.5) for i, n in fl) / math.sqrt(v))
        zmax = max(zmax, z)
    out = {"source_build": tag, "n_features": len(F), "score_before": round(score(rates), 2),
           "score_after": round(bs, 2), "max_abs_z_after": round(zmax, 2), "objective": f"tail Z0={Z0}",
           "n_abs_z_gt4_after": sum(1 for fl, v in zip(Fi, var)
                                    if abs(sum(n * (best[i] - 0.5) for i, n in fl) / math.sqrt(v)) > 4),
           "rates": {c: best[i] for i, c in enumerate(cards)}}
    json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else GEN / "yesrate_assign.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rates"}))


if __name__ == "__main__":
    main()
