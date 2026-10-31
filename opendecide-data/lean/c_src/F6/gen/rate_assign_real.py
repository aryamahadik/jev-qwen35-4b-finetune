"""Card yes-rate swaps against REALISED feature counts (repair r1 v3f; G7 raw multi-card yes/no features).

gen/rate_assign.py permutes the drawn U[20, 80] card rates to keep every multi-card word / word pair near a 50% yes
aggregate, scoring EXPECTED counts (rate x rows). On the v3f pool one feature still failed G7's raw multi-card test:
'18 count' (69 rows; 57 carry it in the F6-S3-yn-11 card text, card rate 0.238, plus 12 S4 record rows that came out
all No by chance; p_raw 1.31e-6 vs Bonferroni 1.42e-6; card-adjusted p 0.25). Expected-count scoring cannot see the
realised part. Builds are deterministic per card and rate (same plan, same seeds), so the rows of a card whose rate
is unchanged come out identical in the next build. This step therefore scores, per feature, the REALISED yes count
of the last build plus the expected change on cards whose rate moves:

    yes'(f) = yes(f) + sum_c n(f, c) * (r'_c - r_c)

and makes at most MAX_SWAPS greedy best-improving swaps of two cards' rates (tail objective as rate_assign: steep
above Z0). It never reads or changes a row, never relabels: it only re-decides which card carries which of the drawn
rates (the multiset of rates, so the per-card U[20, 80] draws and the 50% aggregate, is unchanged), and the next
build regenerates every row of a swapped card from its plan.

  python -m gen.rate_assign_real <pool jsonl> [max_swaps] [Z0]   -> gen/yesrate_assign.json (old kept in _prev)
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict

from .common import GEN

sys.path.insert(0, str(GEN.parent / "qc"))
from g7 import ngrams          # noqa: E402  (the checker's own G7 tokeniser and n-grams)
import qc_lib as q            # noqa: E402

N_MIN = 20


def main():
    pool = sys.argv[1]
    max_swaps = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    z0 = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
    ra = json.load(open(GEN / "yesrate_assign.json"))
    rates = dict(ra["rates"])
    n = defaultdict(lambda: defaultdict(int))
    y = defaultdict(int)
    for line in open(pool):
        r = json.loads(line)
        if not q.is_yn(r):
            continue
        c = r["meta"]["card_id"]
        g = 1 if r["gold"] in (1, True, "yes", "Yes") else 0
        for f in ngrams(q.full_text(r)):
            n[f][c] += 1
            y[f] += g
    feats = [(f, dict(per), sum(per.values()), y[f]) for f, per in n.items()
             if len(per) >= 2 and sum(per.values()) >= N_MIN and all(c in rates for c in per)]
    by_card = defaultdict(list)
    for k, (f, per, m, yy) in enumerate(feats):
        for c, x in per.items():
            by_card[c].append((k, x))
    dev = [yy - m / 2.0 for f, per, m, yy in feats]      # realised yes minus 50%
    sd = [math.sqrt(m / 4.0) for f, per, m, yy in feats]

    def g(d, s):
        z = abs(d) / s
        return (z - z0) ** 4 * 100.0 + z * z if z > z0 else z * z

    def zmax(dv):
        return max(abs(d) / s for d, s in zip(dv, sd))

    cards = sorted(c for c in rates if c in by_card)
    before = {"max_abs_z": round(zmax(dev), 2), "n_gt4": sum(1 for d, s in zip(dev, sd) if abs(d) / s > 4),
              "n_gt3.5": sum(1 for d, s in zip(dev, sd) if abs(d) / s > 3.5)}
    swaps = []
    for _ in range(max_swaps):
        best = (0.0, None)
        for i, a in enumerate(cards):
            for b in cards[i + 1:]:
                if rates[a] == rates[b]:
                    continue
                dd = defaultdict(float)
                for k, x in by_card[a]:
                    dd[k] += x * (rates[b] - rates[a])
                for k, x in by_card[b]:
                    dd[k] += x * (rates[a] - rates[b])
                delta = sum(g(dev[k] + v, sd[k]) - g(dev[k], sd[k]) for k, v in dd.items())
                if delta < best[0]:
                    best = (delta, (a, b, dd))
        if best[1] is None:
            break
        a, b, dd = best[1]
        for k, v in dd.items():
            dev[k] += v
        swaps.append({"a": a, "b": b, "rate_a": round(rates[b], 4), "rate_b": round(rates[a], 4),
                      "objective_delta": round(best[0], 1)})
        rates[a], rates[b] = rates[b], rates[a]
    after = {"max_abs_z": round(zmax(dev), 2), "n_gt4": sum(1 for d, s in zip(dev, sd) if abs(d) / s > 4),
             "n_gt3.5": sum(1 for d, s in zip(dev, sd) if abs(d) / s > 3.5)}
    worst = sorted(((abs(d) / s, feats[k][0], feats[k][2]) for k, (d, s) in enumerate(zip(dev, sd))), reverse=True)[:5]
    out = dict(ra)
    out["_prev_rates"] = ra["rates"]
    out["rates"] = rates
    out["real_swaps"] = {"_doc": "gen/rate_assign_real.py (repair r1 v3f): greedy rate swaps scored on the realised "
                                 "feature counts of the pool below plus the expected change on swapped cards",
                         "pool": pool.split("/")[-1], "max_swaps": max_swaps, "Z0": z0, "n_features": len(feats),
                         "before": before, "after_estimated": after, "swaps": swaps,
                         "worst_after": [[round(a, 2), f, m] for a, f, m in worst]}
    json.dump(out, open(GEN / "yesrate_assign.json", "w"), indent=1)
    print(json.dumps(out["real_swaps"]))


if __name__ == "__main__":
    main()
