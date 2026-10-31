"""A57 step 4c for T40: G13-seed stage 1 on the merged G-LEX survivors (skin pool survivors + 2/2 wording survivors), every item a
template unit, vs every existing target (g13_c2 engine, AC checkers run-only). Drops only. Counts / C2 ids only.
  ../../.venv/bin/python -B zed_orch/a57_t40_stage4c.py"""
import json, sys, time
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import g13_c2 as G
Q = C2 / "a57_pool_quarantine" / "T40"
OUT = C2 / "logs" / "a57"
LEAN = G.LEAN

def main():
    st = json.loads((Q / "_work" / "step4_merged_state.json").read_text())
    res = json.loads((OUT / "T40_glex_merged.json").read_text())
    skins = [i for i in st["survivors"] if st["items"][i]["kind"] == "skin"]
    ids = sorted(set(skins) | set(res["admitted_item_ids"]))
    texts = {i: st["items"][i]["text"] for i in ids}
    units = [{"key": f"pool:a57_t40/{i}#0", "rows": [], "source": "pool:T40", "seed": True, "public": False, "line": 0,
              "template": True, "template_id": i, "file": f"a57_t40/{i}", "texts": [("pool", texts[i])]} for i in ids]
    sets = {"c2_seed_T40": {"units": units, "code": [], "train_shas": {}, "seed_shas": {}, "train_path": None, "block": "T40", "guard_shas": {}}}
    G.build_sets = lambda run_name, blocks, ilog: sets
    t0 = time.time()
    rec = G.run("seed", ["T40"], write=False)["c2_seed_T40"]
    q = rec.get("quarantine") or []
    dropped = sorted({(x if isinstance(x, str) else x.get("key", str(x))).split("/")[-1].rsplit("#", 1)[0] for x in q})
    rows = [{"id": i, "call_id": i, "state": texts[i]} for i in ids]
    ac_rows = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py", "--rows", rows)
    trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", texts[i])} for i in ids]
    ac_tpl = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", trecs, extra=["--min-shared", "1", "--parts", "all"])
    out = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wall_s": round(time.time() - t0), "items_checked": len(ids),
           "skin_checked": len(skins), "wording_checked": len(ids) - len(skins),
           "engine_complete": rec.get("complete"), "engine_dropped_items": dropped, "engine_counts": rec.get("counts_by_target_and_method"),
           "report_only": rec.get("report_only"),
           "ohsac_rows": {k: ac_rows.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids", "hit_ids_by_method")},
           "ohsac_templates": {k: ac_tpl.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids")}}
    out["ac_dropped_items"] = sorted(set(ac_rows.get("hit_ids") or []) | set(ac_tpl.get("hit_ids") or []))
    (OUT / "T40_g13seed_stage1.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("engine_dropped_items", "ac_dropped_items")}, default=str)[:3000])
    print("dropped engine", len(dropped), "dropped ac", len(out["ac_dropped_items"]))

main()
