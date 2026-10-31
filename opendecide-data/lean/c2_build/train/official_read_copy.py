"""official_read_copy.py: PREREG A97 (2): the chosen candidate's H100 grid reads become the official q35_4b_c2 pre-gate reads. CPU only.

The owner (A97 2) allowed reusing the chosen candidate's reads of the H100 grid job as the official pre-gate reads, copied AFTER
CANDIDATE_C2.json exists (A42-D 9.6, A89: the candidate is written before the official pre-gate reads). gate_c2.pred_files() looks
at the exact name q35_4b_c2 (and _perm), and gate_c2.check_candidate refuses a CANDIDATE_C2.json written after the first read of
that name, so the copies must carry the name q35_4b_c2 and be made after the record. This tool does exactly that and nothing else:

  * every file of the chosen candidate's read (q35_4b_c2grid_<G>[_perm].jsonl / .meta.json in every preds_* folder; 48 for the
    grid job) is copied BYTE FOR BYTE to the same folder under q35_4b_c2[_perm]; no prediction value, no meta field is edited
    (the meta's own "name" keeps the grid read name, which is honest provenance; no reader of gate_dev / gate_c2 / grid_elig uses
    it: gate_dev.pipe_sig reads base / host / gpu / torch / cuda / revision / chat_template_sha / tta / perm_seed / layout / style);
  * before copying, every source file is hashed and held to the sha256 in the job's own DONE.json (the pulled run dir of the H100
    job), the source set must equal DONE.json's file list, the job must be complete with no errors, and grid_plan.candidate_check
    must say OK_BEFORE_READS (CANDIDATE_C2.json identity and timing, CHOSEN.json agreement, no official read yet);
  * a destination that exists is a refusal (reads are placed once); the copy time must be later than CANDIDATE_C2.json's
    written_unix; after the copy each destination is re-hashed;
  * the record OFFICIAL_READ_COPY_A97.json lists per file the source and destination sha256, the source job id, the candidate
    record's sha256, written_unix and the copy time (unix and UTC).

  official_read_copy.py plan     all checks, the file list, nothing written
  official_read_copy.py copy     the copy + the record
  official_read_copy.py verify   re-hash every source and destination against the record
Exit 0 = ok, 1 = a check failed (verify), 2 = refused.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
LEAN = C2B.parent
for _p in (str(HERE), str(C2B), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import grid_plan as gp  # noqa: E402

Refused = gp.Refused
RUN_NAME = gp.RUN_NAME                                           # q35_4b_c2
SLACK = gp.SLACK
RUN_DIR = HERE / "grid_h100/results/grid_1018_1215/grid_1018_1215"     # the pulled run folder of the H100 job
RECORD = HERE / "OFFICIAL_READ_COPY_A97.json"
CANDIDATE = C2B / "CANDIDATE_C2.json"
CHOSEN = HERE / "CHOSEN.json"
GRID = Path("models/q35_4b_c2_grid/grid.json")                  # relative to LEAN
GRID_RECORD = HERE / "GRID_RECORD.json"


def _dst_rel(rel: str, src: str) -> str:
    d, name = rel.rsplit("/", 1)
    if not name.startswith(src) or name[len(src):][:1] not in ("_", "."):
        raise Refused(f"{rel}: not a file of the read {src}")
    return f"{d}/{RUN_NAME}{name[len(src):]}"


def check_job(run_dir: Path, src: str) -> dict:
    """The job's own records for the source read: complete, no errors, DONE.json file shas. Raises Refused."""
    plan_p, res_p, done_p = run_dir / "plan.json", run_dir / "session_result.json", run_dir / "models" / src / "DONE.json"
    for p in (plan_p, res_p, done_p):
        if not p.exists():
            raise Refused(f"{p} missing: the H100 job's records are not here")
    plan, res, done = (json.loads(p.read_text()) for p in (plan_p, res_p, done_p))
    if not res.get("complete"):
        raise Refused("the H100 session is not complete (session_result.json)")
    if res.get("errors"):
        raise Refused(f"the H100 session reported errors: {res['errors'][:2]}")
    if src not in (res.get("models_done") or []):
        raise Refused(f"{src} is not in the job's models_done")
    if done.get("read_name") != src or not done.get("files"):
        raise Refused(f"{done_p}: not the DONE record of {src}")
    return {"run_id": plan.get("run_id") or run_dir.name, "files": done["files"], "done_utc": done.get("done_utc"),
            "adapter_sha256": done.get("adapter_sha256")}


