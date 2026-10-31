#!/usr/bin/env python3
"""G10 balance for public-3 (independent checker, prep5/B4; own code, counts only, never prints row text).

Spec 8 G10, with the public dataset as the "family":
  yes/no (qtype noul): yes rate 50% +/- 2 pp per dataset x wording_id x difficulty_bin x negation count
           (negation = role "neg"); also the aggregate per dataset.
  choice : canonical gold position uniform per option bucket k (chi-square p > 0.01) per dataset and pooled;
           "longest option is gold" (tie-aware: 1/t when gold is among t longest, characters) within +/- 2 pp of
           mean 1/k per dataset (pooled over its choice rows) and per dataset x k;
           abstain-like options (regex) wrong on >= 50% of rows that show them;
           (gate = the dataset-pooled rate, the family-level reading the F11 checker uses; dataset x k cells are
           reported with a two-sided normal p, info only, as spec G10 names no per-k rule for this check);
           "attack present" (meta.edge / meta.twin_kind / role naming an injection) vs label: reported (n).
Run on rows_r1 (the training rows), reserve and their union (rows a refill can bring in). The gate is on each file
and the union. Writes qc/g10.json."""
import json, math, re
from collections import Counter, defaultdict
from pathlib import Path
from scipy.stats import chisquare, norm

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
FILES = {"rows_r1": ["public3_rows_r1.jsonl"], "reserve": ["public3_reserve.jsonl"],
         "union": ["public3_rows_r1.jsonl", "public3_reserve.jsonl"]}
ABST = re.compile(r"\b(cannot|can't|not enough|unclear|unknown|none of (the|these)|undetermined|insufficient|"
                  r"not sure|no clear|can not)\b", re.I)
ATT = re.compile(r"attack|inject", re.I)


def check(rows):
    prob, res = [], {}
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    cell = defaultdict(lambda: [0, 0])
    agg = defaultdict(lambda: [0, 0])
    for r in yn:
        k = (r["source"], r["meta"].get("wording_id"), str(r["meta"].get("difficulty_bin")), int(r["role"] == "neg"))
        cell[k][0] += r["gold"] == 1
        cell[k][1] += 1
        agg[r["source"]][0] += r["gold"] == 1
        agg[r["source"]][1] += 1
    dev = {"|".join(map(str, k)): round(100 * (y / n - 0.5), 2) for k, (y, n) in cell.items()}
    worst = max(dev.items(), key=lambda x: abs(x[1])) if dev else None
    res["yn"] = {"rows": len(yn), "cells": len(cell), "cells_over_2pp": sum(abs(v) > 2 for v in dev.values()),
                 "worst_cell_dev_pp": worst, "min_cell_n": min((n for _, n in cell.values()), default=0),
                 "yes_rate_by_dataset": {k: round(y / n, 4) for k, (y, n) in agg.items()}}
    if res["yn"]["cells_over_2pp"] or any(abs(y / n - 0.5) > 0.02 for y, n in agg.values()):
        prob.append("yes rate")
    pos = defaultdict(Counter)
    lg = defaultdict(list)
    ab = [0, 0]
    att = Counter()
    for r in ch:
        o, g, k = r["options"], r["gold"], len(r["options"])
        gi = o.index(g)
        pos[(r["source"], k)][gi] += 1
        pos[("ALL", k)][gi] += 1
        m = max(len(x) for x in o)
        t = [i for i, x in enumerate(o) if len(x) == m]
        credit = (1 / len(t)) if gi in t else 0.0
        lg[(r["source"], k)].append((credit, 1 / k))
        lg[(r["source"], "all")].append((credit, 1 / k))
        for i, x in enumerate(o):
            if ABST.search(x):
                ab[0] += i != gi
                ab[1] += 1
    for r in rows:
        if ATT.search(json.dumps([r["meta"].get("edge"), r["meta"].get("twin_kind"), r.get("role")])):
            att[str(r["gold"])] += 1
    pp = {}
    for key, c in pos.items():
        obs = [c[i] for i in range(key[1])]
        p = float(chisquare(obs).pvalue) if sum(obs) and key[1] > 1 else 1.0
        pp["|".join(map(str, key))] = {"n": sum(obs), "p": round(p, 4)}
    res["gold_position"] = {"buckets": len(pp), "min_p": min((v["p"] for v in pp.values()), default=1.0),
                            "fail": [k for k, v in pp.items() if v["p"] <= 0.01]}
    if res["gold_position"]["fail"]:
        prob.append("gold position")
    lr = {}
    for key, v in lg.items():
        rate, base = sum(a for a, _ in v) / len(v), sum(b for _, b in v) / len(v)
        var = sum(b * (1 - b) for _, b in v)
        z = (sum(a for a, _ in v) - sum(b for _, b in v)) / math.sqrt(var) if var else 0.0
        lr["|".join(map(str, key))] = {"n": len(v), "rate": round(rate, 4), "mean_inv_k": round(base, 4),
                                       "dev_pp": round(100 * (rate - base), 2), "p_two_sided": round(2 * norm.sf(abs(z)), 4)}
    res["longest_is_gold"] = {"by": lr, "fail_dataset_pooled": [k for k, v in lr.items()
                                                                if k.endswith("|all") and abs(v["dev_pp"]) > 2],
                              "over_2pp_dataset_x_k": [k for k, v in lr.items()
                                                       if not k.endswith("|all") and abs(v["dev_pp"]) > 2]}
    if res["longest_is_gold"]["fail_dataset_pooled"]:
        prob.append("longest option is gold")
    res["abstain"] = {"rows_showing": ab[1], "wrong_share": round(ab[0] / ab[1], 4) if ab[1] else None}
    if ab[1] and ab[0] / ab[1] < 0.5:
        prob.append("abstain")
    res["attack_rows_by_gold"] = dict(att)
    if att and len(att) == 1 and sum(att.values()) >= 20:
        prob.append("attack present correlates with label")
    return prob, res


def main():
    out = {"gate": "G10", "files": {}}
    allp = []
    for name, fs in FILES.items():
        rows = [json.loads(l) for f in fs for l in open(OUT / f)]
        p, r = check(rows)
        out["files"][name] = {"pass": not p, "problems": p, **r}
        allp += [f"{name}: {x}" for x in p]
    out["pass"] = not allp
    out["problems"] = allp
    (HERE / "g10.json").write_text(json.dumps(out, indent=1))
    for name, f in out["files"].items():
        print(name, f["pass"], f["problems"], "yn", {k: f["yn"][k] for k in ("rows", "cells", "cells_over_2pp",
              "worst_cell_dev_pp", "min_cell_n")}, "pos_min_p", f["gold_position"]["min_p"],
              "longest", f["longest_is_gold"]["fail_dataset_pooled"], [(k, v["dev_pp"], v["n"], v["p_two_sided"]) for k, v in f["longest_is_gold"]["by"].items() if k in f["longest_is_gold"]["over_2pp_dataset_x_k"]],
              "abst", f["abstain"], "att", f["attack_rows_by_gold"])


if __name__ == "__main__":
    main()
