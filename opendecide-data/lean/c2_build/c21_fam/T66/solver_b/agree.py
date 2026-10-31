"""In-memory agreement harness for T66 solver B.

    PYTHONDONTWRITEBYTECODE=1 python3 agree.py --rows 2000 --seeds 1,2,3 --out PATH [--log agreement_log.json] [--msg-pool PATH]

Builds rows with the family generator IN MEMORY (stand-in executor; nothing is written, nothing is executed), hands solver B ONLY `schema.b_view(rec)`, and compares B's
label and option letter with the record's gold. MERGE / SEMVER wording comes from the repo pool; the MSG change-form wordings are not written yet, so the harness overlays
the TEST-ONLY stand-in pool `testpool_msg.json` (override with --msg-pool). --out gets the full JSON report (row ids included: keep it in a scratch folder);
--log gets the counts-only summary that may live in the repo."""
import argparse
import collections
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(os.path.dirname(HERE))
if FAM not in sys.path:
    sys.path.insert(0, FAM)

from T66 import generator, schema                                  # noqa: E402  (generator side: allowed in the harness only)
from T66.solver_b import hook, msg_lex                             # noqa: E402

BAR = 0.99


def load_pool(msg_pool_path):
    with open(os.path.join(FAM, "T66", "pools", "wording_pool.json"), "r", encoding="utf-8") as f:
        pool = json.load(f)
    with open(msg_pool_path, "r", encoding="utf-8") as f:
        extra = json.load(f)
    for k, v in extra["forms"].items():
        pool["forms"][k] = v
    return pool


def build_rows(total, seed, pool):
    ctx = generator.Ctx(seed=seed, standin=True, pool=pool)
    rows, rejects = [], 0
    for g in generator.build_plan(total=total, seed=seed):
        try:
            rows += generator.generate_group(ctx, g)
        except Exception:                                          # noqa: BLE001 - the generator could not realise the group: counted, not B's business
            rejects += 1
    return rows, rejects


def kind_of(rec):
    cid = rec["meta"]["construction_id"]
    return cid.split(":")[0] if rec["head"] == "MSG" else cid


def run(total, seeds, msg_pool, keep_rows=False):
    pool = load_pool(msg_pool)
    heads = ("MERGE", "SEMVER", "MSG")
    st = {h: collections.Counter() for h in heads}
    by_kind = {h: collections.defaultdict(collections.Counter) for h in heads}
    classes = collections.Counter()
    abst = collections.Counter()
    detail = []
    gen_rejects = 0
    t0 = time.time()
    for seed in seeds:
        rows, rj = build_rows(total, seed, pool)
        gen_rejects += rj
        for rec in rows:
            h = rec["head"]
            res = hook.solver_b(schema.b_view(rec))
            c, k = st[h], kind_of(rec)
            c["rows"] += 1
            by_kind[h][k]["rows"] += 1
            if res["status"] != "ok":
                c["abstain"] += 1
                by_kind[h][k]["abstain"] += 1
                abst["%s|%s|%s" % (h, res["status"], res["why"].split(":")[0][:48])] += 1
                detail.append(dict(seed=seed, row_id=rec["row_id"], head=h, kind=k, status=res["status"], why=res["why"], gold=rec["gold"]))
                continue
            c["labelled"] += 1
            ok = res["label"] == rec["gold"] and res["letter"] == rec["gold_letter"]
            if ok:
                c["agree"] += 1
                by_kind[h][k]["agree"] += 1
            else:
                c["disagree"] += 1
                by_kind[h][k]["disagree"] += 1
                classes["%s|%s|B=%s gold=%s|%s" % (h, k, res["label"], rec["gold"], res["why"][:40])] += 1
                detail.append(dict(seed=seed, row_id=rec["row_id"], head=h, kind=k, status="disagree", why=res["why"], gold=rec["gold"], b=res["label"]))
    tot = collections.Counter()
    for h in heads:
        tot.update(st[h])
    def pct(a, b):
        return round(100.0 * a / b, 3) if b else None
    summary = {}
    for h, c in list(st.items()) + [("ALL", tot)]:
        summary[h] = dict(rows=c["rows"], b_labelled=c["labelled"], agree=c["agree"], disagree=c["disagree"], b_abstained=c["abstain"],
                          agreement_pct_labelled=pct(c["agree"], c["labelled"]), agreement_pct_all=pct(c["agree"], c["rows"]),
                          meets_bar_099_labelled=(c["agree"] >= BAR * c["labelled"]) if c["labelled"] else None)
    report = dict(seeds=list(seeds), total_param=total, generator_group_rejects=gen_rejects, seconds=round(time.time() - t0, 1), summary=summary,
                  by_construction_kind={h: {k: dict(v) for k, v in sorted(d.items())} for h, d in by_kind.items()},
                  disagreement_classes=dict(classes.most_common()), abstain_classes=dict(abst.most_common()))
    return report, detail


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000, help="plan size per seed (rows actually built are ~15%% higher: oversampling)")
    ap.add_argument("--seeds", default="1,2")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None, help="counts-only summary (no ids, no text); appended as one run entry")
    ap.add_argument("--msg-pool", default=os.path.join(HERE, "testpool_msg.json"))
    ap.add_argument("--min-top", type=int, default=None, help="override msg_lex.MIN_TOP for this run (harness only)")
    ap.add_argument("--min-margin", type=int, default=None, help="override msg_lex.MIN_MARGIN for this run (harness only)")
    a = ap.parse_args(argv)
    if a.min_top is not None:
        msg_lex.MIN_TOP = a.min_top
    if a.min_margin is not None:
        msg_lex.MIN_MARGIN = a.min_margin
    report, detail = run(a.rows, [int(x) for x in a.seeds.split(",")], a.msg_pool)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(dict(report, rows_detail=detail), f, indent=1, sort_keys=True)
    if a.log:
        entry = dict(msg_pool=os.path.basename(a.msg_pool), msg_min_top=msg_lex.MIN_TOP, msg_min_margin=msg_lex.MIN_MARGIN, seeds=report["seeds"], plan_rows_per_seed=a.rows, summary=report["summary"],
                     by_construction_kind=report["by_construction_kind"], disagreement_classes=report["disagreement_classes"],
                     abstain_classes=report["abstain_classes"])
        runs = []
        if os.path.exists(a.log):
            with open(a.log, "r", encoding="utf-8") as f:
                runs = json.load(f).get("runs", [])
        runs.append(entry)
        note = ("counts only (no row text, ids or names). MERGE / SEMVER wording is the repo pool; the MSG change-form wordings are TEST-ONLY stand-in pools "
                "because the production MSG message pool is not written yet.")
        with open(a.log, "w", encoding="utf-8") as f:
            json.dump(dict(note=note, runs=runs), f, indent=1, sort_keys=True)
    print(json.dumps(report["summary"], indent=1))
    print("disagreement classes:", json.dumps(report["disagreement_classes"], indent=1)[:3000])
    print("abstain classes:", json.dumps(report["abstain_classes"], indent=1)[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
