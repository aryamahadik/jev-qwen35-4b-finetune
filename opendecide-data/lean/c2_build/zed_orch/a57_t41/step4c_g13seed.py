"""A57 step 4c for T41: G13-seed stage 1 on the step-4a survivors (template units, one per item), against every target that
exists now: g13_c2 seed engine (public anchors, dev splits, JevBench, OHS-1/2/3 etc via the C2 tool, A53 / G-proxy targets as the
tool resolves them), the OHS-4 hash export, the OHS-4 checkers (run only), the OHS-AC freeze export (hash compare, done in 4a, repeated
here for the survivors) and the OHS-AC checkers (run only). Drops only; nothing admitted. Counts and C2 ids only.
Run from c2_build on the MAC:  ../../.venv/bin/python -B zed_orch/a57_t41/step4c_g13seed.py"""
import json, sys, time
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
import g13_c2 as G
Q = C2 / "a57_pool_quarantine" / "T41"
STATE = Q / "_work" / "step4a_state.json"
OUTJ = Path(__file__).parent / "g13_seed_stage1.json"
LEAN = G.LEAN
AC_ROWS = LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py"
AC_TPL = LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py"


def main():
    st = json.loads(STATE.read_text())
    ids = st.get("g13_ids") or st["survivors"]
    units = []
    for iid in ids:
        t = st["texts"][iid]
        units.append({"key": f"pool:a57_t41/{iid}#0", "rows": [], "source": "pool:T41", "seed": True, "public": False, "line": 0,
                      "template": True, "template_id": iid, "file": f"a57_t41/{iid}", "texts": [("pool", t)]})
    sets = {"c2_seed_T41": {"units": units, "code": [], "train_shas": {}, "seed_shas": {}, "train_path": None, "block": "T41",
                            "guard_shas": {}}}
    G.build_sets = lambda run_name, blocks, ilog: sets
    t0 = time.time()
    import os
    SIDE = os.environ.get("SIDE") == "1"          # the sealed-side child (OHS-3 / LongBench) queues behind other families' children
    res = G.run("seed", ["T41"], write=False, side=SIDE)
    rec = res["c2_seed_T41"]
    keep = {k: rec.get(k) for k in ("complete", "quarantine", "counts_by_target_and_method", "report_only", "why_incomplete",
                                    "drop_ids") if k in rec}
    q = rec.get("quarantine") or []
    dropped = sorted({(x if isinstance(x, str) else x.get("key", str(x))).split("/")[-1].rsplit("#", 1)[0] for x in q})
    # OHS-AC checkers (run only), each item its own unit; template check at --min-shared 1 --parts all
    rows = [{"id": f"{i}", "call_id": f"{i}", "state": st["texts"][i]} for i in ids]
    ac_rows = G.run_checker(AC_ROWS, "--rows", rows)
    import re
    trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", st["texts"][i])} for i in ids]
    ac_tpl = G.run_checker(AC_TPL, "--templates", trecs, extra=["--min-shared", "1", "--parts", "all"])
    out = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wall_s": round(time.time() - t0), "items_checked": len(ids),
           "engine_complete": rec.get("complete"), "sealed_side_child_run": SIDE, "engine_dropped_items": dropped,
           "engine_counts_by_target_and_method": rec.get("counts_by_target_and_method"),
           "ohsac_rows": {k: ac_rows.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids",
                                                      "hit_ids_by_method")},
           "ohsac_templates": {k: ac_tpl.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids")},
           "record_keys": sorted(rec.keys())}
    out["ac_dropped_items"] = sorted(set(ac_rows.get("hit_ids") or []) | set(ac_tpl.get("hit_ids") or []))
    OUTJ.write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("engine_dropped_items", "ac_dropped_items", "record_keys")}, default=str)[:3000])
    print("dropped engine", len(dropped), "dropped ac", len(out["ac_dropped_items"]))

main()
