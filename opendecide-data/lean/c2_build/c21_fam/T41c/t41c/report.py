"""Run the PRE-FREEZE CPU gates on a planned set (in memory; prints JSON to stdout, writes nothing).

    python -m t41c.report --n 2000 --boot 300          # test pool (machinery check; the wording gates will FAIL on it)

A production run (after the OHS-5 FREEZE record, the G13 registry sha and the names manifest pins exist) goes through
c21_infra/row_start_guard.py first; this module never starts a row job and never writes rows.
"""
import argparse
import json
import sys
import time

from . import build, export, gates, planner, pools


def run_prefreeze(N=2000, pool=None, boot=2000, solve_b=None, proxy_names=False, with_null=True, checker=None):
    """checker: a rowcheck.RowChecker. With it, every row is checked WHEN it is built (A vs B, invariants, guards, G13 hook,
    stamp) and only accepted rows reach the set-level gates; without it the plain build is used (machinery check only)."""
    pool = pool or pools.make_test_pool(per_cell=12)
    held = planner.draw_heldout()
    t = time.time()
    specs, prep = planner.plan_specs(N, heldout=held, proxy_names=proxy_names)
    chk = export.names_checker()
    ho_specs, _ = planner.plan_heldout(heldout=held, proxy_names=proxy_names)
    if checker is None:
        rows, brep = build.build_rows(specs, pool, proxy_names=proxy_names, check_names=chk)
        ho_rows, hrep = build.build_rows(ho_specs, pool, proxy_names=proxy_names, check_names=chk)
    else:
        acc, crep = build.build_rows_checked(specs, pool, checker, proxy_names=proxy_names)
        rows = [(s, r) for s, r, _ in acc]
        tl = crep["trigger_lines"]
        brep = {"candidates": crep["candidates"], "kept": len(rows), "drops": crep["first_pass_drop_rates"],
                "guard_refusal_rate": tl["guards_names"]["rate"], "anchor_drop_rate": tl["schema_anchor"]["rate"],
                "check_at_generation": {k: crep[k] for k in ("trigger_lines", "combined_fix_triggered", "retired_groups",
                                                             "dropped_groups", "g13_hook")}}
        hacc, hrep = build.build_rows_checked(ho_specs, pool, checker, proxy_names=proxy_names)
        ho_rows = [(s, r) for s, r, _ in hacc]
    kept = [s for s, _ in rows]
    out = {"n_planned": len(specs), "n_built": len(rows), "build": brep, "ho_build": hrep, "heldout": held,
           "pool_kind": pool.kind, "pool_sha": pool.sha(), "gates": {}}
    G = out["gates"]
    G["K4"] = gates.gate_k4(specs, N)
    G["K5"] = gates.gate_k5(specs)
    G["K1"] = gates.gate_k1(rows, boot=boot, with_null=with_null)
    G["K2"] = gates.gate_k2(rows, boot=boot)
    G["K3"] = gates.gate_k3(rows, ho_rows, boot=boot)
    G["K8"] = gates.gate_k8(rows)
    G["K9"] = gates.gate_k9(kept, brep, heldout=held)
    G["K12"] = gates.gate_k12(rows)
    if solve_b is not None:
        G["K6ii"] = gates.gate_k6_rows(rows, solve_b)
    out["provenance_probe_informational"] = gates.provenance_probe(rows)
    out["seconds"] = round(time.time() - t, 1)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--boot", type=int, default=300)
    a = ap.parse_args(argv)
    res = run_prefreeze(a.n, boot=a.boot)
    print(json.dumps(res, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
