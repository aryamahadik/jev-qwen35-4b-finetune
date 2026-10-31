"""In-memory agreement harness (the ONLY module of solver_b that imports the generator side). Builds rows with the T67 generator, hands solver B the b-view only,
and compares B's answer with the record's gold and gold letter. Nothing is written except the JSON report at --out (counts only; no row text, ids or names).

    PYTHONDONTWRITEBYTECODE=1 python3 -m T67.solver_b.agree --rows 1200 --seeds 11,12 --out /path/report.json   (run with c21_fam on PYTHONPATH)
"""
import argparse
import collections
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(_HERE))
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)

from T67 import generator, heads, schema                       # noqa: E402  (generator side: harness only)
from T67.solver_b import hook                                  # noqa: E402

POOL = os.path.join(os.path.dirname(_HERE), "pools", "wording_pool.json")
BAR = 0.99


def build_rows(seed, total):
    with open(POOL) as fh:
        pool = json.load(fh)
    ctx = generator.Ctx(seed=seed, standin=True, pool=pool)
    plan = list(generator.build_plan(total=total, seed=seed))
    recs = []
    for g in plan:
        recs += generator.generate_group(ctx, g)
    head_rows = heads.extra_rows(ctx, recs)
    return recs, head_rows


def run(rows, seeds, solver=None, keep_examples=0):
    solver = solver or hook.solver_b
    stats = collections.defaultdict(lambda: collections.Counter())
    classes = collections.Counter()
    abstain_why = collections.Counter()
    confusion = collections.Counter()
    coverage = collections.Counter()
    examples = []
    for seed in seeds:
        recs, head_rows = build_rows(seed, rows)
        for rec in recs + head_rows:
            res = solver(schema.b_view(rec))
            blk = rec["sub_block"]
            keys = [("ALL", "ALL"), (rec["head"], "ALL"), (rec["head"], rec["witness_inputs"]["carrier"]), (rec["head"], blk)]
            for k in keys:
                stats[k]["rows"] += 1
            if res.get("status") != "ok":
                for k in keys:
                    stats[k]["abstain" if res.get("status") == "abstain" else "error"] += 1
                abstain_why[(rec["head"], blk, res.get("status"), str(res.get("why"))[:40])] += 1
                continue
            confusion["%s gold=%s B=%s" % (rec["head"], rec["gold"], res["label"])] += 1
            if rec["head"] == "T67-GATE":
                for r_ in res.get("rules", ()):
                    coverage["live:" + r_] += 1
                for r_ in res.get("cleared", ()):
                    coverage["cleared:" + r_] += 1
            for k in keys:
                stats[k]["labelled"] += 1
            agree = res["label"] == rec["gold"] and res.get("letter") == rec.get("gold_letter")
            for k in keys:
                stats[k]["agree" if agree else "disagree"] += 1
            if not agree:
                sig = "%s|%s|gold=%s|B=%s|rules=%s|cleared=%s|cell=%s" % (rec["head"], blk, rec["gold"], res["label"], ",".join(res.get("rules", ())),
                                                                       ",".join(res.get("cleared", ())), rec["meta"].get("cell"))
                classes[sig] += 1
                if len(examples) < keep_examples:
                    examples.append((rec, res))
    run.confusion, run.coverage = confusion, coverage
    return stats, classes, abstain_why, examples


def summarise(stats):
    out = {}
    for (head, part), c in sorted(stats.items()):
        lab = c["labelled"]
        out["%s/%s" % (head, part)] = dict(rows=c["rows"], labelled=lab, agree=c["agree"], disagree=c["disagree"], abstain=c["abstain"], error=c["error"],
                                           agree_pct_labelled=round(100.0 * c["agree"] / lab, 2) if lab else None,
                                           agree_pct_all=round(100.0 * c["agree"] / c["rows"], 2) if c["rows"] else None)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1200)
    ap.add_argument("--seeds", default="11,12")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    seeds = [int(x) for x in a.seeds.split(",")]
    stats, classes, why, _ = run(a.rows, seeds)
    rep = dict(rows_param=a.rows, seeds=seeds, bar_pct=BAR * 100, summary=summarise(stats),
               confusion=dict(sorted(run.confusion.items())), rule_coverage_gate_rows=dict(sorted(run.coverage.items())), disagreement_signatures=dict(classes.most_common()), abstain_reasons={"|".join(map(str, k)): v for k, v in why.most_common()})
    with open(a.out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    allc = rep["summary"]["ALL/ALL"]
    print("rows %d labelled %d agree %d disagree %d abstain %d error %d | agree%% labelled %s all %s | bar %.1f" %
          (allc["rows"], allc["labelled"], allc["agree"], allc["disagree"], allc["abstain"], allc["error"], allc["agree_pct_labelled"], allc["agree_pct_all"], BAR * 100))
    return 0


if __name__ == "__main__":
    sys.exit(main())
