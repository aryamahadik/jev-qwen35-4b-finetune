"""grid_h100.driver: the laptop side (CPU, no Modal import, nothing started): plan, preflight, commands, post-processing, tool shas.

  driver.py go-template                         the OWNER_GO1_PAYER.json the owner's GO #1 fills in (the payer guard reads it; no file = refuse)
  driver.py plan [--out F] [--own-dev a,b]      the read plan + the wall-time / cost estimate against the USD 15.00 cap (A88) (writes nothing else)
  driver.py check                               every local precondition of the grid session, as a list of BLOCKERS (exit 1 if any)
  driver.py commands                            the `modal run` commands (printed, never run) and the follow-up steps
  driver.py parity-plan --cand C [--candidate-json c2_build/CANDIDATE_C2.json]   the plan of the merged-vs-HF-adapter parity job
  driver.py post --run-dir DIR [--dry-run]      after `modal volume get`: verify sha256 of every file, put preds_* into lean/, write the
                                                per-candidate latency records (logs/grid/latency_<cand>.json), print the gate_dev / grid_elig steps
  driver.py ledger                              the money ledger
  driver.py shas                                sha256 of every tool file (for c2_build/zed_orch/a64/A64_TOOLS.md)

Everything runs from lean/:  PY=../.venv/bin/python -B;  $PY c2_build/train/grid_h100/driver.py <cmd>   (or  -m grid_h100.driver  from c2_build/train).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

if __package__ in (None, ""):                       # run as a script: make `grid_h100` importable
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "grid_h100"

from grid_h100 import common as C  # noqa: E402
from grid_h100 import plan as PL  # noqa: E402

TRAIN = C.HERE.parent
C2B = TRAIN.parent
RECORD = TRAIN / "GRID_RECORD.json"
PROMPT_CHECK = C2B / "logs" / "p7_prompt_sha_check.json"
PIN = C2B / "serving" / "S1_CONFIG_PIN.json"
CANDIDATE = C2B / "CANDIDATE_C2.json"
GRID_LOGS = C2B / "logs" / "grid"
C1_BACKUP = C.LEAN.parents[1] / "backups" / "modal_models" / C.C1_NAME
WORKLOADS = C.LEAN / "speed" / "workloads"
RUN_DIR_VOLUME = "/vol/models/q35_4b_c2"
PARITY_SPLIT, PARITY_FILE = "gblock_a42d_c1read", "gblock_a42d_c1read.jsonl"
PARITY_SEED, PARITY_N = 20261013, 2000                # C2 seed (c2io.SEED); the A49 (f) sample size
TOOL_FILES = ("__init__.py", "common.py", "plan.py", "merge_direct.py", "gridbuild.py", "servers.py", "reader.py", "hostops.py",
              "session.py", "hf_ref.py", "parity.py", "driver.py", "modal_app_grid.py", "README.md", "RUNBOOK.md", "PAYER_POLICY.json", "OWNER_GO1_PAYER.json", "tests/test_grid_h100.py",
              "tests/test_modal_app.py", "tests/fakes.py")

GO_TEMPLATE = {"profile": "<the Modal profile the owner names>", "go": "GO #1", "written_utc": "<UTC time of the owner's words>",
               "owner_words": "<the owner's own words naming this payer for the A42-D 9 grid reads>",
               "cap_usd": "(optional, may only LOWER the 15.00 cap)"}


def load_json(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return None


def make_plan(run_id: str | None = None, own_dev=(), spent_usd: float | None = None, data_root: Path | None = None,
              record_path: Path = RECORD, grid_source: str = "rebuild", p_ref: dict | None = None,
              prompt_check_path: Path = PROMPT_CHECK) -> dict:
    data_root = Path(data_root or C.LEAN / "data")
    record = load_json(record_path)
    if spent_usd is None:
        spent_usd = C.Budget(persist=True).spent_closed()
    plan = PL.build_plan(data_root, record, own_dev, spent_usd, p_ref=p_ref)
    plan.update({"run_id": run_id or time.strftime("grid_%Y%m%d_%H%M%S", time.gmtime()), "c2_run_dir": RUN_DIR_VOLUME,
                 "grid_source": grid_source, "grid_record": record, "prompt_check_record": load_json(prompt_check_path),
                 "latency": {"n": 400, "warmup": 20, "workload": "S", "seed": 0},
                 "boot_timeout_s": 900, "read_timeout_s": 1800, "reader_ready_timeout_s": 900,
                 "server": dict(C.SERVER_ARGS), "payer_note": "the profile is checked by the payer guard against OWNER_GO1_PAYER.json"})
    return plan


def make_parity_plan(cand: str, candidate_json: Path = CANDIDATE, run_id: str | None = None, data_root: Path | None = None,
                     n: int = PARITY_N, seed: int = PARITY_SEED, record_path: Path = RECORD) -> dict:
    data_root = Path(data_root or C.LEAN / "data")
    record = load_json(record_path)
    if not record:
        raise SystemExit("driver: GRID_RECORD.json missing (grid_plan.py record)")
    cj = load_json(candidate_json)
    if not cj:
        raise SystemExit(f"driver: {candidate_json} missing: the parity check runs for the chosen candidate (CANDIDATE_C2.json)")
    gc = cj.get("grid_candidate")
    if gc != cand or cj.get("adapter_sha256") != (record.get("candidates") or {}).get(cand):
        raise SystemExit(f"driver: CANDIDATE_C2.json names {gc!r} / {str(cj.get('adapter_sha256'))[:16]}, not {cand!r} of the grid record")
    f = data_root / PARITY_FILE
    return {"run_id": run_id or time.strftime("parity_%Y%m%d_%H%M%S", time.gmtime()), "cand": cand, "read_name": C.read_name(cand),
            "expect_adapter_sha256": cj["adapter_sha256"], "split": PARITY_SPLIT, "split_file": PARITY_FILE, "split_sha256": C.sha256_file(f),
            "n": n, "seed": seed, "min_n": 2000, "views": 2, "c2_run_dir": RUN_DIR_VOLUME, "grid_record": record,
            "prompt_check_record": load_json(PROMPT_CHECK), "est_hf_usd": 0.30, "est_served_usd": 0.25,
            "estimate": parity_estimate(), "limits": {"cap_usd": C.CAP_USD, "stop_launch_usd": C.STOP_LAUNCH_USD}}


def parity_estimate() -> dict:
    out = {}
    for i, name in enumerate(("low", "likely", "high")):
        s = PL.PARITY_ASSUME["fixed_s"][i]
        out[name] = {"seconds": s, "usd": round(C.container_cost_usd(s), 2)}
    return out


# ------------------------------------------------------------------ preflight
def preflight(plan: dict | None = None, lean: Path = C.LEAN) -> dict:
    """Blockers (the grid cannot start) and notes. Reads only small files; opens no OHS / sealed path."""
    blockers, notes = [], []
    try:
        go = C.read_go(C.GO_FILE)
        pol = C.read_policy()
        if go["profile"] in pol["never_payers"]:
            blockers.append(f"payer {go['profile']!r} is in PAYER_POLICY.json never_payers")
        why = C.c2_training_problem(go["profile"], pol)
        if why:
            blockers.append(f"payer {go['profile']!r} may not pay yet: {why}")
    except SystemExit as e:
        blockers.append(str(e))
    rec = load_json(RECORD)
    if not rec:
        blockers.append("GRID_RECORD.json missing (grid_plan.py record: the grid sha256 is recorded BEFORE any look, A42-D 9.6)")
    elif len(rec.get("candidates") or {}) != 18:
        blockers.append(f"GRID_RECORD.json holds {len(rec.get('candidates') or {})} candidates, not 18")
    pc = load_json(PROMPT_CHECK)
    if not pc or not pc.get("pass"):
        blockers.append("c2_build/logs/p7_prompt_sha_check.json missing or not a pass (re-run prompt_sha_check.py --adapter <C2 dir>)")
    elif "prompt_sha256" not in pc or "token_ids_digest" not in pc:
        blockers.append("p7_prompt_sha_check.json lacks prompt_sha256 / token_ids_digest")
    pin = load_json(PIN)
    if not pin:
        blockers.append("S1_CONFIG_PIN.json missing")
    else:
        for n, want in ((pin.get("model") or {}).get("tokenizer_pins") or {}).items():
            p = C1_BACKUP / n
            if not p.exists():
                blockers.append(f"C1 backup {n} missing at {C1_BACKUP}")
            elif C.sha256_file(p) != want:
                blockers.append(f"C1 backup {n} differs from the S1 pin")
    plan = plan or make_plan()
    for rel, m in plan["data_manifest"].items():
        if m.get("missing"):
            blockers.append(f"data file {rel} missing")
    if not (WORKLOADS / "S.jsonl").exists():
        blockers.append("speed/workloads/S.jsonl missing")
    wl = load_json(WORKLOADS / "manifest.json")
    if wl and (WORKLOADS / "S.jsonl").exists() and C.sha256_file(WORKLOADS / "S.jsonl") != wl["workloads"]["S"]["sha256"]:
        blockers.append("speed/workloads/S.jsonl differs from its manifest")
    est = plan["estimate"]["verdict"]
    if not est["fits"]:
        blockers.append("COST: " + est["text"])
    spent = C.Budget(persist=True).summary()
    notes.append(f"ledger {json.dumps(spent)}")
    return {"blockers": blockers, "notes": notes, "ready": not blockers, "estimate": est}


def commands(profile: str | None, run_id: str) -> list:
    p = profile or "<profile>"
    base = f"cd {C.LEAN} && MODAL_PROFILE={p} ../.venv/bin/modal run c2_build/train/grid_h100/modal_app_grid.py"
    return [
        f"# nothing below has been run. GO #1 first: the owner names the payer; write OWNER_GO1_PAYER.json ({C.HERE.name}/).",
        f"../.venv/bin/python -B c2_build/train/grid_h100/driver.py check",
        f"{base}::grid --run-id {run_id}                      # THE grid session (one H100 container, ledger cap USD {C.CAP_USD})",
        f"MODAL_PROFILE={p} ../.venv/bin/modal volume get {C.OUT_VOLUME} runs/{run_id} {C.RESULTS}/{run_id}   # free, pulls the outputs",
        f"../.venv/bin/python -B c2_build/train/grid_h100/driver.py post --run-dir {C.RESULTS}/{run_id}",
        "# after select_candidate.py has written CANDIDATE_C2.json:",
        f"{base}::parity --cand <chosen candidate> --run-id parity_<id>",
        f"../.venv/bin/python -B c2_build/train/c2_check.py spend --usd <ledger total> --what 'A42-D 9 grid reads H100' --profile {p}",
    ]


# ------------------------------------------------------------------ post
def _verify_model(mdir: Path) -> dict:
    d = load_json(mdir / "DONE.json")
    if not d:
        return {"ok": False, "why": "no DONE.json"}
    bad = [rel for rel, sha in d["files"].items() if not (mdir / rel).exists() or C.sha256_file(mdir / rel) != sha]
    return {"ok": not bad, "why": f"{len(bad)} files differ / missing: {bad[:3]}" if bad else "", "done": d}


def post(run_dir: Path, lean: Path = C.LEAN, dry_run: bool = False, record_path: Path = RECORD, logs: Path = GRID_LOGS) -> dict:
    run_dir = Path(run_dir)
    C.safe_path(run_dir)
    plan = load_json(run_dir / "plan.json")
    sres = load_json(run_dir / "session_result.json")
    if not plan or not sres:
        raise SystemExit(f"post: {run_dir} has no plan.json / session_result.json")
    if not record_path.exists():
        raise SystemExit("post: GRID_RECORD.json must exist BEFORE the reads are placed (A42-D 9.6: the record is older than every read)")
    out = {"placed": [], "unchanged": [], "refused": [], "latency": {}, "models": {}}
    ref_name = C.REF_NAME
    models = {m["read_name"]: m for m in plan["models"]}
    for rn, m in models.items():
        v = _verify_model(run_dir / "models" / rn)
        out["models"][rn] = {"ok": v["ok"], "why": v["why"]}
        if not v["ok"]:
            continue
        for rel in v["done"]["files"]:
            if not rel.startswith("preds_"):
                continue
            dst = Path(lean) / rel
            src = run_dir / "models" / rn / rel
            if dst.exists():
                if C.sha256_file(dst) == C.sha256_file(src):
                    out["unchanged"].append(rel)
                else:
                    out["refused"].append(f"{rel}: exists with other content (reads are placed once)")
                continue
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
            out["placed"].append(rel)
    # latency records (Q6): one per candidate against the C1 read of the SAME job
    from grid_h100 import servers
    D9 = servers.serving_mod("d9_latency")
    c1b = load_json(run_dir / "models" / ref_name / "block.json") or {}
    c1l = c1b.get("latency")
    for rn, m in models.items():
        if m["kind"] != "cand" or not out["models"][rn]["ok"] or not c1l:
            continue
        cl = (load_json(run_dir / "models" / rn / "block.json") or {}).get("latency")
        if not cl:
            continue
        try:
            rec = D9.combine(c1l, cl)
        except SystemExit as e:
            out["latency"][m["cand"]] = {"refused": str(e)}
            continue
        rec["served_path"] = f"sglang_s1_h100_grid:{c1l['path_sha256'][:16]}"
        rec["note"] = ("A42-D 9 grid eligibility record: C1 and this candidate measured one after the other in the same H100 job on the "
                       "same server arguments (path_sha256), batch 1, workload S. " + rec.get("note", ""))
        out["latency"][m["cand"]] = {"cand_p50_ms": rec["cand_p50_ms"], "ref_p50_ms": rec["ref_p50_ms"], "ratio": rec["ratio"], "pass": rec["pass"]}
        if not dry_run:
            C.write_json(Path(logs) / f"latency_{m['cand']}.json", rec)
    out["next"] = [f"$PY gate_dev.py {rn} {ref_name} --mode ship --size 4b --json c2_build/logs/grid/ship_{m['cand']}.json --no-log"
                   for rn, m in models.items() if m["kind"] == "cand"]
    out["next"] += [f"$PY gate_dev.py {ref_name} q35_4b_main500k --mode refparity     # must PASS before grid_elig.py",
                    "$PY c2_build/train/grid_elig.py all --cfg c2_build/staged/P6-grid/GRID_CFG.json --out-dir c2_build/train/grid_reads"]
    out["complete"] = bool(sres.get("complete")) and all(v["ok"] for v in out["models"].values())
    out["spent_usd"] = sres.get("spent_usd")
    return out


# ------------------------------------------------------------------ shas
def tool_shas() -> dict:
    return {f: C.sha256_file(C.HERE / f) for f in TOOL_FILES if (C.HERE / f).exists()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("go-template")
    p = sub.add_parser("plan")
    p.add_argument("--out", default="")
    p.add_argument("--own-dev", default="")
    sub.add_parser("check")
    c = sub.add_parser("commands")
    c.add_argument("--profile", default="")
    c.add_argument("--run-id", default="grid_<id>")
    pp = sub.add_parser("parity-plan")
    pp.add_argument("--cand", required=True)
    pp.add_argument("--candidate-json", default=str(CANDIDATE))
    po = sub.add_parser("post")
    po.add_argument("--run-dir", required=True)
    po.add_argument("--dry-run", action="store_true")
    sub.add_parser("ledger")
    sub.add_parser("shas")
    a = ap.parse_args(argv)
    if a.cmd == "go-template":
        print(json.dumps(GO_TEMPLATE, indent=1))
    elif a.cmd == "plan":
        plan = make_plan(own_dev=[s for s in a.own_dev.split(",") if s])
        if a.out:
            C.write_json(a.out, plan)
        print(json.dumps({"verdict": plan["estimate"]["verdict"], "scenarios": {k: {kk: v[kk] for kk in ("grid_hours", "grid_cost_usd", "parity_job_cost_usd", "all_in_cost_usd")}
                                                                                for k, v in plan["estimate"]["scenarios"].items()},
                          "basis": plan["estimate"]["basis"]}, indent=1))
    elif a.cmd == "check":
        r = preflight()
        print(json.dumps(r, indent=1))
        return 0 if r["ready"] else 1
    elif a.cmd == "commands":
        print("\n".join(commands(a.profile or None, a.run_id)))
    elif a.cmd == "parity-plan":
        print(json.dumps({k: v for k, v in make_parity_plan(a.cand, Path(a.candidate_json)).items() if k not in ("grid_record", "prompt_check_record")}, indent=1))
    elif a.cmd == "post":
        r = post(Path(a.run_dir), dry_run=a.dry_run)
        print(json.dumps(r, indent=1))
        return 0 if r["complete"] and not r["refused"] else 1
    elif a.cmd == "ledger":
        print(json.dumps(C.Budget().summary(), indent=1))
    elif a.cmd == "shas":
        print(json.dumps(tool_shas(), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