def make_plan(root: Path = LEAN, candidate: Path = CANDIDATE, chosen: Path = CHOSEN, grid: Path | None = None,
              grid_record: Path = GRID_RECORD, run_dir: Path = RUN_DIR) -> dict:
    """Every check; returns {candidate, src, files:[{src_rel, dst_rel, src_sha256}], job, candidate_check, ...}. Writes nothing."""
    root, candidate, chosen, run_dir = Path(root), Path(candidate), Path(chosen), Path(run_dir)
    grid = Path(grid) if grid else root / GRID
    gp.guard(root, candidate, chosen, grid, grid_record, run_dir)
    if not candidate.exists():
        raise Refused("CANDIDATE_C2.json does not exist: the official reads are copied only after it is written (A42-D 9.6, A97 2)")
    cand = json.loads(candidate.read_text())
    g_name = cand.get("grid_candidate")
    if cand.get("name") != RUN_NAME or g_name not in gp.expected_names():
        raise Refused(f"CANDIDATE_C2.json names {cand.get('name')!r} / {g_name!r}, not {RUN_NAME} / a grid candidate")
    adapter = grid.parent / g_name / "adapter_model.safetensors"
    chk = gp.candidate_check(candidate, grid, grid_record, chosen, adapter, root)
    if chk.get("status") == "OK_READS_AFTER":
        raise Refused("official q35_4b_c2 read files exist already: reads are placed once")
    if chk.get("status") != "OK_BEFORE_READS":
        raise Refused(f"grid_plan.candidate_check says {chk.get('status')}: {chk.get('problems') or chk.get('notes')}")
    src = gp.read_name(g_name)
    job = check_job(run_dir, src)
    if job.get("adapter_sha256") != cand.get("adapter_sha256"):
        raise Refused("the job's DONE.json adapter sha256 is not CANDIDATE_C2.json's")
    on_disk = {str(f.relative_to(root)) for f in gp.grid_read_files(root, [src])}
    if on_disk != set(job["files"]):
        extra, miss = sorted(on_disk - set(job["files"])), sorted(set(job["files"]) - on_disk)
        raise Refused(f"the placed read files differ from the job's DONE.json: extra {extra[:3]}, missing {miss[:3]}")
    files = []
    for rel in sorted(job["files"]):
        s, d = root / rel, root / _dst_rel(rel, src)
        h = gp.sha_file(s)
        if h != job["files"][rel]:
            raise Refused(f"{rel}: sha256 differs from the job's DONE.json (placed file changed since the job)")
        if d.exists():
            raise Refused(f"{d.relative_to(root)} exists: reads are placed once")
        files.append({"src_rel": rel, "dst_rel": str(d.relative_to(root)), "src_sha256": h, "bytes": s.stat().st_size})
    if gp.official_reads(root, RUN_NAME):
        raise Refused("official q35_4b_c2 read files exist already")
    return {"candidate": g_name, "src": src, "files": files, "job": {k: job[k] for k in ("run_id", "done_utc")},
            "candidate_written_unix": cand.get("written_unix"), "candidate_check": chk, "adapter": str(adapter)}


def copy(plan: dict, root: Path = LEAN, candidate: Path = CANDIDATE, record: Path = RECORD, now: float | None = None) -> dict:
    root, candidate, record = Path(root), Path(candidate), Path(record)
    gp.guard(record)
    if record.exists():
        raise Refused(f"{record} exists: the official reads are copied once")
    w = float(plan["candidate_written_unix"])
    t = time.time() if now is None else now
    if not t > w:
        raise Refused("the copy time is not later than CANDIDATE_C2.json's written_unix")
    made = []
    try:
        for f in plan["files"]:
            s, d = root / f["src_rel"], root / f["dst_rel"]
            if d.exists():
                raise Refused(f"{f['dst_rel']} exists: reads are placed once")
            shutil.copyfile(s, d)                                   # bytes only; the mtime is the copy time
            made.append(d)
            f["dst_sha256"] = gp.sha_file(d)
            if f["dst_sha256"] != f["src_sha256"] or d.stat().st_size != f["bytes"]:
                raise Refused(f"{f['dst_rel']}: the copy differs from its source")
    except BaseException:
        for d in made:                                              # nothing half-placed
            d.unlink(missing_ok=True)
        raise
    first = min(d.stat().st_mtime for d in made)
    if first + SLACK < w:
        for d in made:
            d.unlink(missing_ok=True)
        raise Refused("a copied file is older than CANDIDATE_C2.json (gate_c2.check_candidate would refuse)")
    rec = {"rule": "PREREG A97 (2): the chosen candidate's H100 grid reads copied byte for byte to the q35_4b_c2 read names, "
                   "after CANDIDATE_C2.json; no prediction value and no meta field changed",
           "candidate": plan["candidate"], "source_read": plan["src"], "dest_read": RUN_NAME, "source_job": plan["job"],
           "candidate_record": str(candidate), "candidate_record_sha256": gp.sha_file(candidate),
           "candidate_written_unix": w, "copy_unix": t, "first_dest_mtime_unix": first,
           "copy_utc": datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "predictions_changed": False, "meta_fields_changed": [],
           "meta_name_note": "each .meta.json keeps \"name\": the source read name; no pre-gate, gate_dev or grid_elig reader uses it",
           "n_files": len(plan["files"]), "files": plan["files"]}
    record.write_text(json.dumps(rec, indent=1) + "\n")
    return rec


def verify(root: Path = LEAN, record: Path = RECORD) -> list:
    """Problems (empty = every source and destination still has the recorded sha256 and the copy is later than the record)."""
    root, record = Path(root), Path(record)
    rec = json.loads(record.read_text())
    bad = []
    for f in rec["files"]:
        for k, rel in (("src_sha256", f["src_rel"]), ("dst_sha256", f["dst_rel"])):
            p = root / rel
            if not p.exists() or gp.sha_file(p) != f[k]:
                bad.append(f"{rel}: missing or changed")
    if not rec["copy_unix"] > rec["candidate_written_unix"]:
        bad.append("copy time is not later than the candidate record")
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "copy", "verify"))
    ap.add_argument("--root", default=str(LEAN), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "verify":
            bad = verify(Path(a.root))
            print(json.dumps({"ok": not bad, "problems": bad[:10]}, indent=1))
            return 0 if not bad else 1
        plan = make_plan(Path(a.root))
        if a.cmd == "plan":
            print(json.dumps({k: plan[k] for k in ("candidate", "src", "job", "candidate_written_unix")} |
                             {"n_files": len(plan["files"]), "first": plan["files"][0], "candidate_check": plan["candidate_check"]["status"]},
                             indent=1))
            return 0
        rec = copy(plan, Path(a.root))
        print(json.dumps({k: rec[k] for k in ("candidate", "source_job", "copy_utc", "n_files", "candidate_record_sha256")}, indent=1))
    except Refused as e:
        print(f"REFUSED: {e}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
