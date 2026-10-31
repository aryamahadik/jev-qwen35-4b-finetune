"""T60 solver B agreement harness (in memory; CPU; nothing is written into the repo except, on request, the counts-only agreement_log.json).

    PYTHONDONTWRITEBYTECODE=1 python3 agree.py --rows 1000 --seeds t60-agree-1,t60-agree-2 --out SCRATCH/agree.json [--log] [--standin] [--no-levers]

Only THIS file imports the generator side. It builds rows with t60_generator (the wording pool, as the real run does), derives the pipeline's
b-view of each row (kpipeline.solver_b_view of the canonical view), runs solver B on that view ONLY, and compares with the record's gold and
gold letter. It also runs the A12 perturbation rows (and, with --a10, the A10 wrapper rows) through the same path.
Report: rows, B-labelled, agree, disagree, B-abstained, agreement % (over labelled and over all), by sub_block, disagreement classes as COUNTS."""
import argparse
import collections
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM_DIR = os.path.dirname(_HERE)                          # .../c21_fam/T60
_ROOT = os.path.dirname(_FAM_DIR)                          # .../c21_fam
for _p in (_ROOT, _FAM_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import hook                                                   # noqa: E402  (solver B)
import t60b_h2 as h2mod                                       # noqa: E402
from LK_COMMON import kpipeline                               # noqa: E402  (b-view builder, shared glue)
from tool_engine.wording import WordingPool                   # noqa: E402
import t60_generator as gen                                   # noqa: E402  (generator side: ONLY this file imports it)
import t60_levers as lev                                      # noqa: E402

POOL = os.path.join(_FAM_DIR, "pools", "wording_pool_v1.json")
BAR = 99.0                                                    # G0-lite K2: agreement >= 99.0% per row on the pilot


def build_rows(rows, seed, standin=False, levers=True, a10=False):
    pool = None if standin else WordingPool.from_json(POOL)
    ctx = gen.Ctx(seed=seed, standin=standin, pool=pool)
    recs = gen.generate_in_memory(total=rows, seed=seed, standin=standin, ctx=ctx)
    extra = lev.make_extra_rows(ctx, recs, a10=a10, include_dev=True) if levers else []
    return recs, extra


def check_one(rec):
    """-> (outcome, reason) with outcome in agree / disagree / abstain; the reason is a short generic class."""
    v = kpipeline.solver_b_view(kpipeline.canonical_view(rec))
    res = hook.solver_b(v)
    rb = hook.render_b(v)
    if res.abstain or res.label is None:
        return "abstain", (res.reason or "abstain"), res
    why = []
    if res.label != rec["gold"]:
        why.append("label differs (B=%s)" % res.label)
    elif res.letter != rec["gold_letter"]:
        why.append("letter differs")
    if rb[0] != "letter":
        why.append("render_b abstains (%s)" % rb[1])
    elif rb[1] != rec["gold_letter"]:
        why.append("render_b letter differs")
    if why:
        return "disagree", "; ".join(why), res
    return "agree", "", res


def run(rows, seeds, standin=False, levers=True, a10=False):
    rep = {"rows": 0, "agree": 0, "disagree": 0, "abstain": 0, "by_head": {}, "classes": collections.Counter(), "by_lever": collections.Counter(),
           "notes": collections.Counter(), "h2_keep_via": collections.Counter(), "examples": {}, "obs": collections.Counter(),
           "cov": collections.defaultdict(lambda: [0, 0]), "by_edit": collections.defaultdict(lambda: [0, 0])}
    heads = collections.defaultdict(lambda: collections.Counter())
    for seed in seeds:
        recs, extra = build_rows(rows, seed, standin=standin, levers=levers, a10=a10)
        for rec in list(recs) + list(extra):
            out, why, res = check_one(rec)
            h = rec["sub_block"]
            rep["rows"] += 1
            rep[out] += 1
            heads[h]["rows"] += 1
            heads[h][out] += 1
            heads[h]["gold_" + rec["gold"]] += 1
            rep["by_lever"][rec.get("lever_tag", "lever.none")] += 1
            ek = "%s/%s" % (h, rec.get("edit") or rec.get("ctl") or rec.get("h2kind") or "none")
            rep["by_edit"][ek][0] += 1
            rep["by_edit"][ek][1] += 1 if out == "agree" else 0
            if out != "agree":
                key = "%s: %s" % (h, why)
                rep["classes"][key] += 1
                rep["examples"].setdefault(key, []).append(rec["row_id"])
            if res.parsed is not None:
                observe(h, res.parsed, rec["rendered"]["context"], rep)
            if res.parsed is not None and h == "h2":
                for n in res.parsed.get("notes", []):
                    rep["notes"][n] += 1
                if res.label == "KEEP":
                    plan = {s["n"]: s for s in res.parsed["plan"]}
                    lv = set()
                    for n in res.parsed["broken_steps"]:
                        for r in plan[n]["refs"]:
                            lv.add("L%d" % r["level"])
                        if plan[n]["host"] is not None:
                            lv.add("contingency")
                    rep["h2_keep_via"][",".join(sorted(lv)) or "none"] += 1
    rep["by_head"] = {h: dict(c) for h, c in sorted(heads.items())}
    return rep


def observe(head, parsed, context, rep):
    """Counts of rendering oddities that did not cause a disagreement (from B's own parse; informational)."""
    if head == "h2":
        _t, _r, by = h2mod.coverage(context)
        for k, (a, b) in by.items():
            rep["cov"][k][0] += a
            rep["cov"][k][1] += b
        facts = [f for f in h2mod.fact_table(parsed["events"]) if f["ftype"] != "M"]
        q = [f for f in facts if f["turn"] == parsed["quote"]["turn"]][0]
        later = [f for f in facts if f["turn"] > q["turn"] and f["handle"] == q["handle"] and f["entity"] == q["entity"]]
        if later:
            rep["obs"]["h2: quoted fact has a later statement of the same handle and entity (supersession)"] += 1
            if any(f["value"] == q["value"] for f in later):
                rep["obs"]["h2: ...of which the later statement repeats the SAME value (no change of value is visible)"] += 1
        if re.search(r"derived in step s\d", context):
            rep["obs"]["h2: chain reference written 'step s<k>' while plan lines say 'step <k>'"] += 1
        status = {s["n"]: s["status"] for s in parsed["plan"]}
        if any(s["host"] is not None and status.get(s["host"]) != "todo" for s in parsed["plan"]):
            rep["obs"]["h2: contingency step whose host step is not todo"] += 1
    elif head == "h3":
        days = [int(m) for m in re.findall(r"can be undone for (\d+) more day", context)]
        if days and min(days) <= 1:
            rep["obs"]["h3: an undo window of 1 day or less is shown"] += 1


def summarise(rep, rows, seeds):
    labelled = rep["agree"] + rep["disagree"]
    s = {"bar_pct": BAR, "rows_per_seed_requested": rows, "seeds": len(seeds), "rows": rep["rows"], "b_labelled": labelled, "agree": rep["agree"],
         "disagree": rep["disagree"], "b_abstained": rep["abstain"],
         "agreement_pct_over_labelled": round(100.0 * rep["agree"] / labelled, 3) if labelled else None,
         "agreement_pct_over_all": round(100.0 * rep["agree"] / rep["rows"], 3) if rep["rows"] else None,
         "meets_bar": bool(labelled and 100.0 * rep["agree"] / rep["rows"] >= BAR)}
    per = {}
    for h, c in rep["by_head"].items():
        lab = c.get("agree", 0) + c.get("disagree", 0)
        per[h] = {"rows": c["rows"], "agree": c.get("agree", 0), "disagree": c.get("disagree", 0), "abstain": c.get("abstain", 0),
                  "agreement_pct_over_labelled": round(100.0 * c.get("agree", 0) / lab, 3) if lab else None,
                  "agreement_pct_over_all": round(100.0 * c.get("agree", 0) / c["rows"], 3),
                  "gold_counts": {k[5:]: v for k, v in c.items() if k.startswith("gold_")}}
    s["by_sub_block"] = per
    s["disagreement_and_abstain_classes"] = dict(rep["classes"])
    s["lever_rows"] = dict(rep["by_lever"])
    s["by_edit_or_control_kind"] = {k: {"rows": a, "agree": b} for k, (a, b) in sorted(rep["by_edit"].items())}
    s["h2_notes"] = dict(rep["notes"])
    s["observations_not_disagreements"] = dict(rep["obs"])
    s["h2_reference_resolver_coverage"] = {k: {"references": a, "resolved": b} for k, (a, b) in sorted(rep["cov"].items())}
    s["h2_keep_decided_via_reference_level"] = dict(rep["h2_keep_via"])
    return s


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000, help="rows requested per seed (generator total; lever rows come on top)")
    ap.add_argument("--seeds", default="t60-agree-1,t60-agree-2")
    ap.add_argument("--out", default=None, help="JSON report path (put it in the scratch dir; it carries example row ids)")
    ap.add_argument("--log", action="store_true", help="also write the counts-only solver_b/agreement_log.json")
    ap.add_argument("--standin", action="store_true", help="generator stand-in wording instead of the pool")
    ap.add_argument("--no-levers", action="store_true", help="skip the A12 / dev lever rows")
    ap.add_argument("--a10", action="store_true", help="also build the A10 wrapper rows")
    a = ap.parse_args(argv)
    seeds = [s for s in a.seeds.split(",") if s]
    rep = run(a.rows, seeds, standin=a.standin, levers=not a.no_levers, a10=a.a10)
    s = summarise(rep, a.rows, seeds)
    print(json.dumps(s, indent=1, sort_keys=True))
    if a.out:
        full = dict(s, examples={k: v[:5] for k, v in rep["examples"].items()})
        with open(a.out, "w") as f:
            json.dump(full, f, indent=1, sort_keys=True)
    if a.log:
        with open(os.path.join(_HERE, "agreement_log.json"), "w") as f:
            json.dump(dict(s, note="counts only: no row text, ids or names; generated in memory, seeds %s" % ",".join(seeds)), f, indent=1, sort_keys=True)
    return s


if __name__ == "__main__":
    main()
