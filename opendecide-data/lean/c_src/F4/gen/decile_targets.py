"""Repair r2 (G10, G0 8 decisive statement position, read literally): per-unit target deciles for the second build pass.

  python decile_targets.py cand   (reads out/candidates_r1.jsonl + .sidecar.jsonl of the first, untargeted pass)

Each kept row has a measured block and the set of literal deciles its last decisive statement can reach there
(sidecar decisive_reach: {floor(10 L / n) : L feasible}). A unit's rows share one target decile t; each row realises
the reachable decile nearest to t (ties: the lower), exactly as render_f4.decile_pick / _interleave_place do. The
targets minimise the summed chi-square statistic of the literal decile over the G10 cells (per sampler, per label tag,
per sampler x measured block) by local search from a stratified start. The block layout, the row's structure and its
label are not changed; only which feasible slot holds the last decisive statement. Output: gen/decile_targets_<set>.json
"""
from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}


def realise(reach, t):
    return min(reach, key=lambda d: (abs(d - t), d))


def chi(h):
    n = sum(h)
    if n == 0:
        return 0.0
    e = n / 10.0
    return sum((o - e) ** 2 / e for o in h)


def main(set_name):
    name = NAMES[set_name]
    rows = {}
    if len(sys.argv) > 2:      # test input: a build pickle (tmp/rows_<tag>.pkl) instead of the finalized files
        import pickle
        pk = pickle.load(open(sys.argv[2], "rb"))
        rows = {r["id"]: r for r in pk["rows"]}
        side_rows = pk["side"]
    else:
        for line in open(F4 / "out" / f"{name}.jsonl"):
            r = json.loads(line)
            rows[r["id"]] = r
        side_rows = (json.loads(line) for line in open(F4 / "out" / f"{name}.sidecar.jsonl"))
    units = collections.defaultdict(list)   # key -> [(cells, reach)]
    for s in side_rows:
        reach = s.get("decisive_reach")
        if not reach:
            continue
        r = rows[s["id"]]
        lab = next((t for t in r["meta"].get("edge", []) if str(t).startswith("L:")), None)
        cells = ("sampler=" + s["sampler"], "label=" + str(lab), f"sampler_x_block={s['sampler']}|{s['decisive_block']}")
        _, _, card_no, ui, _ = s["id"].split("-")
        units[f"{card_no}-{ui}"].append((cells, tuple(reach)))
    keys = sorted(units)
    rng = random.Random(f"f4-decile-targets:{set_name}")
    # stratified start: targets 0..9 in a shuffled cycle
    perm = list(range(len(keys)))
    rng.shuffle(perm)
    tgt = {keys[i]: perm.index(i) % 10 for i in range(len(keys))}
    hist = collections.defaultdict(lambda: [0] * 10)
    for k in keys:
        for cells, reach in units[k]:
            d = realise(reach, tgt[k])
            for c in cells:
                hist[c][d] += 1
    total0 = sum(chi(h) for h in hist.values())
    for sweep in range(40):
        moved = 0
        order = list(keys)
        rng.shuffle(order)
        for k in order:
            cur = tgt[k]
            touched = {c for cells, _ in units[k] for c in cells}
            for cells, reach in units[k]:      # take the unit out
                d = realise(reach, cur)
                for c in cells:
                    hist[c][d] -= 1
            best, best_cost = cur, None
            for t in range(10):
                for cells, reach in units[k]:
                    d = realise(reach, t)
                    for c in cells:
                        hist[c][d] += 1
                cost = sum(chi(hist[c]) for c in touched)
                for cells, reach in units[k]:
                    d = realise(reach, t)
                    for c in cells:
                        hist[c][d] -= 1
                if best_cost is None or cost < best_cost - 1e-12 or (abs(cost - best_cost) <= 1e-12 and t == cur):
                    best, best_cost = t, cost
            tgt[k] = best
            moved += best != cur
            for cells, reach in units[k]:
                d = realise(reach, best)
                for c in cells:
                    hist[c][d] += 1
        if moved == 0:
            break
    from scipy.stats import chisquare
    cells_out = {c: {"n": sum(h), "hist": h, "chi2_p": round(float(chisquare(h).pvalue), 5)}
                 for c, h in sorted(hist.items()) if sum(h) >= 50}
    out = {"set": set_name, "source": f"out/{name}.sidecar.jsonl (first, untargeted pass)", "units": len(keys),
           "sweeps": sweep + 1, "chi2_sum_start": round(total0, 2),
           "chi2_sum_end": round(sum(chi(h) for h in hist.values()), 2), "planned_cells": cells_out,
           "targets": tgt}
    json.dump(out, open(HERE / f"decile_targets_{set_name}.json", "w"), indent=0)
    worst = sorted(cells_out.items(), key=lambda kv: kv[1]["chi2_p"])[:5]
    print(json.dumps({"units": len(keys), "sweeps": sweep + 1, "chi2_sum_start": out["chi2_sum_start"],
                      "chi2_sum_end": out["chi2_sum_end"],
                      "worst": [(c, v["n"], v["chi2_p"]) for c, v in worst]}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
