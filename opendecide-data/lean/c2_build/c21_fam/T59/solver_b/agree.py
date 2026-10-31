"""T59 solver A-vs-B agreement harness (IN MEMORY, CPU only). NOT part of solver B: this file imports the generator side, solver B never does.

    PYTHONDONTWRITEBYTECODE=1 python3 agree.py --rows 1000 --seeds s1,s2 --out /path/to/scratch/report.json [--levers] [--log]

Builds rows with the family generator (generate_in_memory), hands solver B ONLY the pipeline's b-view (kpipeline.solver_b_view of the
canonical view: family, sub_block, options{letter,label,text}, rendered{context,question,options_text,text}) and compares its label and
letter with the record's gold / gold_letter, and render_b's letter with gold_letter. Nothing is written except --out (and, with --log, the
counts-only agreement_log.json beside this file). Row text, ids and names never leave memory.
K2 bar (G0-lite 8.1): agreement >= 99.0% per run; reported overall and per trigger (abstains count as non-agreement, as in the pipeline).
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM_T59 = os.path.dirname(HERE)
FAM_ROOT = os.path.dirname(FAM_T59)
for _p in (FAM_ROOT, FAM_T59):
    if _p not in sys.path:
        sys.path.insert(0, _p)

K2_BAR = 99.0


def _load_hook():
    import importlib
    return importlib.import_module("solver_b.hook")


def _view(rec):
    from LK_COMMON import kpipeline
    return kpipeline.solver_b_view(kpipeline.canonical_view(rec))


def build_rows(rows, seed, levers, standin=True):
    import t59_generator as g
    from t59_build import Ctx
    ctx = Ctx(seed=seed, standin=standin)
    recs = g.generate_in_memory(total=rows, seed=seed, ctx=ctx)
    extra = []
    if levers:
        import t59_levers as lv
        extra = lv.make_extra_rows(ctx, recs, a10=True, include_dev=True)
    return recs, extra


def evaluate(recs, hook, tag):
    out = {"rows": 0, "labelled": 0, "agree": 0, "disagree": 0, "abstain": 0}
    by = collections.defaultdict(lambda: {"rows": 0, "labelled": 0, "agree": 0, "disagree": 0, "abstain": 0})
    classes = collections.Counter()
    abstain_reasons = collections.Counter()
    dis_ids = []
    for rec in recs:
        v = _view(rec)
        res = hook.solver_b(v)
        rb = hook.render_b(v)
        st = rec["sub_block"]
        for d in (out, by[st]):
            d["rows"] += 1
        if res.abstain or res.label is None:
            for d in (out, by[st]):
                d["abstain"] += 1
            abstain_reasons[(st, res.reason)] += 1
            continue
        for d in (out, by[st]):
            d["labelled"] += 1
        ok = (res.label == rec["gold"] and res.letter == rec["gold_letter"] and rb == ("letter", rec["gold_letter"]))
        if ok:
            for d in (out, by[st]):
                d["agree"] += 1
        else:
            for d in (out, by[st]):
                d["disagree"] += 1
            if res.label != rec["gold"]:
                kind = "label differs"
            elif res.letter != rec["gold_letter"]:
                kind = "letter differs (option text vs gold letter)"
            else:
                kind = "render_b letter differs"
            classes["%s: B rule %s says %s, A gold %s (%s)" % (st, res.rule, res.label, rec["gold"], kind)] += 1
            dis_ids.append(rec["row_id"])
    return {"tag": tag, "total": out, "by_sub_block": dict(by), "classes": dict(classes),
            "abstain_reasons": {"%s|%s" % k: v for k, v in abstain_reasons.items()}, "_dis_ids": dis_ids}


B_REASONS = ("B_error", "B_abstain", "A_B_label_differs", "A_B_letter_differs", "render_fidelity", "render_unobservable")


def pipeline_pass(recs, hook):
    """check_row of the shared pipeline with solver B plugged into the family adapter (counts of B-related reasons only)."""
    import t59_checked
    from tool_engine import row_pipeline as rp
    ad = t59_checked.adapter(solver_b=hook.solver_b, render_b=hook.render_b)
    c = collections.Counter()
    c["rows"] = len(recs)
    for rec in recs:
        reasons, _notes = rp.check_row(rec, ad)
        for r in reasons:
            if r in B_REASONS:
                c[r] += 1
    return dict(c)


def pct(a, b):
    return round(100.0 * a / b, 3) if b else None


def merge(reports):
    tot = collections.Counter()
    by = collections.defaultdict(collections.Counter)
    classes = collections.Counter()
    ab = collections.Counter()
    for r in reports:
        tot.update(r["total"])
        for k, v in r["by_sub_block"].items():
            by[k].update(v)
        classes.update(r["classes"])
        ab.update(r["abstain_reasons"])
    return tot, by, classes, ab


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--seeds", default="a1,a2")
    ap.add_argument("--out", default=None)
    ap.add_argument("--levers", action="store_true", help="also check the derived A12 / A10 / dev lever rows (canonical view)")
    ap.add_argument("--log", action="store_true", help="write the counts-only agreement_log.json beside this file")
    ap.add_argument("--real-names", action="store_true", help="generate with standin=False (frozen namespace names instead of stand-ins)")
    ap.add_argument("--pipeline", action="store_true",
                    help="also run the family pipeline's check_row through t59_checked.adapter(solver_b=hook.solver_b, render_b=hook.render_b) "
                         "and count the B-related reasons")
    ap.add_argument("--dump-ids", default=None, help="write disagreeing row ids to this scratch path (never into the repo)")
    a = ap.parse_args(argv)
    hook = _load_hook()
    reports = []
    pipeline_runs = []
    for seed in [s for s in a.seeds.split(",") if s]:
        recs, extra = build_rows(a.rows, seed, a.levers, standin=not a.real_names)
        reports.append(evaluate(recs, hook, "clean:" + seed))
        if a.pipeline:
            pipeline_runs.append(pipeline_pass(recs + extra, hook))
        if extra:
            reports.append(evaluate(extra, hook, "levers:" + seed))
    tot, by, classes, ab = merge(reports)
    result = {"rows_requested_per_seed": a.rows, "seeds": a.seeds.split(","), "levers": a.levers,
              "total": dict(tot), "agreement_pct_labelled": pct(tot["agree"], tot["labelled"]),
              "agreement_pct_all": pct(tot["agree"], tot["rows"]), "k2_bar_pct": K2_BAR,
              "k2_pass": bool(tot["rows"]) and pct(tot["agree"], tot["rows"]) >= K2_BAR,
              "by_sub_block": {k: dict(v, agreement_pct_labelled=pct(v["agree"], v["labelled"]), agreement_pct_all=pct(v["agree"], v["rows"]),
                                       k2_pass=pct(v["agree"], v["rows"]) >= K2_BAR) for k, v in sorted(by.items())},
              "disagreement_classes": dict(classes), "abstain_reasons": dict(ab),
              "per_run": [{"tag": r["tag"], "total": r["total"]} for r in reports],
              "pipeline_check_row_b_reasons": pipeline_runs}
    print(json.dumps({k: v for k, v in result.items() if k != "per_run"}, indent=1, sort_keys=True))
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
    if a.dump_ids:
        with open(a.dump_ids, "w") as fh:
            json.dump([i for r in reports for i in r["_dis_ids"]], fh)
    if a.log:
        with open(os.path.join(HERE, "agreement_log.json"), "w") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
    return 0 if result["k2_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
