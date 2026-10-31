"""DI-TS manifest + QC_REPORT after apply. Usage: python -I -B dits_package.py <di_train_dir>"""
import sys, json, datetime
from pathlib import Path
D = Path(sys.argv[1]); DT = D / "DI-TS"; LEAN = D.parents[2]
sys.path.insert(0, str(D.parents[1])); import c2io
A = json.load(open(DT / "stage/APPLY_REPORT.json")); F = json.load(open(DT / "stage/files.json"))
G1 = json.load(open(DT / "meta/G1_PROVENANCE.json")); P = json.load(open(DT / "SRC_PINS.json")); B = json.load(open(DT / "stage/BUILD_REPORT.json"))
S = json.load(open(DT / "reads/SCORE.json")); G6 = json.load(open(DT / "stage/G6_REPORT_ONLY.json")); DD = json.load(open(DT / "stage/DEDUPE_VS_C2.json"))
RUL = json.load(open(DT / "rulings/R1_ANSWER.json"))
out = LEAN / "data/c2_parts/DI-TS"
parents = [{"task": t, "repo": v.get("repo"), "pinned_commit": v.get("commit"), "licence": v.get("licence"), "licence_sha256": v.get("licence_sha256"), "train_file": v.get("train_file"),
            "train_sha256": v.get("train_sha256")} for t, v in G1["tasks"].items()]
man = {"family": "DI-TS", "stage": "round 3: A46 screen applied (54 dropped), gates 100%, C1 crowd read done; G13 not run (Mon)", "ruling": "A61 (draft) DI-TS; head: choice; natural label sets",
       "parents": parents, "tasks": list(B["tasks"]), "inputs": {"SRC_PINS.json": c2io.sha256_file(DT / "SRC_PINS.json") if hasattr(c2io, "sha256_file") else None, "build": "zed_orch/di_train/tools/build_dits.py + dits_apply.py"},
       "files": {k: v for k, v in F.items() if k != "mixdev_S5.jsonl"}, "own_dev": {"mixdev_S5.jsonl": F["mixdev_S5.jsonl"]}}
(out / "out" / c2io.MAN).write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
gc, gd = A["gates_candidates"], A["gates_owndev"]
qc = {"pass": bool(gc["pass"] and gd["pass"] and not A["candidate_problems"]), "passed_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "family": "DI-TS", "ruling": "A61 (draft)",
      "stage": "final for round 3: G13 seed/candidates/final not run (Mon); selection (<=600 per task) and joint DI pilot pending",
      "files": {k: {"sha256": v["sha256"]} for k, v in F.items() if k != "mixdev_S5.jsonl"}, "own_dev_file": F["mixdev_S5.jsonl"],
      "counts": {"staged_candidates": 4426, "staged_owndev": 300, "a46_reads": 9452, "a46_reads_missing": S["missing"], "a46_flagged": len(S["flagged"]), "opus_called": 58, "opus_gold_ok": 4,
                 "dropped_total": A["drop_ids"], "dropped_by_verdict": A["by_verdict"], "dropped_by_task": A["dropped_by_task"], "candidates": F["candidates_c2.jsonl"]["rows"], "owndev": F["mixdev_S5.jsonl"]["rows"],
                 "per_task_candidates": {t: p["rows"] for t, p in gc["per_task"].items()}, "per_task_owndev": {t: p["rows"] for t, p in gd["per_task"].items()},
                 "build_drops": {t: v["drops"] for t, v in B["tasks"].items()}, "dedupe_vs_c2_dev_eval_replay": {k: DD[k] for k in ("dev_eval_rows_compared", "replay_c1_rows_compared", "exact_dev_eval", "near_dev_eval", "exact_replay_c1")}},
      "gates_candidates": gc, "gates_owndev": gd, "g6_report_only": G6, "r1_rulings": {r["id"]: r["verdict"] for r in RUL},
      "licences": sorted({p["licence"] for p in parents if p["licence"]}), "crowd_read": "done 17 Oct on od-l4b fast path (one view); see verify step", "drops_only": True}
(out / "qc").mkdir(exist_ok=True); (out / "qc" / c2io.QC).write_text(json.dumps(qc, indent=1, ensure_ascii=False) + "\n")
print(qc["pass"], qc["licences"], qc["counts"]["candidates"], qc["counts"]["owndev"])
