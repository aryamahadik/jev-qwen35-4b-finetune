#!/usr/bin/env python3
"""public-3 self-check (counts only, no text): G10-style balance on a row file.

Per dataset x framing: rows, yes rate per wording (yes/no rows), gold class counts and max share (choice), wording x
gold-class chi-square p (choice), gold position per k (chi-square p), "longest option is gold" rate vs mean 1/k,
negated-wording share, cards / wordings / defs styles / format styles, twin units, records per text (must be 1).
Usage: selfcheck.py FILE.jsonl [OUT.json]
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict


def chi2_p(obs: list[list[int]]) -> float:
    """Pearson chi-square test of independence on a contingency table; p via the regularized gamma (Wilson-Hilferty
    approximation is enough here)."""
    rows = [r for r in obs if sum(r) > 0]
    if len(rows) < 2:
        return 1.0
    cols = [j for j in range(len(rows[0])) if sum(r[j] for r in rows) > 0]
    if len(cols) < 2:
        return 1.0
    t = [[r[j] for j in cols] for r in rows]
    n = sum(map(sum, t))
    rs = [sum(r) for r in t]
    cs = [sum(t[i][j] for i in range(len(t))) for j in range(len(cols))]
    x2 = sum((t[i][j] - rs[i] * cs[j] / n) ** 2 / (rs[i] * cs[j] / n) for i in range(len(t)) for j in range(len(cols)))
    df = (len(t) - 1) * (len(cols) - 1)
    z = ((x2 / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return 0.5 * math.erfc(z / math.sqrt(2))


def gof_p(counts: list[int]) -> float:
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return 1.0
    e = n / k
    x2 = sum((c - e) ** 2 / e for c in counts)
    df = k - 1
    z = ((x2 / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return 0.5 * math.erfc(z / math.sqrt(2))


def check(rows):
    out = {}
    by = defaultdict(list)
    for r in rows:
        by[(r["source"], r["id"].split("-")[2])].append(r)
    for (src, fr), rs in sorted(by.items()):
        d = {"rows": len(rs), "cards": len({r["meta"]["card_id"] for r in rs}),
             "wordings": len({r["meta"]["wording_id"] for r in rs}),
             "defs_styles": dict(Counter(r["meta"]["defs_style"] for r in rs)),
             "format_styles": len({r["meta"]["format_style"] for r in rs}),
             "twin_rows": sum(1 for r in rs if r["meta"].get("twin_of"))}
        yn = [r for r in rs if r["qtype"] == "noul"]
        ch = [r for r in rs if r["qtype"] == "choice"]
        if yn:
            d["yes_rate"] = round(sum(r["gold"] for r in yn) / len(yn), 4)
            wr = defaultdict(list)
            for r in yn:
                wr[r["meta"]["wording_id"]].append(r["gold"])
            d["yes_rate_by_wording"] = {w: [len(g), round(sum(g) / len(g), 3)] for w, g in sorted(wr.items())}
            d["max_wording_yes_dev_pp"] = round(max(abs(sum(g) / len(g) - 0.5) for g in wr.values()) * 100, 1)
            d["neg_wording_share"] = round(sum(r["role"] == "neg" for r in yn) / len(yn), 3)
            asked = defaultdict(list)
            for r in yn:
                if "asked" in r["meta"]:
                    asked[str(r["meta"]["asked"]) + "|" + str(r["meta"].get("asked_polarity", ""))].append(r["gold"])
            if asked and len(asked) <= 40:
                d["yes_rate_by_asked"] = {a: [len(g), round(sum(g) / len(g), 3)] for a, g in sorted(asked.items())}
        if ch:
            gc = Counter(r["gold"] for r in ch)
            d["gold_classes"] = len(gc)
            d["gold_max_share"] = round(max(gc.values()) / len(ch), 3) if len(gc) <= 12 else None
            if len(gc) <= 12:
                ws = sorted({r["meta"]["wording_id"] for r in ch})
                cl = sorted(gc)
                t = [[sum(1 for r in ch if r["meta"]["wording_id"] == w and r["gold"] == c) for c in cl] for w in ws]
                d["wording_x_gold_chi2_p"] = round(chi2_p(t), 4)
            pos = defaultdict(lambda: Counter())
            for r in ch:
                pos[len(r["options"])][r["options"].index(r["gold"])] += 1
            d["gold_pos_p_by_k"] = {k: round(gof_p([c[i] for i in range(k)]), 4) for k, c in sorted(pos.items())}
            lg = []
            for r in ch:                                   # tie-aware: credit 1/t when gold is among t longest
                m = max(len(o) for o in r["options"])
                t = [o for o in r["options"] if len(o) == m]
                lg.append(1 / len(t) if r["gold"] in t else 0.0)
            d["longest_is_gold_rate"] = round(sum(lg) / len(lg), 3)
            d["mean_inv_k"] = round(sum(1 / len(r["options"]) for r in ch) / len(ch), 3)
            d["option_counts"] = dict(Counter(len(r["options"]) for r in ch))
        out[f"{src}:{fr}"] = d
    texts = Counter()
    for r in rows:
        recs = r["meta"]["record_uid"] if isinstance(r["meta"]["record_uid"], list) else [r["meta"]["record_uid"]]
        for x in set(recs):
            texts[(x, r["group_id"])] += 1
    rec_groups = Counter(x for x, _ in texts)
    out["_records_in_more_than_one_group"] = sum(1 for v in rec_groups.values() if v > 1)
    out["_rows"] = len(rows)
    out["_yes_no_share"] = round(sum(r["qtype"] == "noul" for r in rows) / max(1, len(rows)), 3)
    return out


if __name__ == "__main__":
    rows = [json.loads(l) for l in open(sys.argv[1])]
    res = check(rows)
    s = json.dumps(res, indent=1)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(s)
    print(s)
