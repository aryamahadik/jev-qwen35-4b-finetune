"""T27 G11 fix round 2: install the staged generation (zed_orch/t27_fix_r2/gen_root/T27) into data/c2_parts/T27.
RUN ONLY AFTER THE G13 RUN HAS ENDED (it replaces data/c2_parts/T27/out and changes families/T27/plugin.py + pools_v2/, which
g13_c2.py guards). Modelled on zed_orch/w9_t32/install.py.

  ../../.venv/bin/python -B zed_orch/t27_fix_r2/install.py [--skip-code] [--allow-mixdev-change] [--dry-run]    (from c2_build)

Steps (nothing is changed before every pre-check passes):
  0. pre-checks: the staged GEN_REPORT exists and was built with the fix-round seed bases (72M / 73M / 68M); the old task folders
     are not yet superseded; mixdev_S5.jsonl is byte-identical to the installed one (else refused unless --allow-mixdev-change:
     a changed mixdev changes a G13 target);
  1. install_code.py --verify (the generator change and the new ch_next + yn_beyond wordings into families/T27; the INSTALLED code must
     rebuild the first staged candidates) unless --skip-code;
  2. data/c2_parts/T27/qc/g5h (and g3h) -> qc/_superseded_r2/, with the old GEN_REPORT / QC_REPORT / G6_A50 and a copy of the old out/;
  3. copy the staged out/ and qc/ into data/c2_parts/T27/ (never the _superseded* / _backup* folders);
  4. rewrite the VM tree prefix to the Mac path in every .md / .json / .txt, recompute each G5-H / G3-H task_sha256;
  5. A50 aggregate against data/c2_parts/T27 (B0 = the new QC build + the three builds in zed_orch/t27_fix_r2/out_a50).
"""
import argparse, hashlib, json, os, shutil, stat, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
LEAN = C2.parent
sys.path.insert(0, str(C2))
sys.path.insert(0, str(C2 / "zed_orch"))
SRC = HERE / "gen_root" / "T27"
DST = LEAN / "data" / "c2_parts" / "T27"
VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/t27_fix_r2/gen_root/T27"
STAGE_MAC = None            # the Mac staging path (localize_staging.py rewrote the VM prefix to it); default str(SRC)
BASES = {"candidates": 72_000_000, "qc": 73_000_000, "mixdev": 68_000_000}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def set_write(root: Path, on: bool) -> None:
    """chmod u+w (on) or a-w (off) on `root` and everything below it (data/c2_parts/<FAM>/out is read-only during a G13 run)."""
    for p in [root, *sorted(root.rglob("*"))]:
        m = p.stat().st_mode
        os.chmod(p, (m | stat.S_IWUSR) if on else (m & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)))


def sup() -> Path:
    return DST / "qc" / "_superseded_r2"


def installed_mixdev() -> Path | None:
    """The installed mixdev_S5.jsonl: out/ or, when the orchestrator holds it aside for a G13 batch, _hold_batch4/."""
    for p in (DST / "out" / "mixdev_S5.jsonl", DST / "_hold_batch4" / "mixdev_S5.jsonl"):
        if p.is_file():
            return p
    return None


def precheck(allow_mixdev_change: bool) -> dict:
    out = {}
    gen = SRC / "qc" / "GEN_REPORT.json"
    if not gen.is_file():
        sys.exit(f"{gen} is missing: the staged generation is not pulled")
    rep = json.loads(gen.read_text())
    seeds = rep.get("seeds") or {}
    if {k: seeds.get(k) for k in BASES} != BASES:
        sys.exit(f"staged seeds {seeds} differ from the fix-round bases {BASES}")
    if not rep.get("written"):
        sys.exit("staged GEN_REPORT says written=false")
    if sup().exists():
        sys.exit(f"{sup()} exists: already installed")
    for f in ("candidates_c2.jsonl", "candidates_c2.relations.jsonl", "MANIFEST.json", "mixdev_S5.jsonl"):
        if not (SRC / "out" / f).is_file():
            sys.exit(f"staged out/{f} is missing")
    old_mix, new_mix = installed_mixdev(), SRC / "out" / "mixdev_S5.jsonl"
    out["mixdev_installed_at"] = str(old_mix.relative_to(DST)) if old_mix else None
    out["mixdev_byte_identical"] = old_mix is not None and sha(old_mix) == sha(new_mix)
    if not out["mixdev_byte_identical"] and not allow_mixdev_change:
        sys.exit("staged mixdev_S5.jsonl differs from the installed one (a G13 target would change): "
                 "rerun with --allow-mixdev-change only if the orchestrator wants that")
    out["staged_program_pass_a50"] = rep.get("program_pass_a50")
    out["staged_program_failing_a50"] = rep.get("program_failing_a50")
    return out


