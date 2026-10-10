"""Optional: the 2B -> 4B cascade on OHS-3, offline, from the two models' preds (no new model read).

  ../.venv/bin/python prep89/ohs3_cascade.py --config prep89/ohs3_config.json [--root ...]

Routing (FINETUNE_PLAN 5.3, cascade_sim.py): the small model answers every row; a row goes to the big model when the
top of the small model's routing probabilities (normalised over the row's answers) is below tau; on a routed row the
answer is w_big * p_big + (1 - w_big) * p_small (both PRIMARY: A5 readout + T). Routing probabilities
(cascade.route_on): "primary" = <small>_cal.jsonl (A5 item 5: the 2B's served probabilities), "raw" =
<small>.jsonl (the A5 readout before T; FINETUNE_PLAN 5.3). tau, w_big and route_on come from the pre-registered
config only (set on dev-select by prep89/cascade_rule_fit.py; on real OHS-3 ohs3_lib.require_fit_logs stops the run
unless they equal that dev-only fit log). The rule is ohs3_lib.cascade_answer, the same
function the served cascade (ohs3_lib.CascadeDecider, timed end to end by ohs3_timing.py --model-key cascade) uses.
Writes preds_ohs3/<cascade.name>_cal.jsonl (+ meta: routed share). It is a third OpenDecide system and is reported
as such (rule 4): it refuses to run when the cascade already has a run (offline, or a served cascade pass written
with --od-preds-name by ohs3_timing.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

norm = L.cascade_norm  # kept under its old name (cascade_sim.py's)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(L.LEAN))
    ap.add_argument("--config", required=True)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    cfg = L.load_config(a.config, require_complete=True, model_keys=["cascade"])
    c = cfg["cascade"]
    if L.is_real_ohs3(root):
        L.require_frozen(root)
        L.require_fit_logs(cfg, ["cascade"], rehash=True)  # tau / w_big / route_on == the dev-only cascade_rule_fit log
    small, big = cfg["models"][c["small"]]["name"], cfg["models"][c["big"]]["name"]
    route_on = c.get("route_on", "primary")
    pd = root / f"preds_{L.SPLIT}"
    out = pd / f"{c['name']}_cal.jsonl"
    if out.exists() or L.completed_runs(root, c["name"]):
        raise SystemExit(f"STOP (rule 4): the cascade {c['name']} already has a run ({out.name} or the ledger)")
    rows = L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")
    Ps = {p["id"]: p["probs"] for p in L.read_jsonl(pd / f"{small}_cal.jsonl")}
    Pb = {p["id"]: p["probs"] for p in L.read_jsonl(pd / f"{big}_cal.jsonl")}
    Pr = Ps if route_on == "primary" else {p["id"]: p["probs"] for p in L.read_jsonl(pd / f"{small}.jsonl")}
    tau, w = float(c["tau"]), float(c["w_big"])
    recs, routed = [], 0
    for r in rows:
        rt = L.cascade_routed(r, Pr[r["id"]], tau)
        routed += rt
        recs.append({"id": r["id"], "model": f"{c['name']}_cal",
                     "probs": L.cascade_answer(r, Ps[r["id"]], Pb[r["id"]] if rt else None, rt, w), "routed": rt})
    L.write_jsonl_atomic(out, recs)
    meta = {"name": f"{c['name']}_cal", "small": small, "big": big, "tau": tau, "w_big": w, "route_on": route_on,
            "rows": len(rows), "routed": routed, "routed_share": round(routed / len(rows), 4),
            "config_sha256": cfg["_sha256"], "kind": "offline",
            "from": [f"{small}_cal.jsonl", f"{big}_cal.jsonl"] + ([f"{small}.jsonl"] if route_on == "raw" else []),
            "rule": "ohs3_lib.cascade_answer (same function as the served CascadeDecider)", "utc": L.utc()}
    (pd / f"{c['name']}_cal.meta.json").write_text(json.dumps(meta, indent=2))
    L.ledger_append(root, {"name": c["name"], "status": "complete", "kind": "cascade",
                           **{k: meta[k] for k in ("tau", "w_big", "route_on", "routed")}})
    L.blind_print(f"cascade {c['name']}: routed {routed}/{len(rows)} rows to {big} (route_on {route_on}); wrote {out.name}")
    return meta


if __name__ == "__main__":
    main()
