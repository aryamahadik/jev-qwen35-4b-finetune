"""di_rebuild.py: rebuild the Decision Index 0.3 public suite with the kit (draft ruling A61 e 2, the fallback path), into
bench/external_quarantine/decision_index_03/ (git-ignored by that folder's own .gitignore, outside data/, on the engine's QUARANTINE_OK only).
It prints counts, hashes and paths only (the kit's own JSON events: benchmark names, row counts); it never prints a row.

Why a rebuild: the suite is not redistributed (several sources forbid it) and the Hub datasets multimodalart/decision-index-suite-0.x are private
(HTTP 401), so there is no published frozen file to download and sha256-check. The kit's `suite rebuild` stops after the release-v1 rows unless they
are byte-identical to the lab's, and HLE (catalog 45, 513 requests, gated) cannot be fetched without an accepted licence, so those rows differ. This
driver therefore runs the kit's own steps WITHOUT that gate (kit modules decision_index.suite.build.rebuild / release_v2 / gsm8k_v3, unchanged):
  1. release-v1 rows of every benchmark but HLE (acquire at the pinned sources, normalize, freeze);
  2. the release-v2 cut with the kit's published subset lists and the 442-row exclusion list of the kit's hub/ folder;
  3. the seven benchmarks added in 0.2 (MMLU-Pro, BBH, When2Call, New Yorker, RAGTruth, HoVer, PhishNChips);
  4. the 0.3 GSM8K rows (gsm8k-rows.jsonl.gz).
`g13_di/di_register.py finalize` then hashes the three files, reports byte-identity against hub/0.3/manifest.json ("rebuilt" when not identical), the
per-benchmark counts and the coverage gaps (HLE only is accepted, under ruling tag A61-HLE).

  cd lean
  ../.venv/bin/python -B c2_build/g13_di/di_rebuild.py setup                 # clone the kit at the pin + a venv with the kit's [rebuild] extras (network, ~0.5 GB)
  bench/external_quarantine/decision_index_03/venv/bin/python -B c2_build/g13_di/di_rebuild.py run     # download (~7 GB) + build (needs ~17 GB free; heavy)
      options: --only N ...   release-v1 benchmarks to (re)build (default: all but 45)      --added N ...   release-v2 additions (default: all seven; [] none)
               --download-only (network + disk only)   --skip-download --skip-normalize --skip-v3      --work DIR (default <quarantine>/work)
  ../.venv/bin/python -B c2_build/g13_di/di_register.py finalize && ... export

Run it ALONE on the Mac (the G13 rule of HANDOFF.md: 16 GB; normalizers load multi-GB parquet files). Not on od-l4b, not on Modal.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # lean/c2_build/g13_di
LEAN = HERE.parents[1]
REPO = LEAN.parents[1]                                      # jev/
QROOT = REPO / "bench/external_quarantine/decision_index_03"
KIT_URL = "https://github.com/apolinario/decision-index.git"
LOGS = HERE / "logs"
HLE = 45


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pinned_commit() -> str:
    try:
        return json.loads((HERE / "kit_pin.json").read_text(encoding="utf-8"))["commit"]
    except (OSError, ValueError, KeyError):
        raise SystemExit("no g13_di/kit_pin.json: run di_register.py pin first") from None


def sh(cmd: list[str], **kw) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def cmd_setup(a) -> None:
    commit = pinned_commit()
    QROOT.mkdir(parents=True, exist_ok=True)
    repo = QROOT / "repo"
    if not (repo / ".git").is_dir():
        sh(["git", "clone", "--quiet", KIT_URL, str(repo)])
    sh(["git", "-C", str(repo), "fetch", "--quiet", "origin", commit])
    sh(["git", "-C", str(repo), "checkout", "--quiet", commit])
    got = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    if got != commit:
        raise SystemExit(f"the kit checkout is {got}, not the pinned {commit}")
    venv = QROOT / "venv"
    if not (venv / "bin/python").is_file():
        sh(["uv", "venv", "--quiet", "--python", "3.12", str(venv)])
    sh(["uv", "pip", "install", "--quiet", "--python", str(venv / "bin/python"), "-e", f"{repo}[rebuild]"])
    print(json.dumps({"kit_commit": got, "venv": str(venv.relative_to(REPO)), "python": subprocess.run(
        [str(venv / "bin/python"), "-c", "import sys, pyarrow; print(sys.version.split()[0], pyarrow.__version__)"],
        capture_output=True, text=True).stdout.strip()}))


def cmd_run(a) -> dict:
    sys.path.insert(0, str(QROOT / "repo"))
    from decision_index.suite.build import gsm8k_v3, rebuild as RB, release_v2
    from decision_index.suite.build.layout import Layout

    work = Path(a.work) if a.work else QROOT / "work"
    work.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    logf = open(LOGS / f"rebuild_{stamp}.log", "a", encoding="utf-8")

    def log(msg):
        line = msg if isinstance(msg, str) else json.dumps(msg)
        logf.write(line + "\n")
        logf.flush()
        print(line[:600], flush=True)

    numbers = sorted(a.only) if a.only else sorted(n for n in RB.BUILDERS if n != HLE)
    log({"event": "start", "utc": utc(), "work": str(work.relative_to(REPO)) if work.is_relative_to(REPO) else "(outside)", "v1_numbers": numbers,
         "hle_skipped": HLE not in numbers})
    if a.download_only:                      # network + disk only (no normalizer, no freeze): shortens the heavy run that follows with --skip-download
        from decision_index.suite.build import acquire as acq, adapters_added
        layout0 = Layout(work)
        acq.acquire(layout0, numbers, log=log)
        add_numbers = list(adapters_added.ORDER) if a.added is None else [n for n in adapters_added.ORDER if n in a.added]
        if add_numbers:
            adapters_added.acquire(layout0, add_numbers, log=log)
        log({"event": "download_only_done", "v1_numbers": numbers, "added": add_numbers})
        return {"downloaded": numbers, "added": add_numbers}
    v1 = RB.main_v1(work, only=numbers, skip_download=a.skip_download, skip_normalize=a.skip_normalize, reference=None, log=log)
    log({"event": "release_v1_done", "requests": v1.get("requests"), "byte_identical": v1.get("byte_identical"),
         "selected_rows_sha256": v1.get("selected_rows_sha256"), "expected_sha256": v1.get("expected_sha256")})
    v1_rows = Path(v1["out"]) / "selected-rows.jsonl"
    exclusions = QROOT / "repo/hub/excluded-questions.json"
    added = None if a.added is None else list(a.added)
    layout = Layout(work)
    v2 = release_v2.main(layout, v1_rows, exclusions, added=added, skip_download=a.skip_download, log=log)
    log({"event": "release_v2_done", **{k: v2.get(k) for k in ("rows", "rows_byte_identical", "added", "added_byte_identical") if k in v2}})
    gsm = None
    if not a.skip_v3:
        rows_gz = Path(v2["out"]) / "selected-rows.jsonl.gz"
        gsm = gsm8k_v3.main(Layout(work), rows_gz, log=log)
        log({"event": "release_v3_done", **{k: v for k, v in gsm.items() if k != "examples"}})
    out = {"finished_utc": utc(), "v1": {k: v1.get(k) for k in ("requests", "byte_identical", "selected_rows_sha256")},
           "v2": {k: v2.get(k) for k in ("rows", "rows_byte_identical", "added", "added_byte_identical")},
           "v3": gsm and {k: v for k, v in gsm.items() if k != "examples"}}
    (LOGS / f"rebuild_{stamp}.json").write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    log({"event": "done", "next": "di_register.py finalize, then export"})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    r = sub.add_parser("run")
    r.add_argument("--only", type=int, nargs="*")
    r.add_argument("--added", type=int, nargs="*", default=None)
    r.add_argument("--skip-download", action="store_true")
    r.add_argument("--skip-normalize", action="store_true")
    r.add_argument("--skip-v3", action="store_true")
    r.add_argument("--download-only", action="store_true", help="acquire the pinned sources only; run again with --skip-download to build")
    r.add_argument("--work")
    a = ap.parse_args(argv)
    return {"setup": cmd_setup, "run": cmd_run}[a.cmd](a)


if __name__ == "__main__":
    main()
