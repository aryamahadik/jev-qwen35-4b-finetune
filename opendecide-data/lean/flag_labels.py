"""Label-audit screen before 2B step 0 (FINETUNE_PLAN.md 3.4): flags 4B-E labels that disagree with gold, ranked within
groups (not one fixed p cut), and finds the groups (source x question-type bucket) whose flag rate stands out.

Flags (out-of-sample labelled rows only; designed-hard rows - attacked/definition-swap/fact-flip twins, near-miss rows -
are left out of the bug hunt unless --include-hard):
  yes/no:     p(gold) < --p-min after the yes/no temperature --T, or the lowest --low-frac of p(gold);
  choice:     the lowest --low-frac of p(gold) within option-count buckets 2-4 / 5-9 / 10-19 / 20+;
  vote share: rows with a human teacher where |p_teacher - share| >= --vote-gap (largest gap over the options).
Outlier groups: flag rate >= baseline of their bucket + --excess and n >= --min-n, ranked by excess x n. The audit
sample: --per-group flagged rows from each of the top --top groups, --n-spread flagged rows spread across groups, and
--n-human random disagreement rows from human-labelled (non-generator) sources. Nothing is dropped or relabelled here.

  python flag_labels.py --labels data/v14_label_shards/labels_q35_4b_pxE --shards-dir data/v14_label_shards
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import shard_golden as sg

HERE = Path(__file__).resolve().parent
HARD_ROLES = ("attacked", "defswap", "trap_aff", "trap_neg")


def designed_hard(r, inv_b=frozenset()) -> bool:
    """Rows built to be hard (their disagreement is the point, not a label bug)."""
    m = r.get("meta") or {}
    return (r["id"] in inv_b or r.get("role") in HARD_ROLES or bool(m.get("near_miss")) or "defswap" in m
            or "attack_target" in m or bool(m.get("twin_of")))


def is_generator(source: str) -> bool:
    return source.startswith("gd_gen")


def bucket(r) -> str:
    if r["qtype"] == "noul":
        return "yn"
    n = len(r["options"])
    return "2-4" if n <= 4 else "5-9" if n <= 9 else "10-19" if n <= 19 else "20+"


def temper(p, T):
    """p_yes through the yes/no temperature: sigmoid(logit(p) / T)."""
    p = min(max(float(p), 1e-7), 1 - 1e-7)
    return 1.0 / (1.0 + math.exp(-math.log(p / (1 - p)) / T))


def score_row(r, probs, T):
    """(p(gold), model distribution used for comparisons, model agrees with gold)."""
    if r["qtype"] == "noul":
        py = temper(probs["yes"], T)
        return (py if r["gold"] == 1 else 1 - py), {"yes": py}, (py >= 0.5) == (r["gold"] == 1)
    top = max(probs.values())
    best = [o for o, v in probs.items() if v == top]
    return float(probs.get(r["gold"], 0.0)), probs, best == [r["gold"]]


def vote_gap(r, dist):
    t = (r.get("meta") or {}).get("teacher")
    if not isinstance(t, dict) or not t or (r.get("meta") or {}).get("teacher_src") == "blend50":
        return None
    if r["qtype"] == "noul":
        return abs(dist["yes"] - float(t["yes"]))
    return max(abs(float(dist.get(o, 0.0)) - float(t.get(o, 0.0))) for o in r["options"])


def screen(rows, labels, inv_b=frozenset(), T=0.9, p_min=0.10, low_frac=0.03, vote_min=0.5, include_hard=False,
           group_key=lambda r: r["source"]):
    """Per-row records for every labelled, screened row: id, group, bucket, p_gold, agree, flags."""
    recs, n_hard = [], 0
    for r in rows:
        if r["id"] not in labels:
            continue
        if not include_hard and designed_hard(r, inv_b):
            n_hard += 1
            continue
        pg, dist, agree = score_row(r, labels[r["id"]], T)
        g = vote_gap(r, dist)
        recs.append({"id": r["id"], "group": group_key(r), "bucket": bucket(r), "source": r["source"], "p_gold": pg,
                     "agree": agree, "vote_gap": g, "flags": []})
    by_b = defaultdict(list)
    for x in recs:
        by_b[x["bucket"]].append(x)
    for b, xs in by_b.items():
        k = math.ceil(low_frac * len(xs))
        for x in sorted(xs, key=lambda x: (x["p_gold"], x["id"]))[:k]:
            x["flags"].append("lowest")
        if b == "yn":
            for x in xs:
                if x["p_gold"] < p_min:
                    x["flags"].append("p_below")
    for x in recs:
        if x["vote_gap"] is not None and x["vote_gap"] >= vote_min:
            x["flags"].append("vote_gap")
    return recs, n_hard


def group_table(recs, min_n=100, excess=0.02):
    """Rows per (group, bucket) cell with its flag rate, the bucket baseline and the excess; outliers ranked first by
    excess x n."""
    base_n, base_f = Counter(), Counter()
    cell_n, cell_f = Counter(), Counter()
    for x in recs:
        f = bool(x["flags"])
        base_n[x["bucket"]] += 1
        base_f[x["bucket"]] += f
        cell_n[(x["group"], x["bucket"])] += 1
        cell_f[(x["group"], x["bucket"])] += f
    baseline = {b: base_f[b] / base_n[b] for b in base_n}
    cells = []
    for (g, b), n in cell_n.items():
        rate = cell_f[(g, b)] / n
        ex = rate - baseline[b]
        cells.append({"group": g, "bucket": b, "n": n, "flagged": cell_f[(g, b)], "rate": round(rate, 4),
                      "baseline": round(baseline[b], 4), "excess": round(ex, 4), "score": round(ex * n, 2),
                      "outlier": n >= min_n and ex >= excess - 1e-12})
    cells.sort(key=lambda c: (not c["outlier"], -c["score"], c["group"], c["bucket"]))
    return cells, {b: round(v, 4) for b, v in baseline.items()}


def audit_sample(recs, cells, top=10, per_group=30, n_spread=100, n_human=100, seed=0):
    """[(audit_set, record)]: flagged rows from the top outlier groups, flagged rows spread across groups, and random
    disagreement rows from human-labelled sources. Seeded; no row appears twice."""
    rng = random.Random(seed)
    taken, out = set(), []
    flagged = defaultdict(list)
    for x in recs:
        if x["flags"]:
            flagged[(x["group"], x["bucket"])].append(x)
    for c in [c for c in cells if c["outlier"]][:top]:
        xs = sorted(flagged[(c["group"], c["bucket"])], key=lambda x: x["id"])
        for x in rng.sample(xs, min(per_group, len(xs))):
            out.append(("top_group", x))
            taken.add(x["id"])
    pools = {k: [x for x in sorted(v, key=lambda x: x["id"]) if x["id"] not in taken] for k, v in sorted(flagged.items())}
    for v in pools.values():
        rng.shuffle(v)
    keys = sorted(pools)
    rng.shuffle(keys)
    k = 0
    while k < n_spread and any(pools.values()):
        for key in keys:
            if k >= n_spread:
                break
            if pools[key]:
                x = pools[key].pop()
                out.append(("flagged_spread", x))
                taken.add(x["id"])
                k += 1
    dis = sorted((x for x in recs if not x["agree"] and not is_generator(x["source"]) and x["id"] not in taken),
                 key=lambda x: x["id"])
    for x in rng.sample(dis, min(n_human, len(dis))):
        out.append(("human_disagree", x))
    return out


def markdown(cells, baseline, top=10):
    lines = [f"Baselines (flag rate by bucket): {baseline}", "",
             "| group | bucket | n | flagged | rate | baseline | excess | excess x n |", "|---|---|---|---|---|---|---|---|"]
    for c in [c for c in cells if c["outlier"]][:max(top, 20)]:
        lines.append(f"| {c['group']} | {c['bucket']} | {c['n']} | {c['flagged']} | {c['rate']:.3f} | "
                     f"{c['baseline']:.3f} | {c['excess']:+.3f} | {c['score']:.1f} |")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, help="label dir from od_gcp.py label, or a preds .jsonl")
    ap.add_argument("--shards-dir", default="", help="read rows from the shards (and require every shard labelled)")
    ap.add_argument("--rows", default="", help="rows file instead of the shards (e.g. data/v14_parts/golden_train.jsonl)")
    ap.add_argument("--relations", default=str(sg.DATA / "v14_parts/golden_relations.jsonl"))
    ap.add_argument("--T", type=float, default=0.9, help="yes/no temperature; 0.9 = 4B-E's fitted value (the plan's "
                                                          "0.65 is the 2B arm-I fit, critic gap 11)")
    ap.add_argument("--p-min", dest="p_min", type=float, default=0.10)
    ap.add_argument("--low-frac", dest="low_frac", type=float, default=0.03)
    ap.add_argument("--vote-gap", dest="vote_gap", type=float, default=0.5)
    ap.add_argument("--min-n", dest="min_n", type=int, default=100)
    ap.add_argument("--excess", type=float, default=0.02)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--per-group", dest="per_group", type=int, default=30)
    ap.add_argument("--n-spread", dest="n_spread", type=int, default=100)
    ap.add_argument("--n-human", dest="n_human", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--include-hard", dest="include_hard", action="store_true")
    ap.add_argument("--out-dir", dest="out_dir", default="logs/label_audit")
    a = ap.parse_args(argv)
    if a.shards_dir:
        rows = [r for s in sg.shard_files(a.shards_dir) for r in sg.read_jsonl(s)]
    elif a.rows:
        rows = sg.read_jsonl(a.rows)
    else:
        raise SystemExit("pass --shards-dir or --rows")
    labels = sg.load_labels(Path(a.labels), Path(a.shards_dir) if a.shards_dir else None)
    rels = sg.read_jsonl(a.relations) if a.relations and Path(a.relations).exists() else []
    inv_b = frozenset(x["b"] for x in rels if x["type"] == "inv")
    recs, n_hard = screen(rows, labels, inv_b, a.T, a.p_min, a.low_frac, a.vote_gap, a.include_hard)
    cells, baseline = group_table(recs, a.min_n, a.excess)
    sample = audit_sample(recs, cells, a.top, a.per_group, a.n_spread, a.n_human, a.seed)
    out = Path(a.out_dir) if Path(a.out_dir).is_absolute() else HERE / a.out_dir
    out.mkdir(parents=True, exist_ok=True)
    params = {k: v for k, v in vars(a).items()}
    summary = {"params": params, "screened": len(recs), "designed_hard_skipped": n_hard,
               "flagged": sum(bool(x["flags"]) for x in recs),
               "flags": dict(Counter(f for x in recs for f in x["flags"])), "baseline": baseline,
               "outliers": [c for c in cells if c["outlier"]], "cells": cells}
    sg.write_json_atomic(out / "flag_groups.json", summary)
    by_id = {r["id"]: r for r in rows}
    sg.write_atomic(out / "audit_rows.jsonl",
                    [json.dumps({"audit_set": s, **x, "probs": labels[x["id"]], **{k: by_id[x["id"]].get(k) for k in (
                        "qtype", "gold", "options", "instructions", "card", "state", "meta")}}) for s, x in sample])
    print(json.dumps({k: summary[k] for k in ("screened", "designed_hard_skipped", "flagged", "flags", "baseline")}))
    print(markdown(cells, baseline, a.top))
    print(f"audit sample: {Counter(s for s, _ in sample)} -> {out / 'audit_rows.jsonl'}")
    return summary, sample


if __name__ == "__main__":
    main()