def supersede():
    S = sup()
    S.mkdir(parents=True)
    for g in ("g5h", "g3h"):
        if (DST / "qc" / g).exists():
            shutil.move(str(DST / "qc" / g), str(S / g))
    for f in ("GEN_REPORT.json", "QC_REPORT.json", "G6_A50.json"):
        if (DST / "qc" / f).exists():
            shutil.copy2(DST / "qc" / f, S / f)
            if f == "G6_A50.json":
                (DST / "qc" / f).unlink()
    if (DST / "out").exists():
        shutil.copytree(DST / "out", S / "out")
    if (DST / "_hold_batch4" / "mixdev_S5.jsonl").is_file():
        shutil.copy2(DST / "_hold_batch4" / "mixdev_S5.jsonl", S / "mixdev_S5.hold_batch4.jsonl")


def copy_staged():
    hold = DST / "_hold_batch4" / "mixdev_S5.jsonl"
    for sub in ("out", "qc"):
        for p in sorted((SRC / sub).rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(SRC / sub)
            if sub == "out" and rel.name == "mixdev_S5.jsonl" and hold.is_file() and not (DST / "out" / rel.name).exists():
                if sha(p) != sha(hold):                       # held aside for a G13 batch: keep it there, not in out/
                    shutil.copy2(p, hold)
                continue
            if any(x.startswith(("_superseded", "_backup")) for x in rel.parts):
                continue
            t = DST / sub / rel
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)


def rewrite_paths() -> int:
    n = 0
    prefixes = [VMPFX, STAGE_MAC or str(SRC)]
    for p in sorted(DST.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".json", ".txt") and not any(
                x.startswith(("_superseded", "_hold", "_generated")) for x in p.relative_to(DST).parts):
            s = p.read_text(encoding="utf-8")
            if any(x in s for x in prefixes):
                for x in prefixes:
                    s = s.replace(x, str(DST))
                p.write_text(s, encoding="utf-8")
                n += 1
    for gate in ("g5h", "g3h"):
        mp = DST / "qc" / gate / "manifest.json"
        if mp.exists():
            m = json.loads(mp.read_text())
            for t in m.get("tasks", []):
                tf = Path(t["task_file"])
                if not tf.is_file() or not str(tf).startswith(str(DST)) or not str(t["answer_file"]).startswith(str(DST)):
                    sys.exit(f"{gate}: task path not on the Mac tree: {tf}")
                t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
            mp.write_text(json.dumps(m, indent=1))
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-code", action="store_true")
    ap.add_argument("--allow-mixdev-change", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-a50", action="store_true", help="tests only")
    ap.add_argument("--chmod-out", action="store_true",
                    help="data/c2_parts/T27/out is read-only (set for the G13 run): make it writable for the install and "
                         "read-only again afterwards")
    a = ap.parse_args(argv)
    rep = {"prechecks": precheck(a.allow_mixdev_change)}
    ro = (DST / "out").is_dir() and not os.access(DST / "out", os.W_OK)
    rep["prechecks"]["out_read_only"] = ro
    if ro and not a.chmod_out and not a.dry_run:
        sys.exit(f"{DST / 'out'} is read-only (kept so for the G13 run): the G13 run must have ended; rerun with --chmod-out")
    if a.dry_run:
        print(json.dumps({**rep, "dry_run": True}, indent=1))
        return rep
    if not a.skip_code:
        r = subprocess.run([sys.executable, "-B", str(HERE / "install_code.py"), "--verify"], capture_output=True, text=True)
        sys.stderr.write(r.stderr[-2000:])
        if r.returncode:
            sys.exit(f"install_code.py failed: {r.stdout[-1500:]}")
        rep["install_code"] = json.loads(r.stdout)
        if rep["install_code"].get("verify") not in ("equal", "skipped: no staged candidates yet"):
            sys.exit(f"the installed generator does not rebuild the staged candidates: {rep['install_code']}")
    if ro:
        set_write(DST / "out", True)
    supersede()
    copy_staged()
    rep["files_rewritten"] = rewrite_paths()
    if ro:
        set_write(DST / "out", False)
    if not a.skip_a50:
        import g6_a50_full as A
        A.OUTDIR = HERE / "out_a50"
        r = A.aggregate("T27")
        rep["A50"] = {"verdict": r["verdict"], "worst": r["worst_cell"], "failing": r["failing_cells"],
                      "bases": r["seed_bases"], "single": r["single_build_max_excess_pp"],
                      "program_pass_a50": r.get("program_pass_a50"), "program_failing_a50": r.get("program_failing_a50")}
    left = [str(p) for p in DST.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt", ".jsonl")
            and "_superseded" not in p.parts and "_hold_batch4" not in p.parts and "/home/aryamahadik" in
            p.read_text(encoding="utf-8", errors="replace")]
    rep["files_with_vm_path_left"] = left
    rep["n_files"] = sum(1 for p in DST.rglob("*") if p.is_file())
    print(json.dumps(rep, indent=1, default=str))
    return rep


if __name__ == "__main__":
    main()
