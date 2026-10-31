"""In-memory agreement harness for T65 solver B (the ONLY solver_b module that touches the generator side).

Builds rows with the family generator (CPU, in memory, stand-in executor; nothing written to disk except the --out report), hands solver B ONLY
`schema.b_view(rec)`, and compares its label and option letter with the record's gold and gold_letter.

    PYTHONDONTWRITEBYTECODE=1 python3 -m T65.solver_b.agree --rows 1000 --seeds 11,12 --out /path/report.json    (run from the c21_fam folder)
Bar (G0-lite T65-K3 / ROW_SCHEMA): agreement with solver A on 100% of kept rows; a class with > 1% disagreement returns to the generator.
"""
import argparse
import collections
import hashlib
import json
import os
import pathlib
import sys

_FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)
sys.dont_write_bytecode = True

from T65 import config as C                   # noqa: E402
from T65 import generator as G                # noqa: E402
from T65 import schema                        # noqa: E402
from T65.solver_b import hook                 # noqa: E402

_POOL = os.path.join(_FAM, "T65", "pools", "wording_pool.json")


def build_rows(seed, rows_target, real_pool=True):
    ctx = G.Ctx(seed=seed, standin=True, pool_path=_POOL if real_pool else None)
    plan = G.build_plan(total=max(2, int(rows_target * 0.80)), seed=seed)   # plan total ~0.87 x rows (x1.15 oversample, + CWE head rows)
    rows, builder_rejects = [], 0
    for g in plan:
        try:
            rows.extend(G.generate_group(ctx, g))
        except Exception:                       # noqa: BLE001 - a builder that cannot realise the group is not an answer-check row
            builder_rejects += 1
    heads = G.extra_rows(ctx, rows)
    return rows, heads, builder_rejects


def judge(rec, res):
    """-> 'agree' | 'disagree' | 'abstain' | 'error' (+ letter_ok)."""
    if res.get("status") == "abstain":
        return "abstain", None
    if res.get("status") != "ok" or res.get("label") is None:
        return "error", None
    ok = res["label"] == rec["gold"]
    letter_ok = res.get("letter") == rec["gold_letter"]
    return ("agree" if ok else "disagree"), letter_ok


def run(rows_target, seeds, real_pool=True, keep=None):
    stats = collections.defaultdict(lambda: collections.Counter())
    classes = collections.Counter()
    reasons = collections.Counter()
    sample = []
    total = collections.Counter()
    builder_rejects = 0
    uniq = set()
    for seed in seeds:
        rows, heads, br = build_rows(seed, rows_target, real_pool)
        builder_rejects += br
        for rec in rows + heads:
            uniq.add(hashlib.sha256(rec["rendered"]["text"].encode()).hexdigest()[:20])
            view = schema.b_view(rec)
            res = hook.solver_b(view)
            verdict, letter_ok = judge(rec, res)
            keys = ["ALL", "head:" + rec["head"], "sub:" + (rec["sub_block"] if rec["head"] == "VULN" else "CWE/" + rec["sub_block"]),
                    "kind:" + rec["meta"]["pair_kind"].split(":")[0] + ("" if ":" not in rec["meta"]["pair_kind"] else ":" + rec["meta"]["pair_kind"].split(":")[1]),
                    "gold:" + (rec["gold"] if rec["head"] == "VULN" else "CWE")]
            for k in keys:
                stats[k]["rows"] += 1
                stats[k][verdict] += 1
                if letter_ok is False:
                    stats[k]["letter_mismatch"] += 1
            if verdict in ("abstain", "error"):
                reasons[(rec["sub_block"] if rec["head"] == "VULN" else "CWE", verdict, res.get("reason", "")[:60])] += 1
            if verdict == "disagree":
                classes[(rec["head"], rec["sub_block"], rec["meta"]["pair_kind"], "B=" + str(res["label"]) if rec["head"] == "VULN" else "B!=gold")] += 1
                if keep is not None:
                    keep.append((rec, res))
            elif verdict in ("abstain", "error") and keep is not None:
                keep.append((rec, res))
            total[verdict] += 1
    total["distinct_texts"] = len(uniq)
    return stats, classes, reasons, total, builder_rejects


