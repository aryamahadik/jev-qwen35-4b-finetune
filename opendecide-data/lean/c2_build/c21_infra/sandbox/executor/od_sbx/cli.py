"""od-sbx command line.  Run as root via /opt/od-sbx/bin/od-sbx (sudo), which runs
`python3 -I /opt/od-sbx/executor/od_sbx_launcher.py ...` (the launcher sets sys.path; `-I` ignores PYTHONPATH).

  selftest --out FILE        run ST-1..ST-7, write JSON, exit 1 on any failure
  run-batch --jobs F --out F run jobs (JSON lines) after checking the self-test result; write results + batch manifest
  cleanup                    remove any container labelled od-sbx=1 and stale stage dirs
  treehash DIR               print the executor tree hash (used by 60_finalize_image.sh)

Job line: {"row_id": str, "toolchain": "python|node|go|sh", "kind": "run|suite", "will_this_test_fail": bool,
           "files": {relpath: base64},          # the (untrusted) patch tree; sanitized on kind=suite
           "suite_files": {relpath: base64},    # optional PRISTINE hidden suite + support files, copied in AFTER sanitizing
           "argv": [..], "report": "junit.xml|go.json|null",
           "expected_ids": [..] | null}
A python suite job must start its argv with `python -s -P` (no user site, no cwd on sys.path: a patch file pytest.py cannot
replace pytest). A job that does not is rejected and counted (`rejected_bad_suite_argv`).
A batch ends at BATCH_MAX_EXEC executions or BATCH_MAX_SECONDS, whichever is first; the VM is then re-imaged.
STATUS: skeleton. `expected_ids` comes from a collect-only run of the pristine hidden suite (L-C wires this up).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import platform
import shutil
import sys
import time

from .config import MANIFEST, REPEATS_DEFAULT, REPEATS_WILL_THIS_TEST_FAIL, SELFTEST_JSON, STAGE_ROOT
from .runner import BatchCounters, StageError, cleanup_containers, load_manifest, run_repeated
from . import verdict as V

BATCH_MAX_EXEC = 5000
BATCH_MAX_SECONDS = 3600


def _selftest_ok() -> tuple[bool, str]:
    try:
        d = json.loads(SELFTEST_JSON.read_text())
    except Exception as e:
        return False, f"no self-test result: {e}"
    cur = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    if d.get("status") != "PASS":
        return False, f"self-test status {d.get('status')}"
    if d.get("manifest_sha256") != cur:
        return False, "self-test was run against a different image manifest"
    return True, "ok"


def _suite_argv_ok(toolchain: str, kind: str, argv: list) -> bool:
    return not (toolchain == "python" and kind == "suite") or list(argv[:3]) == ["python", "-s", "-P"]


def run_batch(jobs_path: str, out_path: str) -> int:
    ok, why = _selftest_ok()
    if not ok:
        print(f"REFUSING to run: {why}", file=sys.stderr)
        return 2
    # M5 (Opus 10.1): the boot-time self-test can be stale by the time a batch starts (an SSH login may have added a docker-group
    # member or the firewall may have been flushed). Re-run the cheap host guards NOW.
    from .selftest import host_guards
    bad = host_guards()
    if bad:
        print(f"REFUSING to run: host guard failed at batch start: {bad}", file=sys.stderr)
        return 2
    cleanup_containers()                       # leftovers from an aborted batch would collide on container names
    man, counters, t0, n = load_manifest(), BatchCounters(), time.monotonic(), 0
    batch = time.strftime("%Y%m%dT%H%M%S")
    with open(jobs_path) as fin, open(out_path, "w") as fout:
        for line in fin:
            if n >= BATCH_MAX_EXEC or time.monotonic() - t0 > BATCH_MAX_SECONDS:
                counters.bump("batch_limit_reached_remaining_rows_not_run")
                break
            j = json.loads(line)
            if not _suite_argv_ok(j["toolchain"], j.get("kind", "run"), j["argv"]):
                counters.bump("rejected_bad_suite_argv")
                fout.write(json.dumps({"row_id": j["row_id"], "rejected": "python suite argv must start with python -s -P"}) + "\n")
                continue
            files = {k: base64.b64decode(v) for k, v in j["files"].items()}
            suite = {k: base64.b64decode(v) for k, v in (j.get("suite_files") or {}).items()} or None
            reps = REPEATS_WILL_THIS_TEST_FAIL if j.get("will_this_test_fail") else REPEATS_DEFAULT
            try:
                rr = run_repeated(j["toolchain"], files, j["argv"], kind=j.get("kind", "run"), batch=batch,
                                  row=j["row_id"], repeats=reps, manifest=man,
                                  read_back=[j["report"]] if j.get("report") else [], overlay=suite)
            except StageError as e:                        # hostile/odd path keys (`../x`, file-vs-directory clash): reject the row, keep the batch
                counters.bump("rejected_unstageable_tree")
                fout.write(json.dumps({"row_id": j["row_id"], "rejected": f"patch tree cannot be staged: {e}"}) + "\n")
                continue
            n += reps
            rec = {"row_id": j["row_id"], "deterministic": rr.deterministic, "runs": [r.brief() for r in rr.results]}
            if rr.results and rr.results[0].stripped:
                counters.bump("rows_with_stripped_patch_files")
            if not rr.deterministic:
                counters.bump("dropped_nondeterministic")      # row dropped by the caller; counted, never silent
                rec["dropped"] = True
            elif j.get("expected_ids") is not None:
                r0 = rr.results[0]
                rep = None
                try:
                    data = r0.out_files.get(j["report"], b"")
                    rep = (V.parse_go_json(data) if j["report"].endswith(".json") else V.parse_junit(data)) if data else None
                except Exception:
                    counters.bump("unparsable_report")
                v = V.compute(r0.exit_code, r0.outcome, rep, set(j["expected_ids"]))
                rec["verdict"] = {"verdict": v.verdict, "detail": v.detail}
            fout.write(json.dumps(rec) + "\n")
    man_out = {"batch": batch, "image_manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
               "runsc": man["runsc_version_line"], "kernel": platform.release(), "executions": n,
               "elapsed_s": round(time.monotonic() - t0, 1), "counters": counters.c, "pins": man["toolchains"]}
    open(out_path + ".manifest.json", "w").write(json.dumps(man_out, indent=1))
    return 0


def cleanup() -> int:
    cleanup_containers()
    # STAGE_ROOT is a tmpfs mount point (M4): empty it, never remove the directory itself
    if STAGE_ROOT.is_dir():
        for child in STAGE_ROOT.iterdir():
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="od-sbx")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("selftest"); s.add_argument("--out", required=True)
    b = sub.add_parser("run-batch"); b.add_argument("--jobs", required=True); b.add_argument("--out", required=True)
    sub.add_parser("cleanup")
    t = sub.add_parser("treehash"); t.add_argument("dir")
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        from .selftest import run_selftest
        return run_selftest(a.out)
    if a.cmd == "run-batch":
        return run_batch(a.jobs, a.out)
    if a.cmd == "cleanup":
        return cleanup()
    if a.cmd == "treehash":
        from .treehash import tree_hash
        print(tree_hash(a.dir))
        return 0
    return 1
