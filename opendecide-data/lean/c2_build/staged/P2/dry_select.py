"""P2 SCRATCH-ONLY dry selection (A69 draft): the 15 program families on the CURRENT candidates, the batch-5 G13 drops WITHOUT
OHS-AC (A68; staged/P2/drop_ids_no_ohsac.json), C1 labels as they are. Writes nothing to crowd_c2/ and nothing to data/; the
summary goes to staged/P2/dry_summary.json (counts, ids-free). Three variants per family: baseline (the pre-A69 selection),
trap (A69 b only) and trap + repair (A69 b + drop-only repair).
  HF_HUB_OFFLINE=1 ../../.venv/bin/python -B c2_build/staged/P2/dry_select.py [FAM ...]
"""
import json
import os
import sys
import time
from pathlib import Path

LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
os.chdir(LEAN)
sys.path.insert(0, LEAN + "/c2_build")
sys.path.insert(0, LEAN + "/c_build")
sys.path.insert(0, LEAN)
import c2io  # noqa: E402
import c2_select as S  # noqa: E402
import mixer as mx  # noqa: E402

STG = Path(LEAN) / "c2_build/staged/P2"
DROPS = json.load(open(STG / "drop_ids_no_ohsac.json"))


def summarize(rec, fam, n_pool, n_pool_units):
    rep = rec["report"]
    a = rep["a49c"]
    ck = rep["checks"]
    failing = a["failing"]
    cardmax = a["card_max"]
    out = {"rows": rep["rows"], "target": rec["target"], "short_by": rep["short_by"], "units": rep["units"],
           "bins": rep["bins"], "easy_share": round(rep["bins"].get("easy", 0) / max(1, rep["rows"]), 4),
           "hard_share": round(rep["bins"].get("hard", 0) / max(1, rep["rows"]), 4),
           "medium_share": round(rep["bins"].get("medium", 0) / max(1, rep["rows"]), 4),
           "selection_checks": ck, "chi2": rep["chi2_label_x_bin"], "a49c_failing": failing, "card_max": cardmax,
           "card_ok": cardmax <= 64,
           "a49c_values": {k: v["value"] for k, v in a["checks"].items() if v["verdict"] in ("fail",)},
           "swap": {k: a["balance_swap"].get(k) for k in ("swaps", "violation_before", "violation_after")} if a["balance_swap"] else None,
           "pool_rows_after_g13": n_pool, "pool_units_after_g13": n_pool_units}
    checks_ok = all(v for k, v in ck.items() if k != "total_eq_target")
    out["all_checks_pass_except_total"] = bool(checks_ok and not failing and cardmax <= 64)
    out["all_checks_pass_incl_total"] = bool(out["all_checks_pass_except_total"] and ck.get("total_eq_target"))
    if "a69" in rep:
        a69 = rep["a69"]
        keep = ("flagged_units", "flagged_rows", "flagged_units_by_type", "treated_units_final", "treated_selected_units",
                "treated_selected_by_type", "flagged_selected_by_type_reported_only", "type_cap_steps", "weight", "scaled",
                "hard_share", "hard_assert_ok", "type_order")
        out["a69"] = {k: a69[k] for k in keep}
        ts = a69["treated_selected_units"]
        out["a69"]["max_type_share_of_treated_selected"] = (round(max(a69["treated_selected_by_type"].values()) / ts, 4)
                                                             if ts else None)
        out["a69"]["trap_rows_selected_share"] = None
        out["a69"]["pick_rates_top"] = dict(list(a69["pick_rates_post_g13"].items())[:6])
        out["a69"]["n_tags"] = len(a69["pick_rates_post_g13"])
        out["a69"]["repair"] = a69["repair"]
    return out


def main():
    fams = sys.argv[1:] or list(S.TRAP_FAMS)
    ilog = S.LinkGuardedInputLog()
    summary = {}
    for fam in fams:
        t0 = time.time()
        rows, rels, _ = S.family_inputs(ilog, fam)
        sd = S.SHARDS / fam
        pg, view, probs = S.load_c1_full(ilog, rows, sd / f"labels_{S.C1}", sd)
        drop = set(DROPS[fam]["drop_ids"])
        rows_in_pool = [r for r in rows if r["id"] not in drop]
        units_all = S.cs.units_of(rows, rels)
        # token counts of the pool (cached under staged/P2)
        cache = STG / f"ntok_{fam}.json"
        if cache.exists():
            ntok = json.load(open(cache))
        else:
            ntok = dict(zip((r["id"] for r in rows), mx.token_counts(ilog, rows)))
            cache.write_text(json.dumps(ntok))
        target = S.TARGETS[fam]
        pool_rows, _ = S.drop_excluded(rows, rels, drop)
        n_units = len(S.cs.units_of(pool_rows, [x for x in rels if x["a"] in {r["id"] for r in pool_rows}]))
        res = {"pool_rows_before_drop": len(rows), "drop_rows": len(drop), "pool_rows_after_drop": len(pool_rows)}
        for name, kw in (("baseline_pre_a69", dict(probs=None, repair=False)),
                         ("a69_trap", dict(probs=probs, repair=False)),
                         ("a69_trap_repair", dict(probs=probs, repair=True))):
            t1 = time.time()
            rec = S.select_family(fam, rows, rels, pg, target, S.SEED, drop, ntok=ntok, **kw)
            res[name] = summarize(rec, fam, len(pool_rows), n_units)
            res[name]["seconds"] = round(time.time() - t1, 1)
            print(f"{fam} {name}: rows {res[name]['rows']}/{target} trap_fail {res[name]['a49c_failing']} card {res[name]['card_max']} "
                  f"pass_ex_total {res[name]['all_checks_pass_except_total']} ({res[name]['seconds']}s)", flush=True)
        summary[fam] = res
        (STG / "dry_summary.json").write_text(json.dumps(summary, indent=1))
    print("done", flush=True)


main()