def _pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def summarise(stats, classes, reasons, total, builder_rejects, rows_target, seeds):
    out = {"bar": "100% of kept rows (T65-K3); a class with > 1% disagreement returns to the generator", "rows_target_per_run": rows_target, "seeds": list(seeds),
           "builder_rejects": builder_rejects, "groups": {}}
    for k in sorted(stats):
        s = stats[k]
        lab = s["agree"] + s["disagree"]
        out["groups"][k] = {"rows": s["rows"], "labelled": lab, "agree": s["agree"], "disagree": s["disagree"], "abstain": s["abstain"], "error": s["error"],
                            "letter_mismatch": s["letter_mismatch"], "agree_pct_labelled": _pct(s["agree"], lab), "agree_pct_all": _pct(s["agree"], s["rows"])}
    out["disagreement_classes"] = [{"head": h, "sub_block": sb, "pair_kind": pk, "b": b, "count": n} for (h, sb, pk, b), n in sorted(classes.items(), key=lambda kv: -kv[1])]
    out["abstain_reasons"] = [{"sub_block": sb, "status": st, "reason": r, "count": n} for (sb, st, r), n in sorted(reasons.items(), key=lambda kv: -kv[1])]
    out["totals"] = dict(total)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000, help="plan total PER SEED handed to the generator; rows built are about 1.05 x this (VULN pairs x 1.15 oversample, plus CWE head rows)")
    ap.add_argument("--seeds", default="11,12")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None, help="write the counts-only agreement log (no row text, ids or names) to this path")
    ap.add_argument("--stand-in-pool", action="store_true", help="use the TEST-ONLY wording pool instead of the real pool file")
    a = ap.parse_args(argv)
    seeds = [int(x) for x in a.seeds.split(",") if x]
    keep = [] if a.out else None
    stats, classes, reasons, total, br = run(a.rows, seeds, real_pool=not a.stand_in_pool, keep=keep)
    rep = summarise(stats, classes, reasons, total, br, a.rows, seeds)
    g = rep["groups"]["ALL"]
    print("rows %d labelled %d agree %d disagree %d abstain %d error %d  agree%%(labelled) %s  agree%%(all) %s" % (
        g["rows"], g["labelled"], g["agree"], g["disagree"], g["abstain"], g["error"], g["agree_pct_labelled"], g["agree_pct_all"]))
    for k in sorted(rep["groups"]):
        if k.startswith(("sub:", "head:")):
            x = rep["groups"][k]
            print("  %-26s rows %4d agree %4d dis %3d abst %3d err %2d  %s%% / %s%%" % (k, x["rows"], x["agree"], x["disagree"], x["abstain"], x["error"],
                                                                                    x["agree_pct_labelled"], x["agree_pct_all"]))
    if a.log:
        log = {k: rep[k] for k in ("bar", "groups", "disagreement_classes", "abstain_reasons", "totals", "builder_rejects")}
        log["run"] = {"seeds": "%d seeds (%d..%d)" % (len(seeds), min(seeds), max(seeds)), "plan_total_per_seed": a.rows,
                      "generator": "T65 generator in memory, stand-in executor, real wording pool file" if not a.stand_in_pool else "TEST-ONLY wording pool",
                      "solver_b_input": "schema.b_view(rec) only", "gold": "rec['gold'] and rec['gold_letter']"}
        pathlib.Path(a.log).write_text(json.dumps(log, indent=1, sort_keys=True) + "\n")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(rep, indent=1, sort_keys=True))
        # row-level detail for triage goes next to the report (scratch only; contains rendered text, never to be committed)
        detail = [{"row": r["row_id"], "head": r["head"], "sub_block": r["sub_block"], "gold": r["gold"], "pair_kind": r["meta"]["pair_kind"], "res": res,
                   "code": r["rendered"]["context"].split("):\n", 1)[1]} for r, res in keep]
        pathlib.Path(a.out.replace(".json", "_rows.json")).write_text(json.dumps(detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
